from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.database.models import Event, Incident, ForensicNode, ForensicEdge
def upsert_node(db:Session,node_id:str,node_type:str,label:str,properties:dict|None=None):
    node=db.scalar(select(ForensicNode).where(ForensicNode.node_id==node_id))
    if not node: node=ForensicNode(node_id=node_id,node_type=node_type,label=label,properties=properties or {}); db.add(node)
    else:
        node.label=label
        if properties: node.properties=properties
    return node
def add_edge(db:Session,source:str,target:str,relationship:str,properties:dict|None=None):
    exists=db.scalar(select(ForensicEdge).where(ForensicEdge.source_node_id==source,ForensicEdge.target_node_id==target,ForensicEdge.relationship==relationship))
    if not exists: db.add(ForensicEdge(source_node_id=source,target_node_id=target,relationship=relationship,properties=properties or {}))
def update_forensic_graph(db:Session,event:Event,related:list[Event],incident:Incident|None):
    event_node=f"EVENT:{event.event_id}"; upsert_node(db,event_node,"EVENT",event.event_id,{"type":event.event_type,"timestamp":event.timestamp.isoformat()})
    if event.user_id:
        user_node=f"USER:{event.user_id}"; upsert_node(db,user_node,"USER",event.user_id); add_edge(db,user_node,event_node,"GENERATED_EVENT")
    if event.device_id:
        dev_node=f"DEVICE:{event.device_id}"; upsert_node(db,dev_node,"DEVICE",event.device_id); add_edge(db,event.user_id and f"USER:{event.user_id}" or event_node,dev_node,"USED_DEVICE"); add_edge(db,dev_node,event_node,"GENERATED_EVENT")
    if event.source_ip:
        ip_node=f"IP:{event.source_ip}"; upsert_node(db,ip_node,"IP",event.source_ip)
        if event.user_id:add_edge(db,f"USER:{event.user_id}",ip_node,"OBSERVED_FROM")
        add_edge(db,event_node,ip_node,"FROM_IP")
    if event.resource:
        res_node=f"RESOURCE:{event.resource}"; upsert_node(db,res_node,"RESOURCE",event.resource); add_edge(db,event_node,res_node,"ACCESSED_RESOURCE")
    if event.asset_id:
        asset_node=f"ASSET:{event.asset_id}"; upsert_node(db,asset_node,"ASSET",event.asset_id); add_edge(db,event_node,asset_node,"AFFECTED_ASSET")
    if event.cve_id:
        cve_node=f"CVE:{event.cve_id}"; upsert_node(db,cve_node,"VULNERABILITY",event.cve_id); add_edge(db,event_node,cve_node,"REFERENCES_VULNERABILITY")
    if incident:
        inc_node=f"INCIDENT:{incident.incident_id}"; upsert_node(db,inc_node,"INCIDENT",incident.incident_id,{"risk_score":incident.risk_score}); add_edge(db,event_node,inc_node,"CONTRIBUTED_TO_INCIDENT")
        for e in related:
            if e.event_id!=event.event_id:
                rel_node=f"EVENT:{e.event_id}"; upsert_node(db,rel_node,"EVENT",e.event_id,{"type":e.event_type,"timestamp":e.timestamp.isoformat()}); add_edge(db,rel_node,inc_node,"RELATED_TO_INCIDENT")
    db.flush()
def get_graph(db:Session,incident_id:str|None=None):
    nodes=list(db.scalars(select(ForensicNode)).all()); edges=list(db.scalars(select(ForensicEdge)).all())
    if not incident_id:return nodes,edges
    inc_node=f"INCIDENT:{incident_id}"; allowed={inc_node}; changed=True
    while changed:
        changed=False
        for e in edges:
            if e.target_node_id in allowed and e.source_node_id not in allowed: allowed.add(e.source_node_id); changed=True
            if e.source_node_id in allowed and e.target_node_id not in allowed and e.relationship in {"CONTRIBUTED_TO_INCIDENT","RELATED_TO_INCIDENT","AFFECTED_ASSET","REFERENCES_VULNERABILITY","FROM_IP","ACCESSED_RESOURCE","GENERATED_EVENT","USED_DEVICE","OBSERVED_FROM"}: allowed.add(e.target_node_id); changed=True
    return [n for n in nodes if n.node_id in allowed],[e for e in edges if e.source_node_id in allowed and e.target_node_id in allowed]
