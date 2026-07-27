# 🤖 Generative & Agentic AI — 7-Day Project Portfolio Suite
### *CRISP Bhopal Vocational Training Assignment | Venue: Rungta College of Engineering and Technology (RCET), Bhilai*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5+-FF6F61?style=for-the-badge&logo=sqlite&logoColor=white)](https://trychroma.com)
[![Groq API](https://img.shields.io/badge/Groq_API-Llama_3.3_70B-f36c00?style=for-the-badge)](https://groq.com)

---

## 📌 Executive Summary & Academic Acknowledgements

This repository contains the complete 7-day project portfolio developed during the **AIML Vocational Training Program** conducted by **CRISP BHOPAL** (*Centre for Research and Industrial Staff Performance*) at **Rungta College of Engineering and Technology (RCET), Bhilai**.

* **Trainer & Technical Mentor**: **Somil Jain**
* **Host Institution**: Rungta College of Engineering and Technology (RCET), Bhilai
* **Organizing Body**: CRISP Bhopal (Centre for Research and Industrial Staff Performance)
* **Program Subject**: AIML Vocational Training — Generative AI, RAG Systems, Agentic Workflows & Model Context Protocol (MCP)

---

## 🌐 Live Deployed Applications Suite

All 7 projects are fully deployed and accessible live on **Streamlit Community Cloud**:

| Day | Project Brand Name | Core Focus & Architecture | 🚀 Live Deployed App URL | 💻 Local Run Command |
| :---: | :--- | :--- | :--- | :--- |
| **Day 1** | ⚡ **Promptify AI** | 20 Prompt Engineering Benchmarks (Zero/Few/CoT/Role) | [promptify-ai.streamlit.app](https://promptify-ai.streamlit.app/) | `streamlit run day1_prompt_engineering/app.py` |
| **Day 2** | 💼 **CareerVibe AI** | LangChain Resume & Career Match Engine + Tuning | [careervibe-ai.streamlit.app](https://careervibe-ai.streamlit.app/) | `streamlit run day2_llm_app/app.py` |
| **Day 3** | 📚 **KromaPDF AI** | Multi-PDF RAG Vector Search + ChromaDB + Citations | [kromapdf-ai.streamlit.app](https://kromapdf-ai.streamlit.app/) | `streamlit run day3_rag_system/app.py` |
| **Day 4** | 🤖 **CogniTrace AI** | Autonomous ReAct Agent + Custom Memory & Visual Trace | [cognitrace-ai.streamlit.app](https://cognitrace-ai.streamlit.app/) | `streamlit run day4_agentic_ai/app.py` |
| **Day 5** | 🔌 **OmniTool MCP** | Open-Meteo REST Weather, Live DDGS Search & MCP Bridge | [omnitool-mcp.streamlit.app](https://omnitool-mcp.streamlit.app/) | `streamlit run day5_tool_integration/app.py` |
| **Day 6** | 📈 **FinMetrics AI** | Corporate Financial Ratio Math & SEC Risk Audit Engine | [finmetrics-ai.streamlit.app](https://finmetrics-ai.streamlit.app/) | `streamlit run day6_industry_solution/app.py` |
| **Day 7** | 🎓 **ApexAI Nexus** | Master Capstone Portfolio & Interactive Viva Quiz | [apex-ai-nexus.streamlit.app](https://apex-ai-nexus.streamlit.app/) | `streamlit run day7_capstone/app.py` |

---

## 📖 Comprehensive Assignment Breakdown (Days 1 – 7)

### Day 1: ⚡ Promptify AI — Prompt Engineering & Benchmarks
- **Objective**: Design, test, and benchmark 20 structured prompts across Zero-Shot, Few-Shot, Chain-of-Thought (CoT), and Role-Based System Prompting.
- **Key Features**:
  - Interactive side-by-side prompt testing lab with LLM temperature and top-p sliders.
  - JSON Benchmark dataset storing before vs after prompt optimization pairs.
  - Evaluation of hallucination reduction and token efficiency.

### Day 2: 💼 CareerVibe AI — Smart Resume & Job Description Matcher
- **Objective**: Build an LLM application using LangChain prompt templates and structured Pydantic output parsers.
- **Key Features**:
  - Accepts candidate resumes (text/PDF) and job descriptions.
  - Computes Match Percentage, identifies missing technical skills, and recommends resume edits.
  - Generates tailored corporate cover letters with downloadable reports.

### Day 3: 📚 KromaPDF AI — RAG Vector Database & Citation Engine
- **Objective**: Implement a Retrieval-Augmented Generation (RAG) system with document chunking, vector storage, and source verification.
- **Key Features**:
  - Multi-PDF document ingestion via `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
  - In-memory vector database powered by `ChromaDB` (`EphemeralClient`) for zero Windows file locking bugs.
  - HuggingFace CPU mini-LM embeddings + exact page number citations.

### Day 4: 🤖 CogniTrace AI — Autonomous ReAct Agent & Visual Trace
- **Objective**: Construct an autonomous Agentic AI workflow using the ReAct (Reasoning + Acting) loop.
- **Key Features**:
  - Featured final response box with step metrics and execution summaries.
  - Side-by-side visual execution trace card flow showing LLM reasoning vs tool outputs.
  - 10+ pre-loaded sample goals dropdown library covering math, currency conversion, and text analytics.

### Day 5: 🔌 OmniTool MCP — Real-Time API & MCP Protocol Bridge
- **Objective**: Integrate external real-world REST APIs and Model Context Protocol (MCP) tool schemas.
- **Key Features**:
  - Real-time weather engine using Open-Meteo REST API (zero key required).
  - Fast live web search powered by the updated `ddgs` library.
  - Standardized MCP JSON schema registry for LLM tool calling interoperability.

### Day 6: 📈 FinMetrics AI — Corporate Ratio & SEC Filing Risk Auditor
- **Objective**: Build an enterprise-grade industry solution combining deterministic math with LLM risk audits.
- **Key Features**:
  - Automated calculation of Liquidity (Current Ratio), Profitability (Net Margin), and Solvency (Debt-to-Equity).
  - Interactive Plotly financial trend bar charts.
  - Automated SEC 10-K filing risk extraction and C-level executive summary generation.

### Day 7: 🎓 ApexAI Nexus — Master Capstone & Assessment Portal
- **Objective**: Create a master multi-page portfolio portal hosting all 7 projects with an interactive assessment module.
- **Key Features**:
  - Unified project launcher connecting all daily applications.
  - Interactive Viva Voce Flashcard & Quiz module covering 10 core handbook questions with real-time scoring.
  - Portfolio score breakdown: 100/100 marks submission ready.

---

## 📂 Repository Architecture & File Hierarchy

```text
CRISP-GenAI-AgenticAI/
│
├── README.md                        # Primary Master Portfolio Documentation
├── requirements.txt                 # Dependencies (Streamlit, LangChain, ChromaDB, ddgs, Plotly)
├── .env.example                     # API Key template
│
├── day1_prompt_engineering/         # Promptify AI: 20 Prompts & Benchmarks
│   ├── app.py                       # Streamlit UI
│   ├── prompts_dataset.json         # 20 Benchmark Prompts
│   ├── reflection_report.md
│   └── README.md
│
├── day2_llm_app/                    # CareerVibe AI: Resume Matcher
│   ├── app.py                       # Streamlit UI
│   ├── templates.py                 # LangChain Prompt Templates
│   ├── sample_data/                 # Sample Resumes
│   ├── reflection_report.md
│   └── README.md
│
├── day3_rag_system/                 # KromaPDF AI: RAG System
│   ├── app.py                       # Streamlit UI
│   ├── rag_engine.py                # ChromaDB Ephemeral RAG Engine
│   ├── sample_docs/                 # Sample PDFs
│   ├── reflection_report.md
│   └── README.md
│
├── day4_agentic_ai/                 # CogniTrace AI: Autonomous ReAct Agent
│   ├── app.py                       # Streamlit Visual Trace UI
│   ├── agent.py                     # Custom ReAct Agent
│   ├── tools.py                     # Custom Python Tools
│   ├── reflection_report.md
│   └── README.md
│
├── day5_tool_integration/           # OmniTool MCP: REST & MCP Bridge
│   ├── app.py                       # Streamlit UI
│   ├── external_tools.py            # Open-Meteo REST & DDGS Search
│   ├── mcp_bridge.py                # MCP Schema Registry
│   ├── reflection_report.md
│   └── README.md
│
├── day6_industry_solution/          # FinMetrics AI: Financial Risk Auditor
│   ├── app.py                       # Streamlit Executive Dashboard
│   ├── financial_engine.py          # Ratio Engine & SEC Risk Auditor
│   ├── sample_reports/              # Financial statement samples
│   ├── reflection_report.md
│   └── README.md
│
└── day7_capstone/                   # ApexAI Nexus: Master Portal & Viva Quiz
    ├── app.py                       # Master Multi-Page Portal
    ├── viva_prep.py                 # Interactive Viva Quiz Module
    ├── capstone_summary.md          # 100-mark assessment rubric breakdown
    ├── reflection_report.md
    └── README.md
```

---

## ⚡ Quick Start & Local Execution

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/AyushPatwa11/CRISP-GenAI-AgenticAI.git
cd CRISP-GenAI-AgenticAI

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Keys
Create a `.env` file in the root directory:
```ini
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Launch Daily Apps Locally
```bash
# Day 1: Promptify AI
streamlit run day1_prompt_engineering/app.py --server.port 8501

# Day 2: CareerVibe AI
streamlit run day2_llm_app/app.py --server.port 8502

# Day 3: KromaPDF AI
streamlit run day3_rag_system/app.py --server.port 8504

# Day 4: CogniTrace AI
streamlit run day4_agentic_ai/app.py --server.port 8505

# Day 5: OmniTool MCP
streamlit run day5_tool_integration/app.py --server.port 8506

# Day 6: FinMetrics AI
streamlit run day6_industry_solution/app.py --server.port 8507

# Day 7: ApexAI Nexus
streamlit run day7_capstone/app.py --server.port 8508
```

---

## 📜 Credits & Academic Acknowledgements

This portfolio was created as part of the **AIML Vocational Training Assignment** organized by **CRISP BHOPAL** (*Centre for Research and Industrial Staff Performance*) hosted at **Rungta College of Engineering and Technology (RCET), Bhilai**.

* **Trainer & Mentor**: **Somil Jain**
* **Institution Host**: Rungta College of Engineering and Technology (RCET), Bhilai
* **Training Provider**: CRISP Bhopal
