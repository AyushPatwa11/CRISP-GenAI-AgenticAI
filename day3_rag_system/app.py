import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from rag_engine import RAGEngine

load_dotenv()

st.set_page_config(
    page_title="Day 3 - RAG PDF Knowledge Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Day 3: RAG PDF Knowledge Chatbot")
st.caption("Powered by LangChain, HuggingFace Embeddings, ChromaDB & Groq/OpenAI LLMs")

# Initialize session state for RAG engine and chat history
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Sidebar Configuration
st.sidebar.header("⚙️ RAG & Model Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")

chunk_size = st.sidebar.slider("Chunk Size (chars)", 200, 2000, 1000, 100)
chunk_overlap = st.sidebar.slider("Chunk Overlap", 0, 500, 200, 50)
top_k = st.sidebar.slider("Retrieved Chunks (k)", 1, 6, 3)

st.sidebar.divider()
st.sidebar.header("📂 Document Ingestion")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT Documents",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

use_sample_doc = st.sidebar.button("📄 Load Sample CRISP Handbook Document")

temp_files_to_process = []

if use_sample_doc:
    sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "ai_handbook_summary.txt")
    if os.path.exists(sample_path):
        temp_files_to_process.append(sample_path)

if uploaded_files:
    for file in uploaded_files:
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, file.name)
        with open(temp_path, "wb") as f:
            f.write(file.read())
        temp_files_to_process.append(temp_path)

if temp_files_to_process:
    if st.sidebar.button("⚡ Index Documents in ChromaDB", type="primary"):
        with st.spinner("Processing & embedding documents into ChromaDB..."):
            try:
                st.session_state.rag_engine.chunk_size = chunk_size
                st.session_state.rag_engine.chunk_overlap = chunk_overlap
                num_docs, num_chunks = st.session_state.rag_engine.process_documents(temp_files_to_process)
                st.session_state.indexed = True
                st.sidebar.success(f"Indexed {num_docs} document(s) into {num_chunks} vector chunks!")
            except Exception as e:
                st.sidebar.error(f"Error indexing docs: {str(e)}")

# Display Vector Store Status
if st.session_state.rag_engine.load_existing_db():
    st.session_state.indexed = True

if st.session_state.indexed:
    st.info("🟢 Vector DB Status: Active & Indexed in ChromaDB.")
else:
    st.warning("⚠️ Vector DB Status: Empty. Upload a document or click 'Load Sample Document' in the sidebar.")

st.divider()

# Chat Interface
st.markdown("### 💬 Conversational QA with Document Citations")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("📍 View Retrieved Source Citations"):
                for idx, src in enumerate(msg["sources"], 1):
                    st.markdown(f"**[{idx}] Source:** `{src['source']}` | **Page:** `{src['page']}`")
                    st.caption(f"\"{src['content']}\"")

user_query = st.chat_input("Ask a question about your uploaded documents...")

if user_query:
    if not st.session_state.indexed:
        st.error("Please load and index at least one document before asking questions.")
    elif not api_key:
        st.error("Please enter your API Key in the sidebar.")
    else:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # Generate RAG response
        with st.chat_message("assistant"):
            with st.spinner("Retrieving vector chunks & generating answer..."):
                try:
                    if provider == "Groq":
                        from langchain_groq import ChatGroq
                        llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                    else:
                        from langchain_openai import ChatOpenAI
                        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                    res = st.session_state.rag_engine.query(user_query, llm=llm, k=top_k)
                    
                    st.write(res["answer"])
                    
                    if res["sources"]:
                        with st.expander("📍 View Retrieved Source Citations"):
                            for idx, src in enumerate(res["sources"], 1):
                                st.markdown(f"**[{idx}] Source:** `{src['source']}` | **Page:** `{src['page']}`")
                                st.caption(f"\"{src['content']}\"")
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": res["answer"],
                        "sources": res["sources"]
                    })
                except Exception as e:
                    st.error(f"Error querying RAG system: {str(e)}")
