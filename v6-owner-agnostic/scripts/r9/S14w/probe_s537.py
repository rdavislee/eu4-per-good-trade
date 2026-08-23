import numpy as np, collections
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of, has_cycle

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
gidx = {g: gi for gi, g in GL}

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])

for good in ("cloves", "spices"):
    gi = gidx[good]
    b = S[gi] - C[gi]
    r = run_drain(b)
    directed = r["directed"]
    outd = collections.Counter(u for u,_ in directed)
    ind  = collections.Counter(v for _,v in directed)
    sources = sorted(ORDER[i] for i in range(N) if ind[i]==0 and outd[i]>0)
    sinks = sorted(ORDER[i] for i in range(N) if outd[i]==0)
    print(good, "sources:", sources)
    print(good, "sinks:", sinks)
    # demand rank of sinks
    Cg = C[gi]
    order = np.argsort(-Cg)
    rank = {ORDER[order[k]]: k+1 for k in range(N)}
    print(good, "sink demand ranks:", [(s, rank[s]) for s in sinks])
    print()
