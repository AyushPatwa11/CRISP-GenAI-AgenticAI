import streamlit as st
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from financial_engine import FinancialAnalysisEngine

load_dotenv()

st.set_page_config(
    page_title="FinMetrics AI - Financial & Risk Audit Engine",
    page_icon="📈",
    layout="wide"
)

# Custom High-Aesthetic Corporate Financial Styling
st.markdown("""
<style>
    .fin-header {
        background: linear-gradient(135deg, #004D40 0%, #00C853 50%, #FFD600 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0, 200, 83, 0.25);
    }
    .fin-header h1 { color: white !important; font-weight: 800; font-size: 2.2rem; margin: 0; }
    .fin-header p { color: rgba(255,255,255,0.9) !important; font-size: 1.05rem; margin-top: 6px; margin-bottom: 0; }
    
    .metric-container {
        background: #F4F6F9;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fin-header">
    <h1>📈 FinMetrics AI Audit Engine</h1>
    <p>Corporate Financial Ratio Math Engine, Plotly Data Visualizer & SEC Filing Risk Auditor</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/combo-chart.png", width=64)
    st.header("⚙️ Model Settings")
    
    provider = st.radio("Select Provider", ["Groq", "OpenAI"])
    if provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
        default_key = os.getenv("GROQ_API_KEY", "")
    else:
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
        default_key = os.getenv("OPENAI_API_KEY", "")

    api_key = st.text_input("API Key", value=default_key, type="password")

# Load Sample Financial Report
sample_report_path = os.path.join(os.path.dirname(__file__), "sample_reports", "sample_financial_report.txt")
default_report = ""
if os.path.exists(sample_report_path):
    with open(sample_report_path, "r", encoding="utf-8") as f:
        default_report = f.read()

st.markdown("### 📄 Corporate Financial Statement / 10-K Input")
financial_text = st.text_area("Paste Financial Report Text or Edit Preset Below", value=default_report, height=200)

col_act1, col_act2 = st.columns(2)
with col_act1:
    revenue = st.number_input("Total Revenue ($)", value=150000000.0, step=1000000.0)
    net_income = st.number_input("Net Income ($)", value=35000000.0, step=1000000.0)
with col_act2:
    total_assets = st.number_input("Total Assets ($)", value=210000000.0, step=1000000.0)
    total_liabilities = st.number_input("Total Liabilities ($)", value=70000000.0, step=1000000.0)

ratios = FinancialAnalysisEngine.calculate_ratios(revenue, net_income, total_assets, total_liabilities)

st.divider()

st.markdown("### 📊 Automated Corporate Financial Ratios")
mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1.metric("Net Profit Margin", f"{ratios['net_profit_margin_pct']}%")
mcol2.metric("Stockholder Equity", f"${ratios['stockholder_equity']:,.0f}")
mcol3.metric("Debt-to-Equity Ratio", f"{ratios['debt_to_equity_ratio']}x")
mcol4.metric("Asset Coverage", f"{round(total_assets/total_liabilities, 2) if total_liabilities else 0}x")

if st.button("🚀 Audit SEC Filing & Generate Executive Briefing", type="primary", use_container_width=True):
    if not financial_text.strip():
        st.error("Please provide financial report text.")
    elif not api_key:
        st.error("Please provide a valid API Key in the sidebar.")
    else:
        with st.spinner("⚡ Running financial ratio engine & SEC risk audit..."):
            try:
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                analysis = FinancialAnalysisEngine.generate_executive_financial_summary(llm, financial_text)

                st.success("Executive Financial Audit Complete!")

                st.markdown("### 🏢 C-Level Executive Briefing")
                st.markdown(f"**Target Enterprise:** `{analysis.get('company_name', 'ACME Tech Corp')}` | **Reporting Period:** `{analysis.get('reporting_period', 'FY2025')}`")
                
                ecol1, ecol2 = st.columns(2)
                with ecol1:
                    st.info(f"**Top-Line Revenue Summary:**\n\n{analysis.get('revenue_summary', 'Strong growth recorded across core segments.')}")
                with ecol2:
                    st.success(f"**Profitability & Operating Health:**\n\n{analysis.get('profitability_summary', 'Healthy operating margins retained.')}")

                st.divider()

                # Visual Charts: Segment Breakdown & Ratios
                st.markdown("### 📈 Visual Financial Performance & Asset Breakdown")
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    fig_balance = go.Figure(data=[
                        go.Bar(name='Assets ($)', x=['Balance Sheet'], y=[total_assets], marker_color='#00C853'),
                        go.Bar(name='Liabilities ($)', x=['Balance Sheet'], y=[total_liabilities], marker_color='#FF3D00'),
                        go.Bar(name='Equity ($)', x=['Balance Sheet'], y=[ratios['stockholder_equity']], marker_color='#29B6F6')
                    ])
                    fig_balance.update_layout(title="Balance Sheet Capital Structure", barmode='group', height=350)
                    st.plotly_chart(fig_balance, use_container_width=True)

                with chart_col2:
                    fig_rev = px.bar(
                        x=["Revenue", "Net Income"],
                        y=[revenue, net_income],
                        labels={'x': 'Metric', 'y': 'Amount ($)'},
                        title="Top-Line Revenue vs Net Profit",
                        color_discrete_sequence=['#7C4DFF']
                    )
                    fig_rev.update_layout(height=350)
                    st.plotly_chart(fig_rev, use_container_width=True)

                st.divider()

                # Risk Audit Factors
                st.markdown("### ⚠️ SEC Risk Audit & Investment Assessment")
                
                risk_col1, risk_col2 = st.columns(2)
                with risk_col1:
                    st.markdown("#### 🚨 Identified Corporate Risk Factors")
                    for risk in analysis.get("key_risk_factors", ["Debt refinancing timeline", "Supply chain concentration"]):
                        st.warning(f"⚠️ {risk}")
                        
                with risk_col2:
                    st.markdown("#### 💡 Investment Recommendation")
                    rec_text = analysis.get("investment_recommendation", "BUY / ACCUMULATE - Solid balance sheet coverage.")
                    st.success(f"📌 {rec_text}")

            except Exception as e:
                st.error(f"❌ Audit Error: {str(e)}")
