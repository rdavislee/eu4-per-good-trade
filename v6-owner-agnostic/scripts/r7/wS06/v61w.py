# -*- coding: utf-8 -*-
"""v6.1 batch W -- 3.3's node-size illustration uses alpha = 1.5, which is a per-good alpha (sugar's
and coffee's, at base price 3.0) and not alpha_Phi. With alpha_Phi now 2.0 the bare '1.5' reads as a
stale figure. Name which alpha it is, and give the aggregate case too."""
import patch_lib
E = [dict(id="W1", clears="W1: disambiguate the per-good alpha from alpha_Phi", section="3.3",
old="""k-province node by `k^(α−1)` at fixed per-province wealth, so at α = 1.5 a 77-province node is
favoured over a 19-province one by `(77/19)^0.5 ≈ 2×` purely on slicing, and Nippon (68 land
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`.""",
new="""k-province node by `k^(α−1)` at fixed per-province wealth. Worked at **α(g) = 1.5** — a per-good α,
sugar's and coffee's at base price 3.0, not `α_Φ` — a 77-province node is
favoured over a 19-province one by `(77/19)^0.5 ≈ 2×` purely on slicing, and Nippon (68 land
provinces) over the Paris node (`champagne`, 33) by `(68/33)^0.5 ≈ 1.44×`. At the installed
`α_Φ = 2.0` the exponent is 1 and the same two comparisons give `77/19 ≈ 4.1×` and `68/33 ≈ 2.1×`,
so the slicing distortion the per-province form avoids is larger on the aggregate graph than on any
per-good one.""")]
patch_lib.apply(E)
