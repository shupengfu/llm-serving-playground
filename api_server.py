from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm_client import chat, stream_chat, BASE_URL, MODEL


app = FastAPI(
    title="LLM Serving Playground",
    description="A local OpenAI-compatible LLM serving wrapper based on FastAPI.",
    version="0.1.0"
)


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 500


class ChatResponse(BaseModel):
    model: str
    answer: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "backend_base_url": BASE_URL,
        "model": MODEL
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.messages
    ]

    try:
        answer = chat(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return ChatResponse(
            model=MODEL,
            answer=answer
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/stream")
def stream_endpoint(request: ChatRequest):
    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.messages
    ]

    def token_generator():
        try:
            for delta in stream_chat(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                yield delta
        except Exception as e:
            yield f"\n[ERROR] {str(e)}"

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )