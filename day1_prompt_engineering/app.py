import streamlit as st
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Promptify AI - Benchmark & Studio",
    page_icon="⚡",
    layout="wide"
)

# Custom High-Aesthetic CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarUserContent"] {
        overflow-y: auto !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        max-height: 260px !important;
        overflow-y: auto !important;
    }
    .main-header {
        background: linear-gradient(135deg, #651FFF 0%, #7C4DFF 50%, #00E5FF 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(101, 31, 255, 0.25);
    }
    .main-header h1 { color: white !important; font-weight: 800; font-size: 2.2rem; margin: 0; }
    .main-header p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-right: 8px;
    }
    .badge-zero { background: rgba(255, 171, 0, 0.15); color: #FFAB00; border: 1px solid rgba(255, 171, 0, 0.3); }
    .badge-few { background: rgba(0, 229, 255, 0.15); color: #00E5FF; border: 1px solid rgba(0, 229, 255, 0.3); }
    .badge-cot { background: rgba(101, 31, 255, 0.15); color: #B388FF; border: 1px solid rgba(101, 31, 255, 0.3); }
    .badge-role { background: rgba(0, 230, 118, 0.15); color: #00E676; border: 1px solid rgba(0, 230, 118, 0.3); }
    
    .card-before {
        background: rgba(255, 235, 238, 0.5);
        border-left: 5px solid #FF5252;
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .card-after {
        background: rgba(232, 245, 233, 0.5);
        border-left: 5px solid #00E676;
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>⚡ Promptify AI Studio</h1>
    <p>Interactive Prompt Engineering Benchmark Suite — Master Zero-Shot, Few-Shot, Chain-of-Thought & Role Instructions</p>
</div>
""", unsafe_allow_html=True)

# Load dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "prompts_dataset.json")

@st.cache_data
def load_prompts():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            try:
                return json.loads(content)
            except Exception:
                return json.loads(content, strict=False)
    return []

prompts = load_prompts()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/lightning-bolt.png", width=64)
    st.header("⚙️ Model Configuration")
    
    provider = st.radio("LLM Provider", ["Groq", "OpenAI"], index=0)
    if provider == "Groq":
        model_name = st.selectbox("Model Architecture", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
        default_key = os.getenv("GROQ_API_KEY", "")
    else:
        model_name = st.selectbox("Model Architecture", ["gpt-4o-mini", "gpt-4o"])
        default_key = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input("API Key", value=default_key, type="password", help="Provided Groq or OpenAI API Key")

    st.subheader("🎛️ Hyperparameters")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05, help="Lower values = deterministic, higher = creative")
    top_p = st.slider("Top-P Nucleus", 0.1, 1.0, 0.9, 0.05)

    st.divider()
    st.header("🎯 Benchmark Selector")
    categories = ["All", "Zero-shot", "Few-shot", "Chain-of-Thought", "Role Prompting"]
    selected_category = st.selectbox("Filter Technique", categories)

if selected_category != "All":
    filtered_prompts = [p for p in prompts if p["category"] == selected_category]
else:
    filtered_prompts = prompts

prompt_titles = [f"#{p['id']} [{p['category']}] {p['title']}" for p in filtered_prompts]
selected_title = st.selectbox("📌 Select Benchmark Scenario", prompt_titles)

selected_id = int(selected_title.split(" ")[0].replace("#", ""))
item = next(p for p in prompts if p["id"] == selected_id)

# Metrics Banner
mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1.metric("Benchmark ID", f"#{item['id']}")
mcol2.metric("Technique Category", item['category'])
mcol3.metric("Prompts Evaluated", f"{len(prompts)} Total")
mcol4.metric("Provider Engine", provider)

st.markdown(f"**Goal & Scenario**: {item['description']}")
st.divider()

# Side by Side Comparison
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ Naive (Before) Prompt")
    st.markdown(f"<div class='card-before'><b>Prompt Input:</b><br>{item['naive_prompt']}</div>", unsafe_allow_html=True)
    st.markdown("#### 🔴 Raw Baseline LLM Output")
    st.error(item["before_output"])

with col2:
    st.markdown("### ✅ Engineered (After) Prompt")
    st.markdown(f"<div class='card-after'><b>Engineered Prompt:</b><br>{item['engineered_prompt']}</div>", unsafe_allow_html=True)
    st.markdown("#### 🟢 Optimized LLM Output")
    st.code(item["after_output"], language="markdown" if "{" not in item["after_output"] else "json")

st.divider()

# Live Studio Lab
st.markdown("### 🧪 Live Prompt Studio Laboratory")
st.caption("Edit the input context below and test live model inference with your engineered prompt template.")

user_custom_input = st.text_area("Live Input Context", value=item["input_text"], height=110)

if st.button("🚀 Execute Engineered Prompt Live", type="primary"):
    if not api_key.strip():
        st.error("⚠️ Please provide a valid API key in the sidebar on the left.")
    else:
        try:
            start_time = time.time()
            with st.spinner("⚡ Running live inference engine..."):
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=temperature, top_p=top_p)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=temperature)

                full_prompt = f"{item['engineered_prompt']}\n\n[INPUT DATA]:\n{user_custom_input}"
                response = llm.invoke(full_prompt)
                elapsed = time.time() - start_time
                
                st.success(f"✨ Inference Complete in {elapsed:.2f} seconds!")
                
                res_col1, res_col2 = st.columns([3, 1])
                with res_col1:
                    st.markdown("#### 🌟 Live Model Response")
                    st.write(response.content)
                with res_col2:
                    st.markdown("#### 📊 Execution Metrics")
                    st.info(f"**Tokens Approx**: {len(response.content.split()) * 1.3:.0f}\n\n**Latency**: {elapsed:.2f}s\n\n**Model**: {model_name}")
        except Exception as e:
            st.error(f"❌ Execution Error: {str(e)}")
