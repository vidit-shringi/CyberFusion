from __future__ import annotations
import httpx
from backend.config import settings
async def fetch_cisa_kev()->list[dict]:
    async with httpx.AsyncClient(timeout=20) as client:
        r=await client.get(settings.cisa_kev_url); r.raise_for_status(); data=r.json()
    return data.get("vulnerabilities",[])
async def fetch_nvd_cve(cve_id:str)->dict|None:
    headers={"apiKey":settings.nvd_api_key} if settings.nvd_api_key else {}; url="https://services.nvd.nist.gov/rest/json/cves/2.0"
    async with httpx.AsyncClient(timeout=20,headers=headers) as client:
        r=await client.get(url,params={"cveId":cve_id})
        if r.status_code==404:return None
        r.raise_for_status(); data=r.json()
    vulns=data.get("vulnerabilities",[]); return vulns[0].get("cve") if vulns else None
