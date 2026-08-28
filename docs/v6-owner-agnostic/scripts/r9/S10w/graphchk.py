# Graph-structure checks: V009, V091, V095, V092, V132, V135, V130, connectivity (V031 premise)
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

HERE = os.path.dirname(os.path.abspath(__file__))
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"

ND = json.load(open(os.path.join(HERE, "nodes.json")))
ORDER, NODES = ND["order"], ND["nodes"]
N = len(ORDER)
NIDX = {n: i for i, n in enumerate(ORDER)}

UND = [set() for _ in range(N)]
EDGES = []
for n in ORDER:
    for m in NODES[n]["outgoing"]:
        a, b = NIDX[n], NIDX[m]
        UND[a].add(b); UND[b].add(a)
        EDGES.append((a, b))
EDGES_UND = sorted(set(tuple(sorted((a, b))) for a, b in EDGES))

print("== V091: edge counts ==")
print("declared directed links:", len(EDGES), "| distinct undirected:", len(EDGES_UND),
      "| arcs presented to flow solve (2x):", 2 * len(EDGES_UND))

print("\n== V009: min degree + bridges ==")
deg = [len(UND[i]) for i in range(N)]
print("min degree:", min(deg), "at", [ORDER[i] for i in range(N) if deg[i] == min(deg)][:5])
print("degree-1 nodes:", sum(1 for d in deg if d == 1))

# bridges via Tarjan
timer = [0]; disc = [-1]*N; low = [0]*N; bridges = []
def dfs(root):
    stack = [(root, -1, iter(UND[root]))]
    disc[root] = low[root] = timer[0]; timer[0] += 1
    while stack:
        u, parent, it = stack[-1]
        adv = False
        for v in it:
            if disc[v] == -1:
                disc[v] = low[v] = timer[0]; timer[0] += 1
                stack.append((v, u, iter(UND[v]))); adv = True; break
            elif v != parent:
                low[u] = min(low[u], disc[v])
        if not adv:
            stack.pop()
            if stack:
                p = stack[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] > disc[p]:
                    bridges.append((p, u))
for i in range(N):
    if disc[i] == -1:
        dfs(i)
print("bridges:", len(bridges), [(ORDER[a], ORDER[b]) for a, b in bridges])

print("\n== connectivity (V031 premise) ==")
seen = [False]*N; comps = 0
for i in range(N):
    if not seen[i]:
        comps += 1; st = [i]; seen[i] = True
        while st:
            u = st.pop()
            for v in UND[u]:
                if not seen[v]: seen[v] = True; st.append(v)
print("connected components:", comps)

print("\n== V095: topological declaration order ==")
viol = [(n, m) for n in ORDER for m in NODES[n]["outgoing"] if NIDX[n] > NIDX[m]]
print("links violating sources-first declaration order:", len(viol), "of", len(EDGES), viol[:10])

print("\n== V092: siberia members that are coastal ==")
coastal = set(json.load(open(os.path.join(HERE, "coastal.json"))))
sib = [p for p in NODES["siberia"]["members"] if p in coastal]
print("siberia coastal members:", sib, "| inland flag:", NODES["siberia"]["inland"])

print("\n== V132/V135: LAND member counts ==")
dm = pdx.load(os.path.join(EU4, "map", "default.map"))
sea = set(int(x) for x in pdx.values(dm.get("sea_starts")))
lakes = set(int(x) for x in pdx.values(dm.get("lakes"))) if dm.get("lakes") else set()
nonland = sea | lakes
land_ct = {n: sum(1 for p in NODES[n]["members"] if p not in nonland) for n in ORDER}
tot_ct = {n: len(NODES[n]["members"]) for n in ORDER}
mx = sorted(land_ct.items(), key=lambda kv: -kv[1])[:6]
mn = sorted(land_ct.items(), key=lambda kv: kv[1])[:6]
print("largest land counts:", mx)
print("smallest land counts:", mn)
for t in ("cape_of_good_hope", "girin", "nippon", "champagne", "mexico"):
    print("  %-20s land=%d total_members=%d" % (t, land_ct[t], tot_ct[t]))

print("\n== V130: hop counts (unweighted shortest paths on node graph) ==")
def bfs(src):
    dist = {src: 0}; q = collections.deque([src])
    par = {src: None}
    while q:
        u = q.popleft()
        for v in UND[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; par[v] = u; q.append(v)
    return dist, par
def path(par, dst):
    p = []
    while dst is not None:
        p.append(ORDER[dst]); dst = par[dst]
    return list(reversed(p))
cape, chan, alex = NIDX["cape_of_good_hope"], NIDX["english_channel"], NIDX["alexandria"]
d_cape, par_cape = bfs(cape)
print("cape -> english_channel:", d_cape[chan], "hops:", path(par_cape, chan))
d_alex, par_alex = bfs(alex)
print("alexandria -> english_channel:", d_alex[chan], "hops:", path(par_alex, chan))
for src in ("zanzibar", "gulf_of_aden", "malacca", "ceylon", "comorin_cape"):
    if src in NIDX:
        s = NIDX[src]
        ds, ps = bfs(s)
        via_cape = ds.get(cape, 99) + d_cape[chan]
        via_alex = ds.get(alex, 99) + d_alex[chan]
        print("%-16s -> channel: direct=%d  via cape=%d  via alexandria=%d" %
              (src, ds.get(chan, -1), via_cape, via_alex))
