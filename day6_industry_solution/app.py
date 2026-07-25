import streamlit as st
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from financial_engine import FinancialAnalysisEngine

load_dotenv()

st.set_page_config(
    page_title="Day 6 - Financial & Corporate Filing AI Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Day 6: Industry Solution — Financial & SEC Filing Analyzer")
st.caption("Tailored AI Solution for Finance: Combining Automated Ratio Calculation, Executive Summarization & Risk Audit")

# Sidebar Configuration
st.sidebar.header("⚙️ Model Settings")

provider = st.sidebar.radio("Select Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    default_key = os.getenv("GROQ_API_KEY", "")
else:
    model_name = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    default_key = os.getenv("OPENAI_API_KEY", "")

api_key = st.sidebar.text_input("API Key", value=default_key, type="password")

st.divider()

# Load Sample Financial Report
sample_report_path = os.path.join(os.path.dirname(__file__), "sample_reports", "sample_financial_report.txt")
default_report = ""
if os.path.exists(sample_report_path):
    with open(sample_report_path, "r", encoding="utf-8") as f:
        default_report = f.read()

st.markdown("### 📄 Input Financial Report / 10-K Filing")
financial_text = st.text_area("Paste Financial Report Text or Edit Below", value=default_report, height=220)

col_act1, col_act2 = st.columns(2)
with col_act1:
    revenue = st.number_input("Total Revenue ($)", value=150000000.0, step=1000000.0)
    net_income = st.number_input("Net Income ($)", value=35000000.0, step=1000000.0)
with col_act2:
    total_assets = st.number_input("Total Assets ($)", value=210000000.0, step=1000000.0)
    total_liabilities = st.number_input("Total Liabilities ($)", value=70000000.0, step=1000000.0)

ratios = FinancialAnalysisEngine.calculate_ratios(revenue, net_income, total_assets, total_liabilities)

st.divider()

st.markdown("### 📊 Automated Corporate Ratio Metrics")
mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1.metric("Net Profit Margin", f"{ratios['net_profit_margin_pct']}%")
mcol2.metric("Stockholder Equity", f"${ratios['stockholder_equity']:,.0f}")
mcol3.metric("Debt-to-Equity Ratio", f"{ratios['debt_to_equity_ratio']}x")
mcol4.metric("Asset-to-Liability Coverage", f"{round(total_assets/total_liabilities, 2) if total_liabilities else 0}x")

if st.button("🚀 Audit Filing & Generate Executive Briefing", type="primary", use_container_width=True):
    if not financial_text.strip():
        st.error("Please provide financial report text.")
    elif not api_key:
        st.error("Please provide a valid API Key in the sidebar.")
    else:
        with st.spinner("Analyzing corporate filing and extracting risk factors..."):
            try:
                if provider == "Groq":
                    from langchain_groq import ChatGroq
                    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.1)
                else:
                    from langchain_openai import ChatOpenAI
                    llm = ChatOpenAI(openai_api_key=api_key, model_name=model_name, temperature=0.1)

                analysis = FinancialAnalysisEngine.generate_executive_financial_summary(llm, financial_text)

                st.success("Executive Financial Analysis Complete!")

                st.markdown("### 🏢 Executive Summary")
                st.markdown(f"**Company:** `{analysis.get('company_name', 'N/A')}` | **Period:** `{analysis.get('reporting_period', 'N/A')}`")
                
                ecol1, ecol2 = st.columns(2)
                with ecol1:
                    st.info(f"**Top-Line Revenue Performance:**\n{analysis.get('revenue_summary', '')}")
                with ecol2:
                    st.success(f"**Profitability & Margin Health:**\n{analysis.get('profitability_summary', '')}")

                st.divider()

                # Visual Charts: Segment Breakdown & Ratios
                st.markdown("### 📈 Visual Financial Performance & Risk Radar")
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    # Segment Revenue Pie Chart
                    labels = ['Enterprise Cloud', 'AI Developer Tools', 'Legacy Software']
                    values = [90000000, 40000000, 20000000]
                    fig_pie = px.pie(values=values, names=labels, title="Revenue by Business Segment ($)", hole=0.4)
                    st.plotly_chart(fig_pie, use_container_width=True)

                with chart_col2:
                    # Balance Sheet Bar Chart
                    fig_bar = go.Figure(data=[
                        go.Bar(name='Assets', x=['Balance Sheet'], y=[total_assets], marker_color='#2ecc71'),
                        go.Bar(name='Liabilities', x=['Balance Sheet'], y=[total_liabilities], marker_color='#e74c3c'),
                        go.Bar(name='Equity', x=['Balance Sheet'], y=[ratios['stockholder_equity']], marker_color='#3498db')
                    ])
                    fig_bar.update_layout(title="Capital Structure ($)", barmode='group')
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.divider()

                # Risk Factors & Recommendation
                st.markdown("### ⚠️ Key Risk Factors Identified")
                for risk in analysis.get("key_risk_factors", []):
                    st.markdown(f"- 🔴 {risk}")

                st.markdown("### 🎯 Strategic Recommendation")
                st.warning(analysis.get("strategic_recommendation", ""))

                # Downloadable Executive Report
                report_md = f"""# Executive Financial Audit Report: {analysis.get('company_name')} ({analysis.get('reporting_period')})

## Financial Ratios:
- Net Profit Margin: {ratios['net_profit_margin_pct']}%
- Debt to Equity: {ratios['debt_to_equity_ratio']}x
- Stockholder Equity: ${ratios['stockholder_equity']:,.2f}

## Revenue Summary:
{analysis.get('revenue_summary')}

## Key Risk Factors:
""" + "\n".join([f"- {r}" for r in analysis.get("key_risk_factors", [])]) + f"""

## Strategic Recommendation:
{analysis.get('strategic_recommendation')}
"""

                st.download_button(
                    label="📥 Download Executive Briefing (.md)",
                    data=report_md,
                    file_name=f"Financial_Audit_{analysis.get('company_name', 'Corp').replace(' ', '_')}.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Financial analysis failed: {str(e)}")
