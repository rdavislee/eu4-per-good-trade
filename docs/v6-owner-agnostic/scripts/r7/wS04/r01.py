# -*- coding: utf-8 -*-
"""v6 batch 1 — §1.3: wealth becomes development + trade good + province condition (option c)."""
import io, patch_lib
E = []

E.append(dict(id="R1-formula", clears="R1: the wealth formula", section="1.3",
old="""```
goods_produced(p)   = GP_COEFF · base_production(p) · (1 + Σ local goods-produced modifiers)
                                                             # + local flat goods bonuses
trade_value(p)      = goods_produced(p) · price(good(p)) · (1 + Σ local trade-value modifiers)
                                                             # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p) · (1 + Σ local tax modifiers)   # ducats / YEAR
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR""",
new="""```
goods_produced(p)   = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)
trade_value(p)      = goods_produced(p) · price(good(p))     # ducats / YEAR
tax_value(p)        = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)
wealth(p)           = tax_value(p) + trade_value(p)          # ducats / YEAR"""))

E.append(dict(id="R1-inputs", clears="R1: three inputs, stated up front", section="1.3",
old="""**Wealth is owner-agnostic.** It is a property of the *place* — what the land is worth per year,
before anyone's government touches it. No autonomy, no production efficiency, no national ideas,
no estate or government modifiers, no technology. Two provinces with the same terrain, development
and trade good have the same wealth whoever owns them, and a province's wealth does not change
when it is conquered.""",
new="""**Wealth is owner-agnostic, and it reads three things about the province: its development, its
trade good, and its own current condition.** It is a property of the *place* — what the land is
worth per year, before anyone's government touches it. No autonomy, no production efficiency, no
national ideas, no estate or government modifiers, no technology. Two provinces with the same
development, trade good and condition have the same wealth whoever owns them, and a province's
wealth does not change when it is conquered.

**Owner-agnosticism is true by construction here, not by a rule that has to be policed.** v3.0
through v5.0 stated the property and then defended it with a two-test classifier applied to a sweep
of the install — is this modifier local, does it enter wealth — which is a large surface to keep
correct and was wrong in every audit that examined it. `base_tax`, `base_production` and the trade
good are bare attributes of the place, so nothing about them needs classifying. *What this gives up:*
`gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely province-scoped and
are no longer read, along with great projects, permanent province modifiers and the DLC state they
depended on. On the 1444 start that whole apparatus was worth **0.98%** of world wealth over 87 of
2,472 provinces, and the model trades that fidelity for an input surface with no classification
question in it."""))

E.append(dict(id="R1-table", clears="R1: the classification table is deleted", section="1.3",
old_file_slice=("**Which modifiers are local, and which of those enter wealth.**",
                "The two rows that are local but do not enter — glass and chinaware — are the whole of the\nrule-versus-vocabulary tension: §1.3 excludes production efficiency and autonomy by name, and the\nsecond test excludes them again for the same reason, so there is nothing left to decide.\n"),
new="""**Province condition is the one thing besides development and the good that wealth reads.** Four
static modifiers describe a province's own state, and all four are read from
`common/static_modifiers/00_static_modifiers.txt`:

| modifier | what it grants | enters |
|---|---|---|
| `devastation` | `trade_goods_size_modifier = -2`, scaled by the devastation level | `goods_produced` |
| `prosperity` | `trade_goods_size_modifier = 0.25` | `goods_produced` |
| `under_siege` | `trade_goods_size_modifier = -0.25` | `goods_produced` |
| `occupied` | `trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5` | both |

Only `occupied` touches the tax term; the other three reach `goods_produced` alone. These are what
make the map answer to war — §1.2's volatility and §3.3's "a besieged province genuinely produces
less" both rest on them, and §2.8's war rows are their test.

**They are not all quiet at the 1444 start.** Ten provinces begin devastated — Bohemia at 50 and
Erzgebirge and Moravia at 20 — and no province-history file says so: the devastation is applied by
`on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite Wars"). It costs **13.40
ducats** across the eleven affected counted provinces. The chain is
`common/on_actions/00_on_actions.txt` → `on_startup_effect` →
`common/scripted_effects/01_scripted_effects_for_on_actions.txt` → `country_event flavor_boh.15`.

**The start state is what the engine produces, not what the history files say.** That is the general
form of the point above, and it costs three separate reads:

1. **`on_startup` effects**, as above. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`,
   `flavor_geo.1` and others, and `flavor_geo.1` carries `add_base_tax`, `add_base_production` *and*
   `add_devastation` — so development itself can move before the first tick.
2. **`add_base_*` in a dated block before the start date accumulates**, and v5.0 and earlier
   overwrote instead of adding, silently dropping the grant. Province 1 (Uppland) has `base_tax = 5`
   undated plus 1 at `1436.4.28`; the game has 6.
3. **`is_city = yes` is not a filter the engine applies.** 20 owned provinces omit or comment out
   that line — province 265 is one, and it is also one of the devastated ten — and the engine treats
   them as cities. The model counts a province when it has an owner and lies in a trade node:
   **2,472** provinces, not 2,452.

**Twenty counted provinces have no trade good in their history file** (`trade_goods = unknown`); the
engine assigns one at start from each good's `chance = { }` block. The wealth field is therefore
partly the result of one random draw. The model does not try to predict the draw: it reads whatever
the game's current state holds, which is what it does for development too.
"""))

txt = io.open(patch_lib.SPEC, encoding="utf-8").read()
for e in E:
    if "old_file_slice" in e:
        a, b = e.pop("old_file_slice")
        i = txt.index(a); j = txt.index(b) + len(b)
        e["old"] = txt[i:j]
patch_lib.apply(E)
