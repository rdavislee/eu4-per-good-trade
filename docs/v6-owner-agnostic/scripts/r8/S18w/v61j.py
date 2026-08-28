# -*- coding: utf-8 -*-
"""v6.1 batch J -- three passages a reading caught that no check covers: the b-scaling note, the
European-node scaling note, and 3.9's vanilla comparison, whose 'rich non-sink' example is now the
sink."""
import patch_lib
E = []

E.append(dict(id="J1", clears="J1: the b-scaling figures, re-measured", section="1.6",
old="""scaling `b` *down* pushes genuine flow arcs into the free set. Measured: identical orientation at
×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶, where the sink set also collapses to
`{genua}` — the orientation degrades and the sink
set happens to survive, so the sink set is not the quantity to watch here.""",
new="""scaling `b` *down* pushes genuine flow arcs into the free set. Measured: identical orientation from
×1 down to ×10⁻², **22** edge flips at ×10⁻⁴ where the sink set becomes `{english_channel, hangzhou}`,
and **96** at ×10⁻⁶ where it becomes `{hangzhou}`. The orientation degrades before the sink set does,
so the sink set is not the quantity to watch here."""))

E.append(dict(id="J2", clears="J2: the European-node scaling note, re-measured", section="1.6",
old="""model: scaling the 22 European *nodes* rather than European provinces makes `genua` the sole sink
from about ×1.65 (the 18-node western/central subset needs about ×2.15), and somewhere inside
roughly ×2.9–×3.5 the Cape of Good Hope **reverses** — 1444's Atlantic→Cape→Indian-Ocean drainage
becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast. The reversal is bounded above as well as
below, so it is a window and not a threshold, and its edges move with the field.""",
new="""model: scaling the 18 western and central European *nodes* rather than European provinces makes
`genua` the sole sink from about ×1.55, while scaling all 22 does not produce a sole sink anywhere
below ×4 — the eastern four keep pulling ends of their own. The Cape of Good Hope **reverses** under
the same growth: 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` drainage becomes
`comorin_cape`/`malacca`/`zanzibar`→Cape→`ivory_coast` by about ×1.6 on the 22-node scaling. It is not
a single window — the Cape's in- and out-sets change several times across ×1–×3 and reverse more than
once — so the observation is that the Cape's direction is a function of European development, not that
there is a threshold at which it turns."""))

E.append(dict(id="J3", clears="J3: 3.9's wealth-versus-sink illustration, with the correct roles",
section="3.9",
old="""intent from the world state instead of authoring it: all wealth pulls (a rich non-sink node —
`genua`, `gulf_of_siam` and `sevilla` rank 4th, 3rd and 7th by node wealth on the corrected field
(`mexico` is 2nd)
— 296.0, 297.9 and 266.5 against `english_channel`'s 316.6, which is a sink — draws more edges in than it sends out as a net demander even though flow passes through),
the wealthiest places win, and the ends emerge and move when the wealth moves —""",
new="""intent from the world state instead of authoring it. **Wealth pulls, but the wealthiest node is not
automatically an end.** On this field `english_channel` is the richest node at 316.6 and is *not* a
sink: it drains to `genua`, which is 4th at 296.0. `mexico` (300.4, 2nd), `gulf_of_siam` (297.9, 3rd)
and `sevilla` (266.5, 7th) are likewise net demanders that draw more edges in than they send out
while flow still passes through them. What makes an end is where the flow *terminates*, which is a
property of the whole field and the graph rather than of a single node's rank — and the ends emerge
and move when the wealth moves —"""))

patch_lib.apply(E)
