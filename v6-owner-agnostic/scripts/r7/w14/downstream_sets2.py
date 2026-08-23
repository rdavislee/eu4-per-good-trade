import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, GOODS, PRICES, build_sc
from drain import run_drain

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]

gos = NIDX["gulf_of_siam"]
sets = {}
for gi, g in GL:
    r = run_drain(S[gi] - C[gi])
    direct = frozenset(ORDER[v] for u, v in r["directed"] if u == gos)
    sets[g] = direct

distinct = collections.Counter(sets.values())
print("distinct ONE-HOP downstream-neighbour sets:", len(distinct))
for s, cnt in sorted(distinct.items(), key=lambda kv: -kv[1]):
    goods_with = [g for g in sets if sets[g]==s]
    print(" count=%d set=%s goods=%s" % (cnt, sorted(s), goods_with))
