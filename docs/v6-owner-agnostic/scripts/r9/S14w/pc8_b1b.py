import os, sys, io, contextlib
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import flowop
from flowop import ARCS, AEQ, TIE_COST
from solver import N, GOODS, PRICES, EDGES_UND, build_sc
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
gi = GOODS.index("copper"); B = S[gi] - C[gi]
def orient(tol, perm):
    opts = None if tol is None else {"dual_feasibility_tolerance": tol, "primal_feasibility_tolerance": tol}
    with contextlib.redirect_stderr(io.StringIO()):
        r = linprog(c=TIE_COST[perm], A_eq=AEQ[:, perm], b_eq=np.zeros(N) - B, bounds=(0, None),
                    method="highs", options=opts)
    x = np.zeros(len(ARCS)); x[perm] = r.x
    net = np.zeros(len(EDGES_UND))
    for ai, (_u,_v,ei,sg) in enumerate(ARCS): net[ei] += sg*x[ai]
    return tuple(np.sign(np.where(np.abs(net) > 1e-11, net, 0.0)).astype(int))
ref = orient(None, np.arange(len(ARCS)))
for seed in (4, 20260821, 7, 4242):
    rng = np.random.default_rng(seed)
    six = [rng.permutation(len(ARCS)) for _ in range(6)]
    fl = [sum(1 for a,b in zip(ref, orient(None,p)) if a!=b) for p in six]
    rng2 = np.random.default_rng(seed)
    four = [rng2.permutation(len(ARCS)) for _ in range(4)]
    fl2 = [sum(1 for a,b in zip(ref, orient(None,p)) if a!=b) for p in four]
    print("seed %-10s  draw-6 first4 sum=%2d   draw-4 sum=%2d   equal=%s" % (seed, sum(fl[:4]), sum(fl2), sum(fl[:4])==sum(fl2)))
import scipy; print("scipy", scipy.__version__)
