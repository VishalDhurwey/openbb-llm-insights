import os
import requests
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def analyze_with_llm(metrics):
    formatted = "\n".join([f"{name}: {value}" for name, value in metrics])
    prompt = f"""
You are a financial analyst.

Given the following market data for today, write:
1. A short summary of overall performance.
2. Three actionable recommendations to improve or capitalize on the current market condition.

Data:
{formatted}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]
