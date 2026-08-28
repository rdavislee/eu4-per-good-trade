import os,sys,re,io,numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from solver import (ROWS,PROV,PRICES,GOODS_PRODUCED_FACTOR,TAX_COEFF,ON_STARTUP_DEVASTATION,
                    N,ORDER,NIDX,EU4)
import drain
A_PHI=2.0
PN=np.array([NIDX[r["node"]] for r in ROWS])
W=np.array([r["tax"]+r["prod_income"] for r in ROWS])
def ph(a,w):
    t=(w/w.max())**a
    nn=np.zeros(N); np.add.at(nn,PN,t)
    return drain.run_drain(np.full(N,1.0/N)-nn/nn.sum())
BD=set(ph(A_PHI,W)["directed"])
_h=os.path.join(EU4,"history","provinces"); coal=set()
for fn in os.listdir(_h):
    m=re.match(r"^\s*(\d+)",fn)
    if not m: continue
    tx=io.open(os.path.join(_h,fn),encoding="latin-1",errors="replace").read()
    if re.search(r"latent_trade_goods[^=]*=[^{]*\{[^}]*coal",tx): coal.add(int(m.group(1)))
print("latent-coal:",len(coal),"| owned&counted:",sum(1 for r in ROWS if r["pid"] in coal))
print("4237 base_production:",PROV[4237]["base_production"],"base_tax:",PROV[4237]["base_tax"],
      "dev:",ON_STARTUP_DEVASTATION.get(4237))
def variant(keep_dev):
    W2=W.copy()
    for i,r in enumerate(ROWS):
        if r["pid"] in coal:
            gp=GOODS_PRODUCED_FACTOR*PROV[r["pid"]]["base_production"]
            if keep_dev and r["pid"] in ON_STARTUP_DEVASTATION:
                gp*=1.0+(-2.0*ON_STARTUP_DEVASTATION[r["pid"]]/100.0)
            W2[i]=TAX_COEFF*PROV[r["pid"]]["base_tax"]+max(0.0,gp)*PRICES["coal"]
    return W2
for keep in (True,False):
    W2=variant(keep)
    d=set(ph(A_PHI,W2)["directed"])
    print("keep_devastation=%s  wealth delta %.2f  flips vs base %d  edges %d"
          %(keep, W2.sum()-W.sum(), len(BD^d)//2, len(d)//2))
A=variant(True); B=variant(False)
print("mixed-minus-held wealth difference: %.2f"%(B.sum()-A.sum()))
dA=set(ph(A_PHI,A)["directed"]); dB=set(ph(A_PHI,B)["directed"])
print("edges differing between the two counterfactuals:",len(dA^dB)//2)
