# -*- coding: utf-8 -*-
"""Isolate index-dependent instances that have NO exact (DEF,b) tie, and find which
tiebreak is responsible."""
import sys, itertools, random, collections
sys.path.insert(0, "C:/Users/rdavi/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/mod/per-good-trade/v5-owner-agnostic/scripts")
from _audit_b_drain import drain
from drain import flow_def
random.seed(11)

def connected(n, edges):
    adj = collections.defaultdict(set)
    for u, v in edges: adj[u].add(v); adj[v].add(u)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == n

def relabel(n, edges, b, w, p):
    e2 = sorted(tuple(sorted((p[u], p[v]))) for u, v in edges)
    b2 = [0.]*n; w2 = [0.]*n
    for i in range(n): b2[p[i]] = b[i]; w2[p[i]] = w[i]
    return e2, b2, w2

found = []
BV = [-2., -1., 0., 1., 2.]
for n in (4, 5, 6):
    pairs = list(itertools.combinations(range(n), 2))
    for _ in range(2500):
        m = random.randint(n, min(len(pairs), n+3))
        edges = sorted(random.sample(pairs, m))
        if not connected(n, edges): continue
        b = [random.choice(BV) for _ in range(n)]
        b[random.randrange(n)] -= sum(b)
        w = [random.choice([0., 1., 2., 3.]) for _ in range(n)]
        r = drain(list(map(str, range(n))), edges, b, wealth=w)
        if r is None or r.get("livelock") or r.get("no_candidate"): continue
        base = set(r["directed"]); basesup = set(r["flow_arc"].values())
        DEF = flow_def(r["core"], r["beta"], r["flow_arc"])
        keys = {v: (DEF[v], r["beta"][v]) for v in r["core"]}
        if any(keys[u] == keys[v] for u, v in itertools.combinations(sorted(r["core"]), 2)):
            continue                      # only want NO-tie instances
        for _t in range(6):
            p = list(range(n)); random.shuffle(p)
            e2, b2, w2 = relabel(n, edges, b, w, p)
            r2 = drain(list(map(str, range(n))), e2, b2, w2)
            if r2 is None or r2.get("livelock") or r2.get("no_candidate"): continue
            inv = {p[i]: i for i in range(n)}
            back = set((inv[u], inv[v]) for u, v in r2["directed"])
            sup2 = set((inv[u], inv[v]) for u, v in r2["flow_arc"].values())
            if back != base and sup2 == basesup:
                found.append((n, edges, b, w, p, r, r2, inv, keys, base, back))
                break
        if found: break
    if found: break

for (n, edges, b, w, p, r, r2, inv, keys, base, back) in found[:1]:
    print("n=%d edges=%s\n b=%s\n wealth=%s\n perm(old->new)=%s" % (n, edges, b, w, p))
    print(" keys (DEF,beta):", {k: (round(float(a), 6), round(float(c), 6)) for k, (a, c) in keys.items()})
    print(" BASE  selected=%s promos=%s fbs=%s" % (sorted(r["S"]), sorted(r["promos"]), sorted(r["fbs"])))
    print(" RELAB selected=%s promos=%s fbs=%s (mapped back)" % (
        sorted(inv[x] for x in r2["S"]), sorted(inv[x] for x in r2["promos"]), sorted(inv[x] for x in r2["fbs"])))
    print(" BASE  beta=%s" % {v: float(r["beta"][v]) for v in r["core"]})
    print(" BASE  flow arcs=%s free=%s" % (sorted(r["flow_arc"].values()), [r["ce"][ei] for ei in r["free"]]))
    print(" BASE  order=%s" % r["order"])
    print(" RELAB order (mapped back)=%s" % {inv[k]: v for k, v in r2["order"].items()})
    print(" BASE  directed=%s" % sorted(base))
    print(" RELAB directed=%s" % sorted(back))
    print(" diff:", sorted(base - back), "->", sorted(back - base))
