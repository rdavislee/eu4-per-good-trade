# Validation — Per-Good Trade Network Spec v6.0

Grades every row of `claims-v6.md` (Y001–Y188) against primary sources: the 1.37.5.0 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (Leviathan present), the
vanilla save `save games\VANILLA_start.eu4`, `per-good-trade-spec.md` itself, the shipped scripts in
`scripts\`, and the v1–v5 trees. **Nothing is inherited.** No status here was taken from
`validation-v5.md`, from `preconfirm-round*.md`, or from the three prior-round validation files that
sit in `scripts\`; every figure below was re-derived this session. Where the spec quotes a file, the
file was opened.

## Summary

| Status | Count |
|---|---|
| CONFIRMED | 168 |
| PARTIAL | 19 |
| REFUTED | 1 |
| UNVERIFIABLE | 0 |
| **Total** | **188** |

**REFUTED:** Y134.
**PARTIAL:** Y008, Y010, Y015, Y016, Y047, Y080, Y083, Y084, Y086, Y092, Y100, Y106, Y108, Y117,
Y129, Y132, Y143, Y168, Y178.

---

## Instruments, and what validating them showed

Every model measurement below runs through one of two instruments. Both were validated before use.

**1. The shipped reference implementation** (`scripts/solver.py` + `scripts/drain.py`).
Its two data caches were checked against the install rather than trusted:

- `nodes.json` vs `common/tradenodes/00_tradenodes.txt`: **80 nodes, node order identical, 0 member
  mismatches, 0 outgoing mismatches**, 159 directed `outgoing` links = 159 distinct undirected
  edges, `end=yes` on exactly `genua`, `venice`, `english_channel` (vanilla's three authored ends),
  `inland=yes` on 26 nodes.
- `prov1444.json` vs a fresh `provinces.py` parse of `history/provinces/`: **3,923 provinces,
  0 differences** on `owner`, `trade_goods`, `base_tax`, `base_production`, `is_city`.
- `measure6.py` was re-run from scratch: it reproduces the shipped `measure6.out` **byte for byte**
  (60 labelled figures). So `measure6.out` is a faithful record of what the script computes, and
  every figure attributed to `measure6.py` below was re-computed rather than read off that file.

**2. An independent five-phase reimplementation** (`../v5-owner-agnostic/scripts/_audit_b_drain.py`),
written from the spec text and parameterised by node order, driven by my own permutation harness.
Validated against `drain.py` on the identity permutation: **159 of 159 edges agree, sink set matches
(`english_channel`, `hangzhou`), core 80, 2 promotions, 0 fallbacks, 80 free edges**, and its LP
objective **0.7122759778293255** is bit-identical to `drain.py`'s `flowop` cost. This is the
instrument the relabelling claims are graded on, because the alternatives fail one-sidedly —
`drain.py`'s `sweep_priority(pid=…)` hook re-keys only the sweep and reports **0 flips** across 2
index permutations × 29 goods (reproduced via `final.py`, item V035), so a test built on it would
report "no effect" for the wrong reason.

**Instrument gap found.** `relabel6.py` — the script §1.6 and §2.4 name for the relabelling figures —
does **not** compute the LP objective at all. It prints flips, sink sets and end-holder counts and
nothing else. The "LP objective identical to within 4.44e-16" of Y086/Y132 is therefore not produced
by the script it is attributed to; I measured it with my own harness (see Y086).

**Two documentation facts.** `scripts\` contains **no README** (the audit brief expected one), and it
still carries `wealthmodel.py`, v5.0's whole-install-sweep model, which nothing in the v6.0 chain
imports (`grep -l wealthmodel *.py` → no hits).

---

# §0 — Front matter

## Y001 — v6.0's substantive change is §1.3: wealth reads development, trade good and condition, and nothing else
**Status:** CONFIRMED
**Method:** read `per-good-trade-spec.md` lines 14–27 and §1.3 lines 186–332; read
`scripts/solver.py` `province_table()` and the wealth expression.
**Evidence:** the solver's wealth is
`TAX_COEFF*base_tax*(1+tmod) + max(0, GP_COEFF*base_production*(1+gmod))*price`, where `gmod` comes
only from `STATE_GOODS_MOD` (the four province-condition static modifiers) and `tmod` only from
`STATE_TAX_MOD`. No owner, autonomy, efficiency, idea, estate, building, great-project, trade-good
or DLC term appears anywhere in the chain. Owner-agnosticism is a property of the expression, not of
a rule applied to it.

## Y002 — the two-test classifier, everything it governed, and the whole-install sweep are deleted
**Status:** CONFIRMED
**Method:** compared v5.0 §1.3's classification table (quoted in `changes-v6.md` entry 3) against
v6.0 §1.3; grepped `scripts/*.py` for the sweep's data structures.
**Evidence:** the table, the great-project enumeration, the ten permanent modifiers, the 361
centres of trade, `production_leader`, the buildings row, the terrain/climate row and the
Leviathan-conditionality paragraph are all absent from v6.0. `LOCAL_TAX_MOD` / `PERM_FLAT` /
`MON_FLAT` appear in no script the solver chain imports (only in `preconfirm3.py`, an audit file).
`verify6.py`'s absence check for `exactly **two** modifiers enter wealth` passes.
*Note:* v5.0's `wealthmodel.py` is still physically present in `scripts/`, unreferenced.

## Y003 — the deleted apparatus is dated by version (two-test = v4.0, structural rule = v3.0, sweep = v5.0)
**Status:** CONFIRMED
**Method:** grepped each prior spec for the apparatus language.
**Evidence:** v3.0 `per-good-trade-spec.md:162-167` — "The engine's own data model draws the line for
us: a trade good's `province = { … }` block is province-scoped and its `modifier = { … }` block is
country-scoped" (a structural rule). v4.0 `:184-191` is the first "Two tests, and a modifier must
pass both". "whole install"/"whole-install" has **zero** hits in v2, v3 and v4 and 4 hits in v5.0
(`:17, 201, 628, 1275`), the first being `:201` "The tests are applied to the whole install, not to
one file." One qualification: v5.0 itself credits v4.0 with *stating* the file-agnostic principle,
so "v5.0's alone" is true of the sweep, not of the idea behind it.

## Y004 — the apparatus was worth 105.30 ducats: 0.98% of 10,712.70 with it, 0.99% of 10,607.40 without
**Status:** CONFIRMED
**Method:** re-ran `measure6.py` for the (c) field, then reconstructed v5.0's apparatus on top of it
from `v5-owner-agnostic/scripts/solver.py`'s own tables (`gems` +15% tax, `incense` +10% trade
value, `MON_FLAT`, `MON_GPMOD`, `MON_TVMOD`, `PERM_FLAT`) and summed both fields. Two orderings of
the flat/percentage composition were tried.
**Evidence:** field without = **10,607.40**; field with = **10,712.70** under both orderings;
difference **105.30**; 105.30/10,712.70 = **0.9829%** → 0.98%; 105.30/10,607.40 = **0.9927%** →
0.99%. All four figures exact.

## Y005 — the classification was wrong in both audits that examined it, and passed by v4.0's own harness
**Status:** CONFIRMED
**Method:** read the W041 entry in `v3-owner-agnostic/validation-v3.md`, the X035 entry in
`v5-owner-agnostic/validation-v5.md`, and `v4-owner-agnostic/scripts/validate_v4.py`.
**Evidence:** `validation-v3.md:37` lists W041 among **REFUTED (10)**; its entry at `:68` finds a
fourth trade-good modifier (`chinaware`) and `bonus_from_merchant_republics` as a place-scoped
income modifier the rule cannot see. `validation-v5.md:42` grades **X035 REFUTED** — the enumeration
misses `provincial_production_size` and two `province_triggered_modifiers`, and counts five
province-state static modifiers where there are four. v4.0 shipped 203 assertions, 0 failed
(`validation-v4.md:9-18`) and graded **W041 CONFIRMED**; `validate_v4.py:44` loads only
`common/tradegoods/00_tradegoods.txt`, which is exactly the scope X035 refuted.

## Y006 — three start-state reads corrected in the same pass
**Status:** CONFIRMED
**Method:** each of the three verified independently against the save and the history files (see
Y052–Y053, Y059–Y060, Y061).
**Evidence:** `on_startup` devastation — 11 provinces carry non-zero `devastation` in the save and
no history file sets it. Dated `add_base_*` accumulation — province 1 has `base_tax = 5` undated
plus `add_base_tax = 1` at 1436.4.28 and the save holds 6. `is_city` — 20 owned provinces lack
`is_city = yes` in history and the save gives all 2,472 owned provinces `is_city=yes`.

## Y007 — Phase 2's min-cost flow is degenerate, so presentation order selects which optimum is returned
**Status:** CONFIRMED
**Method:** 400 node relabellings (four seeds × 100) through the validated five-phase instrument,
recording the LP support (the Phase-2 flow-arc set, mapped back through the permutation) and the LP
objective for each.
**Evidence:** the LP support differed from the shipped support in **400 of 400** relabellings while
the objective stayed at 0.7122759778293255 to within 5.55e-16 — many distinct supports at one
optimal cost, which is degeneracy. Independently, `final.py` V035 shows a *sweep-only* index
permutation changes nothing (0 flips, 29 goods × 2 permutations), so the sensitivity is Phase 2's
and not the sweep's.

## Y008 — prose convention: no empirical absolutes
**Status:** PARTIAL
**Method:** read §0's statement of the convention, then swept the spec for surviving superlatives,
universal quantifiers and unscoped thresholds.
**Evidence:** the convention is coherent and visibly applied — the widest-band justification is
withdrawn, the graveyard is de-quantified, the Cape universal is narrowed to "No Europe→sink route",
the caravan and node-set thresholds are re-stated as observations, and `TAX_COEFF` is carefully
scoped to "in no file that has been found". But the document still asserts absolutes in text the
pass did not open. §3.6: "Acyclicity is enforced because the engine **provably** cannot survive its
absence" — a universal about the engine resting on three launches of one build. §3.9 and §3.15:
"the most self-coherent aggregate measured", an unscoped superlative. §3.5: "At vanilla base prices
**nothing** sits below the 2.0 anchor" and "the minimum tradeable base price is exactly 2.0".
**Should say:** the convention holds for every passage v6.0 edited and fails in §3.6, §3.9 and
§3.15 — the same "patch what you touch" defect `changes-v6.md` diagnoses for round one.

## Y009 — prose convention: no maintained figures for any rejected operator, covering §3.15
**Status:** CONFIRMED
**Method:** grepped the spec for every figure the graveyard previously carried.
**Evidence:** `60.3` → 0 hits, `62.7` → 0, `88.4` → 0, `97 of 159` → 0, `13 end nodes` → 0,
`68/159` → 0. §3.15's five rejected-operator entries (`Φ_ord`, gravity kernels, v1 Laplacian, RANK,
seeded basins) carry design arguments and no operator scores. The only number left in §3.15's
Laplacian entry is "`cloves` has a single producer", which is a supply-sparsity fact about the game
data rather than a score for the rejected operator.

## Y010 — those numbers were re-measured and re-refuted in three successive audits, and no rejection argument depends on them
**Status:** PARTIAL
**Method:** traced each figure family through `validation-v2.md`, `validation-v3.md`,
`validation-v4.md` and `validation-v5.md`.
**Evidence:** the three families behave differently. `Φ_ord` self-coherence: re-measured in v2
(V062 REFUTED), v3 (W061–W063 **CONFIRMED**) and v5 (X075 PARTIAL / X076 **CONFIRMED**) — three
audits, but **not successive**, because `validation-v4.md` contains no occurrence of `Φ_ord` or any
coherence percentage. Gravity-kernel agreement: **four** audits (V225, W190, v4's W190
text-presence check, X190). v1 Laplacian contrast: three successive (v3, v4, v5), ending in X185
REFUTED. So "re-refuted" also overstates — two of the re-measurements CONFIRMED the figure. And the
second clause fails historically: `validation-v3.md:150-156` calls the supply-contrast ratio §3.2's
"**load-bearing**" premise, and `validation-v4.md:234-238` had to **replace** that premise.
**Should say:** the figures were re-measured in three or four audits depending on the family, some
of those re-measurements confirmed rather than refuted them, and the v1 Laplacian rejection argument
*did* depend on one of them until v4.0 replaced the premise.

## Y011 — a load-bearing comparison is stated as a direction, not a maintained figure
**Status:** CONFIRMED
**Method:** located both quoted phrases in the spec.
**Evidence:** §3.9 line 1364 — "scores **higher** than `Φ_w` on self-coherence" — and line 1367 —
"the end count does not concentrate as demand concentrates". Neither carries a percentage. §1.6's
counterpart at line 467 likewise: "The superseded marking-order aggregate scored higher on that
measure".

## Y012 — every graded claim from validation-v5.md (22 refuted, 39 partial, 1 unverifiable) is folded through, and fixes-agreed.md maps each one
**Status:** CONFIRMED
**Method:** counted the status column of `v5-owner-agnostic/validation-v5.md` and diffed the ID set
against `fixes-agreed.md`'s mapping table in both directions.
**Evidence:** `validation-v5.md:25-31` gives 134 CONFIRMED / 22 REFUTED / 39 PARTIAL / 1
UNVERIFIABLE over 196. The extracted open set is exactly 62 IDs; `fixes-agreed.md` §5 has exactly
62 rows; the set difference is **empty in both directions**. No refuted, partial or unverifiable X
ID is unmapped.

## Y013 — verify6.py reads figures out of the document text and fails when they disagree with a computed value
**Status:** CONFIRMED
**Method:** read `verify6.py` in full; ran it on the spec; ran `mutate6.py` on the spec.
**Evidence:** `run_spec()` builds every needle from `measure6.OUT` (`shows(doc, …, O[...])`) and
`every_site()` compares a quantity across phrasings, so a stale figure in the document fails. On the
spec: **29 checks, 0 failed**. `mutate6.py` plants 12 errors one at a time and the verifier catches
**12 of 12**, so the failure path works.
*Two notes.* The checklist path `run()` still carries **typed** literals (5703, 6320, 1.70, 3.51,
13.40, 132, 27.00, 8), several now stale — so `verify6.py` asserts the widest band is `1.70` wide
over `[3.51, 5.21]` when checking `fixes-agreed.md` and `1.71` over `[3.50, 5.21]` when checking the
spec, i.e. the harness holds two values for one quantity. Run against `fixes-agreed.md` it reports
**21 checks, 5 failed**, because that document still carries the pre-round-two field (10,594.70,
5,703, 90.2%).

## Y014 — it does not cover every figure the document prints; under half are guarded, and the remainder are not all covered elsewhere
**Status:** CONFIRMED
**Method:** counted the numeric tokens the spec prints, counted the numeric slots `verify6.py` pins,
and ran `coverage6.py`.
**Evidence:** the spec contains **1,148 numeric tokens, 303 distinct** (483 of them decimal-bearing,
163 distinct; 70 percentages, 41 distinct). `verify6.py`'s spec pass pins roughly 38 numeric slots
across its 29 checks. `coverage6.py` finds only 9 computed figures uniquely locatable in the prose,
protects 8 of them, and lists 25 further computed figures it cannot aim at and therefore does not
score. Under half is a large understatement of the gap, so the claim holds in the direction it
asserts.

## Y015 — a script is named about a dozen times against roughly three times that many unguarded figures
**Status:** PARTIAL
**Method:** counted `.py` citations in the spec and compared against the guarded/unguarded figure
counts from Y014.
**Evidence:** 18 `.py` citations across 9 script names; the measurement attributions alone
(`measure6.py` 7, `relabel6.py` 2, `europe.py` 1, `drain.py` 1, `toys.py` 1) total **12** — "about a
dozen" is right. But unguarded figures are not ~36: with 303 distinct numeric tokens and ~38 pinned,
roughly **265** are unguarded, about **22×** the attribution count rather than 3×.
**Should say:** a script is named about a dozen times against roughly twenty times that many
unguarded figures — or drop the ratio, since the document offers no definition of "figure" that
makes 3× come out.

## Y016 — coverage6.py measures that honestly by corrupting each spec-printed figure whether the harness looks at it or not
**Status:** PARTIAL
**Method:** read `coverage6.py` line by line and ran it (it writes and deletes `_cov.md`; the spec's
md5 was unchanged afterwards).
**Evidence:** the "whether the harness looks at it or not" half is true — the script iterates
`measure6.out` independently of `verify6.py`'s check list, and `verify6.py:150-155` carries a block
commented "figures coverage6.py reported unguarded", direct evidence it found real gaps. The
denominator half is not. The candidate set is `measure6.out`'s 60 keys, filtered to numeric
renderings with `1.0 ≤ |v| ≤ 1e7` (which silently drops `largest |b_w|` = 0.0225 and `GP_COEFF` =
0.2, both of which `verify6.py` does check) and then to renderings occurring **exactly once** in the
spec. That leaves **9** targets; 25 further figures are explicitly unscored. My run: **8 of 9
protected (89%)**, the miss being `ordered pairs connected`.
**Should say:** it corrupts each *uniquely locatable* figure `measure6.py` computes — 9 of 60 — and
lists the rest as unscored; the denominator is not "what the document asserts".

## Y017 — mutate6.py reports a higher score and is not coverage: it plants errors only in figures verify6.py already checks
**Status:** CONFIRMED
**Method:** read `mutate6.py`'s `_spec_mutations()`, matched each of its twelve anchors against
`verify6.py`'s `run_spec()` needles, and ran both scripts.
**Evidence:** all twelve anchors are substrings of, or identical to, needles `run_spec()` already
asserts (world wealth, counted provinces, both coherence figures, sinks-per-good mean, connected
pairs, largest `|b_w|`, α band, European provinces, coal flips, coal delta, price census).
`mutate6.py` scores **12 of 12** against `coverage6.py`'s **8 of 9 (89%)** — higher, as claimed, and
guaranteed by construction. *Incidental:* the script's docstring and its `>= 9` gate still say "ten"
while it runs twelve on the spec.

---

# §1.1 — Trade direction

## Y018 — the fallback fires only when every candidate is support-isolated with zero post-peel balance
**Status:** CONFIRMED (derivation)
**Method:** checked the argument against `drain.py`'s `sweep_priority` and the stall handler.
**Evidence:** `ready(u)` is true whenever `len(outs[u]) > 0`, so any candidate holding a flow
out-arc is ready and cannot be at a stall; `terminals` collects gated nodes with `len(outs)==0 and
inflow > ZERO_TOL`, which take the promotion branch. The fallback is therefore reached only when
every gated node has no flow out-arc and no inflow — support-isolated. Flow conservation then forces
β = 0 at such a node, because a node with β ≠ 0 must carry flow on some incident arc.

## Y019 — the key reads Phase 0's folded balance, so a map with non-zero raw balances can still reach the branch
**Status:** CONFIRMED (derivation, plus a construction)
**Method:** read `phase0` and `sweep_priority` (the key is `(-DEF[v], beta[v], pid[v])` on the
post-fold `beta`); then built a case through the five-phase instrument.
**Evidence:** triangle A,B,C with raw balances +1, +2, +3 and a pendant on each carrying −1, −2, −3.
Phase 0 peels all three pendants, folded β = 0 at all three core nodes, and the run reports
`fallbacks=['A']` with sinks `{a, b, c}` — the fallback branch reached from strictly non-zero raw
balances.

## Y020 — on a connected core the folded balance must vanish across the core; for the aggregate that needs equal node Σ wealth^α_Φ, which uniform per-province wealth does not give
**Status:** CONFIRMED (derivation, plus a construction)
**Method:** derived the condition, then tested the contrapositive on a connected core with a
zero-balance region beside a flow-carrying region.
**Evidence:** at the first stall, `gated` is the set of flow-terminal nodes; if any flow exists at
all the flow DAG has a sink with `inflow > 0`, which takes the promotion branch — so a fallback at
the first stall requires no flow, i.e. β = 0 across the core. Constructed check: triangle A,B,C with
β = 0 joined by an edge to a 4-cycle carrying +1/−1. The run reports `S=['F'] promos=[]
fallbacks=[]` — the zero-balance triangle is absorbed through free edges and the fallback never
fires. The aggregate half follows from `b_w = 1/N − c_w`: b_w vanishes iff every node's
`Σ wealth^α_Φ` is equal, which needs equal node sums, not equal provinces (Y021).

## Y021 — ⚑ nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes unequal node sums
**Status:** CONFIRMED
**Method:** counted, per trade node, the provinces that have an owner at 1444.11.11 and appear in
that node's `members` list.
**Evidence:** minimum **0** (`cape_of_good_hope`), maximum **72** (`mexico`); the 80 counts sum to
2,472. Raw `members` counts run 20–77 and disagree sharply with the counted counts
(`carribean_trade` 62 members → 1 counted; `california` 74 → 9).

## Y022 — where the wealth key ties, the node index decides
**Status:** CONFIRMED (derivation)
**Method:** read the fallback line in both sweeps.
**Evidence:** `max(gated, key=lambda v: (NODEW[v], -v))` in `drain.py` (`sweep` and
`sweep_priority`) — on equal `NODEW` the maximum of `-v` picks the lowest index. v5.0's additional
claim that the tied candidates are usually all zero-wealth is absent from v6.0, correctly: T3's
constructed fallback has wealths 3, 2, 1 and needs no tie at all.

## Y023 — §2.8's containment set includes the fallbacks because of T3, not the wealth tie; and that is not why §2.4 needs a canonical node order
**Status:** CONFIRMED
**Method:** ran `scripts/toys.py`; compared against the Phase-2 degeneracy measurement.
**Evidence:** T3 reproduces exactly — triangle with b = 0 everywhere and wealths 3, 2, 1, no
selection, no flow, fallback promotes A, free edges orient B→A and C→A, actual sinks `{A}`, formula
set empty, and `sink inside {selected} ∪ {promoted}: False / inside ∪ {fallbacks}: True`. The wealth
values are distinct, so no tie is involved. The canonical-order requirement is Phase 2's: the LP
support changed in 400 of 400 relabellings while free-edge key ties stayed at zero.

## Y024 — on 1444 fallback and pendant cases are empty and the sink set is exactly {selected ∩ flow-terminal} ∪ {promoted}: 29/29, 1–8 sinks, mean 3.72, zero fallbacks
**Status:** CONFIRMED
**Method:** rebuilt the per-good fields from the solver (α(g) = clamp((price/2), 0.2, 3), ε = 0) and
ran DRAIN on all 29 live goods, comparing the actual sink set against
`(S0 ∩ flow-terminal) ∪ promotions` per good.
**Evidence:** live goods 29; sinks/good min **1**, max **8**, mean **3.7241** → 3.72; acyclic
**29/29**; fallbacks fired **0**; Phase 0 peels **0** on the vanilla map; the equality holds on
**29 of 29** goods.

## Y025 — that equality is a measurement on this input, not a theorem, and "Phase 0 a no-op and no fallback firing" is not sufficient because T2 satisfies both
**Status:** CONFIRMED
**Method:** ran `scripts/toys.py`, checking T2's premises.
**Evidence:** T2 — five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2) with chord w–S1 — has minimum degree
2 (Phase 0 a no-op) and `fallbacks=[]`, yet actual sinks are `{u2}` against the formula's
`{u1, u2}`. Both attached conditions are satisfied and the equality still breaks.

---

# §1.3 — Demand

## Y026 — wealth reads three things about the province
**Status:** CONFIRMED
**Method:** read the wealth expression in `solver.py` against §1.3's statement.
**Evidence:** the only inputs are `base_tax`, `base_production`, `trade_goods` (via `PRICES`) and the province-condition modifier from `ON_STARTUP_DEVASTATION`. Nothing else is read.

## Y027 — two provinces with the same development, trade good and condition have the same wealth whoever owns them
**Status:** CONFIRMED
**Method:** checked the expression for owner dependence; compared v5.0's wording as quoted in `changes-v6.md` entry 2.
**Evidence:** wealth is a function of (base_tax, base_production, good, devastation level) only, so it is constant on that equivalence class. v5.0's removed text reads "the same **terrain**, development and trade good", and terrain was never an input to v5.0's wealth either — the correction also drops a term that was never there.

## Y028 — owner-agnosticism is true by construction, not by a rule that has to be policed
**Status:** CONFIRMED (stipulation; the stated rationale holds)
**Method:** checked internal consistency, then checked the stated reason.
**Evidence:** the stipulation is consistent with Y026's expression, and its rationale — the classifier was "a large surface to keep correct and was wrong in both independent audits that examined it" — is itself confirmed at Y005 (W041 REFUTED, X035 REFUTED, v4.0's own harness passing it).

## Y029 — base_tax, base_production and the trade good are bare attributes of the place
**Status:** CONFIRMED (derivation)
**Method:** read the province-history schema and the save's province records.
**Evidence:** all three are scalar or string fields of the province record with no country reference; they are set in `history/provinces/*.txt` and carried in the save's province block. No classification question arises because there is no modifier to classify.

## Y030 — what this gives up: gems' local_tax_modifier, incense' trade_value_modifier, great projects, permanent province modifiers, and the DLC state they depended on
**Status:** CONFIRMED
**Method:** compared v5.0's inputs (from its own `solver.py`) against v6.0's; confirmed the DLC gate in the install.
**Evidence:** v5.0 read `{"gems": 0.15}` as `local_tax_modifier`, `{"incense": 0.10}` as `trade_value_modifier`, five monument flat bonuses, one monument goods modifier, four monument trade-value modifiers and ten permanent province modifiers. None appears in v6.0's chain. The DLC dependence was real: `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = 5.0` on province 8 — the same province `falun_copper_mine` covers at 3.0.

## Y031 — the apparatus covered 89 of the 2,472 counted provinces: 43 gems + 31 incense + 16 great-project/permanent-modifier, less province 542
**Status:** CONFIRMED
**Method:** counted goods over the counted set (using the engine's rolled good where history says `unknown`) and intersected with v5.0's own 16-province modifier set.
**Evidence:** gems **43**, incense **31**, no overlap between them; the great-project and permanent-modifier provinces are {6, 8, 262, 362, 363, 370, 371, 387, 542, 684, 1821, 1822, 2145, 2151, 2316, 4316} = **16**; the union over counted provinces is **89**; the single overlap is **542** (Golconda is both `gems` and `diamond_mines_of_golconda_modifier`). 43 + 31 + 16 − 1 = 89, and the reconstructed field differs from the v6.0 field by exactly 105.30 ducats over those 89 provinces (Y004).
*One qualification, recorded rather than scored against the claim:* the ten permanent modifiers are the complete set — a sweep of every undated `add_permanent_province_modifier` resolved against all modifier definitions yields exactly those ten — but the six great projects are the subset with an **empty** `can_use_modifiers_trigger`. A reading of the two-test rule that admitted *satisfied* triggers would add 104 (`duomo_milano`, `local_tax_modifier = 0.25`, Christian trigger satisfied) and 852 (`tenochtitlan` tier 2, `trade_goods_size_modifier = 0.33`, Central American trigger satisfied), giving 18 and a total of 91/89. That is a defect in v5.0's classifier rather than in v6.0's description of what it deleted: the claim is about the apparatus as it existed, and 89 is what that apparatus covered.

## Y032 — the count is 87 under the withdrawn is_city filter, and 89 rather than 88 because province 4856 rolled incense
**Status:** CONFIRMED
**Method:** recomputed the apparatus union under the `is_city = yes` filter; checked 4856's history and the save.
**Evidence:** counted-with-`is_city` = 2,452, and the apparatus union over that set = **87** — the two lost are 1207 (Ogaden) and 4856 (Barunggam), both incense, both lacking `is_city = yes`. Province 4856's history carries `trade_goods = unknown` and the save gives it `incense`. History-only incense over the counted set is **30**, so without the roll the apparatus would be 88.

## Y033 — goods_produced = GP_COEFF x base_production x (1 + sum of province-state goods modifiers), no flat-goods-bonus term
**Status:** CONFIRMED
**Method:** read the formula block at spec lines 208–213 against `solver.py`.
**Evidence:** `gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))` — identical in form, with no additive term. There is no flat table in `province_table()`.

## Y034 — trade_value = goods_produced x price, ducats per year, with no trade-value-modifier term
**Status:** CONFIRMED
**Method:** same comparison.
**Evidence:** `prod_income = gp * price`. No `(1 + trade_value_modifier)` factor anywhere in the chain; v5.0's `LOCAL_TV_MOD` and `MON_TVMOD` are gone.

## Y035 — tax_value = TAX_COEFF x base_tax x (1 + sum of province-state tax modifiers), ducats per year
**Status:** CONFIRMED
**Method:** same comparison; checked the save for live tax modifiers.
**Evidence:** `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)` with `tmod` drawn only from `STATE_TAX_MOD = {"occupied": -0.5}`, which is 0 for every province at 1444 — the save carries zero `occupied` records.

## Y036 — GP_COEFF is a shipped file value: provincial_production_size = { trade_goods_size = 0.2 ... }, localised "Base Production"
**Status:** CONFIRMED
**Method:** opened `common/static_modifiers/00_static_modifiers.txt` and grepped `localisation/`.
**Evidence:** lines 251–254 hold `provincial_production_size = { trade_goods_size = 0.2  ship_recruit_speed = -0.01 }`, and `localisation/EU4_l_english.yml:815` holds `provincial_production_size:0 "Base Production"`. The block's second key is covered by the claim's ellipsis. `solver.py` reads 0.2 out of this block at import time rather than carrying it.

## Y037 — it is therefore moddable and is read at runtime, not hardcoded
**Status:** CONFIRMED
**Method:** read `solver._read_gp_coeff()` and §2.3's emitter instruction.
**Evidence:** `_read_gp_coeff()` opens the file, regexes the block and raises if the block or the key is missing, so a mod or patch changing 0.2 changes the model's coefficient. §2.3 instructs the emitter to read it. The shipped DLL does not exist, so the runtime half is a design commitment rather than an observation — which is how §2.3 states it.

## Y038 — TAX_COEFF is in no file that has been found
**Status:** CONFIRMED
**Method:** grepped `common/defines.lua`, `common/defines/` and `common/static_modifiers/00_static_modifiers.txt` for any per-base_tax income coefficient.
**Evidence:** `TAX_COEFF` appears nowhere in the install. `common/defines/` holds only `00_dummy.lua` and four difficulty files, with no tax key. Every TAX define in `defines.lua` is unrelated — `PS_RAISE_WAR_TAXES = 2`, `ENFORCE_CULTURE_TAX_MULTIPLIER = 2`, `SCUTAGE_TAX_FRACTION = 0.5`, `BASE_TAX_COST_MODIFIER = 0.5`, `FLAT_TAX_AMOUNT = 4`. The sibling static-modifier block `provincial_tax_income` grants recruit-speed, build-time and institution-spread keys and no income key at all.

## Y039 — the tax tooltip reads Base: trunc(base_tax x 0.0833333) (Yearly base_tax); twelve times the displayed figure would give 5.88 and 1.92
**Status:** CONFIRMED
**Method:** checked the schema's arithmetic against both quoted observations. The tooltip readings are prior in-game observations; only a running game could re-take them, and I did not.
**Evidence:** trunc(6 x 0.0833333) = trunc(0.4999998) = 0.49 and trunc(2 x 0.0833333) = trunc(0.1666666) = 0.16, matching the observed `Base: 0.49 (Yearly 6.00)` and `Base: 0.16 (Yearly 2.00)`. The rejected reading gives 12 x 0.49 = 5.88 and 12 x 0.16 = 1.92, neither of which is the displayed parenthetical. The schema is exact on both data points; the readings are inherited.

## Y040 — v4.0 and v5.0 wrote Base: X (Yearly 12·X), false on both data points; v3.0 carries neither that schema nor the 0.6125 arithmetic
**Status:** CONFIRMED
**Method:** grepped v2–v5 specs for "Yearly 12" and for "0.6125".
**Evidence:** the schema appears at v4.0 line 163 and v5.0 line 170, verbatim in both, and nowhere in v2 or v3. v3.0 line 149 carries only the instance ("`Base: 0.49 (Yearly 6.00)` for a province with `base_tax = 6`"). "0.6125" has hits only at v4.0 line 178 and v5.0 line 185; v3.0 lines 157–158 write the truncation-consistent "giving 0.61". The attribution is correct for both halves.

## Y041 — the monthly production tooltip is consistent with the same relation on one observation, 3.52 to +0.29, fixing the divisor only to within (11.73, 12.14]
**Status:** CONFIRMED
**Method:** solved the truncation interval from the single observation. Re-taking the reading needs a running game.
**Evidence:** trunc to 2dp of 3.52/d = 0.29 requires 0.29 <= 3.52/d < 0.30, i.e. 3.52/0.30 < d <= 3.52/0.29, i.e. 11.7333 < d <= 12.1379 — **(11.73, 12.14]** exactly as printed, open at the low end. That open lower bound is what v5.0's `[12.00, 12.14]` got wrong.

## Y042 — both monthly figures being the annual value over twelve is what lets the annual forms add, and the tax pair establishes it at two development levels
**Status:** CONFIRMED (derivation)
**Method:** checked the argument against Y039 and Y041.
**Evidence:** the tax pair fixes the relation at `base_tax` 2 and 6 — two levels — and the production reading is consistent with the same divisor to within (11.73, 12.14]. With both monthly displays being annual/12, the annual `tax_value` and `trade_value` share a basis and add without conversion, which is exactly what `solver.py` does.

## Y043 — Garnatah: base_tax 6 at 125.0% displays 0.49 then 0.62; the engine multiplies the untruncated monthly value
**Status:** CONFIRMED
**Method:** checked both arithmetic branches. The reading is a prior in-game observation.
**Evidence:** multiplying the *displayed* figure gives 0.49 x 1.25 = 0.6125, which truncates to **0.61**, not 0.62. Multiplying the untruncated monthly gives 6 x 0.0833333 = 0.4999998, x 1.25 = 0.62499975, truncating to **0.62**. Only the second reading reproduces the observation, and it is consistent with §2.3's truncation rule.

## Y044 — the example establishes the ordering and nothing finer
**Status:** CONFIRMED (derivation)
**Method:** checked what a two-number observation can and cannot fix.
**Evidence:** one base figure and one post-percentage figure fix the order of the two operations — development-derived base first, percentage second — and nothing about how multiple percentages combine, whether flats precede percentages, or where truncation falls for other keys. The stated limit is the honest one.

## Y045 — v4.0 and v5.0 read this as 0.49 x 1.25 = 0.6125 shown as 0.62, which requires rounding while §2.3 requires truncation
**Status:** CONFIRMED
**Method:** quoted both versions and each document's own §2.3 rule.
**Evidence:** v4.0 lines 177–178 and v5.0 lines 184–185, identical: "giving 0.6125, which the province window shows as 0.62". Both documents' §2.3 tables state "The displayed monthly is the truncation of `base_tax x 0.083333`" (v4.0 line 624, v5.0 line 724, v6.0 line 857). Truncating 0.6125 gives 0.61, so the two statements cannot both hold.

## Y046 — flat goods bonuses would add before the price multiply, but under §1.3 no source grants one, so the ordering is exercised by no province in the model
**Status:** CONFIRMED
**Method:** searched `solver.py` for any additive goods term; read §1.3's modifier set.
**Evidence:** `province_table()` contains no flat table and no additive term inside the `gp` expression; `STATE_GOODS_MOD` holds only percentage keys. So no province in the model carries an extra flat bonus and the stated ordering is never exercised, exactly as claimed.
*One precision:* GP_COEFF itself enters the engine through the same additive key (`provincial_production_size = { trade_goods_size = 0.2 }`), so the engine's additive block is not empty — it holds the base term the model computes as GP_COEFF x base_production. "No source grants one" is true of *additional* flat bonuses only.

## Y047 — province condition is the one thing besides development and the good that wealth reads: four static modifiers, all read from 00_static_modifiers.txt
**Status:** PARTIAL
**Method:** enumerated every block in `common/static_modifiers/00_static_modifiers.txt` granting `trade_goods_size`, `trade_goods_size_modifier`, `local_tax_modifier` or `trade_value_modifier`, then checked the save for which of them are live at 1444.
**Evidence:** the four named modifiers are all in that file with the stated grants, and the claim is true of the model as implemented. But the file grants a wealth key in **25** blocks, and at least three of the others describe province state rather than owner state: `unrest` (`local_tax_modifier = -0.02`), `expanded_infrastructure` (`local_tax_modifier = 0.1` and `trade_goods_size_modifier = 0.05`) and `native_assimilation` (`trade_goods_size = 0.05`). **`unrest` is live on 21 counted provinces at the 1444 start** — the save carries a non-zero `unrest` field on 21 records — so the model omits a province-state tax modifier that is biting on the start date. That is structurally the same defect the eleven devastated provinces were.
**Sizing it, and the scaling question.** The 21 provinces carry unrest **4.834 to 14.834** (one at 4.834, three at 7.834, six at 9.834, eleven at 14.834): 331, 418, 419, 1071, 1074, 1075, 1076, 1227, 1966, 2205, 2305, 2427, 2433, 2441, 2771, 2772, 4292, 4688, 4689, 4690, 4745. Applied per point of unrest the modifier costs **12.23 ducats, 0.1153% of world wealth**, worst at pid 1075 (unrest 14.834, `base_tax` 4, −1.19 ducats) — and it moves the orientation by **0 edge flips**, with the sink set unchanged. So it is a fidelity correction with no map consequence at 1444.
**And unlike `devastation`, its scaling law *is* in the file.** The `unrest` block (lines 487–491) carries an in-block comment on its first key — `regiment_recruit_speed = 0.1   #10% longer time to build troops for each rr` — which states that the block's values apply per point of revolt risk. The neighbouring `nationalism` block does the same (`local_unrest = 0.5   #for each year revolt risk!`). The `devastation` block (453–462) carries no such comment, which is exactly why Y049 stands. Adding `unrest` therefore adds a **sourced** scaling law rather than a second assumption.
**Should say:** four static modifiers are *read*, and the choice of four is a classification judgement rather than a file fact — `00_static_modifiers.txt` grants a wealth key in 25 blocks, of which `unrest` is province state and is live on 21 provinces at 1444, worth 12.23 ducats. If it is admitted, its per-point scaling is sourced to the block's own comment, so only `devastation`'s proportionality remains an assumption.

## Y048 — the four grants: devastation −2 scaled by level, prosperity +0.25, under_siege −0.25, occupied −0.5 and local_tax_modifier −0.5
**Status:** CONFIRMED
**Method:** opened each block in `00_static_modifiers.txt`.
**Evidence:** `occupied` (lines 433–441) `local_tax_modifier = -0.5`, `trade_goods_size_modifier = -0.5`; `under_siege` (444–450) `trade_goods_size_modifier = -0.25`; `devastation` (453–462) `trade_goods_size_modifier = -2`; `prosperity` (464–468) `trade_goods_size_modifier = 0.25`. All four values exact. Each block carries further keys the claim does not assert (supply limit, institution spread, movement speed, autonomy and so on).

## Y049 — the devastation scaling law is in no shipped file; −2 x level/100 is an assumption
**Status:** CONFIRMED
**Method:** grepped `common/defines.lua`, `common/defines/`, `common/`, `hints/`, `tests/` and `patchnotes/` for any rule scaling the devastation static modifier.
**Evidence:** no shipped file states a scaling law. `common/defines/` has zero devastation mentions. The 13 devastation defines in `defines.lua` govern accumulation and decay (`FORT_DEVASTATION_IMPACT`, `LOOT_DEVASTATION_IMPACT`, `DEVASTATION_DEVELOPMENT_SCALE = 5` and so on), not the modifier's output. The nearest support is indirect: `patchnotes/1.20 patchnotes.txt:39` fixes the 0–100 range. The proportionality is genuinely an assumption, as stated.
*A contrast that sharpens the claim:* two other scaled blocks in the same file **do** state their scaling in an in-block comment — `unrest` with "#10% longer time to build troops for each rr" and `nationalism` with "#for each year revolt risk!" — so the convention exists in the file and `devastation` simply does not use it. The gap is specific to this modifier rather than general to the file.

## Y050 — only occupied touches the tax term; the other three reach goods_produced alone
**Status:** CONFIRMED
**Method:** listed every key in each of the four blocks.
**Evidence:** `local_tax_modifier` appears in `occupied` and in none of `devastation`, `prosperity`, `under_siege`; those three carry `trade_goods_size_modifier` plus non-wealth keys only. `solver.py` encodes exactly this: `STATE_TAX_MOD = {"occupied": -0.5}`.

## Y051 — these four are what make the map answer to war; §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them
**Status:** CONFIRMED
**Method:** traced the three cross-references in the spec.
**Evidence:** §1.2 line 173 names `devastation`, `occupied`, `under_siege`, `prosperity` as the volatility carriers, citing the same file. §3.3 line 1200 carries "a besieged province genuinely produces less". §2.8 carries "Major war in China — corridors shift for the duration, revert as devastation heals" and the Razed-China row. The dependency chain is real, and these four modifiers are its only mechanism in the model.

## Y052 — eleven counted provinces begin devastated (Bohemia 50, Erzgebirge and Moravia 20) and no province-history file says so
**Status:** CONFIRMED
**Method:** parsed the save's province records for a non-zero `devastation` field, then grepped all of `history/provinces/` for devastation.
**Evidence:** exactly **11** records carry `devastation`, all non-zero, all BOH-owned, all counted: 266, 2968, 2970, 4724, 4725 at **50.000**; 265, 267, 1771, 2967, 4237, 4726 at **20.000**. From `map/area.txt`, `bohemia_area` is those five, `erzgebirge_area` is 267/1771/2967 and `moravia_area` is 265/4237/4726 — the areas match the values exactly. A recursive grep for devastation across `history/provinces/` returns nothing. `solver.py`'s hardcoded dict matches the save on all eleven, with no extras either way.
*Wording note:* Bohemia, Erzgebirge and Moravia are area names, not province names; the Bohemian area is five provinces.

## Y053 — the devastation is applied by on_startup firing flavor_boh.15, via 00_on_actions.txt to on_startup_effect to 01_scripted_effects_for_on_actions.txt
**Status:** CONFIRMED
**Method:** followed every link of the chain in the install.
**Evidence:** `common/on_actions/00_on_actions.txt`'s `on_startup` ends with `on_startup_effect = yes`. `common/scripted_effects/01_scripted_effects_for_on_actions.txt:4716` defines `on_startup_effect`, and at line 4795 fires `country_event = { id = flavor_boh.15 }` for BOH behind a flag — the only firing site in the install. `events/flavorBOH.txt:938`, "The Aftermath of the Hussite Wars", carries `immediate = { hidden_effect = { bohemia_area = { add_devastation = 50 } erzgebirge_area = { add_devastation = 20 } moravia_area = { add_devastation = 20 } ... } }`, which expands to exactly the 5 + 3 + 3 provinces and values of Y052.

## Y054 — it costs 13.40 ducats across the eleven affected counted provinces
**Status:** CONFIRMED
**Method:** re-ran `measure6.py` and independently recomputed the no-devastation field.
**Evidence:** field with devastation **10,607.40**; the same field with the devastation multiplier removed **10,620.80**; difference **13.40**.

## Y055 — the start state is what the engine produces, not what the history files say, and it costs three separate reads
**Status:** CONFIRMED
**Method:** verified each of the three reads separately (Y053, Y059–Y060, Y061) and checked that each changes the field or the counted set.
**Evidence:** `on_startup` devastation is invisible to the history files and worth 13.40 ducats; dated `add_base_*` accumulation is invisible to an overwrite parse and worth one development point; the absent `is_city` filter is worth 20 provinces. All three are cases where the save disagrees with a naive read of `history/provinces/`, and none is derivable from the history text alone.

## Y056 — on_startup also fires flavor_mng.42, flavor_mos.1, flavor_geo.1 and others from its own events = { } list, a second path
**Status:** CONFIRMED
**Method:** read the whole `on_startup` block.
**Evidence:** it carries an `events = { }` list with seven live entries — `muslim_school_events.20`, `flavor_got.1`, `flavor_mng.42`, `flavor_mos.1`, `flavor_fra.206`, `flavor_geo.1`, `flavor_mam.111` — plus one commented out (`flavor_fra.15000`). All three named events are in it. `flavor_boh.15` is **not** in this list, so the two paths are genuinely distinct.

## Y057 — development does not move before the first tick: 2,472 of 2,472 match on base_tax, base_production and owner; only trade_goods differs, on exactly twenty
**Status:** CONFIRMED
**Method:** compared the 1444.11.11 history state (undated block plus every dated block at or before the start date, with `add_base_*` accumulating) against the save's province records for every counted province.
**Evidence:** `base_tax` matching 2,472 with 0 mismatches; `base_production` 2,472 / 0; `owner` 2,472 / 0; `trade_goods` 2,452 / **20**. The twenty are exactly the `unknown` provinces of Y063.

## Y058 — v6.0's first draft said flavor_geo.1 carries add_base_tax; it does not, and those keys are in flavor_geo.3, which on_startup does not fire
**Status:** CONFIRMED
**Method:** read `changes-v6.md` entry 3 (the first draft's text), then `flavor_geo.1` and `flavor_geo.3` in `events/FlavorGEO.txt`, then grepped the install for `flavor_geo.3`.
**Evidence:** the first draft reads "`flavor_geo.1` carries `add_base_tax`, `add_base_production` *and* `add_devastation` — so development itself can move before the first tick." `flavor_geo.1` (`FlavorGEO.txt:8`) has one effect block: `add_legitimacy = -20`, `add_country_modifier = { name = "geo_powerful_nobles" duration = -1 }`, `set_country_flag = geo_received_starting_event` — legitimacy, a country modifier and a flag, with no province scope at all. `flavor_geo.3` (line 98) option `.b` carries `capital_scope = { add_base_tax = 2  add_base_production = 2  add_base_manpower = 1 }`. The only non-localisation reference to `flavor_geo.3` besides its definition is `missions/KoK_Georgian_Missions.txt:2043`, mission `geo_sack_sarai` — a mission, not `on_startup`.

## Y059 — add_base_* in a dated block before the start date accumulates, and v5.0 and earlier overwrote
**Status:** CONFIRMED
**Method:** compared both readings against the save across all counted provinces; read v5.0's `provinces.py`.
**Evidence:** the accumulate reading matches the save on 2,472 of 2,472 provinces (Y057); the overwrite reading fails on province 1. World totals: accumulate `base_tax` 6,938 against overwrite 6,937. v5.0's `provinces.py` writes `state["add_base_tax"]` and leaves `base_tax` alone, which is the overwrite behaviour. The whole game contains exactly one province history file with a pre-start `add_base_*`, so the fix is a correctness fix worth one development point.

## Y060 — province 1 (Uppland) has base_tax = 5 undated plus 1 at 1436.4.28; the game has 6
**Status:** CONFIRMED
**Method:** read `history/provinces/1-Uppland.txt` and the save's province 1 record.
**Evidence:** the file has `base_tax = 5` undated and `1436.4.28 = { ... add_base_tax = 1 }`; a further `1444.11.12 = { add_base_tax = 2 }` falls one day after the start and is correctly excluded. The save holds `base_tax=6.000`.

## Y061 — is_city = yes is not a filter the engine applies: 20 owned provinces omit or comment it out, including 265, and the engine treats them as cities
**Status:** CONFIRMED
**Method:** listed counted provinces lacking `is_city = yes` in their 1444 history state, then read the save's `is_city` field.
**Evidence:** the 20 are 265, 774, 857, 913, 958, 966, 1035, 1038, 1207, 2527, 2579, 2593, 2617, 2671, 2779, 2932, 4573, 4576, 4640, 4856 — one commented out (`265 - Brno.txt:13` is literally `#is_city = yes`), twelve carrying the line only in a post-1444 dated block, seven with no such line at all. The save carries `is_city=yes` on **2,472 records, exactly the owned set**, including all twenty, and on **none** of the 1,451 unowned provinces. 265 is among them and is also one of the devastated eleven, as claimed.

## Y062 — the model counts a province when it has an owner and lies in a trade node: 2,472, not 2,452
**Status:** CONFIRMED
**Method:** computed both counts from history plus `00_tradenodes.txt`.
**Evidence:** owned at 1444.11.11 = **2,472**; owned and in a trade node = **2,472**; owned and `is_city = yes` = **2,452**.
*Note:* every owned province lies in some node's `members` list (897 members are unowned), so the trade-node conjunct filters nothing at 1444 — the operative condition is "has an owner". The unowned-provinces rationale is consistent with §1.2 and §1.3.

## Y063 — twenty counted provinces have no trade good in history; the engine assigns one from each good's chance = { } block
**Status:** CONFIRMED
**Method:** counted counted provinces whose 1444 history `trade_goods` is `unknown`; read the `chance = { }` blocks in `common/tradegoods/00_tradegoods.txt`.
**Evidence:** exactly **20**, all carrying the literal token `unknown` rather than omitting the key: 774, 862, 895, 897, 907, 966, 1809, 2014, 2503, 2510, 2571, 2593, 2596, 2669, 2671, 2932, 4856, 4901, 4902, 4923. Every good definition carries a `chance = { ... }` block (coal's is `chance = { factor = 1 }`), which is the draw mechanism.

## Y064 — the model reads the good the engine actually rolled, as it does for development
**Status:** CONFIRMED
**Method:** read `solver._rolled_trade_goods()` and `province_table()`.
**Evidence:** `_rolled_trade_goods()` opens `VANILLA_start.eu4`, slices the `provinces={}` section and reads the two-tab-indented `trade_goods` field per record; `province_table()` substitutes it whenever history gives `None` or `unknown`. This is the same read-the-engine's-state rule the document applies to development.

## Y065 — pricing those twenty at zero instead understates world wealth by 12.70 ducats
**Status:** CONFIRMED
**Method:** recomputed the field with those twenty provinces' production income zeroed.
**Evidence:** field with the rolled goods **10,607.40**; with the twenty priced at zero **10,594.70**; difference **12.70**.

## Y066 — on this save the twenty came up seven fur, five grain, three wool, two livestock, and one each of cotton, incense and naval_supplies
**Status:** CONFIRMED
**Method:** tallied the save's `trade_goods` for exactly those twenty pids.
**Evidence:** fur 7, grain 5, wool 3, livestock 2, cotton 1, incense 1, naval_supplies 1 — term for term. The section marker is right: this is one draw, and the field carries it.

## Y067 — a different roll gives a slightly different field, and nothing in the model depends on which one
**Status:** CONFIRMED
**Method:** checked the magnitude of the dependence and the model's structural dependence on it.
**Evidence:** the whole twenty are worth 12.70 ducats, 0.12% of world wealth, so a different draw moves the field by at most that order. Nothing in the solver branches on the drawn good — it is priced through the same expression as every other province. The one downstream figure that does move is Y032's 89-versus-88.

## Y068 — TAX_COEFF applies to every counted province: ownership is not modelled, so every province is treated as cored and settled
**Status:** CONFIRMED (derivation)
**Method:** checked the arithmetic of the reference condition and the engine's treatment of the twenty non-`is_city` provinces.
**Evidence:** `Core` +75% and `City` +25% sum to 1.00, so a cored city province carrying nothing else yields `base_tax` ducats a year, which is `TAX_COEFF = 1.0`. Applying it universally *and* carrying either term would double-count. The engine agrees on the settled half: the save marks all 2,472 owned provinces `is_city=yes` (Y061).

## Y069 — TAX_COEFF = 1.0 rests on two readings at base_tax 2 and 6, while base_tax at 1444 runs up to 15 (province 1821), with total development 33 there
**Status:** CONFIRMED
**Method:** computed the maximum `base_tax` and total development over counted provinces from the 1444 history state, cross-checked against the save; read §2.3's measurement row.
**Evidence:** max `base_tax` = **15**, uniquely at **1821** (Nanjing); its development is 15 + 15 + 3 = **33**, which is also the maximum total development over the counted set. The save agrees on both (15.000 / 33.0). §2.3's `TAX_COEFF` row cites exactly two readings, at `base_tax` 6 and 2.

## Y070 — the change removes a large source of hidden owner-dependence from the aggregate graph, no longer "the single largest"
**Status:** CONFIRMED
**Method:** grepped the spec for the superlative; sized the excluded owner terms from the document's own itemisation.
**Evidence:** "single largest" is absent from v6.0. The size is supportable from §1.3's own Garnatah itemisation: `Tax Income Efficiency: 125.0%` = 75 (Core) + 25 (City) + 5 (Reform Iqta) + 5 (Clergy) + 15 (national ideas), of which **25 percentage points are owner terms** — 20% of that province's tax term, against the 0.98% the deleted classifier was worth. So "large" is the right word, and the retreat from the superlative is a real weakening rather than a cosmetic one.

---

# §1.5 — Goods without a graph

## Y071 — repricing the 45 owned latent-coal provinces flips 10 of 159 Phi_w edges and adds 214.60 ducats
**Status:** CONFIRMED
**Method:** re-scanned `history/provinces/` for `latent_trade_goods` blocks containing coal, then repriced those provinces to coal holding every other input fixed and re-ran Phi_w.
**Evidence:** latent-coal provinces **58**, of which **45** are owned and counted. Repricing gives **+214.60** ducats and **10** of 159 edges flipped. Coal's base price is 10.0, the highest of the 32 entries in `common/prices/00_prices.txt` (next is cloves at 8.0).

## Y072 — the counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and devastated, worth 2.40 ducats and 3 extra flips
**Status:** CONFIRMED
**Method:** ran the counterfactual twice — once retaining 4237's devastation multiplier, once dropping it.
**Evidence:** 4237 is in the latent-coal set and in the devastated eleven. Clean: +214.60 ducats, **10** flips. Mixed, with devastation silently dropped: +217.00 ducats, **13** flips. Contamination is therefore **2.40 ducats and 3 extra flips**, and the arithmetic is exactly 0.2 x 3 x 10 x (1 − 0.6) = 2.40 on 4237's `base_production` of 3 at devastation 20.

---

# §1.6 — The aggregate graph

## Y073 — both the sink count and the locations move with the wealth field, and alpha_Phi sets how sharply concentration is read
**Status:** CONFIRMED
**Method:** scanned alpha_Phi over [1, 8] at 0.01 on the fixed 1444 field (701 solves), then scaled the field at fixed alpha_Phi.
**Evidence:** at fixed field the sink set is a 15-band step function of alpha_Phi, with counts 6, 2, 1, 2, 3, 1 at alpha = 1, 1.5, 2, 3, 4, 8 — so the constant moves both count and membership. At fixed alpha_Phi = 1.5, scaling European development moves the set through {ec, hz} to {ec, hz, wien} to {ec, rheinland} to {genua} — so the field does too. Both halves hold.

## Y074 — at alpha_Phi = 1.5 the 1444 field gives two sinks, and a modestly grown Europe gives three or one
**Status:** CONFIRMED
**Method:** ran Phi_w at alpha_Phi = 1.5 on the 1444 field and on European development scaled by 1.02 and 2.00.
**Evidence:** x1.00 gives `{english_channel, hangzhou}` (two); x1.02 gives `{english_channel, hangzhou, wien}` (three); x2.00 gives `{genua}` (one). Neither count nor placement is fixed by the constant.

## Y075 — v2.0–v4.0's "emerges from concentration" and v5.0's "set by alpha_Phi" are wrong the same way: the count is a function of the field and the constant
**Status:** CONFIRMED
**Method:** quoted all four versions; verified the joint dependence.
**Evidence:** the string "emerges from concentration exactly as per-good sink counts do" appears in v2 lines 154–155, v3.0 lines 257–258 and v4.0 lines 306–307; v5.0 lines 342–344 read "Their count is set by `alpha_Phi`; only their locations are emergent." Neither is right: Y073's two scans show the count moving with each of the two inputs while the other is held fixed.

## Y076 — identical orientation at x1 and above, 12 edge flips at x10^-2 and 100 at x10^-6, where the sink set also collapses to {genua}
**Status:** CONFIRMED
**Method:** scaled `b_w` by x100, x10, x1, x10^-2 and x10^-6 and diffed the orientation against the baseline.
**Evidence:** x100 and x10 give **0** flips with the set unchanged; x10^-2 gives **12** flips with the set still `{english_channel, hangzhou}`; x10^-6 gives **100** flips and the set collapses to **{genua}**. All three figures exact, and the observation that the orientation degrades while the sink set survives at x10^-2 is borne out.

## Y077 — 1444's b_w has largest magnitude 0.0225
**Status:** CONFIRMED
**Method:** computed max |1/N − c_w| at alpha_Phi = 1.5.
**Evidence:** **0.022531**, which prints as 0.0225.

## Y078 — two sinks, english_channel and hangzhou; c_w ranks 2 and 3, node-wealth ranks 1 and 12
**Status:** CONFIRMED
**Method:** ran Phi_w and ranked all 80 nodes by c_w and by raw node wealth.
**Evidence:** sinks `('english_channel', 'hangzhou')`. `english_channel`: c_w rank **2**, node-wealth rank **1** (316.6). `hangzhou`: c_w rank **3**, node-wealth rank **12** (226.7). The c_w rank-1 node is `genua`, which is not a sink.

## Y079 — one of the two is a property of the world and the other of the node ordering, and the difference matters more than the count
**Status:** CONFIRMED
**Method:** three independent 800-relabelling sets through the validated five-phase instrument.
**Evidence:** `hangzhou` holds an end in 785, 784 and 771 of 800 (96.4–98.1%); `english_channel` in 315, 324 and 336 (39.4–42.0%). One is near-invariant, the other is one of several, and the count itself ranges 1 to 5. The characterisation is right.

## Y080 — over 800 relabellings the orientation changed every time, a mean of 25 of 159 edges moved, and the sink set came back exactly in 64 of 800
**Status:** PARTIAL
**Method:** three independent sets of 8 seeds x 100 relabellings (set A = 4242/7/999/20250821/1/2/3/4, set B = 11–18, set C = 101/202/303/404/505/606/707/808), each trial re-sorting the arc list after permuting so the relabelling is genuine.
**Evidence:** the orientation changed in **800/800 in all three sets**, and mean flips were **25.35, 25.48 and 25.66**, which rounds to 25 in every set. But the baseline sink set came back **57, 62 and 60** times of 800 (7.1%, 7.75%, 7.5%), not 64 (8.0%). The document names no seeds and `relabel6.py`'s default is four, so 64/800 cannot be reproduced from the shipped tree.
**Should say:** the sink set came back exactly `{english_channel, hangzhou}` in about 7–8% of runs. The correction here is to say **less**: a specific count out of 800 is a sample, and the honest form is the proportion to one figure, or the seeds alongside the count. The 800/800 and mean-25 halves are exact and should stay.

## Y081 — hangzhou was an end in about 98% of them and english_channel in about 40%
**Status:** CONFIRMED
**Method:** the same three 800-trial sets.
**Evidence:** `hangzhou` 785/800 = 98.1%, 784/800 = 98.0%, 771/800 = 96.4%. `english_channel` 315/800 = 39.4%, 324/800 = 40.5%, 336/800 = 42.0%. Both "about" figures survive reseeding at n = 800. The second significant figure does not, which the document's own hedging paragraph anticipates and which Y084 addresses.

## Y082 — the Asian end is the robust one, not invariant, since orderings exist where it loses its end
**Status:** CONFIRMED
**Method:** counted trials in which `hangzhou` held no end.
**Evidence:** 15, 16 and 29 trials of 800 across the three sets. Not invariant, and near enough to invariant to be a fact about that node.

## Y083 — after english_channel the most frequent ends are gulf_of_siam (a little over half), wien (about a third), then rheinland and sevilla; the count ranged 1 to 5, most often 2 or 3
**Status:** PARTIAL
**Method:** the same three 800-trial sets, tallying every end-holder and the count distribution.
**Evidence:** every individual figure checks. `gulf_of_siam` 458/456/421 of 800 = **52.6–57.3%**, a little over half; `wien` 265/261/269 = **32.6–33.6%**, about a third; then `rheinland` (109–120) and `sevilla` (93–123), whose order swaps between sets. Count distribution 1 to 5 in all three sets, modal 2 or 3 (2: 268/244/233; 3: 252/288/283). But the sentence's ranking is wrong: `gulf_of_siam` at 52.6–57.3% is **more** frequent than `english_channel` at 39.4–42.0%, so "after `english_channel` the most frequent ends are `gulf_of_siam` ..." reads as a rank the data do not support.
**Should say:** `hangzhou` about 98%, `gulf_of_siam` a little over half, `english_channel` about 40%, `wien` about a third, then `rheinland` and `sevilla` — or drop "after `english_channel`", which is the phrase doing the false work.

## Y084 — the leading proportions are quoted to two figures and the trailing ones qualitatively; across three 800-trial sets hangzhou came in at 784–789, english_channel 322–336, sevilla 79–117, rheinland 112–136
**Status:** PARTIAL
**Method:** ran three independent 800-trial sets of my own and compared the four ranges.
**Evidence:** the reasoning is exactly right and my data confirm it — a range is a function of which seeds are drawn. But none of the four quoted ranges reproduces. Mine: `hangzhou` **771–785** against 784–789; `english_channel` **315–336** against 322–336; `sevilla` **93–123** against 79–117; `rheinland` **109–120** against 112–136. My sets also show the *leading* proportions moving in the second figure (98%, 98%, 96%), so "quoted to two figures" is generous by the document's own standard.
**Should say:** here too the correction is to say **less**. Quote the leading proportions to one significant figure and describe the trailing ones; delete the four specific ranges rather than re-measure them, since a fresh set of seeds produces a fourth set of ranges and the paragraph's own argument is that this is what happens.

## Y085 — conditional on the node order: the sink set's membership and size, §2.4's end-flag list, and which European node holds an end in the growth table
**Status:** CONFIRMED
**Method:** measured each of the three under relabelling.
**Evidence:** membership and size both vary (Y079–Y083; counts 1 to 5). The end-flag list *is* the sink set by §2.4 item 2, so it varies with it. On the growth table, `english_channel`, `wien`, `rheinland` and `sevilla` all hold ends in different relabellings of the same field, so which European node holds one at the smaller factors is ordering-dependent.

## Y086 — not conditional: fully oriented (159/159), acyclic every time, no fallback ever fires, and the LP objective identical to within 4.44e-16
**Status:** PARTIAL
**Method:** for every one of 2,800 relabellings (the 400-trial set plus three 800-trial sets) recorded the oriented-edge count, ran an acyclicity check, counted fallbacks, and recomputed the LP objective with the same arc formulation the reimplementation uses.
**Evidence:** not-fully-oriented **0**, non-acyclic **0**, fallbacks **0** — all three exact, over 2,800 trials. The objective bound is not: the maximum deviation from the identity permutation's 0.7122759778293255 was **5.551e-16** over the 400-trial set and **6.661e-16** over each 800-trial set, i.e. up to 6 units in the last place, exceeding the claimed 4.44e-16 (4 ULP). Separately, the figure is attributed to `relabel6.py`, which does not compute the objective at all — it prints flips, sink sets and end-holder counts.
**Should say:** the LP objective is identical to within about 7e-16 (six units in the last place), measured with a harness that computes it. If a tighter bound is wanted it has to be re-measured at the intended trial count; if not, "identical to within a few units in the last place" is the safe form and needs no maintenance.

## Y087 — Phase 1 selects genua; both sinks arrive by stall promotion and genua ends a transit node, so 2 promotions and 0 fallbacks
**Status:** CONFIRMED
**Method:** read `run_drain`'s `S0`, `promotions` and `fallbacks` on the Phi_w field, and checked `genua`'s out-degree.
**Evidence:** `S0 = ['genua']`; `promotions = ['english_channel', 'hangzhou']`; `fallbacks = []`. `genua` is not in the sink set and has non-zero out-degree, so it is a transit node. Two promotions, zero fallbacks, exactly as stated.

## Y088 — eight sources, all in the bottom half of the wealth field, c_w ranks 44–75, mean degree 3.1 against the map's 4.0; v2's "cul-de-sacs" is not supported
**Status:** CONFIRMED
**Method:** listed nodes with in-degree 0 on Phi_w and computed their c_w ranks and undirected degrees.
**Evidence:** eight sources — `australia`, `chengdu`, `cuiaba`, `james_bay`, `kongo`, `mississippi_river`, `safi`, `yumen` — with c_w ranks spanning **44 to 75** of 80, all in the bottom half, and mean undirected degree **3.12** against the map's **3.98**. A mean degree of 3.1 is not a cul-de-sac.

## Y089 — every node drains to a sink; acyclic, 159/159 oriented; the sink set unchanged under +/-1% wealth noise on three seeds
**Status:** CONFIRMED
**Method:** BFS from every node to the sink set; acyclicity check; +/-1% uniform multiplicative wealth noise at six seeds.
**Evidence:** **80 of 80** nodes reach a sink; the orientation is acyclic; 159 of 159 edges oriented. The sink set is `{english_channel, hangzhou}` under noise at seeds 0 through 5 — six seeds, three more than the claim needs.

## Y090 — 89.6% of ordered node pairs (5,663 of 6,320) are connected by at least one good's directed path
**Status:** CONFIRMED
**Method:** BFS on each of the 29 per-good orientations, unioning the reachability matrix over goods.
**Evidence:** **5,663 of 6,320 = 89.60%**. The spec states the figure at two sites (lines 465 and 1340) and both carry 5,663 and 89.6%, which `verify6.py`'s cross-phrasing `every_site` check independently enforces.

## Y091 — agreement with the per-good graphs is 53.6% of edge-goods, 52.3% value-weighted
**Status:** CONFIRMED
**Method:** compared Phi_w's orientation against each good's orientation over the 4,611 oriented edge-good pairs, weighting by the good's world trade value.
**Evidence:** **53.63%** unweighted and **52.26%** value-weighted, which print as 53.6% and 52.3%.

## Y092 — the superseded marking-order aggregate scored higher on that measure, and the document no longer maintains a figure for an operator the model does not install
**Status:** PARTIAL
**Method:** computed Phi_ord = sum over goods of V_g x order_g from the per-good marking orders, measured its self-coherence, and grepped the spec for surviving Phi_ord figures.
**Evidence:** the comparison is right — Phi_ord scores **60.36%** (60.09% value-weighted) against Phi_w's 53.63%, so "scored higher" is confirmed, and the percentage itself is gone ("60.3" has zero hits). The second clause is not: §3.9 line 1365 prints "**half** of them terminate no good at all (**7 of 14** on the 1444 field)" six lines before "*No figure is maintained for it here.*"
That "7 of 14" is a maintained figure by the document's own operational test — a number that has to be re-measured whenever the wealth field moves — and its history proves it: v2 line 682 and v3.0 line 958 say "of its 13 end nodes at 1444, **9** terminate no good at all"; v4.0 line 1048 says **10**; v5.0 line 1175 says **8**; v6.0 says **7 of 14**. Five versions, five values, with the end count itself moving from 13 to 14.
Decisively, **v6.0's own R3 pass already deleted it.** `changes-v6.md` entry 13 (`R4-39`, §3.9) replaced the quantified clause with "a majority of them terminate no good at all" and added the sentence "*No figure is maintained for it here.*" A later round re-inserted the figure as "half ... (7 of 14 on the 1444 field)". So the disclaimer is a survivor of the version in which the figure was genuinely gone, and the two now sit six lines apart.
**Should say:** the fix is *not* to restore entry 13's "a majority", which is false on this field — 7 of 14 is exactly half — and was refuted on that arithmetic by the round-3 validator. Nor is "half" durable: it is true **only** on the v6.0 field and was false on all four earlier ones, where the fractions were 9/13, 9/13, 10/13 and 8/13, every one of them a majority. "Half" is a figure spelled as a word, carrying the same maintenance burden as the parenthetical while being invisible to the harness — `verify6.py`'s `WORD` map covers only One through Twelve, and `coverage6.py` names "a count spelled as a word" as the class its pattern cannot match.
The quantifier that survives every field this project has measured is a **bound**: `at least half of them terminate no good at all` is true at 9/13, 10/13, 8/13 and 7/14, still rules out "a few", and cannot be falsified by a field change in the direction the data have actually moved. Failing that, keep "7 of 14" and delete the disclaimer instead — a maintained figure honestly labelled is better than an unguarded word that has already been wrong four times. What cannot stand is a disclaimer beside a figure, in either direction.

## Y093 — alpha_Phi = 1.5 is a stipulated design constant exactly as P0 = 2.0 is: superlinear and round
**Status:** CONFIRMED (stipulation; the stated rationale holds)
**Method:** checked internal consistency and both stated reasons.
**Evidence:** 1.5 > 1, so the exponent is superlinear, and §1.4's semantics make superlinear alpha concentrate demand on individually rich provinces — the stated reason is the right one for the stated effect. §2.3 lists both `P0 = 2.0` and `alpha_Phi = 1.5` as design constants "chosen rather than derived", so the analogy is carried consistently in both sections.

## Y094 — the document no longer offers any derivation: v2.1–v4.0's two-sink calibration was fitted to a field that no longer exists, and v5.0's widest-band ground depended on where the scan was truncated
**Status:** CONFIRMED
**Method:** quoted the prior justifications; re-ran the band scan over both ranges.
**Evidence:** v2 lines 372–374, v3.0 lines 558–560 and v4.0 lines 632–634 carry, verbatim, "calibrated so the 1444 start yields the two-sink hangzhou/english_channel map"; v5.0 lines 395–396 read "retained at 1.5 because it sits inside the widest band". The first was fitted to a field that gave one sink under v5.0 and two under v6.0. The second is truncation-dependent: restricted to [1, 3] the widest band is [2.05, 3.00] at 0.95 wide, while extended to [1, 8] it is [3.50, 5.21] at 1.71 wide, and 1.5's band is 0.25 either way.

## Y095 — scanned over [1, 8] the widest band is 1.71 wide, [3.50, 5.21], {doab, genua, hangzhou}, and 1.5's is not the widest by any margin
**Status:** CONFIRMED
**Method:** scanned alpha_Phi = 1.00 to 8.00 at 0.01 and collapsed the results into bands.
**Evidence:** 15 bands. Widest: **[3.50, 5.21], width 1.71, {doab, genua, hangzhou}**. Next: [6.30, 8.00] at 1.70, which is truncated by the scan's own upper limit, then [2.05, 3.49] at 1.44. 1.5's band is 0.25 wide, seventh widest.
*Harness note:* `verify6.py` checks this figure twice with two different values — the computed 1.71/[3.50, 5.21] against the spec and typed literals 1.70/[3.51, 5.21] against `fixes-agreed.md`. The spec carries the computed one, which is the correct one.

## Y096 — across alpha_Phi = 1.00 to 8.00 at 0.01 the sink set is a step function, and 1.5 sits in [1.38, 1.63], width 0.25, giving {english_channel, hangzhou}
**Status:** CONFIRMED
**Method:** the same scan.
**Evidence:** the sink set is piecewise constant in alpha_Phi with 15 pieces. The band containing 1.5 is **[1.38, 1.63], width 0.25**, and its sink set is **{english_channel, hangzhou}**.

## Y097 — sampled at v2's six values the count is non-monotone: 6, 2, 1, 2, 3, 1
**Status:** CONFIRMED
**Method:** ran Phi_w at alpha_Phi in {1, 1.5, 2, 3, 4, 8}.
**Evidence:** counts **6, 2, 1, 2, 3, 1**, with sets {comorin_cape, doab, english_channel, gulf_of_siam, mexico, sevilla}, {english_channel, hangzhou}, {hangzhou}, {genua, hangzhou}, {doab, genua, hangzhou}, {hangzhou}.

## Y098 — a standing warning: 1444 has two ends and vanilla three, and 1.5 must not be justified by the resemblance
**Status:** CONFIRMED
**Method:** located the warning; checked both counts; checked that §3.9's adoption argument does not use it.
**Evidence:** the warning is at spec lines 493–496. The 1444 sink set has two members (Y078) and `00_tradenodes.txt` carries `end=yes` on exactly three nodes — `genua`, `venice`, `english_channel`. §3.9's adoption bullet states the resemblance argument only in order to disown it. The stipulation is coherent and the facts it rests on are true.

## Y099 — "Europe becomes the centre of trade as it develops" is the design claim, and it is what §3.1's first goal asks the field to deliver
**Status:** CONFIRMED
**Method:** read §3.1's goal list against §1.6's design claim and its stated mechanism.
**Evidence:** Goal 1 is "World responsiveness. Trade direction follows the world's current state, never authored arrows. A horde razing `hangzhou` moves the sink because the wealth moved." The Europe claim is that mechanism run forwards rather than backwards, and Y101–Y103 show the field delivers it. The attribution is loose in one respect — Goal 3's feedback loop is the closer match to "becomes the centre" — but the mechanism the claim invokes is Goal 1's, so the sentence is not misdirected.

## Y100 — the Channel's basin grows from 18 nodes to 28 by about x1.44
**Status:** PARTIAL
**Method:** scaled European development from x1.00 to x2.00 at 0.01 and counted, at each step, the nodes with a directed path to `english_channel`.
**Evidence:** both endpoints are exact on the shipped node ordering — basin **18** at x1.00 and **28** at x1.44, counting `english_channel` itself (17 and 27 strictly upstream). The path between them is not growth. Sampled at every 0.01 from x1.00 to x1.63: 18, 19, 18 (x1.02), 19, 21 (x1.20), 24, 27 (x1.26), 24 (x1.28), 23 (x1.30), **31** (x1.32), 28 (x1.34 through x1.44), 27, 28, **33** (x1.53), 26 (x1.55 through x1.63), and no basin at all from x1.64 where `genua` takes the map. Six reversals, and the maximum is **33 at x1.53–x1.54**, not the 31 at x1.32 that a coarser sample shows.
*And the quantity is ordering-dependent, which settles whether it can be quoted at all.* Over 60 relabellings per factor through the validated instrument: at x1.00 `english_channel` is an end in 27 of 60 and its basin ranges **16 to 75** (median 20) against the shipped 18; at x1.32, an end in 8 of 60, basin 21–31 against the shipped 31; at x1.44, 8 of 60, basin 22–28 against the shipped 28; at x1.53, 4 of 60, basin **24–29 — the shipped 33 falls outside the relabelled range entirely**. So both quoted endpoints are properties of one node ordering, and at the larger factors they are conditional on an end that most orderings do not put there.
**Should say:** delete both figures. The honest sentence is directional — the Channel's basin widens as Europe develops, non-monotonically, and then the end migrates to `genua` at x1.64 — and it needs no maintenance. Naming the endpoints and dropping the verb is not enough: 18 and 28 are as ordering-dependent as the sink membership §1.6 already flags, and the basin size is not among the quantities §1.6's conditional/not-conditional split currently covers.

## Y101 — genua first holds an end at x1.63 and is the sole end from x1.64 through x2.00; past a broad range Asia holds no end
**Status:** CONFIRMED
**Method:** the same 0.01-step scan, read at every step from x1.55 to x2.04.
**Evidence:** `{english_channel, rheinland}` through x1.62; **x1.63** gives `{english_channel, genua, rheinland}`, which is genua's first end; **x1.64 through x2.04** gives `{genua}` alone. Asia holds no end from x1.44 onward except at the transient x1.45–x1.54 steps, so "past a broad range of European growth Asia holds no end at all" holds.

## Y102 — the mechanism carries it: wealth is linear in development, so developing a region moves its c_w share directly and Phi_w's ends follow the wealth
**Status:** CONFIRMED (derivation)
**Method:** checked linearity in the wealth expression and confirmed it numerically.
**Evidence:** wealth = TAX_COEFF x base_tax x (1+t) + GP_COEFF x base_production x (1+g) x price is linear and homogeneous of degree 1 in (base_tax, base_production), so scaling both by k scales wealth by k exactly. Confirmed numerically at Y106 — identical sink sets from dev-scaling and wealth-scaling at every factor. c_w is proportional to wealth^alpha_Phi normalised, so the share moves directly with it.

## Y103 — growth table on 824 counted European provinces: x1.00 {ec, hz}; x1.02 adds wien; x1.56 {ec, rheinland} with Asia none; x2.00 genua alone
**Status:** CONFIRMED
**Method:** took the European province set from `map/continent.txt`, intersected it with the counted set, scaled and re-solved.
**Evidence:** **824** counted European provinces. x1.00 gives `{english_channel, hangzhou}`; x1.02 gives `{english_channel, hangzhou, wien}`; x1.56 gives `{english_channel, rheinland}` with no Asian node; x2.00 gives `{genua}`. All four rows exact.

## Y104 — read the table as a direction rather than a trajectory, and on one node ordering: which European node holds an end at the smaller factors is ordering-dependent
**Status:** CONFIRMED
**Method:** cross-checked against the relabelling data.
**Evidence:** over 800 relabellings of the x1.00 field, `english_channel`, `wien`, `rheinland` and `sevilla` all hold ends in some ordering, so the membership at the smaller factors is not a property of the field. The direction — ends move west, Asia's fades — survives (Y101, Y105). Y100 gives a second, independent reason to read the table as a direction: the basin size is non-monotone in the factor.

## Y105 — at x2.00 genua held an end in 60 of 60 relabellings
**Status:** CONFIRMED
**Method:** 60 relabellings of the x2.00 European-development field (six seeds x 10) through the validated five-phase instrument.
**Evidence:** `genua` an end in **60 of 60**. The full sink set was {genua} in 47 runs, {genua, rheinland} in 7 and {genua, wien} in 6 — so the single-Mediterranean-end reading is a property of the field, while the exact set still moves. Separating this row from the rest of the table is correct.

## Y106 — scaling development and scaling wealth are the same operation here: maximum difference 0.0 across the European set
**Status:** PARTIAL
**Method:** recomputed the field from **scaled development** (base_tax x f, base_production x f, devastation retained) and compared element-wise against the scaled-wealth array at four factors.
**Evidence:** the substantive claim holds — the sink sets from the two constructions are identical at x1.02, x1.44, x1.56 and x2.00 — but "maximum difference 0.0" is a rounding artifact of `measure6.py`'s `round(..., 12)`. The exact maximum is **3.553e-15** at x1.02, x1.44 and x1.56 (float associativity: scaling each term before summing rather than scaling the sum), and exactly 0 only at x2.00.
**Should say:** state that the two constructions give identical sink sets at every factor and drop the difference figure, or print 3.55e-15. The document reports floating-point residuals to two figures elsewhere (3.7e-16, 4.44e-16), so printing 0.0 here is inconsistent with its own practice — and the residual is not the point the paragraph is making.

## Y107 — the 1444 Silk Road route runs genua, alexandria, aleppo, persia, lahore, lhasa, ganges_delta, burma, gulf_of_siam, canton, hangzhou
**Status:** CONFIRMED
**Method:** BFS shortest path on the Phi_w orientation.
**Evidence:** the path reproduces exactly, including `lhasa` where v5.0 had `doab`.

## Y108 — no route leaves english_channel at all: out-degree 0, so the Hansa and the Danube carry power into it, and v5.0's route described a path that does not exist
**Status:** PARTIAL
**Method:** measured `english_channel`'s out-degree and attempted routes out of it; read v5.0's sentence and how `validation-v5.md` graded it.
**Evidence:** the first half is exact — `english_channel` has out-degree **0** on the 1444 Phi_w, no route leaves it, and `north_sea` to `english_channel` runs inward. The retraction is misleading: on v5.0's own field `english_channel` was **not** a sink (v5.0 measured one sink, `hangzhou`), and `validation-v5.md:1396-1403` graded X096 **CONFIRMED**, reproducing `english_channel, lubeck, saxony, wien, venice, ragusa, constantinople, aleppo, ...` edge by edge.
**Should say:** the path does not exist **on v6.0's field**, because option (c) makes `english_channel` a sink. It existed and was independently verified on v5.0's field. That is a consequence of v6.0's own wealth-model change, not an error in v5.0's measurement, and the parenthetical should say so rather than imply v5.0 described something imaginary.

## Y109 — no Europe-to-sink route passes the Cape of Good Hope, checked from genua, north_sea and english_channel
**Status:** CONFIRMED
**Method:** enumerated the routes from each of the three origins to each of the two sinks and tested for `cape_of_good_hope` membership.
**Evidence:** genua-to-hangzhou avoids the Cape; north_sea-to-hangzhou avoids it; north_sea-to-english_channel avoids it; genua-to-english_channel and english_channel-to-hangzhou have no directed route at all. No Europe-to-sink route touches the Cape.

## Y110 — the Cape is a live conduit: in-degree 1, out-degree 3, with 132 ordered node pairs whose path runs through it
**Status:** CONFIRMED
**Method:** measured degrees and counted ordered pairs (a, b) with a reaching the Cape and the Cape reaching b on the Phi_w DAG.
**Evidence:** in-degree **1** (`ivory_coast`), out-degree **3** (`comorin_cape`, `malacca`, `zanzibar`), **132** ordered pairs. The single in-arc from `ivory_coast` and the three Indian-Ocean out-arcs are literally Atlantic drainage into the Indian Ocean, as the claim describes.

## Y111 — v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe-to-sink routes
**Status:** CONFIRMED
**Method:** read v5.0's sentence in context and its grading.
**Evidence:** v5.0 lines 421–429 state it universally, immediately after listing three Europe-to-sink routes and nothing else, and `validation-v5.md:1407-1424` graded X097 **REFUTED** with in-degree 1, out-degree 3 and 115 ordered pairs on v5.0's field. Both halves of the retraction are right.

## Y112 — scaling the 22 European nodes makes genua the sole sink from about x1.65; the 18-node subset needs about x2.15
**Status:** CONFIRMED
**Method:** scaled the wealth of provinces in the 22 named nodes, then in the 18-node western and central subset, on a 0.05 grid and again on 0.01.
**Evidence:** on the 0.05 grid `genua` becomes the sole sink at **x1.65** (22 nodes) and **x2.15** (18 nodes), matching the stated resolution exactly. Refined to 0.01 the first contiguous sole-genua factors are x1.63 and x2.14, so "about" is doing the right work and the two figures are not over-precise.

## Y113 — somewhere inside roughly x2.9 to x3.5 the Cape reverses; bounded above as well as below, so it is a window
**Status:** CONFIRMED
**Method:** tracked the Cape's in- and out-neighbours while scaling the 22 European nodes from x1.0 to x6.0 at 0.1, refined to 0.05 across the window.
**Evidence:** the reversed state — in from {comorin_cape, malacca, zanzibar}, out to {ivory_coast} — holds on **[2.90, 3.40]** and is gone by x3.45, where the Cape returns to in from {malacca}, out to {comorin_cape, ivory_coast, zanzibar}. Bounded on both sides, inside the stated interval, and the 1444 state is the Atlantic-to-Indian direction the claim names.

## Y114 — dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected
**Status:** CONFIRMED
**Method:** multiplied the wealth of the richest province in `hangzhou` (pid 1821) and in `english_channel` (pid 1744) by 2, 5, 10, 20, 30 and 50.
**Evidence:** `hangzhou` becomes the sole sink at x2, x5, x20, x30 and x50, with a transient split into {genua, gulf_of_siam, hangzhou} at x10. `english_channel` becomes the sole sink at x50, with intermediate splits at x10 and x20. Concentration on the boosted node with extra sinks at intermediate boosts, exactly as described, and the de-quantified form is the right one — the transient factors move with the node chosen.

---

# §1.10 — Direction-dependent systems

## Y115 — banding absorbs very little chatter; the flicker-risk set stays every country at a single-valued limit plus flagless countries at Propagate Religion's 50/50 or 35/35
**Status:** CONFIRMED
**Method:** read §1.10's threshold table against the softened wording; ran `verify6.py`'s absence check for v5.0's phrasing.
**Evidence:** of the seven threshold rows, only Improve Inland Routes is banded (50 to establish, 40 to maintain) and only Propagate Religion's nine flag rungs are banded; the other five are single-valued. So banding absorbs little, and the flicker-risk set is as stated. `verify6.py`'s absence check for "So almost nothing absorbs threshold chatter" passes, so the softening is real and not just claimed.
*Scope note:* the play-behaviour half — how often a share actually oscillates across a limit in a running campaign — needs the built mod and cannot be settled from files. This is graded on the file evidence, which is what the claim's mechanism rests on.

## Y116 — banding is not the only damper: three shipped defines rate-limit the mechanics that carry these thresholds
**Status:** CONFIRMED
**Method:** grepped `common/defines.lua`.
**Evidence:** `TRADING_POLICY_COOLDOWN_MONTHS = 12` at line 1045, with the shipped comment "Cooldown until you can change Trading Policy after selecting."; `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` at 1212; `TRADE_COMPANY_COOLDOWN = 60` at 1214. Three shipped defines, and the first demonstrably gates two of the table's rows.

## Y117 — TRADING_POLICY_COOLDOWN_MONTHS = 12 applies to seven of the nine entries — five distinct policies, four with an _upgraded twin, plus Propagate Religion which has none — so four of the five families are rate-limited
**Status:** PARTIAL
**Method:** enumerated every top-level entry in `common/trading_policies/00_trading_policies.txt` and grepped the file for `cooldown`.
**Evidence:** the file has exactly **nine** entries — `maximize_profit` (line 3), `maximize_profit_upgraded` (29), `hostile_trading` (55), `hostile_trading_upgraded` (78), `improve_inland_routes` (101), `improve_inland_routes_upgraded` (146), `establish_communities` (192), `establish_communities_upgraded` (218), `propagate_religion` (239) — and `cooldown` appears at exactly two lines, 25 and 52, both in the `maximize_profit` family. So **seven of nine** entries are rate-limited and **four of the five families** are: both numeric conclusions are correct. The appositive is not. The seven are **three** twinned families plus `propagate_religion`, not "five distinct policies, four of them with an `_upgraded` twin, plus Propagate Religion" — that phrase enumerates all **nine** entries, and the "so" that follows makes it read as a description of the seven.
**Should say:** the cooldown applies to seven of the nine entries — three twinned families (`hostile_trading`, `improve_inland_routes`, `establish_communities`) plus `propagate_religion`, which has no twin — so four of the file's five families are rate-limited. This is a wording fix, not an arithmetic one.

## Y118 — maximize_profit and maximize_profit_upgraded are the exceptions, carrying cooldown = no
**Status:** CONFIRMED
**Method:** read lines 25 and 52 of `00_trading_policies.txt`.
**Evidence:** `cooldown = no` appears exactly twice in the file, once in each of those two entries and nowhere else. No other cooldown key of any kind is present in the file.

## Y119 — TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30 and TRADE_COMPANY_COOLDOWN = 60 are the other two
**Status:** CONFIRMED
**Method:** read `common/defines.lua` lines 1212 and 1214.
**Evidence:** `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30,` and `TRADE_COMPANY_COOLDOWN = 60,`, both uncommented and both present.

## Y120 — a flickering share does not translate into a flickering effect at those three; what is left exposed is everything without a cooldown, which is most of the ladder
**Status:** CONFIRMED
**Method:** matched each of the seven threshold rows against the three defines, using only what the install states about each define's scope.
**Evidence:** the trading-policy cooldown demonstrably damps two rows — Improve Inland Routes and Propagate Religion, both entries in `00_trading_policies.txt`. That leaves five of seven rows exposed: both trade-conflict casus belli rows, privateer blocking, trade-company extra merchant and trade-company control. Five of seven is most of the ladder.
*A caveat the install does not resolve:* the two trade-company defines carry no comment and nothing in the install says what they gate. If they do gate the two trade-company rows, only three of seven remain exposed, which would not be "most of the ladder" — so the claim's strength depends on a scope the files do not state. Settling it needs the running game.

## Y121 — the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.6% over the flag's 26 inland nodes, totals 106.4 at xian to 532.0 at champagne
**Status:** CONFIRMED
**Method:** parsed the save's `trade={ node={ ... } }` section, summed each node's country sub-blocks' `val` fields at their own brace depth, and took the flag's 26 inland nodes from `00_tradenodes.txt`.
**Evidence:** 26 flag-inland nodes; totals run **106.4 at `xian`** to **532.0 at `champagne`**; 50/total ranges **9.4% to 47.0%** with median **21.6%**. The node `total` field agrees with the country-block sum on these nodes, so the two possible readings of "total trade power" coincide here.

## Y122 — as a share after the grant lands, 50/(total+50), the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right
**Status:** CONFIRMED
**Method:** recomputed 50/(total+50) on the same 26 nodes; checked v5.0's sentence and the arithmetic it implies.
**Evidence:** **8.6% to 32.0%, median 17.7%** — exact. v5.0 line 553 attaches 8.6%–32.0% to "of an inland node's total trade power", the first description. 0.086 x 532.0 = 45.75, not 50, so the attribution is arithmetically impossible; 50/532 = 9.40% and 50/582 = 8.59% confirm which description each figure belongs to.

## Y123 — on §2.2's derived 25-node inland basis the median is 21.3%, or 17.5% after the grant
**Status:** CONFIRMED
**Method:** rebuilt the derived inland set (nodes with no coastal province among `members`) and recomputed both medians.
**Evidence:** the derived set has **25** nodes and differs from the flag's set only by `siberia`. Median 50/total = **21.3%**; median 50/(total+50) = **17.5%**. The range endpoints are unchanged at 9.4–47.0% and 8.6–32.0%, so only the medians move, exactly as the parenthetical says.

---

# §2.2 — Solver

## Y124 — solver item 4's wealth expression, with no autonomy, efficiency, ideas or owner terms and no trade-value-modifier factor
**Status:** CONFIRMED (stipulation, matched to the implementation)
**Method:** compared §2.2 item 4's text against `solver.province_table()` term by term.
**Evidence:** the stated expression and the implemented one agree exactly, including the absence of a `(1 + trade_value_modifier)` factor and of any owner term. The stipulation and the reference implementation do not diverge, which is the property the row asserts.

## Y125 — the only modifiers the solver reads are the four province-condition ones, and at 1444 only devastation is live, on eleven provinces
**Status:** CONFIRMED
**Method:** read `STATE_GOODS_MOD` and `STATE_TAX_MOD`, then checked the save for each of the four conditions.
**Evidence:** the solver declares all four and applies devastation on the eleven `ON_STARTUP_DEVASTATION` provinces. The save carries **11** non-zero `devastation` records, **0** `prosperity` records and **0** `occupied` records, and no siege is in progress at the start date — so devastation is indeed the only live one.

## Y126 — world wealth is 10,607.40 annual ducats over 2,472 counted provinces
**Status:** CONFIRMED
**Method:** re-ran the field from the install and the save.
**Evidence:** **2,472** counted provinces, sum **10,607.40**. Both figures independently reproduced, and `verify6.py` pins both against the spec text in one needle.

## Y127 — of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average, and that is the whole of the claim
**Status:** CONFIRMED
**Method:** timed 3 replicates x 12 runs of the full 29-good DRAIN pass (scipy/HiGHS plus the deterministic sweep) after a warm-up pass, on one machine.
**Evidence:** all-29 totals **0.110 s to 0.291 s** across 36 runs — every run of order 0.1 s. Per-good averages **3.8 ms to 10.0 ms**, with replicate means 7.6, 6.1 and 5.3 ms — single digits in every replicate. The refusal to quote anything finer is Y128's subject and is the right call.

## Y128 — repeated 12-run experiments do not reproduce each other closely enough to support anything finer; three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms
**Status:** CONFIRMED
**Method:** the same three replicates.
**Evidence:** my three replicates span **4.0–10.0**, **5.2–7.3** and **3.8–6.9 ms**, and the replicate means differ by 44% (5.3 against 7.6 ms). Three replicates of twelve genuinely do not reproduce each other, which is the proposition. The three specific spans are a machine-and-scheduler sample and, by the claim's own argument, are not reproducible — mine differ, as expected, and the claim survives that because it is asserting the irreproducibility rather than the numbers.

## Y129 — across three replicates of twelve runs, the number of runs landing inside v5.0's quoted 0.17–0.21 s interval was 1, then 0, then 0
**Status:** PARTIAL
**Method:** counted the runs inside [0.17, 0.21] s in each of my three replicates.
**Evidence:** **2, then 6, then 1** — 9 of 36 runs inside the interval, against the claimed 1 of 36. The quantity is a machine-and-scheduler sample and does not reproduce, so the specific counts cannot stand. The weaker conclusion the counts were offered for still holds: 27 of my 36 runs fell outside the interval and the observed totals span 0.110–0.291 s, so v5.0's interval does not describe the distribution.
**Should say:** here the honest correction is to say **less** — drop the count entirely and keep the observed range (0.110–0.291 s against v5.0's 0.17–0.21 s), which is all Y128's argument needs and is the only part that will not move on the next machine.

---

# §2.2a — What map this is for

## Y130 — where Phase 0 acts, free-edge determinism holds only in half: the key reads the post-fold beta, so peeling can create ties the raw balances do not have
**Status:** CONFIRMED (derivation, plus a construction)
**Method:** read the key in `sweep_priority`, then built a case where peeling creates a tie and ran it through the validated five-phase instrument.
**Evidence:** the key is (−DEF[v], beta[v], pid[v]) on the *folded* beta, so ties are a property of the folded field. Constructed case: a 4-cycle A(+0.3), B(+0.7), C(0), D(0) with pendants a(−0.3) on A and b(−0.7) on B. The raw balances at A and B are distinct; after peeling, beta = 0 at all four core nodes, so the key ties where the raw balances do not. Vanilla peels nothing — Phase 0 is a no-op, 0 `Plog` entries — so the 1444 zero-tie measurement says nothing about a map with pendants, exactly as claimed. The determinism half is unaffected because the key remains a deterministic function of the folded field.

---

# §2.3 — Constants

## Y131 — v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them
**Status:** CONFIRMED
**Method:** quoted the provenance statements in v3.0, v4.0 and v5.0; read the script v5.0's README credits with the sweep.
**Evidence:** §1.3 in all three, byte-identical: "neither is a define (`defines.lua` was searched), so both are engine constants recovered by observation". §2.3 in all three: "The two wealth coefficients of §1.3 are hardcoded in the binary". v5.0's README attributes the sweep to `wealthmodel.py`, which **opens no files at all** — the 16 provinces are typed literals and `GP_COEFF` is the literal 0.2. A recursive grep for `static_modifiers` across `v5-owner-agnostic/scripts/*.py` returns nothing, so no v5.0 script ever opened the file holding `provincial_production_size`.

---

# §2.4 — The tradenodes file

## Y132 — relabelling changed the orientation in 400 of 400 runs across four independent seeds, always by returning a different optimal vertex and never by a sweep tiebreak, mean 25 of 159 edges, objective identical to within 4.44e-16
**Status:** PARTIAL
**Method:** 400 relabellings at `relabel6.py`'s documented default seeds (4242, 7, 999, 20250821) through the validated five-phase instrument, recording flips, the LP support mapped back through the permutation, the LP objective, and every exact (DEF, beta) tie on free edges.
**Evidence:** the orientation changed in **400 of 400**; the LP support differed from the shipped support in **400 of 400**, so "always by returning a different optimal vertex" is confirmed directly rather than inferred; exact free-edge key ties were **0 across all 400**, so "never by a sweep tiebreak" is confirmed too; mean flips **25.14**, which rounds to 25. The objective bound fails: the maximum deviation was **5.551e-16** over these 400 trials and **6.661e-16** over 800, both above 4.44e-16. And `relabel6.py` does not compute the objective — it prints flips, sink sets and end-holder counts only, so that one figure is attributed to a script that cannot produce it. The instrument-validation half of the parenthetical is correct: `relabel6.py` does validate against `drain.py` on the identity permutation and exits if that fails.
**Should say:** keep 400 of 400, the mean of 25, the different-optimal-vertex finding and the no-tiebreak finding — all four are exact and all four are `relabel6.py`'s or reproducible from it. Replace the objective figure with "identical to within a few units in the last place", or measure it and attribute it separately; the current form is both too tight and mis-attributed.

## Y133 — twenty-five flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event
**Status:** CONFIRMED
**Method:** compared the relabelling mean against the razed-China flip count, both re-measured this session.
**Evidence:** relabelling mean **25.14 to 25.66** of 159 across four sets; zeroing `hangzhou`-node development flips **22** of 159. Same magnitude, and the comparison is stated as a magnitude rather than a ratio, which is what the data support.

## Y134 — earlier versions quoted a 580-of-580 per-good sweep and an arc-permutation result whose scripts were never shipped
**Status:** REFUTED
**Method:** grepped v1 through v5 specs for "580" and for the arc-permutation result; searched every `scripts/` directory in the tree for a script computing either.
**Evidence:** **no v1–v5 spec contains the figure 580.** It appears in `v5-owner-agnostic/fixes-agreed.md:223-229` — the v5-to-v6 negotiation record, "580 runs on 1444 / orientation changed 580 of 580" — and in four earlier v6 claim drafts under `scripts/`. In a document where every other such parenthetical means v1 through v5, "earlier versions quoted" is false. And the script does exist in the tree: `v5-owner-agnostic/scripts/_audit_b_1444perm.py` computes exactly 29 goods x 20 permutations = 580 and prints "orientation changed", "with the SAME LP support (the sweep's index tiebreaks)" and "with a DIFFERENT support (LP vertex choice)". It is undocumented in v5.0's README, which is presumably what "never shipped" was reaching for. The arc-permutation half of the claim is correct — no script in any tree computes it.
**This is an attribution error, not an arithmetic one, so the fix is wording.** **Should say:** the 580-of-580 sweep came from the v5-to-v6 negotiation record and earlier drafts of this document rather than from any released version, and the script that computes it is `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`, undocumented in that tree's README; the arc-permutation result has no script anywhere. Both are withdrawn in favour of `relabel6.py`'s figure, which is the substantive point and is unaffected.

## Y135 — the canonical order must be the order Phase 2's LP input is built in, not merely the order the sweep breaks ties in
**Status:** CONFIRMED (derivation, and measured both ways)
**Method:** compared a full relabelling against a sweep-only re-keying.
**Evidence:** a full relabelling changes the LP support in 400 of 400 runs and moves a mean of 25 edges. A sweep-only index permutation changes **nothing** — `final.py` item V035 reports 0 orientation flips across 2 index permutations x 29 goods, because Phase 1, the stall promotion and Phase 2 all still read the true index. So fixing the sweep's tiebreak order is provably insufficient, and fixing the LP input order is what the requirement has to name.

## Y136 — everything §1.6 and §2.8 report about stability is measured at fixed node order; re-order the same world and the map moves, with alpha_Phi and every input held fixed
**Status:** CONFIRMED
**Method:** re-ran the relabelling experiment with alpha_Phi and every input identical to the baseline.
**Evidence:** 2,800 relabellings; the orientation changed every time; mean 25 flips; sink-set membership and size both varying (1 to 5 sinks) — with the wealth field, alpha_Phi, the zero-flow tolerance and the graph all byte-identical to the baseline run. The stability figures §1.6 and §2.8 report are therefore conditional in exactly the way stated.

## Y137 — the specific counts are HiGHS-specific in their detail but not in kind; any simplex returns a vertex of a degenerate optimal face
**Status:** CONFIRMED (derivation)
**Method:** checked the LP-theory claim against the measured degeneracy.
**Evidence:** the simplex family terminates at a basic feasible solution, which is a vertex of the feasible polyhedron; when the optimal face has more than one vertex, which one is reached depends on the pivoting sequence and therefore on presentation order. The degeneracy is measured rather than assumed: 400 distinct supports at one objective value, identical to about 6e-16. Both halves of the claim follow.

## Y138 — making the orientation order-independent would need a tie-breaking objective; that is a design change and is not adopted
**Status:** CONFIRMED (stipulation)
**Method:** checked the stated mechanisms against the nature of the degeneracy, and checked that the spec does not adopt either.
**Evidence:** the degeneracy is exactly a non-unique argmin, so uniqueness requires either a lexicographic secondary cost or a strictly convex perturbation — the two mechanisms named. §2.2's solver list requires network simplex or a simplex LP and imposes no secondary objective, and §2.3's knob list carries none, so the change is genuinely not adopted anywhere in the document.

## Y139 — the priority key ties in more places than §1.1 documents: Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass
**Status:** CONFIRMED
**Method:** read all four tie sites in `drain.py`.
**Evidence:** the free-edge sweep uses `keyfn = (-DEF[v], beta[v], pid[v])`. Phase 1 uses `S.add(min(comps[j], key=lambda v: (beta[v], v)))`. The stall promotion uses `min(terminals, key=lambda v: (beta[v], v))`, identical in form. The top-k cut uses `sorted(range(len(comps)), key=lambda j: -M[j])[:k]`, whose sort is stable, so equal masses are cut in cluster-construction order, which derives from node order. Four sites, three of them undocumented in §1.1.

## Y140 — none of them fires on 1444: zero exact (DEF, beta) ties on free edges across 29/29 goods, zero within-cluster beta ties, zero tied cluster masses
**Status:** CONFIRMED
**Method:** instrumented Phase 0, Phase 1, Phase 2 and the DEF computation for every good and for Phi_w, counting each of the three tie classes exactly.
**Evidence:** Phi_w — free-edge (DEF, beta) ties **0**, within-cluster beta ties **0**, tied cluster masses **0**, with 4 clusters, k = 1 and 0 peels. Across the 29 goods — **0**, **0**, **0**. Independently, `final.py` reports "exact (DEF, b) ties on free edges: 0" and `rankrep.py` reports "exact score ties over 4611 edge-good pairs: 0".

## Y141 — the end-flag list is a function of the canonical node order, not of the world alone
**Status:** CONFIRMED
**Method:** end flags are the Phi_w sink set by §2.4 item 2, so measured the sink set under relabelling.
**Evidence:** over 800 relabellings of one unchanged world, the sink set took sizes 1 to 5 and included `hangzhou`, `gulf_of_siam`, `english_channel`, `wien`, `rheinland`, `sevilla`, `champagne`, `genua` and `ganges_delta` in various combinations. Changing the order changes the flags with nothing in the world changing, which is the claim.

## Y142 — end flags at 1444 in the shipped order: two end nodes, english_channel and hangzhou, against vanilla's three
**Status:** CONFIRMED
**Method:** ran Phi_w in the shipped node order; counted `end=yes` in `00_tradenodes.txt`.
**Evidence:** sink set `{english_channel, hangzhou}` — two. Vanilla's file carries `end=yes` on `genua`, `venice` and `english_channel` — three. Both counts read from primary sources rather than from the spec's own quotation of them.

---

# §2.7 — Probes

## Y143 — item 15's finding is consistent with §1.9's rule: one observation on one node, enough to retire the cautionary case and not enough to promote the rule to a measurement; v3.0–v5.0 said §1.9 was "correct as written and gains no qualifier"
**Status:** PARTIAL
**Method:** read the probe-15 section of `v2-drain/game-session.md` in full and the corresponding sentence in v3.0, v4.0 and v5.0.
**Evidence:** the quotation is exact and byte-identical in all three (v3.0 lines 645–649, v4.0 lines 720–724, v5.0 lines 831–835), and the epistemic judgement — consistent with the rule, closes the cautionary case, does not amount to a measurement of it — is right. But the evidence base is understated. `game-session.md:395-448` records **two** country-node observations, not one: the clean case is France in Sevilla (`Transfers from traders downstream: +3.1`, total 3.3, provincial power 0.0), and a section headed "## Corroboration" records **Castile in Safi** — total 27.0 of which `Transfers from traders downstream: +25.9`, on 0.0 provincial power.
**Should say:** two observations on two nodes — France in Sevilla and Castile in Safi — still not enough to promote the rule to a measurement, but the single-observation marker does not apply to this row and should be dropped from it. The judgement itself needs no change.

---

# §2.8 — Validation

## Y144 — sinks are {selected and flow-terminal} union promoted, 1 to 8 per good, and high-demand nodes are sinks at 16.8% in the top demand decile against 6.9% in the bottom
**Status:** CONFIRMED
**Method:** re-ran all 29 goods; computed P(sink | top decile) and P(sink | bottom decile) by per-good demand rank, testing several candidate definitions of "decile" before settling.
**Evidence:** the equality holds 29/29 and sinks run 1 to 8. With a true decile of 80 nodes — the top and bottom **8** — the figures are **16.8% and 6.9%** exactly, over 232 node-goods in each tail. The barbell shape is real and sharp: at a top-10 cut the figures are 14.1%/6.9%, at top-16 10.3%/4.5%, at top-20 8.6%/5.0%, so the concentration sits in the extreme tails and the decile is the right cut for the claim.

## Y145 — the Razed-China row is ordering-robust: it turns on hangzhou holding an end, which it does in about 98% of relabellings, and on the razed field hangzhou loses its end in every relabelling tried
**Status:** CONFIRMED
**Method:** 200 relabellings of the razed field (eight seeds x 25) through the validated instrument.
**Evidence:** on the baseline field `hangzhou` holds an end in 96.4–98.1% of relabellings. On the razed field it holds an end in **0 of 200**. The most frequent razed sink sets are `{gulf_of_siam}`, `{english_channel, gulf_of_siam}` and `{english_channel, gulf_of_siam, rheinland}` — the end has moved off `hangzhou` under every ordering tried, which is what the row asserts and the correct quantifier for it.

## Y146 — zeroing hangzhou-node development moves the Phi_w sinks to {doab, english_channel, gulf_of_siam}, with 22 of 159 edges flipping
**Status:** CONFIRMED
**Method:** zeroed the wealth of every counted province in the `hangzhou` node and re-solved.
**Evidence:** sinks `{doab, english_channel, gulf_of_siam}`, **22** of 159 edges flipped.

## Y147 — hangzhou, not beijing, is China's wealth pole: node wealth 226.7 against 143.0, and it holds the richest single province the model counts
**Status:** CONFIRMED
**Method:** summed node wealth and found the richest province in each node.
**Evidence:** `hangzhou` **226.7** (node-wealth rank 12), `beijing` **143.0** (rank 39). `hangzhou`'s richest province is pid **1821 at 27.00**, which is the maximum over all 2,472 counted provinces; `beijing`'s best is pid 1816 at 19.50. The qualifier "the model counts" is load-bearing and correct — 1821 is also the province v5.0's deleted apparatus boosted, so under that field the ranking was different.

## Y148 — zeroing beijing also moves the map (15 flips), because deleting a percent of world wealth renormalises c_w everywhere; what separates the cases is that hangzhou survives as a sink when beijing is zeroed
**Status:** CONFIRMED
**Method:** zeroed the `beijing` node and re-solved.
**Evidence:** **15** of 159 edges flipped and the sink set stayed `{english_channel, hangzhou}` — so the map moves and `hangzhou` survives. Zeroing `hangzhou` moves 22 edges and `hangzhou` does not survive. The asymmetry is which node keeps its end, not whether the map moves, exactly as stated.

---

# §3.2 — Why a flow and a drainage sweep

## Y149 — what the ratio metric cannot see is the thing the diagnosis rests on: a max/min ratio over producing nodes is blind to sparsity, and on the contrast metric the demand side is the wider one
**Status:** CONFIRMED
**Method:** computed, per good, the max/min ratio over nodes with non-zero supply and over nodes with non-zero demand, and counted producers per good.
**Evidence:** supply contrast **4.0 to 97.0** over the 28 goods with more than one producer; demand contrast **211 to 15,010** over all 29 — the demand side is the wider one. Sparsity is invisible to the metric by construction: spices are produced in **18 of 80** nodes and cloves in **exactly 1**, and a ratio taken over producing nodes cannot express how few they are (cloves' supply contrast is 1.0 by definition). §3.15 no longer copies the measurement, as claimed.
*One precision:* §3.2 states the *direction* rather than the numbers, so "a measurement §3.2 carries" means the conclusion, not a figure. That is consistent with the R3 convention and is the right reading.

## Y150 — better wealth inputs move Genoa to a co-sink at roughly x1.7 without making demand the determinant of placement
**Status:** CONFIRMED
**Method:** reimplemented the operator being diagnosed — the v1 Laplacian on spices, alpha = 1.5, supply from goods produced, demand wealth^alpha normalised over the world — and bisected the wealth multiple on `genua`'s counted provinces to 60 iterations.
**Evidence:** the LAP spices baseline sink is **`saxony` alone**; `genua` joins the sink set at **x1.7244**, which is "roughly x1.7". It joins as a *co*-sink beside `saxony`, so the qualifier is right, and demand is still not what places the sink.

## Y151 — moving the spice sink to a Chinese node takes a wealth multiple of 3.6–4.8x: beijing 3.63x, hangzhou 4.13x, xian 4.61x, canton 4.78x
**Status:** CONFIRMED
**Method:** the same bisection, per node.
**Evidence:** `beijing` **x3.6264** (3.63), `hangzhou` **x4.1253** (4.13), `xian` **x4.6056** (4.61), `canton` **x4.7754** (4.78). Range 3.63 to 4.78, i.e. 3.6–4.8x. All four figures exact to the two decimals quoted.

## Y152 — those are wealth multiples, not demand multiples: because demand is wealth^alpha normalised, the same move expressed in demand is a much larger factor
**Status:** CONFIRMED (derivation, and measured)
**Method:** compared each node's realised demand share before and after applying its wealth multiple.
**Evidence:** demand-share multiples at the thresholds are **x6.34** (beijing, 1.50% to 9.52%), **x6.80** (hangzhou, 3.15% to 21.43%), **x8.79** (xian) and **x8.78** (canton), against wealth multiples of 3.63 to 4.78. The mechanism is the exponent: k^alpha = k^1.5, so 3.6264^1.5 = 6.91, with the realised ratio a little lower because the world denominator grows too. The claim is stated qualitatively ("a much larger factor"), which is the right form — the exact ratio depends on which normalisation is reported.

## Y153 — the four named are not the cheapest: girin needs 3.89x and yumen 4.49x, both inside the range
**Status:** CONFIRMED
**Method:** ran the same bisection on every Chinese-region node.
**Evidence:** thresholds in order — `beijing` 3.6264, **`girin` 3.8876**, `hangzhou` 4.1253, **`yumen` 4.4928**, `xian` 4.6056, `canton` 4.7754, with `chengdu` 8.0876 and `lhasa` 10.6697 well outside. Both quoted figures are exact, both lie inside 3.6–4.8x, and the four named are not the four cheapest — `girin` and `yumen` are cheaper than `xian` and `canton`. So the claim is about the size of the intervention rather than about which node is easiest to move, as it says.

## Y154 — two cautions: the key reads the post-fold beta so peeling can create ties, and the indexing is load-bearing wherever the key ties, which is not only the fallback branch — and none of them is why §2.4 requires a canonical node order
**Status:** CONFIRMED
**Method:** each of the three parts verified separately — the post-fold caution at Y130 (constructed), the four tie sites at Y139 (code), the Phase-2 attribution at Y132 and Y135 (measured).
**Evidence:** the folded-beta construction produces a tie the raw balances lack; the key ties at four sites, only one of which is the fallback; and the canonical-order requirement is measured to come from Phase 2, since a sweep-only re-keying changes nothing (0 flips over 2 permutations x 29 goods) while a full relabelling changes the LP support in 400 of 400 runs with zero key ties anywhere. All three clauses hold, and the third is the one that closes the loop with §2.4.

---

# §3.3 — Why wealth, and why per province

## Y155 — cape_of_good_hope's members list has 20 entries, but 1460 is a sea zone in map/default.map's sea_starts, so the node holds 19 land provinces
**Status:** CONFIRMED
**Method:** read the node block in `00_tradenodes.txt`, the `sea_starts` list in `map/default.map`, `map/definition.csv` and 1460's history file.
**Evidence:** members are 1460, 789, 833, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1173, 1800, 2856, 2864, 2880, 4781, 4782, 4783, 4784 — **20**. `sea_starts` holds 668 ids and **1460 is among them**; it is not in `lakes`. `definition.csv:1461` names it "Cape of Good Hope" and its history file carries only `discovered_by` lines — no owner, no `base_tax`, no `trade_goods`. Exactly one water member, so **19 land provinces**. §3.3's companion figures also check: `girin` 77 land, `champagne` 33, `nippon` 68 land of 69 members. The round-five revert to 19 was correct.

---

# §3.4 — Why supply is pre-modifier

## Y156 — in v1 the production-income substitution broke the alpha = 1 identity, measured as orientation agreement collapsing to well under half the map; the 159/159-to-68/159 figure is no longer carried
**Status:** CONFIRMED
**Method:** located the figure's origin and its removal; re-ran the substitution on the current field.
**Evidence:** `v1-laplacian/validation.md:4517` — "Orientation agreement collapses from 159/159 to 68/159" — measured on v1's alpha = 1 identity with production-income supply. 68/159 = 42.8%, so "well under half" is a faithful de-quantification. The figure appears verbatim in v2 line 586, v3.0 line 848, v4.0 line 933 and v5.0 line 1057, and "68/159" has **zero** hits in the v6 spec.
*Worth recording:* on the v6.0 field the substitution no longer collapses agreement at all — `final.py` item V138 reports 159/159 — so the claim is true only as scoped, "in v1", which is how it is written. Dropping the figure was the right call for a second reason the document does not give: the figure would not reproduce if anyone tried.

---

# §3.5 — Why alpha is anchored absolutely

## Y157 — change_price values are fractions of the good's base price, and the shipped tutorial save settles it: paper 4.375 on a base of 3.5 is x1.25, gems 5.000 on a base of 4.0
**Status:** CONFIRMED
**Method:** opened `tutorial/eu4_tutorial_chapter10.eu4` (plain-text `EU4txt`, dated 1492.2.6), read its `change_price` section, and took base prices from `common/prices/00_prices.txt`.
**Evidence:** `paper={ current_price=4.375  change_price={ key="PAPER_IN_BUREAUCRACY" value=0.250 } }` and `gems={ current_price=5.000  change_price={ key="FACETING" value=0.250 } }`; every other good in the save sits at its base price. Bases: paper **3.5**, gems **4**. 3.5 x 1.25 = 4.375 and 4.0 x 1.25 = 5.000, while the additive readings would give 3.75 and 4.25 — both excluded. The producing entries were also located: `events/PriceChanges.txt` prices.35 and prices.38, plus the same keys in `history/countries/HAB - Austria.txt` at 1490.1.1 and 1485.1.1, both before the save date.
*One limit worth knowing:* no shipped save carries a good with two simultaneous keys, so whether multiple keys sum or compound is not settled by any file. The claim does not assert that, and should not start to.

## Y158 — the install carries 161 textual change_price blocks: 93 events, 14 missions, 1 common, 53 history of which 13 are negative (all in HAB - Austria.txt), and none in decisions
**Status:** CONFIRMED
**Method:** walked each of the five trees, stripped `#` comments to end of line, and counted `change_price` followed by an opening brace; cross-checked with an independent grep.
**Evidence:** events **93** across 12 files, missions **14** across 10 files, common **1** (`common/parliament_issues/01_english_parliament_actions.txt`), history **53** in one file, decisions **0** — total **161**. Both counting methods agree, so there are no line-split `change_price =` / `{` forms hiding from the regex. History negatives: **13**, all in `history/countries/HAB - Austria.txt` — fish −0.1, wool −0.10, wool −0.25, incense −0.25, fish −0.1, grain −0.20, copper −0.35, coffee −0.4, spices −0.4, paper −0.5, chinaware −0.5, gems −0.5, slaves −0.4. `change_price` appears in no other tree.

## Y159 — ten of the 161 never execute: four in effect_tooltip strings, three in a country_event_with_effect_insight's effect string, three in tooltip = { } wrappers, so 151 are executable
**Status:** CONFIRMED
**Method:** a character-level scan tracking quote state, comment state and a brace stack labelled by the key introducing each brace, so a block inside a quoted string is distinguishable from one in code position.
**Evidence:** 161 total = 154 in code position plus 7 inside quoted strings; of the 154, **3** sit under a `tooltip` frame. That is **10 non-executing and 151 executable**, and the 4/3/3 split is exact. `effect_tooltip`: `missions/DOM_Britain_Missions.txt:919` (fur) and `KoK_Persia_Missions.txt:3384`, `:3390`, `:3396` (silk, dyes, cloth), all inside a `country_event_with_insight`. `effect = "..."` of a `country_event_with_effect_insight`: `KoK_Byzantine_Missions.txt:2070` (silk), `KoK_Yemen_Missions.txt:954` (coffee), `WOC_Italian_Missions.txt:2841` (wine). `tooltip = { }`: `events/flavorMAL.txt:1736` (ivory) and `WOC_Hisn_Kayfa_Missions.txt:1448`, `:1459` (grain).

## Y160 — six of the seven quoted ones duplicate a block already counted in events/, and the seventh names a price key no event in the install ever sets
**Status:** CONFIRMED
**Method:** matched each of the seven on `trade_goods`, `value` **and** `key` against the 151 executable blocks, then searched the whole install for each key.
**Evidence:** six match an executable block exactly — silk 0.2 `BYZ_growing_demand` to `events/flavorBYZ.txt:1921`; silk 0.25 `PERSIAN_SILK` to `FlavorPER.txt:1463`; dyes 0.5 `PERSIAN_DYES` to `:1469`; cloth 0.35 `PERSIAN_CLOTH` to `:1475`; coffee 0.25 `YEM_coffee_price_boost` to `flavorYEM.txt:89`; wine 0.4 `ITA_wine_upgrade` to `flavorITA.txt:448`. The seventh, fur 0.25 **`ENGLISH_FUR_TRADE`**, exists in the install only as that tooltip string plus four localisation entries; the event it advertises (`FlavorGBR.txt:465-470`) uses the different key `FUR_TRADE`. No executable block anywhere sets `ENGLISH_FUR_TRADE`.

## Y161 — all ten are positive and every negative block in the install is executable, so the partition is identical under either census
**Status:** CONFIRMED
**Method:** read the sign of each of the ten; enumerated every negative block install-wide and classified its position; recomputed the partition from scratch.
**Evidence:** the ten are +0.25, +0.2, +0.25, +0.5, +0.35, +0.25, +0.4, +0.33, +0.1, +0.1 — no negatives. Install-wide negatives: **40** (27 in `events/`, 13 in `history/`), **all in executable position**. Since §3.5's partition is computed from each good's most negative single event and no negative is among the ten, the partition is identical under either census. Recomputed independently: **13 below 2.0** (grain and wine reaching 0.625), **2 exactly on 2.0** (gems, silk), **4 with a negative that does not reach 2.0** (cloth, coal, dyes, iron), **11 with no negative event at all** (cloves, cocoa, cotton, fur, ivory, naval_supplies, salt, sugar, tea, tobacco, tropical_wood) — 13/2/4/11 summing to 30.

## Y162 — v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one
**Status:** CONFIRMED
**Method:** quoted both censuses.
**Evidence:** v4.0 line 949 — "All **154** `change_price` blocks were parsed — 93 in `events/`, 7 in `missions/`, 1 in `common/`..."; v5.0 lines 1073–1077 — "All **161** ... 93 in `events/`, 14 in `missions/`...". The missions gap is exactly 7, the quoted set. The executable count is 151, so neither figure is it, and the diagnosis is right.

## Y163 — v5.0's claim that the scan was "guarded by a per-file count assertion" is false; there was no assertion anywhere in its toolchain
**Status:** CONFIRMED
**Method:** read v5.0's sentence, then the script its README credits with the scan, then grepped the whole v5.0 toolchain for `assert`.
**Evidence:** v5.0 lines 1075–1076 — "so the scan is now guarded by a per-file count assertion". The README attributes the scan to `w10.py`, which contains zero `assert` statements, no per-file counting, and the same silent `except Exception: pass`. Across all of `v5-owner-agnostic/scripts/*.py`, `assert` appears only in `patch_lib.py`, `stats5.py` and `toys.py`, none of which touches the `change_price` scan; `validate_v5.py` contains none at all.

## Y164 — verify6.py now checks the census, but only by requiring the printed total to match a computed one rather than by reconciling per file, and measure6.py's walker still swallows parse failures in a bare except
**Status:** CONFIRMED
**Method:** read both scripts.
**Evidence:** `verify6.py` checks the printed total against the computed total and, separately, the events-tree count against the computed events count — a total and one tree, not a per-file reconciliation. `measure6.py`'s walker is `try: walk(pdx.load(fp), tree)` / `except Exception: pass`. Both halves exact.
*Mitigating detail the claim does not mention:* the 161 total comes from a regex over the raw text rather than from the walker, so a swallowed parse failure cannot corrupt the census total — only the negative-value partition, which is built from the walker's `hits`.

## Y165 — the reason a plain parse misses these is mechanical: pdx.py tokenises a quoted string as one opaque unit
**Status:** CONFIRMED
**Method:** read `pdx.py`'s tokenizer.
**Evidence:** `TOK = re.compile(r'"[^"]*"|[{}=]|[^\s{}=]+')` — the first alternative consumes a whole double-quoted string as a single token, so `change_price` inside `effect_tooltip = "..."` never becomes a key and the walker cannot see it. `tooltip = { }` blocks, by contrast, *are* parsed into the tree, which is why they need a separate rule — exactly the mechanism the claim states.

---

# §3.9 — Why Phi_w is the installed graph

## Y166 — genua, gulf_of_siam and sevilla rank 4th, 3rd and 7th by node wealth (mexico 2nd) at 296.0, 297.9 and 266.5 against english_channel's 316.6, which is a sink
**Status:** CONFIRMED
**Method:** summed node wealth over counted provinces and ranked all 80 nodes.
**Evidence:** `english_channel` **316.6** (rank 1, and a sink); `mexico` **300.4** (rank 2); `gulf_of_siam` **297.9** (rank 3); `genua` **296.0** (rank 4); `sevilla` **266.5** (rank 7). All six figures exact.

## Y167 — Phi_ord scores higher than Phi_w on self-coherence; its ends are scheduling artifacts, half of them terminate no good at all (7 of 14), no demand capital is among them, and its end count does not concentrate as demand concentrates
**Status:** CONFIRMED
**Method:** computed Phi_ord = sum over goods of V_g x order_g from the per-good marking orders, oriented by it, measured all four properties, and swept cloves-alpha from 2 to 64.
**Evidence:** self-coherence **60.36%** (60.09% value-weighted) against Phi_w's 53.63% — higher. **14** ends, of which **7** — `amazonas_node`, `basra`, `chengdu`, `james_bay`, `ragusa`, `rio_grande`, `yumen` — terminate **no** good, exactly half. The top-five demand nodes are `genua`, `english_channel`, `hangzhou`, `gulf_of_siam`, `champagne`, and **none** is among the 14. The end count is **14 at every one of cloves-alpha in {2, 4, 8, 16, 32, 64}** — it does not concentrate at all. All four sub-claims verified.
*Cross-reference:* Y092 records the consequence — §3.9 prints this 7-of-14 figure six lines before saying no figure is maintained for the operator. The figure is right; keeping it is what contradicts the neighbouring sentence.

## Y168 — the "two vanilla-like ends at 1444" premise should not be revived even though the field again gives two ends: the count is a property of the field, not the operator, and pinning the operator to it would be the calibration §2.3 withdrew
**Status:** PARTIAL
**Method:** checked the stipulation for internal consistency and tested the stated rationale by holding each input fixed in turn.
**Evidence:** the recommendation is sound and its history is right — v2.1 through v4.0 did justify adoption by the resemblance, and §2.3 does withdraw it. But the stated rationale is imprecise in two ways the document itself supplies the counter-evidence for. §1.6's own Y075 says the count is a function of the field **and** alpha_Phi, and my scan confirms it: 6, 2, 1, 2, 3, 1 at six alpha values on one unchanged field. And the count *is* partly a property of the operator: on the identical 1444 field, Phi_ord gives **14** ends against Phi_w's 2.
**Should say:** the count is a property of the field and of alpha_Phi, and not something the operator guarantees. That is the point that matters and it is what makes pinning the operator to the count a calibration; "not the operator" as written is the half that does not survive checking.

## Y169 — the trade is stated as a direction: what it costs is self-coherence, what it buys is one operator, one set of guarantees and ends where the wealth is, with no points figure attached
**Status:** CONFIRMED
**Method:** read §3.9's adoption bullet; grepped for a points figure.
**Evidence:** the bullet states the cost as "self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on" and the gain as "one operator, one set of guarantees, and ends that sit where the wealth is". "60.3" and "62.7" have zero hits in the spec, so no points figure is attached; the actual gap (60.36% against 53.63%, 6.7 points) is not printed anywhere.

---

# §3.10 — Why the engine's economy is overwritten

## Y170 — the two forms agree to a worst relative disagreement of 0 to 3.7e-16, one to three units in the last place (v5.0 said at most one)
**Status:** CONFIRMED
**Method:** ran `scripts/audit_f4.py`, which builds each node's real 1444 country table from the save and evaluates both forms of income_C in doubles at the five named nodes.
**Evidence:** worst relative disagreement on the single graph: `sevilla` **1.71e-16**, `genua` **2.17e-16**, `gulf_of_siam` **2.47e-16**, `malacca` **2.63e-16**, `champagne` **2.99e-16** — a range of 1.5 to 2.7 units in the last place (one double ULP is 1.11e-16 relative), with per-collector errors printing as exactly 0.0 at every collector. Every value lies inside the claimed bound of 3.7e-16, and "one to three units in the last place" is the right characterisation where v5.0's "at most one" was not.

## Y171 — propagation is kept on a single graph, and the reason is not the one v1 through v6.0's own first draft gave: reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction
**Status:** CONFIRMED
**Method:** checked the argument; located the first draft's version in `changes-v6.md`.
**Evidence:** propagation off a single graph contributes a term carrying no good index, so powershare_C(n) remains good-independent and factors out of the sum over goods — the identity is structural. The first draft argued from magnitude instead: `changes-v6.md:1118` reads "the error is **at most 0.1%** at every node measured" and "a per-node error that a reasonable scalar keeps within a tenth of a percent". v1 through v5 likewise argued from a magnitude (Y177). The reason genuinely changed, and the new one does not depend on a measurement.

## Y172 — per-good propagation makes a country's power differ by good: gulf_of_siam's 29 goods leave it by seven distinct downstream sets (v5.0 said eight)
**Status:** CONFIRMED
**Method:** enumerated `gulf_of_siam`'s out-neighbour set in each of the 29 per-good orientations.
**Evidence:** exactly **seven** distinct sets: {}, {burma}, {canton}, {burma, canton}, {burma, malacca}, {canton, malacca}, {burma, canton, malacca}. v5.0 line 1210 says "eight distinct downstream sets and still shows a 0.003% effect"; `validation-v5.md` graded X169 REFUTED on that count, and seven is what the current field gives.

## Y173 — with ps-bar_C = sum of v_g x cs_g x ps_C(g) over sum of v_g x cs_g, collect_pool x ps-bar_C = income_C follows algebraically and the shares sum to 1
**Status:** CONFIRMED (derivation)
**Method:** checked the algebra.
**Evidence:** income_C = sum over g of v_g x cs_g x ps_C(g), and collect_pool = sum over g of v_g x cs_g, so ps-bar_C = income_C / collect_pool and collect_pool x ps-bar_C = income_C is definitional. Summing over collectors, sum_C ps-bar_C = sum_g v_g x cs_g x (sum_C ps_C(g)) / collect_pool = sum_g v_g x cs_g / collect_pool = 1, using sum_C ps_C(g) = 1 per good. Both statements hold, and the claim correctly labels this algebraic rather than measured — it is true by the construction of ps-bar, which is exactly what makes the objection structural rather than numeric.

## Y174 — both inputs already exist per good at write time, and §2.6 sums exactly them into collect_pool
**Status:** CONFIRMED
**Method:** compared §2.6's written-fields table against the definition of ps-bar_C.
**Evidence:** §2.6 writes "Node collectible pool = sum over g of value_g(n) x collected_share(n,g)", which is literally the denominator of ps-bar_C. Both `value_g(n)` and `collected_share(n,g)` exist per good at that point by §1.8, so the numerator's inputs are available too. Nothing new would have to be computed.

## Y175 — the real cost is that ps-bar_C is not derivable from trade power alone: it is value-weighted, so installing it means writing a fictitious per-node trade power, and every other consumer of that field reads the fiction
**Status:** CONFIRMED (derivation)
**Method:** checked what ps-bar_C depends on, and what the engine exposes.
**Evidence:** ps-bar_C is a function of v_g (node value per good) and cs_g (collected share per good) in addition to the per-good power shares, so it is not recoverable from any per-country power scalar. The engine's node structure exposes a per-country trade *power*, not a per-country income *share*, so installing ps-bar_C means writing a power value chosen to make the ratio come out right — and §1.10's threshold mechanics, §1.9's propagation and the casus-belli checks all read that same field. The objection is structural, as claimed, and does not depend on how large any error would be.

## Y176 — that is a claim about what the engine exposes rather than about a magnitude, and it is why the single graph stays
**Status:** CONFIRMED (derivation)
**Method:** checked the inference.
**Evidence:** on one graph the propagated term carries no good index, so powershare_C *is* the country's power share and the scalar the engine already holds is the right one — no invention needed. That is the whole content of the preference, and it holds independently of any measured magnitude.

## Y177 — every magnitude previous versions quoted was an artifact of substituting some other weighting: v1–v3.0's 5.96 ducats, v4.0's 0.41%, v5.0's single-digit percent, v6.0's first draft's at most 0.1%
**Status:** CONFIRMED
**Method:** quoted all four attributions; checked v4.0's harness assertion; reproduced the artifact.
**Evidence:** v1 line 440, v2 line 708 and v3.0 line 986 carry "off by 5.96 ducats on a node paying ~250" verbatim; v4.0 line 1076 carries "0.41%"; v5.0 line 1210 carries "redistributive and single-digit percent, with the sign varying by collector — Sevilla −0.82%, −0.87%, +7.44%"; `changes-v6.md:1118` carries the first draft's "at most **0.1%**". v4.0's harness did assert the deletion: `validate_v4.py:452` contains `hasnt("3.10", "the 5.96-ducat figure", "off by 5.96 ducats on a node paying ~250")`. My own run of `audit_f4.py` reproduces the artifact directly: per-good propagation gives per-collector errors of +7.255% at `sevilla` but only 0.004% at `gulf_of_siam` on the same construction, so the magnitude is a property of which node and which collectors are chosen rather than of the design.

## Y178 — no figure of the author's own is quoted here, because the identity holds and the objection is structural
**Status:** PARTIAL
**Method:** read §3.10's parenthetical in place and checked what figures the section carries.
**Evidence:** within its scope — the magnitude of the per-good-propagation error, which is what the parenthetical is about — the claim holds: every number in that parenthetical is attributed to v1 through v5 or to the first draft, and no replacement magnitude is offered. But §3.10 does quote two of the author's own figures elsewhere in the same section: the 0-to-3.7e-16 float residual and `gulf_of_siam`'s seven downstream sets. So "no figure of my own is quoted here" is false of the section and true only of the parenthetical.
**Should say:** no figure of my own is quoted **for the magnitude**, because the identity holds and the objection is structural. That is a one-word scope fix, and it is the smaller change than deleting the two figures — both of which are correct and both of which the section needs.

---

# §3.13 — Open questions

## Y179 — the open wealth question is now a design question rather than a classification one, since §1.3 reads development, the trade good and the four province-state modifiers and nothing else
**Status:** CONFIRMED
**Method:** read §3.13's wealth bullet against §1.3 and the solver.
**Evidence:** the question is posed as "Should any source beyond province condition be allowed to multiply `goods_produced`?" — a decision about scope, not about how to classify a given modifier, because the model has no classifier left to apply. The premise is confirmed at Y026 and Y033–Y035: the solver reads exactly those inputs. Y047's caveat — the choice of four is itself a judgement, and `unrest` is a live province-state tax modifier the model omits — qualifies the premise without changing the character of the question.

## Y180 — trade_goods_size and trade_goods_size_modifier are granted in buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments
**Status:** CONFIRMED
**Method:** grepped each of the eight directories for both keys.
**Evidence:** all eight grant at least one. Buildings `00_buildings.txt:2216` (`trade_goods_size = 1.0` in a manufactory modifier); event modifiers `00_event_modifiers.txt:176` and `:362`; great projects `01_monuments.txt:3609` and `:9724`; static modifiers `00_static_modifiers.txt:252` and `:454`; province-triggered modifiers `00_modifiers.txt:867` (3.0) and `:1189` (5.0); holy orders `00_holy_orders.txt:30` (`trade_goods_size_modifier = 0.1`); state edicts `zzz_urbanization.txt:13` (0.33) and `zzz_chinese_industrialization.txt:12` (0.2); trade-company investments `00_Investments.txt:206` (0.15, `brokers_office`) and `:227` (0.3, `brokers_exchange`).

## Y181 — re-admitting any of those sources re-admits the maintenance burden, so the question is whether the fidelity is worth about one percent of world wealth either way the ratio is taken
**Status:** CONFIRMED
**Method:** checked the "one percent" against Y004 and the maintenance premise against Y005.
**Evidence:** the apparatus was 0.98% of the field with it and 0.99% of the field without — about one percent either way, exactly, and the "either way the ratio is taken" hedge is doing real work rather than decorating. The maintenance premise is the audit history: the classification it required was refuted in both audits that examined it and passed by v4.0's own harness.

## Y182 — under the calibration's alpha = 16 the cloves demand order is hangzhou, beijing, doab, and the sink lands on a high-demand node rather than a geographic accident
**Status:** CONFIRMED
**Method:** computed the cloves demand vector at alpha = 16 on the v6.0 field, then ran the full §3.13 calibration — alpha unclamped at exponent 2, demand-mass quantile rho = 0.5, twig tolerance 3e-4 — via `final.py`.
**Evidence:** the demand order at alpha = 16 is **hangzhou, beijing, doab**, then canton, lahore, genua. Under the full calibration the cloves sink set is **['beijing']** alone, and `beijing` is demand rank **2** — a high-demand node, not a geographic accident. (At DRAIN defaults, without rho and the twig tolerance, the set is {beijing, genua, gujarat, kongo, timbuktu}, so the claim needs the full calibration — which is the configuration it is stated under.)

## Y183 — v2's "Beijing holds the richest single province" is wrong — that is hangzhou — with the 30.4/19.5 figures and the Deccan demand-rank claim no longer carried
**Status:** CONFIRMED
**Method:** found the richest counted province; quoted v2's and v5.0's sentences; grepped the v6 spec.
**Evidence:** the richest counted province is pid **1821 at 27.00**, in the `hangzhou` node; `beijing`'s best is pid 1816 at 19.50. v2 lines 775–777 read "Beijing, holding the richest single province, becomes the cloves sink". v5.0 lines 1301–1305 carried "**30.4 against Beijing's 19.5**" and "Deccan, **demand rank 2** under alpha = 16 ... becomes the cloves sink". In the v6 spec, "30.4" has **zero** hits and the Deccan demand-rank claim is gone, replaced by the alpha = 16 demand order of Y182.

---

# §3.15 — Rejected

## Y184 — the Laplacian entry keeps the sparsity argument, no longer maintains a copy of §3.2's contrast measurement, and adds that cloves has a single producer and so no contrast to measure at all
**Status:** CONFIRMED
**Method:** read §3.15's Laplacian entry; measured cloves' producer count.
**Evidence:** the entry keeps "sinks land where the field is locally flat ... the supply signal is **sparse** rather than large", states that §3.2 carries the measurement and this entry does not maintain a copy of it, and adds the cloves observation. Measured: cloves is produced in **exactly 1** of 80 nodes, so its supply max/min ratio is 1.0 by construction — there is no contrast to measure. The sparsity point in miniature, as claimed, and the one number left in the entry is a fact about the game data rather than a score for the rejected operator.

## Y185 — ranked orientation is de-quantified: a far higher share of top-demand nodes in its sink sets than DRAIN, and it fails on delivery — a large share of world demand stranded, orphan sinks, net-producer sinks where DRAIN, LAP and FLOW post none, and several times DRAIN's sinks per good
**Status:** CONFIRMED
**Method:** ran `rankop.py` and `rankrep.py` on the v6.0 field, then measured stranded demand, orphan sinks and net-producer sinks for RANK, DRAIN and LAP myself.
**Evidence:** P(sink | top-10 demand) is **46.6%** for RANK against DRAIN's 14.1% at the same cut (16.8% at a true decile) — far higher, as claimed. Delivery: mean unserved demand share **16.67%** for RANK against **0.0000%** for both DRAIN and LAP; **32** orphan sinks against 0 and 0; **8** net-producer sinks against 0 and 0. Sinks per good **12 to 17, mean 13.3** against DRAIN's 1 to 8, mean 3.72 — 3.6x the mean, so "several times" is right. And Genoa is a cloves sink with **no directed path** from the sole cloves producer (`the_moluccas`), the named failure. Every clause verified, and the entry carries no figures — which is the correct form, since the shares move with the field.

## Y186 — seeded basin growth leaves demand unserved at every tuning tried; the 88.4%-reach figure is dropped
**Status:** CONFIRMED
**Method:** ran `basin.py` on spices at seed counts 1, 3, 5, 8 and 13; grepped the spec for 88.4.
**Evidence:** unserved demand **0.4518, 0.5303, 0.5009, 0.4994, 0.4619** at S = 1, 3, 5, 8, 13 — 45% to 53% unserved at every tuning tried, with unserved equal to stranded in each case. "88.4" has **zero** hits in the v6 spec. Dropping it was doubly right: the same sentence read 88.5% in v2 and v3.0 and 88.6% in v4.0, so the figure had already drifted three times without the argument changing.

## Y187 — the 3-mass gravity kernel reproduces whatever end count it is seeded with while gamma is small enough and loses that property as gamma approaches 1; and a pure wealth^alpha edge comparison with no reach term does not concentrate ends at all
**Status:** CONFIRMED
**Method:** built the kernel Phi(n) = max over m of c_alpha(m) x gamma^dist(n,m) over the top-k pairwise-unconnected demanders and counted ends at gamma in {0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99} for k = 1 to 6; then counted ends under a pure wealth^alpha endpoint comparison at alpha in {0.5, 1, 1.5, 2, 4, 8, 16, 32}.
**Evidence:** for gamma at or below 0.7 the end count equals the seed count **exactly for every k from 1 to 6**; at gamma = 0.9 the 5- and 6-mass fields both give 4; at gamma = 0.95 the 4-, 5- and 6-mass fields all give 3; at gamma = 0.99 every k gives 1. The property holds while gamma is small and fails as gamma approaches 1, as stated. The pure comparison never concentrates: ends are 15, 15, 13, 14, 11, 10, 12, 12 across those eight alphas — never fewer than 10, because a local wealth maximum survives every positive alpha. No figures are maintained in the entry.

---

# §3.16 — Evidence standard

## Y188 — failure mechanism 3 is restated with both magnitudes: the alpha = 1 identity's residual reached 1e-5 against v1's epsilon of 1e-6
**Status:** CONFIRMED
**Method:** located v1's epsilon and its measured residual; re-ran the literal instantiation through `final.py`; compared against v5.0's wording.
**Evidence:** v1's spec line 46 gives `s <- (1 - eps) x s + eps/N` with `eps ~ 10^-6`. v1's `validation.md:4921` records "`eps=1e-6 -> 1.151e-05`" for the spec-literal reading. Re-run on the current field, `final.py` reports **V204(a) eps on per-good s only: rel residual 9.11e-06** against **V204(b) eps on both sides: 1.22e-15** — the residual is of order 1e-5 when the identity is instantiated as written and vanishes when epsilon is applied to phi-0's supply as well. v5.0 lines 1454–1456 carried only one magnitude ("the identity failed at 1e-5"); v6.0 carries both, which is what the row claims and what makes the failure legible.

---

# Report

## Counts by status

| Status | Count |
|---|---|
| CONFIRMED | 168 |
| PARTIAL | 19 |
| REFUTED | 1 |
| UNVERIFIABLE | 0 |
| **Total** | **188** |

No claim was graded UNVERIFIABLE. Three rows rest on in-game tooltip readings that only a running game could re-take (Y039, Y041, Y043); all three are graded on the arithmetic those readings imply, which is checkable and exact, and each section says so. Two rows are OUTCOME claims about a mod that does not exist yet (Y115, Y120); both are graded on the file evidence their mechanism rests on, and Y120 records the one scope the install does not settle.

## REFUTED, with the reason

- **Y134** — an **attribution** error, so the fix is wording rather than arithmetic. No v1–v5 spec contains the figure 580 (it comes from `v5-owner-agnostic/fixes-agreed.md:223-229` and four earlier v6 claim drafts), and the script that computes it does exist in the tree at `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. The arc-permutation half of the sentence is correct.

## PARTIAL, with the reason

- **Y008** — the no-absolutes convention is stated but not enforced in sections the pass never opened: §3.6's "provably cannot survive", §3.9 and §3.15's unscoped "most self-coherent aggregate measured", §3.5's "nothing sits below the 2.0 anchor".
- **Y010** — "three successive audits" holds only for the Laplacian contrast; two re-measurements CONFIRMED rather than refuted; and the Laplacian rejection argument did depend on the contrast ratio until v4.0 replaced the premise.
- **Y015** — "about a dozen" checks, but unguarded figures are roughly 265 of 303 distinct numeric tokens, about 22x rather than 3x. **Say less:** drop the ratio.
- **Y016** — `coverage6.py`'s denominator is 9 of `measure6.out`'s 60 keys after two filters, with 25 more unscored; not "each spec-printed figure".
- **Y047** — `00_static_modifiers.txt` grants a wealth key in 25 blocks, and `unrest` is province state and live on 21 counted provinces at 1444, so "four" is a classification judgement rather than a file fact.
- **Y080** — the sink set came back 57, 62 and 60 times of 800 across three independent sets, not 64, and the seeds are unstated. **Say less:** "about 7–8% of runs".
- **Y083** — `gulf_of_siam` (52.6–57.3%) is more frequent than `english_channel` (39.4–42.0%), so "after `english_channel` the most frequent ends are `gulf_of_siam`" mis-ranks them.
- **Y084** — none of the four quoted 800-trial ranges reproduces. **Say less:** one significant figure for the leaders, no ranges for the trailers.
- **Y086** — the LP objective deviates by up to 6.66e-16, above the claimed 4.44e-16, and the figure is attributed to a script that does not compute it.
- **Y092** — §3.9 prints "7 of 14 on the 1444 field" for `Phi_ord` six lines before saying no figure is maintained for it. **Say less:** delete the parenthetical, keep "half".
- **Y100** — the basin is 18 at x1.00 and 28 at x1.44 but non-monotone in between, peaking near 31 at x1.32, so "grows from 18 to 28" is not the trajectory.
- **Y106** — the maximum difference is 3.55e-15, not 0.0, which is `round(..., 12)`. **Say less:** state that the sink sets are identical and drop the residual.
- **Y108** — v5.0's Channel route existed on v5.0's field and was CONFIRMED edge by edge; v6.0's own field change is what makes `english_channel` a sink.
- **Y117** — the appositive enumerates all nine entries, not the seven; the rate-limited seven are three twinned families plus `propagate_religion`. Wording fix.
- **Y129** — on re-run, 2, 6 and 1 of 12 runs landed inside v5.0's interval, not 1, 0, 0. **Say less:** drop the count, keep the range.
- **Y132** — same objective-bound overrun and the same misattribution; the 400/400, mean-25, different-vertex and no-tiebreak halves are exact.
- **Y143** — `game-session.md` records two country-node observations, not one (France in Sevilla and Castile in Safi), so the single-observation marker does not apply.
- **Y168** — "the count is a property of the field, not the operator" is imprecise on both sides: alpha_Phi also sets it, and `Phi_ord` gives 14 ends on the identical field.
- **Y178** — true of the parenthetical, false of the section: §3.10 quotes the author's own 0-to-3.7e-16 residual and seven-downstream-sets count. One-word scope fix.

## Where the honest correction is to say less rather than to restate a number

Seven of the nineteen partials are figures quoted more precisely than their sample supports, and in each the smaller and safer repair is deletion:

- **Y080** and **Y084** — counts and ranges over 800 random relabellings. Three independent 800-trial sets give three different answers, which is the paragraph's own thesis; the leading proportions to one significant figure are the only durable form.
- **Y086** and **Y132** — the LP objective bound. It is a floating-point artifact that grows with trial count; "identical to within a few units in the last place" needs no maintenance and is what the argument uses.
- **Y106** — the dev-versus-wealth scaling difference. The claim's content is that the sink sets are identical; the residual figure is noise either way it is printed.
- **Y129** — the count of timing runs inside v5.0's interval. It measures a scheduler. The observed total range is the part that will still be true on another machine.
- **Y092** — `Phi_ord`'s 7-of-14. The figure is correct but keeping it contradicts the sentence six lines below it, and "half of them terminate no good at all" carries the whole argument.

Two further partials are wording rather than arithmetic (**Y117**, **Y178**), two are attributions to prior versions that need re-scoping (**Y010**, **Y108**), and one — **Y047** — is the only partial whose repair adds rather than removes: `unrest` is a live province-state tax modifier on 21 provinces at the 1444 start, and the model does not read it.

## Two incidental findings, outside the Y rows

- **§3.5's `NEW_DRAPERIES` conclusion.** The base price, both key values and the 1.875 arithmetic all check, but the same `1540.1.1` block in `history/countries/HAB - Austria.txt` also applies `COTTON_IMPORTS = -0.10` to `wool` under a different key, so a campaign reaching 1540 holds two live negative keys and wool sits near 1.625 (if keys sum) or 1.6875 (if they compound), not 1.875. 1.875 is wool's single-event floor, which is the right figure for the 13/2/4/11 partition and the wrong one for the campaign statement. This proposition is carried as UNCHANGED in `claims-v6.md`, so it has no Y row.
- **`fixes-agreed.md` is stale.** It still records world wealth 10,594.70, connectivity 90.2% and 5,703 connected pairs — the pre-round-two field — so `verify6.py` reports 21 checks with 5 failed against it while reporting 29 checks with 0 failed against the spec. The two documents state the same quantities differently and the harness holds a typed literal for each, which is the defect class `every_site()` was added to catch.
