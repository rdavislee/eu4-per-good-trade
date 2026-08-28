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
unre = []; tot_un = 0.0; tot_all = 0.0
for g in GL:
    gi = GI[g]; c = C0[gi]
    srcs = [i for i in range(N) if GP[gi][i] > 0]
    rs = reach(RK[g]["rank_dir"], srcs)
    un = c.sum() - c[list(rs)].sum()
    unre.append(un / c.sum())
    tot_un += un; tot_all += c.sum()
print("unweighted per-good mean unreachable : %.4f%%" % (100*np.mean(unre)))
print("value-weighted unreachable           : %.4f%%" % (100*tot_un/tot_all))
# genua a cloves sink?
gi = GI['cloves']; d = RK['cloves']["rank_dir"]
od = collections.Counter(u for u,_ in d)
sk = [ORDER[i] for i in range(N) if od[i]==0 and (S0[gi][i]>0 or C0[gi][i]>0)]
srcs=[i for i in range(N) if GP[gi][i]>0]
rs=reach(d,srcs)
print("cloves RANK sinks:", sorted(sk))
print("genua in cloves sinks:", NIDX['genua'] in [i for i in range(N) if od[i]==0])
print("genua reachable from cloves source:", NIDX['genua'] in rs, "| sources:", [ORDER[i] for i in srcs])
