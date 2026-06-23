\# Backend Configuration



\## 1. Goal



This stage makes the LLM backend configurable through environment variables.



The project currently uses Ollama as the local backend. In the future, the backend can be switched to vLLM without changing application code.



\## 2. Configuration File



The backend configuration is defined in `config.py`.



```python

LLM\_BACKEND = os.getenv("LLM\_BACKEND", "ollama")

LLM\_BASE\_URL = os.getenv("LLM\_BASE\_URL", "http://localhost:11434/v1")

LLM\_API\_KEY = os.getenv("LLM\_API\_KEY", "ollama")

LLM\_MODEL = os.getenv("LLM\_MODEL", "qwen2.5:0.5b")

\## 3. Local Ollama Configuration

PowerShell:

$env:LLM_BACKEND="ollama"
$env:LLM_BASE_URL="http://localhost:11434/v1"
$env:LLM_API_KEY="ollama"
$env:LLM_MODEL="qwen2.5:0.5b"

\## 4. Future vLLM Configuration

PowerShell:

$env:LLM_BACKEND="vllm"
$env:LLM_BASE_URL="http://SERVER_IP:8000/v1"
$env:LLM_API_KEY="EMPTY"
$env:LLM_MODEL="Qwen/Qwen2.5-1.5B-Instruct"

\## 5. Check Backend

Run:

python check_backend.py

This script prints the current backend configuration and checks the /models endpoint.

\## 6. Why This Matters

Separating configuration from code makes the project easier to migrate from Ollama to vLLM.

The application code can remain the same:

api_client.py
    ↓
FastAPI
    ↓
llm_client.py
    ↓
OpenAI-compatible backend

Only the backend URL and model name need to be changed.