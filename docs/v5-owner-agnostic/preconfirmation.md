# Pre-confirmation of the v6 fix batch

**Purpose.** Every replacement value in `fixes-agreed.md` computed *before* it is written into the
spec, on the option-(c) wealth field, so that the v6 draft starts from confirmed numbers instead of
generating a fresh round of refutations. Nothing here has been applied to any spec.

**Method.** `field_c.py` and `field_c2.py` build the (c) field from `base_tax`, `base_production`,
the trade good and the four province-state static modifiers (only `devastation` is live at 1444, on
the ten `on_startup` Hussite provinces, scaled by level/100), then recompute every figure the batch
would quote. `devastation` grants `trade_goods_size_modifier = -2`, verified in
`common/static_modifiers/00_static_modifiers.txt`.

---

## The (c) field at 1444 — the new baseline

| quantity | v5.0 | **(c), pre-confirmed** |
|---|---|---|
| world wealth | 10,677.50 | **10,559.60** over 2,452 provinces |
| cost of devastation on ten provinces | not modelled | **12.80 ducats** |
| `Φ_w` sinks | `hangzhou` | **`english_channel`, `hangzhou`** |
| their `c_w` / node-wealth ranks | 1 / 10 | **2 / 1** and **3 / 12** |
| Phase 1 selects | `hangzhou` | **`genua`**, both sinks by promotion (2 promotions, 0 fallbacks) |
| sources | 7, `c_w` 52–79, degree 3.0 | **8**, `c_w` **44–75**, degree **3.1** vs map 4.0 |
| largest \|b_w\| | 0.0227 | **0.0226** |
| richest province | 1821 at 30.40 | **1821 at 27.00** |
| `Φ_w` agreement | 52.5% / 51.5% | **53.7% / 52.4%** |
| `Φ_ord` agreement | 60.3% | **60.5%**, **14** ends |
| sinks per good | 1–7, mean 3.6 | **1–8, mean 3.48** |
| acyclic / fallbacks | 29/29 / 0 | **29/29 / 0** |
| ordered pairs connected | 92.2% | **90.1%** |
| supply / demand contrast | 4–97 / 211–20,400 | **4–97 over 28 goods / 211–15,010** |
| `gulf_of_siam` downstream sets | 8 (claimed) | **7** |

**The (c) field reproduces v2.0's original §1.6 block almost exactly** — `genua` selected, both sinks
by promotion, 8 sources, `c_w` 44–75, degree 3.1, \|b_w\| 0.0226. v2 measured a field with no
modifier sweep, which is what (c) returns to. v5.0's rewrite of §1.6 was tracking a field that (c)
discards.

---

## Three claims change meaning, not just value

**P1 — `english_channel` is a sink at 1444 under (c), with no European growth at all.** The entire
Europe/institutions demonstration was built to answer "can Europe hold a sink?" Under (c) the answer
at the start date is yes. The demonstration's *purpose* changes: it is no longer an existence proof,
it is a statement about how Europe's sink strengthens and Asia's fades.

**P2 — the Lowlands result becomes vacuous.** "Developing the nine Lowland provinces by ×1.20 makes
`english_channel` a sink" is trivially true when `english_channel` is already one at ×1.00. Pre-
confirmed: Lowlands ×1.20 and ×10 both give `{english_channel, hangzhou}` — the same set as baseline.
This claim must be deleted or restated as a threshold for something else.

**P3 — `α_Φ = 1.5` sits in a band of width 0.25 on the (c) field**, `[1.38, 1.63]`, giving
`{english_channel, hangzhou}`; the widest bands are **1.70** (`[3.51, 5.21]` and `[6.30, 8.00]`).
So the "widest band" justification is false on the (c) field too, by a different margin. **A1's
resolution — 1.5 as a stipulation — is confirmed as the only defensible option, on both fields.**

---

## Pre-confirmed replacement values

| item | replacement value | status |
|---|---|---|
| **A1** | widest band on (c) is 1.70 at [3.51, 5.21]; 1.5's band is [1.38, 1.63], width 0.25 | **pre-confirmed** |
| **B1** | ten provinces devastated 20–50; cost 12.80 ducats on (c) | **pre-confirmed** |
| **B2** | 33 counted provinces carry `trade_goods = unknown` in history | **pre-confirmed** (14 was the agent's count of a subset; mine is 33 — to reconcile before drafting) |
| **B3** | Uppland `base_tax` 5 → 6, one province, 1.00 ducat | **pre-confirmed** |
| **C1** | 151 executable of 161; ten non-executable; partition 13/2/4/11 unmoved | **pre-confirmed** |
| **C2** | zero `assert` statements in `validate_v5.py` | **pre-confirmed** |
| **C3** | `change_price` values are fractions: paper 4.375 = 3.5 × 1.25 | **pre-confirmed** |
| **D1** | value-weighted mean share error ≤ 0.1% at all five nodes | **pre-confirmed** |
| **E1** | caravan cap 9.4–47.0%, median 21.9% | **pre-confirmed** |
| **E2** | 15 provinces beyond the trade goods | **pre-confirmed** — *and moot under (c)* |
| **E3** | 7 downstream sets; holdings 9.84/9.78/6.49; shares 0.3724 vs 0.3725 | **pre-confirmed** |
| **E4** | `highest_power` = strongest single province: 17/79 exact, 62/79 strictly less | **pre-confirmed** |
| **E5** | 3.69e-16 = 1.7–3.3 ULP | **pre-confirmed** |
| **E6** | orders span 11.3–14.3 | **pre-confirmed** |
| **E7** | 12 runs 0.088–0.181 s, 1 of 12 inside the stated range | **pre-confirmed** |
| **E8** | three cooldowns at `defines.lua` 1045 / 1212 / 1214 | **pre-confirmed** |
| **E9** | Cape in-degree 1, out-degree 3, 115 ordered pairs; no Europe→sink route | **pre-confirmed** |
| **E10** | 4–97 over 28 goods; only `cloves` has one producer | **pre-confirmed on both fields** |
| **E11** | four index tiebreaks, not two; zero ties on 1444 | **pre-confirmed** (tiebreak count from the sub-audit; the 1444 zero-ties result is mine) |
| **E12** | dev-scaling ≡ wealth-scaling under (c): max difference **0.00e+00** | **pre-confirmed — the defect is deleted, not corrected** |
| **G1** | (c) field figures, whole table above | **pre-confirmed** |
| **H1** | arc-order permutation changes the LP support on 10 of 10 goods, gaps ≤ 1.8e-15 | **pre-confirmed** |
| **X065** | at fixed α = 1.5 on (c) the count takes 1, 2, 3 and 4 | **pre-confirmed** |
| **X099** | 22-node sole-`genua` at **×1.65**; 18-node at **×2.15** | **pre-confirmed on (c)** |
| **X100** | Cape reversed on a **single** contiguous run **[2.88, 3.45]** on (c) — no interior gap | **pre-confirmed on (c)**; the agent's two-run result was on the v5 field |
| **X143** | spice thresholds `beijing` 3.61, `hangzhou` 4.12, `xian` 4.60, `canton` 4.77 | **pre-confirmed on (c)** |
| **X086/X087** | Europe dev ×1.02 → `{english_channel, hangzhou, wien}`; ×1.56 → `{english_channel, rheinland}`; ×2.00 → `{genua}` | **pre-confirmed on (c)** |

## Not pre-confirmable from files

| item | why |
|---|---|
| **X022** | the production tooltip's ÷12 divisor needs the running game; any divisor in [12.00, 12.14] fits one observation |
| **X021, X027, X177, X178** | rest on tooltip readings; the *arithmetic* is checkable and checks out, the readings are not reproducible without a session |
| **X056** | "the monument system is inert without Leviathan" is an engine behaviour, not a file fact — and moot under (c) |
| **A1, X008–X011, X013, X117, X145** | derivations and quantifier narrowings; confirmed by argument, no number to compute |

## Moot under (c) — subject deleted rather than corrected

**X035, X043, X045, X046, X047, X048, X050, X055, X056, X058, X059, X112, X176, X179** — the
classification table, the great-project machinery, the DLC gate, the CoT count, the buildings row,
the terrain/climate key list and the modifier-source enumeration all go. **Fourteen of the 62 open
items, five of them refutations.**
