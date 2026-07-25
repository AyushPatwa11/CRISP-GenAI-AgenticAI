import json
from typing import Dict, Any

class FinancialAnalysisEngine:
    """Domain-Specific Financial & Corporate Filing Analysis Engine."""
    
    @staticmethod
    def calculate_ratios(revenue: float, net_income: float, total_assets: float, total_liabilities: float) -> Dict[str, Any]:
        """Calculates core corporate financial ratios."""
        net_profit_margin = (net_income / revenue * 100) if revenue else 0
        equity = total_assets - total_liabilities
        debt_to_equity = (total_liabilities / equity) if equity > 0 else 0
        return {
            "net_profit_margin_pct": round(net_profit_margin, 2),
            "stockholder_equity": round(equity, 2),
            "debt_to_equity_ratio": round(debt_to_equity, 2)
        }

    @staticmethod
    def generate_executive_financial_summary(llm: Any, financial_text: str) -> Dict[str, Any]:
        """Uses LLM to extract key metrics, strategic highlights, and risk factors."""
        prompt = f"""You are a Senior Wall Street Financial Analyst auditing corporate filings.
Examine the financial document text below and return a JSON object with:
1. "company_name": Name of the firm
2. "reporting_period": Q1/Q2/Q3/Q4 or Fiscal Year
3. "revenue_summary": Brief summary of top-line revenue
4. "profitability_summary": Brief summary of net profit
5. "key_risk_factors": Array of 3 key operational or market risks identified
6. "strategic_recommendation": 2-sentence executive investment/management recommendation

DOCUMENT CONTENT:
{financial_text}

Return RAW valid JSON only.
"""
        response = llm.invoke(prompt)
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
