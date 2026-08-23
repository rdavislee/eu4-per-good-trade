# -*- coding: utf-8 -*-
"""v6.1 batch AJ -- 2.2's multiplayer position. It was written when vertex selection was
machine-dependent. With the optimum unique and the tolerance pinned, the exposure is much narrower and
the remaining work is verification rather than design."""
import patch_lib
E = [dict(id="AJ1", clears="AJ1: the multiplayer position, restated against what is now measured",
section="2.2",
old="""§2.3's tie-break narrows one part of this and leaves the rest. On the aggregate graph the optimum is
unique, so *which vertex of a degenerate optimal face the solver lands on* is no longer a desync path
— that was the largest single exposure and it is closed. What remains is ordinary float
reproducibility: the cost vector itself is computed from wealth, so the same accumulation-order
question applies to it. And the per-good graphs are untouched — their optima are still degenerate
(§2.4 item 1), so vertex selection remains an exposure there, and the whole propagated per-good
economy is downstream of it: node values, the ledger and the economy tab all read numbers that a
different optimal vertex would change. The value weights are not — `V_g` is a producer sum with no
direction in it.""",
new="""**§2.3's two changes move this from a design problem to a verification one.** The largest exposure was
*which vertex of a degenerate optimal face the solver lands on*, which is genuinely machine-dependent.
The tie-break makes the optimum unique, and pinning the solver's optimality tolerance makes the solver
actually reach it. What is measured on this field:

| | |
|---|---|
| randomness in the solve | none. Identical output fingerprint over repeated runs, separate processes, and five `PYTHONHASHSEED` values including `random` — so there is no seed to pin and no set-iteration order to depend on |
| margin by which the optimum is unique | **3.8e-8** worst per good, **7.5e-6** on the aggregate — 8 to 10 orders above double-precision unit roundoff |
| orientation under LP column permutation | **0** flips, aggregate and all 29 goods; objective spread 1.1e-15 |
| orientation under node relabelling | **0** of 180 aggregate, **0** of 290 per-good (§2.4 item 1) |
| free-versus-flow classification margin | the per-good `\|net\|` distribution is bimodal — 2,321 edge-goods at exactly 0 and 2,290 above 1e-6, with **nothing between** — so the absolute `1e-11` threshold sits in an empty band six orders wide and last-bit noise cannot reclassify an edge |

So a few units in the last place cannot change any decision this solver makes. **What remains is not
bit-reproducibility of a simplex, which would be a hard guarantee to earn, but three checks:**

1. **One binary per platform, and no cross-platform sessions.** A single compiled instruction stream
   gives identical IEEE-754 results on any x86-64 host. The `../v2-drain/` DLL precedent is already
   Windows- and Steam-only, so this matches practice rather than constraining it.
2. **No runtime CPU dispatch in the LP solver, and single-threaded.** This is the live risk: numeric
   libraries commonly select an AVX2 or SSE2 path at runtime *from the same binary*, and a threaded
   reduction has no fixed accumulation order. Both must be pinned in the solver build and verified,
   not assumed.
3. **§2.8's cross-implementation orientation check.** It compares the DLL against the reference
   implementation exactly, and it cannot run until the DLL exists. It is the test that would catch a
   divergence the three points above missed.

*What the engine itself does about the same problem is worth knowing and is only half-answered.* Every
trade number EU4 writes to a save is quantised to **1/1000** — 495 of 495 sampled values land exactly
on that grid across `total`, `val`, `p_pow`, `retention`, `collector_power` and `max_pow`. Quantisation
of that kind erases any divergence below half a grid step, which is the standard cheap defence. What
the files cannot settle is whether the rounding happens in the simulation or only in the serialiser;
that needs a memory read and is added to §2.7. It would not rescue this solver either way: the
orientation margins above are 3.8e-8 to 7.5e-6, three to five orders *below* a 1e-3 grid, so
quantising the model's own inputs to match would erase the tie-break rather than protect it.

**Until points 1–3 are done, ship single-player only.** The reason has changed, though, and the change
is the point: it is no longer "vertex selection is machine-dependent" but "the build discipline is
unverified and the DLL that would prove it does not exist yet.\"""")]
patch_lib.apply(E)
