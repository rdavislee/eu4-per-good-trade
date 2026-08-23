import os,sys,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N, NIDX, ORDER, GOODS, PRICES, ROWS, build_sc
from flowop import TIE_EPS, TIE_EPS2, mincost_flow, ARCS, AEQ
from scipy.optimize import linprog
W=np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN=np.array([NIDX[r["node"]] for r in ROWS])
NODEW=np.zeros(N); np.add.at(NODEW,PN,W)
ALPHA=lambda g: max(0.2,min(3.0,(PRICES[g]/2.0)**1.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
gi=GOODS.index("paper"); b=S[gi]-C[gi]
WMM=(NODEW-NODEW.min())/(NODEW.max()-NODEW.min())
a1=np.array([WMM[u] for (u,_v,_e,_s) in ARCS]); a2=np.array([WMM[v] for (_u,v,_e,_s) in ARCS])
cost=1.0+TIE_EPS*(a1+a2)/2.0+TIE_EPS2*np.modf(np.minimum(a1,a2)*np.maximum(a1,a2)*7919.0)[0]
fl,du,res=mincost_flow(b+0,np.zeros(N),cost=cost)
obj=float(cost@fl)
rc=np.array([cost[i]-(du[ARCS[i][1]]-du[ARCS[i][0]]) for i in range(len(ARCS))])
off=np.where(fl<=1e-12)[0]
zer=[i for i in off if abs(rc[i])<=1e-14]
print("paper: optimal objective %.15g ; zero-rc off-support arcs: %s"%(obj,[(ORDER[ARCS[i][0]],ORDER[ARCS[i][1]]) for i in zer]))
LPO={"dual_feasibility_tolerance":1e-10,"primal_feasibility_tolerance":1e-10}
for i in zer:
    lb=np.zeros(len(ARCS)); ub=np.full(len(ARCS),None,dtype=object)
    for eps in (1e-9,1e-6,1e-4):
        bounds=[(0,None)]*len(ARCS); bounds[i]=(eps,None)
        r2=linprog(cost,A_eq=AEQ,b_eq=b,bounds=bounds,method="highs",options=LPO)
        print("   force arc %s->%s >= %g : success=%s obj=%.15g  delta=%.3g"%(ORDER[ARCS[i][0]],ORDER[ARCS[i][1]],eps,r2.success,r2.fun if r2.success else float('nan'),(r2.fun-obj) if r2.success else float('nan')))
