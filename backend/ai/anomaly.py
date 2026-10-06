from __future__ import annotations
import os
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, "isolation_forest.npy")
FEATURE_ORDER = [
    "failed_logins_5m", "successful_logins_1h", "new_device", "new_ip",
    "login_hour_deviation", "resource_rarity", "privilege_change",
    "number_of_destinations", "network_volume", "process_rarity",
    "session_duration", "authentication_frequency"
]

class AnomalyEngine:
    def __init__(self):
        self.model = IsolationForest(n_estimators=120, contamination=0.08, random_state=42)
        self.scaler = StandardScaler()
        self.fitted = False

    def fit(self, rows: list[dict]):
        if len(rows) < 20:
            self.fitted = False
            return
        X = np.array([[float(r.get(f, 0.0)) for f in FEATURE_ORDER] for r in rows], dtype=float)
        Xs = self.scaler.fit_transform(X)
        self.model.fit(Xs)
        self.fitted = True

    def score(self, features: dict) -> tuple[float, dict]:
        if not self.fitted:
            heuristic = 0.0
            heuristic += min(float(features.get("failed_logins_5m", 0)) / 5, 1) * 25
            heuristic += float(features.get("new_device", 0)) * 15
            heuristic += float(features.get("new_ip", 0)) * 15
            heuristic += float(features.get("login_hour_deviation", 0)) * 10
            heuristic += min(float(features.get("resource_rarity", 0)), 1) * 10
            heuristic += float(features.get("privilege_change", 0)) * 15
            heuristic += min(float(features.get("authentication_frequency", 0)) / 2, 1) * 10
            score = max(0.0, min(100.0, heuristic))
            return score, {"mode": "heuristic_bootstrap", "top_features": _top_features(features)}
        X = np.array([[float(features.get(f, 0.0)) for f in FEATURE_ORDER]], dtype=float)
        Xs = self.scaler.transform(X)
        raw = float(-self.model.decision_function(Xs)[0])
        score = max(0.0, min(100.0, (raw + 0.2) * 125.0))
        return score, {"mode": "isolation_forest", "top_features": _top_features(features)}

def _top_features(features: dict) -> list[dict]:
    items = sorted(((k, float(v)) for k, v in features.items()), key=lambda x: abs(x[1]), reverse=True)
    return [{"feature": k, "value": round(v, 4)} for k, v in items[:5]]

anomaly_engine = AnomalyEngine()
