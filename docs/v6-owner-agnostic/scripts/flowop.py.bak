# -*- coding: utf-8 -*-
"""Three orientation operators on the same 1444 data:
     LAP   - the current Laplacian potential (spec 1.1), uniform eps
     FLOW  - per-good min-cost flow on the undirected adjacency, unit arc cost,
             targeted eps (eps supply only to nodes with c(g)==0)
     TREE  - spanning-tree subtree-sign baseline, targeted eps
No tuning: every constant is taken from the spec or from the brief.
"""
import numpy as np, collections, sys, os
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, PROV, PNODE,
                    ROWS, EXCLUDED, build_sc, solve_phi, orient, laplacian, COMPS)

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
EPS = 1e-6                      # spec 1.2 value, unchanged
DEG = np.array([len(UND[i]) for i in range(N)])
E = len(EDGES_UND)              # 159
ZERO_TOL = 1e-11                # net flow below this counts as zero

# ------------------------------------------------------------------ inputs ---
S0, C0, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)     # raw, no eps
S_UNI, _, _, _, _, _ = build_sc(ALPHA, eps=EPS)           # spec 1.2 uniform eps


def s_targeted(gi):
    """eps supply to nodes with zero demand for this good, nothing to the rest."""
    s = S0[gi].copy()
    s[C0[gi] == 0.0] += EPS
    return s / s.sum()


# ----------------------------------------------------------- arc structures --
ARCS = []                                  # (u, v, edge_index, sign)
for ei, (u, v) in enumerate(EDGES_UND):
    ARCS.append((u, v, ei, +1))
    ARCS.append((v, u, ei, -1))
A = len(ARCS)
_rows, _cols, _vals = [], [], []
for ai, (u, v, ei, sg) in enumerate(ARCS):
    _rows += [v, u]; _cols += [ai, ai]; _vals += [1.0, -1.0]   # inflow - outflow
AEQ = csr_matrix((_vals, (_rows, _cols)), shape=(N, A))


def mincost_flow(s, c):
    """min sum(f) s.t. inflow-outflow = c - s, f >= 0. Returns (arcflow, duals, res)."""
    b = c - s
    res = linprog(c=np.ones(A), A_eq=AEQ, b_eq=b, bounds=(0, None), method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    duals = None
    if getattr(res, "eqlin", None) is not None:
        duals = np.asarray(res.eqlin.marginals)
    return res.x, duals, res


def net_per_edge(f):
    net = np.zeros(E)
    for ai, (u, v, ei, sg) in enumerate(ARCS):
        net[ei] += sg * f[ai]
    return net


def has_cycle(directed):
    adj = collections.defaultdict(list)
    for u, v in directed:
        adj[u].append(v)
    colour = [0] * N
    stack_path = []
    found = []

    def dfs(u):
        colour[u] = 1; stack_path.append(u)
        for w in adj[u]:
            if colour[w] == 1:
                found.append(stack_path[stack_path.index(w):] + [w]); return True
            if colour[w] == 0 and dfs(w):
                return True
        stack_path.pop(); colour[u] = 2; return False

    for i in range(N):
        if colour[i] == 0 and dfs(i):
            return found[0]
    return None


def cancel_cycles(net):
    """Remove directed cycles from a net-flow vector by cancelling the minimum
    flow around each cycle. Returns (net, [(cycle, amount_cancelled), ...])."""
    net = net.copy()
    removed = []
    for _ in range(10000):
        directed = edges_from_net(net)
        cyc = has_cycle(directed)
        if cyc is None:
            break
        # map cycle node pairs back to edge indices and cancel the min |net|
        eidx, sgn = [], []
        for a, b in zip(cyc, cyc[1:]):
            for ei, (u, v) in enumerate(EDGES_UND):
                if (u, v) == (a, b):
                    eidx.append(ei); sgn.append(+1); break
                if (v, u) == (a, b):
                    eidx.append(ei); sgn.append(-1); break
        amt = min(abs(net[ei]) for ei in eidx)
        for ei, sg in zip(eidx, sgn):
            net[ei] -= sg * amt
        removed.append(([ORDER[x] for x in cyc], amt))
    return net, removed


def edges_from_net(net):
    out = []
    for ei, (u, v) in enumerate(EDGES_UND):
        if net[ei] > ZERO_TOL:
            out.append((u, v))
        elif net[ei] < -ZERO_TOL:
            out.append((v, u))
    return out


# ------------------------------------------------------------------- TREE ----
def spanning_tree(root, order="bfs"):
    parent = {root: None}; kids = collections.defaultdict(list); seq = [root]
    if order == "bfs":
        q = collections.deque([root])
        pop = q.popleft
    else:
        q = collections.deque([root]); pop = q.pop
    seen = {root}
    tree_edges = set()
    while q:
        u = pop()
        for v in UND[u]:
            if v not in seen:
                seen.add(v); parent[v] = u; kids[u].append(v); seq.append(v)
                q.append(v)
                tree_edges.add(tuple(sorted((u, v))))
    return parent, kids, seq, tree_edges


def tree_orient(gi, root, order="bfs"):
    s = s_targeted(gi); c = C0[gi]
    b = s - c
    parent, kids, seq, tree_edges = spanning_tree(root, order)
    T = np.zeros(N)
    for u in reversed(seq):                    # children precede parents reversed
        T[u] = b[u] + sum(T[v] for v in kids[u])
    directed = []
    for ei, (u, v) in enumerate(EDGES_UND):
        key = tuple(sorted((u, v)))
        if key in tree_edges:
            child = v if parent.get(v) == u else u
            other = u if child == v else v
            directed.append((child, other) if T[child] > 0 else (other, child))
        else:
            if T[u] > T[v]:
                directed.append((u, v))
            elif T[v] > T[u]:
                directed.append((v, u))
    return directed, T, tree_edges


# ------------------------------------------------------------------- runner --
def sinks_of(directed):
    od = collections.Counter(u for u, _ in directed)
    return [i for i in range(N) if od[i] == 0], od


def run_all():
    out = {}
    for gi, g in enumerate(GOODS):
        if not LIVE[gi]:
            continue
        rec = {}
        # LAP: current operator, uniform eps
        phi = solve_phi(S_UNI[gi] - C0[gi])
        rec["lap_dir"] = orient(phi); rec["phi"] = phi
        # FLOW
        s = s_targeted(gi)
        f, duals, res = mincost_flow(s, C0[gi])
        net = net_per_edge(f)
        net2, removed = cancel_cycles(net)
        rec["flow_net"] = net2
        rec["flow_raw_net"] = net
        rec["flow_cycles"] = removed
        rec["flow_dir"] = edges_from_net(net2)
        rec["flow_duals"] = duals
        rec["flow_cost"] = res.fun
        rec["s_t"] = s
        # TREE, three spanning trees
        rec["tree"] = {}
        for tag, (root, order) in {"bfs@malacca": (NIDX["malacca"], "bfs"),
                                   "bfs@genua": (NIDX["genua"], "bfs"),
                                   "dfs@saxony": (NIDX["saxony"], "dfs")}.items():
            d, T, te = tree_orient(gi, root, order)
            rec["tree"][tag] = {"dir": d, "T": T, "tree_edges": te}
        out[g] = rec
    return out


if __name__ == "__main__":
    R = run_all()
    print("goods solved:", len(R))
    g = "spices"
    net = R[g]["flow_net"]
    print("spices  LP optimal cost = %.6f" % R[g]["flow_cost"])
    print("spices  edges with |net| <= %g : %d of %d" % (ZERO_TOL, int((np.abs(net) <= ZERO_TOL).sum()), E))
    print("spices  oriented edges: %d" % len(R[g]["flow_dir"]))
    print("spices  cycles cancelled:", R[g]["flow_cycles"])
    sk, od = sinks_of(R[g]["flow_dir"])
    print("spices  FLOW sinks:", [ORDER[i] for i in sk])
    sk2, _ = sinks_of(R[g]["lap_dir"])
    print("spices  LAP  sinks:", [ORDER[i] for i in sk2])
