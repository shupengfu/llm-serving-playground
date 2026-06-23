from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm_client import chat, stream_chat, get_backend_info


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
        "backend_info": get_backend_info()
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

        backend_info = get_backend_info()

        return ChatResponse(
            model=backend_info["model"],
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