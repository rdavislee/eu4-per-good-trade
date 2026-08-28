import os,sys,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N, NIDX, EDGES_UND, GOODS, PRICES, ROWS, build_sc
from flowop import TIE_EPS, TIE_EPS2, mincost_flow, ARCS
W=np.array([r["tax"]+r["prod_income"] for r in ROWS])
PN=np.array([NIDX[r["node"]] for r in ROWS])
NODEW=np.zeros(N); np.add.at(NODEW,PN,W)
ALPHA=lambda g: max(0.2,min(3.0,(PRICES[g]/2.0)**1.0))
S,C,V,LIVE,GP,WORLD=build_sc(ALPHA,eps=0.0)
GL=[(gi,g) for gi,g in enumerate(GOODS) if LIVE[gi]]
A_PHI=2.0
wv=NODEW**A_PHI; cw=wv/wv.sum()
# c_w must be sum over provinces of wealth^alpha, not node total^alpha
wp=W**A_PHI; cwp=np.zeros(N); np.add.at(cwp,PN,wp); cwp=cwp/wp.sum()
bw=np.full(N,1.0/N)-cwp
WMM=(NODEW-NODEW.min())/(NODEW.max()-NODEW.min())
a1=np.array([WMM[u] for (u,_v,_e,_s) in ARCS]); a2=np.array([WMM[v] for (_u,v,_e,_s) in ARCS])
unit=np.ones(len(ARCS)); first=1.0+TIE_EPS*(a1+a2)/2.0
ship=first+TIE_EPS2*np.modf(np.minimum(a1,a2)*np.maximum(a1,a2)*7919.0)[0]
def zeros_off(b,cost):
    fl,du,_=mincost_flow(b+0,np.zeros(N),cost=cost)
    rc=np.array([cost[i]-(du[ARCS[i][1]]-du[ARCS[i][0]]) for i in range(len(ARCS))])
    off=rc[fl<=1e-12]
    return int((np.abs(off)<=1e-14).sum())
print("aggregate b_w zero-reduced-cost off-support arcs:")
for name,c in (("unit",unit),("first-order",first),("shipped",ship)):
    print("   %-12s %d"%(name,zeros_off(bw,c)))
print("per-good:")
for name,c in (("unit",unit),("first-order",first),("shipped",ship)):
    per=[(g,zeros_off(S[gi]-C[gi],c)) for gi,g in GL]
    tot=sum(z for _,z in per); ng=sum(1 for _,z in per if z>0)
    print("   %-12s total %d arcs on %d of %d goods %s"%(name,tot,ng,len(GL),[g for g,z in per if z>0]))
