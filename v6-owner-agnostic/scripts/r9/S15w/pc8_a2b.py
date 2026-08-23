# -*- coding: utf-8 -*-
"""A2 revised: is 'an end is a node the orientation gives no out-arc - no flow arc AND no
free edge' true of the shipped operator?  Aggregate + all 29 per-good solves."""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, EDGES_UND, ROWS, GOODS, PRICES, build_sc
from drain import run_drain, sinks_of

EIDX = {tuple(sorted(e)): i for i, e in enumerate(EDGES_UND)}

def audit(tag, r):
    free = set(r["free"]); flow = r["flow_arc"]
    outflow = collections.defaultdict(int); outfree = collections.defaultdict(int)
    other = 0
    for (u, v) in r["directed"]:
        ei = EIDX[tuple(sorted((u, v)))]
        if ei in flow and flow[ei] == (u, v): outflow[u] += 1
        elif ei in free:                      outfree[u] += 1
        else:                                 other += 1          # phase-0 pendant, or reversed flow arc
    sk, od = sinks_of(r["directed"])
    ends = set(sk)
    bad_end = [ORDER[i] for i in ends if outflow[i] or outfree[i]]
    bad_non = [ORDER[i] for i in range(N) if i not in ends and not (outflow[i] or outfree[i])]
    # how many non-ends are kept off the end list by a FREE edge alone (no outgoing flow arc)?
    freeonly = [ORDER[i] for i in range(N) if i not in ends and outflow[i] == 0 and outfree[i] > 0]
    return dict(tag=tag, ends=len(ends), bad_end=bad_end, bad_non=bad_non,
                freeonly=freeonly, other_arcs=other, pend=len(r.get("directed", [])) )

W = np.array([x["tax"] + x["prod_income"] for x in ROWS]); pn = np.array([NIDX[x["node"]] for x in ROWS])
t = (W / W.max()) ** 2.0; nn = np.zeros(N); np.add.at(nn, pn, t)
agg = audit("PHI_W", run_drain(np.full(N, 1.0/N) - nn/nn.sum()))
print("AGGREGATE: ends=%d  ends-with-an-out-arc=%s  non-ends-with-no-out-arc=%s  arcs that are neither flow nor free=%d"
      % (agg["ends"], agg["bad_end"], agg["bad_non"], agg["other_arcs"]))
print("   non-ends held off the end list by a FREE edge alone (%d): %s" % (len(agg["freeonly"]), sorted(agg["freeonly"])))

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, world = build_sc(ALPHA, eps=0.0)
GL = [GOODS[i] for i in range(len(GOODS)) if LIVE[i]]
tot_bad_end = tot_bad_non = tot_other = 0; tot_freeonly = 0
for g in GL:
    j = GOODS.index(g)
    a = audit(g, run_drain(S[j] - C[j]))
    tot_bad_end += len(a["bad_end"]); tot_bad_non += len(a["bad_non"])
    tot_other += a["other_arcs"];     tot_freeonly += len(a["freeonly"])
print("PER-GOOD (%d goods): ends-with-an-out-arc=%d ; non-ends-with-no-out-arc=%d ; arcs neither flow nor free=%d"
      % (len(GL), tot_bad_end, tot_bad_non, tot_other))
print("   non-ends held off the end list by a FREE edge alone, summed over goods: %d" % tot_freeonly)
