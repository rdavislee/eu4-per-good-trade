# Identity-permutation agreement of the UNPATCHED v5 reimplementation (unit-cost Phase 2)
# against the shipped drain.py (TIE_COST Phase 2).  Tests spec 2.4 item 1's parenthetical
# "did abort ... and disagreed on 26 of 159 edges".
import collections, io, os, sys, types
import numpy as np
HERE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic\scripts"
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
src = io.open(os.path.join(V5, "_audit_b_drain.py"), encoding="utf-8").read()
ab = types.ModuleType("abd_raw"); ab.__dict__["__name__"] = "abd_raw"
exec(compile(src, "_audit_b_drain[raw]", "exec"), ab.__dict__)
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NODEW = np.zeros(N); np.add.at(NODEW, pn, W)
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()
ship = set(run_drain(BW)["directed"])
r = ab.drain(list(ORDER), sorted(EDGES_UND), BW, NODEW)
d = set(r["directed"] if isinstance(r, dict) else r)
print("unpatched (unit-cost) instrument vs drain.py on identity:")
print("  edges agreeing : %d of %d" % (len(d & ship), len(ship)))
print("  edges disagreeing : %d" % (len(ship) - len(d & ship)))
od = collections.Counter(u for u,_ in d)
print("  its sinks:", sorted(ORDER[i] for i in range(N) if od[i]==0))
