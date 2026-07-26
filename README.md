# 🚀 ApexAI Suite — 7 Complete Generative & Agentic AI Projects

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5+-FF6F61?style=for-the-badge&logo=sqlite&logoColor=white)](https://trychroma.com)
[![Groq API](https://img.shields.io/badge/Groq_API-Llama_3.3_70B-f36c00?style=for-the-badge)](https://groq.com)

Welcome to the **ApexAI Suite**, a modern collection of 7 production-ready Generative & Agentic AI applications built for the **CRISP Assignment & Assessment Handbook** at **Rungta Engineering College, Bhilai** (Trainer: **Somil Jain**).

---

## 🌟 Modern Project Suite

| # | Brand Name | Icon | Category | Core Tech Stack |
|---|---|---|---|---|
| 1 | **Promptify AI** | ⚡ | Prompt Engineering & Benchmarks | Streamlit, JSON Datasets, Groq/OpenAI |
| 2 | **CareerVibe AI** | 💼 | Smart Resume & Career Match Engine | LangChain, Pydantic, Structured Prompting |
| 3 | **KromaPDF AI** | 📚 | RAG PDF & Knowledge Search Engine | ChromaDB, HuggingFace Embeddings, PyPDF |
| 4 | **AgentFlow AI** | 🤖 | Autonomous ReAct Agent & Visual Trace | ReAct Framework, Memory, Custom Tools |
| 5 | **OmniTool MCP** | 🔌 | Real-Time API & Protocol Bridge | Open-Meteo REST, DuckDuckGo, MCP Registry |
| 6 | **FinPulse AI** | 📈 | Financial & SEC Filing Risk Auditor | Plotly Charts, Financial Math, SEC Audits |
| 7 | **ApexAI Hub** | 🎓 | Master Portfolio & Viva Prep Center | Multi-page Portal, Interactive Viva Quiz |

---

## 📂 Repository Directory Structure

```text
CRISP-GenAI-AgenticAI/
│
├── README.md                        # Primary Portfolio Documentation
├── requirements.txt                 # Project dependencies
├── .env.example                     # Environment key template
│
├── day1_prompt_engineering/         # Promptify AI: 20 Prompts & Evaluation Suite
│   ├── app.py                       # Promptify AI Streamlit App
│   ├── prompts_dataset.json         # 20 Benchmark Zero/Few/CoT/Role prompts
│   ├── reflection_report.md
│   └── README.md
│
├── day2_llm_app/                    # CareerVibe AI: Resume & Career Matcher
│   ├── app.py                       # CareerVibe AI Streamlit App
│   ├── templates.py                 # Structured prompt templates & output parsers
│   ├── sample_data/                 # Sample resumes & job descriptions
│   ├── reflection_report.md
│   └── README.md
│
├── day3_rag_system/                 # KromaPDF AI: RAG Knowledge Engine
│   ├── app.py                       # KromaPDF AI Streamlit App
│   ├── rag_engine.py                # PyPDF Loader, Text Splitter, HuggingFace & ChromaDB
│   ├── sample_docs/                 # Sample handbook document
│   ├── reflection_report.md
│   └── README.md
│
├── day4_agentic_ai/                 # AgentFlow AI: Autonomous ReAct Agent
│   ├── app.py                       # AgentFlow AI Visual Trace Dashboard
│   ├── agent.py                     # Custom ReAct agent (Memory, Planning, Tools)
│   ├── tools.py                     # Calculator, Text Analyzer, Currency Converter
│   ├── reflection_report.md
│   └── README.md
│
├── day5_tool_integration/           # OmniTool MCP: REST & Tool Protocol Bridge
│   ├── app.py                       # OmniTool MCP Interactive Hub
│   ├── external_tools.py            # Open-Meteo Weather API, DuckDuckGo Search
│   ├── mcp_bridge.py                # Model Context Protocol (MCP) tool registry
│   ├── reflection_report.md
│   └── README.md
│
├── day6_industry_solution/          # FinPulse AI: Financial & SEC Risk Auditor
│   ├── app.py                       # FinPulse AI Dashboard
│   ├── financial_engine.py          # Corporate ratio math & SEC risk extraction
│   ├── sample_reports/              # Financial statement sample
│   ├── reflection_report.md
│   └── README.md
│
└── day7_capstone/                   # ApexAI Hub: Master Portfolio & Viva Center
    ├── app.py                       # ApexAI Hub Multi-Page Master Portal
    ├── viva_prep.py                 # Interactive Viva Voce Quiz module
    ├── capstone_summary.md          # 100-mark assessment rubric breakdown
    ├── reflection_report.md
    └── README.md
```

---

## ⚡ Quick Start & Setup

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/AyushPatwa11/CRISP-GenAI-AgenticAI.git
cd CRISP-GenAI-AgenticAI

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment Keys
Create a `.env` file in the root directory based on `.env.example`:
```ini
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Launching Applications

Launch any application suite directly via Streamlit:

| Project Brand Name | Launch Command | Features |
|---|---|---|
| ⚡ **Promptify AI** | `streamlit run day1_prompt_engineering/app.py` | 20 Prompt Engineering Showcase |
| 💼 **CareerVibe AI** | `streamlit run day2_llm_app/app.py` | Smart Resume & Career Match Engine |
| 📚 **KromaPDF AI** | `streamlit run day3_rag_system/app.py` | RAG PDF Knowledge Search |
| 🤖 **AgentFlow AI** | `streamlit run day4_agentic_ai/app.py` | Autonomous ReAct Agent Visual Trace |
| 🔌 **OmniTool MCP** | `streamlit run day5_tool_integration/app.py` | Real-Time API & MCP Protocol Bridge |
| 📈 **FinPulse AI** | `streamlit run day6_industry_solution/app.py` | Financial & SEC Filing Risk Auditor |
| 🎓 **ApexAI Hub** | `streamlit run day7_capstone/app.py` | **Master Capstone & Viva Prep Center** |

---

## 📜 License & Credits
Built for **Rungta Engineering College, Bhilai** as part of the CRISP Generative & Agentic AI Bootcamp. Trainer: **Somil Jain**.
