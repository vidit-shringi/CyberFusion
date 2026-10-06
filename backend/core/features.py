from __future__ import annotations
from datetime import timedelta
from collections import Counter
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.models import Event
FEATURE_NAMES=["failed_logins_5m","successful_logins_1h","new_device","new_ip","login_hour_deviation","resource_rarity","privilege_change","number_of_destinations","network_volume","process_rarity","session_duration","authentication_frequency"]
def _recent(db:Session,event,minutes:int=60):
    start=event.timestamp-timedelta(minutes=minutes); q=select(Event).where(Event.timestamp>=start,Event.timestamp<=event.timestamp)
    if event.user_id: q=q.where(Event.user_id==event.user_id)
    return list(db.scalars(q).all())
def extract_features(db:Session,event:Event)->dict[str,float]:
    recent_1h=_recent(db,event,60); recent_5m=_recent(db,event,5); failures_5m=sum(1 for x in recent_5m if x.event_type=="LOGIN_FAILURE"); successes_1h=sum(1 for x in recent_1h if x.event_type=="LOGIN_SUCCESS")
    devices={x.device_id for x in recent_1h if x.device_id}; ips={x.source_ip for x in recent_1h if x.source_ip}; destinations={x.destination_ip for x in recent_1h if x.destination_ip}
    resources=[x.resource for x in recent_1h if x.resource]; resource_counts=Counter(resources); current_resource_count=resource_counts.get(event.resource,0) if event.resource else 0
    normal_hours=[x.timestamp.hour for x in recent_1h if x.event_type=="LOGIN_SUCCESS"]; hour_dev=min(abs(event.timestamp.hour-(sum(normal_hours)/len(normal_hours))),12)/12 if normal_hours else 0.5
    return {"failed_logins_5m":float(failures_5m),"successful_logins_1h":float(successes_1h),"new_device":1.0 if event.event_type=="NEW_DEVICE" else 0.0,"new_ip":1.0 if event.event_type=="NEW_IP" else 0.0,"login_hour_deviation":hour_dev,"resource_rarity":1.0/max(current_resource_count,1),"privilege_change":1.0 if event.event_type=="PRIVILEGE_CHANGE" else 0.0,"number_of_destinations":float(len(destinations)),"network_volume":min(sum(float((x.metadata_json or {}).get("bytes",0) or 0) for x in recent_1h)/1_000_000.0,1000.0),"process_rarity":1.0 if event.event_type=="PROCESS_EVENT" and len(recent_1h)<3 else 0.0,"session_duration":min(float((event.metadata_json or {}).get("session_duration_seconds",0) or 0)/3600.0,24.0),"authentication_frequency":min(sum(1 for x in recent_1h if x.event_type.startswith("LOGIN_"))/60.0,10.0)}
