import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from natlas.harness.tools import SovereignToolRegistry
from natlas.guardrails import SovereignCulturalGuardrail

@dataclass
class AgentStep:
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[Dict[str, Any]] = None

@dataclass
class AgentExecutionResult:
    query: str
    language: str
    steps: List[AgentStep]
    final_response: str
    tools_invoked: List[str]
    guardrail_passed: bool

class SovereignAgentHarness:
    """
    Indigenous Agent Execution Harness for N-ATLAS.
    Inspired by DeepSeek-Harness modular agent loops.
    
    Provides:
    1. Pre-execution Cultural Guardrail Safety Check.
    2. Multi-step reasoning & tool calling against Nigerian environmental databases.
    3. Multilingual indigenous response formulation.
    """

    def __init__(self, client, tool_registry: Optional[SovereignToolRegistry] = None):
        self.client = client
        self.registry = tool_registry or SovereignToolRegistry()

    def run(self, query: str, language: str = "en", max_steps: int = 3) -> AgentExecutionResult:
        # Step 0: Sovereign Safety Verification
        safety = SovereignCulturalGuardrail.check_safety(query)
        if not safety.is_safe:
            return AgentExecutionResult(
                query=query,
                language=language,
                steps=[AgentStep(thought="Query flagged by sovereign safety guardrails.")],
                final_response=safety.mitigated_prompt,
                tools_invoked=[],
                guardrail_passed=False
            )

        steps: List[AgentStep] = []
        tools_invoked: List[str] = []

        # Heuristic intent parser for demonstration across sovereign tools
        lower_q = query.lower()
        if any(w in lower_q for w in ["price", "cost", "farashi", "owo", "ego", "bag", "dawanau", "bodija", "market"]):
            # Trigger market price tool
            commodity = "maize"
            if "yam" in lower_q or "ji" in lower_q or "doya" in lower_q:
                commodity = "yam"
            elif "cassava" in lower_q or "rogo" in lower_q or "paki" in lower_q:
                commodity = "cassava"
            elif "rice" in lower_q or "shinkafa" in lower_q or "iresi" in lower_q:
                commodity = "rice"

            obs = self.registry.execute("get_nigerian_market_prices", {"commodity": commodity})
            tools_invoked.append("get_nigerian_market_prices")
            steps.append(AgentStep(
                thought=f"Farmer query asks about agricultural commodity market rates. Executing sovereign market lookup for {commodity}.",
                action="get_nigerian_market_prices",
                action_input={"commodity": commodity},
                observation=obs
            ))

            # Prompt LLM with observation
            agent_prompt = (
                f"User Question: {query}\n"
                f"Verified Market Observation: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Provide a helpful advisory response in {language} explaining the current price trends."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        elif any(w in lower_q for w in ["rain", "weather", "planting", "season", "ruwa", "kasa", "ojo", "ugbo", "climate"]):
            # Trigger agro weather tool
            state = "Kano"
            if "oyo" in lower_q or "ibadan" in lower_q:
                state = "Oyo"
            elif "benue" in lower_q or "makurdi" in lower_q:
                state = "Benue"
            elif "enugu" in lower_q:
                state = "Enugu"

            obs = self.registry.execute("get_agro_weather_advisory", {"state": state})
            tools_invoked.append("get_agro_weather_advisory")
            steps.append(AgentStep(
                thought=f"User requires localized weather and planting season advisory for {state}.",
                action="get_agro_weather_advisory",
                action_input={"state": state},
                observation=obs
            ))

            agent_prompt = (
                f"User Question: {query}\n"
                f"Agro-Climatic Guidance: {json.dumps(obs, ensure_ascii=False)}\n\n"
                f"Formulate a direct, culturally empathetic answer in {language} for the farmer."
            )
            llm_response = self.client.chat(agent_prompt, language=language)
            final_text = llm_response.text

        else:
            # Direct reasoning
            steps.append(AgentStep(thought="Direct indigenous reasoning without external tool execution required."))
            llm_response = self.client.chat(query, language=language)
            final_text = llm_response.text

        return AgentExecutionResult(
            query=query,
            language=language,
            steps=steps,
            final_response=final_text,
            tools_invoked=tools_invoked,
            guardrail_passed=True
        )
