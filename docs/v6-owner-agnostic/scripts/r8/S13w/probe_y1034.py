import numpy as np
exec(open("p3_perm.py").read().split('print()\nprint("=" * 92); print("A.')[0])
DEFAULT = {}
for g in ("copper","paper") + tuple(g for g in GL if g not in ("copper","paper")):
    d_def, o_def, _ = solve_perm(B_GOOD[g], IDENT, DEFAULT)
    d_pin, o_pin, _ = solve_perm(B_GOOD[g], IDENT, LP_OPTS)
    same = d_def == d_pin
    if not same or g in ("copper","paper"):
        print(g, "identity-order DEFAULT == LP_OPTS:", same, "obj diff", abs(o_def-o_pin))
print("aggregate:")
d_def, o_def, _ = solve_perm(B_AGG, IDENT, DEFAULT)
d_pin, o_pin, _ = solve_perm(B_AGG, IDENT, LP_OPTS)
print(" identity-order DEFAULT == LP_OPTS:", d_def==d_pin, "obj diff", abs(o_def-o_pin))
