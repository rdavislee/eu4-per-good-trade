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
hits=[]
for seed in range(0,40):
    for extra in (5,6):
        rng=np.random.default_rng(seed)
        perms=[np.arange(len(ARCS))]+[rng.permutation(len(ARCS)) for _ in range(extra)]
        res={}
        for g in ("copper","paper"):
            b=S[GOODS.index(g)]-C[GOODS.index(g)]
            ref=orient(b,perms[0]); f=0; sl=set(); pw=0
            for p in perms[1:]:
                got=orient(b,p); d=[k for k,(a,c2) in enumerate(zip(ref,got)) if a!=c2]
                if d: pw+=1
                f+=len(d); sl.update(d)
            res[g]=(f,len(sl),pw)
        if res["copper"][0]==4 and res["paper"][0]==8:
            hits.append((seed,extra,res))
print("seed/extra combos giving copper=4 and paper=8 flips:",hits[:5],"total",len(hits))
