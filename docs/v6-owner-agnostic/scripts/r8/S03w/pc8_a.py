# -*- coding: utf-8 -*-
"""preconfirm round 8: A1, A2, B3, B4, C5 re-derivation"""
import os, sys, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from solver import (N, ORDER, NIDX, UND, EDGES_UND, GOODS, PRICES, ROWS, build_sc)
from drain import run_drain, sinks_of, has_cycle

ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
W = np.array([r["tax"] + r["prod_income"] for r in ROWS])
pn = np.array([NIDX[r["node"]] for r in ROWS])
NW = np.zeros(N); np.add.at(NW, pn, W)

print("== A1: alpha / prices ==")
for g in ("cloves","coal","sugar","coffee","grain"):
    print("  %-8s price=%s alpha=%.4f exponent=%.4f" % (g, PRICES.get(g), ALPHA(g), ALPHA(g)-1))
S0,C0,V,LIVE,GP,world = build_sc(ALPHA, eps=0.0)
livegoods = [GOODS[i] for i in range(len(GOODS)) if LIVE[i]]
print("  live goods count:", len(livegoods))
print("  cloves live?", "cloves" in livegoods, " coal live?", "coal" in livegoods)
gi = GOODS.index("cloves")
prod_nodes = [ORDER[j] for j in range(N) if GP[gi][j] > 0]
print("  cloves producing nodes:", prod_nodes)
for (a,b) in ((77,19),(68,33)):
    print("  (%d/%d)^1 = %.4f   ^0.5 = %.4f   ^2 = %.4f" % (a,b,a/b,(a/b)**0.5,(a/b)**2))

print()
print("== A2 / B3: aggregate Phi_w ==")
def cv(a, w=None):
    w = W if w is None else w
    t = (w/w.max())**a; n = np.zeros(N); np.add.at(n, pn, t); return n/n.sum()
def ph(a): return run_drain(np.full(N,1.0/N) - cv(a))
for a in (1,1.4,1.5,1.6,1.63,2,3,4,8):
    r = ph(a); sk,od = sinks_of(r["directed"])
    print("  alpha_Phi=%-5s sinks=%s" % (a, sorted(ORDER[i] for i in sk)))

base = ph(2.0)
bw = np.full(N,1.0/N) - cv(2.0)
net = base["net"]; flow_arc = base["flow_arc"]
fin = np.zeros(N); fout = np.zeros(N)
for ei,(u,v) in flow_arc.items():
    m = abs(net[ei]); fout[u]+=m; fin[v]+=m
od = collections.Counter(u for u,_ in base["directed"])
ind = collections.Counter(v for _,v in base["directed"])
wr = {ORDER[i]: k+1 for k,i in enumerate(np.argsort(-NW))}
for nm in ("english_channel","mexico","gulf_of_siam","sevilla","genua","hangzhou"):
    i = NIDX[nm]
    print("  %-16s wealth=%.1f rank=%d  flow_in=%.4f flow_out=%.4f  outdeg=%d indeg=%d  b_w=%.6f" %
          (nm, NW[i], wr[nm], fin[i], fout[i], od[i], ind[i], bw[i]))
resid = max(abs((fin[i]-fout[i]) - (-bw[i])) for i in range(N))
print("  max residual |flow_in-flow_out+b_w| =", resid)
nd = [i for i in range(N) if bw[i] < 0]
print("  net demanders (b_w<0):", len(nd))
zeroout = [ORDER[i] for i in range(N) if od[i] > 0 and fout[i] <= 1e-11]
print("  nodes with outdeg>0 and zero outgoing flow:", len(zeroout))
print("   ->", sorted(zeroout))
print("  mexico in that set:", "mexico" in zeroout, " gulf_of_siam:", "gulf_of_siam" in zeroout)

print()
print("== C5: per-node out-arc coverage over 29 live goods ==")
cnt = np.zeros(N, dtype=int); sinkfor = np.zeros(N, dtype=int)
for k,g in enumerate(livegoods):
    j = GOODS.index(g)
    r = run_drain(S0[j]-C0[j])
    o = collections.Counter(u for u,_ in r["directed"])
    for i in range(N):
        if o[i] > 0: cnt[i]+=1
        else: sinkfor[i]+=1
print("  goods=%d ; min goods-with-out-arc over nodes = %d ; max = %d" % (len(livegoods), cnt.min(), cnt.max()))
print("  nodes with out-degree 0 for every good:", int((cnt==0).sum()))
print("  nodes that are a sink for >=1 good:", int((sinkfor>0).sum()))
print("  argmin node:", ORDER[int(np.argmin(cnt))])
