# Day 2 Reflection Report: Streamlit LLM Application Architecture

## 🎯 Executive Summary
Day 2 focused on building a fully functional, user-facing LLM Streamlit application: the **AI Resume & Career Match Analyzer**. The project combined LangChain prompt templates, dynamic hyperparameter controls (Temperature, Top-P, Max Tokens), multi-modal input processing (PDF/TXT uploads), and structured JSON output parsing.

---

## 🏗️ Architectural Insights

1. **Structured Output Enforcement**:
   - By embedding JSON schema specifications directly into the `PromptTemplate`, the application consistently outputs valid JSON matching the UI requirements without breaking the Streamlit rendering pipeline.
2. **Hyperparameter Sensitivity**:
   - **Temperature (0.2)**: Essential for factual score computation and skill gap identification. Higher temperatures (>0.7) led to score variance for identical resume inputs.
   - **Top-P (0.9)**: Allowed creative vocabulary in the generated cover letter while keeping the skill extraction strictly grounded.

---

## 🛠️ Lessons & Challenges
- **PDF Extraction**: Used `pypdf` for clean text extraction from uploaded resume documents. Added handling for missing/malformed PDF buffers.
- **Provider Interchangeability**: Designed the LLM wrapper layer to seamlessly switch between Groq (`llama-3.3-70b-versatile`) and OpenAI (`gpt-4o-mini`) based on environment keys.
