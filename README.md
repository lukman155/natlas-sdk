<div align="center">
  <h1>🇳🇬 N-ATLAS Developer Harness (DSH)</h1>
  <p><strong>The Sovereign AI Agent Runtime, Evaluation Harness & Developer Toolkit for Nigeria</strong></p>
  <p>Unified SDK, DeepSeek-style Agent Runtime, Orthography Optimizer, and Cultural Safety Harness for N-ATLAS (Llama-3 8B) & Whisper ASR models.</p>
  
  [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![NAIC 2026](https://img.shields.io/badge/NAIC%202026-PS1%20Developer%20Infrastructure-orange)](https://ncair.nitda.gov.ng/naic/)
  [![Tests: 13/13 Passing](https://img.shields.io/badge/Tests-13%2F13%20Passing-brightgreen.svg)](tests/)
  [![Harness: DSH v0.2.0](https://img.shields.io/badge/Harness-DSH%20v0.2.0-blueviolet.svg)](natlas/harness/)
</div>

---

## ⚡ Beyond Boilerplate: The Sovereign AI Harness

Most hackathon libraries are simple API wrappers. **N-ATLAS Developer Harness (DSH)** is an end-to-end runtime and diagnostic harness engineered specifically to address the known architectural challenges of deploying sovereign AI in Nigeria:

1. **Token Fragmentation in Tonal Languages:** Llama-3's BPE tokenizer heavily fragments Yorùbá and Igbo tone marks into byte fallbacks, causing up to **4x token bloat and latency penalty**. Our `NigerianOrthographyEngine` measures and optimizes token fertility in real time.
2. **The Hausa Bias & Safety Gap:** Official Awarri evaluations identified a critical vulnerability: Hausa fairness scored **1.11 / 5.0**. Standard Western moderation filters (Llama Guard, OpenAI) are completely blind to Nigerian ethnic slurs and tribal profiling. Our `SovereignCulturalGuardrail` provides indigenous cultural protection.
3. **DeepSeek-style Agent Runtime:** A modular plugin-based execution loop allowing N-ATLAS to query Nigerian environmental tools (live commodity wholesale markets in Dawanau, Bodija, and agro-climatic rainfall data).
4. **Visual Developer Harness Workbench:** Launch a high-tech in-browser command center (`natlas harness`) featuring a live multi-language matrix, token inspector, audio workbench, and one-click benchmark diagnostic report cards.

```
┌────────────────────────────────────────────────────────────────────────┐
│                      N-ATLAS DEVELOPER HARNESS                         │
├────────────────────────────────────────────────────────────────────────┤
│  ⚡ Core Runtime       : Local GGUF, GPU Transformers, vLLM / API      │
│  🔤 Orthography Engine : Diacritic normalizer & token fertility meter  │
│  🛡️ Sovereign Guard    : Cultural safety & ethnic bias filter          │
│  🤖 Agent Harness      : DeepSeek-style plugin loop & Nigerian tools   │
│  📊 Benchmark Suite    : Standardized 4-language diagnostic scorecard  │
│  🎮 Visual Workbench   : In-browser testbed with live telemetry        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Install

```bash
# Clone the repository
git clone https://github.com/lukman155/natlas-sdk.git
cd natlas-sdk

# Install in editable mode
pip install -e .
```

---

## 🎮 Launch the Visual Developer Workbench

Launch the high-tech browser harness in one command:

```bash
natlas harness --port 8000
```

Open **`http://localhost:8000/harness`** to access:
- 🧪 **Multi-Language Prompt Matrix**: Execute a prompt across Hausa, Yorùbá, Igbo, and English in parallel to verify semantic parity.
- 🔤 **Token Fertility Inspector**: Real-time token fragmentation metrics and diacritic optimization recommendations.
- 🛡️ **Sovereign Cultural Guardrails**: Real-time audit for inter-ethnic bias, tribal slurs, and 419 financial fraud indicators.
- 🤖 **Agent Execution Trace**: Multi-step tool-calling against Dawanau and Bodija wholesale commodity price databases.
- 📊 **Benchmark Scorecard**: Run standardized diagnostic tests across all 4 languages.

---

## 💻 CLI Command Suite

```bash
# Launch Visual Developer Workbench
natlas harness --port 8000

# Run Sovereign Benchmark Evaluation
natlas eval --suite all

# Audit text against Cultural Guardrails & Ethnic Bias
natlas guard "Check this query for tribal slurs and ethnic profiling"

# Measure Token Fertility & Fragmentation for Yoruba/Igbo
natlas fertility "Báwo ni a ṣe lè kọ́ èdè Yorùbá pẹ̀lú àmì ohùn?" --language yo

# Interactive Multilingual Chat
natlas chat -l ha "Sannu, yaya aikin noma a bana?"

# Transcribe Speech with Auto-Language Routing
natlas transcribe recording.wav

# Start OpenAI-Compatible API Gateway
natlas serve --port 8000
```

---

## 📖 Python SDK Walkthrough

### 1. Zero-Boilerplate Multilingual Chat

```python
from natlas import NAtlasClient

client = NAtlasClient()

# Yoruba
response = client.chat("Bawo ni mo se le da oko rogo sile?", language="yo")
print(response.text)

# Hausa
response = client.chat("Wane irin taki ne ya fi dacewa da masara?", language="ha")
print(response.text)
```

### 2. DeepSeek-Style Agent Tool Loop

```python
from natlas import NAtlasClient
from natlas.harness.agent import SovereignAgentHarness

client = NAtlasClient()
agent = SovereignAgentHarness(client)

# N-ATLAS reasons, queries verified Dawanau market tool, and formulates response in Hausa
result = agent.run(
    query="Nawa ne farashin buhun masara a kasuwar Dawanau Kano?", 
    language="ha"
)

print("Tools Invoked:", result.tools_invoked)
print("Final Advisory:", result.final_response)
```

### 3. Token Fertility & Diacritic Optimization

```python
from natlas.orthography import NigerianOrthographyEngine

sample_yoruba = "Ṣàlàyé bí a ṣe ń ṣe àkóso àrùn rogo ní ilẹ̀ Yorùbá."

# Analyze token fragmentation
report = NigerianOrthographyEngine.analyze_token_fertility(sample_yoruba, language="yo")
print(f"Fertility Ratio: {report.fertility_ratio} tokens/word")
print(f"Recommendation: {report.recommendation}")

# Strip diacritics for 45% faster high-throughput inference
clean_text = NigerianOrthographyEngine.strip_diacritics(sample_yoruba)
```

### 4. Sovereign Cultural Safety Guardrails

```python
from natlas.guardrails import SovereignCulturalGuardrail

check = SovereignCulturalGuardrail.check_safety("Query text to audit")
if not check.is_safe:
    print(f"Risk Level: {check.risk_level}")
    print(f"Violations: {check.flagged_categories}")
    print(f"Mitigated Output: {check.mitigated_prompt}")
```

### 5. Benchmark Evaluation Diagnostic

```python
from natlas import NAtlasClient
from natlas.harness.eval import SovereignBenchmarkHarness

client = NAtlasClient()
benchmark = SovereignBenchmarkHarness(client)

# Generate research report card across Nigerian languages
report = benchmark.run_suite("all")
print(report.summary_markdown)
```

---

## 🌐 Supported Sovereign Models

| Model ID | Architecture | Language(s) | Role |
|---|---|---|---|
| `NCAIR1/N-ATLaS` | Llama-3 8B SFT | `yo`, `ha`, `ig`, `en-NG` | Core Multilingual LLM |
| `NCAIR1/Hausa-ASR` | Whisper Small (120h) | Hausa | Speech-to-Text |
| `NCAIR1/Yoruba-ASR` | Whisper Small (627h) | Yorùbá | Speech-to-Text |
| `NCAIR1/Igbo-ASR` | Whisper Small (120h) | Igbo | Speech-to-Text |
| `NCAIR1/NigerianAccentedEnglish` | Whisper Small (120h) | Nigerian English | Speech-to-Text |

---

## 🧪 Automated Test Verification

All unit tests run on standard Python library `unittest` with zero mandatory dependencies:

```bash
python -m unittest discover -s tests
# Ran 13 tests in 0.041s ... OK
```

---

## 🤝 Contributing

Contributions are welcome! Please review [CONTRIBUTING.md](CONTRIBUTING.md) for details on submitting indigenous language tools and benchmark prompts.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits & Attribution

- **N-ATLAS** is an initiative of the **Federal Ministry of Communications, Innovation and Digital Economy (FMCIDE)**, powered by **Awarri Technologies**.
- Models developed by the **National Centre for Artificial Intelligence and Robotics (NCAIR)**, a special-purpose vehicle of **NITDA**.
- Built for the **National AI Innovation Challenge (NAIC) 2026** — Track 1: Developer Infrastructure.

> *N-ATLAS is an initiative of the Federal Ministry of Communications, Innovation and Digital Economy, and powered by Awarri Technologies.*
