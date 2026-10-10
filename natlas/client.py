import os
import io
from typing import Optional, Union, BinaryIO

from .chat import ChatPipeline, ChatMessage
from .asr import ASRPipeline
from .pipeline import VoicePipeline

__version__ = "0.1.0"

class NAtlasClient:
    def __init__(
        self,
        hf_token: Optional[str] = None,
        backend: str = "ollama",
        ollama_base_url: str = "http://localhost:11434",
        ollama_model: str = "natlas",
        device: str = "cpu"
    ):
        self.hf_token = hf_token or os.environ.get("HF_TOKEN")
        self.backend_type = backend
        
        self.chat_pipeline = ChatPipeline(
            backend=backend,
            hf_token=self.hf_token,
            ollama_base_url=ollama_base_url,
            ollama_model=ollama_model,
            device=device
        )
        self.asr_pipeline = None
        self.voice_pipeline_instance = None
        self.device = device

    def _init_asr(self):
        if self.asr_pipeline is None:
            self.asr_pipeline = ASRPipeline(hf_token=self.hf_token, device=self.device)

    def chat(self, prompt: str, language: str = "en") -> ChatMessage:
        return self.chat_pipeline.generate(prompt, language=language)
        
    def transcribe(self, audio: Union[str, bytes, BinaryIO], language: Optional[str] = None):
        self._init_asr()
        return self.asr_pipeline.transcribe(audio, language=language)
        
    def voice_pipeline(self, audio: Union[str, bytes, BinaryIO]):
        self._init_asr()
        if self.voice_pipeline_instance is None:
            self.voice_pipeline_instance = VoicePipeline(self.asr_pipeline, self.chat_pipeline)
        return self.voice_pipeline_instance.run(audio)
