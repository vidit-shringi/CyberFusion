from backend.core.risk import calculate_risk
from backend.ai.anomaly import AnomalyEngine
def test_risk_engine():
    score,level,factors=calculate_risk(100,100,100,100); assert score==100; assert level=="CRITICAL"; assert sum(factors.values())==100
def test_anomaly_bootstrap():
    e=AnomalyEngine(); score,meta=e.score({"failed_logins_5m":5,"new_device":1,"new_ip":1,"privilege_change":1}); assert 0<=score<=100; assert meta["mode"]=="heuristic_bootstrap"
