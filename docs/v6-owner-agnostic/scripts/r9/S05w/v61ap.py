# -*- coding: utf-8 -*-
"""v6.1 batch AP -- 2.2's multiplayer opening contradicts what v6.1 added below it: it demands
bit-reproducibility and calls an identical build 'not sufficient', where the measurements say the
decision margins are 8-10 orders above float noise and a single instruction stream is nearly enough.
It also requires 'fixed arc ordering', which column permutation showed does not matter."""
import patch_lib
E = []

E.append(dict(id="AP1", clears="AP1: the MP opening, consistent with what follows it", section="2.2",
old="""**Multiplayer is unsupported by default.** An identical build is necessary and not sufficient: EU4 multiplayer is lockstep with checksums, and an in-process floating-point solve can produce different results on different hardware — differing SIMD dispatch or accumulation order in the linear algebra is enough to desync. Supporting MP requires the computation to be bit-reproducible across machines. For DRAIN the
exposure is narrower than v1's dense linear algebra but still real: the min-cost-flow solve must
return the same optimum given identical input (fixed arc ordering, one solver build, no threading),
and the sweep is deterministic given the LP's support and a fixed accumulation order — its comparisons
are of input-derived floats (`DEF`, `b`), not of solver residuals, which is the distinction that
matters against v1's dense algebra, but it is not integer arithmetic and v2 called it that. Its
cross-machine reproducibility reduces to the LP's.""",
new="""**Multiplayer is not supported yet, and the reason is narrower than it was.** EU4 multiplayer is
lockstep with checksums, so every client must reach the same answer. The classical worry is that an
in-process floating-point solve gives different results on different hardware — differing SIMD
dispatch, accumulation order, or library build. That worry is real in general, and v1's dense linear
algebra was badly exposed to it: comparisons of solved potentials that were mathematically equal and
differed only in their residual (§3.6).

DRAIN's exposure is different in kind. Its comparisons are of input-derived quantities (`DEF`, `b`,
arc costs), not of solver residuals — and, more importantly, every decision it makes now has a margin
far above float noise. What that means in practice is set out below; the short form is that the
question is no longer whether the arithmetic agrees to the last bit, but whether the build is
disciplined enough that the same instruction stream runs everywhere."""))

E.append(dict(id="AP2", clears="AP2: point 3 refers to itself as one of 'the three above'",
section="2.2",
old="""3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the three points above missed.""",
new="""3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the first two points missed."""))

patch_lib.apply(E)
