# -*- coding: utf-8 -*-
"""RANK operator: score = s - c on scored nodes, harmonic extension on the empty set.
Compared against LAP (spec 1.1). No tuning.
"""
import numpy as np, collections, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, PNODE, PROV,
                    build_sc, solve_phi, orient, laplacian, EXCLUDED)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
EPS = 1e-6
DEG = np.array([len(UND[i]) for i in range(N)])
E = len(EDGES_UND)

S0, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)      # raw, defines the empty set
S_UNI, _, _, _, _, _ = build_sc(ALPHA, eps=EPS)            # spec 1.2 uniform eps, for LAP
GOODS_LIVE = [g for gi, g in enumerate(GOODS) if LIVE[gi]]
GIDX = {g: GOODS.index(g) for g in GOODS_LIVE}


def empty_set(gi):
    """nodes with neither supply nor demand for this good (raw, pre-eps)"""
    return [i for i in range(N) if S0[gi][i] == 0.0 and C0[gi][i] == 0.0]


def rank_score(gi):
    """score = s - c on scored nodes; harmonic extension on the empty set.
    Returns (score, empty_list, regions, wellposed_flags)."""
    sc = S0[gi] - C0[gi]
    emp = empty_set(gi)
    if not emp:
        return sc, [], [], []
    empset = set(emp)
    # connected components of the empty set
    regions, seen = [], set()
    for i in emp:
        if i in seen:
            continue
        comp = {i}; stack = [i]; seen.add(i)
        while stack:
            u = stack.pop()
            for v in UND[u]:
                if v in empset and v not in comp:
                    comp.add(v); seen.add(v); stack.append(v)
        regions.append(sorted(comp))
    wellposed = []
    score = sc.copy()
    for comp in regions:
        # Dirichlet problem on comp with boundary = scored neighbours
        idx = {n: k for k, n in enumerate(comp)}
        m = len(comp)
        A = np.zeros((m, m)); b = np.zeros(m)
        has_boundary = False
        for n in comp:
            k = idx[n]
            A[k, k] = len(UND[n])
            for v in UND[n]:
                if v in idx:
                    A[k, idx[v]] -= 1.0
                else:
                    b[k] += sc[v]          # fixed boundary value
                    has_boundary = True
        wellposed.append(has_boundary and np.linalg.matrix_rank(A) == m)
        if has_boundary:
            score[comp] = np.linalg.solve(A, b)
        else:
            score[comp] = 0.0              # isolated empty region: no boundary data
    return score, emp, regions, wellposed


def run():
    out = {}
    for g in GOODS_LIVE:
        gi = GIDX[g]
        sc, emp, regions, wp = rank_score(gi)
        out[g] = {"score": sc, "empty": emp, "regions": regions, "wellposed": wp,
                  "rank_dir": orient(sc),
                  "lap_phi": solve_phi(S_UNI[gi] - C0[gi])}
        out[g]["lap_dir"] = orient(out[g]["lap_phi"])
    return out


def sinks_of(directed):
    od = collections.Counter(u for u, _ in directed)
    return [i for i in range(N) if od[i] == 0], od


def has_cycle(directed):
    adj = collections.defaultdict(list)
    for u, v in directed:
        adj[u].append(v)
    col = [0] * N; path = []; found = []
    def dfs(u):
        col[u] = 1; path.append(u)
        for w in adj[u]:
            if col[w] == 1:
                found.append(path[path.index(w):] + [w]); return True
            if col[w] == 0 and dfs(w): return True
        path.pop(); col[u] = 2; return False
    for i in range(N):
        if col[i] == 0 and dfs(i): return found[0]
    return None


def reach_path(directed, a, z):
    adj = collections.defaultdict(list)
    for u, v in directed:
        adj[u].append(v)
    prev = {a: None}; q = collections.deque([a])
    while q:
        x = q.popleft()
        if x == z:
            p = []
            while x is not None: p.append(x); x = prev[x]
            return p[::-1]
        for y in adj[x]:
            if y not in prev:
                prev[y] = x; q.append(y)
    return None


if __name__ == "__main__":
    R = run()
    g = "spices"; gi = GIDX[g]
    sc = R[g]["score"]
    print("empty set size per good:", sorted({len(R[x]['empty']) for x in GOODS_LIVE}))
    print("spices empty set:", [ORDER[i] for i in R[g]["empty"]], "well-posed:", R[g]["wellposed"])
    print("spices score range: %.6f (%s) .. %.6f (%s)"
          % (sc.min(), ORDER[int(np.argmin(sc))], sc.max(), ORDER[int(np.argmax(sc))]))
    sk, od = sinks_of(R[g]["rank_dir"])
    print("RANK spices sinks (%d):" % len(sk), [ORDER[i] for i in sk])
    print("LAP  spices sinks:", [ORDER[i] for i in sinks_of(R[g]["lap_dir"])[0]])
    print("acyclic:", has_cycle(R[g]["rank_dir"]) is None)
    p = reach_path(R[g]["rank_dir"], NIDX["malacca"], NIDX["genua"])
    print("RANK malacca->genua:", " -> ".join(ORDER[x] for x in p) if p else "NO DIRECTED PATH")
