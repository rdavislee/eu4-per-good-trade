# B2 recheck: distinct edge-slots differing across the 6 default-tolerance permutations
import io, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
src = io.open("p3_perm.py", encoding="utf-8").read()
exec(src.split("# --------------------------------------------------------- validation --------")[0])
for gname in ("copper", "paper"):
    b = B_GOOD[gname]
    rng = np.random.default_rng(20260821)
    d0, o0, _ = solve_perm(b, IDENT, {})
    union = set(); per = []
    for _ in range(6):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(b, p, {})
        diff = {ei for ei in set(d0) | set(d) if d0.get(ei) != d.get(ei)}
        per.append(sorted(diff)); union |= diff
    print(gname, "per-perm differing slots:", per)
    print(gname, "sum of flips:", sum(len(x) for x in per), "union of distinct slots:", len(union), sorted(union))
