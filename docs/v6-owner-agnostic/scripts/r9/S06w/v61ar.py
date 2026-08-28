# -*- coding: utf-8 -*-
"""v6.1 batch AR -- three places still say the per-good optima are degenerate, or that the LP must
'pivot identically'. Neither is the position any more: the optima are unique with margin, and what
matters is reaching the same optimum, not taking the same path to it."""
import patch_lib
E = []

E.append(dict(id="AR1", clears="AR1: 3.6's degeneracy premise, after the tolerance was pinned",
section="3.6",
old="""corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
narrows where that bites: on the aggregate graph it leaves the optimum unique, so the result no longer
rests on the solver's tie-selection; on the per-good graphs, whose `b` a wealth-weighted cost need not
separate, it still does (§2.4 item 1), and that is the premise §3.13 tracks for multiplayer.""",
new="""corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
removes where that bites in practice: with both cost terms and the solver's optimality tolerance
pinned, the optimum is unique on the aggregate and on all 29 per-good solves, with a margin of 3.8e-8
at worst against double-precision noise of 2e-16 — so the result no longer rests on the solver's
tie-selection at all. The discontinuity remains a property of the *program*: an input that made two
routings exactly equal in cost would still have no unique answer. Nothing on this field does."""))

E.append(dict(id="AR2", clears="AR2: 3.6's forward reference to the MP question", section="3.6",
old="""replaces the ε-magnitude question in §3.13 is the cross-machine question: the LP must pivot
identically on identical input for multiplayer (§2.1).""",
new="""replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.2 narrows it: the LP
does not need to *pivot* identically, only to reach the same optimum, which the tie-break's margin
makes robust to a few units in the last place. What is left is build discipline (§2.2)."""))

E.append(dict(id="AR3", clears="AR3: 3.13's open question, restated to what is open", section="3.13",
old="""- LP determinism across machines: the min-cost-flow solve must pivot identically on identical
  input (replaces v1's ε-magnitude question; see §2.1 and §3.6).""",
new="""- **Multiplayer build discipline.** Not LP pivot determinism, which §2.2 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.2 and §3.6."""))

patch_lib.apply(E)
