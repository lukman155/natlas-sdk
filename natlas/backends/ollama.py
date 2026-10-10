import requests
import json
from typing import List, Dict, Any

class OllamaBackend:
    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "natlas"):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name

    def generate(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": stream
        }
        
        # We rely on Ollama to handle the specific template if the Modelfile is properly configured
        # If stream is False, we parse the single response
        if not stream:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "")
            
        else:
            # Yielding stream not fully implemented in pipeline yet, but returning text for now
            raise NotImplementedError("Streaming is not fully implemented in OllamaBackend yet.")
