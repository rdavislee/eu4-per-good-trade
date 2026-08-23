# -*- coding: utf-8 -*-
"""v6 batch 2 — the rest of §1.3 and §2.2's solver item: flat-bonus sentence, the is_city
reference condition, the unowned-province rule, and the tooltip schemas (X021/X027)."""
import patch_lib
E = []

E.append(dict(id="R2-flat", clears="X-flat: the flat-bonus sentence has no table to point at",
section="1.3",
old="""development first and then applies a percentage — `Base 0.49` then `Tax Income Efficiency 125.0%`,
giving 0.6125, which the province window shows as 0.62. Flat goods bonuses are the exception: they
add into `goods_produced` *before* the price multiply. The goods-produced tooltip's shape is
**consistent with** that and does not establish it — it carries an additive `Base Goods Produced`
block (`Base Production: +0.80`) above a separate multiplicative `Goods Produced Efficiency` block.
Fifteen 1444 provinces do carry a flat bonus in the first block (the table above), so the ordering
matters in practice and not only in principle.""",
new="""development first and then applies a percentage. Observed on Garnatah: `base_tax` 6 with
`Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`. **0.49 × 1.25 is 0.6125, which
truncates to 0.61, not 0.62** — so the engine is not multiplying the displayed figure. It multiplies
the untruncated monthly value: 6 × 0.0833… = 0.49999…, × 1.25 = 0.62499…, displayed 0.62. The
example establishes the ordering (base from development first, percentage second) and nothing
finer. *(v3.0 through v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires
rounding while §2.3 requires truncation. Both cannot hold.)* Flat goods bonuses would add into
`goods_produced` before the price multiply — the goods-produced tooltip carries an additive
`Base Goods Produced` block above a multiplicative `Goods Produced Efficiency` block — but under
§1.3 no source grants one, so the ordering is stated for the emitter's benefit and is not exercised
by any province in the model."""))

E.append(dict(id="R2-taxbasis", clears="X021: the tax tooltip schema is arithmetically wrong",
section="1.3",
old="""both as *annual* quantities divided by twelve for display. The tax tooltip reads
`Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6, `Base: 0.16 (Yearly 2.00)` at
`base_tax` 2. The monthly production tooltip's `Trade Value` line is the province window's *annual*
`Trade Value` over twelve — observed 3.52 → `Trade Value: +0.29`. Both monthly figures are the
annual value over twelve, so the annual forms add directly with no conversion.""",
new="""both as *annual* quantities divided by twelve for display. The tax tooltip reads
`Base: trunc(base_tax / 12) (Yearly base_tax)` — observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6
and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2. The parenthetical is `base_tax` itself and the
`Base` line is its truncated twelfth; it is **not** twelve times the displayed figure, which would
give 5.88 and 1.92. *(v3.0 through v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both
of its own data points.)* The monthly production tooltip's `Trade Value` line is consistent with the
same relation on one observation, 3.52 → `+0.29`, which fixes the divisor only to within
[12.00, 12.14]. Both monthly figures being the annual value over twelve is what lets the annual
forms add directly, and the tax pair establishes it at two development levels."""))

E.append(dict(id="R2-refcond", clears="the TAX_COEFF reference condition and the province filter",
section="1.3",
old="""to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year. That is the reference condition
`TAX_COEFF = 1.0` was measured at, and it is the same for every province the model counts: all of
them are cities (`is_city = yes`), and ownership is not modelled, so every one is treated as cored.
Carrying either term again would double-count it.

Unowned provinces are outside the model: `s` and `c` are computed over provinces with an owner and
`is_city = yes`, because an unowned province produces nothing the trade system can move.""",
new="""to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a year. That is the reference condition
`TAX_COEFF = 1.0` was measured at, and the model applies it to every province it counts: ownership
is not modelled, so every province is treated as cored and settled. Carrying either term again would
double-count it. *This is a modelling choice with a known cost — two readings, both on cored city
provinces at `base_tax` 2 and 6, are what `TAX_COEFF = 1.0` rests on, and the development range runs
past 50.*

Unowned provinces are outside the model: `s` and `c` are computed over provinces that have an owner
and lie in a trade node, because an unowned province produces nothing the trade system can move."""))

E.append(dict(id="R2-solver", clears="§2.2 item 4: the solver's wealth expression", section="2.2",
old="""4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + local tax modifiers) + (GP_COEFF · base_production + local flat
   goods bonuses) · (1 + local goods-produced modifiers) · price · (1 + local trade-value
   modifiers)`, and no autonomy, efficiency, ideas or owner terms. The solver reads the local
   modifiers from §1.3's classification, applied to the whole install: in vanilla at 1444 that is
   `gems` (+15% tax, 43 provinces), `incense` (+10% trade value, 29 provinces), six great projects
   and ten permanent province modifiers — 16 provinces beyond the two trade goods. World wealth is
   **10,677.50** annual ducats over 2,452 counted provinces. Then per-node `trade_value`, `s`, `c`
   with per-province α, and the per-good balance `b = s − c`.""",
new="""4. Per-province `wealth` — **owner-agnostic** per §1.3:
   `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production ·
   (1 + province-state goods modifiers) · price`, and no autonomy, efficiency, ideas or owner terms.
   The only modifiers read are the four that describe the province's own condition, and at 1444 only
   `devastation` is live, on eleven provinces. `GP_COEFF` is **read from**
   `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded (§2.3). World wealth is
   **10,594.70** annual ducats over **2,472** counted provinces. Then per-node `trade_value`, `s`,
   `c` with per-province α, and the per-good balance `b = s − c`."""))

patch_lib.apply(E)
