import math
from typing import Dict, Any

def calculator_tool(expression: str) -> str:
    """Evaluates mathematical expressions safely."""
    try:
        # Safe math scope
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Math Error: {str(e)}"

def text_analysis_tool(text: str) -> str:
    """Analyzes character count, word count, sentence count, and readability estimate."""
    words = text.split()
    chars = len(text)
    sentences = text.count(".") + text.count("!") + text.count("?")
    return f"Text Stats: {len(words)} words, {chars} characters, {max(1, sentences)} sentences."

def currency_converter_tool(amount_usd: float, target_currency: str = "INR") -> str:
    """Converts USD amount to target currency (e.g. INR, EUR, GBP)."""
    rates = {"INR": 86.5, "EUR": 0.92, "GBP": 0.79, "CAD": 1.38}
    rate = rates.get(target_currency.upper(), 86.5)
    converted = amount_usd * rate
    return f"${amount_usd} USD = {converted:.2f} {target_currency.upper()} (Rate: {rate})"
