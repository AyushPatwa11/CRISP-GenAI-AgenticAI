import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from rag_engine import RAGEngine

load_dotenv()

st.set_page_config(
    page_title="KromaPDF AI - RAG Vector Engine",
    page_icon="📚",
    layout="wide"
)

# Custom High-Aesthetic Deep Indigo Styling
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarUserContent"] {
        overflow-y: auto !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        max-height: 260px !important;
        overflow-y: auto !important;
    }
    .rag-header {
        background: linear-gradient(135deg, #1A237E 0%, #3F51B5 50%, #00BCD4 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(26, 35, 126, 0.25);
    }
    .rag-header h1 { color: white !important; font-weight: 800; font-size: 2.2rem; margin: 0; }
    .rag-header p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .status-badge-active {
        background: rgba(0, 230, 118, 0.15);
        color: #00E676;
        border: 1px solid #00E676;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 600;
    }
    .status-badge-idle {
        background: rgba(255, 171, 0, 0.15);
        color: #FFAB00;
        border: 1px solid #FFAB00;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 600;
    }
    
    .citation-card {
        background: #F8F9FA;
        border-left: 4px solid #3F51B5;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 6px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rag-header">
    <h1>📚 KromaPDF AI Knowledge Engine</h1>
    <p>Multi-PDF Vector Search & Retrieval-Augmented Generation — Powered by Ephemeral ChromaDB & HuggingFace Embeddings</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = RAGEngine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False

if "active_doc_name" not in st.session_state:
    st.session_state.active_doc_name = ""

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/books.png", width=64)
    st.header("⚙️ RAG & Model Settings")
    
    provider = st.radio("Select Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        default_key = os.getenv("GROQ_API_KEY", "")
    else:
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
        default_key = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input("API Key", value=default_key, type="password")

    st.subheader("🎛️ Vector Chunking Parameters")
    chunk_size = st.slider("Chunk Size (chars)", 200, 2000, 1000, 100)
    chunk_overlap = st.slider("Chunk Overlap", 0, 500, 200, 50)
    top_k = st.slider("Retrieved Chunks (k)", 1, 6, 3)

    st.divider()
    st.header("📂 Knowledge Ingestion")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT Documents",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    use_sample_doc = st.button("💡 Load Sample CRISP Handbook Document")

    if "temp_files_to_process" not in st.session_state:
        st.session_state.temp_files_to_process = []

    if use_sample_doc:
        sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "ai_handbook_summary.txt")
        if os.path.exists(sample_path):
            st.session_state.temp_files_to_process = [sample_path]
            st.session_state.active_doc_name = "Sample CRISP Handbook Document"
            st.session_state.indexed = False

    if uploaded_files:
        names_str = ", ".join([f.name for f in uploaded_files])
        if st.session_state.active_doc_name != names_str:
            uploaded_paths = []
            for file in uploaded_files:
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                uploaded_paths.append(temp_path)
            st.session_state.temp_files_to_process = uploaded_paths
            st.session_state.active_doc_name = names_str
            st.session_state.indexed = False

    if st.session_state.temp_files_to_process:
        st.info(f"📄 Selected Document: **{st.session_state.active_doc_name}**")
        if st.button("⚡ Index Documents in ChromaDB", type="primary"):
            with st.spinner("Processing & embedding documents into ChromaDB..."):
                try:
                    st.session_state.rag_engine.chunk_size = chunk_size
                    st.session_state.rag_engine.chunk_overlap = chunk_overlap
                    num_docs, num_chunks = st.session_state.rag_engine.process_documents(st.session_state.temp_files_to_process)
                    st.session_state.indexed = True
                    st.session_state.chat_history = []
                    st.success(f"Indexed {num_docs} document(s) into {num_chunks} vector chunks!")
                except Exception as e:
                    st.error(f"Error indexing docs: {str(e)}")

    st.divider()
    if st.button("🗑️ Reset Vector DB & Chat"):
        st.session_state.rag_engine.clear_vector_store()
        st.session_state.indexed = False
        st.session_state.chat_history = []
        st.success("Vector DB Cleared!")

# Main Status Bar
col_status1, col_status2, col_status3 = st.columns(3)
with col_status1:
    if st.session_state.indexed:
        st.markdown("<span class='status-badge-active'>🟢 Index Status: Ready</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='status-badge-idle'>🟡 Index Status: Awaiting Ingestion</span>", unsafe_allow_html=True)
with col_status2:
    st.metric("Active Document", st.session_state.active_doc_name if st.session_state.active_doc_name else "None Loaded")
with col_status3:
    st.metric("Top-K Retrieval", f"{top_k} Chunks")

st.divider()

# Chat Interface
st.markdown("### 💬 Conversational Document Q&A")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("📚 View Cited Document Excerpts"):
                for idx, src in enumerate(message["sources"], 1):
                    st.markdown(f"**Citation #{idx}** (Page {src.get('page', 'N/A')}):")
                    st.markdown(f"<div class='citation-card'>{src.get('text', '')}</div>", unsafe_allow_html=True)

user_query = st.chat_input("Ask a question about your indexed PDF documents...")

if user_query:
    if not st.session_state.indexed:
        st.error("⚠️ Please upload and click 'Index Documents in ChromaDB' first in the sidebar.")
    elif not api_key.strip():
        st.error("⚠️ Please enter a valid API key in the sidebar.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Searching ChromaDB vector store & synthesizing answer..."):
                try:
                    if provider == "Groq":
                        from langchain_groq import ChatGroq
                        llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                    else:
                        from langchain_openai import ChatOpenAI
                        llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                    answer, sources = st.session_state.rag_engine.query(
                        user_query,
                        llm=llm,
                        top_k=top_k
                    )

                    st.markdown(answer)

                    if sources:
                        with st.expander("📚 View Cited Document Excerpts"):
                            for idx, src in enumerate(sources, 1):
                                st.markdown(f"**Citation #{idx}** (Page {src.get('page', 'N/A')}):")
                                st.markdown(f"<div class='citation-card'>{src.get('text', '')}</div>", unsafe_allow_html=True)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except Exception as e:
                    st.error(f"❌ Query Error: {str(e)}")
