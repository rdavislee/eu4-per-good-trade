# -*- coding: utf-8 -*-
"""v6.1 batch AU -- Y1030: the tolerance default was asserted with no source. Cite scipy's own
documentation and add the bisection, which confirms the mechanism rather than inferring it."""
import patch_lib
E = [dict(id="AU1", clears="AU1: source the solver tolerance claim and confirm its mechanism",
section="2.3",
old="""**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
stops when reduced costs are within its dual feasibility tolerance of zero, and that default is
**1e-7** — while the margin by which the tie-break makes the optimum unique runs as low as **3.8e-8**
on some per-good solves. The margin sits *inside* the default tolerance, so the solver was free to
stop either side of the true optimum. Measured: over six permutations of the LP's column order,
`copper` and `paper` returned orientations differing on 12 and 8 edge-slots, with objectives differing
by **7.7e-10 relative** — six orders above float noise, so those were unequal-quality answers rather
than tied optima. Setting both feasibility tolerances to **1e-10** (HiGHS's floor for them) takes the
flips to **0** and the objective spread to **1.1e-15**. `flowop.LP_OPTS` carries it, and no figure in
this document moved when it went in — the shipped column order was already reaching the true optimum;
what changed is that every other order now does too.""",
new="""**The solver's optimality tolerance is a correctness requirement, not a performance knob.** HiGHS
stops when reduced costs are within its dual feasibility tolerance of zero, and **`scipy.optimize.linprog`'s
`method="highs"` options document that default as `1e-07`** for both the dual and primal tolerances
(scipy 1.18.0) — while the margin by which the tie-break makes the optimum unique runs as low as
**3.8e-8** on some per-good solves. The margin sits *inside* the default tolerance, so the solver was
free to stop either side of the true optimum. Measured: over six permutations of the LP's column order,
`copper` and `paper` returned orientations differing on 12 and 8 edge-slots, with objectives differing
by **7.7e-10 relative** — six orders above float noise, so those were unequal-quality answers rather
than tied optima.

*The mechanism is confirmed rather than inferred, by bisecting the tolerance against `copper`.* Leaving
it unset and setting it to 1e-7 give the same 8 flips over four permutations, which is what pins the
effective default independently of the documentation; **1e-8 already gives 0**, and 1e-8 is the first
value below `copper`'s 3.765e-8 margin. So the flips appear exactly when the tolerance exceeds the
margin, which is the claim. `flowop.LP_OPTS` ships **1e-10** — HiGHS's floor for these options, taken
for headroom rather than necessity — and the objective spread there is 1.1e-15. No figure in this
document moved when it went in: the shipped column order was already reaching the true optimum, and
what changed is that every other order now does too.""")]
patch_lib.apply(E)
