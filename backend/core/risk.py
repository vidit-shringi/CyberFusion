from __future__ import annotations
WEIGHTS={"rule":0.35,"behavior":0.25,"correlation":0.25,"threat":0.15}
def risk_level(score:float)->str:
    if score>=85:return "CRITICAL"
    if score>=70:return "HIGH"
    if score>=50:return "MEDIUM"
    if score>=25:return "LOW"
    return "INFO"
def calculate_risk(rule:float,behavior:float,correlation:float,threat:float)->tuple[float,str,dict]:
    values={"rule":rule,"behavior":behavior,"correlation":correlation,"threat":threat}; score=round(max(0.0,min(100.0,sum(values[k]*WEIGHTS[k] for k in WEIGHTS))),2); factors={k:round(values[k]*WEIGHTS[k],2) for k in WEIGHTS}; return score,risk_level(score),factors
def recommended_action(score:float,factors:dict)->str:
    if score>=85:return "Require re-authentication, review the session and affected asset, and investigate the linked identity/device/IP before restoring privileged access."
    if score>=70:return "Investigate the correlated event chain, validate the identity and device, and review any linked vulnerability evidence."
    if score>=50:return "Review the event timeline and monitor the affected identity or asset for additional anomalies."
    return "Continue monitoring; validate context if the activity is unexpected."
