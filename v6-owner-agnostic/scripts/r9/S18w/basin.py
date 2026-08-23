# -*- coding: utf-8 -*-
"""BASIN: the 6-phase peel / select / grow / orient / evaluate / refine algorithm,
implemented to the given spec with the given default parameters.

Faithfulness notes (all deviations flagged, none are tuning):
  * `scale` in Phase 5 is unspecified; set to total demand sum(max(0,-b)) which is a
    natural positive normaliser and is recomputed per good, never fitted.
  * b(v)==0 is outside the stated input domain. On the 1444 data exactly one node
    (cape_of_good_hope) has b==0. It is kept in the core with btil=0, excluded from
    the Phase-1 demand candidate list (needs btil<0) and eligible for the fallback pool.
"""
import numpy as np, collections, heapq, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, build_sc, solve_phi, orient

# ------------------------------------------------------------ defaults given --
P = dict(lam=0.5, R=2, gamma=0.0, kplus=1.0, kminus=1.0,
         gmin=0.2, gmax=5.0, eta=0.3, K=4)


# ============================================================== PHASE 0 =======
def phase0(b, adj):
    """Peel to the 2-core. Returns (core, btil, pendants, drains, pend_edges)."""
    n = len(b)
    r = b.astype(float).copy()
    deg = np.array([len(adj[i]) for i in range(n)])
    alive = np.ones(n, dtype=bool)
    pendants = collections.defaultdict(list)
    pend_edges = []                                   # (u,v) oriented
    Q = collections.deque([v for v in range(n) if deg[v] <= 1])
    remaining = n
    while Q and remaining > 1:
        v = Q.popleft()
        if not alive[v] or deg[v] != 1:
            continue
        p = next(u for u in adj[v] if alive[u])
        if r[v] > 0:
            pend_edges.append((v, p))
        elif r[v] < 0:
            pend_edges.append((p, v))
        else:
            pend_edges.append((v, p))                 # zero-flow: point coreward
        r[p] += r[v]
        pendants[p].append((v, r[v]))
        alive[v] = False; remaining -= 1
        deg[p] -= 1
        if deg[p] == 1:
            Q.append(p)
    core = [v for v in range(n) if alive[v]]
    btil = {v: r[v] for v in core}
    drains = {w for w in core if any(rho < 0 for _, rho in pendants[w])}
    return core, btil, pendants, drains, pend_edges


# ============================================================== PHASE 1 =======
def phase1(core, btil, adj, S, lam, R):
    coreset = set(core)
    # diffused demand score
    score = {}
    for v in core:
        tot = 0.0
        seen = {v: 0}
        q = collections.deque([(v, 0)])
        while q:
            x, d = q.popleft()
            if btil[x] < 0:
                tot += (-btil[x]) * (lam ** d)
            if d < R:
                for y in adj[x]:
                    if y in coreset and y not in seen:
                        seen[y] = d + 1; q.append((y, d + 1))
        score[v] = tot
    cands = sorted([v for v in core if btil[v] < 0], key=lambda v: -score[v])
    T, blocked = [], set()
    for v in cands:
        if len(T) == S:
            break
        if v not in blocked:
            T.append(v); blocked |= (set(adj[v]) & coreset)
    if len(T) < S:
        for v in sorted([v for v in core if btil[v] >= 0], key=lambda v: -score[v]):
            if len(T) == S:
                break
            if v not in blocked:
                T.append(v); blocked |= (set(adj[v]) & coreset)
    return T, score


# ============================================================== PHASE 2 =======
def phase2(core, btil, adj, T, drains, mu, gamma, kplus, kminus, gmin, gmax):
    coreset = set(core)
    SEED = list(dict.fromkeys(list(T) + sorted(drains)))
    tier = {v: 2 for v in core}
    for v in drains: tier[v] = 1
    for v in T: tier[v] = 0
    phi = {}; basin = {}; bal = {}; final = set()

    def w(u, v):
        return 1.0 + gamma * (max(0.0, btil[u]) + max(0.0, btil[v])) / 2.0

    def g(t):
        val = mu[t] * (1.0 + kplus * max(0.0, bal[t])) / (1.0 + kminus * max(0.0, -bal[t]))
        return min(max(val, gmin), gmax)

    PQ = []
    for t in SEED:
        phi[t] = 0.0; basin[t] = t; bal[t] = btil[t]; final.add(t)
        heapq.heappush(PQ, (0.0, t, t))
    # seeds' neighbours must be pushed too
    for t in SEED:
        for u in adj[t]:
            if u in coreset and u not in final:
                heapq.heappush(PQ, (w(t, u) * g(basin[t]), u, t))
    parent = {}
    while PQ:
        k, v, par = heapq.heappop(PQ)
        if v in final:
            continue
        phi[v] = k; basin[v] = basin[par]; parent[v] = par; final.add(v)
        bal[basin[v]] += btil[v]
        for u in adj[v]:
            if u in coreset and u not in final:
                heapq.heappush(PQ, (k + w(v, u) * g(basin[v]), u, v))
    return phi, basin, bal, tier, parent, SEED


# ============================================================== PHASE 3 =======
def phase3(core, phi, tier, pend_edges, adj):
    coreset = set(core)
    key = {v: (phi[v], tier[v], v) for v in core}
    directed = list(pend_edges)
    for (u, v) in EDGES_UND:
        if u in coreset and v in coreset:
            directed.append((u, v) if key[u] > key[v] else (v, u))
    return directed, key


# ============================================================== PHASE 4 =======
def phase4(core, btil, directed, key):
    coreset = set(core)
    outs = collections.defaultdict(list)
    for (u, v) in directed:
        if u in coreset and v in coreset:
            outs[u].append(v)
    inc = sorted(core, key=lambda v: key[v])          # increasing key
    dfc = {}
    for v in inc:
        dfc[v] = max(0.0, -btil[v]) + sum(dfc[u] for u in outs[v])
    inflow = {v: 0.0 for v in core}
    unserved = 0.0; stranded = 0.0
    for v in sorted(core, key=lambda v: -key[v][0] if False else key[v], reverse=True):
        if btil[v] > 0:
            out = inflow[v] + btil[v]
        else:
            served = min(inflow[v], -btil[v])
            unserved += (-btil[v]) - served
            out = inflow[v] - served
        tg = outs[v]
        if not tg:
            stranded += out
        else:
            wsum = sum(dfc[t] for t in tg)
            for t in tg:
                share = (dfc[t] / wsum) if wsum > 0 else 1.0 / len(tg)
                inflow[t] += out * share
    return unserved, stranded


# ============================================================== driver ========
def run_basin(b, adj, S, params=P, K=None):
    core, btil, pendants, drains, pend_edges = phase0(b, adj)
    if not core or len(core) <= 1:
        return dict(core=core, T=[], directed=pend_edges, S_actual=0, unserved=0.0,
                    tree=True, drains=drains, btil=btil)
    S_eff = S
    if S_eff < 1 and not drains:
        S_eff = 1                                     # feasibility check
    T, score = phase1(core, btil, adj, S_eff, params["lam"], params["R"])
    mu = {t: 1.0 for t in list(dict.fromkeys(list(T) + sorted(drains)))}
    scale = sum(max(0.0, -btil[v]) for v in core) or 1.0
    best = None
    for it in range(K if K is not None else params["K"]):
        phi, basin, bal, tier, parent, SEED = phase2(
            core, btil, adj, T, drains, mu, params["gamma"], params["kplus"],
            params["kminus"], params["gmin"], params["gmax"])
        directed, key = phase3(core, phi, tier, pend_edges, adj)
        unserved, stranded = phase4(core, btil, directed, key)
        rec = dict(core=core, T=T, directed=directed, S_actual=len(T), unserved=unserved,
                   stranded=stranded, phi=phi, key=key, basin=basin, bal=dict(bal),
                   tier=tier, drains=drains, btil=btil, tree=False, iters=it + 1)
        if best is None or unserved < best["unserved"] - 1e-15:
            best = rec
        for t in mu:
            mu[t] = mu[t] * np.exp(-params["eta"] * bal[t] / scale)
    return best


def sinks_of(directed, n=N):
    od = collections.Counter(u for u, _ in directed)
    return [i for i in range(n) if od[i] == 0], od


def has_cycle(directed, n=N):
    adjd = collections.defaultdict(list)
    for u, v in directed:
        adjd[u].append(v)
    col = [0] * n; path = []; found = []
    def dfs(u):
        col[u] = 1; path.append(u)
        for w_ in adjd[u]:
            if col[w_] == 1:
                found.append(path[path.index(w_):] + [w_]); return True
            if col[w_] == 0 and dfs(w_): return True
        path.pop(); col[u] = 2; return False
    for i in range(n):
        if col[i] == 0 and dfs(i): return found[0]
    return None


if __name__ == "__main__":
    ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
    S0, C0, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
    gi = GOODS.index("spices"); b = S0[gi] - C0[gi]
    core, btil, pend, drains, pe = phase0(b, UND)
    print("PHASE 0: core=%d of %d | pendant edges=%d | drains=%d" % (len(core), N, len(pe), len(drains)))
    for S in (1, 3, 5, 8, 13):
        r = run_basin(b, UND, S)
        sk, od = sinks_of(r["directed"])
        print("S=%-3d S_actual=%-3d sinks=%-3d unserved=%.6f stranded=%.6f acyclic=%s  T=%s"
              % (S, r["S_actual"], len(sk), r["unserved"], r["stranded"],
                 has_cycle(r["directed"]) is None, [ORDER[t] for t in r["T"]][:6]))
