import os,sys,io as _io,contextlib
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from scipy.optimize import linprog
import flowop
from flowop import ARCS
from solver import N,GOODS,PRICES,EDGES_UND,build_sc
ALPHA=lambda g: max(0.2,min(3.0,(PRICES[g]/2.0)**1.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
gi=GOODS.index("copper"); b=S[gi]-C[gi]
def orient(tol,perm):
    opts=None if tol is None else {"dual_feasibility_tolerance":tol,"primal_feasibility_tolerance":tol}
    cost=flowop.TIE_COST[perm]; aeq=flowop.AEQ[:,perm]
    with contextlib.redirect_stderr(_io.StringIO()):
        r=linprog(c=cost,A_eq=aeq,b_eq=np.zeros(N)-b,bounds=(0,None),method="highs",options=opts)
    x=np.zeros(len(ARCS)); x[perm]=r.x
    net=np.zeros(len(EDGES_UND))
    for ai,(_u,_v,ei,sg) in enumerate(ARCS): net[ei]+=sg*x[ai]
    return tuple(np.sign(np.where(np.abs(net)>1e-11,net,0.0)).astype(int))
import collections
vals=collections.Counter()
per={}
for seed in list(range(0,31)):
    rng=np.random.default_rng(seed)
    perms=[np.arange(len(ARCS))]+[rng.permutation(len(ARCS)) for _ in range(4)]
    ref=orient(None,perms[0]); fset=set()
    for pi,p in enumerate(perms[1:],1):
        got=orient(None,p)
        for slot,(a,c2) in enumerate(zip(ref,got)):
            if a!=c2: fset.add((pi,slot))
    per[seed]=len(fset); vals[len(fset)]+=1
print("counts by seed:",per)
print("distinct values observed over seeds 0-30:",sorted(vals),"frequencies",dict(vals))
