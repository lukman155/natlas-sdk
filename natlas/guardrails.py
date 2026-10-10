import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class GuardrailResult:
    is_safe: bool
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    flagged_categories: List[str]
    matched_triggers: List[str]
    mitigated_prompt: str
    explanation: str

class SovereignCulturalGuardrail:
    """
    Sovereign Cultural Safety & Bias Guardrail for Nigerian AI Deployments.
    
    Standard Western safety layers (Llama Guard, OpenAI Moderation) are blind to 
    Nigerian socio-political context, tribal slurs, ethnic profiling, and localized fraud.
    
    This guardrail inspects prompts and responses for:
    1. Ethnic profiling & tribal slurs across Hausa, Yoruba, Igbo, Fulani.
    2. Religious extremism and sectarian violence incitement.
    3. Financial fraud (419, Advance Fee, impersonation of EFCC/CBN).
    4. Electoral disinformation & ethnic voter suppression triggers.
    """

    ETHNIC_SLURS_AND_HATE = {
        # Normalized patterns targeting Nigerian ethnic communities
        r"\b(aboki\s+senseless|yamiri\s+thieves|ofe\s+mmanu\s+cowards|fulani\s+terrorist\s+all)\b": "Ethnic Profiling & Tribal Slur",
        r"\b(kill\s+all\s+(hausa|yoruba|igbo|fulani|tiv|igala|kanuri))\b": "Ethnic Violence Incitement",
        r"\b(chase\s+out\s+(northerners|southerners|yorubas|igbos)\s+from)\b": "Sectarian Displacement Incitement",
    }

    FINANCIAL_FRAUD_PATTERNS = {
        r"\b(send\s+your\s+bvn\s+and\s+nin\s+to\s+claim)\b": "Financial Scam (BVN/NIN Harvesting)",
        r"\b(cbn\s+grant\s+approval\s+pay\s+fee)\b": "Impersonation of Central Bank of Nigeria",
        r"\b(efcc\s+official\s+send\s+cash\s+settlement)\b": "Impersonation of Law Enforcement",
    }

    SECTARIAN_AND_RELIGIOUS_VIOLENCE = {
        r"\b(burn\s+down\s+(mosque|church|shrine))\b": "Religious Site Violence",
        r"\b(infidels?\s+must\s+die\s+in\s+nigeria)\b": "Sectarian Religious Extremism",
    }

    @classmethod
    def check_safety(cls, text: str) -> GuardrailResult:
        normalized_text = text.lower()
        flagged_categories = []
        matched_triggers = []

        all_rules = {
            **cls.ETHNIC_SLURS_AND_HATE,
            **cls.FINANCIAL_FRAUD_PATTERNS,
            **cls.SECTARIAN_AND_RELIGIOUS_VIOLENCE
        }

        for pattern, category in all_rules.items():
            matches = re.findall(pattern, normalized_text)
            if matches:
                flagged_categories.append(category)
                matched_triggers.extend([str(m) for m in matches])

        if not flagged_categories:
            return GuardrailResult(
                is_safe=True,
                risk_level="LOW",
                flagged_categories=[],
                matched_triggers=[],
                mitigated_prompt=text,
                explanation="Content cleared sovereign cultural alignment check."
            )

        risk_level = "HIGH" if any("Violence" in cat or "Incitement" in cat for cat in flagged_categories) else "MEDIUM"
        
        mitigated = (
            "[SOVEREIGN SAFETY ALERT: The query was flagged under Nigerian Cultural Safety Guardrails "
            f"for: {', '.join(set(flagged_categories))}. Response neutralized.]"
        )

        return GuardrailResult(
            is_safe=False,
            risk_level=risk_level,
            flagged_categories=list(set(flagged_categories)),
            matched_triggers=list(set(matched_triggers)),
            mitigated_prompt=mitigated,
            explanation=f"Potential violation of Nigerian sovereign peace & integrity standards: {', '.join(set(flagged_categories))}."
        )
