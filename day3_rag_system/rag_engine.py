import os
import shutil
from typing import List, Dict, Any, Tuple

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

class RAGEngine:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Use lightweight CPU sentence-transformer model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None

    def clear_vector_store(self):
        if os.path.exists(DB_DIR):
            shutil.rmtree(DB_DIR, ignore_errors=True)

    def process_documents(self, file_paths: List[str]) -> Tuple[int, int]:
        """Loads PDFs/TXT files, splits into chunks, and indexes into ChromaDB."""
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

        # Clear previous vector store for fresh session
        self.clear_vector_store()

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=DB_DIR
        )
        return len(docs), len(chunks)

    def load_existing_db(self) -> bool:
        if os.path.exists(DB_DIR) and len(os.listdir(DB_DIR)) > 0:
            self.vector_store = Chroma(
                persist_directory=DB_DIR,
                embedding_function=self.embeddings
            )
            return True
        return False

    def query(self, question: str, llm: Any, k: int = 3) -> Dict[str, Any]:
        """Performs RAG search and generates response with cited sources."""
        if not self.vector_store:
            self.load_existing_db()

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
