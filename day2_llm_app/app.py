import streamlit as st
import json
import os
import pypdf
from dotenv import load_dotenv
from templates import RESUME_ANALYSIS_PROMPT

load_dotenv()

st.set_page_config(
    page_title="Day 2 - AI Resume & Career Analyzer",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Day 2: AI Resume & Career Match Analyzer")
st.caption("Powered by Groq / OpenAI LLMs & LangChain Structured Prompt Templates")

# Sidebar Configuration & Parameters
st.sidebar.header("⚙️ Model Parameters & Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
top_p = st.sidebar.slider("Top-P", 0.1, 1.0, 0.9, 0.05)
max_tokens = st.sidebar.slider("Max Tokens", 500, 4000, 2000, 100)

# Quick Sample Loader
st.markdown("### 📥 Input Resume & Job Details")

use_sample = st.checkbox("Load Sample Resume & Job Description")

sample_resume_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_resume.txt")
sample_jd_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_jd.txt")

default_resume = ""
default_jd = ""

if use_sample and os.path.exists(sample_resume_path):
    with open(sample_resume_path, "r", encoding="utf-8") as f:
        default_resume = f.read()
if use_sample and os.path.exists(sample_jd_path):
    with open(sample_jd_path, "r", encoding="utf-8") as f:
        default_jd = f.read()

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF / TXT)", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            reader = pypdf.PdfReader(uploaded_file)
            resume_text = "\n".join([page.extract_text() for page in reader.pages])
        else:
            resume_text = uploaded_file.read().decode("utf-8")
    else:
        resume_text = st.text_area("Or Paste Resume Text", value=default_resume, height=250)

with col2:
    target_role = st.text_input("Target Job Title", value="Senior AI & LLM Systems Engineer")
    job_description = st.text_area("Target Job Description", value=default_jd, height=250)

st.divider()

if st.button("📊 Analyze Match & Generate Recommendations", type="primary", use_container_width=True):
    if not resume_text.strip() or not job_description.strip():
        st.error("Please provide both Resume and Job Description inputs.")
    elif not api_key:
        st.error("Please enter a valid API key in the sidebar.")
    else:
        with st.spinner("Analyzing resume against job requirements..."):
            try:
                formatted_prompt = RESUME_ANALYSIS_PROMPT.format(
                    resume_text=resume_text,
                    job_description=job_description,
                    target_role=target_role
                )
                
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(
                        groq_api_key=api_key,
                        model_name=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p
                    )
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(
                        openai_api_key=api_key,
                        model_name=model_name,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p
                    )
                
                response = llm.invoke(formatted_prompt)
                
                # Parse JSON
                raw_content = response.content.strip()
                if "```json" in raw_content:
                    raw_content = raw_content.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_content:
                    raw_content = raw_content.split("```")[1].split("```")[0].strip()
                
                result = json.loads(raw_content)
                
                st.success("Analysis Complete!")
                
                # Score Metric & Overview
                mcol1, mcol2 = st.columns([1, 3])
                with mcol1:
                    score = result.get("match_score", 0)
                    st.metric(label="Overall Match Score", value=f"{score}%")
                    st.progress(score / 100.0)
                with mcol2:
                    st.markdown("#### Executive Summary")
                    st.write(result.get("summary", ""))
                
                st.divider()
                
                # Skills & Strengths Breakdown
                scol1, scol2 = st.columns(2)
                with scol1:
                    st.markdown("#### ✅ Matching Skills")
                    for s in result.get("matching_skills", []):
                        st.markdown(f"- **{s}**")
                    
                    st.markdown("#### 🌟 Key Strengths")
                    for strg in result.get("key_strengths", []):
                        st.markdown(f"- {strg}")
                        
                with scol2:
                    st.markdown("#### ⚠️ Missing / Gap Skills")
                    for m in result.get("missing_skills", []):
                        st.markdown(f"- 🔴 {m}")
                    
                    st.markdown("#### 🚀 Actionable Recommendations")
                    for rec in result.get("improvement_recommendations", []):
                        st.markdown(f"- 💡 {rec}")
                
                st.divider()
                
                # Tailored Cover Letter
                st.markdown("### ✉️ Tailored Cover Letter")
                cover_letter = result.get("tailored_cover_letter", "")
                st.info(cover_letter)
                
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"Cover_Letter_{target_role.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Failed to analyze: {str(e)}")
