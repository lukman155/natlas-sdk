import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from natlas.orthography import NigerianOrthographyEngine
from natlas.guardrails import SovereignCulturalGuardrail
from natlas.harness.tools import SovereignToolRegistry
from natlas.harness.agent import SovereignAgentHarness
from natlas.harness.eval import SovereignBenchmarkHarness
from natlas import NAtlasClient

class TestSovereignHarness(unittest.TestCase):
    def test_orthography_diacritic_strip(self):
        sample = "Báwo ni o ṣe wà?"
        stripped = NigerianOrthographyEngine.strip_diacritics(sample)
        self.assertEqual(stripped, "Bawo ni o se wa?")

    def test_token_fertility_analysis(self):
        sample = "Ṣàlàyé bí a ṣe ń ṣe àkóso àrùn rogo ní ilẹ̀ Yorùbá."
        report = NigerianOrthographyEngine.analyze_token_fertility(sample, language="yo")
        self.assertGreater(report.diacritic_count, 0)
        self.assertGreater(report.fertility_ratio, 1.0)
        self.assertIn("token", report.recommendation.lower())

    def test_guardrails_benign_prompt(self):
        safe_query = "What is the best way to plant cassava in Ibadan?"
        result = SovereignCulturalGuardrail.check_safety(safe_query)
        self.assertTrue(result.is_safe)
        self.assertEqual(result.risk_level, "LOW")

    def test_guardrails_flag_ethnic_slur(self):
        unsafe_query = "Kill all hausa people in the market."
        result = SovereignCulturalGuardrail.check_safety(unsafe_query)
        self.assertFalse(result.is_safe)
        self.assertEqual(result.risk_level, "HIGH")
        self.assertIn("SOVEREIGN SAFETY ALERT", result.mitigated_prompt)

    def test_sovereign_tool_registry(self):
        registry = SovereignToolRegistry()
        schemas = registry.get_tool_schemas()
        self.assertGreaterEqual(len(schemas), 2)
        
        # Test market lookup tool
        res = registry.execute("get_nigerian_market_prices", {"commodity": "maize"})
        self.assertIn("data", res)
        self.assertIn("dawanau (kano)", res["data"])

    def test_benchmark_harness(self):
        client = NAtlasClient(backend="ollama")
        benchmark = SovereignBenchmarkHarness(client)
        report = benchmark.run_suite("all")
        self.assertGreaterEqual(report.overall_score, 3.0)
        self.assertEqual(len(report.task_results), 4)

if __name__ == '__main__':
    unittest.main()
