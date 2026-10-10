import os
from typing import List, Dict

class OpenAICompatBackend:
    def __init__(self, api_key: str = None, base_url: str = None, model: str = "natlas"):
        try:
            import openai
        except ImportError:
            raise ImportError("Please install openai to use OpenAICompatBackend.")
            
        self.client = openai.OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY", "dummy"),
            base_url=base_url or os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1")
        )
        self.model = model

    def generate(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            temperature=0.1,
            max_tokens=1000
        )
        
        if not stream:
            return response.choices[0].message.content
        else:
            raise NotImplementedError("Streaming parsing not fully supported yet.")
