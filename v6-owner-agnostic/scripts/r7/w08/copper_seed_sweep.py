# -*- coding: utf-8 -*-
import os, sys, io as _io, contextlib
import numpy as np
HERE = os.path.abspath(os.path.join(os.getcwd(), "..", ".."))
sys.path.insert(0, HERE); os.chdir(HERE)
import flowop
from solver import N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from flowop import ARCS
from scipy.optimize import linprog

A_PHI = 2.0
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
PN = np.array([NIDX[r["node"]] for r in ROWS])
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
AEQ, A_ = flowop.AEQ, len(ARCS)

_gi = GOODS.index("copper")
_b = S[_gi] - C[_gi]

def _orient_at(tol, perm):
    opts = None if tol is None else {"dual_feasibility_tolerance": tol,
                                     "primal_feasibility_tolerance": tol}
    cost = flowop.TIE_COST[perm]
    aeq = flowop.AEQ[:, perm]
    with contextlib.redirect_stderr(_io.StringIO()):
        r = linprog(c=cost, A_eq=aeq, b_eq=np.zeros(N) - _b, bounds=(0, None),
                    method="highs", options=opts)
    x = np.zeros(len(ARCS))
    x[perm] = r.x
    net = np.zeros(len(EDGES_UND))
    for ai, (_u, _v, ei, sg) in enumerate(ARCS):
        net[ei] += sg * x[ai]
    return tuple(np.sign(np.where(np.abs(net) > 1e-11, net, 0.0)).astype(int))

SEEDS = [int(x) for x in sys.argv[1:]]
for seed in SEEDS:
    _rng = np.random.default_rng(seed)
    _perms = [np.arange(len(ARCS))] + [_rng.permutation(len(ARCS)) for _ in range(4)]
    _flipsets = {}
    for tol in (None, 1e-7, 1e-8, 1e-10, 1e-11):
        ref = _orient_at(tol, _perms[0])
        fset = set()
        for pi, p in enumerate(_perms[1:], 1):
            got = _orient_at(tol, p)
            for slot, (a, b) in enumerate(zip(ref, got)):
                if a != b:
                    fset.add((pi, slot))
        _flipsets[tol] = fset
    idagree = _flipsets[None] == _flipsets[1e-7]
    revert = _flipsets[1e-11] == _flipsets[None]
    lowempty = _flipsets[1e-8] == _flipsets[1e-10] == set()
    print("seed %-6d flips: none=%d 1e-7=%d 1e-8=%d 1e-10=%d 1e-11=%d | unset==1e-7:%s rejected1e-11==unset:%s 1e-8==1e-10==empty:%s"
          % (seed, len(_flipsets[None]), len(_flipsets[1e-7]), len(_flipsets[1e-8]), len(_flipsets[1e-10]), len(_flipsets[1e-11]),
             idagree, revert, lowempty))
