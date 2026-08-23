# -*- coding: utf-8 -*-
"""v6 batch 22 — the pre-confirmed statement fixes, S01-S14 plus N15-N20."""
import patch_lib
E = []

E.append(dict(id="S05a", clears="S05: the universal, in 0", section="0",
old="""world wealth; what it cost was an input surface whose classification was wrong in every audit that
examined it.""",
new="""world wealth; what it cost was an input surface whose classification was **wrong in both independent
audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X030 and X034 — and passed by v4.0's own repair harness,
which v5.0 then refuted."""))

E.append(dict(id="S05b", clears="S05: the universal, in 1.3", section="1.3",
old="""correct and was wrong in every audit that examined it.""",
new="""correct and was wrong in **both independent audits** that examined it — v4.0's own repair harness
passed it, and v5.0's audit then refuted what that harness had passed."""))

E.append(dict(id="S05c", clears="S05: the universal, in 3.13", section="3.13",
old="""  rule. That rule was wrong in every audit that examined it, which is why v6.0 drops it.""",
new="""  rule. That rule was wrong in both independent audits that examined it, which is why v6.0 drops
  it."""))

E.append(dict(id="S02", clears="S02/S03: flavor_geo.1 is fired but carries no development grant",
section="1.3",
old="""1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and*
   `add_devastation` — so development itself can move before the first tick.""",
new="""1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, directly from its own `events = { }` list in
   `common/on_actions/00_on_actions.txt` — a second path alongside the `on_startup_effect` chain that
   carries `flavor_boh.15`. **Development itself does not move before the first tick:** on this start
   the history parse matches the save on **2,472 of 2,472** provinces for `base_tax`,
   `base_production` and owner, and only `trade_goods` differs, on exactly the twenty provinces
   below. *(v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development
   pre-tick. It does not: its whole effect is legitimacy, a country modifier and a flag. Those keys
   are in `flavor_geo.3`, which `on_startup` does not fire — a mission does.)*"""))

E.append(dict(id="S04", clears="S04: no route leaves the Channel", section="1.6",
old="""the Channel the Hansa and the Danube. **No Europe→sink route passes the Cape of Good Hope** —""",
new="""**No route leaves `english_channel` at all** — it is a sink, out-degree 0, so the Hansa and the
Danube carry power *into* it rather than out. **No Europe→sink route passes the Cape of Good Hope** —"""))

E.append(dict(id="S07", clears="S07: uniform wealth does not equalise the per-node sum", section="1.1",
old="""equal, which uniform *wealth* gives but is not the same condition.""",
new="""equal — which uniform *per-province* wealth does **not** give, because nodes hold between 0 and 72
counted provinces, so equal provinces make unequal node sums.""",
))

E.append(dict(id="S09", clears="S09: the divisor bound from one observation", section="1.3",
old="""[12.00, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual""",
new="""(11.73, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual"""))

E.append(dict(id="N17", clears="N17: the non-executable blocks, itemised", section="3.5",
old="""seven sit inside quoted `effect_tooltip = "…"` strings and three inside `tooltip = { }` display
wrappers, so **151 are executable**.""",
new="""**four** sit inside `effect_tooltip = "…"` strings, **three** inside the `effect = "…"` string of a
`country_event_with_effect_insight`, and **three** inside `tooltip = { }` display wrappers, so
**151 are executable**."""))

E.append(dict(id="N18", clears="N18: the node-wealth ranks", section="3.9",
old="""`genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field""",
new="""`genua`, `gulf_of_siam` and `sevilla` rank 4th, 3rd and 7th by node wealth on the corrected field
(`mexico` is 2nd)"""))

E.append(dict(id="N20", clears="N20: 1e-5 was the residual, not a tolerance", section="3.16",
old="""   the identity failed at the tolerance v1 used and would have been diagnosed as a solver bug.""",
new="""   the identity's residual reached 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a
   solver bug."""))

E.append(dict(id="S13", clears="S13: the containment set is grounded on T3", section="1.1",
old="""the **node index decides** — that is why §2.8 asserts containment over a set that includes the
fallbacks.""",
new="""the **node index decides**. §2.8 asserts containment over a set that includes the fallbacks, and the
reason is **T3** (§3.2) — a fallback promotion that is a sink in neither the selected nor the promoted
set — not the wealth tie, which is incidental to it."""))

patch_lib.apply(E)
