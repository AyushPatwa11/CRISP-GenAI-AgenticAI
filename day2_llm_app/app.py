import streamlit as st
import json
import os
import pypdf
from dotenv import load_dotenv
from templates import RESUME_ANALYSIS_PROMPT

load_dotenv()

st.set_page_config(
    page_title="CareerVibe AI - Executive Match Engine",
    page_icon="💼",
    layout="wide"
)

# Custom High-Aesthetic Corporate HR CSS
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        overflow-y: auto !important;
    }
    .header-box {
        background: linear-gradient(135deg, #1A237E 0%, #303F9F 50%, #00C853 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(26, 35, 126, 0.25);
    }
    .header-box h1 { color: white !important; font-weight: 800; font-size: 2.2rem; margin: 0; }
    .header-box p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .score-card {
        background: linear-gradient(135deg, #F5F7FA 0%, #E4E7EB 100%);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #CFD8DC;
    }
    .score-title { font-size: 1.1rem; color: #37474F; font-weight: 600; }
    .score-val { font-size: 3rem; font-weight: 800; color: #1A237E; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>💼 CareerVibe AI Engine</h1>
    <p>Executive Resume & Job Description Matcher — Automated ATS Skill Gap Audit & Custom Cover Letter Generator</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/briefcase.png", width=64)
    st.header("⚙️ Model Parameters")
    
    provider = st.radio("Select Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"])
        default_key = os.getenv("GROQ_API_KEY", "")
    else:
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
        default_key = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input("API Key", value=default_key, type="password")

    st.subheader("🎛️ Hyperparameters")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    top_p = st.slider("Top-P", 0.1, 1.0, 0.9, 0.05)
    max_tokens = st.slider("Max Tokens", 500, 4000, 2000, 100)

# Main Form Inputs
st.markdown("### 📥 Document Upload & Role Inputs")

use_sample = st.checkbox("💡 Load Preset Sample Resume & Job Description (Senior AI Engineer)")

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
    st.markdown("#### 📄 Candidate Resume")
    uploaded_file = st.file_uploader("Upload PDF or TXT Document", type=["pdf", "txt"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            reader = pypdf.PdfReader(uploaded_file)
            resume_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        else:
            resume_text = uploaded_file.read().decode("utf-8")
    else:
        resume_text = st.text_area("Or Paste Candidate Resume Text", value=default_resume, height=220)

with col2:
    target_role = st.text_input("Target Job Title", value="Senior AI & LLM Systems Engineer")
    job_description = st.text_area("Target Job Description (JD)", value=default_jd, height=220)

st.divider()

if st.button("📊 Execute Executive Career Audit", type="primary", use_container_width=True):
    if not resume_text.strip() or not job_description.strip():
        st.error("⚠️ Please provide both Candidate Resume and Job Description inputs.")
    elif not api_key:
        st.error("⚠️ Please enter a valid API key in the sidebar.")
    else:
        with st.spinner("⚡ Running LangChain prompt template & Pydantic parser..."):
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
                        max_tokens=max_tokens
                    )
                
                response = llm.invoke(formatted_prompt)
                content = response.content.strip()
                
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                    
                result = json.loads(content)
                
                # Results Dashboard
                st.markdown("### 🌟 Executive Career Analysis Report")
                
                rcol1, rcol2, rcol3 = st.columns([1, 1, 1])
                
                match_pct = result.get('match_percentage', 0)
                rcol1.metric("Overall Match Score", f"{match_pct}%", delta=f"{match_pct-50}% vs Avg")
                rcol2.metric("Target Role", target_role)
                rcol3.metric("Parsing Status", "Pydantic Verified")
                
                st.progress(min(match_pct / 100.0, 1.0))
                
                st.divider()
                
                bcol1, bcol2 = st.columns(2)
                
                with bcol1:
                    st.markdown("#### ✅ Matched Core Skills")
                    for skill in result.get("matched_skills", []):
                        st.success(f"✔️ {skill}")
                        
                    st.markdown("#### ❌ Missing Critical Skills")
                    for skill in result.get("missing_skills", []):
                        st.error(f"⚠️ {skill}")
                        
                with bcol2:
                    st.markdown("#### 📝 Recommended Resume Edits")
                    for rec in result.get("recommendations", []):
                        st.info(f"💡 {rec}")
                        
                st.divider()
                
                st.markdown("#### ✉️ Tailored Executive Cover Letter")
                cover_letter = result.get("cover_letter", "Not generated.")
                st.text_area("Generated Cover Letter", value=cover_letter, height=220)
                
                st.download_button(
                    label="📥 Download Cover Letter (.txt)",
                    data=cover_letter,
                    file_name=f"Cover_Letter_{target_role.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"❌ Analysis Error: {str(e)}")
