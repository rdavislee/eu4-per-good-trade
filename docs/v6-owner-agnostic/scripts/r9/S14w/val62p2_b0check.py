import numpy as np
from solver import ROWS, PRICES, GOODS, N, ORDER, NIDX, build_sc
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S,C,V,live,gp,world = build_sc(ALPHA, eps=0.0)
from collections import Counter
cnt = Counter()
per_good_zero = {}
for gi,g in enumerate(GOODS):
    if not live[gi]: continue
    b = S[gi]-C[gi]
    zeros = [ORDER[i] for i in range(N) if b[i]==0.0]
    per_good_zero[g] = zeros
    for n in zeros: cnt[n]+=1
print("nodes with b==0, by count of goods:", dict(cnt))
print("num live goods:", sum(live))
# is cape_of_good_hope zero for ALL live goods?
capezero = sum(1 for g in per_good_zero if "cape_of_good_hope" in per_good_zero[g])
print("cape_of_good_hope zero for", capezero, "of", sum(live), "live goods")
# any other node ever zero?
others = {n:c for n,c in cnt.items() if n!="cape_of_good_hope"}
print("other nodes ever zero:", others)
