from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
from natlas.client import NAtlasClient

app = FastAPI(title="N-ATLAS API", version="0.1.0")
client = NAtlasClient()

class ChatMessageInput(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessageInput]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
    last_message = req.messages[-1].content
    
    # We do a basic blocking call for now; stream would use SSE
    response = client.chat(last_message)
    
    return {
        "id": "chatcmpl-natlas",
        "object": "chat.completion",
        "created": 1234567890,
        "model": req.model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response.text,
            },
            "finish_reason": "stop"
        }]
    }

@app.post("/v1/audio/transcriptions")
async def transcribe_audio(file: UploadFile = File(...), model: str = "whisper-1"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        
        result = client.transcribe(tmp.name)
        
    os.unlink(tmp.name)
    return {"text": result.text, "language": result.language}

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "natlas", "object": "model", "owned_by": "ncair"},
            {"id": "whisper-1", "object": "model", "owned_by": "ncair"}
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}
