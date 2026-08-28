# -*- coding: utf-8 -*-
"""Independent reimplementation of spec 1.1 DRAIN, written from the spec text.
Cross-checked against toys.py on T1/T2/T3 (identical output)."""
import numpy as np, collections, heapq
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

TOL = 1e-11

def drain(names, edges, b, wealth=None, trace=False):
    n = len(names)
    if wealth is None: wealth = [0.0]*n
    und = [[] for _ in range(n)]
    for u, v in edges:
        und[u].append(v); und[v].append(u)
    beta = np.asarray(b, float).copy()
    alive = np.ones(n, bool); deg = np.array([len(und[i]) for i in range(n)])
    Plog = []
    ch = True
    while ch:
        ch = False
        for v in range(n):
            if alive[v] and deg[v] == 1:
                u = next(x for x in und[v] if alive[x])
                Plog.append((v, u, beta[v])); beta[u] += beta[v]
                alive[v] = False; deg[u] -= 1; deg[v] = 0; ch = True
    core = [v for v in range(n) if alive[v]]
    cs = set(core)
    D = [v for v in core if beta[v] < 0]
    S = set()
    if D:
        ds = set(D); comps = []; seen = set()
        for v in D:
            if v in seen: continue
            comp = {v}; st = [v]; seen.add(v)
            while st:
                x = st.pop()
                for y in und[x]:
                    if y in ds and y not in comp: comp.add(y); seen.add(y); st.append(y)
            comps.append(sorted(comp))
        M = [sum(-beta[v] for v in c) for c in comps]
        tot = sum(M); q = [m/tot for m in M]; HHI = sum(x*x for x in q)
        k = int(min(max(round(1.0/HHI), 1), len(comps)))
        for j in sorted(range(len(comps)), key=lambda j: -M[j])[:k]:
            S.add(min(comps[j], key=lambda v: (beta[v], v)))
    ce = [(u, v) for (u, v) in edges if u in cs and v in cs]
    flow_arc = {}; free = []; net = np.zeros(len(ce))
    if ce:
        arcs = []
        for ei, (u, v) in enumerate(ce):
            arcs.append((u, v, ei, +1)); arcs.append((v, u, ei, -1))
        rr, cc, vv = [], [], []
        for ai, (u, v, ei, sg) in enumerate(arcs):
            rr += [v, u]; cc += [ai, ai]; vv += [1.0, -1.0]
        AEQ = csr_matrix((vv, (rr, cc)), shape=(n, len(arcs)))
        rhs = np.zeros(n)
        for v in core: rhs[v] = -beta[v]
        res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")
        if not res.success: return None
        for ai, (u, v, ei, sg) in enumerate(arcs): net[ei] += sg*res.x[ai]
    for ei, (u, v) in enumerate(ce):
        if net[ei] > TOL: flow_arc[ei] = (u, v)
        elif net[ei] < -TOL: flow_arc[ei] = (v, u)
        else: free.append(ei)
    outs = collections.defaultdict(list); ins = collections.defaultdict(list)
    for ei, (u, v) in flow_arc.items(): outs[u].append(v); ins[v].append(u)
    freeadj = collections.defaultdict(list)
    for ei in free:
        u, v = ce[ei]; freeadj[u].append(v); freeadj[v].append(u)
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
    flow_cyclic = (len(topo) != len(core))
    DEF = {}
    for v in reversed(topo): DEF[v] = max(0.0, -beta[v]) + sum(DEF[u] for u in outs[v])
    for v in core: DEF.setdefault(v, max(0.0, -beta[v]))
    key = lambda v: (DEF[v], beta[v], v)
    cnt = {u: len(outs[u]) for u in core}
    marked = set(); order = {}; t = 0
    Sset = set(S); promos = []; fbs = []; stalls = []
    def ready(u):
        return (u not in marked and cnt[u] == 0 and
                ((u in Sset) or (len(outs[u]) > 0) or any(w in marked for w in freeadj[u])))
    heap = []
    for u in core:
        if ready(u): heapq.heappush(heap, (key(u), u))
    guard = 0
    while len(marked) < len(core):
        guard += 1
        if guard > 10*n + 50: return dict(livelock=True)
        found = None
        while heap:
            k_, u = heapq.heappop(heap)
            if ready(u): found = u; break
        if found is None:
            gated = [u for u in core if u not in marked and cnt[u] == 0]
            if not gated: return dict(no_candidate=True, core=core, marked=set(marked))
            term = [u for u in gated if len(outs[u]) == 0 and inflow[u] > TOL]
            stalls.append(dict(gated=list(gated), marked=set(marked), term=list(term)))
            if term:
                s = min(term, key=lambda v: (beta[v], v)); promos.append(s)
            else:
                s = max(gated, key=lambda v: (wealth[v], -v)); fbs.append(s)
            Sset.add(s)
            if ready(s): heapq.heappush(heap, (key(s), s))
            continue
        u = found; marked.add(u); order[u] = t; t += 1
        for x in ins[u]:
            cnt[x] -= 1
            if ready(x): heapq.heappush(heap, (key(x), x))
        for w in freeadj[u]:
            if ready(w): heapq.heappush(heap, (key(w), w))
    directed = list(flow_arc.values())
    for ei in free:
        u, v = ce[ei]
        directed.append((u, v) if order[u] > order[v] else (v, u))
    for (v, u, bv) in reversed(Plog):
        directed.append((v, u) if bv >= 0 else (u, v))
    od = collections.Counter(u for u, _ in directed)
    sinks = set(i for i in range(n) if od[i] == 0)
    ft = set(v for v in core if len(outs[v]) == 0)
    return dict(sinks=sinks, S=set(S), promos=set(promos), fbs=set(fbs), core=core,
                beta=beta, directed=directed, order=order, ft=ft, free=free,
                flow_arc=flow_arc, stalls=stalls, Plog=Plog, ce=ce, net=net,
                flow_cyclic=flow_cyclic, livelock=False, no_candidate=False,
                formula=(set(S) & ft) | set(promos),
                contain=set(S) | set(promos) | set(fbs))
