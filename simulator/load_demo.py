from __future__ import annotations
import json,sys
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
TOKEN_URL="http://127.0.0.1:8000/api/auth/login"
EVENT_URL="http://127.0.0.1:8000/api/events/bulk"
def main(path="datasets/synthetic/demo_events.jsonl",username="admin",password="ChangeMe123!"):
    data=[json.loads(x) for x in (ROOT/path).read_text(encoding="utf-8").splitlines() if x.strip()]
    r=requests.post(TOKEN_URL,json={"username":username,"password":password},timeout=15); r.raise_for_status(); token=r.json()["access_token"]
    for i in range(0,len(data),250):
        rr=requests.post(EVENT_URL,headers={"Authorization":f"Bearer {token}"},json=data[i:i+250],timeout=30); rr.raise_for_status(); print(rr.json()["count"])
if __name__=="__main__": main(*(sys.argv[1:] or ["datasets/synthetic/demo_events.jsonl"]))
