from openai import OpenAI

from config import (
    LLM_BACKEND,
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_REQUEST_TIMEOUT,
)


# 为了兼容之前其他文件里的 import
BACKEND = LLM_BACKEND
BASE_URL = LLM_BASE_URL
API_KEY = LLM_API_KEY
MODEL = LLM_MODEL


client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    timeout=LLM_REQUEST_TIMEOUT,
)


def get_backend_info():
    return {
        "backend": BACKEND,
        "base_url": BASE_URL,
        "model": MODEL,
        "timeout": LLM_REQUEST_TIMEOUT,
    }


def chat(messages, temperature=0.7, max_tokens=500):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


def stream_chat(messages, temperature=0.7, max_tokens=500):
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )

    for chunk in stream:
        try:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
        except Exception:
            continue