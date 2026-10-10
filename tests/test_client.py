import pytest
from unittest.mock import MagicMock
from natlas import NAtlasClient

def test_client_initialization():
    client = NAtlasClient(backend="ollama")
    assert client.backend_type == "ollama"
    assert client.chat_pipeline is not None

def test_client_chat():
    client = NAtlasClient(backend="ollama")
    client.chat_pipeline.generate = MagicMock(return_value=MagicMock(text="Test reply", language="en"))
    
    res = client.chat("Hello")
    assert res.text == "Test reply"
    assert res.language == "en"
