import requests
import json


url = "http://127.0.0.1:8001/chat"

payload = {
    "messages": [
        {
            "role": "system",
            "content": "你是一个中文 AI 学习助手，回答要清楚、简洁。"
        },
        {
            "role": "user",
            "content": "用三句话解释什么是 vLLM。"
        }
    ],
    "temperature": 0.7,
    "max_tokens": 300
}

response = requests.post(url, json=payload)

print("HTTP status code:", response.status_code)
print("Raw response text:")
print(response.text)

if response.status_code == 200:
    print("\nJSON response:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
else:
    print("\n请求失败，请查看 FastAPI / Uvicorn 服务端窗口的报错信息。")