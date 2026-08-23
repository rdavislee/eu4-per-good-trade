import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)

order_idx = np.argsort(-NW)
rank = {ORDER[i]: k+1 for k, i in enumerate(order_idx)}

print("Top 10 nodes by node wealth:")
for k, i in enumerate(order_idx[:10]):
    print(k+1, ORDER[i], round(float(NW[i]), 1))

for name in ["english_channel", "genua", "mexico", "gulf_of_siam", "sevilla", "hangzhou", "venice"]:
    i = NIDX[name]
    print(name, "wealth=%.1f" % NW[i], "rank=%d" % rank[name])

# now compute Phi_w baseline (alpha=2 aggregate) sinks & flow in/out per node
A_PHI = 2.0
def cv(a=A_PHI, w=None):
    w = W if w is None else w
    t = (w / w.max()) ** a; n = np.zeros(N); np.add.at(n, pn, t); return n / n.sum()
base = run_drain(np.full(N, 1.0/N) - cv())
directed = base["directed"]
outd = collections.Counter(u for u,_ in directed)
ind = collections.Counter(v for u,v in directed)
sinks = sorted(ORDER[i] for i in range(N) if outd[i]==0)
print("Phi_w (alpha=2) sinks:", sinks)

# flow: use b_w = full(1/N) - cv() as demand vector (net flow into node = b_w?), but real "flow_in - flow_out" needs a specific good's flow model;
# Here we just check degree-based: is english_channel a sink (no outgoing edges)?
for name in ["english_channel", "genua", "mexico", "gulf_of_siam", "sevilla"]:
    i = NIDX[name]
    print(name, "out-degree(directed)=%d in-degree=%d is_sink=%s" % (outd[i], ind[i], outd[i]==0))
