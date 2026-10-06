from __future__ import annotations
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.models import Event, Rule
DEFAULT_RULES=[
{"rule_id":"BRUTE_FORCE_5","name":"Repeated Failed Logins","description":"Five or more failed logins for one user within five minutes.","severity":"high","score":45,"conditions":{"type":"failed_logins_window","count":5,"minutes":5}},
{"rule_id":"NEW_DEVICE_PRIV","name":"New Device + Privileged Access","description":"New device activity followed by privileged resource access.","severity":"high","score":65,"conditions":{"type":"new_device_privilege"}},
{"rule_id":"NEW_IP_SUCCESS","name":"New IP After Failed Logins","description":"Successful login from an IP not previously observed for the user after failures.","severity":"medium","score":30,"conditions":{"type":"new_ip_after_failures"}},
{"rule_id":"KEV_EXPOSED","name":"Known Exploited Vulnerability on Exposed Asset","description":"CISA KEV vulnerability associated with an internet-facing asset.","severity":"critical","score":35,"conditions":{"type":"kev_exposed"}}]
def ensure_default_rules(db:Session):
    existing={r.rule_id for r in db.scalars(select(Rule)).all()}
    for item in DEFAULT_RULES:
        if item["rule_id"] not in existing: db.add(Rule(**item))
    db.commit()
def apply_rules(db:Session,event:Event)->tuple[float,list[dict]]:
    rules=list(db.scalars(select(Rule).where(Rule.enabled==True)).all()); total=0.0; matches=[]; start=event.timestamp-timedelta(minutes=5)
    recent=list(db.scalars(select(Event).where(Event.timestamp>=start,Event.timestamp<=event.timestamp,Event.user_id==event.user_id)).all()) if event.user_id else []; failures=[x for x in recent if x.event_type=="LOGIN_FAILURE"]
    for rule in rules:
        t=rule.conditions.get("type"); matched=False; evidence={}
        if t=="failed_logins_window": matched=len(failures)>=int(rule.conditions.get("count",5)); evidence={"failed_logins":len(failures),"window_minutes":5}
        elif t=="new_device_privilege": matched=event.event_type in {"PRIVILEGE_CHANGE","RESOURCE_ACCESS"} and any(x.event_type=="NEW_DEVICE" for x in recent); evidence={"new_device_seen":matched,"event_type":event.event_type}
        elif t=="new_ip_after_failures":
            ips={x.source_ip for x in recent if x.source_ip}; matched=event.event_type=="LOGIN_SUCCESS" and len(failures)>=2 and event.source_ip is not None and len(ips)>1; evidence={"failed_logins":len(failures),"observed_ips":list(ips)}
        elif t=="kev_exposed":
            md=event.metadata_json or {}; matched=bool(event.event_type=="VULNERABILITY_EVENT" and md.get("kev") and md.get("internet_exposed")); evidence={"kev":bool(md.get("kev")),"internet_exposed":bool(md.get("internet_exposed")),"cve_id":event.cve_id}
        if matched: total+=rule.score; matches.append({"rule_id":rule.rule_id,"name":rule.name,"severity":rule.severity,"score":rule.score,"evidence":evidence})
    return min(total,100.0),matches
