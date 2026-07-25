# 🚀 CRISP Generative & Agentic AI — 7-Day Complete Project Suite

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5+-FF6F61?style=for-the-badge&logo=sqlite&logoColor=white)](https://trychroma.com)
[![Groq API](https://img.shields.io/badge/Groq_API-Llama_3.3_70B-f36c00?style=for-the-badge)](https://groq.com)

Welcome to the official repository for the **CRISP Generative & Agentic AI 7-Day Assignment & Assessment Handbook**, conducted at **Rungta Engineering College, Bhilai** (Trainer: **Somil Jain**).

---

## 📅 Daily Projects Directory Structure

```text
CRISP-GenAI-AgenticAI/
│
├── README.md                        # Master Portfolio Documentation
├── requirements.txt                 # Project dependencies
├── .env.example                     # Environment key template
│
├── day1_prompt_engineering/         # DAY 1: 20 Prompts & Evaluation Suite
│   ├── app.py                       # Interactive Prompt Evaluation UI
│   ├── prompts_dataset.json         # 20 Benchmark Zero/Few/CoT/Role prompts
│   ├── reflection_report.md         # Reflection report & outputs analysis
│   └── README.md
│
├── day2_llm_app/                    # DAY 2: AI Resume & Career Matcher
│   ├── app.py                       # Streamlit app with prompt templates & parameter tuning
│   ├── templates.py                 # Structured prompt templates & output parsers
│   ├── sample_data/                 # Sample resumes & job descriptions
│   ├── reflection_report.md
│   └── README.md
│
├── day3_rag_system/                 # DAY 3: LangChain & ChromaDB PDF Chatbot
│   ├── app.py                       # RAG Q&A Streamlit app with page citations
│   ├── rag_engine.py                # PyPDF Loader, Text Splitter, HuggingFace & ChromaDB
│   ├── sample_docs/                 # Sample CRISP handbook document
│   ├── reflection_report.md
│   └── README.md
│
├── day4_agentic_ai/                 # DAY 4: Autonomous ReAct AI Agent
│   ├── app.py                       # Visual execution trace dashboard
│   ├── agent.py                     # Custom ReAct agent (Memory, Planning, Tools)
│   ├── tools.py                     # Safe Calculator, Text Analyzer, Currency Converter
│   ├── reflection_report.md
│   └── README.md
│
├── day5_tool_integration/           # DAY 5: Weather, Web Search & MCP Integration
│   ├── app.py                       # Tool Testing & MCP Assistant Hub
│   ├── external_tools.py            # Open-Meteo Weather API, DuckDuckGo Search
│   ├── mcp_bridge.py                # Model Context Protocol (MCP) tool registry
│   ├── reflection_report.md
│   └── README.md
│
├── day6_industry_solution/          # DAY 6: Financial Report & SEC Filing Analyzer
│   ├── app.py                       # Executive Financial & Risk Analysis Dashboard
│   ├── financial_engine.py          # Ratio calculation & SEC risk extraction
│   ├── sample_reports/              # Financial statement sample
│   ├── reflection_report.md
│   └── README.md
│
└── day7_capstone/                   # DAY 7: Unified Portfolio Hub & Viva Assessment
    ├── app.py                       # Master multi-page portal hosting all projects
    ├── viva_prep.py                 # Interactive Viva Voce & Quiz module (10 handbook Qs)
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

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate   # Windows

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

## 🚀 Running the Applications

Launch any day's application directly using Streamlit:

| Day | Command | Description |
|---|---|---|
| **Day 1** | `streamlit run day1_prompt_engineering/app.py` | 20 Prompt Engineering Showcase |
| **Day 2** | `streamlit run day2_llm_app/app.py` | AI Resume & Career Matcher |
| **Day 3** | `streamlit run day3_rag_system/app.py` | RAG PDF Knowledge Chatbot |
| **Day 4** | `streamlit run day4_agentic_ai/app.py` | Autonomous ReAct Agent Visual Trace |
| **Day 5** | `streamlit run day5_tool_integration/app.py` | Tool Integration & MCP Bridge |
| **Day 6** | `streamlit run day6_industry_solution/app.py` | Financial Filing Industry Solution |
| **Day 7** | `streamlit run day7_capstone/app.py` | **Master Capstone & Viva Prep Center** |

---

## 📊 Assessment Rubric Alignment (100 Marks)

| Assessment Component | Marks | Status | Implementation Details |
|---|---|---|---|
| **Daily Assignments** | 20 | ✅ Complete | Days 1–6 modular applications & datasets |
| **Capstone Project** | 20 | ✅ Complete | Master multi-page Streamlit portal (Day 7) |
| **MCQ Test** | 20 | ✅ Complete | Interactive Viva Quiz with instant scoring |
| **Coding Challenge** | 20 | ✅ Complete | Clean modular Python & LangChain architecture |
| **Viva & Demo** | 20 | ✅ Complete | 10 sample Viva Q&A explanations in Day 7 |

---

## 📜 License & Credits
Built for **Rungta Engineering College, Bhilai** as part of the CRISP Generative & Agentic AI Bootcamp. Trainer: **Somil Jain**.
