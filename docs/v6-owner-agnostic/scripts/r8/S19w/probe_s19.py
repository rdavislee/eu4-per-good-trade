# -*- coding: utf-8 -*-
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import drain
import flowop
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS,
                    PRICES, ROWS, build_sc)
from drain import (run_drain, sinks_of, phase0, phase1, phase2,
                   sweep_priority, compile_dirs)
from flowop import mincost_flow, ARCS, TIE_EPS, TIE_EPS2

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

B = bw()

print("=== node wealth ranking (raw NODEW = tax+prod_income summed to node) ===")
rank = sorted(range(N), key=lambda i: -NODEW[i])
for r, i in enumerate(rank[:10], 1):
    print("  rank %2d  %-20s  NODEW=%.4f  b_w=%.6f" % (r, ORDER[i], NODEW[i], B[i]))

ec = NIDX["english_channel"]
mex = NIDX["mexico"]
gos = NIDX["gulf_of_siam"]
sev = NIDX["sevilla"]
gen = NIDX["genua"]
print()
print("english_channel NODEW=%.4f rank=%d" % (NODEW[ec], rank.index(ec)+1))
print("mexico          NODEW=%.4f rank=%d" % (NODEW[mex], rank.index(mex)+1))
print("gulf_of_siam    NODEW=%.4f rank=%d" % (NODEW[gos], rank.index(gos)+1))
print("genua           NODEW=%.4f rank=%d" % (NODEW[gen], rank.index(gen)+1))
print("sevilla         NODEW=%.4f rank=%d" % (NODEW[sev], rank.index(sev)+1))

print()
print("=== drain run: sinks and where english_channel drains ===")
res = run_drain(B)
d = res["directed"]
sk, src = sinks_of(d)
sinks_named = sorted(ORDER[i] for i in sk)
print("sinks:", sinks_named)
adj = {}
for u, v in d:
    adj.setdefault(u, []).append(v)
print("english_channel out-arcs ->", [ORDER[v] for v in adj.get(ec, [])])
print("english_channel is sink?", ec in sk)
print("genua is sink?", gen in sk)

print()
print("=== flow identity: flow_in - flow_out == -b_w ===")
core, beta, Plog = phase0(B)
Sset, info = phase1(core, beta)
fa, free, net, cost = phase2(core, beta)
print("fa (flow arcs) sample:", list(fa)[:5] if hasattr(fa, '__iter__') else fa)

# Determine flow arc structure -- inspect types
print("type(fa)=", type(fa), "type(free)=", type(free), "type(net)=", type(net))
