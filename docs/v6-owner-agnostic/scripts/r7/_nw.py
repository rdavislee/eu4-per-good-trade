import os,sys,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE); os.chdir(HERE)
from solver import N,ORDER,NIDX,ROWS
W=np.array([r["tax"]+r["prod_income"] for r in ROWS]); PN=np.array([NIDX[r["node"]] for r in ROWS])
NW=np.zeros(N); np.add.at(NW,PN,W)
rank=sorted(range(N),key=lambda i:-NW[i])
for k,i in enumerate(rank[:14],1): print("%2d %-20s %8.1f"%(k,ORDER[i],NW[i]))
print("...")
for n in ("hangzhou","beijing","genua","sevilla","mexico","gulf_of_siam","english_channel"):
    i=NIDX[n]; print("%-18s %8.1f rank %d"%(n,NW[i],rank.index(i)+1))
nz=[i for i in range(N) if NW[i]>0]
print("nodes with counted provinces:",len(nz))
r2=sorted(nz,key=lambda i:-NW[i])
for n in ("hangzhou","beijing"): print("  %s rank among %d nonzero: %d"%(n,len(nz),r2.index(NIDX[n])+1))
