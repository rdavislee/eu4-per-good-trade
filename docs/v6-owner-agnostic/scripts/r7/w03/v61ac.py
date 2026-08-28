# -*- coding: utf-8 -*-
"""v6.1 batch AC -- 2.3 claimed the normalisation is not load-bearing, on the argument that rescaling
w equals rescaling TIE_EPS. That holds for a linear term and not for frac(lo*hi*7919). Measured: the
aggregate is still normalisation-independent, 5 of 29 per-good graphs are not."""
import patch_lib
E = [dict(id="AC1", clears="AC1: the normalisation is load-bearing per good", section="2.3",
old="""relabelling by construction. The normalisation is not load-bearing: dividing by the maximum, the mean
or the world total gives the same orientation, because rescaling `w` is equivalent to rescaling
`TIE_EPS` and the answer is constant over about six orders of magnitude of it (§1.6).""",
new="""relabelling by construction.

**The normalisation is load-bearing per good, and this is a cost of the second-order term.** For the
first-order term alone it was not: rescaling `w` is exactly equivalent to rescaling `TIE_EPS`, and the
answer is constant over about six orders of magnitude of that (§1.6), so dividing by the maximum, the
mean or the world total gave the same orientation. `frac(lo·hi·7919)` is not linear in `w`, so that
argument no longer applies. Measured across the three normalisations: the aggregate `Φ_w` is unchanged
— **0 of 159 edges differ** — but **5 of the 29 per-good graphs do**. So the choice of normalisation is
a third arbitrary decision with an observable consequence, where before it was free. It is recorded
here rather than defended: min-max is what the implementation uses, and an implementer changing it
should expect a handful of per-good graphs to move.""")]
patch_lib.apply(E)
