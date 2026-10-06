import unittest

try:
    from backend.core.risk_engine import calculate_risk
except Exception:
    calculate_risk = None

class CyberFusionSmokeTests(unittest.TestCase):
    def test_risk_score_bounds(self):
        self.assertIsNotNone(calculate_risk)
        score = calculate_risk(90, 80, 95, 70)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == "__main__":
    unittest.main()
