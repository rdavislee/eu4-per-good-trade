import sys, os, collections, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, ROWS, EDGES_UND
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def cv(a=2.0, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a
    n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()

res = run_drain(np.full(N, 1.0/N) - cv())
flow_arc = res["flow_arc"]   # ei -> (u,v) oriented with flow
net = res["net"]             # per-edge signed net flow

si = NIDX["sevilla"]
inflow = 0.0; outflow = 0.0
for ei, (u, v) in flow_arc.items():
    mag = abs(net[ei])
    if v == si: inflow += mag
    if u == si: outflow += mag
print("sevilla node index", si)
print("inflow", inflow, "outflow", outflow)
