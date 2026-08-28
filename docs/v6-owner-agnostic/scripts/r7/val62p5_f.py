# -*- coding: utf-8 -*-
"""Part-5: 3.2 monotone-operator claims, 2.8 conservation/latent, contrast metrics."""
import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain, flowop
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc,
                    solve_phi, orient)
from drain import run_drain, sinks_of, phase0, phase1, phase2, sweep_priority, compile_dirs

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]
W = np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN = np.array([NIDX[r["node"]] for r in ROWS])

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

print("== Y591: the monotone s-c operator ==")
tot_r = []; orphans = 0
for gi,g in GL:
    b = S[gi]-C[gi]
    d = []
    for (u,v) in EDGES_UND:
        if b[u] > b[v]: d.append((u,v))
        elif b[v] > b[u]: d.append((v,u))
    r,seen = reach_share(d, S[gi], C[gi]); tot_r.append(r)
    od = collections.Counter(u for u,_ in d)
    orphans += sum(1 for i in range(N) if od[i]==0 and i not in seen)
print("  s-c operator: mean reach %.2f%% -> unreachable %.2f%% ; orphan sinks %d"
      % (100*np.mean(tot_r), 100*(1-np.mean(tot_r)), orphans))
gi = GOODS.index("cloves"); b = S[gi]-C[gi]
d = []
for (u,v) in EDGES_UND:
    if b[u] > b[v]: d.append((u,v))
    elif b[v] > b[u]: d.append((v,u))
od = collections.Counter(u for u,_ in d)
r, seen = reach_share(d, S[gi], C[gi])
gn = NIDX["genua"]
print("  cloves: genua is a sink: %s ; genua reachable from supply: %s"
      % (od[gn]==0, gn in seen))
# rank operator (v1 strawman): orient by node wealth rank
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)
rr = []
for gi,g in GL:
    d = [(u,v) if NODEW[u]<NODEW[v] else (v,u) for (u,v) in EDGES_UND]
    r,_ = reach_share(d, S[gi], C[gi]); rr.append(r)
print("  wealth-rank operator: mean reach %.2f%% -> unreachable %.2f%%" % (100*np.mean(rr), 100*(1-np.mean(rr))))

print("\n== Y561: Phase-4 conservation residual (machine precision?) ==")
worst = 0.0
for gi,g in GL:
    b = S[gi]-C[gi]
    r = run_drain(b)
    d = r["directed"]
    # unserved / stranded on the compiled orientation: net imbalance carried at each node
    adj = collections.defaultdict(list)
    for u,v in d: adj[u].append(v)
    _, seen = reach_share(d, S[gi], C[gi])
    unserved = sum(C[gi][i] for i in range(N) if i not in seen)
    # stranded: supply that cannot reach any demand
    radj = collections.defaultdict(list)
    for u,v in d: radj[v].append(u)
    dem = [i for i in range(N) if C[gi][i] > 0]
    seen2 = set(dem); st = list(dem)
    while st:
        x = st.pop()
        for y in radj[x]:
            if y not in seen2: seen2.add(y); st.append(y)
    stranded = sum(S[gi][i] for i in range(N) if i not in seen2)
    worst = max(worst, abs(unserved - stranded))
print("  max |sum unserved - sum stranded| over 29 goods: %.3g  (eps=%.3g)" % (worst, np.finfo(float).eps))

print("\n== Y596/Y157/Y158: contrast vs sparsity ==")
EPS = 1e-6
S_UNI, C_UNI, _,_,_,_ = build_sc(ALPHA, eps=EPS)
for g in ("spices","cloves"):
    gi = GOODS.index(g)
    su = S_UNI[gi]
    print("  %-7s max(s_uni)/min(s_uni) with eps floor = %.3g" % (g, su.max()/su.min()))
sc = []; dc = []
for gi,g in GL:
    pos = S[gi][S[gi]>0]; sc.append(pos.max()/pos.min())
    posc = C[gi][C[gi]>0]; dc.append(posc.max()/posc.min())
print("  supply contrast over producing nodes: %.0f .. %.0f" % (min(sc), max(sc)))
print("  demand contrast over demanding nodes: %.0f .. %.0f" % (min(dc), max(dc)))
print("  producers per good: min %d max %d ; goods with 1 producer: %s"
      % (min(int((S[gi]>0).sum()) for gi,_ in GL), max(int((S[gi]>0).sum()) for gi,_ in GL),
         [g for gi,g in GL if int((S[gi]>0).sum())==1]))

print("\n== Y595: v1 Laplacian placement diagnostics (current field) ==")
gi = GOODS.index("spices")
phi = solve_phi(S_UNI[gi]-C_UNI[gi]); d = orient(phi)
od = collections.Counter(u for u,_ in d)
sk = [i for i in range(N) if od[i]==0]
top = max(range(N), key=lambda i: C_UNI[gi][i])
print("  v1 spices sinks: %s ; highest-demand node = %s (a sink: %s)"
      % (sorted(ORDER[i] for i in sk), ORDER[top], top in sk))
zero = [i for i in range(N) if C_UNI[gi][i]==0.0]
print("  zero-demand nodes: %s ; phi at them vs genua/beijing: %s"
      % ([ORDER[i] for i in zero],
         [(ORDER[i], round(float(phi[i]),4)) for i in zero]
         + [("genua", round(float(phi[NIDX['genua']]),4)), ("beijing", round(float(phi[NIDX['beijing']]),4))]))
# uniform demand: delete demand variation entirely
cu = np.full(N, 1.0/N)
od2 = collections.Counter(u for u,_ in orient(solve_phi(S_UNI[gi]-cu)))
print("  spices sinks with demand variation deleted (uniform c): %s"
      % sorted(ORDER[i] for i in range(N) if od2[i]==0))

print("\n== Y564/Y605: 2-core containment on 1444, all goods ==")
bad = 0
for gi,g in GL:
    r = run_drain(S[gi]-C[gi])
    core = set(r["core"]); sk,_ = sinks_of(r["directed"])
    allowed = set(r["S"])           # S = selected U promoted U fallbacks after sweep
    for i in sk:
        if i in core and i not in allowed: bad += 1
print("  core sinks outside {selected} U {promoted} U {fallbacks}: %d" % bad)

print("\n== Y572: Phi_w vs per-good sign agreement ==")
Bw = np.full(N,1.0/N)
t = (W/W.max())**2.0; nn = np.zeros(N); np.add.at(nn, PN, t); Bw = Bw - nn/nn.sum()
dw = {tuple(sorted((u,v))): (u,v) for u,v in run_drain(Bw)["directed"]}
agree = tot = 0; wagree = wtot = 0.0
val = {g: np.zeros(N) for _,g in GL}
for i,r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][PN[i]] += r["prod_income"]
for gi,g in GL:
    r = run_drain(S[gi]-C[gi])
    net = r["net"]
    wgt = PRICES[g]*WORLD[gi]
    for (u,v) in r["directed"]:
        k = tuple(sorted((u,v)))
        if k not in dw: continue
        tot += 1; wtot += wgt
        if dw[k] == (u,v): agree += 1; wagree += wgt
print("  edge-good agreement %.1f%% ; value-weighted %.1f%%" % (100*agree/tot, 100*wagree/wtot))
