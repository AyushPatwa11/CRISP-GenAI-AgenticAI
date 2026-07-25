import streamlit as st
import json
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Promptify AI - Interactive Benchmark Lab",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Promptify AI — Interactive Prompt Engineering Lab")
st.caption("Explore 20 Mastered Prompts across Zero-shot, Few-shot, Chain-of-Thought, and Role Prompting techniques.")

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

# Sidebar Configuration
st.sidebar.header("⚙️ Model & API Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password", help="Enter your Groq or OpenAI API Key here")

st.sidebar.divider()
st.sidebar.header("🎯 Prompt Navigator")
categories = ["All", "Zero-shot", "Few-shot", "Chain-of-Thought", "Role Prompting"]
selected_category = st.sidebar.selectbox("Filter by Category", categories)

if selected_category != "All":
    filtered_prompts = [p for p in prompts if p["category"] == selected_category]
else:
    filtered_prompts = prompts

prompt_titles = [f"#{p['id']} [{p['category']}] {p['title']}" for p in filtered_prompts]
selected_title = st.sidebar.selectbox("Select Prompt Benchmark", prompt_titles)

# Selected prompt object
selected_id = int(selected_title.split(" ")[0].replace("#", ""))
item = next(p for p in prompts if p["id"] == selected_id)

st.subheader(f"📌 #{item['id']}: {item['title']}")
st.markdown(f"**Category:** `{item['category']}` | **Goal:** {item['description']}")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ Naive (Before) Prompt")
    st.info(item["naive_prompt"])
    st.markdown("#### 🔴 Raw LLM Output")
    st.error(item["before_output"])

with col2:
    st.markdown("### ✅ Engineered (After) Prompt")
    st.success(item["engineered_prompt"])
    st.markdown("#### 🟢 Optimized LLM Output")
    st.code(item["after_output"], language="markdown" if "{" not in item["after_output"] else "json")

st.divider()

# Live Playground
st.subheader("🧪 Live Interactive Execution & Comparison")
user_custom_input = st.text_area("Input Text / Context", value=item["input_text"], height=100)

if st.button("🚀 Execute Engineered Prompt Live", type="primary"):
    if not api_key.strip():
        st.warning("⚠️ Please enter your API Key in the sidebar on the left.")
    else:
        try:
            with st.spinner("Generating live response..."):
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.2)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.2)
                
                prompt_to_send = item["engineered_prompt"].replace(item["input_text"], user_custom_input)
                response = llm.invoke(prompt_to_send)
                st.markdown("### 🌟 Live Execution Result")
                st.write(response.content)
        except Exception as e:
            st.error(f"Error during execution: {str(e)}")

# Summary Metrics Footer
st.sidebar.divider()
st.sidebar.metric(label="Total Prompts Evaluated", value=len(prompts))
st.sidebar.metric(label="Categories Covered", value="4 / 4")
