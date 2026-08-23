# Y141 parenthetical: does the OLD (unit-cost) reimplementation objective disagree with drain.py's
# shipped (tie-break) support on the identity permutation, and by how many of 159 edges?
import io, os, sys, types, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(HERE, "..", "..", "v5-owner-agnostic", "scripts")
sys.path.insert(0, HERE); os.chdir(HERE)
from solver import N, ORDER, NIDX, EDGES_UND, ROWS
from drain import run_drain
from flowop import LP_OPTS

_p5 = os.path.join(V5, "_audit_b_drain.py")
_src = io.open(_p5, encoding="utf-8").read()
# leave the reimplementation UNPATCHED: it still minimises unit arc cost natively
ab = types.ModuleType("abd_unit"); ab.__dict__["__name__"] = "abd_unit"
exec(compile(_src, "_audit_b_drain[unit,unpatched]", "exec"), ab.__dict__)

W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
t = (W / W.max()) ** 2.0
num = np.zeros(N); np.add.at(num, pn, t)
BW = np.full(N, 1.0 / N) - num / num.sum()

shipped = run_drain(BW)
SHIP_E = set(shipped["directed"])

perm = list(range(N))
names = ORDER[:]
edges = sorted(tuple(sorted((u, v))) for u, v in EDGES_UND)
r = ab.drain(names, edges, BW, np.zeros(N))
d = r["directed"] if isinstance(r, dict) else r
d = set(d)
print("edges agreeing (unpatched/unit-cost reimpl vs shipped tie-break support): %d of %d"
      % (len(d & SHIP_E), len(SHIP_E)))
print("edges disagreeing: %d of %d" % (len(SHIP_E) - len(d & SHIP_E) + len(d - SHIP_E) - len(d&SHIP_E)+len(d&SHIP_E), len(SHIP_E)))
sym = d ^ SHIP_E
print("symmetric difference size:", len(sym))
