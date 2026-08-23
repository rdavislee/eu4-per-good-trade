# -*- coding: utf-8 -*-
"""General-input counterexamples for the v2 derivation claims.

A faithful generic DRAIN implementation (same logic as drain.py, parameterized graph):
peel -> HHI cluster select -> min-cost b-flow (scipy HiGHS) -> deterministic
gated drainage sweep, key (DEF asc, b asc, index) -> un-peel.

T1  V029/V126: pendant net-importer leaf  -> sink outside the formula set AND a
    selected flow-terminal demander stripped of sinkhood by the pendant edge.
T2  V029 core-only: two selected flow-terminal demanders; the heavy one (popped
    late under DEF-ascending) gains an out-arc over a free edge to an
    earlier-marked conduit -> not a sink, though in the formula set.
T3  V151: two equal-cost corridors; an infinitesimal demand perturbation swaps
    the LP support -> a link alternating support membership carries the FULL flow.
T4  V031 premise: disconnected graph with per-component imbalance -> LP infeasible.
"""
import numpy as np, collections, heapq
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def drain_generic(names, edges, b, verbose=False):
    N = len(names); E = len(edges)
    UND = [[] for _ in range(N)]
    for u, v in edges:
        UND[u].append(v); UND[v].append(u)
    # phase 0
    beta = np.asarray(b, float).copy()
    alive = np.ones(N, bool); deg = np.array([len(UND[i]) for i in range(N)])
    Plog = []
    changed = True
    while changed:
        changed = False
        for v in range(N):
            if alive[v] and deg[v] == 1:
                u = next(x for x in UND[v] if alive[x])
                Plog.append((v, u, beta[v])); beta[u] += beta[v]
                alive[v] = False; deg[u] -= 1; deg[v] = 0; changed = True
    core = [v for v in range(N) if alive[v]]
    coreset = set(core)
    # phase 1
    Dset = [v for v in core if beta[v] < 0]
    S = set()
    if Dset:
        ds = set(Dset); comps = []; seen = set()
        for v in Dset:
            if v in seen: continue
            comp = {v}; st=[v]; seen.add(v)
            while st:
                x = st.pop()
                for y in UND[x]:
                    if y in ds and y not in comp: comp.add(y); seen.add(y); st.append(y)
            comps.append(sorted(comp))
        M = [sum(-beta[v] for v in c) for c in comps]
        D = sum(M); q = [m/D for m in M]; HHI = sum(x*x for x in q)
        k = int(min(max(round(1.0/HHI), 1), len(comps)))
        for j in sorted(range(len(comps)), key=lambda j: -M[j])[:k]:
            S.add(min(comps[j], key=lambda v: (beta[v], v)))
    # phase 2 (core only)
    cedges = [(u, v) for (u, v) in edges if u in coreset and v in coreset]
    arcs = []
    for ei, (u, v) in enumerate(cedges):
        arcs.append((u, v, ei, +1)); arcs.append((v, u, ei, -1))
    A = len(arcs)
    rows, cols, vals = [], [], []
    for ai, (u, v, ei, sg) in enumerate(arcs):
        rows += [v, u]; cols += [ai, ai]; vals += [1.0, -1.0]
    AEQ = csr_matrix((vals, (rows, cols)), shape=(N, A))
    rhs = np.zeros(N)
    for v in core: rhs[v] = -beta[v]     # inflow - outflow = c - s = -b
    res = linprog(c=np.ones(A), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")
    assert res.success, res.message
    net = np.zeros(len(cedges))
    for ai, (u, v, ei, sg) in enumerate(arcs): net[ei] += sg * res.x[ai]
    TOL = 1e-11
    flow_arc = {}; free = []
    for ei, (u, v) in enumerate(cedges):
        if net[ei] > TOL: flow_arc[ei] = (u, v)
        elif net[ei] < -TOL: flow_arc[ei] = (v, u)
        else: free.append(ei)
    # phase 3: deterministic sweep, key (DEF asc, beta asc, index)
    outs = collections.defaultdict(list); ins = collections.defaultdict(list)
    for ei, (u, v) in flow_arc.items(): outs[u].append(v); ins[v].append(u)
    freeadj = collections.defaultdict(list)
    for ei in free:
        u, v = cedges[ei]; freeadj[u].append(v); freeadj[v].append(u)
    inflow = collections.defaultdict(float)
    for ei, (u, v) in flow_arc.items(): inflow[v] += abs(net[ei])
    indeg = collections.Counter()
    for ei, (u, v) in flow_arc.items(): indeg[v] += 1
    ind = dict(indeg); topo = []
    q = collections.deque([v for v in core if ind.get(v, 0) == 0])
    while q:
        x = q.popleft(); topo.append(x)
        for y in outs[x]:
            ind[y] -= 1
            if ind[y] == 0: q.append(y)
    DEF = {}
    for v in reversed(topo): DEF[v] = max(0.0, -beta[v]) + sum(DEF[u] for u in outs[v])
    for v in core: DEF.setdefault(v, max(0.0, -beta[v]))
    keyfn = lambda v: (DEF[v], beta[v], v)
    cnt = {u: len(outs[u]) for u in core}
    marked = set(); order = {}; t = 0
    Sset = set(S); promotions = []; fallbacks = []
    def ready(u):
        return (u not in marked and cnt[u] == 0 and
                ((u in Sset) or (len(outs[u]) > 0) or any(w in marked for w in freeadj[u])))
    heap = []
    for u in core:
        if ready(u): heapq.heappush(heap, (keyfn(u), u))
    while len(marked) < len(core):
        found = None
        while heap:
            k, u = heapq.heappop(heap)
            if ready(u): found = u; break
        if found is None:
            gated = [u for u in core if u not in marked and cnt[u] == 0]
            term = [u for u in gated if len(outs[u]) == 0 and inflow[u] > TOL]
            s_star = min(term or gated, key=lambda v: (beta[v], v))
            (promotions if term else fallbacks).append(s_star)
            Sset.add(s_star)
            if ready(s_star): heapq.heappush(heap, (keyfn(s_star), s_star))
            continue
        u = found; marked.add(u); order[u] = t; t += 1
        for x in ins[u]:
            cnt[x] -= 1
            if ready(x): heapq.heappush(heap, (keyfn(x), x))
        for w in freeadj[u]:
            if ready(w): heapq.heappush(heap, (keyfn(w), w))
    directed = list(flow_arc.values())
    for ei in free:
        u, v = cedges[ei]
        directed.append((u, v) if order[u] > order[v] else (v, u))
    for (v, u, bv) in reversed(Plog):
        directed.append((v, u) if bv >= 0 else (u, v))
    od = collections.Counter(u for u, _ in directed)
    sinks = [i for i in range(N) if od[i] == 0]
    ft = set(v for v in core if len(outs[v]) == 0)
    claimed = (S & ft) | set(promotions)
    if verbose:
        nm = lambda xs: sorted(names[i] for i in xs)
        print("  S0(selected)=%s  flow-terminal=%s  promoted=%s" % (nm(S), nm(ft), nm(promotions)))
        print("  directed: %s" % sorted((names[u], names[v]) for u, v in directed))
        print("  actual sinks = %s | formula set {S0 cap ft} U promoted = %s | EQUAL: %s"
              % (nm(sinks), nm(claimed), set(sinks) == claimed))
    return set(sinks), claimed, directed, order

print("="*90)
print("T1  V029/V126 - pendant net-importer (Phase 0 active)")
print("="*90)
# triangle A,B,D + leaf C hanging off B.  A supplies 5; B demands 3; C demands 2; D conduit.
names = ["A", "B", "D", "C"]
edges = [(0,1), (1,2), (2,0), (1,3)]
b = [5.0, -3.0, 0.0, -2.0]
sk, cl, d, o = drain_generic(names, edges, b, verbose=True)

print()
print("="*90)
print("T2  V029 core-only - selected flow-terminal demander loses sinkhood on a free edge")
print("="*90)
# 5-cycle S1-u1-w-u2-S2-S1 plus chord w-S1. Balanced. Two demand clusters {u1},{u2}.
names = ["S1", "u1", "w", "u2", "S2"]
edges = [(0,1), (1,2), (2,3), (3,4), (4,0), (2,0)]
b = [3.0, -3.0, 0.0, -2.0, 2.0]
sk, cl, d, o = drain_generic(names, edges, b, verbose=True)

print()
print("="*90)
print("T3  V151 - equal-cost corridors: support membership alternates, flow is NOT small")
print("="*90)
# square: A(+1) - B(0) - C(-1) - D(0) - A. Two 2-hop routes A->B->C and A->D->C.
# month 1: tiny extra demand at B (balanced by A); month 2: tiny extra demand at D.
def solve_square(eps_at):
    nm = ["A", "B", "C", "D"]
    edges = [(0,1), (1,2), (2,3), (3,0)]
    b = np.array([1.0, 0.0, -1.0, 0.0])
    b[eps_at] -= 1e-9; b[0] += 1e-9
    arcs = []
    for ei, (u, v) in enumerate(edges):
        arcs.append((u, v, ei, +1)); arcs.append((v, u, ei, -1))
    rows, cols, vals = [], [], []
    for ai, (u, v, ei, sg) in enumerate(arcs):
        rows += [v, u]; cols += [ai, ai]; vals += [1.0, -1.0]
    AEQ = csr_matrix((vals, (rows, cols)), shape=(4, len(arcs)))
    res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=-b, bounds=(0, None), method="highs")
    net = np.zeros(4)
    for ai, (u, v, ei, sg) in enumerate(arcs): net[ei] += sg * res.x[ai]
    return {("ABCD"[u] + "-" + "ABCD"[v]): round(net[ei], 6) for ei, (u, v) in enumerate(edges)}

m1 = solve_square(1)   # tiny demand at B
m2 = solve_square(3)   # tiny demand at D
print("  month 1 (eps demand at B): net per edge:", m1)
print("  month 2 (eps demand at D): net per edge:", m2)
for e in m1:
    in1, in2 = abs(m1[e]) > 1e-11, abs(m2[e]) > 1e-11
    if in1 != in2:
        print("  -> edge %s alternates support membership carrying %.6f vs %.6f  (NOT near-zero)"
              % (e, m1[e], m2[e]))

print()
print("="*90)
print("T4  V031 premise - disconnected graph, per-component imbalance -> LP infeasible")
print("="*90)
# component 1: A(+0.6) - B(-0.4); component 2: C(+0.4) - D(-0.6). Shares balance globally.
nm = ["A", "B", "C", "D"]
edges = [(0,1), (2,3)]
b = np.array([0.6, -0.4, 0.4, -0.6])
arcs = []
for ei, (u, v) in enumerate(edges):
    arcs.append((u, v, ei, +1)); arcs.append((v, u, ei, -1))
rows, cols, vals = [], [], []
for ai, (u, v, ei, sg) in enumerate(arcs):
    rows += [v, u]; cols += [ai, ai]; vals += [1.0, -1.0]
AEQ = csr_matrix((vals, (rows, cols)), shape=(4, len(arcs)))
res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=-b, bounds=(0, None), method="highs")
print("  LP success:", res.success, "|", res.message.strip()[:80])
