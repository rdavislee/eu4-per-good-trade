# -*- coding: utf-8 -*-
"""v6.1 batch Q -- 2.2's multiplayer exposure. A unique optimum removes vertex-selection as a desync
path on the aggregate graph; it does not remove float reproducibility, and it does not help the
per-good graphs, whose optima are still degenerate."""
import patch_lib
E = [dict(id="Q1", clears="Q1: the MP exposure, narrowed by the tie-break", section="2.2",
old="""exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
pivot identically given identical input (fixed arc ordering, one solver build, no threading), and
the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.""",
new="""exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
return the same optimum given identical input (fixed arc ordering, one solver build, no threading),
and the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.

§2.3's tie-break narrows one part of this and leaves the rest. On the aggregate graph the optimum is
unique, so *which vertex of a degenerate optimal face the solver lands on* is no longer a desync path
— that was the largest single exposure and it is closed. What remains is ordinary float
reproducibility: the cost vector itself is computed from wealth, so the same accumulation-order
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the value weights and survival table
are downstream of it.""")]
patch_lib.apply(E)
