# 🇳🇬 N-ATLAS Developer Harness (DSH v0.2.0)
### Sovereign AI Agent Runtime, Evaluation Harness & Developer Toolkit for Nigeria

Welcome to the official technical documentation for the **N-ATLAS Developer Harness (DSH)**, submitted to the National AI Innovation Challenge (NAIC 2026) under **Problem Statement 1: Developer Infrastructure & Tooling**.

---

## 📚 Complete Documentation Suite

| Document | Description |
|---|---|
| **[🚀 Quickstart Guide](quickstart.md)** | Zero-to-hero installation, client configuration, and first inference in under 2 minutes. |
| **[🏛️ Technical Architecture](architecture.md)** | System design, subsystem interactions, ReAct loop, and benchmark telemetry. |
| **[📖 Complete API Reference](api-reference.md)** | Full class definitions, method signatures, return dataclasses, and REST API endpoints. |
| **[🤖 Sovereign Agents & Custom Tools](agent-tools-guide.md)** | How to build multi-step agents and author custom tools for Nigerian environments. |
| **[🔤 Token Fertility & Orthography Optimization](orthography-optimization.md)** | Deep-dive into BPE byte-fallback, fertility measurement, and cutting Yorùbá token bloat by 45%. |
| **[🛡️ Cultural Safety & Guardrails Specification](guardrails-safety.md)** | Threat model, contextual honorific parsing (*"aboki"*), and financial fraud / BVN protection. |
| **[🚢 Deployment & Infrastructure Guide](deployment-guide.md)** | Production hosting, Docker Compose, Kaggle/Colab GPU deployment, and Windows CLI setup. |
| **[💡 Real-World Developer Examples](examples.md)** | Production patterns for customer support bots, commodity price monitors, and CI/CD quality gates. |

---

## 🌟 Core Technical Innovations

1. **DeepSeek-Style Sovereign Agent Runtime (`natlas.harness.agent`):**  
   A modular plugin loop enabling N-ATLAS (8B) to reason autonomously and execute multi-step lookups across verified Nigerian environmental databases (wholesale commodity prices in Dawanau/Bodija, agro-climatic seasonal rainfall, state ADP extension offices, and parallel FX benchmarks).

2. **Orthography & Token Fertility Engine (`natlas.orthography`):**  
   Eliminates byte-fallback token fragmentation in Yorùbá and Igbo tone marks, reducing generation latency and inference costs by **up to 45%**.

3. **Contextual Cultural Safety Guardrails (`natlas.guardrails`):**  
   A localized safety layer that intercepts ethnic slurs, tribal profiling, religious sectarianism, and 419 financial fraud (BVN/NIN harvesting), while preserving friendly greetings like *"Aboki"* (friend in Hausa).

4. **Visual Developer Workbench (`natlas.server` / `harness.html`):**  
   An in-browser command center at `http://localhost:8000/harness` featuring a 4-language prompt matrix, token inspector, guardrail auditor, live agent trace, and one-click GPU reconfiguration.

5. **Standardized Benchmark Evaluation (`natlas.harness.eval`):**  
   Standardized 4-language diagnostic report cards testing Hausa bias, Yorùbá fertility, Igbo reasoning, and Nigerian English ASR.

---

## 💻 CLI Quick Commands

```bash
# Launch in-browser Visual Developer Workbench
python -m natlas.cli harness --port 8000

# Execute Sovereign Agent against Nigerian environmental tools
python -m natlas.cli agent "Nawa ne farashin buhun masara a Dawanau?" --language ha

# Audit prompt against Cultural Safety Guardrails
python -m natlas.cli guard "All Fulani herdsmen are terrorists"

# Analyze token fragmentation ratio
python -m natlas.cli fertility "Báwo ni a ṣe lè kọ́ èdè Yorùbá pẹ̀lú àmì ohùn?" --language yo

# Run standardized AfroBench evaluation suite
python -m natlas.cli eval --suite all
```

---

## 🏛️ Attribution & Credits

- **N-ATLAS** is an initiative of the **Federal Ministry of Communications, Innovation and Digital Economy (FMCIDE)**, powered by **Awarri Technologies**.
- Models developed by the **National Centre for Artificial Intelligence and Robotics (NCAIR)**, a special-purpose vehicle of **NITDA**.
- Distributed under the MIT Open Source License.
