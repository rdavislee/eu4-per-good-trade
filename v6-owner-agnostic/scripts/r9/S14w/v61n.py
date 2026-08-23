# -*- coding: utf-8 -*-
"""v6.1 batch N -- 1.3's condition table. Two corrections a reading caught:

  * `unrest` is listed as entering `tax_value`, but solver.py never implemented it -- STATE_TAX_MOD
    holds only `occupied`. The document described a model feature that does not exist.
  * "admitting it moves no edge" is false at alpha_Phi = 2.0: it moves 4 of 159.
  * devastation's scaling law is documented behaviour, not an assumption of this design.
"""
import patch_lib
E = []

E.append(dict(id="N1", clears="N1: devastation's scaling is documented, not assumed", section="1.3",
old="""| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier applies in proportion to the level, `-2 × level/100`, and that proportionality is an assumption rather than a file value. It is the **only** such assumption in this table — `unrest` and `nationalism` both carry per-unit comments in that same file, so the convention for stating a scaling exists and `devastation` simply does not use it.* | |""",
new="""| | *The magnitudes and directions above are all read from `00_static_modifiers.txt`. That file does not state the **scaling law** for `devastation`, and it is the only row here whose scaling it leaves open — `unrest` and `nationalism` both carry per-unit comments in it. The wiki settles the law: the penalties are "scaled linearly according to the percentage value" and are quoted at 100% devastation, which is the `-2 × level/100` the model applies. **This is the one row whose scaling rests on community documentation rather than on a shipped file**, and that difference is worth stating rather than smoothing over.* | |"""))

E.append(dict(id="N2", clears="N2: unrest is identified but not read by the model", section="1.3",
old="""`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. **`unrest`
is live at the 1444 start**: 21 counted provinces carry revolt risk between 4.834 and 14.834 in the
save, costing **12.23 ducats — 0.115% of world wealth** — and admitting it moves **no edge** of the
installed graph, so it is a fidelity correction with no orientation consequence. *Its scaling is
stated in the file:* the `unrest` block's own comment reads `#10% longer time to build troops for each
rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention.
*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so the model reads the save.)* These are what""",
new="""`occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. *Its
scaling is stated in the file:* the `unrest` block's own comment reads `#10% longer time to build
troops for each rr`, so its values apply per point, and the neighbouring `nationalism` block uses the
same convention.

**`unrest` is live at the 1444 start and the reference implementation does not read it.** This is a
known gap, stated rather than papered over: `solver.py`'s `STATE_TAX_MOD` carries `occupied` alone,
so four of the five rows above are applied and `unrest` is not. What it would cost is measured. 21
counted provinces carry revolt risk between 4.834 and 14.834 in the start save — the figure is stable
across all three start saves in the tree — worth **12.23 ducats, 0.115%** of the 10,607.40 the model
computes; applying it would put world wealth at **10,595.17** and move **4 of 159 edges** of the
installed graph, leaving the sink set `{genua, hangzhou}` unchanged. *(An earlier version of this
paragraph said admitting it moves no edge. That was measured at α_Φ = 1.5 and does not hold at 2.0.)*
Closing the gap is a one-line change to `STATE_TAX_MOD` plus reading the save, and it moves the world
wealth figure that the rest of this document quotes, so it is recorded here as a decision rather than
made silently.

*(Sixteen of the 21 are resolvable from `history/provinces` at integer risk 5/8/10/15; the other five,
all Shirvan-owned, receive theirs at runtime, so reading them needs the save.)* These are what"""))

E.append(dict(id="N3", clears="N3: the table's lead-in says which are applied", section="1.3",
old="""**Province condition is the one thing besides development and the good that wealth reads.** Five
static modifiers describe a province's own state, and all five are read from
`common/static_modifiers/00_static_modifiers.txt`:""",
new="""**Province condition is the one thing besides development and the good that wealth reads.** Five
static modifiers describe a province's own state, all five are defined in
`common/static_modifiers/00_static_modifiers.txt`, and **four of the five are applied by the
reference implementation** — see the note below the table on `unrest`:"""))

patch_lib.apply(E)
