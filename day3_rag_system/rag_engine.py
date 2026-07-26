import os
import shutil
from typing import List, Dict, Any, Tuple

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

_cached_embeddings = None

def get_embeddings():
    global _cached_embeddings
    if _cached_embeddings is None:
        try:
            import streamlit as st
            @st.cache_resource
            def load_hf_model():
                from langchain_community.embeddings import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
            _cached_embeddings = load_hf_model()
        except Exception:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            _cached_embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
    return _cached_embeddings


class RAGEngine:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vector_store = None

    @property
    def embeddings(self):
        return get_embeddings()

    def clear_vector_store(self):
        self.vector_store = None
        if os.path.exists(DB_DIR):
            try:
                shutil.rmtree(DB_DIR, ignore_errors=True)
            except Exception:
                pass

    def process_documents(self, file_paths: List[str]) -> Tuple[int, int]:
        """Loads PDFs/TXT files, splits into chunks, and creates a fresh vector database."""
        docs = []
        for file_path in file_paths:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                loaded_docs = loader.load()
                docs.extend(loaded_docs)
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                loaded_docs = loader.load()
                docs.extend(loaded_docs)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(docs)

        # Create fresh vector store containing ONLY newly processed documents
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings
        )
        return len(docs), len(chunks)

    def query(self, question: str, llm: Any, k: int = 3) -> Dict[str, Any]:
        """Performs RAG search and generates response with cited sources."""
        if not self.vector_store:
            raise ValueError("No indexed vector store found. Please process documents first.")

        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        retrieved_docs = retriever.invoke(question)

        prompt_template = """You are a helpful AI Assistant answering questions based strictly on the retrieved context below.
If the context does not contain enough information, state that clearly. Do not invent facts.

--- RETRIEVED CONTEXT ---
{context}

--- USER QUESTION ---
{question}

--- INSTRUCTIONS ---
Answer the question concisely and cite relevant page numbers or sources if available.
"""
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        context_text = "\n\n".join([f"[Source: {d.metadata.get('source', 'doc')} | Page: {d.metadata.get('page', 0)+1}]\n{d.page_content}" for d in retrieved_docs])
        
        chain = prompt | llm | StrOutputParser()
        response_text = chain.invoke({"context": context_text, "question": question})

        sources = []
        for d in retrieved_docs:
            sources.append({
                "source": os.path.basename(d.metadata.get("source", "Document")),
                "page": d.metadata.get("page", 0) + 1,
                "content": d.page_content[:250] + "..."
            })

        return {
            "answer": response_text,
            "sources": sources,
            "context_used": context_text
        }
