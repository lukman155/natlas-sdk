# 📖 Complete API Reference Manual

## N-ATLAS Developer Harness (DSH v0.2.0)
**Core SDK Classes, Data Structures, Methods, and REST Endpoints**

---

## 1. Module: `natlas.client`

### `class natlas.client.NAtlasClient`
The primary client orchestrator unifying multilingual text generation, ASR transcription, and agent pipelines.

#### Constructor:
```python
NAtlasClient(
    hf_token: Optional[str] = None,
    backend: Optional[str] = None,
    api_url: Optional[str] = None,
    ollama_base_url: str = "http://localhost:11434",
    ollama_model: str = "natlas",
    device: str = "cpu"
)
```
- **`hf_token`** *(str, optional)*: Hugging Face API access token (reads from `HF_TOKEN` environment variable if omitted). Required for gated model weights.
- **`backend`** *(str, optional)*: Explicit backend selection: `"api"`, `"openai"`, `"transformers"`, or `"ollama"`. Automatically infers `"api"` if `api_url` or `NATLAS_API_URL` is set.
- **`api_url`** *(str, optional)*: Base URL of a remote GPU or vLLM inference server.
- **`ollama_base_url`** *(str, default `"http://localhost:11434"`)*: Base endpoint for local Ollama daemon.
- **`ollama_model`** *(str, default `"natlas"`)*: Model tag for local GGUF execution.
- **`device`** *(str, default `"cpu"`)*: PyTorch device (`"cpu"`, `"cuda:0"`, `"mps"`).

#### Methods:
##### `client.chat(...) -> ChatResponse`
```python
chat(
    prompt: str,
    language: str = "en",
    isolate: bool = False,
    max_tokens: Optional[int] = None,
    system_prompt: Optional[str] = None
) -> ChatResponse
```
- **`prompt`** *(str)*: User input text query.
- **`language`** *(str, default `"en"`)*: Language code (`"ha"`, `"yo"`, `"ig"`, `"en"`).
- **`isolate`** *(bool, default `False`)*: When `True`, executes an ephemeral single-turn session without appending to persistent conversation history.
- **`max_tokens`** *(int, optional)*: Generation token budget.
- **`system_prompt`** *(str, optional)*: Custom system instruction override.
- **Returns:** [`ChatResponse`](#class-chatresponse) containing generated `text` and `language`.

##### `client.transcribe(...) -> ASRResult`
```python
transcribe(
    audio: Union[str, bytes, BinaryIO, np.ndarray],
    language: Optional[str] = None
) -> ASRResult
```
- **`audio`**: File path (`.wav`, `.mp3`), raw audio bytes, file pointer, or 16kHz numpy array.
- **`language`** *(str, optional)*: Target language code. If omitted, performs multi-model confidence evaluation to auto-detect language.
- **Returns:** [`ASRResult`](#class-asrresult) containing `text`, `language`, and `confidence`.

##### `client.voice_pipeline(...) -> VoicePipelineResult`
```python
voice_pipeline(
    audio: Union[str, bytes, BinaryIO],
    language: Optional[str] = None
) -> VoicePipelineResult
```
- Executes full voice advisory loop: Audio In $\rightarrow$ Transcribe $\rightarrow$ LLM Chat $\rightarrow$ Audio Out.

---

## 2. Module: `natlas.orthography`

### `class natlas.orthography.NigerianOrthographyEngine`
Engine for evaluating token fragmentation and optimizing diacritic representations.

#### Methods:
##### `analyze_token_fertility(text: str, language: str = "yo") -> TokenFertilityReport`
- Calculates word count, character count, diacritic density, estimated BPE tokens, and tokens-per-word fertility ratio.
- **Returns:** [`TokenFertilityReport`](#class-tokenfertilityreport).

##### `strip_diacritics(text: str) -> str`
- Performs O(N) tone mark stripping, replacing tonal and under-dot vowels with unaccented Latin characters while preserving casing. Reduces token bloat by ~45%.
- **Returns:** `str` (normalized text).

##### `count_diacritics(text: str) -> int`
- Counts the number of tonal accents (`á`, `à`, `ā`) and under-dots (`ẹ`, `ọ`, `ṣ`, `ị`, `ụ`, `ṅ`).
- **Returns:** `int`.

---

## 3. Module: `natlas.guardrails`

### `class natlas.guardrails.SovereignCulturalGuardrail`
Culturally grounded safety and ethical compliance auditor for Nigerian AI deployments.

#### Methods:
##### `check_safety(text: str) -> GuardrailResult`
- Audits text against:
  1. Ethnic slurs and inter-communal profiling.
  2. Sectarian displacement and religious violence.
  3. Sensitive credential harvesting (BVN, NIN, ATM PIN, OTP).
  4. 419 cybercrime and advance-fee fraud generation.
- **Returns:** [`GuardrailResult`](#class-guardrailresult).

---

## 4. Module: `natlas.harness.agent`

### `class natlas.harness.agent.SovereignAgentHarness`
DeepSeek-Harness inspired ReAct agent runtime.

#### Constructor:
```python
SovereignAgentHarness(client: NAtlasClient, tool_registry: Optional[SovereignToolRegistry] = None)
```

#### Methods:
##### `run(query: str, language: str = "en", max_steps: int = 3) -> AgentExecutionResult`
- Executes autonomous reasoning loop: Safety check $\rightarrow$ Intent reasoning $\rightarrow$ Tool execution $\rightarrow$ Grounded response formulation.
- Includes automatic synthesis fallback if the backend LLM is unreachable.
- **Returns:** [`AgentExecutionResult`](#class-agentexecutionresult).

---

## 5. Module: `natlas.harness.tools`

### `class natlas.harness.tools.SovereignToolRegistry`
Central catalog for indigenous Nigerian environmental tools.

#### Methods:
- **`register(tool: ToolDefinition) -> None`**: Registers a new tool into the runtime.
- **`get_tool_schemas() -> List[Dict[str, Any]]`**: Exports all tool definitions in OpenAI Function Calling format.
- **`execute(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]`**: Dispatches arguments to the registered tool handler.

---

## 6. Module: `natlas.harness.eval`

### `class natlas.harness.eval.SovereignBenchmarkHarness`
Standardized evaluation framework for Nigerian multilingual LLMs.

#### Methods:
##### `run_suite(suite_name: str = "all", live: bool = False) -> SovereignEvaluationReport`
- Executes diagnostic evaluation across:
  - Hausa Cultural Bias & Neutrality Audit
  - Yorùbá Diacritic & Token Fertility Test
  - Igbo Dialectal Reasoning
  - Nigerian English Acoustic Alignment
- **Returns:** [`SovereignEvaluationReport`](#class-sovereignevaluationreport).

---

## 7. Data Classes Reference

### `class ChatResponse`
```python
@dataclass
class ChatResponse:
    text: str        # Generated response text
    language: str    # Language code used (ha, yo, ig, en)
```

### `class TokenFertilityReport`
```python
@dataclass
class TokenFertilityReport:
    text: str
    language: str
    character_count: int
    word_count: int
    estimated_token_count: int
    fertility_ratio: float       # BPE tokens per word
    diacritic_count: int
    diacritic_ratio: float
    recommendation: str
```

### `class GuardrailResult`
```python
@dataclass
class GuardrailResult:
    is_safe: bool                 # True if cleared, False if flagged
    risk_level: str              # "LOW", "MEDIUM", "HIGH"
    flagged_categories: List[str]# Specific violation categories
    matched_triggers: List[str]  # Substring matches
    mitigated_prompt: str        # Cleaned / Neutralized alert message
    explanation: str             # Human-readable policy rationale
```

### `class AgentExecutionResult`
```python
@dataclass
class AgentExecutionResult:
    query: str
    language: str
    steps: List[AgentStep]       # Trace of thought, action, observation
    final_response: str          # Final synthesized advice
    tools_invoked: List[str]     # Names of tools executed
    guardrail_passed: bool       # Whether prompt cleared safety
```

### `class AgentStep`
```python
@dataclass
class AgentStep:
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[Dict[str, Any]] = None
```

---

## 8. REST API Endpoints (`natlas.server`)

When running `natlas serve --port 8000` or `natlas harness --port 8000`:

| Endpoint | Method | Description |
|---|---|---|
| `/harness` | `GET` | Interactive in-browser developer workbench UI |
| `/v1/chat/completions` | `POST` | Standard OpenAI-compatible chat completion endpoint |
| `/v1/audio/transcriptions` | `POST` | Standard OpenAI-compatible Whisper transcription endpoint |
| `/v1/models` | `GET` | Lists available N-ATLAS LLM and ASR model IDs |
| `/health` | `GET` | Server health check and active GPU tunnel status |
| `/harness/status` | `GET` | Telemetry on active backend and connection latency |
| `/harness/set-endpoint` | `POST` | Dynamically updates the remote GPU ngrok URL |
| `/harness/query-single` | `POST` | Executes isolated query with token throughput metrics |
| `/harness/matrix-query` | `POST` | Executes prompt concurrently across all 4 languages |
| `/harness/analyze-tokens`| `POST` | Runs token fertility diagnostic on input text |
| `/harness/guardrail-check`| `POST` | Audits input text against cultural safety rules |
| `/harness/agent-run` | `POST` | Executes autonomous sovereign agent reasoning loop |
| `/harness/eval-suite` | `GET` | Runs complete benchmark evaluation suite |
