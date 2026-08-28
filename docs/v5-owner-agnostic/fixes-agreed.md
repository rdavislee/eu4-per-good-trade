# Agreed fix batch — v5.0 → v6.0

Negotiated between the author and the no-context validation agent that produced
`validation-v5.md` (134 CONFIRMED / 39 PARTIAL / 22 REFUTED / 1 UNVERIFIABLE over X001–X196).
Every item below is agreed by both. Each names what the spec says now, what it should say, and who
verified it. The owner's architecture decision is recorded at **G1**: option (c).

Conventions: *verified by both* = the author re-derived the agent's finding independently.
*conceded by the agent* = the author's counter-argument was accepted.

---

## A. A justification is withdrawn, and nothing replaces it

**A1 — `α_Φ = 1.5` becomes a stipulation.** §1.6 and §2.3 currently retain 1.5 "because it sits
inside the widest sink-count band". Over α_Φ ∈ [1, 8] the widest band is `{deccan, hangzhou}` at
[4.19, 6.73], width **2.54**; the [1.43, 1.93] band is **fourth**, width 0.50. The superlative
depended entirely on an undefended scan cap of 3.00. *Verified by both.*

The author proposed replacing it with noise-stability of the sink set. **The agent tested and
refuted that**: the sink set is stable on 8/8 seeds at *every* α tested, on both the v5 field and the
plain field — no discriminating power at all — and it contradicts §1.6's own X068 finding that the
sink set is not the quantity to watch under perturbation. Orientation flip count does discriminate
(0 flips at α ∈ {1.2, 1.5}, 19 at α = 3.0) but selects a *range*, and its low end gives five sinks.

**Agreed resolution:** own 1.5 as a design constant exactly as `P₀ = 2.0` is owned — superlinear,
round, chosen rather than derived. The band table stays as a record of what other values give.
No new justification is manufactured, because *every candidate creates a fresh claim of the kind
that has failed in each of the last five rounds*.

**A1-trap (agreed, must be written into the section as a warning):** if the wealth model changes and
the two-sink map returns, **do not** justify 1.5 by "it reproduces the vanilla-like two-end map at
1444". That is V213 verbatim — the calibration §2.3 has just withdrawn — re-entering through the
back door, and it drags §3.9's withdrawn "two vanilla-like ends" premise (X162) back with it.

---

## B. The model misreads the 1444 start state (solver fixes, not only spec fixes)

**The start state is `history/provinces/` *plus* `on_startup`.** Chain verified by both:
`common/on_actions/00_on_actions.txt:33` → `common/scripted_effects/01_scripted_effects_for_on_actions.txt:4795`
→ `events/flavorBOH.txt` `flavor_boh.15` → `add_devastation`. A history-file sweep cannot see this
by construction. `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1`,
`flavor_mam.111` and two others; `flavor_geo.1` carries `add_base_tax`, `add_base_production` **and**
`add_devastation`.

| | defect | cost |
|---|---|---|
| **B1** | Ten provinces carry devastation 20–50 at the start (Hussite aftermath: 50 on 266/2968/2970/4724/4725, 20 on 265/267/1771/2967/4237/4726). §1.3 states "all are zero at the 1444 start" — **false**. | 6.92–17.30 ducats overstated |
| **B2** | Fourteen counted provinces are `trade_goods = unknown` in history and hold a real good in game, rolled at start from each good's `chance = { }` block. **The wealth field is therefore partly randomised**, and §3.16's own caution about randomised inputs applies to it. | 8.20 ducats missing; 14 provinces absent from six goods' supply shares |
| **B3** | `add_base_tax` in a dated block *before* the start date is not applied. Province 1 (Uppland): `base_tax = 5` undated, `1436.4.28 = { add_base_tax = 1 }`, game has 6. Swept all three `add_base_*` keys over every dated block ≤ 1444.11.11 — exactly one province. | 1.00 ducat |

**Total: 43.95 ducats across 45 provinces (0.41%), plus 6.92–17.30 overstated.** That is between a
third and a half the size of the entire province-modifier apparatus (105.10), and it lands in
`base_tax`, `base_production` and trade good — the only inputs the simplified model would retain.
**These fixes are required under every architecture option.**

---

## C. §3.5's price census, including the worst error in the document

**C1 — the executable census is 151, not 161 and not v4.0's 154.** Ten of the 161 textual
`change_price` blocks never execute: **seven** inside quoted `effect_tooltip = "…"` /
`country_event_with_effect_insight`'s `effect = "…"` strings, and **three** inside EU4's explicit
`tooltip = { }` display wrapper (`WOC_Hisn_Kayfa:1448`, `:1459`, `events/flavorMAL.txt:1736`).
`pdx.py` swallows quoted strings but parses `tooltip = { }` fine, which is exactly why v4.0 reached
154 and v5.0 reached 161 and both are wrong. Six of the seven quoted blocks duplicate a block
already counted in `events/`; the seventh, `DOM_Britain_Missions.txt`'s `ENGLISH_FUR_TRADE`, names a
price key **no event in the install ever sets** — decisive on its own.

**The 13 / 2 / 4 / 11 partition does not move** under either census: all ten non-executable blocks
are positive, all 40 negative blocks in the install are executable, and the partition is
`min(negatives)` per good. *Verified by both.*

**C2 — delete the claim of a guard that does not exist.** §3.5 says the scan is *"now guarded by a
per-file count assertion."* **`validate_v5.py` contains zero `assert` statements** and `w10.py` has a
bare `except` with none. The claim is false. This is the most serious error class in the audit —
the document tells a reader a thing is checked when nothing checks it. Either build the guard
(`assert sum(raws.values()) - len(hits) == 10`, with the ten named) or delete the sentence. **Agreed:
build it, then the sentence is true.**

Also delete the stated mechanism: "a bare `except` hid it" is wrong. No exception ever fires;
`pdx.TOK`'s `"[^"]*"` alternative collapses a quoted tooltip into one opaque token, so the walker
never sees inside it.

**C3 — state that `change_price` values are fractions of base price, not ducats.** The spec writes
`NEW_DRAPERIES` "at −0.25 for 2.5 → 1.875" and never says why that isn't 2.25. Proof from shipped
save state (`tutorial/eu4_tutorial_chapter10.eu4`): `paper` `current_price=4.375` with base 3.5
(**× 1.25**, not + 0.25) and `gems` `current_price=5.000` with base 4.0. *Verified by the author.*
One clause fixes the section and makes "grain and wine reach 0.625" legible as 2.5 × 0.25.

---

## D. §3.10's magnitude claim does not survive

**D1.** §3.10 says per-good propagation makes the income error "redistributive and single-digit
percent" and quotes nine per-collector percentages. The agent found they are artifacts of freezing
the powershare at one reference commodity (`ref = GL[0]` in `audit_f4.py`); sweeping the reference
moves Sevilla's MOR from −9.84% to +7.93%, a 17.77-point swing.

**The author went further and both agree the conclusion changes.** Computing the scalar a real
implementation would store — the **value-weighted mean powershare** — the error is:

| node | quoted triple | range over references | value-weighted mean |
|---|---|---|---|
| sevilla | +1.08 / +1.16 / −9.84 | 17.77 pts | **−0.01 / −0.01 / +0.10** |
| champagne | +0.35 / −0.63 / +0.31 | 1.47 | ~0.00 |
| genua | +0.23 / −0.18 / −0.19 | 1.88 | −0.01 / −0.00 / +0.01 |
| malacca | +0.59 / −0.53 / −0.28 | 0.90 | +0.01 / −0.01 / −0.00 |
| gulf_of_siam | ~0.00 | 0.12 | ~0.00 |

**≤ 0.1% everywhere — three orders of magnitude below "single-digit percent".** So per-good
propagation breaks **exactness**, not materiality, and the magnitude is a property of which scalar
you substitute rather than of the design choice. "Keeping propagation on a single graph is
load-bearing for Goal 7" must be restated as load-bearing for *exactness*. The identity itself
(single graph, 0 to 3.7e-16) is untouched.

This is the same defect class as v4.0's 0.41%: v5.0 diagnosed it, fixed `collect_pool` to be per
good, and re-committed it with a different arbitrary choice.

---

## E. Precision corrections — the conclusion stands, the number or quantifier does not

| # | claim | now | should be |
|---|---|---|---|
| **E1** | X107 caravan share | "8.6%–32.0% of an inland node's total trade power" — impossible: 8.6% of 532.0 is 45.8, not 50 | **9.4%–47.0%, median 21.9%** as the share of the node's total; the 8.6–32.0 figures are the share *after* the grant and must be labelled as such |
| **E2** | X112 | "16 provinces beyond the two trade goods" | **15** — province 542 (Golconda) is a gems province *and* carries `diamond_mines_of_golconda_modifier` |
| **E3** | X169 | `gulf_of_siam` has 8 downstream sets; effect is small because collectors "hold almost nothing" downstream | **7** sets; collectors hold 9.84 / 9.78 / 6.49 in `burma`. The effect is small because their shares *among the three* are near-identical at the node (0.3724) and at `burma` (0.3725) — near-**proportionality**, not smallness |
| **E4** | X196 | `highest_power`'s meaning "was not determined" | it is the **strongest single province's** trade power: equals `max(country province_power)` on exactly 17 of 79 nodes and is strictly less on the other 62 |
| **E5** | X166 | "at most one unit in the last place" | 3.69e-16 is **1.7–3.3 ULP** |
| **E6** | X171 | "thirteen orders of magnitude" | the set spans 11.3–14.3 → **eleven to fourteen** |
| **E7** | X114 | "0.17–0.21 s for all 29 goods, 5.7–7.3 ms per good, individual 5.4–24 ms" | author's 12 runs: 0.088–0.181 s, 1 of 12 inside; agent's: 0.100–0.274 s, 5 of 12. **Quote the order of magnitude** — a wall-clock timing to two significant figures is a claim about a machine |
| **E8** | X106 | "almost nothing absorbs threshold chatter" | name the three shipped cooldowns: `TRADING_POLICY_COOLDOWN_MONTHS = 12`, `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30`, `TRADE_COMPANY_COOLDOWN = 60` |
| **E9** | X097 | "Nothing routes through the Cape" | false as a universal — **115 ordered pairs** route through it (in-degree 1, out-degree 3). True as intended: no Europe→sink route passes it (verified for `genua`, `english_channel`, `north_sea`). Narrow the quantifier and state the conduit |
| **E10** | X185 | "supply contrast 4–97 across the 29 goods" | **4–97 over the 28 goods with more than one producing node**; `cloves` has a single producer and no contrast to measure. *(The author claimed three such goods; the agent corrected this to one, and the author accepts.)* Both agree the ratio is a weak proxy — the thesis is **sparsity**, carried better by "18 of 80 nodes for spices, 1 for cloves" |
| **E11** | X151 | "the one place the indexing is load-bearing is the fallback branch" | false — the index decides at **any** exact `(DEF, b)` tie. Of 2,670 order-sensitive constructed instances, 2,669 sit on such a tie; the one exception exposed an **undocumented** tiebreak (Phase 1's `min(comps[j], key=(beta[v], v))`). §1.1 documents **two** index tiebreaks; there are **four** — add Phase 1's cluster argmin, the stall promotion's identical form, and the top-k cut's equal-mass enumeration order. On 1444 none of them bite (zero `(DEF,b)` ties on free edges, zero within-cluster β ties, zero tied cluster masses), so no 1444 number moves *from this cause*. See **H1** for the cause that does. |
| **E12** | X091 | the Europe demonstration is described as a *development* edge but `europe.py` scales **wealth** | at ×1.02 the sink sets differ (`wien` present under wealth-scaling, absent under development-scaling) and **at ×1.56 `hangzhou` survives under development-scaling, so "Asia holds none" is false.** Five European provinces with flat goods bonuses break the linearity. Re-run the demonstration on development, or state plainly that wealth was scaled |

---

## F. The verification harness is rebuilt, not patched

**F1.** The agent's audit of `validate_v5.py`: 133 assertion sites — 51 text-presence, 66
self-confirming numeric, 13 genuine re-derivations, 5 tautological (one compares a hardcoded tuple to
itself). **82 of the 83 numeric checks never open the spec document**, so no assertion anywhere
compares a figure *printed in the spec* to a figure *computed from the game*. A mutation test
planting ten factual errors in a spec copy caught **one**, and only as a missing byte string; world
wealth altered to 12,345.67 passed while the same run printed `got=10677.5 exp=10677.5`. None of the
22 refutations was in a position to be caught by it. *Accepted in full by the author.*

**Agreed rebuild:** every numeric check must parse the figure out of the spec text and compare it to
the computed value. The mutation test is the acceptance criterion, not the pass count — a harness
that does not catch ≥ 9 of 10 planted errors is not evidence of anything.

Also to fix: the README credits a "whole-install modifier sweep" to `wealthmodel.py`; the numbers
live only in `q01.py`, the patch script that types them into the spec.

---

## G. The wealth model — DECIDED: option (c)

**The owner has chosen (c): drop the classification table, keep province state.**

**G1 — §1.3 is replaced.** Wealth becomes a function of **development, the trade good, and the
province's current condition**:

```
wealth(p) = TAX_COEFF · base_tax(p) · (1 + state tax modifiers)
          + GP_COEFF · base_production(p) · (1 + state goods modifiers) · price(good(p))
```

**Deleted outright:** the two-test classification rule and its whole table; `gems` +15% tax and
`incense` +10% trade value; the six great projects; the ten `add_permanent_province_modifier`
provinces; the Leviathan gate on `stora_kopparberget_modifier`; the `starting_tier`-versus-later-tier
question; buildings; centres of trade; `production_leader`; the whole-install sweep and the
`wealthmodel.py` claim attached to it. `solver.py` loses `LOCAL_TAX_MOD`, `LOCAL_TV_MOD`, `MON_FLAT`,
`MON_GPMOD`, `MON_TVMOD` and `PERM_FLAT`.

**Kept:** `devastation`, `occupied`, `under_siege`, `prosperity` — province state, not owner state,
and the mechanism by which the map answers to war. Note X040's correction: three of the four enter
`goods_produced` only, **not** `tax_value`, which §1.3 currently gets wrong.

**What this buys.** Five refutations lose their subject (X035, X050, X058, X112, X176) along with
most of systemic findings 2 and 3. The DLC dependency goes. "Owner-agnostic" stops being a property
defended by a rule and a sweep and becomes **true by construction** — every input is a bare attribute
of the place. And wealth becomes linear in development for undamaged provinces, which disposes of
**E12**: scaling development and scaling wealth coincide to 3.55e-15, so §1.6's Europe demonstration
becomes valid as written rather than needing a re-run.

**What this costs, measured.** World wealth 10,677.50 → **10,572.40** (the deleted modifiers are
**0.98%**, over 87 of 2,452 provinces). The aggregate map moves **10 of 159 edges** and the 1444 sinks
become **{`english_channel`, `hangzhou`}**. Per-good: 235 of 4,611 good-edges flip, 14 of 29 sink sets
move, all 29 stay acyclic.

**Two warnings attached to this choice, both agreed:**

1. **The two-sink map returns — do not use it as a justification.** See **A1-trap**. `α_Φ = 1.5` is a
   stipulation under (c) exactly as it is under any other option. The temptation to write "1.5 is
   retained because it reproduces the vanilla-like two-end map" must be refused; that is V213 verbatim.
2. **The 0.98% is measured on the one date when three of the four retained state modifiers are inert.**
   It is not evidence that the deleted apparatus was worth little in general — it is evidence that it
   was worth little *at the start date*. The retained four are precisely the ones whose worth grows.

**Also agreed, independent of this choice:** `GP_COEFF = 0.2` is a shipped file value at
`common/static_modifiers/00_static_modifiers.txt:251` (`provincial_production_size`, localised
"Base Production") — §2.3's claim that neither coefficient is in a file is wrong, and the emitter
should read it rather than hardcode it. `provincial_tax_income` at line 244 carries no tax
coefficient, so `TAX_COEFF = 1.0` genuinely is not in that file and stays a measured constant.

**Consequence for B1–B3:** under (c) the model's only inputs are `base_tax`, `base_production`, the
trade good and province state — and all four start-state defects land in exactly those. The B items
move from "important" to **load-bearing**.

---

## H. The orientation is not a function of the world state alone

**H1 — Phase 2's LP is massively degenerate, and the node/arc ordering selects which optimum you
get.** This is the largest structural finding in the audit and it was found last.

The sub-auditor permuted node labels end-to-end through every phase, 29 goods × 20 relabellings =
**580 runs on 1444**:

| | |
|---|---|
| orientation changed | **580 of 580** |
| ...with the **same** LP support (i.e. a sweep tiebreak decided it) | **0** |
| ...with a **different** LP support (i.e. the LP returned another optimal vertex) | **580** |
| magnitude | **mean 22.1 of 159 edges flip**, max 45; sink set moves by up to 8 nodes |
| objective | identical to **8.9e-16** — every one of them is optimal |

**The author verified this independently by a different route:** permuting only the *arc presentation
order* into `linprog`, holding node labels fixed, changes the optimal support on **10 of 10 goods
tested**, with objective gaps of 0 to 1.8e-15 and symmetric differences of 20–50 arcs.

Consequences, all agreed:

1. **§2.4 item 1's conclusion is right and its stated reason is wrong.** A canonical node order is a
   correctness requirement — but because Phase 2's optimum is degenerate, not because of any
   tiebreak. The spec currently attributes it to the fallback branch (§3.2, T3), which on 1444
   never fires.
2. **22 flips is not a rounding effect.** It is the same magnitude as the razed-China perturbation
   §2.8 presents as a major world event. Same world, different ordering, comparable movement.
3. **§1.6's stability results are conditional on a fixed ordering.** "0 edge flips and 0 sink-set
   changes under ±1% wealth noise" is measured holding arc order constant. The map is stable in the
   world and unstable in its own presentation order, and the document currently reports only the
   first.
4. **§3.13's "LP determinism across machines" is a same-machine concern** the moment node order
   changes — and §2.8's determinism assertions (`retention` identical on 80 of 80 nodes) are
   measuring a fixed ordering rather than determinism of the model.

**Agreed fix:** state the degeneracy plainly as a property of the formulation; make the canonical
order a requirement *of Phase 2's input*, not only of the sweep; re-state every stability figure as
"at fixed node order"; and record that the 580/580 result is HiGHS-specific in detail though not in
kind — any simplex will pick *a* vertex of a degenerate optimal face. If a unique orientation is
wanted independent of ordering, that needs a tie-breaking objective (e.g. lexicographic or a strictly
convex perturbation), which is a design change and is **not** proposed here.

**H2 — two more DRAIN refutations, both on v5.0's own repairs.**

- **X009.** §1.1's fallback-reachability sentence is wrong in both cases: the condition is on the
  **post-peel** balance, not the raw `b`, and the aggregate case needs uniform `Σ wealth^α_Φ` per
  node, not uniform wealth.
- **X125.** §1.1 says that on the fallback branch "the candidates are usually all zero-wealth, the
  wealth key ties, and the index decides". **T3 — the spec's own worked example — has wealths 3, 2
  and 1.** The general claim contradicts the example offered to demonstrate it.
- **X013 / X145.** §3.2 claim 1 states the sink-set equality "on a map where Phase 0 is a no-op and
  no fallback fires" and then names T2 as a counterexample. **T2 satisfies both conditions.** The
  conditions v5.0 added look like they establish the claim and do not; the honest form is that the
  equality is a 1444 measurement with no conditions attached that make it more than that.

---

## Scope note

This batch covers all 22 refutations and all 8 systemic findings. The **39 PARTIAL** gradings are
not individually itemised here; each narrows a claim to what is proved or measured, and they are
folded per their individual reasons during drafting. That is the same treatment v4.0 gave v3.0's
partials — and it is worth recording that this is the step where v4.0's errors were introduced, so
the rebuilt harness (F1) is applied to them as well as to the items above.
