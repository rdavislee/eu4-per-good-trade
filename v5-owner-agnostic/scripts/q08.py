# -*- coding: utf-8 -*-
"""v5 batch 8 — v5.0's own overstatement of the narrow-window result, refuted by running the noise
test at 8 seeds instead of the handful the sentence was written from (`audit_bands2.py`)."""
import patch_lib
E = [dict(id="H64", clears="the narrow alpha window shrinks under noise; it does not disappear",
section="1.6",
old="""The last row is v4.0's result and it is **not reproducible**: under ±1% wealth noise that window
moves or disappears entirely, while the wide bands move by ≤0.03. It is not a band, so no constant
could honestly sit in it.""",
new="""The last row is v4.0's result and it is **not a band**. Refined to 0.001 it spans [1.406, 1.424] —
**0.018 wide**, against the one-sink band's 0.506 — and under ±1% wealth noise across 8 seeds its
edges move by up to 0.02 while its width ranges **0.00 to 0.03**: the window is the same size as the
noise that perturbs it, and on some seeds it collapses to a single sampled α. The three wide bands
over those same seeds keep widths of 0.28–0.51 with edges moving ≤0.03. A constant cannot honestly
be placed inside a window narrower than the uncertainty in its own edges. *(An earlier draft of this
paragraph said the window "moves or disappears entirely" under noise. At 8 seeds it disappears on
none of them — it shrinks. The weaker claim is the true one and it is sufficient.)*""")]

E.append(dict(id="H65", clears="2.3 repeated the same overstatement about the fitted map",
section="2.3",
old="""corrected wealth field of §1.3 it does not yield that map, and the map it was fitted to is not
reproducible under noise (§1.6).""",
new="""corrected wealth field of §1.3 it does not yield that map, and the α_Φ window that does yield it is
narrower than the uncertainty in its own edges under ±1% wealth noise (§1.6)."""))
patch_lib.apply(E[1:])
