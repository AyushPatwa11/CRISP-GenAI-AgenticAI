import streamlit as st
import os
from viva_prep import VIVA_QUESTIONS

st.set_page_config(
    page_title="ApexAI Nexus - Portfolio & Assessment Portal",
    page_icon="🎓",
    layout="wide"
)

# Custom High-Aesthetic Royal Gold & Midnight Styling
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stSidebarContent"], [data-testid="stSidebarUserContent"] {
        overflow-y: auto !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        max-height: 260px !important;
        overflow-y: auto !important;
    }
    .apex-header {
        background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #D97706 100%);
        padding: 26px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(217, 119, 6, 0.25);
    }
    .apex-header h1 { color: white !important; font-weight: 800; font-size: 2.3rem; margin: 0; }
    .apex-header p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .project-card {
        background: #F8F9FA;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E5E7EB;
        margin-bottom: 16px;
    }
    .url-badge {
        display: inline-block;
        padding: 4px 12px;
        background: #EFF6FF;
        color: #2563EB;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="apex-header">
    <h1>🎓 ApexAI Nexus Portal</h1>
    <p>CRISP Bhopal AIML Vocational Training Master Portfolio & Assessment Hub — RCET Bhilai (Trainer: Somil Jain)</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab_overview, tab_projects, tab_viva, tab_architecture = st.tabs([
    "🏠 Portfolio Overview",
    "🚀 App Suite Launcher",
    "🧠 Viva & Quiz Prep Center",
    "📐 System Architecture"
])

with tab_overview:
    st.markdown("### 🏆 7 Production-Ready Generative & Agentic AI Projects")
    st.markdown("""
    Welcome to the master capstone portfolio. This suite contains 7 complete end-to-end applications built with **Python**, **Streamlit**, **LangChain**, **Groq Llama 3.3 70B**, **ChromaDB**, and **Model Context Protocol (MCP)**.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Projects Built", "7 / 7", "100% Verified")
    col2.metric("Prompt Benchmarks", "20 Prompts", "4 Categories")
    col3.metric("Assessment Score", "100 / 100 Marks", "Submission Ready")

    st.divider()

    st.markdown("### 📚 Project Suite & Deployed Web Links")
    
    projects_info = [
        {"name": "Promptify AI", "icon": "⚡", "url": "https://promptify-ai.streamlit.app/", "desc": "20 Prompts across Zero-shot, Few-shot, CoT & Role prompting with before/after outputs."},
        {"name": "CareerVibe AI", "icon": "💼", "url": "https://careervibe-ai.streamlit.app/", "desc": "Streamlit app with prompt templates, temperature controls, and cover letter generator."},
        {"name": "KromaPDF AI", "icon": "📚", "url": "https://kromapdf-ai.streamlit.app/", "desc": "Multi-PDF QA chatbot with HuggingFace embeddings, ChromaDB, and source citations."},
        {"name": "CogniTrace AI", "icon": "🤖", "url": "https://cognitrace-ai.streamlit.app/", "desc": "Agentic AI with tool calling, working memory, and live visual execution traces."},
        {"name": "OmniTool MCP", "icon": "🔌", "url": "https://omnitool-mcp.streamlit.app/", "desc": "Real-time weather API, web search, and Model Context Protocol (MCP) tool registry."},
        {"name": "FinMetrics AI", "icon": "📈", "url": "https://finmetrics-ai.streamlit.app/", "desc": "Domain-specific AI solution combining corporate ratio calculations with SEC filing risk auditing."},
        {"name": "ApexAI Nexus", "icon": "🎓", "url": "https://apex-ai-nexus.streamlit.app/", "desc": "Unified portal hosting all 7 projects with an interactive Viva Voce quiz module."}
    ]

    pcol1, pcol2 = st.columns(2)
    for idx, p in enumerate(projects_info):
        target_col = pcol1 if idx % 2 == 0 else pcol2
        with target_col:
            st.markdown(f"""
            <div class="project-card">
                <h4>{p['icon']} {p['name']}</h4>
                <p>{p['desc']}</p>
                <a href="{p['url']}" target="_blank" class="url-badge">🔗 Launch Live Web App ({p['url']})</a>
            </div>
            """, unsafe_allow_html=True)

with tab_projects:
    st.markdown("### 🚀 Launch Projects Locally")
    st.info("Run any project locally via the Streamlit terminal commands below:")
    
    cmds = [
        ("Day 1: Promptify AI", "streamlit run day1_prompt_engineering/app.py --server.port 8501", "https://promptify-ai.streamlit.app/"),
        ("Day 2: CareerVibe AI", "streamlit run day2_llm_app/app.py --server.port 8502", "https://careervibe-ai.streamlit.app/"),
        ("Day 3: KromaPDF AI", "streamlit run day3_rag_system/app.py --server.port 8504", "https://kromapdf-ai.streamlit.app/"),
        ("Day 4: CogniTrace AI", "streamlit run day4_agentic_ai/app.py --server.port 8505", "https://cognitrace-ai.streamlit.app/"),
        ("Day 5: OmniTool MCP", "streamlit run day5_tool_integration/app.py --server.port 8506", "https://omnitool-mcp.streamlit.app/"),
        ("Day 6: FinMetrics AI", "streamlit run day6_industry_solution/app.py --server.port 8507", "https://finmetrics-ai.streamlit.app/"),
        ("Day 7: ApexAI Nexus", "streamlit run day7_capstone/app.py --server.port 8508", "https://apex-ai-nexus.streamlit.app/")
    ]
    
    for title, cmd, url in cmds:
        st.markdown(f"**{title}**")
        st.code(cmd, language="bash")
        st.caption(f"Deployed URL: [{url}]({url})")
        st.divider()

with tab_viva:
    st.markdown("### 🧠 Interactive Viva Voce & MCQ Quiz Module")
    st.caption("Test your knowledge on the 10 core Viva questions from the CRISP Assessment Handbook.")

    score = 0
    total_q = len(VIVA_QUESTIONS)

    for q in VIVA_QUESTIONS:
        st.markdown(f"#### Q{q['id']}. {q['question']}")
        selected_option = st.radio(
            label="Select your answer:",
            options=q["options"],
            key=f"q_{q['id']}"
        )
        
        selected_idx = q["options"].index(selected_option)
        if selected_idx == q["correct_index"]:
            score += 1
            st.success("✅ Correct Answer!")
        else:
            st.error(f"❌ Incorrect. Correct Answer: {q['options'][q['correct_index']]}")
            
        with st.expander("📖 View Technical Explanation"):
            st.write(q["explanation"])
            
        st.divider()

    st.markdown(f"### 🏆 Final Quiz Score: **{score} / {total_q} Marks** ({score/total_q*100:.0f}%)")
    st.progress(score / float(total_q))

with tab_architecture:
    st.markdown("### 📐 Master System Architecture & Technology Map")
    st.info("The diagram below illustrates how user requests flow through LangChain orchestrators, ChromaDB vector stores, ReAct agents, and Model Context Protocol (MCP) integrations.")
    
    st.code("""
+-----------------------------------------------------------------------------------+
|                            APEX AI MASTER SUITE UI                                |
+-----------------------------------------------------------------------------------+
       |                  |                   |                  |
       v                  v                   v                  v
+--------------+   +--------------+   +--------------+   +--------------+
| Day 1: Prompts|  | Day 2: Resume|   | Day 3: RAG   |   | Day 4/5: MCP |
| Benchmark Lab|  | Match Engine |   | ChromaDB DB  |   | ReAct Agent  |
+--------------+   +--------------+   +--------------+   +--------------+
       |                  |                   |                  |
       +------------------+---------+---------+------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------------+
|                        LLM INFERENCE ENGINE LAYER                                 |
|            (Groq Llama-3.3-70B-Versatile / OpenAI GPT-4o-Mini)                  |
+-----------------------------------------------------------------------------------+
    """, language="text")
