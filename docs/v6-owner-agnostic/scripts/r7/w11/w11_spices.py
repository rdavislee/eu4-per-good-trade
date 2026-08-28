import sys, os, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, build_sc
from drain import run_drain

for good in ("spices", "cloves"):
    s, c = build_sc(good)
    b = s - c
    r = run_drain(b)
    o = collections.Counter(u for u,_ in r["directed"])
    sinks = sorted(ORDER[i] for i in range(N) if o[i] == 0)
    # demand rank: nodes ranked by c (demand) descending
    demand_rank = {ORDER[i]: k+1 for k,i in enumerate(np.argsort(-c))}
    print(good, "baseline sinks:", sinks, {n: demand_rank[n] for n in sinks})
    # sources: nodes with net supply s-c>0 and in-degree 0? Let's check graph sources (in-degree 0 among nodes with positive net supply)
    ind = collections.Counter(v for _,v in r["directed"])
    srcs = sorted(ORDER[i] for i in range(N) if ind[i]==0)
    print(good, "graph sources (in-degree 0):", srcs)
