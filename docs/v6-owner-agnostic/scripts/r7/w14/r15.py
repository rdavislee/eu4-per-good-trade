# -*- coding: utf-8 -*-
"""v6 batch 15 — the contradictions the no-context extraction of v6.0 found. Every one of them sits
in a passage the first patch pass never opened, which is the defect class that survived v3, v4 and
v5: patch what you touch, and the untouched neighbour keeps the old claim."""
import patch_lib
E = []

E.append(dict(id="R15-23", clears="R2 + contradiction: 2.3's alpha paragraph", section="2.3",
old="""the aggregate-graph exponent `α_Φ = 1.5` (a constant like `P₀`; world-responsiveness flows through
wealth, never through this knob). **Its stated calibration is withdrawn.** v2.1 through v4.0 said
1.5 was "calibrated so the 1444 start yields the two-sink hangzhou/english_channel map"; on the
corrected wealth field of §1.3 it does not yield that map, and the α_Φ window that does yield it is
narrower than the uncertainty in its own edges under ±1% wealth noise (§1.6). 1.5 is retained because it sits inside the widest sink-count band
and nothing now selects a different value — not because it was derived. Any future change to it is
a design decision about how many ends the installed graph should have, and should be recorded as
one, and DRAIN's three knobs at their defaults""",
new="""the aggregate-graph exponent `α_Φ = 1.5` (a **stipulated** constant like `P₀`: superlinear, round,
and chosen rather than derived — world-responsiveness flows through wealth, never through this
knob). **Every derivation previously offered for it is withdrawn.** v2.1 through v4.0 said 1.5 was
calibrated so that 1444 yields a two-sink map; v5.0 said it sat in the widest sink-count band.
Neither is a reason: the first fits a constant to one date, and the second depended on where the α
scan was truncated (§1.6). Any future change to it is a design decision about how many ends the
installed graph should have, and should be recorded as one, and DRAIN's three knobs at their
defaults"""))

E.append(dict(id="R15-16count", clears="X065 + contradiction: the count is not set by alpha alone",
section="1.6",
old="""the sinks are wherever the wealth flow terminates. **Their count is set by `α_Φ`; only their""",
new="""the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5
the 1444 field gives two sinks and a modestly grown Europe gives three or one (§1.6's Europe table),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration"; v5.0 over-corrected to "the count is set by `α_Φ`". Both are wrong in
the same way — the count is a function of the field **and** the constant, and only their"""))

E.append(dict(id="R15-bandref", clears="the two dangling 'band table below' references", section="1.6",
old="""of it (the band table below), and v2.1 chose the value with a target count in view — a calibration
§2.3 now withdraws, since the ground on which 1.5 is *retained* is the band table and not that
target. What the world""",
new="""of it, and v2.1 chose the value with a target count in view — a calibration §2.3 withdraws without
replacing, since `α_Φ` is stipulated rather than derived. What the world"""))

E.append(dict(id="R15-39", clears="R3 + contradiction: 3.9's adoption note", section="3.9",
old="""  the wealth actually is, so they move when the wealth moves (§1.6's institution result). *v2.1
  through v4.0 justified the adoption by "two vanilla-like ends at 1444" — the reason it was
  accepted despite losing self-coherence. On the corrected wealth field there is one end, in China,
  matching none of vanilla's three, so that premise is withdrawn. The trade is now stated as what it
  is: 7.8 points of self-coherence given up for one operator and world-responsive ends, and the
  1444 count is whatever the field gives.*""",
new="""  the wealth actually is, so they move when the wealth moves (§1.6). *v2.1 through v4.0 justified the
  adoption by "two vanilla-like ends at 1444" — a resemblance to vanilla's authored map. That is not
  the argument, and it should not be revived even though the 1444 field again gives two ends: the
  count is a property of the field, not of the operator, and pinning the operator to it would be the
  calibration §2.3 withdrew. What the trade actually costs is self-coherence with the per-good
  graphs, which the superseded marking-order aggregate scores higher on; what it buys is one
  operator, one set of guarantees, and ends that sit where the wealth is.*"""))

E.append(dict(id="R15-ulp", clears="3.10 contradicted itself two paragraphs apart", section="3.10",
old="""agree to a worst relative disagreement of **0 to 3.7e-16** — at most one unit in the last place.""",
new="""agree to a worst relative disagreement of **0 to 3.7e-16** — one to three units in the last place."""))

E.append(dict(id="R15-dev", clears="ten vs eleven devastated provinces", section="1.3",
old="""**They are not all quiet at the 1444 start.** Ten provinces begin devastated — Bohemia at 50 and""",
new="""**They are not all quiet at the 1444 start.** Eleven counted provinces begin devastated — Bohemia at 50 and"""))

patch_lib.apply(E)
