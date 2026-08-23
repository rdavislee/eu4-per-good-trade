import os,sys,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N,ORDER,NIDX,ROWS
from flowop import mincost_flow, ARCS, TIE_EPS, TIE_EPS2
W=np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN=np.array([NIDX[r["node"]] for r in ROWS])
NODEW=np.zeros(N); np.add.at(NODEW,PN,W)
A=2.0; wp=W**A; cw=np.zeros(N); np.add.at(cw,PN,wp); cw=cw/wp.sum()
bw=np.full(N,1.0/N)-cw
WMM=(NODEW-NODEW.min())/(NODEW.max()-NODEW.min())
a1=np.array([WMM[u] for (u,_v,_e,_s) in ARCS]); a2=np.array([WMM[v] for (_u,v,_e,_s) in ARCS])
cost=1.0+TIE_EPS*(a1+a2)/2.0+TIE_EPS2*np.modf(np.minimum(a1,a2)*np.maximum(a1,a2)*7919.0)[0]
fl,du,_=mincost_flow(bw+0,np.zeros(N),cost=cost)
fin=np.zeros(N); fout=np.zeros(N)
for i,(u,v,e,s) in enumerate(ARCS):
    fout[u]+=fl[i]; fin[v]+=fl[i]
res=np.abs(fin-fout+bw)
print("identity max residual %.3g ; holds on %d of %d"%(res.max(),int((res<1e-12).sum()),N))
print("net demanders (-b_w>0):",int((-bw>0).sum()))
import measure6 as M
r=M.ph(); D=set(r["directed"])
outdeg=np.zeros(N)
for u,v in D: outdeg[u]+=1
z=[i for i in range(N) if outdeg[i]>0 and fout[i]<=1e-12]
print("nodes with out-degree>0 but zero outgoing flow:",len(z))
for n in ("english_channel","mexico","gulf_of_siam","sevilla","genua","hangzhou"):
    i=NIDX[n]
    print("  %-16s b_w=%+.5f  flow_in=%.4f flow_out=%.4f outdeg=%d  in-zero-set=%s"%(n,bw[i],fin[i],fout[i],outdeg[i],i in z))
