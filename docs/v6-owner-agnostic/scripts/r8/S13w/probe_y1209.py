import numpy as np, collections
exec(open("p3_perm.py").read().split('print()\nprint("=" * 92); print("A.')[0])
DEFAULT = {}
d0, o0, _ = solve_perm(B_GOOD["copper"], IDENT, DEFAULT)
counts = []
for s in range(31):
    rng = np.random.default_rng(s)
    tot = 0
    for _ in range(4):
        p = list(rng.permutation(A))
        d, o, _ = solve_perm(B_GOOD["copper"], p, DEFAULT)
        tot += flips(d0, d)
    counts.append(tot)
print("seed 0..30 copper sum-over-4-perms flip counts:", counts)
print("min", min(counts), "max", max(counts))
c = collections.Counter(counts)
print("mode:", c.most_common(5))
