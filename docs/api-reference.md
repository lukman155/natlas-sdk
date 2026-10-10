# API Reference

## `NAtlasClient`
The main entry point for the SDK.

### `chat(prompt: str, language: str = "en") -> ChatResponse`
Send a chat message to the LLM.

### `transcribe(audio: Union[str, bytes], language: Optional[str] = None) -> ASRResult`
Transcribe audio file or bytes.

### `voice_pipeline(audio: Union[str, bytes]) -> VoicePipelineResult`
Run the full ASR -> Chat pipeline.
