import os,sys,collections
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N,ORDER,NIDX,GOODS,PRICES,build_sc
from drain import run_drain
ALPHA=lambda g: max(0.2,min(3.0,(PRICES[g]/2.0)**1.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
GL=[(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]
out=collections.Counter(); sink=collections.Counter()
for gi,g in GL:
    d=run_drain(S[gi]-C[gi])["directed"]
    od=collections.Counter(u for u,v in d)
    for n in range(N):
        if od[n]>0: out[n]+=1
        else: sink[n]+=1
nodes_never_out=[ORDER[n] for n in range(N) if out[n]==0]
print("live goods:",len(GL))
print("nodes with out-degree 0 for EVERY good (globally inert nodes):",nodes_never_out)
print("min goods-with-outgoing over nodes:",min(out[n] for n in range(N)),"max:",max(out[n] for n in range(N)))
print("nodes that are a sink for at least one good:",sum(1 for n in range(N) if sink[n]>0))
