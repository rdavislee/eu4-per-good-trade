# -*- coding: utf-8 -*-
"""v6.1 batch C -- 1.6's Europe narrative and table, re-measured. The trajectory is non-monotone with
narrow reversals, so it is stated as a direction with the reversals shown rather than smoothed."""
import patch_lib
E = []

E.append(dict(id="C1", clears="C1: the Europe narrative, re-measured", section="1.6",
old="""**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map already ends in the Channel and in
Hangzhou; as European development compounds the ends move west and Asia's pole fades — the Channel's
basin widens, non-monotonically, and then gives way as the end itself migrates: `genua` first holds an
end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and
past a broad range of European growth Asia holds no end at all. The mechanism is what carries this:
wealth is linear in development (§1.3), so developing a region moves its `c_w` share directly, and
`Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 1.5 and scaling European development only (`europe.py`,
824 counted European provinces):

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 (1444) | `english_channel`, `hangzhou` |
| ×1.02 | `english_channel`, `hangzhou`, **`wien`** |
| ×1.56 | `english_channel`, **`rheinland`** — Asia holds none |
| ×2.00 | `genua` alone |

Read the table as a direction rather than a trajectory, and on one node ordering: growth moves the
ends westward and thins Asia's, and by ×2.00 a single Mediterranean end at `genua` holds the map.
*Which* European node holds an end at the smaller factors is ordering-dependent in the same way the
1444 set is, so the direction is the claim and the membership is not. The last row is the exception
and is worth separating: at ×2.00 `genua` held an end in **60 of 60** relabellings, so a single
Mediterranean end under that much European growth is a property of the field rather than of the
ordering.""",
new="""**Europe becomes the centre of trade as it develops.** That is the design claim, and it is what
§3.1's first goal asks the field to deliver. At 1444 the map ends in Genoa and in Hangzhou; as
European development compounds Europe gains ends and Asia loses its one. The mechanism is what
carries this: wealth is linear in development (§1.3), so developing a region moves its `c_w` share
directly, and `Φ_w`'s ends follow the wealth.

Observed on the 1444 field, holding α_Φ = 2.0 and scaling European development only (`europe.py`,
824 counted European provinces). Boundaries are bisected, so each row is the interval over which the
set is constant:

| European development | `Φ_w` sinks |
|---|---|
| ×1.00 – ×1.14 | `genua`, `hangzhou` |
| ×1.14 – ×1.16 | `english_channel`, `genua`, `hangzhou`, **`rheinland`** |
| ×1.16 – ×1.19 | `genua`, `hangzhou` |
| ×1.19 – ×1.35 | `genua`, `hangzhou`, **`gulf_of_siam`** |
| ×1.35 – ×1.36 | `english_channel`, `genua`, `gulf_of_siam`, `hangzhou`, `rheinland` |
| ×1.36 – ×1.38 | `genua`, `gulf_of_siam` |
| **×1.38 – ×1.95** | **`english_channel`, `genua`, `rheinland` — Asia holds none** |
| ×1.95 – ×1.97 | `english_channel`, `genua`, `hangzhou`, `rheinland` |
| ×1.97 – ×2.46 | `english_channel`, `genua`, `rheinland` |
| ×2.46 – ×2.50 | `genua`, `rheinland` |

**Read the table as a direction, not a trajectory.** The direction is unambiguous: Europe goes from
one end to three and Asia goes from one to none, and the widest single interval in the table — ×1.38
to ×1.95 — is three European ends with nothing in Asia. But the path is not monotone. `hangzhou`
leaves at ×1.19, returns at ×1.95 and leaves again; `gulf_of_siam` holds an end across ×1.19–×1.38
and nowhere else; two intervals narrower than ×0.03 carry sets that appear once. Those reversals are
in the field, not in the solver: the orientation is order-invariant at every row.

*What this table is not evidence for. It scales all 824 counted European provinces by one factor at
once, which is not how development happens — real growth is province by province, with price changes
and colonisation on top. No save later than 1444 was available to test against, so the honest scope
is: this is the field's response to a uniform European multiplier, and the design intent is that
Europe's end strengthens as Europe develops. The intent is the claim; the row boundaries are a
property of one synthetic experiment.*"""))

patch_lib.apply(E)
