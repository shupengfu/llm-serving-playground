import requests
import json


url = "http://localhost:11434/v1/chat/completions"

payload = {
    "model": "qwen2.5:0.5b",
    "messages": [
        {"role": "system", "content": "你是一个中文 AI 学习助手。"},
        {"role": "user", "content": "解释一下 OpenAI SDK 背后发送了什么请求。"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer ollama"
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)

print("HTTP status code:", response.status_code)
print()

data = response.json()

print("Raw response:")
print(json.dumps(data, ensure_ascii=False, indent=2))

print("\n模型回答：")
print(data["choices"][0]["message"]["content"])