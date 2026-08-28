from solver import GOODS, PRICES, build_sc, N
ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g]/2.0)**1.0))
S, C, V, LIVE, GP, WORLD = build_sc(ALPHA, eps=0.0)
gi = GOODS.index('spices')
print('spices producers:', int((S[gi]>0).sum()), 'of', N)
gi2 = GOODS.index('cloves')
print('cloves producers:', int((S[gi2]>0).sum()), 'of', N)
allc = True
for g2i,g in enumerate(GOODS):
    if not LIVE[g2i]: continue
    if int((C[g2i]>0).sum()) != N:
        allc = False
        print('not all-N demand for', g, int((C[g2i]>0).sum()))
print('every node has demand for every live good:', allc)
