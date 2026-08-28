import collections, numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
import drain
from drain import run_drain, sinks_of

# Y022: counted provinces per node
cnt = collections.Counter(r["node"] for r in ROWS)
per = [cnt.get(n, 0) for n in ORDER]
print("provinces per node: min %d max %d; zero-count nodes: %s" % (min(per), max(per),
      [ORDER[i] for i in range(N) if per[i]==0]))

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
GL = [(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]

# Y255: per-good sink sets
sinksets = {}
for gi,g in GL:
    r = run_drain(S0m[gi]-C0m[gi])
    sk,_ = sinks_of(r["directed"])
    sinksets[g] = frozenset(sk)
distinct = len(set(sinksets.values()))
inall = [ORDER[i] for i in range(N) if all(i in s for s in sinksets.values())]
union = set().union(*sinksets.values())
print("distinct per-good sink sets: %d of %d goods; nodes that are sinks for ALL goods: %s; union size %d" % (distinct, len(GL), inall, len(union)))

# Y269: six identical aggrgate solves in one process
Wp = np.array([r["tax"]+r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
def bw(a=2.0):
    t = (Wp)**a; n=np.zeros(N); np.add.at(n,pn,t); n/=n.sum()
    return np.full(N,1.0/N)-n
sigs=set()
for i in range(6):
    r = run_drain(bw())
    sigs.add((frozenset(r["directed"]), frozenset(r["S"])))
print("six identical aggregate solves -> distinct orientations: %d" % len(sigs))
# and six per-good solves for one good
sigs2=set()
gi = GOODS.index("spices")
for i in range(6):
    r = run_drain(S0m[gi]-C0m[gi]); sigs2.add(frozenset(r["directed"]))
print("six identical spices solves  -> distinct orientations: %d" % len(sigs2))

# Y972 context: aggregate sinks at alpha 1.5 (current operator) and at 2.0
for a in (1.5, 2.0):
    r = run_drain(bw(a)); sk,_ = sinks_of(r["directed"])
    print("alpha_Phi %.1f sinks (tie-break cost): %s" % (a, sorted(ORDER[i] for i in sk)))
