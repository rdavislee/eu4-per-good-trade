# -*- coding: utf-8 -*-
"""v5 batch 7 — the six defects a no-context claims extraction found in the v5.0 text.
Five are contradictions between a regenerated passage and one that was not regenerated with it;
the sixth is the delta's only UNSOURCED row, replaced with a file value."""
import patch_lib
E = []

E.append(dict(id="G58", clears="3.13 still carried the flat-goods denial 1.3 refutes", section="3.13",
old="""(out, its value set by neighbouring countries' government forms) — and no 1444 province was
  observed carrying a *flat* `trade_goods_size` in the additive block. What is unenumerated is the""",
new="""(out, its value set by neighbouring countries' government forms) — and §1.3's whole-install sweep
  settles the additive block too: **fifteen** 1444 provinces carry a flat `trade_goods_size`, five
  from great projects and ten from permanent province modifiers. What is unenumerated is the"""))

E.append(dict(id="G59", clears="2.8's Razed-China row was still on the v4.0 wealth field", section="2.8",
old="""| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: it is a `Φ_w` sink, `c_w` rank 3, node-wealth rank 12, and holds the richest single province in the game. Zeroing `beijing` (node-wealth rank 39) moves nothing |""",
new="""| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{hangzhou}` to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: `c_w` rank 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. Zeroing `beijing` **also** moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — because deleting 1.3% of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does. The rank gap is what carries this row, not a null result.)* |"""))

E.append(dict(id="G60", clears="3.15 still asserted the supply/demand ratio 3.2 withdraws", section="3.15",
old="""sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local
spread, and supply contrast (10⁷) drowns demand contrast (10²–10³). Diagnosed, measured, and
replaced""",
new="""sinks land where the field is locally flat, demand enters only as `(c−s)/deg` against the local
spread, and the supply signal is **sparse** rather than large — most nodes produce nothing at all
of a given good, so `(c−s)/deg` is dominated by where supply *exists*, not by how big it is.
*(v1 and v2 gave the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", and v3.0
through v4.0 repeated it here while §3.2 was withdrawing it. §3.2 is right: that ratio was `max(s)`
over v1's ε floor, and with the floor removed the contrasts run **4–97 on supply against
211–20,400 on demand** across the 29 goods — the demand side is the wider one. Sparsity is what
survives the floor's deletion, and it is what the diagnosis rests on.)* Diagnosed, measured, and
replaced"""))

E.append(dict(id="G61", clears="1.10's caravan measurement did not say which inland basis it used",
section="1.10",
old="""(median 17.9% over the 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at `champagne`)""",
new="""(median 17.9% over the **flag's** 26 inland nodes, whose totals run 106.4 at `xian` to 532.0 at
`champagne` — §2.2 derives inland from `members` instead and gets 25, dropping `siberia`; on that
basis the range, the largest-holder span and the count below are all identical and only the median
moves, to 17.5%)"""))

E.append(dict(id="G62", clears="1.6 gave two live justifications for the same constant", section="1.6",
old="""of it (the band table below), and the value was chosen with a target count in view. What the world""",
new="""of it (the band table below), and v2.1 chose the value with a target count in view — a calibration
§2.3 now withdraws, since the ground on which 1.5 is *retained* is the band table and not that
target. What the world"""))

E.append(dict(id="G63", clears="the Europe demonstration's only unsourced sentence", section="1.6",
old="""holds none. That range is far below what the Renaissance, Colonialism and Printing Press deliver
  over 1450–1550.""",
new="""holds none. **What the model claims here is the threshold, not the size of the historical edge**:
  2% is enough, and the project measures nothing about how much development Europe actually gained.
  What the files do settle (`common/institutions/00_Core.txt`) is that all three institutions the
  period is named for begin **in Europe, inside this window** — Renaissance `1450.1.1` at Florence
  (province 116), Colonialism `1500.1.1` at Sevilla (224), Printing Press `1550.1.1` at Frankfurt
  (1876) — and that the Renaissance's embracement bonus is `development_cost = -0.05`, a standing
  5% discount on every subsequent development point. Those bonuses are **country-scoped and so are
  excluded from wealth by §1.3**; they reach the map only by changing how fast a province's
  development grows, which is the input `europe.py` scales directly."""))

patch_lib.apply(E)
