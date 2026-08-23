# -*- coding: utf-8 -*-
"""v6 batch 5 — repair the edit boundary in 3.15 and strip the gravity kernel's figures (R3)."""
import patch_lib
E = []

E.append(dict(id="R5-fix", clears="corrective: 'The the' at the 3.15 edit boundary", section="3.15",
old="""**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)* The
the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and still acyclic
for free — but its ends are scheduling artifacts rather than places and its end count does not
concentrate with demand (§3.9). *No figures are maintained for it.* v2.0 and v2.1 quoted a
self-coherence ceiling that predates the
deterministic sweep of §3.6 and was never regenerated after it.""",
new="""**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)* It is
the most self-coherent aggregate measured — better than `Φ_w` on that one axis, and acyclic for
free — but its ends are scheduling artifacts rather than places, and its end count does not
concentrate as demand concentrates (§3.9). *No figures are maintained for it:* it is not installed,
its numbers moved with every change to the wealth field, and the design argument does not rest on
them. The self-coherence ceiling v2.0 and v2.1 quoted predates the deterministic sweep of §3.6 and
was never regenerated after it."""))

E.append(dict(id="R5-grav", clears="R3/X190/X191: the gravity kernel keeps its argument, loses its figures",
section="3.15",
old="""demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
four-, five- and six-mass fields all collapse to three ends — with **61%** vanilla-arrow agreement
at its best (γ = 0.90–0.95, 97 of 159 arrows; γ = 0.97 gives 93, and every larger γ is worse).
*v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give
four ends at γ = 0.9; on the corrected wealth field neither holds.* (v2.0 and v2.1 both quoted 69% = 110 of 159, which is not reached at
any γ; the count-follows-seeds behaviour reproduced, that figure did not.) Rejected: it pins
the end count by fiat (a world conquest could never merge the world into one basin), needs a
second operator with its own reach knob γ, and a pure `wealth^α` edge comparison without a reach
term can never concentrate ends at all — a local wealth maximum survives every positive α
(measured: ≥10 ends at α up to 16). The emergent-count wealth good replaced it.""",
new="""demanders reproduces whatever end count it is seeded with while γ is small enough, and loses that
property as γ approaches 1. *No figures are maintained for it* — every agreement percentage this
entry carried in v2.0 through v5.0 was measured on a superseded wealth field and each audit spent
its effort recounting them. Rejected on three grounds, none of which is numeric: it pins the end
count by fiat, so a world conquest could never merge the world into one basin; it needs a second
operator with its own reach knob γ; and a pure `wealth^α` edge comparison with no reach term does
not concentrate ends at all, because a local wealth maximum survives every positive α. The
emergent-count wealth good replaced it."""))

patch_lib.apply(E)
