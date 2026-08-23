import sys, os, collections
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX, GOODS, PRICES, ROWS, build_sc
from flowop import ARCS, AEQ, A, TIE_COST, LP_OPTS, mincost_flow

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S0m, C0m, V, LIVE, GP, W = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("paper")
s = S0m[gi]; c = C0m[gi]
fl, du, res = mincost_flow(s, c, cost=TIE_COST)
rc = np.array([TIE_COST[ai] - (du[ARCS[ai][1]] - du[ARCS[ai][0]]) for ai in range(A)])
off = np.where(fl <= 1e-12)[0]
zero_rc = [ai for ai in off if abs(rc[ai]) <= 1e-14]
print("off-support arcs with zero reduced cost:", len(zero_rc))
for ai in zero_rc:
    u, v, ei, sg = ARCS[ai]
    print("  arc", ORDER[u], "->", ORDER[v], "reduced cost", rc[ai])

# Now try to force flow onto that arc: minimize (TIE_COST - big*e_j) i.e maximize x_j among optimal solutions
obj0 = float(res.fun)
b = c - s
for ai in zero_rc:
    cost2 = TIE_COST.copy()
    cost2[ai] -= 1.0   # incentivize using this arc while keeping same base cost structure approx
    r2 = linprog(c=cost2, A_eq=AEQ, b_eq=b, bounds=(0, None), method="highs", options=LP_OPTS)
    # check whether obj using ORIGINAL TIE_COST is unchanged (i.e. still an optimal vertex of original LP)
    obj2_orig = float(TIE_COST @ r2.x)
    print("  forcing arc", ai, ": new x[arc]=", r2.x[ai], " original-cost of new solution=", obj2_orig, " vs baseline obj=", obj0, " diff=", obj2_orig-obj0)
