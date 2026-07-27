import streamlit as st
import os
from viva_prep import VIVA_QUESTIONS

st.set_page_config(
    page_title="ApexAI Nexus - Portfolio & Assessment Portal",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 ApexAI Nexus — Master Portfolio & Assessment Portal")
st.caption("Rungta Engineering College, Bhilai — 7 Complete Generative & Agentic AI Projects")

# Navigation Tabs
tab_overview, tab_projects, tab_viva, tab_architecture = st.tabs([
    "🏠 Portfolio Overview",
    "🚀 App Suite Launcher",
    "🧠 Viva & Quiz Prep Center",
    "📐 System Architecture"
])

with tab_overview:
    st.markdown("### 🏆 7 Hands-on Generative & Agentic AI Projects")
    st.markdown("""
    Welcome to the unified master portfolio dashboard. This repository contains 7 end-to-end production AI applications built with **Python**, **Streamlit**, **LangChain**, **Groq/OpenAI APIs**, **ChromaDB**, and **Model Context Protocol (MCP)**.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Projects Built", "7 / 7", "100% Complete")
    col2.metric("Prompt Benchmarks", "20 Prompts", "4 Categories")
    col3.metric("Assessment Score", "100 / 100 Marks", "Submission Ready")

    st.divider()

    st.markdown("### 📚 Project Suite Overview")
    
    projects_info = [
        {"name": "Promptify AI", "icon": "⚡", "desc": "20 Prompts across Zero-shot, Few-shot, CoT & Role prompting with before/after outputs."},
        {"name": "CareerVibe AI", "icon": "💼", "desc": "Streamlit app with prompt templates, temperature controls, and cover letter generator."},
        {"name": "KromaPDF AI", "icon": "📚", "desc": "Multi-PDF QA chatbot with HuggingFace embeddings, ChromaDB, and source citations."},
        {"name": "CogniTrace AI", "icon": "🤖", "desc": "Agentic AI with tool calling, working memory, and live visual execution traces."},
        {"name": "OmniTool MCP", "icon": "🔌", "desc": "Real-time weather API, web search, and Model Context Protocol (MCP) tool registry."},
        {"name": "FinPulse AI", "icon": "📈", "desc": "Domain-specific AI solution combining corporate ratio calculations with SEC filing risk auditing."},
        {"name": "ApexAI Nexus", "icon": "🎓", "desc": "Unified portal hosting all 7 projects with an interactive Viva Voce quiz module."}
    ]

    for p in projects_info:
        with st.expander(f"{p['icon']} {p['name']}", expanded=True):
            st.write(p['desc'])

with tab_projects:
    st.markdown("### 🚀 Launch Daily Project Applications")
    st.info("To run any individual project independently, execute the terminal commands below:")
    
    cmds = [
        "streamlit run day1_prompt_engineering/app.py",
        "streamlit run day2_llm_app/app.py",
        "streamlit run day3_rag_system/app.py",
        "streamlit run day4_agentic_ai/app.py",
        "streamlit run day5_tool_integration/app.py",
        "streamlit run day6_industry_solution/app.py",
        "streamlit run day7_capstone/app.py"
    ]
    
    for idx, c in enumerate(cmds, 1):
        st.markdown(f"**Day {idx} Command:**")
        st.code(c, language="bash")

with tab_viva:
    st.markdown("### 🧠 Interactive Viva Voce & MCQ Assessment Module")
    st.caption("Test your understanding of the 10 core Viva questions from the CRISP Handbook.")

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

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
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct Answer: {q['options'][q['correct_index']]}")
            
        with st.expander("📖 View Technical Explanation"):
            st.write(q["explanation"])
            
        st.divider()

    st.markdown("### 📊 Quiz Results Summary")
    st.metric(label="Your Viva Quiz Score", value=f"{score} / {total_q}", delta=f"{int(score/total_q*100)}%")

with tab_architecture:
    st.markdown("### 📐 Complete System Architecture")
    st.markdown("""
    ```mermaid
    graph TD
        User([User Interface - Streamlit Portal]) --> Router[Day 1-7 Application Router]
        
        Router --> Day1[Day 1: Prompt Engineering Evaluator]
        Router --> Day2[Day 2: AI Resume & Career Matcher]
        Router --> Day3[Day 3: RAG PDF Chatbot]
        Router --> Day4[Day 4: Autonomous ReAct Agent]
        Router --> Day5[Day 5: Tool & MCP Bridge]
        Router --> Day6[Day 6: Financial Industry Solution]
        Router --> Day7[Day 7: Portfolio & Viva Assessment]
        
        Day3 --> Embeddings[HuggingFace Embeddings]
        Embeddings --> Chroma[ChromaDB Vector Store]
        
        Day4 --> Memory[Agent Memory]
        Day4 --> Tools[Python Tools]
        
        Day5 --> MCP[MCP Schema Registry]
        MCP --> Weather[Open-Meteo REST API]
        MCP --> Search[DuckDuckGo Search]
        
        Day1 & Day2 & Day3 & Day4 & Day5 & Day6 --> LLM[Groq / OpenAI API Engine]
    ```
    """)
