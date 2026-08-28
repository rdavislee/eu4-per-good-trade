"""Reference solver for the per-good trade spec, run on the real vanilla
1444.11.11 dataset (00_tradenodes.txt + history/provinces + 00_prices.txt).

Implements exactly the equations in spec §1.1-§1.6:
    s(n,g) = goods_produced(n,g) / sum_m goods_produced(m,g)
    s <- (1-eps)*s + eps/N
    wealth(p) = tax_income(p) + production_income(p)
    c(n,g) = sum_{p in n} wealth(p)^a(g) / sum_{q in world} wealth(q)^a(g)
    L phi_g = s_g - c_g,  phi pinned to mean 0 per component
    V_g = price(g) * sum_m goods_produced(m,g)
    Phi = sum_g V_g phi_g
    phi0 = solve with c at alpha=1 and s = node share of world TRADE VALUE
"""
import os, sys, json, itertools, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

HERE = os.path.dirname(os.path.abspath(__file__))
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

# ---------------------------------------------------------------- game data
ND = json.load(open(os.path.join(HERE, "nodes.json")))
ORDER, NODES = ND["order"], ND["nodes"]
N = len(ORDER)
NIDX = {n: i for i, n in enumerate(ORDER)}

PRICES = {}
for k, v in pdx.load(os.path.join(EU4, "common", "prices", "00_prices.txt")):
    if isinstance(v, pdx.Node):
        PRICES[k] = float(v.get("base_price", 1.0))

PROV = {int(k): v for k, v in json.load(open(os.path.join(HERE, "prov1444.json"))).items()}

# province -> node
PNODE = {}
for n in ORDER:
    for p in NODES[n]["members"]:
        PNODE[p] = n

EXCLUDED = {"gold", "unknown"}
GOODS = sorted(g for g in PRICES if g not in EXCLUDED)

# adjacency (undirected, from the vanilla file)
UND = [[] for _ in range(N)]
EDGES = []
for n in ORDER:
    for m in NODES[n]["outgoing"]:
        a, b = NIDX[n], NIDX[m]
        UND[a].append(b); UND[b].append(a)
        EDGES.append((a, b))
EDGES_UND = sorted(set(tuple(sorted(e)) for e in EDGES))

# ------------------------------------------------------- province quantities
GOODS_PRODUCED_FACTOR = 0.2   # EU4: goods produced = 0.2 * base_production


# spec v4.0 §1.3: local modifiers that (a) depend only on the province's own attributes and
# (b) modify a quantity `wealth` computes.  Read from common/tradegoods/00_tradegoods.txt.
LOCAL_TAX_MOD = {"gems": 0.15}          # local_tax_modifier   -> tax_value
LOCAL_TV_MOD  = {"incense": 0.10}       # trade_value_modifier -> trade_value
# glass local_production_efficiency and chinaware local_autonomy are local but modify quantities
# wealth does not compute (production income; autonomy), so they do not enter.


def province_table():
    rows = []
    for pid, s in PROV.items():
        if not s.get("owner") or s.get("is_city") != "yes":
            continue
        node = PNODE.get(pid)
        if node is None:
            continue
        g = s.get("trade_goods")
        gp = GOODS_PRODUCED_FACTOR * s["base_production"]
        price = PRICES.get(g, 0.0)
        rows.append(dict(pid=pid, node=node, good=g, gp=gp,
                         tax=s["base_tax"] * (1.0 + LOCAL_TAX_MOD.get(g, 0.0)),
                         prod_income=gp * price * (1.0 + LOCAL_TV_MOD.get(g, 0.0)),
                         owner=s["owner"]))
    return rows


ROWS = province_table()


def build_sc(alpha_of_good, eps=1e-6, wealth_key=None):
    """returns S[G,N] supply shares, C[G,N] demand shares, V[G] values"""
    G = len(GOODS)
    gp = np.zeros((G, N))
    for r in ROWS:
        if r["good"] in EXCLUDED or r["good"] not in PRICES:
            continue
        gi = GOODS.index(r["good"])
        gp[gi, NIDX[r["node"]]] += r["gp"]
    world = gp.sum(axis=1)
    S = np.zeros((G, N))
    live = world > 0
    S[live] = gp[live] / world[live][:, None]
    # epsilon regularizer, field-level
    S[live] = (1 - eps) * S[live] + eps / N

    wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
    pn = np.array([NIDX[r["node"]] for r in ROWS])
    C = np.zeros((G, N))
    for gi, g in enumerate(GOODS):
        a = alpha_of_good(g)
        w = wealth ** a
        tot = w.sum()
        np.add.at(C[gi], pn, w / tot)
    V = np.array([PRICES[g] * world[gi] for gi, g in enumerate(GOODS)])
    return S, C, V, live, gp, world


# ------------------------------------------------------------------- solver
def laplacian():
    L = np.zeros((N, N))
    for a, b in EDGES_UND:
        L[a, a] += 1; L[b, b] += 1
        L[a, b] -= 1; L[b, a] -= 1
    return L


L = laplacian()


def components():
    seen = [-1] * N
    comps = []
    for i in range(N):
        if seen[i] >= 0:
            continue
        c = len(comps); stack = [i]; seen[i] = c; members = []
        while stack:
            u = stack.pop(); members.append(u)
            for v in UND[u]:
                if seen[v] < 0:
                    seen[v] = c; stack.append(v)
        comps.append(members)
    return comps, seen


COMPS, COMPOF = components()


def solve_phi(b):
    """solve L phi = b per component, pin mean 0 in each component."""
    phi = np.zeros(N)
    for members in COMPS:
        m = np.array(members)
        if len(m) == 1:
            continue
        sub = L[np.ix_(m, m)]
        rhs = b[m].copy()
        rhs -= rhs.mean()                       # renormalize so it balances
        # pin: add rank-1 to make SPD (grounded Laplacian via mean-zero pin)
        A = sub + np.ones((len(m), len(m))) / len(m)
        x = np.linalg.solve(A, rhs)
        x -= x.mean()
        phi[m] = x
    return phi


def solve_all(alpha_of_good, eps=1e-6):
    S, C, V, live, gp, world = build_sc(alpha_of_good, eps)
    PHI = np.zeros((len(GOODS), N))
    for gi in range(len(GOODS)):
        if not live[gi]:
            continue
        PHI[gi] = solve_phi(S[gi] - C[gi])
    Phi = (V[:, None] * PHI).sum(axis=0)
    return dict(S=S, C=C, V=V, live=live, PHI=PHI, Phi=Phi, gp=gp, world=world)


def solve_phi0():
    """single solve: demand at alpha=1, supply = node share of world trade value"""
    tv = np.zeros(N)
    for r in ROWS:
        if r["good"] in EXCLUDED or r["good"] not in PRICES:
            continue
        tv[NIDX[r["node"]]] += r["gp"] * PRICES[r["good"]]
    s0 = tv / tv.sum()
    wealth = np.array([r["tax"] + r["prod_income"] for r in ROWS])
    pn = np.array([NIDX[r["node"]] for r in ROWS])
    c0 = np.zeros(N)
    np.add.at(c0, pn, wealth / wealth.sum())
    return solve_phi(s0 - c0), s0, c0


def orient(phi, tol=0.0):
    """directed edges u->v where phi[u] > phi[v] (+tol)"""
    out = []
    for a, b in EDGES_UND:
        if phi[a] > phi[b] + tol:
            out.append((a, b))
        elif phi[b] > phi[a] + tol:
            out.append((b, a))
    return out


def is_acyclic(directed, n=N):
    adj = collections.defaultdict(list)
    indeg = [0] * n
    for u, v in directed:
        adj[u].append(v); indeg[v] += 1
    q = [i for i in range(n) if indeg[i] == 0]
    seen = 0
    while q:
        u = q.pop(); seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen == n
