# -*- coding: utf-8 -*-
"""Y547 (luxury vs bulk demand), Y548 (alpha under a price crash), Y560 (demand reachable
from supply), Y575 (sum of in-degrees)."""
import collections, os, sys
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from drain import run_drain, sinks_of
from flowop import EDGES_UND
from solver import N, ORDER, NIDX, ROWS, GOODS, PRICES, build_sc
W = np.array([r["tax"] + r["prod_income"] for r in ROWS]); pn = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][pn[i]] += r["prod_income"]
cnt = np.zeros(N); mx = np.zeros(N)
for i, r in enumerate(ROWS):
    cnt[pn[i]] += 1; mx[pn[i]] = max(mx[pn[i]], W[i])
C = {}; S = {}; R = {}
for g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, pn, t)
    C[g] = n / n.sum(); S[g] = val[g] / val[g].sum(); R[g] = run_drain(S[g] - C[g])
# ---- Y547 -------------------------------------------------------------------
lo = min(GL, key=ALPHA); hi = max(GL, key=ALPHA)
print("alpha range over live goods: %s a=%.2f (price %.1f) .. %s a=%.2f (price %.1f)"
      % (lo, ALPHA(lo), PRICES[lo], hi, ALPHA(hi), PRICES[hi]))
def sp(a, b):
    ra = np.argsort(np.argsort(a)); rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])
print("  spearman(c, richest-province-in-node) : luxury %s %+.3f | bulk %s %+.3f"
      % (hi, sp(C[hi], mx), lo, sp(C[lo], mx)))
print("  spearman(c, province-count-in-node)   : luxury %s %+.3f | bulk %s %+.3f"
      % (hi, sp(C[hi], cnt), lo, sp(C[lo], cnt)))
# a node that is 'few rich' vs 'many poor'
score = mx / np.maximum(cnt, 1)
few_rich = ORDER[int(np.argmax(np.where(cnt > 0, score, -1)))]
many_poor = ORDER[int(np.argmax(np.where(mx > 0, cnt / np.maximum(mx, 1e-9), -1)))]
for nm in (few_rich, many_poor):
    i = NIDX[nm]
    rl = 1 + int(np.sum(C[hi] > C[hi][i])); rb = 1 + int(np.sum(C[lo] > C[lo][i]))
    print("  %-16s provinces %3d richest %.2f | luxury rank %2d, bulk rank %2d"
          % (nm, int(cnt[i]), mx[i], rl, rb))
# ---- Y548 -------------------------------------------------------------------
print()
print("Y548: alpha = clamp(price/2, 0.2, 3) so alpha < 1 iff price < 2")
below = [g for g in GL if ALPHA(g) < 1.0]
print("  live goods with alpha < 1 : %d %s" % (len(below), below))
ns = {g: len(sinks_of(R[g]["directed"])[0]) for g in GL}
a = np.array([ALPHA(g) for g in GL]); s = np.array([ns[g] for g in GL], dtype=float)
print("  spearman(alpha, sink count) = %+.3f" % sp(a, s))
print("  mean sinks, alpha<1 : %.2f (n=%d) | alpha>=1 : %.2f (n=%d)"
      % (np.mean([ns[g] for g in GL if ALPHA(g) < 1]), sum(1 for g in GL if ALPHA(g) < 1),
         np.mean([ns[g] for g in GL if ALPHA(g) >= 1]), sum(1 for g in GL if ALPHA(g) >= 1)))
# ---- Y560 -------------------------------------------------------------------
print()
bad = 0; orphan = 0
for g in GL:
    adj = collections.defaultdict(list)
    for u, v in R[g]["directed"]: adj[u].append(v)
    src = [i for i in range(N) if S[g][i] > 0]
    seen = set(src); q = collections.deque(src)
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in seen: seen.add(y); q.append(y)
    dem = [i for i in range(N) if C[g][i] > 0]
    miss = [i for i in dem if i not in seen]
    bad += len(miss)
    sk = set(sinks_of(R[g]["directed"])[0])
    orphan += sum(1 for i in sk if i not in seen)
print("Y560: demanding nodes NOT reachable from any producer, summed over 29 goods : %d" % bad)
print("      sinks not reachable from any producer (orphan sinks)                  : %d" % orphan)
# ---- Y575 -------------------------------------------------------------------
print()
tot = set()
for g in GL:
    ind = collections.Counter(v for _, v in R[g]["directed"])
    tot.add(sum(ind.values()))
print("Y575: sum of in-degrees over each of the 29 per-good graphs : %s (|E| = %d)"
      % (sorted(tot), len(EDGES_UND)))
