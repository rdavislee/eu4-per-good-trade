# -*- coding: utf-8 -*-
"""val part3: the 19 aggregate-graph facts round6.py checks, under DEF-descending (def_beta) vs
shipped (defasc_beta), on the same 1444 field."""
import collections, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from solver import N, ORDER, NIDX, ROWS, UND
from drain import run_drain, phase0, phase1, phase2, sweep_priority, compile_dirs, has_cycle

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
_t = (W / W.max()) ** 2.0
_n = np.zeros(N); np.add.at(_n, PN, _t)
BW = np.full(N, 1.0 / N) - _n / _n.sum()
CW = _n / _n.sum()
cape = NIDX["cape_of_good_hope"]
genua = NIDX["genua"]

def facts(key):
    core, beta, Plog = phase0(BW)
    Sset, _ = phase1(core, beta)
    fa, free, net, _c = phase2(core, beta)
    o_, _S2, promo, fb = sweep_priority(core, beta, Sset, fa, free, net, key)
    d = compile_dirs(core, o_, fa, free, Plog, beta)
    D = set(d)
    od = collections.Counter(u for u, _ in D); idg = collections.Counter(v for _, v in D)
    sinks = sorted(ORDER[i] for i in range(N) if od[i] == 0)
    sources = sorted(ORDER[i] for i in range(N) if idg[i] == 0)
    rank = {i: r for r, i in enumerate(sorted(range(N), key=lambda j: -CW[j]), 1)}
    src_idx = [NIDX[x] for x in sources]
    adj = collections.defaultdict(list)
    for u, v in D: adj[u].append(v)
    def reach(a):
        seen = {a}; q = collections.deque([a])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in seen: seen.add(y); q.append(y)
        return seen
    RCH = {i: reach(i) for i in range(N)}
    up = [i for i in range(N) if i != cape and cape in RCH[i]]
    down = RCH[cape] - {cape}
    cape_pairs = sum(1 for a in up for b in down if b != a and b in RCH[a])
    ec_genua_2hop = (NIDX["english_channel"], NIDX["champagne"]) in D and (NIDX["champagne"], genua) in D
    return dict(
        sinks=sinks, promo=promo, fb=fb, acyclic=has_cycle(D) is None,
        edges_oriented=len(D), sources=sources,
        src_rank_range=(min(rank[i] for i in src_idx), max(rank[i] for i in src_idx)) if src_idx else None,
        src_meandeg=float(np.mean([len(UND[i]) for i in src_idx])) if src_idx else None,
        genua_deg=(idg[genua], od[genua]),
        cape_deg=(idg[cape], od[cape]),
        cape_pairs=cape_pairs,
        white_sea_reaches_hangzhou=NIDX["hangzhou"] in RCH[NIDX["white_sea"]],
        sevilla_reaches_ganges=NIDX["ganges_delta"] in RCH[NIDX["sevilla"]],
        sevilla_reaches_asian_end=any(s in [NIDX[x] for x in sinks if x not in
                                             ("english_channel","genua","rheinland","north_sea","baltic_sea",
                                              "white_sea","novgorod","lubeck","saxony","wien","krakow","pest",
                                              "venice","ragusa","champagne","bordeaux","valencia","sevilla",
                                              "constantinople","crimea","kiev","kazan")]
                                       for s in RCH[NIDX["sevilla"]]),
        ec_genua_2hop=ec_genua_2hop,
    )

ship = facts("defasc_beta")
desc = facts("def_beta")
print("SHIPPED (defasc_beta):")
for k, v in ship.items(): print("  %-28s %s" % (k, v))
print("\nDEF-DESCENDING (def_beta):")
for k, v in desc.items(): print("  %-28s %s" % (k, v))
print("\nDIFFERENCES:")
for k in ship:
    if ship[k] != desc[k]:
        print("  %-28s shipped=%s  descending=%s" % (k, ship[k], desc[k]))
