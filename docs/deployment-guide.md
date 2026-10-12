# 🚢 Deployment & Infrastructure Guide

## N-ATLAS Developer Harness (DSH v0.2.0)
**Production Hosting, Remote GPU Tunneling, Docker, and Windows CLI Setup**

---

## 1. Quick Local Installation

### Prerequisites
- Python 3.9+ (Python 3.10 to 3.14 supported)
- Git
- Optional: NVIDIA GPU with CUDA 11.8+ for local Transformer inference, or [Ollama](https://ollama.ai) for quantized GGUF CPU inference.

### Installation Steps
```bash
# 1. Clone the repository
git clone https://github.com/lukman155/natlas-sdk.git
cd natlas-sdk

# 2. Install core package in editable mode
pip install -e .

# 3. Optional: Install with full GPU transformers and server extras
pip install -e ".[all]"
```

---

## 2. Windows PowerShell Setup & CLI Troubleshooting

### Issue: `natlas : The term 'natlas' is not recognized`
When running `natlas` directly in Windows PowerShell:
```powershell
PS C:\Users\Monsieur Lukman> natlas harness --port 8000
natlas : The term 'natlas' is not recognized as the name of a cmdlet...
```

#### Why This Occurs:
Python installs console script executables (like `natlas.exe`) into Python's `Scripts/` directory:
- Standard location: `C:\Users\<User>\AppData\Local\Python\pythoncore-<version>\Scripts`
- Or: `C:\Users\<User>\AppData\Local\Programs\Python\Python<version>\Scripts`

If this folder is not registered in your Windows system `%PATH%` environment variable, PowerShell cannot find `natlas.exe` directly.

#### Universal Solution (Works Immediately Anywhere):
Invoke the CLI module directly through Python:
```powershell
# Launch Visual Workbench
python -m natlas.cli harness --port 8000

# Execute Sovereign Agent
python -m natlas.cli agent "Nawa ne farashin masara a Dawanau?" --language ha

# Run Cultural Safety Check
python -m natlas.cli guard "All Fulani herdsmen are terrorists"

# Run Benchmark Evaluation
python -m natlas.cli eval --suite all
```

#### Adding Scripts to Windows PATH (To enable direct `natlas` command):
In PowerShell, run:
```powershell
# For the current session:
$env:PATH += ";$env:LOCALAPPDATA\Python\pythoncore-3.14-64\Scripts"

# Permanently for user account:
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$env:LOCALAPPDATA\Python\pythoncore-3.14-64\Scripts",
    "User"
)
```

---

## 3. Remote GPU Deployment (Kaggle & Google Colab)

To serve the real 8B model (`NCAIR1/N-ATLaS`) on free cloud GPUs (e.g. Kaggle T4 x2 or Google Colab T4), use the included notebook `notebooks/deploy_natlas_server.ipynb`:

### Step-by-Step Kaggle/Colab Deployment:
1. Open a new notebook on Kaggle or Google Colab and set Accelerator to **GPU T4**.
2. Run the deployment cell:

```python
# Install dependencies
!pip install -q transformers torch fastapi uvicorn pyngrok accelerate bitsandbytes

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from pyngrok import ngrok
import threading

# Authenticate Hugging Face for gated N-ATLAS model
HF_TOKEN = "your_hf_token_here"
MODEL_ID = "NCAIR1/N-ATLaS"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    token=HF_TOKEN,
    device_map="auto",
    torch_dtype=torch.float16,
    load_in_8bit=True  # Enables 8B inference on 15GB T4 GPU
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Build OpenAI-compatible API
app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatReq(BaseModel):
    messages: List[Message]
    max_tokens: Optional[int] = 120

@app.post("/v1/chat/completions")
def chat(req: ChatReq):
    prompt = req.messages[-1].content
    res = pipe(prompt, max_new_tokens=req.max_tokens, temperature=0.1, repetition_penalty=1.12)
    generated = res[0]["generated_text"][len(prompt):].strip()
    return {
        "choices": [{"message": {"role": "assistant", "content": generated}}]
    }

# Start tunnel
ngrok.set_auth_token("your_ngrok_token")
public_url = ngrok.connect(8000).public_url
print(f"🚀 Live N-ATLAS GPU URL: {public_url}")

# Run server
threading.Thread(target=uvicorn.run, kwargs={"app": app, "host": "0.0.0.0", "port": 8000}, daemon=True).start()
```

3. Copy the generated `https://xxxx.ngrok-free.app` URL.
4. Set it in your local environment:
   ```bash
   export NATLAS_API_URL="https://xxxx.ngrok-free.app"
   ```
   Or in the browser workbench at `http://localhost:8000/harness`, click **"Change URL"** and paste the link.

---

## 4. Docker Containerization

### Standalone Dockerfile
Build and run the OpenAI-compatible gateway:

```bash
# Build the Docker image
docker build -t natlas-server:latest .

# Run container binding to port 8000
docker run -d \
  -p 8000:8000 \
  -e NATLAS_API_URL="https://your-gpu-endpoint.ngrok-free.app" \
  --name natlas-api \
  natlas-server:latest
```

### Docker Compose
Run the API server alongside Ollama for local offline execution:

```yaml
version: '3.8'

services:
  natlas-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - NATLAS_API_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_models:
```

```bash
# Start full stack
docker compose up -d
```

---

## 5. Environment Variables Reference

| Variable | Description | Default | Example |
|---|---|---|---|
| `NATLAS_API_URL` | Remote GPU or vLLM endpoint URL | `None` | `https://xxxx.ngrok-free.app` |
| `HF_TOKEN` | Hugging Face Access Token (for gated model weights) | `None` | `hf_xxxxxxxxxxxxxxxx` |
| `OLLAMA_HOST` | Base URL for local Ollama daemon | `http://localhost:11434` | `http://127.0.0.1:11434` |
| `NATLAS_PORT` | Port for the visual workbench server | `8000` | `8000` |
| `NATLAS_MODEL` | Hugging Face model identifier | `NCAIR1/N-ATLaS` | `NCAIR1/N-ATLaS` |
| `DEVICE` | Target PyTorch device | `cpu` | `cuda:0` / `mps` |
