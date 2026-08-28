import collections
import numpy as np
import drain
import flowop
from solver import N, ORDER, NIDX, ROWS
from drain import run_drain, phase0, phase1, phase2, sweep_priority, compile_dirs
from flowop import mincost_flow, ARCS

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N)
np.add.at(NODEW, PN, W)

def bw(alpha=A_PHI):
    t = (W / W.max()) ** alpha
    n = np.zeros(N)
    np.add.at(n, PN, t)
    return np.full(N, 1.0 / N) - n / n.sum()

B = bw()
f, duals, res = mincost_flow(B + 0, np.zeros(N), cost=flowop.TIE_COST)
fin = np.zeros(N)
fout = np.zeros(N)
for ai, (u, v, _ei, _sg) in enumerate(ARCS):
    fout[u] += f[ai]
    fin[v] += f[ai]

for name in ['sevilla','mexico','gulf_of_siam','english_channel','genua']:
    i = NIDX[name]
    print(name, "b_w=", B[i], "fin=", fin[i], "fout=", fout[i], "deficit(-b_w)=", -B[i])

# out-degree/free-edge structure via phase0-2 + sweep_priority + compile_dirs
core, beta, Plog = phase0(B)
Sset, info = phase1(core, beta)
fa, free, net, cost = phase2(core, beta)
o, S2, promo, fb = sweep_priority(core, beta, Sset, fa, free, net, "def_beta")
d = compile_dirs(core, o, fa, free, Plog, beta)
outd = collections.Counter(u for u, _v in d)
ind = collections.Counter(v for _u, v in d)

# distinguish flow-arc edges vs free edges in d
flow_arc_pairs = set()
for ai,(u,v,ei,sg) in enumerate(ARCS):
    if f[ai] > 1e-12:
        flow_arc_pairs.add((u,v))

for name in ['sevilla','mexico','gulf_of_siam']:
    i = NIDX[name]
    outs = [v for u,v in d if u==i]
    print(name, "out-degree in d:", outd[i], "out-neighbors:", [ORDER[v] for v in outs])
    print("   fout[i]=", fout[i], " nonzero flow out-arcs from i (f[ai]>1e-12):", 
          [(ORDER[u],ORDER[v]) for ai,(u,vv,ei,sg) in enumerate(ARCS) if u==i and f[ai]>1e-12])

sinks = [ORDER[i] for i in range(N) if outd[i]==0]
print("sinks (out-degree 0 in final directed graph):", sinks)

# count nodes with out-degree>0 in d, but fout==0 (zero flow) - matches round6.out "18 of 80"
cnt = sum(1 for i in range(N) if outd[i]>0 and fout[i] < 1e-12)
print("nodes outdeg>0 but fout~0:", cnt)
namez = [ORDER[i] for i in range(N) if outd[i]>0 and fout[i] < 1e-12]
print(sorted(namez))
