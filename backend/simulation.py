from __future__ import annotations
import random,uuid
from datetime import datetime,timedelta,timezone
def _event(ts,event_type,user,device,ip,label="normal",**kw):
    return {"event_id":f"SIM-{uuid.uuid4().hex[:12].upper()}","timestamp":ts,"event_type":event_type,"user_id":user,"device_id":device,"source_ip":ip,"destination_ip":kw.get("destination_ip"),"resource":kw.get("resource"),"action":kw.get("action",event_type.lower()),"status":kw.get("status"),"severity":kw.get("severity","low"),"asset_id":kw.get("asset_id"),"session_id":kw.get("session_id"),"cve_id":kw.get("cve_id"),"metadata":{**kw.get("metadata",{}),"label":label}}
def build_demo_events(scenario="account_compromise",count=30,seed=42):
    rng=random.Random(seed); now=datetime.now(timezone.utc); out=[]
    if scenario=="normal":
        for i in range(count):
            user=f"USR-{rng.randint(1,5):03d}"; device=f"DEV-{int(user[-3:]):03d}"; ip=f"10.0.0.{rng.randint(10,14)}"; typ=rng.choice(["LOGIN_SUCCESS","LOGOUT","RESOURCE_ACCESS","NETWORK_EVENT"])
            out.append(_event(now-timedelta(minutes=rng.randint(1,600)),typ,user,device,ip,resource=rng.choice(["/home","/profile","/reports"]),status="success",asset_id="ASSET-DEV-01"))
        return out
    if scenario=="account_compromise":
        user="USR-001"; device="DEV-999"; ip="198.51.100.77"; sess="SIM-SESS-01"; base=now
        seq=[("LOGIN_FAILURE","failed","medium",None),("LOGIN_FAILURE","failed","medium",None),("LOGIN_FAILURE","failed","medium",None),("LOGIN_FAILURE","failed","medium",None),("LOGIN_FAILURE","failed","medium",None),("NEW_DEVICE",None,"medium",None),("NEW_IP",None,"medium",None),("LOGIN_SUCCESS","success","high",None),("PRIVILEGE_CHANGE","success","high","/admin"),("RESOURCE_ACCESS","success","critical","/db/export")]
        for i,(typ,status,sev,res) in enumerate(seq): out.append(_event(base+timedelta(seconds=i*45),typ,user,device,ip,label="attack",status=status,severity=sev,resource=res,asset_id="ASSET-DB-01",session_id=sess,metadata={"bytes":20000000 if typ=="RESOURCE_ACCESS" else 0}))
        if count>len(out):out+=build_demo_events("normal",count-len(out),seed+1)
        return out
    return build_demo_events("normal",max(0,count-8),seed)+build_demo_events("account_compromise",seed=seed)[0:8]
