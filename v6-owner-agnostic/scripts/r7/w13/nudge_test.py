# -*- coding: utf-8 -*-
"""Reproduce Y656: 29 goods x 6 random 1e-9 demand nudges -> support-membership churn,
and +/-1% wealth noise on six seeds -> aggregate edge-orientation churn.
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

from solver import N, ORDER, NIDX, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import phase0, phase1, phase2, run_drain, sinks_of

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("live goods:", len(GL))

def support_partition(b):
    core, beta, Plog = phase0(b)
    if len(core) <= 1:
        return set(), set(), {}
    flow_arc, free, net, cost = phase2(core, beta)
    support_edges = set(flow_arc.keys())
    free_edges = set(free)
    return support_edges, free_edges, dict(net_by_edge={ei: net[ei] for ei in range(len(EDGES_UND))})

rng = np.random.default_rng(12345)

print()
print("=== PART 1: per-good demand nudges (29 goods x 6 seeds of 1e-9 magnitude) ===")
total_trials = 0
total_membership_changes = 0
max_flow_on_changed_edge = 0.0
worst = None
per_good_changes = {}
for gi, g in GL:
    b0 = S[gi] - C[gi]
    sup0, free0, aux0 = support_partition(b0)
    changes_this_good = 0
    for seed in range(6):
        nudge = rng.normal(0.0, 1e-9, size=N)
        nudge -= nudge.mean()  # b must sum to 0 (mass balance) for the flow LP to stay feasible
        b1 = b0 + nudge
        sup1, free1, aux1 = support_partition(b1)
        total_trials += 1
        # edges that flipped membership (support <-> free) between baseline and nudged
        flipped = (sup0 ^ sup1)  # symmetric difference among edges considered (only those in either)
        # also consider edges only classified in one due to core changing; treat conservatively
        for ei in flipped:
            changes_this_good += 1
            total_membership_changes += 1
            f0 = abs(aux0['net_by_edge'].get(ei, 0.0))
            f1 = abs(aux1['net_by_edge'].get(ei, 0.0))
            mflow = max(f0, f1)
            if mflow > max_flow_on_changed_edge:
                max_flow_on_changed_edge = mflow
                worst = (g, seed, ei, f0, f1)
    per_good_changes[g] = changes_this_good

print("total (good,seed) trials:", total_trials)
print("total support-membership changes observed:", total_membership_changes)
print("goods with >=1 membership change:", [g for g, c in per_good_changes.items() if c > 0])
print("max |flow| observed on any changed edge:", max_flow_on_changed_edge)
if worst:
    print("worst case:", worst)
print("claim check: zero changes moved more than 1e-6 of flow ->",
      (max_flow_on_changed_edge <= 1e-6) if total_membership_changes > 0 else "N/A (zero membership changes at all)")

print()
print("=== PART 2: aggregate map under +/-1% wealth noise, six seeds ===")
A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)

def bw_from_provw(provw, alpha=A_PHI):
    t = (provw / provw.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

base_b = bw_from_provw(W)
base = run_drain(base_b)
base_directed = set(base["directed"])
print("baseline sinks:", [ORDER[i] for i in sinks_of(base_directed)[0]])
print("baseline edges oriented:", len(base_directed))

rng2 = np.random.default_rng(999)
edges_moved_total = 0
for seed in range(6):
    # +/-1% multiplicative noise applied PER PROVINCE ROW before aggregating to node wealth,
    # matching m6.out's own "sinks under +/-1% wealth noise" methodology (perturb the underlying
    # province wealth W, not the aggregated NODEW, to avoid perfectly-correlated per-node noise).
    noise = rng2.uniform(-0.01, 0.01, size=len(W))
    Wp = W * (1.0 + noise)
    bp = bw_from_provw(Wp)
    rp = run_drain(bp)
    directed_p = set(rp["directed"])
    diff = base_directed ^ directed_p
    # only count as "moved" an edge whose orientation actually differs (same edge, opposite dir),
    # not edges present in one set only because sink-count/core differs trivially
    moved = 0
    base_pairs = {frozenset((u, v)) for (u, v) in base_directed}
    p_pairs = {frozenset((u, v)) for (u, v) in directed_p}
    for (u, v) in base_directed:
        if (v, u) in directed_p:
            moved += 1
    print(f"  seed {seed}: sinks={[ORDER[i] for i in sinks_of(directed_p)[0]]}  "
          f"edges differing (symmetric diff of directed-edge sets)={len(diff)}  "
          f"edges with REVERSED orientation={moved}  "
          f"edge SET (undirected) identical={base_pairs==p_pairs}")
    edges_moved_total += moved

print("total reversed-orientation edges across 6 seeds:", edges_moved_total)
print("claim check: aggregate map moved no edge at all ->", edges_moved_total == 0)
