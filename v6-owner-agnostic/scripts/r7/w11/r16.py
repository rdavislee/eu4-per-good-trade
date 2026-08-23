# -*- coding: utf-8 -*-
"""v6 batch 16 — passages the first pass never opened: 3.13's surviving classifier, 2.8's
razed-China row, 3.9's node wealths, and the R3 leftovers in 3.4 and 3.16."""
import patch_lib
E = []

E.append(dict(id="R16-313", clears="3.13 kept the classifier and its flat-bonus count", section="3.13",
old="""- **What else multiplies `goods_produced`, and which side of the owner line does each source fall
  on?** §1.3's classification handles the sources observed so far — the owner's
  `global_trade_goods_size_modifier` (out, country-scoped) and `bonus_from_merchant_republics`
  (out, its value set by neighbouring countries' government forms) — and §1.3's whole-install sweep
  settles the additive block too: **fifteen** 1444 provinces carry a flat `trade_goods_size`, five
  from great projects and ten from permanent province modifiers. What is unenumerated is the
  rest of the surface: `trade_goods_size` and `trade_goods_size_modifier` appear in buildings,
  estate privileges, government reforms, church aspects, fervor, ages and event modifiers, and
  each source needs the §1.3 locality test applied to it before a modded or late-game province can
  be priced. Settling work: enumerate every source of both keys and classify each; the model needs
  the answer only for sources that can be live with no owner input.""",
new="""- **Should any source beyond province condition be allowed to multiply `goods_produced`?** §1.3
  reads development, the trade good and the four province-state modifiers, and nothing else — so
  this is now a **design** question rather than a classification one. The keys
  `trade_goods_size` and `trade_goods_size_modifier` are granted in many places (buildings, event
  modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts,
  trade-company investments), and v3.0 through v5.0 tried to admit the province-scoped subset by
  rule. That rule was wrong in every audit that examined it, which is why v6.0 drops it. Re-admitting
  any of those sources means re-admitting the maintenance burden with it, and the question to settle
  first is whether the fidelity is worth it — on the 1444 start the whole set was worth 0.98% of
  world wealth."""))

E.append(dict(id="R16-28razed", clears="2.8's razed-China row, on the v6 field", section="2.8",
old="""| Razed China | Zeroing `hangzhou`-node development relocates the sink in one solve — measured: the `Φ_w` sinks move from `{hangzhou}` to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: `c_w` rank 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single province in the game. Zeroing `beijing` **also** moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — because deleting 1.3% of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does. The rank gap is what carries this row, not a null result.)* |""",
new="""| Razed China | Zeroing `hangzhou`-node development relocates an end in one solve — measured: the `Φ_w` sinks move from `{english_channel, hangzhou}` to `{doab, english_channel, gulf_of_siam}`, 23 of 159 edges flipping. `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0, and it holds the richest single province the model counts. Zeroing `beijing` **also** moves the map — 15 flips — because deleting a percent of world wealth renormalises `c_w` everywhere; what separates the two is that `hangzhou` **survives as a sink** when `beijing` is zeroed and does not when `hangzhou` is. *(v2 through v4.0 said zeroing `beijing` "moves nothing". It does; the asymmetry is which node keeps its end, not whether the map moves.)* |"""))

E.append(dict(id="R16-39wealth", clears="3.9's node wealths on the v6 field", section="3.9",
old="""— 296.0, 299.2 and 266.5 against `english_channel`'s 316.6 — and none of them is a sink —""",
new="""— 296.0, 297.9 and 266.5 against `english_channel`'s 316.6, which is a sink —"""))

E.append(dict(id="R16-313cal", clears="3.13's cloves calibration on the v6 field", section="3.13",
old="""  Deccan, **demand rank 2** under α = 16 with the rank-1 demander `hangzhou` acting as a transit
  node, becomes the cloves sink; v2 said Beijing "holds the richest single province", which it
  does not — that is `hangzhou`, at 30.4 against Beijing's 19.5, and under this calibration Beijing
  is only demand rank 3), the tolerance re-routes arcs""",
new="""  under α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a
  high-demand node rather than a geographic accident; v2 said Beijing "holds the richest single
  province", which it does not — that is `hangzhou`), the tolerance re-routes arcs"""))

E.append(dict(id="R16-34", clears="R3: 3.4's v1 identity figures", section="3.4",
old="""agreement collapsing from 159/159 to 68/159; the identity is gone in v2 but the reason to refuse""",
new="""agreement collapsing to well under half the map; the identity is gone in v2 but the reason to refuse"""))

E.append(dict(id="R16-316", clears="R3: 3.16's v1 tolerance figure", section="3.16",
old="""   the identity failed at 1e-5 and would have been diagnosed as a solver bug.""",
new="""   the identity failed at the tolerance v1 used and would have been diagnosed as a solver bug."""))

patch_lib.apply(E)
