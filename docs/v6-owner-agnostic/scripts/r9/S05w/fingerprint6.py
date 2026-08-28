# -*- coding: utf-8 -*-
"""Determinism fingerprint: Phi_w + all 29 per-good graphs, sinks, sources, promotions,
fallbacks and the Phase-2 objective, hashed. Cited by spec 2.1 and 2.8's Determinism row.

Renamed from p3_fp.py under C4: the spec cites this instrument by name, and a p3_* name says
"round-3 working file", which is not what a cited instrument is.

One run hashes ONE process. Repeat under different PYTHONHASHSEED values to test what a single
process cannot see -- iteration order that varies between processes rather than within one:

    for s in 0 1 2 42 12345 random; do PYTHONHASHSEED=$s python fingerprint6.py; done
"""
import hashlib, os, sys, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import drain
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cvag(a=2.0):
    t = (W / W.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
def rec(tag, r):
    d = sorted((ORDER[u], ORDER[v]) for u, v in r["directed"])
    od = collections.Counter(u for u, _ in r["directed"])
    ind = collections.Counter(v for _, v in r["directed"])
    sinks = sorted(ORDER[i] for i in range(N) if od[i] == 0)
    srcs = sorted(ORDER[i] for i in range(N) if ind[i] == 0)
    return "%s|%s|%s|%s|%s|%s|%.17g" % (
        tag, d, sinks, srcs, sorted(ORDER[i] for i in r.get("promotions", [])),
        sorted(ORDER[i] for i in r.get("fallbacks", [])), r.get("cost", 0.0))
parts = [rec("PHI_W", drain.run_drain(np.full(N, 1.0 / N) - cvag()))]
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    parts.append(rec(g, drain.run_drain(val[g] / val[g].sum() - n / n.sum())))
print(hashlib.sha256("\n".join(parts).encode()).hexdigest(),
      "PYTHONHASHSEED=" + str(os.environ.get("PYTHONHASHSEED")))
