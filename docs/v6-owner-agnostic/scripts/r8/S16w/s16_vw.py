import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc, solve_phi, orient)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]

def reach_share(directed, s, c):
    adj = collections.defaultdict(list)
    for u,v in directed: adj[u].append(v)
    srcs = [i for i in range(N) if s[i] > 0]
    seen = set(srcs); st = list(srcs)
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    tot = c.sum()
    return (sum(c[i] for i in seen)/tot if tot else 1.0), seen

tot_r = []; wts = []
for gi,g in GL:
    b = S[gi]-C[gi]
    d = []
    for (u,v) in EDGES_UND:
        if b[u] > b[v]: d.append((u,v))
        elif b[v] > b[u]: d.append((v,u))
    r,seen = reach_share(d, S[gi], C[gi]); tot_r.append(r)
    wts.append(PRICES[g]*WORLD[gi])
tot_r = np.array(tot_r); wts = np.array(wts)
unweighted = 1 - tot_r.mean()
vw = 1 - np.average(tot_r, weights=wts)
print("unweighted unreachable: %.4f%%" % (100*unweighted))
print("value-weighted unreachable: %.4f%%" % (100*vw))
print("weights used: PRICES[g]*WORLD[gi] (trade value)")
