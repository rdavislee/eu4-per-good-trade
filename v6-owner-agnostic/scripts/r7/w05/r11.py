# -*- coding: utf-8 -*-
"""v6 batch 11 — E7/E8/E5 and the version banner: timing as an order of magnitude, the cooldowns
named, ULP corrected, and the header rewritten for v6.0."""
import patch_lib
E = []

E.append(dict(id="R11-cooldown", clears="E8/X106: the shipped cooldowns absorb some chatter",
section="1.10",
old="""only on its flag ladder. So almost nothing absorbs threshold chatter — a power share oscillating
across any single-valued limit flickers the mechanic, and that includes Propagate Religion for the
flagless countries its default and terminal branches cover.""",
new="""only on its flag ladder. So banding absorbs very little chatter — a power share oscillating across
any single-valued limit flickers the mechanic, and that includes Propagate Religion for the flagless
countries its default and terminal branches cover. **Banding is not the only damper, though:** three
shipped defines rate-limit the mechanics that carry these thresholds —
`TRADING_POLICY_COOLDOWN_MONTHS = 12` (both banded policies), and
`TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` — so a flickering share
does not translate into a flickering *effect* at those three. What is left exposed is everything
without a cooldown, which is most of the ladder."""))

E.append(dict(id="R11-timing", clears="E7/X114: a wall-clock timing is an order of magnitude",
section="2.2",
old="""**0.17–0.21 s for all 29 goods, a mean of 5.7–7.3 ms per good across runs** — individual goods
range 5.4–24 ms, so 7.3 is an average and not a maximum. "Milliseconds each" therefore holds
already,""",
new="""**of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average.** Repeated
runs on one machine span roughly 0.09–0.27 s for the full set and 3–7 ms per good as an average,
with individual goods reaching about 20 ms — so a two-significant-figure range is a statement about
a machine and a scheduler rather than about the algorithm, and none is quoted. *(v5.0 quoted
"0.17–0.21 s"; twelve fresh runs put only one inside that interval.)* "Milliseconds each" therefore
holds already,"""))

E.append(dict(id="R11-ulp", clears="E5/X166: 3.7e-16 is not one ULP", section="3.10",
old="""worst relative disagreement 0 to 3.7e-16, which is 1.7 to 3.3 units in the last place.""",
new="""worst relative disagreement 0 to 3.7e-16 — one to three units in the last place, not the single
ULP v5.0 claimed."""))

E.append(dict(id="R11-hdr", clears="the v6.0 banner and lineage", section="0",
old="""**Version:** 5.0""", new="""**Version:** 6.0"""))

patch_lib.apply(E)
