import requests
from app.config import OPENROUTER_API_KEY

def ask_ai(question):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }

        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        ).json()

        return r["choices"][0]["message"]["content"]

    except:
        return "صار خطأ بالذكاء الصناعي"
