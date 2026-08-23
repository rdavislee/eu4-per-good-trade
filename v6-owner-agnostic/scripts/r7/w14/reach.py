import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
A_PHI = 2.0
def cv(a=A_PHI):
    t = (W / W.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
def bw(a=A_PHI): return np.full(N, 1.0/N) - cv(a)
base = run_drain(bw())
directed = base["directed"]
adj = collections.defaultdict(list)
for u,v in directed:
    adj[u].append(v)

def reaches(a, b):
    seen = set(); stack=[NIDX[a]]
    target = NIDX[b]
    path = {}
    while stack:
        u = stack.pop()
        if u == target: return True, path
        if u in seen: continue
        seen.add(u)
        for v in adj[u]:
            if v not in seen:
                path[v] = u
                stack.append(v)
    return False, path

ok, path = reaches("english_channel", "genua")
print("english_channel reaches genua:", ok)
if ok:
    # reconstruct
    cur = NIDX["genua"]; chain=[cur]
    while cur != NIDX["english_channel"]:
        cur = path[cur]; chain.append(cur)
    print(" path:", " -> ".join(ORDER[i] for i in reversed(chain)))

for name in ["mexico", "gulf_of_siam", "sevilla"]:
    ok, _ = reaches(name, "genua")
    print(name, "reaches genua:", ok)
    ok2, _ = reaches(name, "hangzhou")
    print(name, "reaches hangzhou:", ok2)
