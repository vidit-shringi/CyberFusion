from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from backend.simulation import build_demo_events
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--scenario',choices=['normal','account_compromise','mixed'],default='mixed'); ap.add_argument('--events',type=int,default=1000); ap.add_argument('--seed',type=int,default=42); ap.add_argument('--output',default='datasets/synthetic/demo_events.jsonl'); args=ap.parse_args()
    events=build_demo_events(args.scenario,args.events,args.seed); path=ROOT/args.output; path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8') as f:
        for e in events:f.write(json.dumps(e,default=str)+'\n')
    print(f'Generated {len(events)} events -> {path}')
if __name__=='__main__': main()
