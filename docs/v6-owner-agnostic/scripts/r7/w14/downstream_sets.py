import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
print("live goods at gulf_of_siam check:", len(GL))

gos = NIDX["gulf_of_siam"]
sets = {}
for gi, g in GL:
    r = run_drain(S[gi] - C[gi])
    adj = collections.defaultdict(list)
    for u, v in r["directed"]:
        adj[u].append(v)
    # downstream = reachable set from gos following directed edges
    seen = set(); stack=[gos]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v); stack.append(v)
    sets[g] = frozenset(ORDER[i] for i in seen)

distinct = collections.Counter(sets.values())
print("distinct downstream sets:", len(distinct))
for s, cnt in sorted(distinct.items(), key=lambda kv: -kv[1]):
    goods_with = [g for g in sets if sets[g]==s]
    print(" count=%d goods=%s set=%s" % (cnt, goods_with, sorted(s) if len(s)<15 else (sorted(s)[:8]+['...'])))
