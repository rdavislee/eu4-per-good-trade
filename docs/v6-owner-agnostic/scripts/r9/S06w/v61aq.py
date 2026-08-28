# -*- coding: utf-8 -*-
"""v6.1 batch AQ -- 2.8 gains a row for the solver tolerance. It is a correctness requirement that can
regress silently on a solver upgrade, and nothing in the table currently checks it. The determinism row
is also strengthened to what was actually measured."""
import patch_lib
E = []

E.append(dict(id="AQ1", clears="AQ1: the determinism row, at its measured scope", section="2.8",
old="""| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure) |""",
new="""| Determinism | Re-running a tick reproduces the orientation bit-for-bit; promotions and fallbacks are scheduler-invariant (monotone closure). Measured on the reference implementation: one fingerprint over `Φ_w` and all 29 per-good graphs — including sinks, sources, promotions and fallbacks — was identical across repeated runs, separate processes, and five `PYTHONHASHSEED` values including `random`. The solve carries no randomness, so there is no seed to pin |
| Solver optimality tolerance | Assert the LP is configured tighter than the tie-break margin — `flowop.LP_OPTS` sets both feasibility tolerances to 1e-10 against a worst-case margin of 3.8e-8 (§2.3). **This can regress silently on a solver upgrade:** at HiGHS's 1e-7 default the margin sits inside the tolerance and the solver may return a suboptimal vertex, which is what made two goods order-dependent before it was pinned. Assert the option is set and that the returned objective's reduced costs clear the tolerance |"""))

patch_lib.apply(E)
