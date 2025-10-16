import requests
import os

api_key = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [
        {"role": "user", "content": "Design a secure calculator web app for kids using Python and React."}
    ],
    "reasoning": { "effort": "high" },
    # If still no response, comment out reasoning OR lower to "medium"
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
print(response.json())
