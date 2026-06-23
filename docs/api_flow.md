# OpenAI-compatible API Flow

## 1. Project Goal

This project demonstrates how to call a locally deployed LLM through an OpenAI-compatible API.

The current backend is Ollama, and the model is qwen2.5:1.5b.

In the future, the backend can be replaced by vLLM without changing most application-level code.

## 2. System Architecture

```text
Python Application
    ↓
OpenAI SDK or raw HTTP request
    ↓
OpenAI-compatible API
    ↓
Ollama local server
    ↓
qwen2.5:1.5b model
    ↓
Generated response





#### 3\. OpenAI SDK Call

The SDK code:

client.chat.completions.create(

&#x20;   model="qwen2.5:1.5b",

&#x20;   messages=messages,

&#x20;   temperature=0.7,

&#x20;   max\_tokens=500

)



is equivalent to sending an HTTP POST request to:

http://localhost:11434/v1/chat/completions





#### 4\. Why base\_url Matters

In this project

base\_url="http://localhost:11434/v1"

means the request is sent to the local Ollama service, not to OpenAI's official server.



If the backend is changed to vLLM, only the base\_url needs to be changed:

base\_url="http://server-ip:8000/v1"





#### 5\. Streaming

Streaming allows the model to return tokens while generating.



Without streaming, the client waits until the full response is completed.



With streaming, the response is displayed token by token.



#### 6\. What I Learned

Through this project, I learned:

* What an OpenAI-compatible API is
* How OpenAI SDK sends requests
* How to call Ollama through OpenAI SDK
* How to implement multi-turn chat
* How to implement streaming output
* How to send raw HTTP requests without SDK
* How to design a unified LLM client for future vLLM migration

