# -*- coding: utf-8 -*-
"""v5 batch 9 — the three text defects the round-2 claims extraction found, each re-measured first
(`audit_delta2.py`)."""
import patch_lib
E = []

E.append(dict(id="J66", clears="2.8 wore the unweighted agreement under the weighted label",
section="2.8",
old="""  baseline is known — `Φ_w` agrees with the per-good graphs on 52.5% of value-weighted edge-goods —""",
new="""  baseline is known — `Φ_w` agrees with the per-good graphs on **51.5%** of edge-goods *weighted by
  trade value*, and on 52.5% unweighted (§1.6) —"""))

E.append(dict(id="J67", clears="3.9's node-wealth ranks had no v5.0 provenance", section="3.9",
old="""`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth and none of them is a
sink""",
new="""`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field
— 296.0, 299.2 and 266.5 against `english_channel`'s 316.6 — and none of them is a sink""",
))

E.append(dict(id="J68", clears="what the save's highest_power field is not, stated with the test",
section="1.10",
old="""*(v4.0 read the save's `highest_power` field, 9.6–20.7, as the largest incumbent's power. It is not, and the conclusion drawn from it inverted.)*""",
new="""*(v4.0 read the save's per-node `highest_power` field as the largest incumbent's power. It is not: parsing each node's country sub-blocks at their own brace depth and comparing, `highest_power` differs from the largest single country's `val` on **79 of 79** nodes — at `venice` it is 53.2 against Venice's own 106.2 — and it matches no share of `total`, `max`, `p_pow` or `collector_power` either. What it does hold was not determined and the model does not read it; the figures above come from the country sub-blocks. The conclusion v4.0 drew from it inverted.)*"""))

patch_lib.apply(E)
