# -*- coding: utf-8 -*-
"""v6.1 batch R -- 1.3's unrest note. It was written as an unclosed gap; it is a deliberate
exclusion, and the reason is owner-agnosticism, which is the property 1.3 exists to guarantee."""
import patch_lib
E = []

E.append(dict(id="R1", clears="R1: unrest is excluded on owner-agnosticism grounds, not pending",
section="1.3",
old="""**`unrest` is live at the 1444 start and the reference implementation does not read it.** This is a
known gap, stated rather than papered over: `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone,
so four of the five rows above are applied and `unrest` is not. What it would cost is measured. 21
counted provinces carry revolt risk between 4.834 and 14.834 in the start save — the figure is stable
across all three start saves in the tree — worth **12.23 ducats, 0.115%** of the 10,607.40 the model
computes; applying it would put world wealth at **10,595.17** and move **4 of 159 edges** of the
installed graph, leaving the sink set `{genua, hangzhou}` unchanged. *(An earlier version of this
paragraph said admitting it moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*
Closing the gap is a one-line change to `STATE_TAX_MOD` plus reading the save, and it moves the world
wealth figure that the rest of this document quotes, so it is recorded here as a decision rather than
made silently.""",
new="""**`unrest` is live at the 1444 start and is deliberately not read.** It is the one row in the table
that fails the test the rest of §1.3 is built on: **revolt risk is not a property of the place.** In
play it carries separatism from recent conquest, unaccepted culture, wrong religion and nationalism —
all of them relations between a province and *its owner*. Read it, and a province's wealth changes
when it is conquered, which is precisely what this section exists to prevent. `solver.py`'s
`STATE_TAX_MOD` therefore carries `occupied` alone, and four of the five rows above are applied.

The 1444 field shows the split directly. Of the 21 counted provinces carrying revolt risk in the start
save, **16 are authored in `history/provinces`** at integer 5/8/10/15 — Sofala's comment reads
"expansion of Shona into Sofala region causes major disruptions" — and the remaining **five are all
Shirvan-owned and receive theirs at runtime**. So even at the start date a quarter of it is owner-
derived, and during a campaign that share only grows.

**And the effect it would buy is already bought.** Conquest costing a province its wealth is delivered
by `devastation`, `occupied` and `under_siege`, all three of which are properties of the place and all
three of which the model applies. `unrest` would add owner-dependence without adding a mechanic.

What the exclusion costs is measured, so it is a known quantity rather than an assumption: **12.23
ducats, 0.115%** of the 10,607.40 world wealth reading it from the save, or **9.40 ducats, 0.089%**
reading only the authored 16. Either way it moves **4 of 159 edges** of the installed graph and leaves
the sink set `{genua, hangzhou}` unchanged. *(An earlier draft of this paragraph said admitting it
moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*"""))

E.append(dict(id="R2", clears="R2: the table lead-in states why four of five are applied",
section="1.3",
old="""static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied by the
reference implementation** — see the note below the table on `unrest`:""",
new="""static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied** — `unrest` is
excluded because revolt risk depends on the owner, which the note below the table sets out:"""))

patch_lib.apply(E)
