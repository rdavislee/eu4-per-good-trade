# -*- coding: utf-8 -*-
"""Reference orientation dump for the cross-implementation check (spec 2.8, TESTING A5).

Replicates measure6.py's exact constructions (its cv/ph aggregate and its per-good S/C loops)
by importing the reference modules unmodified, then writes one JSON with every orientation:
Phi_w plus the 29 live goods -- directed edges, sinks, sources, Phase-1 selection, promotions,
fallbacks, marking order, flow/free classification, net flows, beta, and the inputs (wealth
field, node wealth, alpha, prices) at full float precision.

The C++ implementation in impl/ dumps the same schema; compare.py diffs the two. Where they
disagree on orientation the reference is correct by definition (spec 2.8).

Usage:  python refdump.py [out.json]
"""
import os, sys, json, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", "v6-owner-agnostic", "scripts"))
sys.path.insert(0, SCRIPTS)

from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS,
                    GOODS_PRODUCED_FACTOR, TAX_COEFF, build_sc)
from drain import run_drain, NODEW
from flowop import TIE_COST, ARCS

A_PHI = 2.0
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])


def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N)
    np.add.at(n, pn, t)
    return n / n.sum()


def graph_record(name, r):
    """Everything the comparison needs, node names not indices, floats via repr round-trip."""
    directed = sorted((ORDER[u], ORDER[v]) for u, v in r["directed"])
    od = collections.Counter(u for u, _ in r["directed"])
    ind = collections.Counter(v for _, v in r["directed"])
    sinks = sorted(ORDER[i] for i in range(N) if od[i] == 0)
    sources = sorted(ORDER[i] for i in range(N) if ind[i] == 0)
    rec = {
        "name": name,
        "directed": ["%s>%s" % e for e in directed],
        "sinks": sinks,
        "sources": sources,
        "S0": sorted(ORDER[i] for i in r.get("S0", set())),
        "promotions": [ORDER[i] for i in r.get("promotions", [])],
        "fallbacks": [ORDER[i] for i in r.get("fallbacks", [])],
        "order": {ORDER[v]: t for v, t in r.get("order", {}).items()},
        "flow_edges": sorted("%s>%s" % (ORDER[u], ORDER[v])
                             for u, v in r.get("flow_arc", {}).values()),
        "free_edges": sorted("%s-%s" % (ORDER[EDGES_UND[ei][0]], ORDER[EDGES_UND[ei][1]])
                             for ei in r.get("free", [])),
        "net": {("%s-%s" % (ORDER[u], ORDER[v])): repr(float(r["net"][ei]))
                for ei, (u, v) in enumerate(EDGES_UND)} if "net" in r else {},
        "beta": {ORDER[i]: repr(float(r["beta"][i])) for i in range(N)} if "beta" in r else {},
        "cost": repr(float(r["cost"])),
    }
    return rec


def main(out_path):
    _, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
    GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

    # per-good supply from prod_income node sums, demand from (W/W.max())^alpha -- measure6's loop
    val = {g: np.zeros(N) for _, g in GL}
    for i, r in enumerate(ROWS):
        if r["good"] in val:
            val[r["good"]][pn[i]] += r["prod_income"]

    graphs = []
    base = run_drain(np.full(N, 1.0 / N) - cv(A_PHI))
    graphs.append(graph_record("PHI_W", base))
    for gi, g in GL:
        t = (W / W.max()) ** ALPHA(g)
        n = np.zeros(N)
        np.add.at(n, pn, t)
        C = n / n.sum()
        S = val[g] / val[g].sum()
        graphs.append(graph_record(g, run_drain(S - C)))

    dump = {
        "node_order": ORDER,
        "edges_und": ["%s-%s" % (ORDER[u], ORDER[v]) for u, v in EDGES_UND],
        "goods_live": [g for _, g in GL],
        "gp_coeff": repr(GOODS_PRODUCED_FACTOR),
        "tax_coeff": repr(TAX_COEFF),
        "alpha": {g: repr(ALPHA(g)) for _, g in GL},
        "prices": {g: repr(PRICES[g]) for g in sorted(PRICES)},
        "node_wealth": {ORDER[i]: repr(float(NODEW[i])) for i in range(N)},
        "counted_provinces": len(ROWS),
        "world_wealth": repr(float(W.sum())),
        "wealth_rows": {str(r["pid"]): {"node": r["node"], "good": r["good"],
                                        "tax": repr(r["tax"]),
                                        "trade_value": repr(r["prod_income"])}
                        for r in ROWS},
        "tie_cost": {"%s>%s" % (ORDER[u], ORDER[v]): repr(float(TIE_COST[ai]))
                     for ai, (u, v, ei, sg) in enumerate(ARCS)},
        "graphs": graphs,
    }
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dump, f, indent=0)
    print("wrote %s: %d graphs, %d counted provinces, world wealth %s"
          % (out_path, len(graphs), len(ROWS), dump["world_wealth"]))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dumps", "ref1444.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    main(out)
