from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
import pathlib

from natlas.client import NAtlasClient
from natlas.orthography import NigerianOrthographyEngine
from natlas.guardrails import SovereignCulturalGuardrail
from natlas.harness.agent import SovereignAgentHarness
from natlas.harness.eval import SovereignBenchmarkHarness

app = FastAPI(title="N-ATLAS Sovereign API & Developer Harness", version="0.2.0")
client = NAtlasClient()
agent_harness = SovereignAgentHarness(client)
benchmark_harness = SovereignBenchmarkHarness(client)

class ChatMessageInput(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "NCAIR1/N-ATLaS"
    messages: List[ChatMessageInput]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False

class OrthographyRequest(BaseModel):
    text: str
    language: Optional[str] = "yo"

class GuardrailRequest(BaseModel):
    text: str

class AgentRequest(BaseModel):
    query: str
    language: Optional[str] = "en"

# Serve the visual developer harness at root and /harness
@app.get("/", response_class=HTMLResponse)
@app.get("/harness", response_class=HTMLResponse)
async def get_harness():
    template_path = pathlib.Path(__file__).parent / "harness" / "templates" / "harness.html"
    if template_path.exists():
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>N-ATLAS Developer Harness</h1><p>Template not found.</p>"

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
    last_message = req.messages[-1].content
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

# HARNESS DIAGNOSTIC API ENDPOINTS
@app.post("/harness/analyze-tokens")
async def analyze_tokens(req: OrthographyRequest):
    report = NigerianOrthographyEngine.analyze_token_fertility(req.text, req.language)
    return report

@app.post("/harness/guardrail-check")
async def guardrail_check(req: GuardrailRequest):
    result = SovereignCulturalGuardrail.check_safety(req.text)
    return result

@app.post("/harness/agent-run")
async def agent_run(req: AgentRequest):
    result = agent_harness.run(req.query, req.language)
    return result

@app.get("/harness/eval-suite")
async def run_eval_suite():
    report = benchmark_harness.run_suite()
    return report

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "NCAIR1/N-ATLaS", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Hausa-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Yoruba-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/Igbo-ASR", "object": "model", "owned_by": "ncair"},
            {"id": "NCAIR1/NigerianAccentedEnglish", "object": "model", "owned_by": "ncair"}
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.2.0-harness"}
