from llm_client import chat


messages = [
    {"role": "system", "content": "你是一个中文 AI 学习助手，回答要通俗易懂。"}
]


while True:
    user_input = input("你：")

    if user_input.lower() in ["exit", "quit", "退出"]:
        print("已退出。")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    answer = chat(messages)

    print("模型：", answer)

    messages.append({
        "role": "assistant",
        "content": answer
    })