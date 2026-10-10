import pytest
from natlas.chat import ChatPipeline

def test_chat_pipeline_init():
    pipeline = ChatPipeline(backend="ollama")
    assert pipeline.backend_type == "ollama"
    assert len(pipeline.history) == 1
    assert pipeline.history[0]["role"] == "system"
