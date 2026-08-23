import numpy as np
exec(open("p3_perm.py").read().split('print()\nprint("=" * 92); print("A.')[0])
DEFAULT = {}
d0, o0, _ = solve_perm(B_GOOD["copper"], IDENT, DEFAULT)
# reproduce round6.py's exact seed-4 permutation draws
_rng = np.random.default_rng(4)
perms = [_rng.permutation(A) for _ in range(4)]
per_perm_flips = []
union_edges = set()
sum_flips = 0
for p in perms:
    d, o, _ = solve_perm(B_GOOD["copper"], list(p), DEFAULT)
    fl = [ei for ei in set(d0)|set(d) if d0.get(ei)!=d.get(ei)]
    per_perm_flips.append(len(fl))
    union_edges |= set(fl)
    sum_flips += len(fl)
print("per-permutation flip counts:", per_perm_flips)
print("sum with multiplicity (p3_bisect-style):", sum_flips)
print("union of distinct edges (round6.py-style):", len(union_edges), sorted(union_edges))
