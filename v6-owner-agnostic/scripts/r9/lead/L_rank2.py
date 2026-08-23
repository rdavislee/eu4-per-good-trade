import os, sys
sys.path.insert(0, os.path.abspath('.')); os.chdir(os.path.abspath('.'))
import numpy as np, collections
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from rankop import run as rank_run
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GI = {g: GOODS.index(g) for g in GL}
RK = rank_run()
def reach(d, srcs):
    adj = collections.defaultdict(list)
    for u, v in d: adj[u].append(v)
    seen = set(srcs); st = list(srcs)
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); st.append(v)
    return seen
print("C0 row sums (first 5):", [round(float(C0[GI[g]].sum()),6) for g in GL[:5]])
print("V shape/type:", type(V), np.shape(V))
frac=[]; wts=[]
for g in GL:
    gi=GI[g]; c=C0[gi]
    srcs=[i for i in range(N) if GP[gi][i]>0]
    rs=reach(RK[g]["rank_dir"], srcs)
    frac.append(1.0 - c[list(rs)].sum()/c.sum())
    wts.append(float(np.sum(V[gi])) if np.ndim(V)>1 else float(V[gi]))
frac=np.array(frac); wts=np.array(wts)
print("unweighted mean  : %.4f%%" % (100*frac.mean()))
print("value-weighted   : %.4f%%" % (100*(frac*wts).sum()/wts.sum()))
