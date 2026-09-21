#!/usr/bin/env python3
import argparse, json, os, time
from pathlib import Path

COMPETENCIES = [
"pronomes_agencia","voz_distanciamento","afiliacao_ordem","palavras_funcionais","poder_status",
"ansiedade_raiva","negacao_evasao","carga_complexidade","blefe_impressao","estrutura_relato",
"detalhes_perspectiva","transicoes_verificabilidade","manipulacao","estado_traco","identidade_vieses",
"defesas","valores_autorregulacao","resiliencia_perspectiva","relacoes_sofrimento","risco_calibracao"
]

def home():
    base = Path(os.environ.get("OPENJARVIS_HOME", Path.home()/".openjarvis"))
    return base / "mindreader-trainer-v2" / "progress.json"

def default():
    return {"version":2,"created":int(time.time()),"sessions":0,"competencies":{
        c:{"attempts":0,"points":0,"max_points":0,"level":1,"last":None,"errors":[]} for c in COMPETENCIES
    },"cards":{},"history":[]}

def load():
    p=home(); p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():
        d=default(); p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8"); return d
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return default()

def save(d):
    p=home(); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")

def cmd_show(_):
    d=load(); rows=[]
    for c,v in d["competencies"].items():
        pct = round(100*v["points"]/v["max_points"],1) if v["max_points"] else 0
        rows.append((pct,v["attempts"],v["level"],c))
    rows.sort()
    print(json.dumps({"sessions":d["sessions"],"weakest":[{"competency":c,"score":p,"attempts":a,"level":l} for p,a,l,c in rows[:5]],"strongest":[{"competency":c,"score":p,"attempts":a,"level":l} for p,a,l,c in rows[-5:][::-1]]},ensure_ascii=False,indent=2))

def cmd_record(a):
    d=load(); c=a.competency
    if c not in d["competencies"]: raise SystemExit(f"competência inválida: {c}")
    v=d["competencies"][c]; v["attempts"]+=1; v["points"]+=a.points; v["max_points"]+=a.max; v["last"]=int(time.time())
    pct=v["points"]/v["max_points"] if v["max_points"] else 0
    v["level"]= min(5,max(1, 1+int(pct*5)))
    if a.error:
        v["errors"].append({"t":int(time.time()),"text":a.error}); v["errors"]=v["errors"][-20:]
    d["history"].append({"t":int(time.time()),"competency":c,"points":a.points,"max":a.max,"error":a.error or ""}); d["history"]=d["history"][-500:]
    save(d); print("ok")

def cmd_card(a):
    d=load(); now=int(time.time()); intervals={0:1,1:3,2:7,3:21}
    days=intervals[a.grade]; d["cards"][a.card]={"grade":a.grade,"last":now,"due":now+days*86400}
    save(d); print(json.dumps(d["cards"][a.card],indent=2))

def cmd_due(a):
    d=load(); now=int(time.time()); due=[k for k,v in d["cards"].items() if v.get("due",0)<=now]
    print(json.dumps(due[:a.limit],ensure_ascii=False,indent=2))

def cmd_session(_):
    d=load(); d["sessions"]+=1; save(d); print(d["sessions"])

def cmd_reset(a):
    if a.confirm != "RESETAR": raise SystemExit("use --confirm RESETAR")
    save(default()); print("resetado")

p=argparse.ArgumentParser()
sp=p.add_subparsers(dest="cmd",required=True)
q=sp.add_parser("show"); q.set_defaults(fn=cmd_show)
q=sp.add_parser("record"); q.add_argument("competency"); q.add_argument("points",type=float); q.add_argument("max",type=float); q.add_argument("--error"); q.set_defaults(fn=cmd_record)
q=sp.add_parser("card"); q.add_argument("card"); q.add_argument("grade",type=int,choices=[0,1,2,3]); q.set_defaults(fn=cmd_card)
q=sp.add_parser("due"); q.add_argument("--limit",type=int,default=20); q.set_defaults(fn=cmd_due)
q=sp.add_parser("session"); q.set_defaults(fn=cmd_session)
q=sp.add_parser("reset"); q.add_argument("--confirm"); q.set_defaults(fn=cmd_reset)
a=p.parse_args(); a.fn(a)
