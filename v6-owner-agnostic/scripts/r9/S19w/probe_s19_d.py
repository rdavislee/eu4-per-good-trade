import numpy as np
import drain, flowop
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, EDGES_UND, build_sc
from drain import run_drain, has_cycle

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

# accumulate value-weighted net per undirected edge
agg_net = np.zeros(len(EDGES_UND))
for gi, g in GL:
    b = S[gi] - C[gi]
    r = run_drain(b)
    net = r.get("net")
    if net is None:
        continue
    agg_net += V[gi] * np.asarray(net)

# build directed graph from sign of agg_net (edges with nonzero weight)
directed = []
for ei, (u, v) in enumerate(EDGES_UND):
    if agg_net[ei] > 1e-9:
        directed.append((u, v))
    elif agg_net[ei] < -1e-9:
        directed.append((v, u))

cyc = has_cycle(directed)
print("edges in value-weighted net-flow graph:", len(directed), "of", len(EDGES_UND))
print("has_cycle ->", cyc)
if cyc:
    print("cycle nodes:", [ORDER[i] for i in cyc])
