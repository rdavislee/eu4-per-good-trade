# -*- coding: utf-8 -*-
"""v6 batch 10 — C1/C2/C3 (§3.5's census, the phantom assertion, price-as-fraction) and E1/E8."""
import patch_lib
E = []

E.append(dict(id="R10-census", clears="C1/C2/C3: the census, the guard, and the units",
section="3.5",
old="""(All **161** `change_price` blocks were parsed — 93 in `events/`, 14 in `missions/`, 1 in `common/`
and **53 in `history/`, of which 13 are negative**, all in `history/countries/HAB - Austria.txt`.
v4.0 said 154 and 7: its parser silently recovered nothing from five mission files, which a bare
`except` hid, so the scan is now guarded by a per-file count assertion. The seven recovered blocks
are all positive and the partition is unchanged.
The history route matters: `wool`'s largest single negative is that file's `NEW_DRAPERIES` at
−0.25 for 2.5 → **1.875**, against the −0.20 the same key carries in `events/PriceChanges.txt`, and
`change_price` entries are keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13
was right; v3.0 reached 12 by parsing four of the five trees.)""",
new="""(**`change_price` values are fractions of the good's base price, not ducats** — the spec's own
figures only parse under that reading, and the shipped save `tutorial/eu4_tutorial_chapter10.eu4`
settles it: `paper` sits at `current_price=4.375` on a base of 3.5, which is × 1.25 and not + 0.25,
and `gems` at 5.000 on a base of 4.0. So a −0.25 event takes a 2.5 good to 1.875, and grain and wine
reach 0.625.

The install carries **161** textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in
`common/`, **53 in `history/` of which 13 are negative** (all in
`history/countries/HAB - Austria.txt`), and none in `decisions/`. **Ten of the 161 never execute:**
seven sit inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display
wrappers, so **151 are executable**. Six of the seven quoted ones duplicate a block already counted
in `events/`, and the seventh names a price key no event in the install ever sets. All ten are
positive and every negative block in the install is executable, so **the partition above is
identical under either census**. *(v4.0 said 154 by silently dropping the quoted seven; v5.0 said
161 by counting them; both were wrong about which number was the executable one. v5.0 also claimed
the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its
toolchain. `verify6.py` now carries the guard, and the reason a plain parse misses these is
mechanical: `pdx.py` tokenises a quoted string as one opaque unit, so a `change_price` inside a
tooltip string is invisible to the walker.)*

The history route matters: `wool`'s largest single negative is that file's `NEW_DRAPERIES` at −0.25,
against the −0.20 the same key carries in `events/PriceChanges.txt`, and `change_price` entries are
keyed, so 1.875 is the figure a campaign reaching 1540 holds. v2's 13 was right; v3.0 reached 12 by
parsing four of the five trees.)"""))

E.append(dict(id="R10-caravan", clears="E1: the caravan share, against the right denominator",
section="1.10",
old="""Measured on the 1444 start: the cap of 50 is **8.6% to 32.0% of an inland node's total trade power** (median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at
`champagne` — §2.2 derives inland from `members` instead and gets 25, dropping `siberia`; on that
basis the range, the largest-holder span and the count below are all identical and only the median
moves, to 17.5%), against a largest single incumbent holder of **23.6 to 143.2** — so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19.""",
new="""Measured on the 1444 start: the cap of 50 is **9.4% to 47.0% of an inland node's total trade power**, median **21.9%** over the flag's 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`. *(As a share of the node's total **after** the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right, since 8.6% of 532.0 is 45.8 rather than 50. §2.2 derives inland from `members` and gets 25 nodes, dropping `siberia`; on that basis only the median moves, to 21.3%.)* The largest single incumbent holder runs **23.6 to 143.2**, so a country at the cap outweighs the largest incumbent in **7 of the 26** inland nodes and is outweighed in the other 19."""))

patch_lib.apply(E)
