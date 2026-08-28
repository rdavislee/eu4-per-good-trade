import collections
import numpy as np
import drain
import flowop
from solver import N, ORDER, NIDX, ROWS, UND, EDGES_UND
from drain import run_drain
from flowop import mincost_flow, ARCS

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

B = bw()
res = run_drain(B)   # default deterministic=True -> sweep_priority(..., "defasc_beta")
d = res["directed"]
flow_arc = res["flow_arc"]
free = set(res["free"])

outd = collections.Counter(u for u, _v in d)
ind = collections.Counter(v for _u, v in d)
sinks = [ORDER[i] for i in range(N) if outd[i]==0]
print("sinks:", sinks)

for name in ["mexico","gulf_of_siam","sevilla","english_channel","genua"]:
    i = NIDX[name]
    outs = [v for u,v in d if u==i]
    print(f"\n{name}: out-degree={outd[i]} out-neighbors={[ORDER[v] for v in outs]}")
    # classify each out edge as flow_arc or free
    for v in outs:
        # find ei for pair (i,v) or (v,i)
        for ei,(a,b) in enumerate(EDGES_UND):
            if {a,b}=={i,v}:
                kind = "flow_arc" if ei in flow_arc else ("free" if ei in free else "?")
                print(f"    -> {ORDER[v]}: edge kind={kind}")
                break
