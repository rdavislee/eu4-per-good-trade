import os,sys,collections
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N,ORDER,NIDX,ROWS,GOODS,PRICES,EDGES_UND
import flowop, drain
from flowop import ARCS
import measure6 as M
# --- (c) are mexico / gulf_of_siam out-arcs FREE edges?
r=M.ph()
free=set(r["free"]); flow=set(r["flow_arc"]) if not isinstance(r["flow_arc"],dict) else set(r["flow_arc"].keys())
D=set(r["directed"])
print("free type",type(r["free"]),"len",len(r["free"]),"| flow_arc type",type(r["flow_arc"]),"len",len(r["flow_arc"]))
for n in ("mexico","gulf_of_siam","english_channel","sevilla"):
    i=NIDX[n]
    outs=[(u,v) for u,v in D if u==i]
    eidx=[]
    for (u,v) in outs:
        for ei,(a,b) in enumerate(EDGES_UND):
            if {a,b}=={u,v}: eidx.append(ei)
    print("%-16s out-arcs %s edge-ids %s  free? %s  flow? %s"%(n,[ORDER[v] for u,v in outs],eidx,[e in free for e in eidx],[e in flow for e in eidx]))
