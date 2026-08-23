import sys, os, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a=2.0, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

res = run_drain(np.full(N, 1.0/N) - cv())
directed = res["directed"]
net = {}
for ei,(u,v) in enumerate(directed): pass
# reconstruct flow in/out per node from directed edges with |net flow| via drain's own net array if available
print(res.keys())
