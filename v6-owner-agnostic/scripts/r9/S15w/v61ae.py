# -*- coding: utf-8 -*-
"""v6.1 batch AE -- 1.6's sensitivity note should record TIE_EPS2's range too, since an implementer
changing it needs to know how wide the usable window is."""
import patch_lib
E = [dict(id="AE1", clears="AE1: 1.6 records the second term's range as well", section="1.6",
old="""the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.""",
new="""the solver's tolerance and stops registering, and above it the term exceeds the base arc cost of 1
and stops being a perturbation. `scripts/epsilon6.py` reports the bands and bisects their edges.
`TIE_EPS2` behaves the same way and was measured at 1e-7, 1e-6 and 1e-5, all three leaving the same
single good with an alternative optimum — so it too is a switch rather than a dial, and its exact
value carries no more meaning than its form does (§2.3).""")]
patch_lib.apply(E)
