import pytest
from natlas.asr import ASRPipeline

def test_asr_pipeline_init():
    # Note: requires HF token and dependencies to run properly
    pipeline = ASRPipeline(device="cpu")
    assert pipeline.device == "cpu"
