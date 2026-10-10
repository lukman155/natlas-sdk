from typing import Optional, List, Dict
from pydantic import BaseModel
import os

class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatResponse(BaseModel):
    text: str
    language: str

SYSTEM_PROMPT = "you are a large language model trained by Awarri AI technologies. You are a friendly assistant and you are here to help."

class ChatPipeline:
    def __init__(self, backend="ollama", hf_token=None, ollama_base_url="http://localhost:11434", ollama_model="natlas", device="cpu"):
        self.backend_type = backend
        self.hf_token = hf_token
        self.system_prompt = SYSTEM_PROMPT
        self.history = [{"role": "system", "content": self.system_prompt}]
        
        if self.backend_type == "transformers":
            from .backends.transformers import TransformersBackend
            self.backend = TransformersBackend(model_id="NCAIR1/N-ATLaS", hf_token=self.hf_token, device=device)
        elif self.backend_type == "ollama":
            from .backends.ollama import OllamaBackend
            self.backend = OllamaBackend(base_url=ollama_base_url, model_name=ollama_model)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def generate(self, prompt: str, language: str = "en", stream: bool = False) -> ChatResponse:
        self.history.append({"role": "user", "content": prompt})
        
        response_text = self.backend.generate(self.history, stream=stream)
        self.history.append({"role": "assistant", "content": response_text})
        
        return ChatResponse(text=response_text, language=language)
