# -*- coding: utf-8 -*-
# Audit harness: v4.0-faithful generic DRAIN.  Identical to toys.drain_generic EXCEPT the
# Phase-3 fallback, which v4.0 §1.1 defines as "promote the highest-wealth candidate, ties by
# index".  toys.py still ships the v3.0 rule (most-negative-beta) in both branches.
import numpy as np, collections, heapq, random
from scipy.optimize import linprog
from scipy.sparse import csr_matrix


def drain_v4(names, edges, b, wealth):
    N = len(names)
    UND = [[] for _ in range(N)]
    for u, v in edges:
        UND[u].append(v); UND[v].append(u)
    beta = np.asarray(b, float).copy()
    alive = np.ones(N, bool)
    deg = np.array([len(UND[i]) for i in range(N)])
    Plog = []
    ch = True
    while ch:
        ch = False
        for v in range(N):
            if alive[v] and deg[v] == 1:
                u = next(x for x in UND[v] if alive[x])
                Plog.append((v, u, beta[v]))
                beta[u] += beta[v]; alive[v] = False; deg[u] -= 1; deg[v] = 0; ch = True
    core = [v for v in range(N) if alive[v]]
    coreset = set(core)
    Dset = [v for v in core if beta[v] < 0]
    S = set()
    if Dset:
        ds = set(Dset); comps = []; seen = set()
        for v in Dset:
            if v in seen:
                continue
            comp = {v}; st = [v]; seen.add(v)
            while st:
                x = st.pop()
                for y in UND[x]:
                    if y in ds and y not in comp:
                        comp.add(y); seen.add(y); st.append(y)
            comps.append(sorted(comp))
        M = [sum(-beta[v] for v in c) for c in comps]
        D = sum(M); qq = [m / D for m in M]
        HHI = sum(x * x for x in qq)
        k = int(min(max(round(1.0 / HHI), 1), len(comps)))
        for j in sorted(range(len(comps)), key=lambda j: -M[j])[:k]:
            S.add(min(comps[j], key=lambda v: (beta[v], v)))
    cedges = [(u, v) for (u, v) in edges if u in coreset and v in coreset]
    arcs = []
    for ei, (u, v) in enumerate(cedges):
        arcs.append((u, v, ei, 1)); arcs.append((v, u, ei, -1))
    rows, cols, vals = [], [], []
    for ai, (u, v, ei, sg) in enumerate(arcs):
        rows += [v, u]; cols += [ai, ai]; vals += [1.0, -1.0]
    AEQ = csr_matrix((vals, (rows, cols)), shape=(N, len(arcs)))
    rhs = np.zeros(N)
    for v in core:
        rhs[v] = -beta[v]
    res = linprog(c=np.ones(len(arcs)), A_eq=AEQ, b_eq=rhs, bounds=(0, None), method="highs")
    if not res.success:
        return None
    net = np.zeros(len(cedges))
    for ai, (u, v, ei, sg) in enumerate(arcs):
        net[ei] += sg * res.x[ai]
    TOL = 1e-11
    flow_arc = {}; free = []
    for ei, (u, v) in enumerate(cedges):
        if net[ei] > TOL:
            flow_arc[ei] = (u, v)
        elif net[ei] < -TOL:
            flow_arc[ei] = (v, u)
        else:
            free.append(ei)
    outs = collections.defaultdict(list); ins = collections.defaultdict(list)
    for ei, (u, v) in flow_arc.items():
        outs[u].append(v); ins[v].append(u)
    freeadj = collections.defaultdict(list)
    for ei in free:
        u, v = cedges[ei]
        freeadj[u].append(v); freeadj[v].append(u)
    inflow = collections.defaultdict(float)
    for ei, (u, v) in flow_arc.items():
        inflow[v] += abs(net[ei])
    indeg = collections.Counter()
    for ei, (u, v) in flow_arc.items():
        indeg[v] += 1
    ind = dict(indeg); topo = []
    q = collections.deque([v for v in core if ind.get(v, 0) == 0])
    while q:
        x = q.popleft(); topo.append(x)
        for y in outs[x]:
            ind[y] -= 1
            if ind[y] == 0:
                q.append(y)
    DEF = {}
    for v in reversed(topo):
        DEF[v] = max(0.0, -beta[v]) + sum(DEF[u] for u in outs[v])
    for v in core:
        DEF.setdefault(v, max(0.0, -beta[v]))
    keyfn = lambda v: (DEF[v], beta[v], v)
    cnt = {u: len(outs[u]) for u in core}
    marked = set(); order = {}; t = 0
    Sset = set(S); promotions = []; fallbacks = []; fb_cands = []

    def ready(u):
        return (u not in marked and cnt[u] == 0 and
                ((u in Sset) or (len(outs[u]) > 0) or any(w in marked for w in freeadj[u])))

    heap = []
    for u in core:
        if ready(u):
            heapq.heappush(heap, (keyfn(u), u))
    while len(marked) < len(core):
        found = None
        while heap:
            k, u = heapq.heappop(heap)
            if ready(u):
                found = u; break
        if found is None:
            gated = [u for u in core if u not in marked and cnt[u] == 0]
            term = [u for u in gated if len(outs[u]) == 0 and inflow[u] > TOL]
            if term:
                s = min(term, key=lambda v: (beta[v], v)); promotions.append(s)
            else:
                assert gated, "SWEEP CANNOT ADVANCE"
                s = max(gated, key=lambda v: (wealth[v], -v))     # v4.0 fallback
                fallbacks.append(s); fb_cands.append(sorted(gated))
            Sset.add(s)
            if ready(s):
                heapq.heappush(heap, (keyfn(s), s))
            continue
        u = found
        marked.add(u); order[u] = t; t += 1
        for x in ins[u]:
            cnt[x] -= 1
            if ready(x):
                heapq.heappush(heap, (keyfn(x), x))
        for w in freeadj[u]:
            if ready(w):
                heapq.heappush(heap, (keyfn(w), w))
    directed = list(flow_arc.values())
    for ei in free:
        u, v = cedges[ei]
        directed.append((u, v) if order[u] > order[v] else (v, u))
    for (v, u, bv) in reversed(Plog):
        directed.append((v, u) if bv >= 0 else (u, v))
    od = collections.Counter(u for u, _ in directed)
    sinks = [i for i in range(N) if od[i] == 0]
    ft = set(v for v in core if len(outs[v]) == 0)
    return dict(sinks=set(sinks), equality=(S & ft) | set(promotions),
                containment=S | set(promotions) | set(fallbacks), core=core,
                directed=set(directed), S=S, promotions=promotions, fallbacks=fallbacks,
                fb_cands=fb_cands, order=order, free=free, flow=flow_arc)


print("=" * 88)
print("E1  random connected 2-core graphs: can the v4.0 fallback fire when b is not identically 0?")
print("=" * 88)
random.seed(7)
trials = fired = zerob = 0
for _ in range(3000):
    n = random.randint(4, 9)
    es = set()
    perm = list(range(n)); random.shuffle(perm)
    for i in range(n):
        es.add(tuple(sorted((perm[i], perm[(i + 1) % n]))))
    for _ in range(random.randint(0, n)):
        a, c = random.sample(range(n), 2)
        es.add(tuple(sorted((a, c))))
    edges = sorted(es)
    bb = np.array([random.choice([-3, -2, -1, 0, 0, 0, 1, 2, 3]) for _ in range(n)], float)
    bb -= bb.mean()
    w = np.array([random.random() for _ in range(n)])
    r = drain_v4([str(i) for i in range(n)], edges, bb, w)
    if r is None:
        continue
    trials += 1
    if r["fallbacks"]:
        fired += 1
        if np.allclose(bb, 0):
            zerob += 1
        if fired <= 3:
            print("   fired: n=%d  b=%s" % (n, list(bb)))
print("   connected trials %d | fallback fired %d | of those with b==0 everywhere: %d"
      % (trials, fired, zerob))

print()
print("=" * 88)
print("E2  the input the fallback exists for: a component with no owned province (b==0, wealth==0)")
print("=" * 88)
n = 6
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5), (0, 3)]
bb = np.zeros(n)
w = np.zeros(n)
r = drain_v4([chr(65 + i) for i in range(n)], edges, bb, w)
nm = lambda xs: sorted(chr(65 + i) for i in xs)
print("   fallbacks=%s   candidate set at the stall=%s" % (nm(r["fallbacks"]), [nm(c) for c in r["fb_cands"]]))
print("   sinks=%s  equality set=%s  containment set=%s"
      % (nm(r["sinks"]), nm(r["equality"]), nm(r["containment"])))
print("   T3 (a sink outside the equality set)?  %s" % (not r["sinks"] <= r["equality"]))
print("   containment assertion holds?           %s" % (r["sinks"] <= r["containment"]))
print("   orientation: %s" % sorted((chr(65 + u), chr(65 + v)) for u, v in r["directed"]))

print()
print("=" * 88)
print("E3  same graph, same balances, node labels permuted -> is the orientation index-free?")
print("=" * 88)
base = None
for perm in ([0, 1, 2, 3, 4, 5], [5, 4, 3, 2, 1, 0], [2, 0, 4, 1, 5, 3]):
    inv = {perm[i]: i for i in range(n)}
    e2 = sorted(tuple(sorted((perm[u], perm[v]))) for u, v in edges)
    r2 = drain_v4([str(i) for i in range(n)], e2, bb, w)
    D = set((inv[u], inv[v]) for u, v in r2["directed"])
    print("   perm=%-18s sink(s)=%s  fallback picks=%s"
          % (perm, nm(inv[s] for s in r2["sinks"]), nm(inv[x] for x in r2["fallbacks"])))
    if base is None:
        base = D
    else:
        print("        edges pointing the other way vs the identity labelling: %d of %d"
              % (len(base - D), len(D)))

print()
print("=" * 88)
print("E4  the realistic 'pocket': a disconnected map, main component balanced, pocket b==0")
print("=" * 88)
# main component 0..4 (cycle), pocket 5..8 (cycle), no edge between them
edges2 = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4), (5, 6), (6, 7), (7, 8), (5, 8)]
b2 = np.array([3.0, -1.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
w2 = np.array([10.0, 8.0, 6.0, 4.0, 2.0, 0.0, 0.0, 0.0, 0.0])   # pocket: no owned province
r4 = drain_v4([str(i) for i in range(9)], edges2, b2, w2)
print("   fallbacks=%s  candidates at that stall=%s" % (r4["fallbacks"], r4["fb_cands"]))
print("   sinks=%s  equality=%s  containment=%s"
      % (sorted(r4["sinks"]), sorted(r4["equality"]), sorted(r4["containment"])))
print("   T3? %s   containment holds? %s"
      % (not r4["sinks"] <= r4["equality"], r4["sinks"] <= r4["containment"]))
print("   wealth of every fallback candidate: %s  -> all tied, the index decides"
      % [w2[i] for i in (r4["fb_cands"][0] if r4["fb_cands"] else [])])

print()
print("=" * 88)
print("E5  sparse supply (one producer, everyone demands) on connected cores - fallback?")
print("=" * 88)
random.seed(11)
fired5 = 0
for _ in range(1500):
    n = random.randint(5, 12)
    es = set()
    perm = list(range(n)); random.shuffle(perm)
    for i in range(n):
        es.add(tuple(sorted((perm[i], perm[(i + 1) % n]))))
    for _ in range(random.randint(0, n)):
        a, c = random.sample(range(n), 2)
        es.add(tuple(sorted((a, c))))
    bb = np.zeros(n)
    src = random.randrange(n)
    dem = random.sample([i for i in range(n) if i != src], random.randint(1, n - 1))
    for d in dem:
        bb[d] = -1.0
    bb[src] = -bb.sum()
    w = np.array([random.random() for _ in range(n)])
    r = drain_v4([str(i) for i in range(n)], sorted(es), bb, w)
    if r and r["fallbacks"]:
        fired5 += 1
print("   trials 1500 | fallback fired %d" % fired5)
