import os,sys,io as _io,contextlib
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from scipy.optimize import linprog
import flowop
from flowop import ARCS
from solver import N,GOODS,PRICES,EDGES_UND,build_sc
ALPHA=lambda g: max(0.2,min(3.0,(PRICES[g]/2.0)**1.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
def orient(b,perm,tol=None):
    opts=None if tol is None else {"dual_feasibility_tolerance":tol,"primal_feasibility_tolerance":tol}
    cost=flowop.TIE_COST[perm]; aeq=flowop.AEQ[:,perm]
    with contextlib.redirect_stderr(_io.StringIO()):
        r=linprog(c=cost,A_eq=aeq,b_eq=np.zeros(N)-b,bounds=(0,None),method="highs",options=opts)
    x=np.zeros(len(ARCS)); x[perm]=r.x
    net=np.zeros(len(EDGES_UND))
    for ai,(_u,_v,ei,sg) in enumerate(ARCS): net[ei]+=sg*x[ai]
    return tuple(np.sign(np.where(np.abs(net)>1e-11,net,0.0)).astype(int))
ident=np.arange(len(ARCS))
for seed in (4,1,2024,606,7,0,42):
    rng=np.random.default_rng(seed)
    perms=[rng.permutation(len(ARCS)) for _ in range(6)]
    out=[]
    for g in ("copper","paper"):
        b=S[GOODS.index(g)]-C[GOODS.index(g)]
        ref=orient(b,ident,1e-10)     # the true optimum
        f=0; sl=set(); pw=0
        for p in perms:
            got=orient(b,p)           # default tolerance
            d=[k for k,(a,c2) in enumerate(zip(ref,got)) if a!=c2]
            if d: pw+=1
            f+=len(d); sl.update(d)
        out.append("%s flips=%d slots=%d perms=%d/6"%(g,f,len(sl),pw))
    print("seed %-5s ref=true-optimum : %s | %s"%(seed,out[0],out[1]))
