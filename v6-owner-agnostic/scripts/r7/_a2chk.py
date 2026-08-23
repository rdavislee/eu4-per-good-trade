import os,sys,collections
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N,ORDER,NIDX,EDGES_UND,GOODS,PRICES,build_sc
from drain import run_drain, sinks_of
import measure6 as M
def eid(u,v):
    for ei,(a,b) in enumerate(EDGES_UND):
        if {a,b}=={u,v}: return ei
    return None
def audit(label,r):
    D=set(r["directed"]); free=set(r["free"]); flow=set(r["flow_arc"].keys())
    sk,_=sinks_of(r["directed"])
    sk=set(sk)
    out=collections.defaultdict(list)
    for u,v in D: out[u].append(eid(u,v))
    neither=[ei for ei in range(len(EDGES_UND)) if ei not in free and ei not in flow]
    both=[ei for ei in range(len(EDGES_UND)) if ei in free and ei in flow]
    ends_with_arc=[ORDER[n] for n in sk if out[n]]
    nonends_without=[ORDER[n] for n in range(N) if n not in sk and not out[n]]
    freeonly=[n for n in range(N) if out[n] and all(e in free for e in out[n])]
    return dict(ends=len(sk),ends_with_arc=ends_with_arc,nonends_without=nonends_without,
                neither=len(neither),both=len(both),freeonly=len(freeonly))
agg=audit("AGG",M.ph())
print("AGGREGATE:",agg)
ALPHA=lambda g: max(0.2,min(3.0,PRICES[g]/2.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
GL=[(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]
bad=[];tot_neither=0;tot_both=0
for gi,g in GL:
    a=audit(g,run_drain(S[gi]-C[gi]))
    tot_neither+=a["neither"]; tot_both+=a["both"]
    if a["ends_with_arc"] or a["nonends_without"]: bad.append((g,a))
print("per-good over %d goods: ends-with-an-out-arc + non-ends-without = %d goods violating; arcs neither flow nor free = %d ; arcs both = %d"%(len(GL),len(bad),tot_neither,tot_both))
print("violations:",bad)
