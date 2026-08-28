# -*- coding: utf-8 -*-
"""Part-5 validator throwaway: figures for 2.8 / 3.2 claims not covered by shipped instruments."""
import collections, sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import drain, flowop
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from drain import run_drain, sinks_of
from flowop import mincost_flow, ARCS, TIE_COST
from scipy.optimize import linprog

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
GL = [(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]
W = np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, PN, W)

print("== supply sources ==")
for g in ("spices","cloves"):
    gi = GOODS.index(g)
    src = [ORDER[i] for i in range(N) if S[gi][i] > 0]
    print(g, "produced in", len(src), "nodes:", src)

print("\n== baseline sinks + demand ranks ==")
for g in ("spices","cloves"):
    gi = GOODS.index(g)
    r = run_drain(S[gi]-C[gi]); sk,_ = sinks_of(r["directed"])
    order_ = sorted(range(N), key=lambda i:-C[gi][i])
    rank = {n:i+1 for i,n in enumerate(order_)}
    print(g, "sinks:", sorted((ORDER[i], rank[i]) for i in sk))
    for bad in ("australia","venice","deccan"):
        if bad in NIDX: print("   ", bad, "is sink:", NIDX[bad] in sk)

print("\n== node wealth poles (Y155) ==")
holding = [i for i in range(N) if NODEW[i] > 0]
rank = {n:r for r,n in enumerate(sorted(holding, key=lambda i:-NODEW[i]),1)}
for n in ("hangzhou","beijing"):
    i = NIDX[n]; print(n, "wealth %.1f rank %d of %d" % (NODEW[i], rank[i], len(holding)))
print("beijing share of world wealth: %.2f%%" % (100*NODEW[NIDX["beijing"]]/NODEW.sum()))

print("\n== every node with an owned province carries demand (Y594) ==")
gi = GOODS.index("spices")
own = set(PN.tolist())
print("nodes with owned provinces:", len(own), "| of them with c>0 for spices:",
      sum(1 for i in own if C[gi][i] > 0), "| nodes with c==0 overall:",
      [ORDER[i] for i in range(N) if C[gi][i] == 0])

print("\n== Malacca hops (Y615) ==")
def bfs_exclude(src, dst, excl=()):
    from collections import deque
    seen={src:0}; q=deque([src])
    while q:
        x=q.popleft()
        if x==dst: return seen[x]
        for y in UND[x]:
            if y not in seen and ORDER[y] not in excl:
                seen[y]=seen[x]+1; q.append(y)
    return seen.get(dst)
m, ec = NIDX["malacca"], NIDX["english_channel"]
print("undirected shortest malacca->english_channel:", bfs_exclude(m,ec))
print("  avoiding cape:", bfs_exclude(m,ec,("cape_of_good_hope",)))
# path through cape: dist(m,cape)+dist(cape,ec)
cp = NIDX["cape_of_good_hope"]; al = NIDX["alexandria"] if "alexandria" in NIDX else None
print("  via cape: ", bfs_exclude(m,cp), "+", bfs_exclude(cp,ec))
if al is not None: print("  via alexandria:", bfs_exclude(m,al), "+", bfs_exclude(al,ec))
# spice flow through the cape as share of world supply
r = run_drain(S[gi]-C[gi])
fa = r["flow_arc"]; net = r["net"]
inflow = sum(abs(net[ei]) for ei,(u,v) in fa.items() if v==cp)
print("spice flow INTO cape: %.4f of world supply (sum s = %.4f)" % (inflow, S[gi].sum()))

print("\n== marking order reproduces DAG (Y612/Y613) ==")
B = np.full(N,1.0/N) - (lambda t: (lambda n: n/n.sum())((lambda z: z)(np.zeros(N))+np.bincount(PN, weights=t, minlength=N)))((W/W.max())**2.0)
rw = run_drain(B)
o = rw["order"]; ok = all(o[u] > o[v] for u,v in rw["directed"]) if len(rw["core"])==N else "core<N"
print("phi_w: core", len(rw["core"]), "of", N, "| every arc later->earlier marked:", ok,
      "| acyclic:", drain.has_cycle(rw["directed"]) is None)
pg_ok = 0
for gi2, g in GL:
    r2 = run_drain(S[gi2]-C[gi2])
    if len(r2["core"])==N and all(r2["order"][u] > r2["order"][v] for u,v in r2["directed"]): pg_ok += 1
print("per-good: marking order reproduces DAG on %d of %d" % (pg_ok, len(GL)))

print("\n== paper genuine tie (Y1120) ==")
gi = GOODS.index("paper")
b = S[gi]-C[gi]
f, du, res = mincost_flow(b+0, np.zeros(N), cost=TIE_COST)
rc = np.array([TIE_COST[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(len(ARCS))])
opt = res.fun
zero_off = [ai for ai in range(len(ARCS)) if f[ai] <= 1e-12 and abs(rc[ai]) <= 1e-14]
print("off-support arcs with zero reduced cost:", len(zero_off))
for ai in zero_off:
    u,v,ei,sg = ARCS[ai]
    # maximize f[ai] subject to same constraints and cost == opt
    A_eq2 = flowop.AEQ
    from scipy.sparse import vstack, csr_matrix
    row = csr_matrix(TIE_COST.reshape(1,-1))
    Afull = vstack([A_eq2, row])
    bfull = np.concatenate([np.zeros(N)-b, [opt]])
    cobj = np.zeros(len(ARCS)); cobj[ai] = -1.0
    r3 = linprog(c=cobj, A_eq=Afull, b_eq=bfull, bounds=(0,None), method="highs",
                 options={"dual_feasibility_tolerance":1e-10,"primal_feasibility_tolerance":1e-10})
    print("  arc %s->%s: max flow at optimality = %.3g (success=%s)" % (ORDER[u],ORDER[v], -r3.fun if r3.success else float('nan'), r3.success))
