import numpy as np
exec(open("p3_perm.py").read().split('print()\nprint("=" * 92); print("A.')[0])
DEFAULT = {}
for g in ("copper","paper"):
    rng = np.random.default_rng(20260821)
    d0, o0, _ = solve_perm(B_GOOD[g], IDENT, DEFAULT)
    objs=[o0]
    all_edges=set()
    per_perm=[]
    for i in range(6):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(B_GOOD[g], p, DEFAULT)
        objs.append(o)
        flipped = [ei for ei in set(d0)|set(d) if d0.get(ei)!=d.get(ei)]
        per_perm.append(flipped)
        all_edges |= set(flipped)
    print(g, "per-perm flipped edges:", per_perm)
    print(g, "distinct edge-slots across all perms:", sorted(all_edges), "count", len(all_edges))
    print(g, "objective rel spread: %.3g" % ((max(objs)-min(objs))/abs(o0)))
