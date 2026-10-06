from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field, ConfigDict
class LoginRequest(BaseModel): username:str; password:str
class TokenResponse(BaseModel): access_token:str; token_type:str="bearer"
class UserOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    user_id:str; username:str; role:str
class EventIn(BaseModel):
    event_id:str|None=None; timestamp:datetime; event_type:str; user_id:str|None=None; device_id:str|None=None; source_ip:str|None=None; destination_ip:str|None=None; resource:str|None=None; action:str|None=None; status:str|None=None; severity:str="low"; asset_id:str|None=None; session_id:str|None=None; cve_id:str|None=None; metadata:dict[str,Any]=Field(default_factory=dict)
class IncidentUpdate(BaseModel): status:str
class EventOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    event_id:str; timestamp:datetime; event_type:str; user_id:str|None; device_id:str|None; source_ip:str|None; destination_ip:str|None; resource:str|None; action:str|None; status:str|None; severity:str; asset_id:str|None; session_id:str|None; cve_id:str|None; metadata_json:dict; rule_score:float; anomaly_score:float; correlation_score:float; threat_score:float
class IncidentOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    incident_id:str; title:str; description:str; risk_score:float; severity:str; status:str; created_at:datetime; updated_at:datetime; affected_users:list; affected_devices:list; affected_ips:list; affected_assets:list; related_vulnerabilities:list; evidence:list; recommended_action:str
class AssetIn(BaseModel):
    asset_id:str; hostname:str|None=None; ip:str|None=None; type:str="server"; criticality:str="MEDIUM"; internet_exposed:bool=False; owner:str|None=None; environment:str="lab"
class VulnerabilityIn(BaseModel):
    cve_id:str; description:str=""; cvss:float|None=None; severity:str="UNKNOWN"; kev:bool=False; affected_products:list=Field(default_factory=list); published_at:str|None=None; last_modified:str|None=None; source:str="local"
class DashboardSummary(BaseModel):
    total_events:int; events_last_hour:int; critical_incidents:int; high_risk_users:int; high_risk_assets:int; open_incidents:int; anomalies_last_hour:int; vulnerabilities:int; kev_vulnerabilities:int
class ForensicGraphOut(BaseModel): nodes:list[dict]; edges:list[dict]
