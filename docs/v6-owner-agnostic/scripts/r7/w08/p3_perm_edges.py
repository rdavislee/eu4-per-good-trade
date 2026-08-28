import sys
sys.path.insert(0, ".")
from p3_perm import B_GOOD, IDENT, solve_perm, A
import numpy as np

for name in ("copper", "paper"):
    b = B_GOOD[name]
    d0, o0, _ = solve_perm(b, IDENT, {})
    rng = np.random.default_rng(20260821)
    all_edges = set()
    per_perm_edges = []
    for i in range(6):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(b, p, {})
        diff = set(ei for ei in set(d0) | set(d) if d0.get(ei) != d.get(ei))
        per_perm_edges.append(diff)
        all_edges |= diff
    print(name, "distinct edge-slots touched:", len(all_edges), all_edges)
    print(name, "per-permutation diff sets:", [len(x) for x in per_perm_edges])
    print(name, "nonzero permutations:", sum(1 for x in per_perm_edges if x))
