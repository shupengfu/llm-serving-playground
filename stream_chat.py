from llm_client import stream_chat


messages = [
    {"role": "system", "content": "你是一个中文 AI 学习助手，回答要通俗易懂。"}
]


while True:
    user_input = input("\n你：")

    if user_input.lower() in ["exit", "quit", "退出"]:
        print("已退出。")
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    print("模型：", end="", flush=True)

    answer = ""

    try:
        for delta in stream_chat(messages, max_tokens=200):
            print(delta, end="", flush=True)
            answer += delta

        print()

        messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        print("\n流式请求失败：", e)
        print("这通常是 Ollama 的 stream=True 接口临时返回 502，不是你的普通调用链路问题。")

        # 删除刚才失败的 user 输入，避免污染历史
        messages.pop()