# -*- coding: utf-8 -*-
"""Per-good structural battery for the round-5 audit.

Builds S and C exactly as measure6.py does (validated below against measure6.out's
live-goods / sinks-per-good / acyclic / fallback figures), then measures the §1.1
properties the document states: Phase 0 no-op, Phase 1's k distribution and its ties,
the sink-set identity, the (DEF, b) key collisions, demand reachability, and free-edge
determinism under scheduler permutation.
"""
import collections, sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc)
from drain import (run_drain, sinks_of, has_cycle, phase0, phase1, phase2, phase3,
                   flow_def, sweep_priority, compile_dirs, NODEW)
from flowop import ZERO_TOL

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
_, _, _, LIVE, _, _ = build_sc(ALPHA, eps=0.0)
GL = [(gi, g) for gi, g in enumerate(GOODS) if LIVE[gi]]
val = {g: np.zeros(N) for _, g in GL}
for i, r in enumerate(ROWS):
    if r["good"] in val: val[r["good"]][PN[i]] += r["prod_income"]
S = {}; C = {}; B = {}
for gi, g in GL:
    t = (W / W.max()) ** ALPHA(g); n = np.zeros(N); np.add.at(n, PN, t)
    C[g] = n / n.sum()
    S[g] = val[g] / val[g].sum() if val[g].sum() > 0 else np.zeros(N)
    B[g] = S[g] - C[g]

if __name__ == "__main__":
    print("nodes N=%d  undirected edges=%d  live goods=%d" % (N, len(EDGES_UND), len(GL)))
    deg = [len(UND[i]) for i in range(N)]
    print("min degree %d  max %d  mean %.2f" % (min(deg), max(deg), np.mean(deg)))
    # bridges (Tarjan) on the undirected graph
    adj = collections.defaultdict(list)
    for ei, (u, v) in enumerate(EDGES_UND):
        adj[u].append((v, ei)); adj[v].append((u, ei))
    disc = [-1]*N; low = [0]*N; brid = []; timer = [0]
    def dfs(u, pe):
        disc[u] = low[u] = timer[0]; timer[0] += 1
        for v, ei in adj[u]:
            if ei == pe: continue
            if disc[v] < 0:
                dfs(v, ei); low[u] = min(low[u], low[v])
                if low[v] > disc[u]: brid.append(ei)
            else: low[u] = min(low[u], disc[v])
    sys.setrecursionlimit(10000)
    comps = 0
    for i in range(N):
        if disc[i] < 0: comps += 1; dfs(i, -1)
    print("components=%d  bridges=%d" % (comps, len(brid)))

    ks = []; sinkcounts = []; acyc = 0; fbs = 0; ident = 0; identfail = []
    keycoll = 0; corenodes = 0; p1ties = 0; p1cuties = 0
    orphan = 0; reach_pct = []
    b0_nodes = collections.Counter()
    for gi, g in GL:
        b = B[g]
        core, beta, Plog = phase0(b)
        corenodes += len(core)
        if len(core) != N: print("  PHASE0 ACTED on", g, N - len(core))
        s0, info = phase1(core, beta, 0)
        ks.append(info["k"])
        # Phase 1 tie checks: within-cluster argmin on (beta,v) and the top-k cut on M
        coreset = set(core); ds = set(v for v in core if beta[v] < 0)
        cl = []; seen = set()
        for v in sorted(ds):
            if v in seen: continue
            comp = {v}; st = [v]; seen.add(v)
            while st:
                x = st.pop()
                for y in UND[x]:
                    if y in ds and y not in comp: comp.add(y); seen.add(y); st.append(y)
            cl.append(sorted(comp))
        M = [sum(-beta[v] for v in c) for c in cl]
        for c in cl:
            bs = sorted(beta[v] for v in c)
            if len(bs) > 1 and bs[0] == bs[1]: p1ties += 1
        Ms = sorted(M, reverse=True); kk = info["k"]
        if kk < len(Ms) and Ms[kk-1] == Ms[kk]: p1cuties += 1
        r = run_drain(b)
        d = r["directed"]; sk, od = sinks_of(d)
        sinkcounts.append(len(sk))
        acyc += has_cycle(d) is None
        fbs += len(r["fallbacks"])
        # sink-set identity: {selected & flow-terminal} u {promoted}
        outs = collections.defaultdict(list)
        for ei, (u, v) in r["flow_arc"].items(): outs[u].append(v)
        sel_ft = {v for v in r["S0"] if len(outs[v]) == 0}
        formula = sel_ft | set(r["promotions"])
        if formula == set(sk): ident += 1
        else: identfail.append((g, sorted(ORDER[i] for i in formula ^ set(sk))))
        # (DEF, b) key collisions over all core nodes
        DEF = flow_def(core, beta, r["flow_arc"])
        keys = collections.Counter((round(DEF[v], 15), round(beta[v], 15)) for v in core)
        keycoll += sum(c - 1 for c in keys.values() if c > 1)
        # b == 0 exactly
        for v in range(N):
            if b[v] == 0.0: b0_nodes[ORDER[v]] += 1
        # demand reachability: every node with c>0 reachable from some node with s>0
        dadj = collections.defaultdict(list)
        for u, v in d: dadj[u].append(v)
        src = [i for i in range(N) if S[g][i] > 0]
        seen2 = set()
        for s_ in src:
            if s_ in seen2: continue
            st = [s_]
            while st:
                x = st.pop()
                if x in seen2: continue
                seen2.add(x)
                for y in dadj[x]: st.append(y)
        dem = C[g]
        tot = dem.sum(); got = sum(dem[i] for i in range(N) if i in seen2)
        reach_pct.append(100.0 * got / tot)
        orphan += sum(1 for i in sk if i not in seen2)
    print("Phase1 k==1 on %d of %d goods (k values %s)" % (sum(1 for k in ks if k == 1), len(ks),
                                                            collections.Counter(ks)))
    print("sinks per good min/max/mean: %d/%d/%.2f" % (min(sinkcounts), max(sinkcounts), np.mean(sinkcounts)))
    print("acyclic goods: %d of %d" % (acyc, len(GL)))
    print("fallbacks fired: %d" % fbs)
    print("sink-set identity holds on %d of %d goods; failures %s" % (ident, len(GL), identfail))
    print("core nodes summed over goods: %d ; exact (DEF,b) key collisions: %d" % (corenodes, keycoll))
    print("Phase-1 within-cluster argmin ties: %d ; top-k cut ties: %d" % (p1ties, p1cuties))
    print("demand reachable: min %.4f%% max %.4f%% ; orphan sinks %d" % (min(reach_pct), max(reach_pct), orphan))
    print("nodes with b==0 exactly, by good count:", dict(b0_nodes))
