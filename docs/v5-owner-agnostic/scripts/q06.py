# -*- coding: utf-8 -*-
"""v5 batch 6 — three figures the regeneration batch missed, found by re-reading the saved run
outputs against the spec text (`v5measure.out` and `phiw3.v5.out`)."""
import patch_lib
E = []

E.append(dict(id="F56", clears="2.9's coal row still carried v4.0's flip count", section="2.9",
old="""Measured: repricing the 45 owned latent-coal provinces flips 10 of 159 `Φ_w` edges |""",
new="""Measured: repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges (§1.5) |"""))

E.append(dict(id="F57", clears="3.15's gravity-kernel end counts at gamma = 0.9", section="3.15",
old="""demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
five- and six-mass fields both give four ends — with **61%** vanilla-arrow agreement at its best
(γ = 0.97, 97 of 159 arrows).""",
new="""demanders hits any chosen end count exactly for γ ≤ 0.7 and any count up to six — at γ = 0.9 the
four-, five- and six-mass fields all collapse to three ends — with **61%** vanilla-arrow agreement
at its best (γ = 0.90–0.95, 97 of 159 arrows; γ = 0.97 gives 93, and every larger γ is worse).
*v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give
four ends at γ = 0.9; on the corrected wealth field neither holds.*"""))

patch_lib.apply(E)
