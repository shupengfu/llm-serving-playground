from llm_client import chat, BASE_URL, MODEL


messages = [
    {"role": "system", "content": "你是一个中文 AI 学习助手，回答要清楚、简洁。"},
    {"role": "user", "content": "用三句话解释什么是 OpenAI-compatible API。"}
]

print("BASE_URL:", BASE_URL)
print("MODEL:", MODEL)
print()

answer = chat(messages)

print("模型回答：")
print(answer)