# -*- coding: utf-8 -*-
"""X151 reconciliation: is EVERY index-dependent orientation sitting on an exact (DEF,b) tie?
Re-runs the exact search3 instance family (seed 11) with the tie test attached."""
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

tot = dep_same = dep_diff = dep_tie = dep_notie = indep_tie = freetie_dep = 0
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
        tot += 1
        base = set(r["directed"]); basesup = set(r["flow_arc"].values())
        DEF = flow_def(r["core"], r["beta"], r["flow_arc"])
        keys = {v: (DEF[v], r["beta"][v]) for v in r["core"]}
        anytie = any(keys[u] == keys[v] for u, v in itertools.combinations(sorted(r["core"]), 2))
        freetie = any(keys[r["ce"][ei][0]] == keys[r["ce"][ei][1]] for ei in r["free"])
        changed = None
        for _t in range(6):
            p = list(range(n)); random.shuffle(p)
            e2, b2, w2 = relabel(n, edges, b, w, p)
            r2 = drain(list(map(str, range(n))), e2, b2, w2)
            if r2 is None or r2.get("livelock") or r2.get("no_candidate"): continue
            inv = {p[i]: i for i in range(n)}
            back = set((inv[u], inv[v]) for u, v in r2["directed"])
            sup2 = set((inv[u], inv[v]) for u, v in r2["flow_arc"].values())
            if back != base:
                changed = "same" if sup2 == basesup else "diff"
                break
        if changed == "same":
            dep_same += 1
            if anytie: dep_tie += 1
            else: dep_notie += 1
            if freetie: freetie_dep += 1
        elif changed == "diff": dep_diff += 1
        elif anytie: indep_tie += 1
print("instances:", tot)
print("index-dependent, SAME LP support :", dep_same)
print("   with an exact (DEF,b) tie in the core :", dep_tie)
print("   with NO exact tie anywhere            :", dep_notie, "   <-- must be 0")
print("   tie sits on an actual FREE edge       :", freetie_dep)
print("index-dependent, DIFFERENT LP support (LP degeneracy, not the sweep):", dep_diff)
print("index-INdependent though a tie exists:", indep_tie)
