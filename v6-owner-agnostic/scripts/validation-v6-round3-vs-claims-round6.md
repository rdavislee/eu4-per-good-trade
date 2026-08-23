# Validation — Per-Good Trade Network Spec v6.0

Every claim in `claims-v6.md` (Y001–Y183) re-derived from primary sources. **No status is inherited
from any prior audit.** `validation-v5.md`, `validation-v3.md`, `validation-v2.md`,
`validation-v4.md`, the earlier `validation-v6.md` that graded a superseded Y-numbering, and the
`scripts/claims-v6-round*.md` drafts were opened only as *documents under examination* — never as
evidence for a verdict.

**Sources actually opened.** The 1.37.5.0 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` — `common/static_modifiers/`,
`common/prices/`, `common/tradegoods/`, `common/tradenodes/`, `common/defines.lua`,
`common/defines/`, `common/on_actions/`, `common/scripted_effects/`, `common/trading_policies/`,
`common/institutions/`, `common/great_projects/`, `common/event_modifiers/`,
`common/tradecompany_investments/`, `common/holy_orders/`, `common/state_edicts/`,
`common/buildings/`, `common/province_triggered_modifiers/`, `events/`, `missions/`, `decisions/`,
`history/provinces/` (all 3,923 files), `history/countries/`, `map/area.txt`, `map/continent.txt`,
`localisation/`; the save `save games\VANILLA_start.eu4` (`gamestate`, parsed independently of
`scripts/prov1444.json`); the shipped save `tutorial/eu4_tutorial_chapter10.eu4`;
`scripts/solver.py`, `drain.py`, `flowop.py`, `measure6.py`, `verify6.py`, `mutate6.py`,
`coverage6.py`, `pdx.py`, `toys.py`, `rankop.py`, `rankrep.py`, `drainrep.py`, `basin.py`,
`europe.py`, `provinces.py`, `nodes.json`, `prov1444.json`, `measure6.out`,
`preconfirm3-relabel.out`, `r06.py`, `r10.py`, `r21.py`, `r24.py`;
`../v5-owner-agnostic/scripts/_audit_b_drain.py`; the v1–v5 specs, claim inventories and validation
documents; `changes-v6.md`, `fixes-agreed.md`; and `per-good-trade-spec.md` itself.

**Method split.** Derivations are checked as arguments; measurements are checked by re-running them.
Where a claim carries both, the two verdicts are stated separately inside the section. New scratch
scripts (`m2.py`, `m4.py`–`m9.py`, `relabel.py`, `relabel2.py`, `perg.py`, `caravan.py`) were written
under `%TEMP%\v6audit\`; none of the project's own files was modified.

## Instrument validation, done first

Three instruments carry most of the numeric load, and each was validated before use.

1. **`measure6.py`.** Re-run from a clean shell: it reproduces `scripts/measure6.out` **byte for
   byte** (60 labelled figures). It is not an independent instrument — it `import`s `solver.py`'s
   `ROWS`, `PROV`, `PRICES` and `drain.py`'s `run_drain` directly, so it *is* the shipped
   implementation with a print harness. Its one re-derivation, the demand share `cv()`
   (`(w/w.max())**a` then normalise), is algebraically identical to `solver.build_sc`'s
   `w**a / Σw**a`. **One check inside it is vacuous** and is flagged at Y103: the
   "dev-scaling equals wealth-scaling (max diff) 0.0" line compares `W*k` against `W*k`.
2. **`_audit_b_drain.py`** (the five-phase reimplementation used for every node-order result).
   On the identity permutation of `Φ_w` it returns core 80, **159 of 159** edges, 2 promotions,
   0 fallbacks, sinks `{english_channel, hangzhou}`, and an orientation **set-identical** to
   `drain.py`'s (symmetric difference 0 edges). It is a faithful instrument.
3. **The relabelling harness itself needed correcting.** A first attempt permuted node indices but
   left the canonical edge list in its original order; it reported **0 of 400** orientation changes.
   `solver.py` builds `EDGES_UND = sorted(set(tuple(sorted(e))))`, so a genuine relabelling re-sorts
   the arc list in the new label space. With that fixed the same harness reports 400 of 400 changes.
   A pure row permutation of the LP (columns untouched) changes nothing; permuting the arc
   *presentation* order is what moves the optimum. Every node-order verdict below rests on the
   corrected harness, and the false-negative variant is recorded because it does not announce itself.

`verify6.py` on the shipped spec: **29 checks, 0 failed**. `mutate6.py` on the shipped spec:
**12 of 12 caught**. `coverage6.py`: **8 of 10** uniquely-locatable spec figures protected, with
23 further computed figures declined as ambiguous and 27 of 60 absent from the spec text.

---

## Summary

| Status | Count |
|---|---|
| CONFIRMED | 158 |
| PARTIAL | 24 |
| REFUTED | 1 |
| UNVERIFIABLE | 0 |
| **Total** | **183** |

### REFUTED

| ID | One-line reason |
|---|---|
| Y140 | "`hangzhou` holds an end under **every** relabelling tried" is false and contradicts §1.6's own 97–100-per-hundred figure; measured 96–100 per hundred over four independent seeds, so the razed-China row rests on a universal quantifier the document elsewhere withdraws. |

### PARTIAL

| ID | One-line reason |
|---|---|
| Y005 | The two cited v5.0 IDs do not refute the classifier — X030 is PARTIAL and X034 is CONFIRMED (and is about v4.0); the actual refutation is X035, and W041 audited v3.0's *pre*-two-test rule. |
| Y008 | The no-absolutes convention is coherent but the document does not obey it: §2.8 still asserts "under every relabelling tried" (Y140). |
| Y009 | True of §3.15, false of the convention as stated: §3.2 still maintains four figures for the rejected v1 Laplacian (×1.7 and 3.61×/4.12×/4.60×/4.77×). |
| Y010 | Three audits did re-measure them (v2, v3, v5 — not v4), but §3.9's rejection argument *does* rest on a number: "a majority terminate no good at all" is 7 of 14 on v6.0's own field, exactly half. |
| Y012 | Three of the spec-path figure needles (13.40, 15, 93) are typed literals rather than the computed values `measure6.py` already exposes, so those three cannot fail if the install changes. |
| Y013 | "About a dozen" script citations confirmed (15) and "under half guarded" confirmed, but the unguarded figure count is nearer five times the citation count than three times. |
| Y014 | `coverage6.py` does **not** corrupt each spec-printed figure: it scores 10 of the 60 figures `measure6.py` computes, declines 23 as ambiguous, and never touches a printed figure `measure6.py` does not compute. |
| Y027 | The two-test classifier is v4.0's, not v3.0's — v3.0 defended the property with a single structural rule (`v3:160–164`). |
| Y042 | "Nothing finer" contradicts the sentence immediately before it, which draws the finer conclusion that the engine multiplies the *untruncated* monthly value. |
| Y046 | The devastation-linearity half is confirmed; `prosperity`'s *direction* **is** in the file (`00_static_modifiers.txt:466`, `+0.25`) — what no file fixes is whether it scales with the prosperity level. |
| Y078 | "5 to 10 runs per hundred" measured **4 to 12** over four independent seeds, and the project's own `preconfirm3-relabel.out` contains a fifth seed at 12. |
| Y079 | Measured `hangzhou` **96–100** (not 97–100) and `english_channel` **31–47** (not 37–44) over four independent seeds plus the harness's own fifth seed. |
| Y081 | `gulf_of_siam` ~half and `wien` ~a third confirmed; `sevilla` measured **8–19 per hundred**, nearer a tenth to a sixth than "a fifth". |
| Y083 | Fully-oriented, acyclic and zero-fallback confirmed; the LP objective's deviation is **4.44e-16**, not "identical to 2.22e-16". |
| Y097 | Asia losing its end over a broad range is confirmed (none from ×1.56 to ×4.00); "the Channel's basin grows" holds only to ×1.56 — at ×1.70 the Channel is not an end at all and `genua` holds all 80 nodes. |
| Y123 | v5.0's interval is quoted correctly, but "1, then 0, then 0" does not reproduce: six replicates of twelve gave 6, 6, 5, then 2, 1, 2 runs inside [0.17, 0.21] s. |
| Y125 | The coefficient-provenance half is confirmed for v3.0, v4.0 and v5.0; the *whole-install* modifier sweep is v5.0's alone — v4.0 stated the rule and swept one directory, v3.0 had neither. |
| Y128 | 580/580, "different optimal vertex every time, never a sweep tiebreak" and 8.9e-16 all reproduce exactly; the mean is **21.39** of 159 at an independent permutation seed, not 22.1. |
| Y146 | The four figures reproduce **exactly** — but as multiples of the node's *wealth*, not of its demand; as demand multiples they are 6.9×, 8.4×, 9.9× and 10.4×. |
| Y147 | The shares-don't-line-up derivation is sound; "other nodes in the region need more still" fails for `girin`, which needs **3.89×** — less than `hangzhou`, `xian` and `canton`. |
| Y155 | The v5.0 half is confirmed (no assertion anywhere in its toolchain); `verify6.py`'s "guard" is a literal-anchored substring needle on the *document*, not a per-file count assertion, and `measure6.py`'s walker still swallows parse failures with a bare `except`. |
| Y158 | Φ_ord's higher self-coherence (60.4% vs 53.6%), the absent demand capitals and the non-concentrating end count all confirm; "**a majority** terminate no good at all" is false — 7 of 14, exactly half. |
| Y168 | "v1–v4.0's 5.96 ducats" is off by one version: the figure is v1 through v3.0; v4.0 deleted it and `v4/scripts/validate_v4.py:452` asserts its absence. |
| Y176 | §3.15 does drop the figures, but §3.2 does not carry them either — **no** section of v6.0 prints the contrast measurement, so the cross-reference points at nothing. |

---

# §0 — Front matter

### Y001 — v6.0's substantive change is to §1.3: wealth is a function of development, trade good and the province's own current condition, and of nothing else

**Status:** CONFIRMED
**Method:** `per-good-trade-spec.md:14–16`, read against `scripts/solver.py:province_table()`.
**Evidence:** The solver's per-province row reads exactly `base_tax`, `base_production`,
`trade_goods` (with the rolled good substituted) and `ON_STARTUP_DEVASTATION`. `STATE_GOODS_MOD`
and `STATE_TAX_MOD` hold only the four province-condition modifiers. No owner, autonomy, efficiency,
idea, great-project, permanent-modifier or trade-good-modifier term appears anywhere in the file.

### Y002 — v6.0 keeps v3.0's owner-agnostic wealth and makes it true by construction rather than by a rule that has to be policed

**Status:** CONFIRMED
**Method:** Diffed the input surface of `solver.py` against `v3-owner-agnostic/scripts/solver.py`;
grepped the v6.0 spec for the classifier vocabulary.
**Evidence:** v3.0's solver read a modifier classification; v6.0's reads four bare province fields
plus a fixed four-entry static-modifier table. `Two tests`, `can_use_modifiers_trigger`,
`stora_kopparberget`, `production_leader` and `centers_of_trade` appear **0 times** in the v6.0 spec.
There is no rule left to police because there is no classification decision in the input path.

### Y003 — the two-test classifier and everything it governed are deleted, along with the whole-install sweep

**Status:** CONFIRMED
**Method:** `grep -c` over `per-good-trade-spec.md` for each governed item; inspection of every
shipped script for a modifier sweep.
**Evidence:** `Two tests`, `can_use_modifiers_trigger`, `stora_kopparberget`, `production_leader`,
`centers_of_trade` → **0 hits each**. No script under `scripts/` walks `common/` for modifiers;
`measure6.py`'s only `common/` reads are `static_modifiers` (one regex for
`provincial_production_size`), `prices`, `defines.lua` and the `change_price` census. The sweep is
gone, not merely unused.

### Y004 — the deleted apparatus was worth 105.30 ducats: 0.98% of 10,712.70 with it, 0.99% of 10,607.40 without

**Status:** CONFIRMED
**Method:** Rebuilt the v5.0 field on v6.0's counted set (2,472 provinces, rolled goods, `on_startup`
devastation) with `gems` +15% tax, `incense` +10% trade value, the six great projects and the ten
permanent province modifiers, reading each flat `trade_goods_size` from
`common/event_modifiers/` rather than assuming it (`m4.py`).
**Evidence:** Field **with** the apparatus **10,712.70**; without **10,607.40**; difference
**105.30**; 105.30/10,712.70 = **0.983%**, 105.30/10,607.40 = **0.993%**. Flat values read from the
files: `granary_of_the_mediterranean` 2.0, `skanemarket` 2.0, `icelanding_fisher_sea` 1.0,
`diamond_mines_of_golconda_modifier` 4.0, `jingdezhen_kilns` 2.5, `coffea_arabica_modifier` 3.0.

### Y005 — the classification was wrong in both independent audits that examined it (validation-v3 W041, validation-v5 X030 and X034) and passed by v4.0's own repair harness, which v5.0 then refuted

**Status:** PARTIAL
**Method:** Read the graded entries for W041 (`v3-owner-agnostic/validation-v3.md:68`, `:644–645`),
X030 (`v5:751–756`), X034 (`v5:772–775`) and X035 (`v5:777`); located v4.0's harness
(`v4-owner-agnostic/scripts/validate_v4.py`, `validate_v4b.py`) and **re-ran both**.
**Evidence (derivation half):** The two cited v5.0 IDs do not carry the weight the sentence puts on
them. **X030 is PARTIAL** — it flags that the locality test's own attribute list does not cover
`devastation`/`occupied`/`under_siege`/`prosperity`. **X034 is CONFIRMED**, and it is a claim *about
v4.0* ("v4.0 stated the rule and then swept only `common/tradegoods/`"), not a refutation of v5.0's
classifier. The v5.0-side refutation of the classifier's application is **X035**, "REFUTED (the
enumeration is incomplete and miscounts)", which the sentence does not cite. **W041** is REFUTED,
but it audits v3.0's *structural* rule ("the income-relevant local ones are exactly three"); the
two-test classifier first appears at `v4:184`.
**Evidence (measurement half — CONFIRMED):** `validate_v4.py` → 163 checks, 0 failed;
`validate_v4b.py` → 40 checks, 0 failed, both on re-run. Section A is headed
"W041 / W040 / W160 - the two-test local-modifier rule" and all 8 checks pass, including
`has("W074", "spec item 4 names both modifiers", "`gems` (+15% tax, 43 provinces) and `incense`")` —
the exact sentence X034 quotes as wrong. So "passed by v4.0's own repair harness, which v5.0 then
refuted" is reproducible.
**Should say:** cite **X035** (and X030 as the internal-inconsistency finding) for v5.0, and
**W040/W041** for v3.0's predecessor rule, or drop the ID list and say "in every audit that examined
the input surface".

### Y006 — three start-state reads are corrected in the same pass

**Status:** CONFIRMED
**Method:** Each of the three verified independently — see Y049/Y051/Y053 (`on_startup`), Y056
(dated `add_base_*`), Y057 (`is_city`).
**Evidence:** All three corrections hold against the install and the save: 11 devastated counted
provinces applied by `flavor_boh.15`; province 1 (Uppland) `base_tax = 5` undated plus
`add_base_tax = 1` at `1436.4.28` against a save value of 6.000; 20 owned provinces with no
effective `is_city = yes`, and 2,472 counted rather than 2,452.

### Y007 — the reason a canonical node order is a correctness requirement is Phase 2's degeneracy, not the priority key's index tiebreak

**Status:** CONFIRMED
**Method:** 29 goods × 20 relabellings on the validated five-phase instrument, recording for each
changed run whether the LP's *flow support* changed or only the sweep's output (`perg.py`); plus a
full priority-key tie census on 1444 (`perg.py`).
**Evidence:** 580 of 580 runs changed the orientation; **580 of 580 changed the flow support**, and
**0 changed with the support held fixed** — so no change is attributable to a sweep tiebreak. The
key never ties on 1444: 0 exact `(DEF, β)` ties among free-edge-incident core nodes across 29/29
goods, 0 within-cluster β argmin ties, 0 tied cluster masses. Degeneracy is the whole mechanism.

### Y008 — prose convention: no empirical absolutes

**Status:** PARTIAL
**Method:** Read the convention at `per-good-trade-spec.md:28–31`, then tested the document against
it.
**Evidence:** The convention is internally coherent and the stated rationale (that quantifier
strength rather than provenance is where the document breaks) is supported by this audit's own
result — the single refutation and eight of the twenty-four partials are quantifier or interval
failures, not provenance failures. But the document does not obey it. §2.8's razed-China row asserts
"which it does under **every relabelling tried**", a universal quantifier about the world, and it is
false (Y140). §1.6, four hundred lines earlier, states the same quantity as "97 to 100 per hundred".
**Should say:** the convention stands; §2.8's row needs the same scoping §1.6 gives it.

### Y009 — prose convention: no maintained figures for any rejected operator

**Status:** PARTIAL
**Method:** Grepped the v6.0 spec for every figure the prior versions maintained for Φ_ord, the
gravity kernels, the v1 Laplacian, RANK and the seeded basins.
**Evidence (the §3.15 half — CONFIRMED):** `60.3` 0 hits, `62.7` 0, `61%` 0, `88.4` 0,
`97 of 159` 0, `110 of 159` 0, `13 end nodes` 0, `4–97` 0, `211` 0, `20,400` 0, `15,010` 0. §3.15's
five graveyard entries carry design arguments and no numbers.
**Evidence (the convention as stated — refuted):** §3.2 maintains four figures for the rejected v1
Laplacian: "better wealth inputs move Genoa to a *co-*sink at roughly **×1.7**" and
"**3.6–4.9×** … `beijing` **3.61×**, `hangzhou` **4.12×**, `xian` **4.60×**, `canton` **4.77×**".
Those are measurements of a rejected operator, maintained.
**Should say:** scope the convention to §3.15's graveyard, or add §3.2's Laplacian thresholds to
what it covers.

### Y010 — those rejected-operator numbers were re-measured and re-refuted in three successive audits and not one of the rejection arguments depends on them

**Status:** PARTIAL
**Method:** Counted engagements with the rejected-operator figures in each audit document; then
re-measured every empirical clause of §3.9's Φ_ord rejection on the v6.0 field (`m7.py`, `m9.py`).
**Evidence (the history half — CONFIRMED, with a correction):** `62.7` appears 11× in
`validation-v2.md` and 3× in `validation-v3.md`; `60.3` appears 7× in `validation-v5.md`; gravity,
basin and RANK figures appear in all three. **`validation-v4.md` engages none of them** (0 hits on
both), so the three audits are v2, v3 and v5 — successive inventories, but not successive versions.
**Evidence (the independence half — refuted):** §3.9's Φ_ord rejection is four clauses and three of
them are measurements. Re-measured on the v6.0 field: Φ_ord has **14** end nodes of which **7**
terminate no good — exactly half, not "a majority"; no demand capital
(`genua`, `english_channel`, `hangzhou`) is among them; and the end count is **14 at every**
cloves-α in {2, 4, 8, 16, 32, 64}, so it does not concentrate. So one rejection argument does depend
on a number, and that number has moved across the wealth-field change.
**Should say:** "…and the rejection arguments that remain are directional" — and fix the majority
clause (Y158).

### Y011 — every graded claim from validation-v5.md (22 refuted, 39 partial, 1 unverifiable) is folded through, and fixes-agreed.md maps each one

**Status:** CONFIRMED
**Method:** Read `validation-v5.md`'s summary table and independently recounted its 196 per-claim
`**Status:**` lines; then cross-checked `fixes-agreed.md`'s mapping table row by row against them.
**Evidence:** Summary table and recount agree exactly — CONFIRMED 134, PARTIAL 39, REFUTED 22,
UNVERIFIABLE 1, total 196 over X001–X196. `fixes-agreed.md` carries **62** rows with 62 unique IDs;
validation-v5's non-CONFIRMED set is 22 + 39 + 1 = **62**; the two sets are equal (nothing open and
unmapped, nothing mapped and not open), and the `was` column matches validation-v5's status on all
62 with **0 mismatches**. Action tallies sum to 62.

### Y012 — verify6.py reads figures out of the document text and fails when they disagree with a value computed from the install, but does not cover every figure the document prints

**Status:** PARTIAL
**Method:** Read `scripts/verify6.py` in full; ran it on the spec; counted the figures it anchors
against `O = measure6.OUT` versus against typed literals; counted the spec's printed figures.
**Evidence (confirmed):** The harness reads the document (`io.open(path).read()`), builds each
needle from a value and requires both presence and internal consistency across phrasings
(`shows()`, `every_site()`). It routes by content, not filename (`verify6.py:185–196`) — the defect
`changes-v6.md` records as round three's find. On the spec: **29 checks, 0 failed**. It plainly does
not cover everything: the spec prints **108** bolded numeric figures and the 21 figure checks span
roughly 30 numbers.
**Evidence (the gap):** three of the spec-path figure needles are **typed literals**, not computed
values — `shows(doc, "spec: devastation cost", …, 13.40)` at line 163,
`shows(doc, "spec: max base_tax province", …, 15, ROWS_MAXPID)` at 164–165, and
`shows(doc, "spec: change_price by tree", "{} in `events/`", 93)` at 168. All three quantities *are*
in `measure6.OUT` (`devastation cost in ducats`, the max-`base_tax` sweep, `change_price by tree`),
so they were available and typed anyway. Those three checks would still pass if the install changed.
The checklist path (`run()`) is worse — `5703`, `0.0227`, `1.70`, `3.51`, `132`, `27.00` and `8` are
all literals, and it currently fails 5 of 21 on the stale `fixes-agreed.md`, including a needle
hard-coding `5,703` where the install now yields **5,663**.
**Should say:** "…fails when they disagree with a value computed from the install, except for three
needles that still carry typed literals."

### Y013 — under half of the printed figures are guarded; a script is named about a dozen times against roughly three times that many unguarded figures

**Status:** PARTIAL
**Method:** Counted `.py` citations in the spec; counted bolded numeric figures; ran `coverage6.py`.
**Evidence:** Script citations: `measure6.py` 7, `verify6.py` 3 (one as `scripts/verify6.py`),
`coverage6.py` 1, `mutate6.py` 1, `europe.py` 1, `toys.py` 1, `pdx.py` 1 — **15 citations over 7
distinct names**, so "about a dozen" is right. Bolded numeric figures in the spec: **108**.
`verify6.py`'s 21 figure checks span ~30 of them, so "under half are guarded" is right by a wide
margin. `coverage6.py` corroborates the gap: of the 60 figures `measure6.py` computes, 10 are
uniquely locatable in the spec (8 caught, 2 missed) and 23 more appear but ambiguously.
**Evidence (the ratio — wrong):** ~78 of the 108 bolded figures are unguarded, which is roughly
**five times** the 15 citations, not three times. And the "most recent additions carry neither a
guard nor an attribution" clause holds: the 400-relabelling figures (25 of 159, 97–100, 37–44,
5–10 per hundred, 60 of 60), 22.1, 580/580, 16.8%/6.9%, 226.7/143.0, 296.0/297.9/266.5/316.6,
3.7e-16, ×1.65/×2.15, ×2.9–×3.5 and the seven downstream sets carry neither.
**Should say:** "roughly five times that many unguarded figures".

### Y014 — coverage6.py measures coverage honestly: it corrupts each spec-printed figure whether the harness looks at it or not, and should be re-run rather than quoted

**Status:** PARTIAL
**Method:** Read `scripts/coverage6.py`; ran it.
**Evidence:** The "re-run rather than quoted" half is right and the script says so itself. The
denominator claim is not. `coverage6.py` iterates `measure6.out`'s 60 keys, keeps only renderings
that occur **exactly once** in the spec, and scores those: **10 targets, 8 caught, 2 missed (80%)**,
with **23** further computed figures listed as ambiguous and *unscored*, and 27 absent from the spec
text. Every printed figure `measure6.py` does not compute — 22.1, 580/580, the four relabelling
frequency bands, 16.8%/6.9%, 3.61×/4.12×/4.60×/4.77×, 226.7/143.0, 105.30, 12.70, 2.40, 3.7e-16,
×1.65/×2.15, ×2.9–×3.5, the seven downstream sets — is never touched at all. So it is an honest
measurement of a **wider** denominator than `mutate6.py`'s, but not of "each spec-printed figure".
**Should say:** "it corrupts every figure `measure6.py` computes that the spec prints uniquely,
whether the verifier looks at it or not — a wider denominator than `mutate6.py`'s and still not the
whole document."

### Y015 — mutate6.py reports a higher score and is not coverage: it plants errors only in figures verify6.py already checks, so it cannot fail

**Status:** CONFIRMED
**Method:** Read `mutate6.py:_spec_mutations()`; matched its 12 mutation targets against
`verify6.py:run_spec()`'s checked set; ran it on the spec.
**Evidence:** **12 of 12 caught.** All twelve targets — world wealth, counted provinces,
self-coherence, value-weighted self-coherence, sinks-per-good mean, connected pairs, largest `|b_w|`,
the α band, European provinces, coal flips, coal delta, price census — are checks `run_spec()`
already performs. There is no target outside the checked set, so the score is guaranteed by
construction. The circularity is exactly as described and is recorded rather than hidden.

---

## §1.1 — Trade direction

### Y016 — the fallback branch fires only when every candidate is support-isolated with zero post-peel balance; the key reads the balance Phase 0 hands on

**Status:** CONFIRMED
**Method:** Read `drain.py:sweep_priority()` and `phase0()` as an argument; confirmed against
`toys.py` T3.
**Evidence:** At a stall the candidates are the unmarked nodes with `cnt == 0`. A candidate with a
flow out-arc satisfies `ready()` and is never a stall candidate; a candidate with
`inflow > ZERO_TOL` is a flow-terminal demander and takes the *promotion* branch. So the fallback
requires every candidate to have no flow arc in either direction — support-isolated. The LP serves
`β`, so `β[v] ≠ 0` forces at least one incident flow arc; support-isolation therefore implies
`β[v] = 0`. And `β` is `phase0`'s return value with each pendant folded into its parent
(`beta[u] += beta[v]`), which is what both `DEF` and the key's second component read. A map with
non-zero raw balances whose folds cancel reaches the branch.

### Y017 — on a connected core the branch needs the folded balance to vanish across the core; uniform per-province wealth does not deliver that

**Status:** CONFIRMED
**Method:** Derivation as above, then an empirical necessity test: 4,000 random connected graphs of
4–8 nodes with minimum degree 2, half given integer mean-zero balances and half all-zero, run
through the validated five-phase instrument (`m9.py`).
**Evidence:** A fallback fired in **2,002 of 4,000** runs, and those 2,002 are *exactly* the runs
whose folded balance is zero at every node. **Zero** runs fired a fallback with a non-zero folded
balance anywhere in the core. So the condition is necessary as well as sufficient on this sample.
The two instantiations are right: for a per-good graph the folded balance vanishes iff the component
has no producer and no consumer; for `Φ_w`, `b_w(n) = 1/N − c_w(n)` vanishes iff every node's
`Σ wealth^α_Φ` is equal.

### Y018 — ⚑ uniform per-province wealth does not deliver that, because nodes hold between 0 and 72 counted provinces

**Status:** CONFIRMED
**Method:** Counted `ROWS` per node (`m2.py`); cross-checked `nodes.json` against
`common/tradenodes/00_tradenodes.txt` (80 nodes, identical member lists).
**Evidence:** Counted provinces per node run **0 to 72** — `cape_of_good_hope` is the unique 0,
`mexico` the unique 72; the 80 counts sum to 2,472. With equal per-province wealth the node sums are
proportional to those counts, so they cannot all be equal.

### Y019 — where the wealth key ties, the node index decides

**Status:** CONFIRMED
**Method:** Read `drain.py:sweep_priority()` line
`s_star = max(gated, key=lambda v: (NODEW[v], -v))`.
**Evidence:** Ties in `NODEW` are broken by `-v`, whose maximum is the smallest index. `NODEW` is
built once from `solver.ROWS` and is good-independent, so it needs no bootstrap, as §1.1 says.

### Y020 — §2.8 asserts containment over a set that includes the fallbacks, and the reason is T3, not the wealth tie

**Status:** CONFIRMED
**Method:** Ran `toys.py`; read §2.8's "Sink set, 2-core" row and §3.2's T3.
**Evidence:** T3 output: triangle A, B, C with `b = 0` everywhere and wealth 3, 2, 1; Phase 1
selects nothing; the fallback promotes A; free edges orient B→A, C→A, C→B. `actual sinks = ['A']`,
`formula set = []`, `sink inside {selected} ∪ {promoted}: False`, `inside ∪ {fallbacks}: True`. The
wealth tie is not exercised (3, 2, 1 are distinct), so it is incidental exactly as claimed.

### Y021 — the fallback branch is not the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2

**Status:** CONFIRMED
**Method:** As Y007.
**Evidence:** On 1444 no fallback ever fires — 0 across 29/29 goods, 0 across 400 relabellings of
`Φ_w`, 0 across 580 per-good relabelled runs — while the orientation changes in 100% of relabelled
runs. The order requirement therefore cannot be carried by the fallback branch or by any index
tiebreak: all four tie sites have exactly zero ties on 1444.

### Y022 — on 1444 the pendant and fallback cases are empty and the sink set is exactly {selected ∩ flow-terminal} ∪ {promoted} — 29/29 goods, 1–8 sinks per good, mean 3.72, zero fallbacks

**Status:** CONFIRMED
**Method:** Recomputed the formula set and the containment set from `run_drain`'s own `S0`,
`promotions`, `fallbacks` and `flow_arc` for all 29 live goods (`m2.py`).
**Evidence:** equality **29/29**; containment **29/29**; sinks per good **min 1, max 8, mean 3.72**;
fallbacks **0**; acyclic **29/29**; Phase-0 peel log length **0** (the vanilla map has minimum
degree 2, so the pendant case is empty).

### Y023 — the equality does not become a theorem by attaching conditions: T2 satisfies both and still breaks it

**Status:** CONFIRMED
**Method:** Ran `toys.py` T2 and read its construction.
**Evidence:** T2 is a five-cycle with a chord — minimum degree 2, so Phase 0 is a no-op — and its
output shows `promoted=[]` with no fallback line, so no fallback fires. Both attached conditions
hold. Yet `actual sinks = ['u2']` against `formula set = ['u1', 'u2']`, `EQUAL: False`. The
conditioned form is not a theorem.

---

## §1.3 — Demand

### Y024 — wealth reads exactly three things about the province and nothing else

**Status:** CONFIRMED
**Method:** `solver.py:province_table()` line by line.
**Evidence:** The only reads are `s["base_tax"]`, `s["base_production"]`, `s.get("trade_goods")`
(with `ROLLED[pid]` substituted where history says `unknown`) and `ON_STARTUP_DEVASTATION.get(pid)`.
Ownership is read only as a membership filter (`if not s.get("owner"): continue`), never as a value.
Stipulation and implementation agree.

### Y025 — two provinces with the same development, trade good and condition have the same wealth whoever owns them

**Status:** CONFIRMED
**Method:** Checked as a derivation from the wealth expression.
**Evidence:** `wealth = TAX_COEFF·base_tax·(1+tmod) + max(0, GP_COEFF·base_production·(1+gmod))·price(good)`.
Every argument is one of the three named inputs; `owner` appears nowhere on the right-hand side, so
the function is constant on the equivalence class the claim names. v3.0–v5.0's "terrain, development
and trade good" was the wrong triple twice over — terrain never entered wealth, and condition, which
does, was missing.

### Y026 — owner-agnosticism is true by construction because base_tax, base_production and the trade good are bare attributes of the place

**Status:** CONFIRMED
**Method:** Checked as an argument against the four condition modifiers' file definitions.
**Evidence:** The three named inputs are province-history fields with no country argument, so there
is no classification decision to get wrong; the fourth input, condition, is a closed four-entry list
read from one file, so it needs no classifying either. Recorded so the property is not over-read:
`occupied` and `under_siege` are facts about *which country's army holds the province*, so wealth is
invariant to **who owns** a province, not to all country state — which is exactly what §3.3 wants
("a besieged province genuinely produces less"). The claim is about the classification burden and is
correct as stated.

### Y027 — v3.0 through v5.0 defended the property with a two-test classifier applied to a sweep of the install

**Status:** PARTIAL
**Method:** Grepped for the two-test vocabulary in the v2, v3.0, v4.0 and v5.0 specs; read §1.3 in
each; read the graded entries W040/W041 and X035.
**Evidence:** "Two tests", "enters wealth" and "locality test" appear **0 times** in v2's and v3.0's
specs and first appear at `v4-owner-agnostic/per-good-trade-spec.md:184`. v3.0's §1.3 (`v3:160–164`)
used a single structural rule instead — "The engine's own data model draws the line for us … In
vanilla the income-relevant local ones are exactly three" — and that is what `validation-v3.md`
graded: W040 PARTIAL ("a correct classifier *for trade-good modifiers* … stated as if it were the
classifier for local modifiers generally") and W041 REFUTED (the "exactly three" enumeration). The
two-test classifier was v4.0's **repair** for W040/W041.
**Evidence (the rest — confirmed):** v4.0 and v5.0 did carry it; v4.0's harness passed it (163 + 40
checks, 0 failed, re-run this session, including a check asserting the presence of the sentence
X034 quotes as wrong); v5.0's audit refuted its application at X035.
**Should say:** "v4.0 and v5.0 defended the property with a two-test classifier, and v3.0 with a
structural rule the same audit refuted."

### Y028 — what this gives up: gems' local_tax_modifier and incense' trade_value_modifier are genuinely province-scoped and are no longer read

**Status:** CONFIRMED
**Method:** Read `common/tradegoods/00_tradegoods.txt`; grepped `solver.py`.
**Evidence:** `gems` (block at line 2015) carries `province = { local_tax_modifier = 0.15 }` at lines
2020–2022; `incense` (line 1890) carries `province = { trade_value_modifier = 0.1 }` at 1895–1897 —
both inside a `province = { }` sub-block, so both genuinely province-scoped. `solver.py` contains no
`local_tax_modifier`, no `trade_value_modifier`, no great-project read, no
`add_permanent_province_modifier` read and no `has_dlc` test.

### Y029 — the deleted apparatus covered 89 of the 2,472 counted provinces — 43 gems plus 31 incense plus 16 great-project and permanent-modifier provinces, less one that is both (province 542)

**Status:** CONFIRMED
**Method:** Counted goods over the counted set from the save; enumerated the great-project and
permanent-modifier provinces carrying a key wealth reads and took the union (`m2.py`, `m4.py`).
**Evidence:** `gems` **43**, `incense` **31** over the 2,472. The modifier set is exactly **16**
counted provinces — `[6, 8, 262, 362, 363, 370, 371, 387, 542, 684, 1821, 1822, 2145, 2151, 2316,
4316]` — being `falun_copper_mine` (8), `krakow_cloth_hall` (262), the four Grand Canal provinces
(684, 1821, 1822, 2145) and the ten permanent province modifiers. Union of the three sets **89**;
overlap of the modifier set with `gems ∪ incense` exactly **{542}** (Golconda: save good `gems`, plus
an undated `add_permanent_province_modifier = { name = diamond_mines_of_golconda_modifier }`).
43 + 31 + 16 − 1 = 89.

### Y030 — that count depends on the field: 87 under the withdrawn is_city filter, and 89 rather than 88 because province 4856 rolled incense

**Status:** CONFIRMED
**Method:** Intersected the 89 with the 20 owned provinces that carry no effective `is_city = yes`;
read 4856's history and save values.
**Evidence:** Two of the 89 are among the 20 — **1207** and **4856**, both `incense` in the save — so
requiring `is_city = yes` gives **87**. Province 4856's history says `trade_goods = unknown`, the
save says `incense`, `solver.ROLLED[4856] == "incense"`, and the solver's row for 4856 carries
`incense`. Without the rolled-goods read it would price as `unknown` and the union would be **88**.

### Y031 — goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers), no local flat goods-bonus term

**Status:** CONFIRMED
**Method:** The spec's formula block against `solver.py:province_table()`.
**Evidence:** `gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))` with
`gmod = STATE_GOODS_MOD["devastation"] * dev`. No additive term exists. The implementation adds a
`max(0, ·)` clamp the spec's formula does not show; it bites only if the modifier sum reaches −1
(devastation 100).

### Y032 — trade_value(p) = goods_produced(p) · price(good(p)), ducats per year; the local trade-value-modifier factor is gone

**Status:** CONFIRMED
**Method:** As above.
**Evidence:** `prod_income = gp * price`, no third factor. v5.0's
`(1 + Σ local trade-value modifiers)` is absent from both the spec formula and the solver, restoring
W028's form.

### Y033 — tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)

**Status:** CONFIRMED
**Method:** As above.
**Evidence:** `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)`, with `tmod = 0.0` at 1444 because
`STATE_TAX_MOD` holds only `occupied` and no province is occupied at the start.

### Y034 — ⚑ GP_COEFF is a shipped file value, localised "Base Production", read at runtime

**Status:** CONFIRMED
**Method:** Read `common/static_modifiers/00_static_modifiers.txt:251–254` and
`localisation/EU4_l_english.yml:815`; read `solver.py:_read_gp_coeff()`.
**Evidence:** The block is exactly
`provincial_production_size = { trade_goods_size = 0.2   ship_recruit_speed = -0.01 }`, and
`provincial_production_size:0 "Base Production"` is the English string.
`find -iname "*static_modifier*"` returns that one file only, so no DLC overrides it. `solver.py`
reads the value with a regex at import time and *raises* rather than defaulting if the block is
missing, so it is genuinely read and genuinely moddable. `GOODS_PRODUCED_FACTOR` is 0.2 on 1.37.5.0.

### Y035 — TAX_COEFF is in no file that has been found

**Status:** CONFIRMED
**Method:** Grepped `common/defines.lua` and every file in `common/defines/` for `TAX`; grepped
`00_static_modifiers.txt` for every tax key; grepped `common/` for "per base_tax" and "ducat per".
**Evidence:** `defines.lua`'s ten TAX matches are `ALLOW_ZERO_BASE_VALUES`, `PS_RAISE_WAR_TAXES`,
`PS_WAR_TAXES_LIMIT_MIN`, `ENFORCE_CULTURE_TAX_MULTIPLIER`, `SCUTAGE_TAX_FRACTION`,
`WARTAXES_DURATION`, `CITY_SPRAWL_NUDGE_TAX_VALUE`, `BASE_TAX_COST_MODIFIER`, `FLAT_TAX_AMOUNT` —
none a per-point rate. `common/defines/` holds five files and **0** TAX matches. The only
base-rate-shaped static-modifier block, `provincial_tax_income = { }` at line 244, carries no tax
value at all (recruit-speed, build-time and institution-spread keys only). `solver.py` keeps
`TAX_COEFF = 1.0` as a literal with the measurement recorded beside it.

### Y036 — ⚑ the tax tooltip's schema is Base: trunc(base_tax × 0.0833333) (Yearly base_tax); it is not twelve times the displayed figure, which would give 5.88 and 1.92

**Status:** CONFIRMED
**Method:** Arithmetic on the two recorded observations. **EU4 was not run in this pass**, so the two
tooltip readings are prior engine observations and are graded on the evidence that exists.
**Evidence:** `trunc(6 × 0.0833333) = trunc(0.4999998) = 0.49` and
`trunc(2 × 0.0833333) = trunc(0.1666666) = 0.16`, both matching the observed `Base` lines; the
parentheticals are 6.00 and 2.00, i.e. `base_tax` itself. `12 × 0.49 = 5.88` and `12 × 0.16 = 1.92`,
neither of which is an observed parenthetical, so the "12·X" reading is arithmetically dead on both
of its own data points. Recorded as a limit of the two observations: they pin the multiplier only to
`[0.081667, 0.083333)`, a divisor in `[12.000, 12.245]`, so the specific constant 0.0833333 sits
inside the admissible interval without being uniquely determined by them. Exact 1/12 *is* excluded —
it would display 0.50 at `base_tax` 6.

### Y037 — v4.0 and v5.0 wrote the schema as Base: X (Yearly 12·X), false on both of its own data points; v3.0 carries neither that schema nor the 0.6125 arithmetic

**Status:** CONFIRMED
**Method:** Grepped `Yearly`, `12·X` and `0.6125` across the v1, v2, v3.0, v4.0 and v5.0 specs.
**Evidence:** `v4:162–164` and `v5:169–171` carry the schema verbatim. `12·X` appears in **no**
v1/v2/v3.0 document and `0.6125` appears **0 times** across all of v1, v2 and v3.0. Recorded rather
than deducted: v3.0 *does* carry the same modifier-ordering passage (`v3:155–157`) but with the
truncated result — "giving **0.61**" — so it has the conclusion without the 0.6125 step. The claim as
written is true.

### Y038 — ⚑§ the monthly production tooltip's Trade Value line is consistent with the annual-over-twelve relation on one observation, 3.52 → +0.29, fixing the divisor only to within (11.73, 12.14]

**Status:** CONFIRMED
**Method:** Interval arithmetic on the single recorded observation.
**Evidence:** If `+0.29` is the truncation of `3.52/d` then `0.29 ≤ 3.52/d < 0.30`, hence
`3.52/0.30 < d ≤ 3.52/0.29`, i.e. **`11.7333 < d ≤ 12.1379`** — exactly the stated `(11.73, 12.14]`,
open below and closed above. The bound is right and the § marker is the right hedge. v6.0's own
earlier draft wrote `[12.00, 12.14]`, which is the interval after intersecting with the tax pair;
the shipped sentence is the production observation alone and is correct.

### Y039 — both monthly figures being the annual value over twelve is what lets the annual forms add directly, and it is the tax pair that establishes it, at two development levels

**Status:** CONFIRMED
**Method:** Checked as a derivation.
**Evidence:** If monthly = annual/12 on both terms then `12·(m_tax + m_trade) = a_tax + a_trade`, so
the annual forms share a basis and add with no conversion — valid. The tax pair carries it because
its parenthetical is *labelled* `Yearly` and equals `base_tax` at two distinct development levels
(6 and 2), pinning the divisor to `[12.000, 12.245]`; the production observation alone gives only
`(11.73, 12.14]`. Intersected: `[12.00, 12.14]`, which contains 12. The attribution to the tax pair
is the right one.

### Y040 — ⚑§ 0.49 × 1.25 is 0.6125, which truncates to 0.61, not 0.62, so the engine multiplies the untruncated monthly value

**Status:** CONFIRMED
**Method:** Arithmetic; the engine reading itself was not re-taken.
**Evidence:** `0.49 × 1.25 = 0.6125`, and truncating to two places gives **0.61**, not the observed
0.62. The untruncated path gives `6 × 0.0833333 = 0.4999998`, `× 1.25 = 0.62499975`, `trunc → 0.62`,
which matches. The conclusion follows *given* §2.3's truncation premise, which is worth stating
because 0.62 is also reachable from 0.6125 by rounding **up**; only truncation closes that door, and
§2.3 supplies it ("The displayed monthly is the truncation of `base_tax × 0.083333`"). The argument
is sound as the document has it.

### Y041 — v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation; both cannot hold

**Status:** CONFIRMED
**Method:** Read `v4:176–178`, `v5:183–185` and each version's §2.3 constants table.
**Evidence:** Both carry, verbatim, "`Base 0.49` then `Tax Income Efficiency 125.0%`, giving 0.6125,
which the province window shows as 0.62", while their own §2.3 says the displayed monthly is the
**truncation** of `base_tax × 0.083333`. 0.6125 truncates to 0.61. The two statements are
inconsistent, exactly as claimed.

### Y042 — the Garnatah example establishes only the ordering — base from development first, percentage second — and nothing finer

**Status:** PARTIAL
**Method:** Read the whole paragraph, not the sentence.
**Evidence:** The ordering conclusion is sound: a `Base` line computed from `base_tax` alone, then a
percentage line, then a product, fixes the order and nothing about the coefficient. But "nothing
finer" contradicts the two sentences immediately before it in the same paragraph, which draw a
strictly finer conclusion from the same example — that the engine "is **not** multiplying the
displayed figure" and instead "multiplies the untruncated monthly value". That is a fact about the
engine's internal arithmetic, established by this example and by no other, and Y040 states it as
such.
**Should say:** "The example establishes the ordering and, given §2.3's truncation, that the
multiply is applied before display — and nothing finer about the coefficient or the divisor."

### Y043 — flat goods bonuses would add into goods_produced before the price multiply, but under §1.3 no source grants one

**Status:** CONFIRMED
**Method:** Grepped `solver.py` for an additive goods term; identified which sources previously
supplied one.
**Evidence:** No additive term exists in the solver's `gp` expression. The only 1444 sources of a
flat `trade_goods_size` were the five great-project provinces (8, 684, 1821, 1822, 2145) and the ten
permanent-modifier provinces — the apparatus Y003 deletes — so under v6.0 no counted province carries
one and the ordering is unexercised. v5.0's X029 ("fifteen 1444 provinces carry a flat goods bonus")
is correctly withdrawn: those fifteen are exactly that set.

### Y044 — province condition is the one thing besides development and the good that wealth reads: four static modifiers, all read from 00_static_modifiers.txt

**Status:** CONFIRMED
**Method:** Located each block; confirmed there is only one static-modifier file in the install.
**Evidence:** `occupied` at line 433, `under_siege` at 444, `devastation` at 453, `prosperity` at 464,
all in `common/static_modifiers/00_static_modifiers.txt`, and `find -iname "*static_modifier*"`
returns that file alone. `solver.py`'s `STATE_GOODS_MOD`/`STATE_TAX_MOD` hold exactly these four.

### Y045 — ⚑ the four values: devastation −2 scaled by level, prosperity 0.25, under_siege −0.25, occupied −0.5 and local_tax_modifier −0.5

**Status:** CONFIRMED
**Method:** Quoted each block in full.
**Evidence:** `devastation` line 454 `trade_goods_size_modifier = -2`; `prosperity` line 466
`trade_goods_size_modifier = 0.25`; `under_siege` line 445 `trade_goods_size_modifier = -0.25`;
`occupied` lines 434–435 `local_tax_modifier = -0.5` **and** `trade_goods_size_modifier = -0.5`. All
four match the table exactly. Each block carries further keys — supply limit, institution spread,
movement speed, development cost, manpower, sailors, province trade power, monthly devastation — none
of which wealth computes.

### Y046 — no shipped file states that the devastation scaling is linear in the level; the model assumes −2 × level/100, and prosperity is likewise applied as stated without a file confirming its direction

**Status:** PARTIAL
**Method:** Grepped the whole of `00_static_modifiers.txt` for `scaled`, `linear`, `multiplied`,
`scaling` in and around the two blocks; read the file header.
**Evidence (devastation half — confirmed):** Nothing in or adjacent to the `devastation` block says
the modifier scales with the level. The file *does* annotate other modifiers that way — line 994
"`# Multiplied by Development/COUNTRY_DEVELOPMENT_SCALE`", line 1052 "`#Scaled, multiplied by current
corruption / 100`" — and there is a separate `development_scaled = { }` block at line 287, so the
absence of such an annotation on `devastation` is meaningful. `solver.py` applies
`-2.0 * level / 100.0`, an assumption.
**Evidence (prosperity clause — wrong as written):** `prosperity`'s **direction is in the file**:
line 466, `trade_goods_size_modifier = 0.25`, positive, sign and magnitude both fixed. What no file
fixes is whether that value scales with the prosperity level, as the model assumes for devastation.
**Should say:** "…and `prosperity` carries the same unstated question about level scaling, though its
sign and magnitude are in the file."

### Y047 — only occupied touches the tax term; the other three reach goods_produced alone

**Status:** CONFIRMED
**Method:** Enumerated every key in the four blocks.
**Evidence:** Of the four, only `occupied` carries a tax key (`local_tax_modifier = -0.5`, line 434).
`devastation`, `under_siege` and `prosperity` carry `trade_goods_size_modifier` and no tax key of any
kind, so within the wealth model they reach `goods_produced` alone.

### Y048 — these four are what make the map answer to war; §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them

**Status:** CONFIRMED
**Method:** Cross-read §1.2, §3.3 and §2.8 against §1.3's table.
**Evidence:** §1.2 names exactly `devastation`, `occupied`, `under_siege`, `prosperity` as what moves
`goods_produced`; §3.3's "a besieged province genuinely produces less" is `under_siege`'s −0.25; and
§2.8's "Major war in China" and "Ming loses the Mandate" rows turn respectively on devastation biting
and on ownership *not* biting. Delete the four and wealth is a pure function of development, good and
price, leaving all three passages without a mechanism. The dependency is real and correctly
attributed.

### Y049 — ⚑ eleven counted provinces begin devastated at 1444 — Bohemia at 50, Erzgebirge and Moravia at 20 — and no province-history file says so; on_startup fires flavor_boh.15

**Status:** CONFIRMED
**Method:** Read `events/flavorBOH.txt:938–976`; resolved the three areas through `map/area.txt`;
checked owner and node membership for each; read `devastation` out of the save's gamestate.
**Evidence:** `flavor_boh.15`'s `immediate/hidden_effect` applies
`bohemia_area = { add_devastation = 50 }`, `erzgebirge_area = { add_devastation = 20 }`,
`moravia_area = { add_devastation = 20 }`. `map/area.txt` gives
`bohemia_area = { 266 2968 2970 4725 4724 }` (5), `erzgebirge_area = { 267 1771 2967 }` (3),
`moravia_area = { 265 4237 4726 }` (3) — **eleven** provinces. All eleven are BOH-owned at 1444 and
all eleven lie in a trade node (`saxony` × 8, `wien` × 3), so all eleven are counted. The save
confirms it independently: exactly **11** provinces have `devastation > 0`, and they are precisely
those eleven at 50/50/50/50/50 and 20/20/20/20/20/20; **0** have `prosperity > 0`. No
`history/provinces/*.txt` file carries `add_devastation` or a `devastation` field for any of them.

### Y050 — that devastation costs 13.40 ducats across the eleven affected counted provinces

**Status:** CONFIRMED
**Method:** Recomputed the field with `gmod = 0` everywhere and differenced (`m2.py`).
**Evidence:** **13.40** ducats over **11** counted devastated provinces. Reproduces `measure6.out`
and is guarded by `verify6.py` — against a typed literal, see Y012.

### Y051 — ⚑ the chain is 00_on_actions.txt → on_startup_effect → 01_scripted_effects_for_on_actions.txt → country_event flavor_boh.15

**Status:** CONFIRMED
**Method:** Followed the chain link by link in the files.
**Evidence:** `common/on_actions/00_on_actions.txt:33` calls `on_startup_effect = yes` inside
`on_startup = { }` (lines 4–36). `common/scripted_effects/01_scripted_effects_for_on_actions.txt`
defines `on_startup_effect = {` at line 4716 and at 4787–4796 carries
`if = { limit = { tag = BOH  NOT = { has_country_flag = boh_hussite_aftermath_flag } }
set_country_flag = boh_hussite_aftermath_flag   country_event = { id = flavor_boh.15 } }`. Every link
exists at the stated file.

### Y052 — the start state is what the engine produces, not what the history files say, and that costs three separate reads

**Status:** CONFIRMED
**Method:** Checked as a derivation against Y049/Y054/Y056/Y057/Y059.
**Evidence:** Four independent gaps between the history files and the engine's 1444 state support the
general claim: eleven devastated provinces no history file records; a dated `add_base_tax` that
accumulates rather than overwrites; twenty owned provinces the engine treats as cities without the
line; and twenty rolled trade goods. Two of the four are the reads the sentence itemises, the
`is_city` item is a read *dropped* rather than added, and the rolled goods are a fifth. The
proposition — that reading history alone gets the start state wrong — is established.

### Y053 — ⚑ on_startup also fires flavor_mng.42, flavor_mos.1, flavor_geo.1 and others directly from its own events = { } list

**Status:** CONFIRMED
**Method:** Quoted `on_startup`'s `events = { }` block.
**Evidence:** `00_on_actions.txt:23–32` lists seven live events — `muslim_school_events.20`,
`flavor_got.1`, **`flavor_mng.42`** (26), **`flavor_mos.1`** (28), `flavor_fra.206`,
**`flavor_geo.1`** (30), `flavor_mam.111` — with `flavor_fra.15000` commented out at 27. This list is
a path parallel to the three `*_effect` calls at 33–35, one of which carries `flavor_boh.15`. Both
halves hold.

### Y054 — development itself does not move before the first tick: the history parse matches the save on 2,472 of 2,472 provinces for base_tax, base_production and owner, and only trade_goods differs, on exactly twenty

**Status:** CONFIRMED
**Method:** Independently parsed all 3,923 `history/provinces/*.txt` files with a Paradox tokenizer,
applying dated blocks with date ≤ 1444.11.11 in chronological order, `base_*` overwriting and
`add_base_*` accumulating; extracted 4,941 province records from the save's `gamestate` at two-tab
field depth; compared over the counted set. **Not** compared against `prov1444.json`.
**Evidence:** counted (owner and in a node) = **2,472**; `base_tax` **2472/2472**;
`base_production` **2472/2472**; `owner` **2472/2472**; `trade_goods` differ on **20**. The
history-owned set and the save-owned set are equal (symmetric difference empty), every history-owned
province lies in a node, and no counted province is missing from the save.

### Y055 — ⚑ flavor_geo.1 does not carry add_base_tax; its whole effect is legitimacy, a country modifier and a flag; those keys are in flavor_geo.3, which on_startup does not fire

**Status:** CONFIRMED
**Method:** Quoted both events in full from `events/FlavorGEO.txt`; grepped the whole install for
`flavor_geo.3`.
**Evidence:** `flavor_geo.1` (lines 8–46) has `add_legitimacy = -20`,
`add_country_modifier = { name = "geo_powerful_nobles" … }` and
`set_country_flag = geo_received_starting_event`, and **no** `add_base_tax`, `add_base_production` or
`add_devastation`. `flavor_geo.3` (98–150) does carry them — `466 = { add_devastation = 100 }` on
option a; `add_devastation = 50` plus
`capital_scope = { add_base_tax = 2  add_base_production = 2  add_base_manpower = 1 }` on option b.
The only script reference to `flavor_geo.3` outside its own definition is
`missions/KoK_Georgian_Missions.txt:2043`, `country_event = { id = flavor_geo.3 }` — a mission, not
`on_startup`.

### Y056 — ⚑ add_base_* in a dated block before the start date accumulates: province 1 (Uppland) has base_tax = 5 undated plus 1 at 1436.4.28 and the game has 6

**Status:** CONFIRMED
**Method:** Read `history/provinces/1-Uppland.txt`; read province 1's `base_tax` from the save.
**Evidence:** line 9 `base_tax = 5`; line 23 `1436.4.28 = { … add_base_tax = 1 … }`; save value
**6.000** (name "Stockholm", owner SWE). 5 + 1 = 6, so the grant accumulates. The file's
`1444.11.12 = { add_base_tax = 2 }` at line 27 is one day after the start date and correctly not
applied — a useful control, since an off-by-one on the date filter would give 8. (The file is
`1-Uppland.txt`, without spaces.)

### Y057 — ⚑ is_city = yes is not a filter the engine applies: 20 owned provinces omit or comment out the line, province 265 among them, and it is also one of the devastated eleven

**Status:** CONFIRMED
**Method:** Enumerated every owned province with no effective `is_city = yes` on or before
1444.11.11, then classified each by how the line is absent.
**Evidence:** **20** provinces — `[265, 774, 857, 913, 958, 966, 1035, 1038, 1207, 2527, 2579, 2593,
2617, 2671, 2779, 2932, 4573, 4576, 4640, 4856]`. `265 - Brno.txt:13` is `#is_city = yes`, commented
out, and 265 is in `moravia_area`, so it is one of the devastated eleven. Seven omit the line
entirely (913, 958, 966, 1207, 2579, 2932, 4856); twelve carry it only in a post-1444 dated block.
All 20 have an owner and lie in a trade node, and the save has them as ordinary provinces. Requiring
the line gives **2,452**.

### Y058 — the model counts a province when it has an owner and lies in a trade node: 2,472 provinces, not 2,452, and world wealth is 10,607.40 annual ducats

**Status:** CONFIRMED
**Method:** Read the filter; recomputed `len(ROWS)` and `W.sum()` (`m2.py`); cross-checked the count
against the independent history/save parse.
**Evidence:** The filter is `if not s.get("owner"): continue` then `if PNODE.get(pid) is None:
continue` — owner and node membership, no `is_city`. `len(ROWS) = 2472`, `world wealth = 10607.40`.
The independent parse gives 2,472 for the same predicate and 2,452 with `is_city = yes` added.

### Y059 — ⚑ twenty counted provinces have no trade good in their history file; the engine assigns one at start from each good's chance = { } block

**Status:** CONFIRMED
**Method:** Counted `trade_goods = unknown` over the counted set from the history parse; checked for
counted provinces with no `trade_goods` key at all; read `common/tradegoods/00_tradegoods.txt`.
**Evidence:** **20** counted provinces carry `trade_goods = unknown`; **0** carry no `trade_goods`
key, so the set is exactly the 20 that differ from the save (Y054). `00_tradegoods.txt` defines 32
goods of which **31** carry a `chance = { }` block — the sole exception is `unknown` itself (lines
2283–2285). Example, `gems` at line 2023: `chance = { factor = 5   modifier = { factor = 0   area =
newfoundland_area } … }`.

### Y060 — the model does not predict the draw: it reads the good the engine actually rolled and prices the province on that, as it does for development

**Status:** CONFIRMED
**Method:** Read `solver.py:_rolled_trade_goods()` and the substitution in `province_table()`;
inspected what `prov1444.json` holds.
**Evidence:** `_rolled_trade_goods()` opens `save games/VANILLA_start.eu4`, reads `gamestate`, walks
the `provinces={}` block at brace depth and takes `trade_goods` at two-tab depth per record;
`province_table()` substitutes it only where history says `None`/`unknown`. `measure6.out` confirms
the result: `provinces with trade_goods unknown  0`. Recorded rather than deducted: the reference
implementation reads *development* from a history parse (`prov1444.json` holds
`{'trade_goods': 'unknown', 'base_tax': 4.0, …}` for 4856), not from the save — but §2.2 item 2
specifies a save parser for both, and Y054 shows the two agree on 2472/2472, so the claim about the
model is right and the implementation's shortcut is numerically free.

### Y061 — pricing those twenty at zero instead understates world wealth by 12.70 ducats

**Status:** CONFIRMED
**Method:** Recomputed the field with `prod_income = 0` for exactly the 20 history-`unknown`
provinces and differenced (`m2.py`).
**Evidence:** difference **12.70** ducats over **20** provinces zeroed.

### Y062 — § on this save the twenty came up seven fur, five grain, three wool, two livestock, and one each of cotton, incense and naval_supplies

**Status:** CONFIRMED
**Method:** Tabulated the save-side good for each of the 20 from the independent gamestate parse.
**Evidence:** `fur 7 | grain 5 | wool 3 | livestock 2 | cotton 1 | incense 1 | naval_supplies 1`,
total 20 — exactly as stated. Per province: 774 wool, 862 wool, 895 naval_supplies, 897 grain, 907
grain, 966 fur, 1809 livestock, 2014 cotton, 2503 fur, 2510 fur, 2571 fur, 2593 fur, 2596 grain,
2669 grain, 2671 fur, 2932 wool, 4856 incense, 4901 fur, 4902 livestock, 4923 grain. The § marker is
the right hedge: this is one draw and the `chance` blocks make it a random variable.

### Y063 — the TAX_COEFF = 1.0 reference condition is applied to every province the model counts; the is_city = yes premise is dropped

**Status:** CONFIRMED
**Method:** Read the filter and the tax expression.
**Evidence:** `tax = TAX_COEFF * base_tax * (1 + tmod)` with `TAX_COEFF = 1.0` for every row, and the
row filter tests owner and node membership only. Nothing in the solver distinguishes a cored from an
uncored, or a settled from an unsettled, province. The premise is dropped exactly as stated.

### Y064 — that is a modelling choice with a known cost: two readings, both on cored city provinces at base_tax 2 and 6, are all TAX_COEFF = 1.0 rests on

**Status:** CONFIRMED
**Method:** Read §2.3's constants table; checked the development range against the save.
**Evidence:** The `TAX_COEFF` row cites exactly two observations — Garnatah (223) at `base_tax` 6 →
`Base: 0.49 (Yearly 6.00)` and Caceres (1747) at `base_tax` 2 → `Base: 0.16 (Yearly 2.00)`, both
cored cities. The extrapolation runs to `base_tax` 15 (Y065), so the cost is real and is correctly
stated as a cost rather than hidden.

### Y065 — ⚑ base_tax at 1444 runs up to 15 (province 1821), with total development reaching 33 there

**Status:** CONFIRMED
**Method:** Maxima over the counted set from the save.
**Evidence:** max `base_tax` = **15.000** at province **1821** (Nanjing), unique, no ties. That
province's `base_tax + base_production + base_manpower = 15 + 15 + 3 = 33`, also the unique maximum
total development. Runners-up: 1816 Beijing 31, 116 Firenze 28, 112 Venezia 27, 667 Canton 27.

### Y066 — owner-agnostic wealth removes a large source of hidden owner-dependence, not "the single largest" as v3.0 through v5.0 had it

**Status:** CONFIRMED
**Method:** Grepped the three prior specs for the phrase; read v6.0's replacement.
**Evidence:** `v3:180`, `v4:229` and `v5:265` all read "It also removes the **single largest** source
of hidden owner-dependence"; v6.0 reads "It also removes **a large** source". The retraction is
correct on its own terms: no version measured the competing sources, so "single largest" was a
superlative with no ranking behind it — precisely what §0's convention forbids.

---

## §1.5 — Goods without a graph

### Y067 — repricing to coal the 45 owned latent-coal provinces flips 10 of 159 Φ_w edges and adds 214.60 ducats; the flip count returns to W187's value after v5.0 reported 29

**Status:** CONFIRMED
**Method:** Re-scanned `history/provinces/` for `latent_trade_goods` containing `coal`, recomputed
the repriced field and the resulting orientation, and differenced the edge sets (`m4.py`); read
W187's row in `claims-v3.md` and v5.0's spec.
**Evidence:** latent-coal provinces **58**; owned and counted **45**; wealth delta **+214.60**;
edge flips **10 of 159**. `claims-v3.md:377` W187 reads "flips **10 of 159 `Φ_w` edges**", and
`v5-owner-agnostic/per-good-trade-spec.md:312` reads "flips **29 of 159**" (repeated in v5.0's §2.8
row), so the return to W187's value is correctly described. Coal's `base_price = 10` is the maximum
in `common/prices/00_prices.txt` (next: `cloves` 8), which is the other half of §1.5's framing.

### Y068 — the counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and one of the devastated eleven, and dropping its devastation measures coal activating plus one province healing — worth 2.40 ducats and 3 extra flips

**Status:** CONFIRMED
**Method:** Ran the coal counterfactual twice, once retaining each repriced province's devastation
multiplier and once dropping it (`m4.py`).
**Evidence:** 4237 is in the latent-coal set **and** in `moravia_area`'s devastated three
(`(True, True)`). Devastation retained: **+214.60** ducats, **10** flips. Devastation dropped:
**+217.00** ducats, **13** flips. Difference exactly **2.40** ducats and **3** flips. `measure6.py`
carries the retaining version and comments the arithmetic (`0.2*3*10*(1-0.6) = 2.40`), which
checks out: 4237 has `base_production` 3, devastation 20, so `0.2·3·(1−0.4)·10 = 3.60` against
`0.2·3·10 = 6.00`.

---

## §1.6 — The aggregate graph

### Y069 — both the sink count and the sink locations move with the wealth field, and α_Φ sets how sharply concentration is read; the count is a function of the field and the constant

**Status:** CONFIRMED
**Method:** Two independent sweeps: the sink set across α_Φ = 1.00…8.00 at 0.01 on a fixed field,
and the sink set across European development factors at fixed α_Φ = 1.5 (`measure6.py`, `m8.py`).
**Evidence:** At fixed field, the count over α_Φ ∈ {1, 1.5, 2, 3, 4, 8} is **6, 2, 1, 2, 3, 1** — so
the constant moves it. At fixed α_Φ = 1.5, European development ×1.00/×1.02/×1.20/×1.56/×1.70 gives
counts **2, 3, 4, 2, 1** and memberships `{english_channel, hangzhou}` → `{…, wien}` →
`{english_channel, gulf_of_siam, hangzhou, wien}` → `{english_channel, rheinland}` → `{genua}` — so
the field moves both count and placement. Neither factor alone determines the count.

### Y070 — at the stipulated α_Φ = 1.5 the 1444 field gives two sinks and a modestly grown Europe gives three or one

**Status:** CONFIRMED
**Method:** As above.
**Evidence:** ×1.00 → **2** (`english_channel`, `hangzhou`); ×1.02 → **3** (adds `wien`); ×2.00 → **1**
(`genua` alone). All at α_Φ = 1.5 with every other input fixed.

### Y071 — v2.0–v4.0's "the count emerges from concentration exactly as per-good sink counts do" and v5.0's "the count is set by α_Φ" are wrong the same way

**Status:** CONFIRMED
**Method:** Located both phrasings; checked the diagnosis against Y069's two sweeps.
**Evidence:** `v2:154`, `v3:257` and `v4:306` all read "Nothing pins their count; it emerges from
concentration exactly as per-good sink counts do." `v5:342` reads "**Their count is set by `α_Φ`;
only their locations are emergent.**" Each attributes the count to a single factor — the field in
the first case, the constant in the second — and Y069 shows both factors move it. The diagnosis
("wrong the same way") is exactly right.

### Y072 — v2.1 chose the value with a target count in view, a calibration §2.3 withdraws without replacing; the band-table ground on which v5.0 retained 1.5 is withdrawn too

**Status:** CONFIRMED
**Method:** Grepped for each version's stated justification; read v6.0's §2.3.
**Evidence:** `v2:372–373`, `v3:558–559` and `v4:632–633` carry, verbatim, "`α_Φ = 1.5` (**calibrated
so the 1444 start yields the two-sink hangzhou/english_channel map**, §1.6…)". `v5:732–737` withdraws
that and substitutes "**1.5 is retained because it sits inside the widest sink-count band**"; "widest"
appears **0 times** in the v1, v2, v3.0 and v4.0 specs, so the band argument is v5.0-only. v6.0's
§2.3 withdraws both and offers no replacement. Both halves confirmed.

### Y073 — measured: identical orientation at ×1 and above, 12 edge flips at ×10⁻², and 100 at ×10⁻⁶, where the sink set also collapses to {genua}

**Status:** CONFIRMED
**Method:** Scaled `b_w` by 1, 1e-2 and 1e-6 and differenced the orientations (`m2.py`).
**Evidence:** ×1 → **0** flips, sinks `{english_channel, hangzhou}`; ×1e-2 → **12** flips, sinks
unchanged; ×1e-6 → **100** flips, sinks **`{genua}`**. The mechanism the spec names is confirmed by
the pattern: `ZERO_TOL` is absolute (`flowop.py:ZERO_TOL = 1e-11`), so scaling `b` down pushes
genuine flow arcs into the free set — 12 flips at 1e-2 and 100 at 1e-6 is the tolerance eating the
support progressively. The spec's own caution that the sink set is not the quantity to watch here is
borne out: it survives the 12-flip degradation and then collapses.

### Y074 — 1444's b_w has largest magnitude 0.0225, so normalising into (−1, 1) scales it up and is safe

**Status:** CONFIRMED
**Method:** `max |1/N − c_w|` at α_Φ = 1.5 (`m2.py`).
**Evidence:** **0.022531**, which rounds to 0.0225 as printed. Since the largest magnitude is well
below 1, mapping into (−1, 1) multiplies `b` up, and Y073 shows only scaling *down* is dangerous.
(v6.0's own earlier draft carried 0.0226; the shipped 0.0225 is the correct rounding.)

### Y075 — measured at α_Φ = 1.5: two sinks, english_channel and hangzhou — c_w ranks 2 and 3, node-wealth ranks 1 and 12

**Status:** CONFIRMED
**Method:** Recomputed `Φ_w`, its sink set, and both rank vectors (`m2.py`), and independently on the
five-phase instrument (`relabel2.py` validation run).
**Evidence:** sinks `['english_channel', 'hangzhou']`; `english_channel` (c_w rank **2**,
node-wealth rank **1**); `hangzhou` (c_w rank **3**, node-wealth rank **12**). Both instruments agree
edge for edge.

### Y076 — one of those two is a property of the world and the other is a property of the node ordering, and the difference matters more than the count

**Status:** CONFIRMED
**Method:** 400 relabellings, four independent seeds of 100, on the validated five-phase instrument
with α_Φ and every input fixed (`relabel2.py`).
**Evidence:** `hangzhou` held an end in **96–100 per hundred** (97, 100, 98, 96); `english_channel` in
**31–47 per hundred** (44, 31, 42, 36 on my seeds; the project's own
`preconfirm3-relabel.out` adds 40, 37, 44, 47, 39). The asymmetry is large and stable across seeds,
so the characterisation holds even though neither individual band matches the document's (Y079).

### Y077 — Phase 2's b-flow is degenerate — many distinct supports carry the same optimal cost — so relabelling the nodes returns a different optimal orientation

**Status:** CONFIRMED
**Method:** 400 relabellings of `Φ_w` and 580 per-good relabelled runs, recording the objective and
the flow support each time (`relabel2.py`, `perg.py`).
**Evidence:** On `Φ_w`, 400 of 400 relabellings changed the orientation while the objective moved by
at most **4.44e-16** (2 ULP) from 0.71227597782932572 — distinct supports at the same optimal cost,
which is degeneracy in the operative sense. Per good, 580 of 580 changed and **580 of 580 changed
the flow support**, with a maximum objective deviation of 8.88e-16.

### Y078 — across 400 relabellings the orientation changed every time, a mean of about 25 of 159 edges moved, and the sink set came back exactly as {english_channel, hangzhou} in 5 to 10 runs per hundred

**Status:** PARTIAL
**Method:** Four independent seeds of 100 relabellings (`relabel2.py`), plus the project's own
five-seed harness output `scripts/preconfirm3-relabel.out`.
**Evidence (confirmed):** orientation changed **100/100 on all four seeds** — 400 of 400. Mean edges
moving **25.6, 25.86, 26.1, 25.38** → "about 25 of 159" is right.
**Evidence (the interval — too narrow):** the exact sink set returned in **12, 4, 12, 9** runs per
hundred on my four seeds, i.e. **4 to 12**, not 5 to 10. The document's own harness output contains
five seeds — 8, 9, 5, 10 and **12** — so the quoted 5–10 is the range over four of those five, with
the twelfth-per-hundred seed excluded. Pooled over my 400 and the harness's 500: 44 of 500 and 37 of
400, i.e. roughly 9 per hundred with a seed-to-seed spread of 4 to 12.
**Should say:** "in about 9 runs per hundred, ranging 4 to 12 across seeds".

### Y079 — hangzhou was an end in 97 to 100 per hundred relabellings and english_channel in 37 to 44

**Status:** PARTIAL
**Method:** As Y078.
**Evidence:** My four independent seeds give `hangzhou` **97, 100, 98, 96** → **96–100**, and
`english_channel` **44, 31, 42, 36** → **31–44**. The project's own five-seed output gives `hangzhou`
100, 99, 97, 100, 98 and `english_channel` 40, 37, 44, **47**, 39. Combining all nine seeds:
`hangzhou` **96–100**, `english_channel` **31–47**. The quoted intervals are the range over four
seeds and fail on the low side for `hangzhou` (96) and on both sides for `english_channel` (31 and
47) — and the 47 is in the document's own harness file.
**Should say:** `hangzhou` about 98 per hundred (96–100 across seeds), `english_channel` about 40
(31–47).

### Y080 — the Asian end is the robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a fact about that node

**Status:** CONFIRMED
**Method:** As Y078; counted the relabellings in which `hangzhou` is not a sink.
**Evidence:** `hangzhou` loses its end in 3, 0, 2 and 4 runs per hundred on my four seeds — non-zero,
so not invariant, and 96–100 per hundred, so robust. The hedge is exactly the right strength, and it
is what Y140 fails to carry.

### Y081 — the European end is one of several the same world admits: gulf_of_siam held an end in about half the runs, wien in a third, sevilla in a fifth; the count ranged 1 to 5, most often 2 or 3

**Status:** PARTIAL
**Method:** As Y078; tabulated every end holder and the full count distribution.
**Evidence (confirmed):** `gulf_of_siam` **52, 63, 57, 50** per hundred — about half ✓ (the harness's
five seeds give 55, 48, 63, 58, 52). `wien` **29, 35, 34, 37** — about a third ✓. Count range
**1 to 5** on every seed ✓, with the mode 2 or 3 on every seed (2: 31, 28, 34, 33; 3: 37, 43, 42,
27) ✓.
**Evidence (sevilla — overstated):** `sevilla` held an end in **17, 12, 8, 17** per hundred on my
seeds and 19, 18, 16, 14, 10 on the harness's — **8 to 19**, i.e. about a tenth to a sixth, not a
fifth.
**Should say:** "`sevilla` in about one run in seven".

### Y082 — conditional on the node order: the sink set's membership and size, and everything derived from them — §2.4's end-flag list, and which European node holds an end in the Europe table

**Status:** CONFIRMED
**Method:** As Y078, plus a 60-relabelling run at ×2.00 European development (`perg.py`).
**Evidence:** Membership and size both move (Y078–Y081: 22–26 distinct sink sets per hundred, count
1–5). §2.4 item 2's end-flag list *is* the sink set, so it inherits the conditionality directly. And
in the Europe table the smaller factors are ordering-dependent: at ×1.02 the shipped order gives
`{english_channel, hangzhou, wien}` while the ×2.00 row is not ordering-dependent (Y102). The
partition the claim draws is the correct one.

### Y083 — not conditional over the same relabellings: the map is fully oriented (159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to 2.22e-16

**Status:** PARTIAL
**Method:** Recorded orientation count, acyclicity, fallback count and objective on all 400 runs
(`relabel2.py`).
**Evidence (confirmed):** fully oriented **100/100 on all four seeds**; acyclic **100/100 on all
four**; fallbacks fired **0 across all 400**. The conclusion — different *optimal* orientations
rather than different answers — is right.
**Evidence (the tolerance — too tight):** the maximum objective deviation from the identity
permutation's 0.71227597782932572 is **4.44e-16** on three of my four seeds and 2.22e-16 on the
fourth. So "identical to 2.22e-16" understates it by a factor of two; the honest figure is 2 ULP.
**Should say:** "the LP objective is identical to within 4.4e-16 (2 ULP)".

### Y084 — Phase 1 selects genua; both sinks arrive by stall promotion and genua ends a transit node, so there are 2 promotions and 0 fallbacks

**Status:** CONFIRMED
**Method:** Read `run_drain`'s `S0`, `promotions` and `fallbacks` on `Φ_w`; measured `genua`'s
degrees in the final orientation (`m2.py`).
**Evidence:** Phase-1 selection `['genua']`; promotions/fallbacks **(2, 0)**; the promoted nodes are
exactly `['english_channel', 'hangzhou']`. `genua`'s out-degree is **2** and in-degree **3**, so it is
a transit node, not a sink. Every clause holds.

### Y085 — eight sources, all in the bottom half of the wealth field, c_w ranks 44–75, mean degree 3.1 against the map's 4.0

**Status:** CONFIRMED
**Method:** Enumerated the in-degree-0 nodes and computed their rank band and mean undirected degree
(`m2.py`).
**Evidence:** **8** sources — `kongo`, `james_bay`, `mississippi_river`, `chengdu`, `cuiaba`,
`australia`, `yumen`, `safi`. `c_w` ranks **44–75** ✓. Node-wealth ranks 44–74, all in the bottom
half of 80 ✓. Mean undirected degree **3.12** against the map's **3.98** — printed as 3.1 and 4.0,
correct to the stated precision. The v5.0 seven-node enumeration is indeed not restated.

### Y086 — every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on three seeds, and v5.0's "0 edge flips across 5 seeds" is not restated

**Status:** CONFIRMED
**Method:** Recomputed acyclicity and orientation count; re-ran the three noise seeds; grepped the
v6.0 spec for the withdrawn phrasing.
**Evidence:** acyclic **True**, oriented **159/159**, every node has a directed path to a sink (the
sources reach `hangzhou`; `english_channel` has out-degree 0 and in-degree > 0). Sinks under ±1%
noise, seeds 0/1/2: `['english_channel', 'hangzhou']` on all three. `0 edge flips`, `across 5 seeds`
and `5 seeds` all appear **0 times** in the v6.0 spec, so the stronger claim is genuinely dropped.

### Y087 — per good on the same field, 89.6% of ordered node pairs (5,663 of 6,320) are connected by at least one good's directed path

**Status:** CONFIRMED
**Method:** `measure6.py`'s per-good BFS census, re-run and byte-identical; `verify6.py` re-checks it
at every phrasing.
**Evidence:** `ordered pairs connected  5663 of 6320`, `89.6`%. 80 × 79 = 6,320 ✓.
`verify6.py`'s `every_site` check reports "all 2 sites carry 5663", so §1.6 and §3.8 now agree —
the cross-phrasing defect `changes-v6.md` records as round three's find is genuinely closed.

### Y088 — agreement with the per-good graphs is 53.6% of edge-goods (52.3% value-weighted)

**Status:** CONFIRMED
**Method:** Recomputed the edge-good agreement independently of `measure6.py`, weighting by
`V_g = price·Σ goods_produced` (`m7.py`).
**Evidence:** **53.6%** edge-goods and **52.3%** value-weighted, over 4,611 (edge, good) pairs where
the good orients that edge. Matches `measure6.out` exactly.

### Y089 — the superseded marking-order aggregate scored higher on that measure, and no figure is maintained for it

**Status:** CONFIRMED
**Method:** Constructed `Φ_ord = Σ_g V_g·order_g` from the same 29 DRAIN runs and measured its
self-coherence on the v6.0 field (`m7.py`, `m9.py`, cross-checked with `drainrep.py`).
**Evidence:** `Φ_ord` **60.4%** edge-goods (60.1% value-weighted) against `Φ_w`'s 53.6% (52.3%) —
higher, as claimed, by 6.8 points on the unweighted measure. `drainrep.py` independently reports
"DRAIN(order) aggregate agrees with its per-good graphs: 2783/4611 (60.4%)". And no figure is
maintained: `60.3`, `62.7`, `60.4`, `7.8 point` all appear **0 times** in the v6.0 spec.

### Y090 — α_Φ = 1.5 is a stipulated design constant, exactly as P₀ = 2.0 is — superlinear, round, chosen, not derived

**Status:** CONFIRMED
**Method:** Checked the stipulation for internal consistency against §2.3 and against the withdrawn
derivations.
**Evidence:** §2.3 lists `α_Φ` alongside `P₀` under "Design constants" with the same
"stipulated … chosen rather than derived" language, so the parallel the claim draws is the document's
own. 1.5 > 1 is superlinear ✓ and is round ✓. And nothing in the document now derives it: Y091 and
Y126 confirm both prior derivations are withdrawn and no replacement is offered. The stipulation is
coherent and its stated rationale (a few very rich provinces outweighing a dense mediocre region) is
exactly what an exponent above 1 inside the sum does.

### Y091 — every derivation previously offered for it is withdrawn: v2.1 through v4.0 said it was calibrated to reproduce a two-sink 1444 map, and v5.0 said it sat in the widest sink-count band

**Status:** CONFIRMED
**Method:** As Y072.
**Evidence:** The calibration wording is verbatim in v2, v3.0 and v4.0; the widest-band wording is
v5.0-only (`v5:732–737`, `v5:383`, `v5:395`) and appears in no earlier spec. v6.0's §1.6 and §2.3
both withdraw both. Attribution and content are correct.

### Y092 — scanned over [1, 8] rather than [1, 3] the widest band is 1.71 wide ([3.50, 5.21], {doab, genua, hangzhou}), and 1.5's is not the widest by any margin

**Status:** CONFIRMED
**Method:** Re-ran the 701-point α sweep and the band segmentation (`measure6.py`).
**Evidence:** `widest band on [1,8]  ('doab+genua+hangzhou', 3.5, 5.21, 1.71)`. Against 1.5's band
width of 0.25 (Y093), the ratio is 6.8×, so "not the widest by any margin" is right. (v6.0's own
earlier draft said 1.70 wide over [3.51, 5.21]; the shipped 1.71 over [3.50, 5.21] is what the sweep
gives.)

### Y093 — across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and α_Φ = 1.5 sits in the band [1.38, 1.63], width 0.25, which gives {english_channel, hangzhou}

**Status:** CONFIRMED
**Method:** As above.
**Evidence:** `band containing alpha=1.5  ('english_channel+hangzhou', 1.38, 1.63, 0.25)`. The
sweep's 701 samples segment into contiguous constant-set runs, which is what "step function" means
here.

### Y094 — sampled at the six values v2 used, the count is non-monotone: 6 → 2 → 1 → 2 → 3 → 1

**Status:** CONFIRMED
**Method:** Sink counts at α_Φ ∈ {1, 1.5, 2, 3, 4, 8} (`measure6.py`).
**Evidence:** `[6, 2, 1, 2, 3, 1]` — it falls, rises, rises and falls, so non-monotone with two
turning points.

### Y095 — a warning to future revisers: the 1444 map has two ends and vanilla's authored map has three, and 1.5 must not be justified by that resemblance

**Status:** CONFIRMED
**Method:** Counted `end = yes` in `common/tradenodes/00_tradenodes.txt`; checked the 1444 count.
**Evidence:** vanilla has **3** end nodes — `genua`, `venice`, `english_channel`; the 1444 `Φ_w` map
has **2**. Both figures are right, so the resemblance the warning guards against is real (two against
three, not a match), and the stipulation is coherent: §2.3 withdrew exactly that calibration
(Y072/Y091), so re-deriving 1.5 from the resemblance would reintroduce it.

### Y096 — Europe becomes the centre of trade as it develops: the design claim §3.1's first goal asks the field to deliver

**Status:** CONFIRMED
**Method:** Read §3.1 goal 1 against the Europe measurements.
**Evidence:** Goal 1 is "Trade direction follows the world's current state, never authored arrows",
and the Europe table is the test of whether the field delivers a European centre when Europe is the
rich region. It does: from ×1.56 upward every end is European (`english_channel`/`rheinland`, then
`genua` alone), and the mechanism is wealth, not a knob. As a directional design statement with a
working mechanism behind it, this is exactly the form §0's convention prescribes.

### Y097 — at 1444 the map already ends in the Channel and in Hangzhou; as European development compounds the Channel's basin grows and Asia's pole fades, and past a broad range of European growth Asia holds no end at all

**Status:** PARTIAL
**Method:** Swept European province development ×1.00 to ×4.00 at α_Φ = 1.5, recording the sink set
and the number of nodes able to reach each sink (`m8.py`, `m9.py`).
**Evidence (confirmed):** Asia's pole fades monotonically — `hangzhou`'s basin runs 78 → 61 → 60 → 33
→ 22 → 14 nodes at ×1.00, ×1.02, ×1.10, ×1.20, ×1.30, ×1.40 — and Asia holds **no** end at ×1.56,
×1.70, ×1.80, ×2.00, ×2.50, ×3.00 and ×4.00, which is a broad range ✓.
**Evidence (the Channel — only to ×1.56):** `english_channel`'s basin does grow, 18 → 18 → 19 → 21 →
23 → 28 → 26 across ×1.00…×1.56. But at **×1.70 and above the Channel is not an end at all** —
`genua` alone holds the map, with a basin of 80. So "the Channel's basin grows" holds over
×1.02–×1.56 and reverses beyond it; the *European* centre survives, the Channel does not.
**Should say:** "the Channel's basin grows through moderate growth and Asia's pole fades; past about
×1.6 Asia holds no end, and past about ×1.7 a single Mediterranean end takes the map."

### Y098 — the mechanism: wealth is linear in development, so developing a region moves its c_w share directly and Φ_w's ends follow the wealth

**Status:** CONFIRMED
**Method:** Checked as a derivation from the wealth expression, then numerically (Y103).
**Evidence:** `wealth(p) = 1.0·base_tax + 0.2·base_production·price` is homogeneous of degree 1 in
`(base_tax, base_production)`, so scaling a province's development by `k` scales its wealth by exactly
`k`. `c_w(n) = Σ_{p∈n} wealth(p)^1.5 / Σ_world wealth^1.5` is then strictly increasing in the scaled
region's share, and `b_w = 1/N − c_w` moves with it. The mechanism is the one stated.

### Y099 — observed with europe.py over 824 counted European provinces: ×1.02 gives {english_channel, hangzhou, wien}

**Status:** CONFIRMED
**Method:** Recomputed the European counted set from `map/continent.txt` and re-ran the scaling
(`measure6.py`, `m8.py`).
**Evidence:** European counted provinces **824**; ×1.02 sinks `['english_channel', 'hangzhou',
'wien']`. Both reproduce exactly, and `verify6.py` guards the 824 against the computed value.

### Y100 — at ×2.00 European development the sink set is genua alone

**Status:** CONFIRMED
**Method:** As above.
**Evidence:** `Europe development x2.00 sinks  ['genua']`, and the same result on the independent
five-phase instrument at the shipped order.

### Y101 — read the table as a direction rather than a trajectory, and on one node ordering: which European node holds an end at the smaller factors is ordering-dependent, so the direction is the claim and the membership is not

**Status:** CONFIRMED
**Method:** Y076–Y081's relabelling result applied to the table's smaller factors, plus Y102's
×2.00 control.
**Evidence:** At ×1.00 the membership is already ordering-dependent (`english_channel` 31–47 per
hundred), and the smaller Europe factors inherit that. The direction — ends move west, Asia thins —
holds on every ordering because it is carried by the wealth field, not the labelling. The
qualification is correct and correctly scoped.

### Y102 — the ×2.00 row is the exception: genua held an end in 60 of 60 relabellings

**Status:** CONFIRMED
**Method:** 60 relabellings of the ×2.00 European field on the validated five-phase instrument
(`perg.py`).
**Evidence:** `genua` held an end in **60 of 60**. Other nodes appear as additional ends in some
orderings (`rheinland` 11, `wien` 4), so the *set* is not invariant, but `genua`'s end is. The claim
is about `genua` holding an end and is exactly right; the shipped order additionally gives `genua`
alone.

### Y103 — because §1.3's wealth is linear in development, scaling development and scaling wealth are the same operation here — maximum difference 0.0 across the European set

**Status:** CONFIRMED
**Method:** Recomputed the field from scratch with `base_tax` and `base_production` multiplied by `k`
for the 824 European provinces, and compared against multiplying the wealth column by `k` (`m8.py`).
**Evidence:** maximum absolute difference **3.55e-15** at ×1.02 and ×1.56 and **0.0** at ×2.00 —
float noise on an exact identity, so "maximum difference 0.0" is right to any printed precision.
**Recorded as an instrument defect, not a claim defect:** `measure6.py`'s own check for this is
vacuous. It computes `a1 = W.copy(); a1[eur] *= 1.56` and compares against
`devscale(eur, 1.56)`, which is the same expression, so the printed
`dev-scaling equals wealth-scaling (max diff)  0.0` is `W·k` against `W·k` and would print 0.0 no
matter what the wealth formula were. The claim is true; the line that appears to verify it does not.

### Y104 — the 1444 Silk Road route from Genoa to the Asian sink runs genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou

**Status:** CONFIRMED
**Method:** BFS on the recomputed `Φ_w` orientation, independently of `measure6.py` (`m5.py`).
**Evidence:** `['genua', 'alexandria', 'aleppo', 'persia', 'lahore', 'lhasa', 'ganges_delta',
'burma', 'gulf_of_siam', 'canton', 'hangzhou']` — the eleven nodes in the stated order, with `lhasa`
where v5.0 had `doab`. The Volga route also holds: `north_sea → white_sea → novgorod → kazan →
astrakhan → persia → …`.

### Y105 — no route leaves english_channel at all: it is a sink with out-degree 0, so the Hansa and the Danube carry power into it, and v5.0's "from the Channel it is the Hansa and the Danube" describes a path that does not exist

**Status:** CONFIRMED
**Method:** Measured `english_channel`'s out-degree; attempted a BFS from it (`m2.py`, `m5.py`).
**Evidence:** out-degree **0**; `route english_channel -> hangzhou` returns **None**. A node with
out-degree 0 has no outgoing route to anywhere, so v5.0's sentence described a path that cannot
exist on its own field either. `measure6.py` now distinguishes "NO ROUTE" from "avoids cape",
having previously printed `False` for both — a real correction, since the two facts read the same
way otherwise.

### Y106 — no Europe→sink route passes the Cape of Good Hope, checked from genua, north_sea and english_channel

**Status:** CONFIRMED
**Method:** Reachability, not path enumeration: computed whether the Cape is reachable at all from
each of the three (`m5.py`).
**Evidence:** `cape reachable from genua  False`; `from north_sea  False`; `from english_channel
False`. That is stronger than the claim needs — no route from any of the three reaches the Cape at
all, so a fortiori no Europe→sink route passes it.

### Y107 — the Cape is a live Φ_w conduit: in-degree 1, out-degree 3, with 132 ordered node pairs whose path runs through it

**Status:** CONFIRMED
**Method:** Degrees and an upstream × downstream reachability count on the recomputed orientation
(`m2.py`, `m5.py`).
**Evidence:** in-degree **1** (`ivory_coast`), out-degree **3** (`comorin_cape`, `malacca`,
`zanzibar`), and **132** ordered pairs `(a, b)` with the Cape upstream of `b`, downstream of `a`, and
`b` reachable from `a`. The Cape reaches a sink (`cape_of_good_hope → malacca → hangzhou`), so the
drainage is genuinely Atlantic-into-Indian-Ocean as described.

### Y108 — v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes

**Status:** CONFIRMED
**Method:** Y107's 132 pairs against v5.0's sentence; `verify6.py` asserts the sentence's absence.
**Evidence:** 132 ordered pairs route through the Cape, so the universal is false. And Y106 shows
what *is* true — the Europe→sink check — which is the narrower claim v5.0's evidence could support.
`verify6.py:156` carries `absent(doc, …, "Nothing routes through the Cape")` and it passes, so the
false universal is out of the document.

### Y109 — in the per-good graphs the Cape also carries Asian spices to Europe; Φ_w models power, not cargo; the specific malacca → cape_of_good_hope → … route v5.0 quoted is no longer given

**Status:** CONFIRMED
**Method:** BFS on the spices graph; grepped the v6.0 spec for the route (`m8.py`).
**Evidence:** The spices orientation carries `malacca → cape_of_good_hope → zanzibar →
gulf_of_aden → alexandria → genua` — exactly the chain v5.0 quoted, so the substantive claim is true
on the current field. The Cape has both in- and out-degree non-zero for **29 of 29** goods, so it is
a conduit for every good. And the route string appears **0 times** in the v6.0 spec, so it is
genuinely no longer given.

### Y110 — scaling the 22 European nodes rather than European provinces makes genua the sole sink from about ×1.65, and the 18-node western/central subset needs about ×2.15

**Status:** CONFIRMED
**Method:** Swept the multiplier on a 0.05 grid then refined to 0.01, for both node sets, checking
the 22 names against the node list first (`m4.py`).
**Evidence:** all 22 names resolve. 22-node set: first sole-`genua` at **×1.65** on the 0.05 grid,
**×1.63** refined. 18-node subset: **×2.15** on the 0.05 grid, **×2.14** refined. Both match the
document's "about" figures to within the grid it was evidently measured on.

### Y111 — the Cape of Good Hope reverses somewhere inside roughly ×2.9–×3.5 — bounded above as well as below, so a window and not a threshold

**Status:** CONFIRMED
**Method:** Swept the 22-node multiplier ×1.0 to ×6.0 at 0.1, recording the Cape's in- and
out-neighbours at each step (`m4.py`).
**Evidence:** baseline in `{ivory_coast}`, out `{comorin_cape, malacca, zanzibar}`. The full
reversal — in `{comorin_cape, malacca, zanzibar}`, out `{ivory_coast}` — holds at
**×2.9, 3.0, 3.1, 3.2, 3.3, 3.4** and at no other sampled factor. At ×2.5–×2.8 and again from ×3.5
the Cape is in a mixed state (in `{malacca}`, out `{comorin_cape, ivory_coast, zanzibar}`). So the
reversal is a window inside the stated ×2.9–×3.5, bounded above as well as below, exactly as
claimed, and it is not a threshold.

### Y112 — dev-stacking a single node's top province concentrates the map on that node; extra sinks at intermediate boosts are expected behaviour, not noise

**Status:** CONFIRMED
**Method:** Multiplied the richest counted province of `hangzhou` and of `genua` by ×2, ×5, ×10, ×20,
×30, ×50 and recorded the sink set (`m8.py`).
**Evidence:** `hangzhou`: ×2 and ×5 → `{hangzhou}` alone; ×10 → `{genua, gulf_of_siam, hangzhou}`
(the intermediate split); ×20, ×30, ×50 → `{hangzhou}` alone. `genua`: ×2 and ×5 →
`{english_channel, hangzhou}`; ×10 → four sinks; ×20 → three; ×30 and ×50 → `{genua}` alone. Both
show concentration on the boosted node with a transient multi-sink phase in between, which is the
claim. The `hangzhou`-specific ×10/×20/×30/×50 figures are indeed dropped from the spec (`×20`
appears 0 times).

---

## §1.10 — Direction-dependent systems

### Y113 — banding absorbs very little chatter, not "almost nothing absorbs threshold chatter", because banding is not the only damper

**Status:** CONFIRMED
**Method:** Checked as a derivation against Y114–Y116's file values, and against the threshold table
in the same section.
**Evidence:** The table lists nine threshold mechanics of which exactly one — Improve Inland Routes,
50/40 — is unconditionally banded, and Propagate Religion is banded only on its flag ladder. So
banding covers very little. But three shipped defines rate-limit the mechanics that carry those
thresholds (Y114, Y115), so *something other than banding* damps the flicker, which is precisely
why "almost nothing absorbs threshold chatter" is the wrong claim and "banding absorbs very little"
is the right one. The correction is sound and the reason it gives is the reason that holds.

### Y114 — ⚑ TRADING_POLICY_COOLDOWN_MONTHS = 12 applies to seven of the nine entries in 00_trading_policies.txt — five distinct policies, four with an _upgraded twin, plus Propagate Religion which has none — so four of the five families are rate-limited; maximize_profit and maximize_profit_upgraded carry cooldown = no

**Status:** CONFIRMED
**Method:** Listed every top-level block and every `cooldown` key in
`common/trading_policies/00_trading_policies.txt`; read the define.
**Evidence:** Nine entries at lines 3, 29, 55, 78, 101, 146, 192, 218, 239 —
`maximize_profit`, `maximize_profit_upgraded`, `hostile_trading`, `hostile_trading_upgraded`,
`improve_inland_routes`, `improve_inland_routes_upgraded`, `establish_communities`,
`establish_communities_upgraded`, `propagate_religion`. `cooldown = no` appears exactly twice, at
lines 25 and 52 — inside `maximize_profit` and `maximize_profit_upgraded`. So **7 of 9** entries take
the cooldown. Five distinct families ✓; four of them have an `_upgraded` twin ✓; `propagate_religion`
has none ✓; and the rate-limited families are `hostile_trading`, `improve_inland_routes`,
`establish_communities` and `propagate_religion` — **four of the five**, including Propagate
Religion ✓. `common/defines.lua:1045`: `TRADING_POLICY_COOLDOWN_MONTHS  = 12`.

### Y115 — ⚑ TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30 and TRADE_COMPANY_COOLDOWN = 60 are shipped defines

**Status:** CONFIRMED
**Method:** Grepped `common/defines.lua`.
**Evidence:** line 1212 `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30,`; line 1214
`TRADE_COMPANY_COOLDOWN = 60,`. Both present, both at the stated values.

### Y116 — at those three, a flickering power share does not translate into a flickering effect; what is left exposed is everything without a cooldown, which is most of the ladder

**Status:** CONFIRMED
**Method:** Checked as a derivation against the section's threshold table and Y114/Y115.
**Evidence:** The three defines cover trading-policy selection (7 of 9 entries) and two
trade-company actions. The table's remaining rows — trade-conflict casus belli target and actor,
privateer blocking, trade-company extra merchant, trade-company control — have no cooldown named
anywhere in the section or in `defines.lua` under those keys, and Improve Inland Routes' banding is
the only structural damper. So "most of the ladder" is exposed, and the inference from a cooldown to
a non-flickering *effect* is the right one: a monthly-recomputed share cannot re-trigger a mechanic
inside its cooldown window.

### Y117 — measured on the 1444 start: the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.6% over the flag's 26 inland nodes, whose totals run 106.4 at xian to 532.0 at champagne

**Status:** CONFIRMED
**Method:** Parsed all 80 `node={}` blocks out of the save's `trade={}` structure at brace depth,
reading each node's `total` and each country sub-block's `val`; took the inland set from
`inland = yes` in `common/tradenodes/00_tradenodes.txt` (`caravan.py`).
**Evidence:** 26 nodes carry `inland = yes`. Over them: totals run **106.366 at `xian`** to
**531.98 at `champagne`** (printed 106.4 and 532.0 ✓); `50/total` runs **9.4%** to **47.0%** with
median **21.6%** ✓. The corroborating figures in the same passage also hold: the largest single
incumbent holder runs **23.6 to 143.2**, and 50 exceeds it in **7 of the 26** nodes.

### Y118 — as a share of the node's total after the grant lands the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8 rather than 50

**Status:** CONFIRMED
**Method:** Recomputed `50/(total+50)` over the same 26 nodes; read v5.0's sentence.
**Evidence:** `50/(total+50)` runs **8.6%** to **32.0%** with median **17.7%** ✓. And
0.086 × 531.98 = **45.75**, not 50 — so the arithmetic check the claim offers is right and it is
decisive. `v5:553–555` reads "the cap of 50 is **8.6% to 32.0% of an inland node's total trade
power** (median 17.9% … whose totals run 106.4 at `xian` to 532.0 at `champagne`)", i.e. the
post-grant numbers under the pre-grant description, with the pre-grant totals in the same
parenthesis. `9.4%`, `47.0%` and `21.6%` appear **0 times** in v5.0's spec.

### Y119 — on §2.2's derived 25-node inland basis the median is 21.3% pre-grant, or 17.5% after

**Status:** CONFIRMED
**Method:** Recomputed both medians over the members-derived inland set (no coastal province among
`members`), and checked the two definitions against each other (`caravan.py`).
**Evidence:** The derived set has **25** nodes; the flag set has 26; the difference is exactly
`{siberia}`, which §2.2 also names. Over the 25: median `50/total` **21.3%**, median
`50/(total+50)` **17.5%** ✓. The range (9.4–47.0 / 8.6–32.0), the largest-incumbent span
(23.6–143.2) and the 7-node count are all unchanged between the two bases, so only the median moves,
as §1.10 says.

---

## §2.2 — Solver

### Y120 — solver item 4 computes the stated expression with no autonomy, efficiency, ideas or owner terms; the only modifiers read are the four province-condition ones, and at 1444 only devastation is live, on eleven provinces

**Status:** CONFIRMED
**Method:** Read §2.2 item 4 against `solver.py:province_table()` term by term.
**Evidence:** The spec's expression is
`TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production ·
(1 + province-state goods modifiers) · price`; the implementation is
`tax = TAX_COEFF*base_tax*(1+tmod)` and `prod_income = max(0, GP_COEFF*base_production*(1+gmod))*price`,
summed. `STATE_GOODS_MOD` and `STATE_TAX_MOD` hold exactly the four condition modifiers; only
`devastation` has a non-zero level at 1444 and only on the eleven provinces of Y049. World wealth
**10,607.40** over **2,472** counted provinces, and `verify6.py` guards both against the computed
values. The one difference is the `max(0, ·)` clamp the spec's formula does not show, which is inert
below devastation 100.

### Y121 — measured on the reference implementation: of order 0.1 s for all 29 goods, and single-digit milliseconds per good on average — and that is the whole of the claim

**Status:** CONFIRMED
**Method:** Six replicates of twelve all-29-goods runs through `run_drain`, three under incidental
load and three idle (`m4.py`, `m5.py`).
**Evidence:** all-29 wall time, medians across the six replicates: 0.173, 0.169, 0.177, 0.245, 0.152,
0.124 s — order 0.1 s ✓. Per-good averages spanned 3.4 to 9.9 ms across all six — single-digit
milliseconds ✓. The claim is stated at exactly the precision the measurement supports, which is the
point of "that is the whole of the claim".

### Y122 — repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer; three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms

**Status:** CONFIRMED
**Method:** As Y121.
**Evidence:** The proposition is confirmed in kind and by re-running: my six replicates gave per-good
spans (4.7–7.4), (4.6–6.4), (4.2–8.5), (3.4–9.9), (5.0–6.4), (3.4–6.9) ms — six different spans, no
two alike, on one machine with one build. The specific spans the document quotes are not
reproducible, which is what the claim itself asserts; quoting them as an illustration of
irreproducibility is self-consistent. Recorded so a later reader does not treat 3.5–10.5 as a
reference interval.

### Y123 — v5.0 quoted "0.17–0.21 s for all 29 goods"; across three replicates of twelve runs, the number of runs landing inside that interval was 1, then 0, then 0

**Status:** PARTIAL
**Method:** Verified the v5.0 quotation; then re-ran the same experiment six times — three replicates
of twelve under incidental load and three idle — counting runs inside [0.17, 0.21] s (`m4.py`,
`m5.py`).
**Evidence (the quotation — confirmed):** `v5:644–645` reads "**0.17–0.21 s for all 29 goods**, a
mean of 5.7–7.3 ms per good across runs".
**Evidence (the counts — not reproducible):** runs inside the interval, six replicates of twelve:
**6, 6, 5, then 2, 1, 2**. Under load the majority of runs landed *inside* v5.0's interval; idle,
one or two did. The document's 1/0/0 is one draw of a quantity §2.2 itself describes as measuring "a
machine and a scheduler rather than the algorithm", and it is the low end of what the same experiment
produces.
**Should say:** either drop the counts and keep "does not reproduce closely enough to support
anything finer", or state them with the spread — 0 to 6 of twelve across replicates.

---

## §2.2a — What map this is for

### Y124 — where Phase 0 acts, free-edge determinism is unaffected but index-independence is not: the key reads the post-fold balance β, so peeling can create exact ties the raw balances do not have, and the 1444 measurement does not transfer

**Status:** CONFIRMED
**Method:** Read `drain.py:phase0()` and `sweep_priority()` as an argument; confirmed the 1444
measurement's scope.
**Evidence:** `phase0` returns `beta` with `beta[u] += beta[v]` for each peeled pendant, and both
`flow_def()` and the priority key read that `beta`, not the input `b`. Folding is a sum, so two
parents with distinct raw balances can receive folds that make their `β` equal — the peel *creates*
ties. Determinism is untouched because the key remains a deterministic function of `(DEF, β, index)`
whatever the values are; what fails is the stronger property that the index never decides. And the
1444 measurement (zero exact ties, 29/29) is taken on a map where Phase 0 removes nothing — the peel
log has length **0** (Y022) — so it says nothing about maps where it acts. The distinction the claim
draws is exactly right.

---

## §2.3 — Constants

### Y125 — v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them

**Status:** PARTIAL
**Method:** Grepped each version's constants section; counted "whole install" occurrences; checked
which files the sweep read.
**Evidence (the provenance half — confirmed):** `v3:544–547`, `v4:616–619` and `v5:716–719` carry,
verbatim, "**Engine constants that are not defines.** The two wealth coefficients of §1.3 are
hardcoded in the binary — `defines.lua` and `common/defines/` were searched and contain neither." All
three assert exactly what Y034 refutes: `provincial_production_size = { trade_goods_size = 0.2 }` is
in a shipped file.
**Evidence (the sweep half — v5.0 only):** "whole install" appears **3 times in v5.0's spec and 0
times in v3.0's and v4.0's**. v4.0 *stated* the whole-install rule (`v4:184`) but swept only
`common/tradegoods/` — which is what `validation-v5.md`'s X034 establishes — and v3.0 had neither the
rule nor a sweep. So only v5.0 shipped the sweep the sentence describes. That v5.0's sweep walked
past the block is right: its §1.3 table reads the four province-state modifiers out of
`00_static_modifiers.txt`, and `provincial_production_size` sits at line 251 of the same file.
**Should say:** "v3.0 through v5.0 said neither wealth coefficient was in a file, and v5.0's
whole-install modifier sweep read the very file holding one of them without noticing it."

### Y126 — every derivation previously offered for α_Φ is withdrawn, and neither is a reason: the first fits a constant to one date, and the second depended on where the α scan was truncated; v5.0's noise-stability rejection ground is not the ground given

**Status:** CONFIRMED
**Method:** Read §2.3's withdrawal paragraph; grepped the v6.0 spec for the noise ground; checked the
truncation claim numerically.
**Evidence:** §2.3 gives exactly two grounds — "the first fits a constant to one date, and the second
depended on where the α scan was truncated (§1.6)" — and both are sound: the calibration was to the
1444 map specifically (Y072), and Y092 shows the "widest band" verdict flips when the scan runs to 8
instead of 3 (1.5's band 0.25 wide against a widest of 1.71). The phrase "narrower than the
uncertainty" appears **0 times** in the v6.0 spec, so v5.0's noise-based rejection ground is indeed
not the ground given. The parenthetical is accurate.

---

## §2.4 — The tradenodes file

### Y127 — the canonical order must be the order Phase 2's LP input is built in, not merely the order the sweep breaks ties in

**Status:** CONFIRMED
**Method:** Isolated the two mechanisms: permuted arc presentation order with node labels held fixed,
and counted priority-key ties (`perg.py`).
**Evidence:** With labels fixed and only the arc list reordered, the optimal *support* changed on
**10 of 10** goods tested, 10 times out of 10 each. Meanwhile the sweep's tie sites never fire on
1444 (0/0/0, Y135). So the order that matters is the LP input's, and the sweep's tiebreak order is
not it. A further control from the corrected harness: a pure permutation of the LP's *rows* with the
column construction untouched changes nothing at all, which locates the sensitivity precisely in arc
presentation.

### Y128 — measured on 1444: relabelling and running end-to-end changed the orientation on 580 of 580 runs (29 goods × 20 relabellings), always by returning a different optimal vertex and never by a sweep tiebreak, with a mean of 22.1 of 159 edges moving and the objective identical to 8.9e-16

**Status:** PARTIAL
**Method:** 29 goods × 20 relabellings on the validated five-phase instrument, recording for each run
whether the flow support changed, the edge distance from the identity-permutation baseline, and the
objective (`perg.py`).
**Evidence (confirmed):** **580 of 580** changed. **580 of 580 changed the flow support**, and **0**
changed with the support held fixed — so "always a different optimal vertex, never a sweep tiebreak"
is exact. Maximum objective deviation **8.88e-16**, which is the quoted 8.9e-16.
**Evidence (the mean):** **21.39** of 159 at an independent permutation seed, against the document's
22.1. The 20 permutations are shared across the 29 goods, so the effective sample is 20, not 580, and
a 0.7-edge difference is within that sampling spread — but the figure is stated without qualification
and does not reproduce.
**Should say:** "a mean of about 21–22 of 159 edges moving".

### Y129 — permuting only the arc presentation order with node labels held fixed changes the optimal support on 10 of 10 goods tested, with objective gaps ≤ 1.8e-15

**Status:** CONFIRMED
**Method:** Ten random arc permutations per good on the first ten live goods, labels fixed
(`perg.py`).
**Evidence:** support changed **10/10 runs on 10/10 goods** (`chinaware`, `cloth`, `cloves`, `cocoa`,
`coffee`, `copper`, `cotton`, `dyes`, `fish`, `fur`); orientation changed 10/10 as well. Maximum
objective gap over all 100 runs **8.88e-16**, comfortably inside the stated ≤ 1.8e-15.
**Recorded as a sourcing defect, not a claim defect:** the spec attributes this to
"(the field from `measure6.py`; the relabelling sweep is recorded in
`../v5-owner-agnostic/validation-v5.md`)". `measure6.py` contains **no** arc-permutation experiment,
and `validation-v5.md` contains no 29 × 20 relabelling sweep — grepping it for `580`, `22.1` and
`8.9e-16` returns nothing. The experiment exists in `scripts/preconfirm3.py` for the `Φ_w` case only;
the per-good and arc-order runs are in no shipped script. The measurement is right and the pointer
to where it came from is not.

### Y130 — twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event

**Status:** CONFIRMED
**Method:** Compared the two measured quantities directly.
**Evidence:** razed-`hangzhou` gives **22 of 159** edges flipping (Y141); relabelling gives a mean of
**21.4–22.1 of 159** (Y128) with a per-run range of 4 to 53. Same magnitude, and the comparison is
the right one to draw: a pure relabelling with every input fixed moves as much of the map as deleting
China's wealth pole.

### Y131 — everything §1.6 and §2.8 report about stability is measured at fixed node order; re-order the same world and the map moves, with α_Φ and every input held fixed

**Status:** CONFIRMED
**Method:** Checked which measurements hold the order fixed; re-ran the relabelling study with α_Φ
and the wealth field untouched.
**Evidence:** Every §1.6 and §2.8 figure comes from `measure6.py` or the same solver at the shipped
`nodes.json` order. The relabelling study varies only the labelling — same `b_w`, same α_Φ = 1.5,
same adjacency — and 400 of 400 runs move the orientation, mean about 25 of 159 edges. The caution is
accurate and is the strongest single finding in this section.

### Y132 — the specific 580/580 result is HiGHS-specific in its detail but not in kind — any simplex returns a vertex of a degenerate optimal face

**Status:** CONFIRMED
**Method:** Checked as a derivation, and checked its premise numerically. Only HiGHS was available,
so the cross-solver half is argued rather than measured, and that is recorded.
**Evidence:** The premise is established: distinct supports occur at the same optimal cost to within
2 ULP (Y077), so the optimal face has multiple vertices. Any method that returns a basic optimum
must therefore select one of them, and its selection is a function of the pivoting rule and the input
order — so the *phenomenon* is not HiGHS's, only the particular vertex is. The derivation is valid;
"in kind" is the right scope and the document does not over-claim it.

### Y133 — making the orientation independent of presentation order would need a tie-breaking objective — a lexicographic secondary cost, or a strictly convex perturbation — which is a design change and is not adopted here

**Status:** CONFIRMED
**Method:** Checked as an argument.
**Evidence:** The degeneracy is in the objective, not in the algorithm: with all arc costs 1, any two
supports serving `b` at the same hop total are exactly tied, and no pivoting rule can break a tie the
objective does not distinguish. The two named remedies are the standard ones and both change the
program being solved — a lexicographic secondary cost changes the optimum's definition, and a
strictly convex perturbation changes the feasible optimum's location. And they are not adopted:
`flowop.py:mincost_flow` passes `c = np.ones(A)` with no secondary term. Both halves hold.

### Y134 — §1.1's priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass

**Status:** CONFIRMED
**Method:** Located each tie site in `drain.py`.
**Evidence:** Four sites. (1) Free-edge sweep: `keyfn(v) = (DEF[v], beta[v], pid[v])` in
`sweep_priority`. (2) Phase 1's within-cluster argmin: `S.add(min(comps[j], key=lambda v: (beta[v],
v)))` in `phase1` — index-broken. (3) The stall promotion: `s_star = min(terminals, key=lambda v:
(beta[v], v))` — the identical form. (4) The top-k cut:
`top = sorted(range(len(comps)), key=lambda j: -M[j])[:k]`, whose order among equal `M[j]` is
Python's stable sort, i.e. cluster-construction order, itself a function of the node indexing. §1.1
documents only the first. The claim is correct and the enumeration is complete.

### Y135 — none of them fires on 1444 — zero exact (DEF, β) ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses

**Status:** CONFIRMED
**Method:** Census over all 29 live goods of each of the three measurable tie sites (`perg.py`).
**Evidence:** exact `(DEF, β)` ties among free-edge-incident core nodes: **0**, goods affected
**0/29**. Within-cluster exact β argmin ties: **0**. Tied cluster masses: **0**. So no measured figure
in the document depends on any index tiebreak — which is what makes Y007's and Y021's attribution to
Phase 2 rather than to the key the only available explanation.

### Y136 — the end-flag list is a function of the canonical node order required by item 1, not of the world alone; fix the order, emit, and keep it

**Status:** CONFIRMED
**Method:** Checked as a derivation against Y078–Y082.
**Evidence:** §2.4 item 2 defines the flag list as `end=yes` on every `Φ_w` sink, and the sink set is
ordering-conditional (membership and size both move; 22–26 distinct sets per hundred relabellings).
So the list is a function of the order as well as the world, and the operational advice — fix it, emit,
keep it — follows directly, because re-emitting under a different order would rewrite the flags with
nothing in the world having changed. The derivation is sound and it is the right consequence to draw.

### Y137 — end flags at 1444 in the shipped order: two end nodes, english_channel and hangzhou, against vanilla's three

**Status:** CONFIRMED
**Method:** Recomputed the sink set at the shipped `nodes.json` order; counted `end = yes` in
`common/tradenodes/00_tradenodes.txt`.
**Evidence:** two ends, `english_channel` and `hangzhou`. Vanilla has **3** `end = yes` nodes —
`genua`, `venice`, `english_channel`. Both figures are right, and Y095's warning against reading the
2-against-3 as a calibration target is the correct accompanying caution.

---

## §2.7 — Probes

### Y138 — § probe 15's finding is one observation on one node — enough to retire §3.16's cautionary case and not enough to promote §1.9's "every immediately upstream node" to a measurement; v3.0 through v5.0 said the rule was "correct as written and gains no qualifier"

**Status:** CONFIRMED
**Method:** Read the probe record in `../v2-drain/game-session.md`; grepped v3.0, v4.0 and v5.0 for
the withdrawn wording. **EU4 was not run in this pass**, so the observation itself is graded on the
record that exists rather than re-taken.
**Evidence (the strength claim):** `game-session.md:412–430` records exactly one case that tests the
qualifier — France in Sevilla, 0.0 provinces and 0.0 merchants, 3.3 power, itemised by the engine as
`Transfers from traders downstream: +3.1` and nothing else. The document's "Corroboration" section
offers Castile in Safi, but Castile holds `Base: 2` and `Merchant Present: +2.0` there, so that case
does **not** test a receiving node where the country has no power. One observation on one node, as
claimed.
**Evidence (the attribution):** `v3:649`, `v4:724` and `v5:835` all read "…as written and gains no
qualifier. §3.16's cautionary case closes." — verbatim in all three.
**Evidence (the split verdict):** retiring the cautionary case needs only that the qualifier be
false once, which the observation gives; promoting "every immediately upstream node" to a measurement
would need a census over upstream nodes, which nothing in the record provides. The asymmetry the
claim draws is the correct one.

---

## §2.8 — Validation

### Y139 — most goods, 1444: sinks are 1 to 8 per good; high-demand nodes are sinks at 16.8% in the top demand decile against 6.9% in the bottom

**Status:** CONFIRMED
**Method:** Reconstructed the decile statistic four different ways to find the one the figures come
from (`m4.py`).
**Evidence:** Taking, per good, the top eight and bottom eight nodes by that good's `c_g` and pooling
over the 29 goods gives **16.8%** and **6.9%** — the document's figures exactly. (The three
alternatives do not: pooling all 2,320 (good, node) pairs and slicing deciles by `c` gives 15.9/8.2;
excluding zero-demand nodes gives 15.7/8.7; slicing nodes by aggregate `c_w` gives 14.7/8.6. The
construction is per-good deciles of nodes, which is the natural reading of "the top demand decile"
for a per-good statistic.) Sinks per good **1 to 8** ✓ (Y022).

### Y140 — the Razed-China row is ordering-robust where §1.6's sink membership is not: it turns on hangzhou holding an end, which it does under every relabelling tried

**Status:** REFUTED
**Method:** 400 relabellings across four independent seeds on the validated five-phase instrument,
counting the runs in which `hangzhou` is not a sink (`relabel2.py`); then read §1.6's own statement
of the same quantity.
**Evidence:** `hangzhou` held an end in **97, 100, 98 and 96** runs per hundred — so it lost its end
in **9 of 400** relabellings. The project's own `scripts/preconfirm3-relabel.out` gives 100, 99, 97,
100, 98 over five seeds, i.e. **6 of 500**. Either way, orderings exist where the Asian end moves,
and "under every relabelling tried" is false on the document's own data.
The claim is also internally contradicted: §1.6, in the passage §2.8 cross-references, states the
same quantity as "`hangzhou` was an end in **97 to 100 per hundred**", and §2.4 item 2 restates it as
"97–100 orderings per hundred". `changes-v6.md`'s round-five note identifies this exact defect —
"a universal quantifier had been introduced *by* the edit that was removing universal quantifiers" —
and fixes §1.6 and §2.4 while leaving §2.8's row unchanged.
**Should say:** "it turns on `hangzhou` holding an end, which it does in about 98 relabellings per
hundred (§1.6) — far more robustly than the sink set as a whole, which returns exactly in about 9."
The row's *comparative* content survives; only the universal does not.

### Y141 — zeroing hangzhou-node development moves the Φ_w sinks from {english_channel, hangzhou} to {doab, english_channel, gulf_of_siam}, with 22 of 159 edges flipping

**Status:** CONFIRMED
**Method:** Zeroed the wealth of every counted province in the `hangzhou` node, re-solved, and
differenced the edge sets (`m2.py`).
**Evidence:** sinks `['doab', 'english_channel', 'gulf_of_siam']`; flips **22 of 159**. Both exact.

### Y142 — hangzhou, not beijing, is China's wealth pole under §1.3: node wealth 226.7 against 143.0, and it holds the richest single province the model counts

**Status:** CONFIRMED
**Method:** Recomputed node wealth and the per-province maximum (`m2.py`).
**Evidence:** `hangzhou` **226.7** (node-wealth rank 12), `beijing` **143.0** (rank 39). The richest
counted province is **1821 at 27.00**, which lies in the `hangzhou` node; `beijing`'s best is 1816 at
19.5. Top five counted provinces: 1821 (hangzhou) 27.00, 684 (hangzhou) 21.60, 1816 (beijing) 19.50,
685 (hangzhou) 19.20, 667 (canton) 18.00 — so `hangzhou` holds three of the top five. The v5.0
`c_w` rank-1-against-31 comparison is indeed not restated, and it would be wrong now:
`hangzhou`'s `c_w` rank is 3.

### Y143 — zeroing beijing also moves the map — 15 flips — because deleting a percent of world wealth renormalises c_w everywhere; what separates the two cases is which node keeps its end

**Status:** CONFIRMED
**Method:** As Y141, for the `beijing` node (`m2.py`).
**Evidence:** zeroing `beijing` gives **15** flips with the sink set **unchanged** at
`{english_channel, hangzhou}`; zeroing `hangzhou` gives 22 flips and a different sink set. So both
perturbations move the map and only one relocates an end — exactly the separation the claim draws,
and the correction to v2–v4.0's "moves nothing" is right. `beijing`'s 143.0 of 10,607.40 is 1.35% of
world wealth, so "a percent" is the right order.

---

## §3.2 — Why a flow and a drainage sweep

### Y144 — what the ratio metric cannot see is the thing the diagnosis rests on: a max/min contrast ratio over producing nodes is blind to sparsity by construction, and on the contrast metric itself the demand side is the wider one

**Status:** CONFIRMED
**Method:** Checked the blindness claim as an argument; re-measured both contrast ranges over the 29
live goods (`m2.py`).
**Evidence (the argument):** A max/min ratio is taken over the set where `s > 0`, so a good produced
in 1 node and a good produced in 18 can both yield the same ratio; the *size* of that set — which is
what sparsity is — is not an input to the statistic at all. `cloves` makes it concrete: one producer,
so no ratio exists (Y177). The blindness is by construction, as claimed.
**Evidence (the measurement):** supply contrast **4 to 97** over the 28 goods with more than one
producer; demand contrast **211 to 15,010** over all 29. The demand side is wider by roughly two
orders of magnitude, so the claim's direction is right. `spices` is produced in **18 of 80** nodes and
`cloves` in exactly **1**, both as §3.2 states.

### Y145 — better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of placement; the ×1.720 figure is no longer given

**Status:** CONFIRMED
**Method:** This is a claim about the **v1 Laplacian** operator, which is what §3.2 is diagnosing, so
it was measured on that operator: `orient(solve_phi(s_uniform_eps − c))` for `spices` at demand
exponent 1.5, bisecting the multiplier on the `genua` node's province wealth (`m5.py`).
**Evidence:** LAP baseline spices sinks `['saxony']` — Genoa is not a sink, which is the diagnosis.
Bisection gives the co-sink threshold at **×1.724**, and just above it the sink set is
`['genua', 'saxony']` — a *co*-sink, not a sole sink, exactly as the claim says. So "roughly ×1.7" is
right and "co-sink" is right. The precise 1.720 is not printed anywhere in the v6.0 spec.
Independently, `scripts/verify.py:124` carries the same bisection with an expected value of 1.725,
which agrees with my 1.724 to the tolerance it uses.

### Y146 — moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of 3.6–4.9×: beijing 3.61×, hangzhou 4.12×, xian 4.60×, canton 4.77×

**Status:** PARTIAL
**Method:** Measured the same relocation two ways on the v1 Laplacian: (a) multiplying the node's
**demand share** `c[node]` and renormalising, and (b) multiplying the node's **province wealth** and
recomputing `c` at exponent 1.5 (`m5.py`, `m6.py`).
**Evidence:** Under (b) — the wealth multiple — the thresholds are **3.626, 4.125, 4.606, 4.775** for
`beijing`, `hangzhou`, `xian`, `canton`. Those are the document's 3.61, 4.12, 4.60, 4.77 to two
decimals. Under (a) — the demand multiple, which is what the sentence says — the thresholds are
**6.906, 8.379, 9.884, 10.435**, i.e. **6.9× to 10.4×**, not 3.6–4.9×. The relation is
`demand multiple = wealth multiple^1.5` (3.61^1.5 = 6.86, 4.12^1.5 = 8.36, 4.60^1.5 = 9.86,
4.77^1.5 = 10.42), which is `α(spices) = 1.5` acting on the scaled wealth — so the two are not
interchangeable and the figures belong to the wealth reading.
Corroboration that the underlying experiment is the wealth one: the world-demand shares the four
nodes then hold — **9.5%, 21.4%, 12.3%, 17.6%** — match v5.0's paired percentages (9.3%, 21.4%,
12.3%) almost exactly, and those were quoted beside the same four multiples.
**Should say:** "takes a multiple of that node's **development** in the region of 3.6–4.9× — which is
a 6.9–10.4× multiple of its demand, since α(spices) = 1.5."

### Y147 — the multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started; other nodes in the region need more still

**Status:** PARTIAL
**Method:** Extended the Y146 measurement to the four further nodes the withdrawn figures named
(`m5.py`, `m6.py`).
**Evidence (the derivation — confirmed):** The multiples rise `beijing` 3.63 → `hangzhou` 4.13 →
`xian` 4.61 → `canton` 4.78 while the shares bought run 9.5% → 21.4% → 12.3% → 17.6% — non-monotone,
so the two orderings genuinely do not line up. And the reason given is the right one: the starting
shares are 1.5%, 3.2%, 1.4%, 2.0%, so equal multiples buy unequal shares.
**Evidence (the "more still" clause — false for one node):** wealth multiples for the four further
nodes are `girin` **3.888**, `yumen` **4.493**, `chengdu` **8.088**, `lhasa` **10.670** — a range of
about 3.9× to 10.7×, matching the withdrawn "4.0–10.8×". But `girin` at 3.89× needs **less** than
`hangzhou` (4.13), `xian` (4.61) and `canton` (4.78), so "other nodes in the region need more still"
is not true of all of them.
**Should say:** "and other nodes in the region range from about the same multiple up to two and a
half times it."

---

## §3.4 — Why supply is pre-modifier

### Y148 — in v1, substituting production income broke the α = 1 identity, measured as orientation agreement collapsing to well under half the map; the 159/159 → 68/159 figures are no longer given

**Status:** CONFIRMED
**Method:** Located the original measurement and v2's grading of it; grepped the v6.0 spec.
**Evidence:** `v1-laplacian/validation.md:4517` (claim C424) records "**Orientation agreement
collapses from 159/159 to 68/159**" with a relative residual of 1.512e+00 against 1.959e-15.
`v2-drain/validation-v2.md:480–489` grades V138 CONFIRMED on a re-run and adds the necessary scoping —
the substitution must model the owner factors `(1 + production_efficiency) × (1 − autonomy)`, since
raw production income is identical to trade value in the proxy dataset and substituting *that*
changes nothing (159/159, checked). 68/159 = **42.8%**, which is well under half ✓. And `68/159` and
`68 of 159` appear **0 times** in the v6.0 spec, so the figures are genuinely dropped while the
directional claim they supported is retained at the strength the evidence carries.

---

## §3.5 — Why α is anchored absolutely

### Y149 — ⚑ change_price values are fractions of the good's base price, not ducats, and the shipped save tutorial/eu4_tutorial_chapter10.eu4 settles it: paper at current_price=4.375 on a base of 3.5, gems at 5.000 on a base of 4.0

**Status:** CONFIRMED
**Method:** Read the shipped save (plain text, magic `EU4txt`, 30,421,736 bytes — not a ZIP); located
its price list; read both goods' base prices from `common/prices/00_prices.txt`; enumerated every
install `change_price` block touching the two goods.
**Evidence:** The save's price block gives
`paper = { current_price = 4.375  change_price = { key="PAPER_IN_BUREAUCRACY"  value=0.250 } }` and
`gems = { current_price = 5.000  change_price = { key="FACETING"  value=0.250 } }`. Base prices 3.5
and 4.0. Multiplicative: 3.5 × 1.25 = **4.375** ✓ and 4.0 × 1.25 = **5.000** ✓. Additive: 3.75 and
4.25 ✗. Both keys resolve to real executable install blocks
(`events/PriceChanges.txt:2009` and `:2247`). Two independent goods, both decisive.
Recorded: the tutorial save is from 1.29.99 "Emperor", not 1.37 — its list omits `cloves` and
includes `nogoods` — so it settles the *units* rather than any 1.37 magnitude, which is all the claim
uses it for.

### Y150 — the install carries 161 textual change_price blocks — 93 in events/, 14 in missions/, 1 in common/, 53 in history/ of which 13 are negative (all in history/countries/HAB - Austria.txt), and none in decisions/

**Status:** CONFIRMED
**Method:** Regex census (`change_price\s*=\s*\{`) over `.txt` files in each of the five trees with
`#`-to-EOL comments stripped, run twice — once with a naive strip and once quote-aware, with identical
results — plus a whole-install completeness check.
**Evidence:** `events/` **93**, `decisions/` **0**, `missions/` **14**, `common/` **1**,
`history/` **53**, total **161**. `decisions/` genuinely has zero across its 196 `.txt` files rather
than being an empty tree. Of the 53 history blocks, **13** carry a negative `value`, and all 53 —
hence trivially all 13 — are in `history/countries/HAB - Austria.txt`. The 13: fish −0.1, wool −0.10,
wool −0.25, incense −0.25, fish −0.1, grain −0.20, copper −0.35, coffee −0.4, spices −0.4, paper
−0.5, chinaware −0.5, gems −0.5, slaves −0.4. `grep -rl change_price` over the whole install returns
nothing outside these five trees except `eu4.exe`, a patchnotes file and the tutorial saves, so 161
is the complete script census.

### Y151 — ⚑ ten of the 161 never execute: four inside effect_tooltip = "…" strings, three inside the effect = "…" string of a country_event_with_effect_insight, and three inside tooltip = { } display wrappers, so 151 are executable

**Status:** CONFIRMED
**Method:** Character-level lexer with real multi-line-string handling, reporting each block's
enclosing wrapper path; reconciled against the 161 total with zero brace imbalance.
**Evidence:** **10** non-executing, exactly as partitioned. (a) four in `effect_tooltip = "…"` —
`missions/DOM_Britain_Missions.txt:919` (fur), `missions/KoK_Persia_Missions.txt:3384` (silk),
`:3390` (dyes), `:3396` (cloth), all inside `country_event_with_insight`. (b) three in the
`effect = "…"` string of a `country_event_with_effect_insight` —
`missions/KoK_Byzantine_Missions.txt:2070` (silk), `missions/KoK_Yemen_Missions.txt:954` (coffee),
`missions/WOC_Italian_Missions.txt:2841` (wine). (c) three in `tooltip = { }` —
`events/flavorMAL.txt:1736` (ivory), `missions/WOC_Hisn_Kayfa_Missions.txt:1448` and `:1459` (grain).
161 − 10 = **151**. Class (c) is corroborated as display-only by construction:
`WOC_Hisn_Kayfa_Missions.txt` pairs its two `tooltip{}` copies with a byte-identical block inside a
`hidden_effect = { if = { … } }` at line 1493 — the standard EU4 pairing — and `flavorMAL.txt`'s
carries the source comment `#Info for other players that Ivory has increased price`. A full
enclosing-path census over all 161 finds no other display-only wrapper.

### Y152 — six of the seven quoted blocks duplicate a block already counted in events/, and the seventh names a price key no event in the install ever sets

**Status:** CONFIRMED
**Method:** For each of the seven quoted-string blocks, searched `events/` for an executable block
with the same `trade_goods`, `key` and `value`, and checked whether the match sits inside the very
event the wrapper fires.
**Evidence:** Six match on all three fields *and* on duration, and each match is the body of the
event its wrapper announces — silk/`BYZ_growing_demand`/0.2 at `events/flavorBYZ.txt:1921` inside
`MEE_Byzantine_Events.26`; silk/dyes/cloth `PERSIAN_*` at `events/FlavorPER.txt:1463`, `:1469`,
`:1475` inside `flavor_per.24`; coffee/`YEM_coffee_price_boost`/0.25 at `events/flavorYEM.txt:89`
inside `flavor_YEM.3`; wine/`ITA_wine_upgrade`/0.4 at `events/flavorITA.txt:448` inside
`flavor_ita.9`. The seventh, `missions/DOM_Britain_Missions.txt:919`, uses the key
**`ENGLISH_FUR_TRADE`**, and `grep -rn ENGLISH_FUR_TRADE` over the whole install returns only four
localisation entries and the tooltip itself — no executable block anywhere sets it. (The event its
wrapper fires, `flavor_gbr.7` at `events/FlavorGBR.txt:466`, does apply fur +0.25, but under the
different key `FUR_TRADE`, and `change_price` entries are keyed.) Six and one, exactly as claimed.

### Y153 — all ten are positive and every negative block in the install is executable, so the 13/2/4/11 partition is identical under either census

**Status:** CONFIRMED
**Method:** Read the ten values; enumerated every negative block and its wrapper path; computed the
price-floor partition twice, once over executable blocks only and once over all 161.
**Evidence:** the ten values are 0.33, 0.25, 0.2, 0.25, 0.5, 0.35, 0.25, 0.1, 0.1, 0.4 — all strictly
positive. There are **40** negative blocks in the install (27 in `events/` — `PriceChanges.txt` 22,
`FlavorPER.txt` 3, `FlavorSWE.txt` 2 — and 13 in `history/`), and **none** sits in a `tooltip{}` or a
quoted string, so all 40 are executable. Since a floor depends only on the most negative value per
good, the two censuses cannot differ, and they do not: **(13, 2, 4, 11)** under both. This is a
genuine derivation and the numerical check confirms it rather than substituting for it.

### Y154 — v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one

**Status:** CONFIRMED
**Method:** Read both versions' sentences; established the executable count independently.
**Evidence:** `v4:949–950` reads "(All **154** `change_price` blocks were parsed — 93 in `events/`,
**7** in `missions/`, 1 in `common/` and 53 in `history/`…)"; `v5:1073–1074` reads the same sentence
with **161** and **14**. The missions figure is the whole difference: 14 textual against 7 visible to
a parse-tree walker, and the seven invisible ones are exactly the quoted-string blocks (Y156). The
executable count is **151** (Y151), which is neither 154 nor 161 — so both were wrong about which
number is the executable one, exactly as the claim says.

### Y155 — v5.0 also claimed the scan was "guarded by a per-file count assertion" — there was no assertion anywhere in its toolchain; verify6.py now carries the guard

**Status:** PARTIAL
**Method:** Read v5.0's sentence; searched every `.py` in `v5-owner-agnostic/scripts/` for an
assertion on the `change_price` scan; then read what `verify6.py` and `measure6.py` actually do.
**Evidence (the v5.0 half — confirmed):** `v5:1075–1076` reads "…so the scan is now guarded by a
per-file count assertion." Across all 62 files in `v5-owner-agnostic/scripts/` there are **six**
`assert` statements and **none** concerns `change_price` — they are two markdown-anchor checks in
`patch_lib.py`, three in `stats5.py`, and `assert res.success` in `toys.py`. The nearest thing is a
per-*tree* regex count compared by a print-based `chk()` at `validate_v5.py:238–241`, sitting directly
above `except Exception: pass`, and that census is never compared against the `pdx` walk's 154 hits.
The phrase "per-file count assertion" appears in `scripts/` exactly once — in `q04.py:26`, the edit
script that inserted the sentence into the spec.
**Evidence (the "verify6.py now carries the guard" half — not as described):** `verify6.py`'s three
`change_price` touchpoints are `present(doc, "change_price census", "161 (events 93, missions 14,
common 1, history 53, decisions 0)")` at line 107 — a substring test against a **constant**, and on
the checklist path only, not the spec path; `present(doc, "price partition", "13-2-4-11")` at 109,
likewise constant; and `shows(doc, "spec: change_price by tree", "{} in `events/`", 93)` at 168, whose
93 is a **typed literal** even though `measure6.OUT["change_price by tree"]` holds the computed
value. Only the total, 161, is anchored on a computed figure (line 150–151). None of these is a
per-file count assertion, and none would fail if a per-file loss recurred. Worse, `measure6.py:227`
still wraps its parse-tree walk in `try: walk(pdx.load(fp), tree)  except Exception: pass` — the same
bare `except` v5.0's sentence was written to answer.
**Should say:** "`verify6.py` now checks the census total against a computed value, and the per-tree
figures against typed literals; a per-file assertion on the scan itself still does not exist, and
`measure6.py`'s walker still swallows parse failures."

### Y156 — the reason a plain parse misses these is mechanical: pdx.py tokenises a quoted string as one opaque unit, so a change_price inside a tooltip string is invisible to the walker

**Status:** CONFIRMED
**Method:** Read `scripts/pdx.py`; demonstrated the tokenisation; then counted `change_price` nodes
visible to a parse-tree walk over all five trees.
**Evidence:** `pdx.py:9` is `TOK = re.compile(r'"[^"]*"|[{}=]|[^\s{}=]+')`. The first alternative
matches a whole double-quoted run, and because `[^"]` includes newlines it spans them, so a
multi-line `effect_tooltip = "…"` body becomes a single token; `parse()` then stores it as a leaf
**string** (`node.append((key, toks[pos].strip('"')))`), never a `Node`. Demonstrated directly: the
tokens of a sample `effect_tooltip` are `'effect_tooltip'`, `'='`, and one token containing the whole
body including `change_price = { … }`.
Walking every `.txt` in the five trees with `pdx.load` and counting `k == "change_price"` nodes gives
`{events: 93, decisions: 0, missions: 7, common: 1, history: 53}` = **154 visible against 161
textual** — exactly the seven quoted blocks invisible, and the six files carrying them show
`visible=0` (`DOM_Britain`, `KoK_Persia`, `KoK_Byzantine`, `KoK_Yemen`, `WOC_Italian`) while
`WOC_Hisn_Kayfa` shows 3, its `tooltip{}` blocks being visible. The mechanism is exactly as stated,
and it also explains v4.0's 154 (Y154).

---

## §3.9 — Why Φ_w is the installed graph

### Y157 — genua, gulf_of_siam and sevilla rank 4th, 3rd and 7th by node wealth on the corrected field (mexico is 2nd) — 296.0, 297.9 and 266.5 against english_channel's 316.6, which is a sink

**Status:** CONFIRMED
**Method:** Recomputed node wealth and its rank vector over all 80 nodes (`m2.py`).
**Evidence:** `genua` **296.0** rank **4**; `gulf_of_siam` **297.9** rank **3**; `sevilla` **266.5**
rank **7**; `mexico` 300.4 rank **2**; `english_channel` **316.6** rank **1**, and it is a sink
(out-degree 0). Every figure and every rank exact. The argument they support — that a rich non-sink
node draws more edges in than it sends out — holds for all three: `genua` in-degree 3 / out-degree 2,
and none of the three is a sink.

### Y158 — Φ_ord scores higher than Φ_w on self-coherence, and was superseded on design grounds: its ends are scheduling artifacts rather than places, a majority terminate no good at all, none of the demand capitals is among them, and the end count does not concentrate as demand concentrates; no figure is maintained for it

**Status:** PARTIAL
**Method:** Rebuilt `Φ_ord = Σ_g V_g·order_g` from the same 29 DRAIN runs and measured each of the
four clauses on the v6.0 field (`m7.py`, `m9.py`), cross-checked against `drainrep.py`.
**Evidence (three clauses confirmed):** self-coherence **60.4%** edge-goods against `Φ_w`'s 53.6% —
higher ✓, and `drainrep.py` independently reports 2783/4611 = 60.4%. The demand capitals — the top
three nodes by `c_w`, `genua`, `english_channel`, `hangzhou` — are **none of them** among `Φ_ord`'s
ends ✓. And the end count **does not** concentrate: sweeping cloves-α over {2, 4, 8, 16, 32, 64}
leaves it at **14 at every value** ✓. No figure is maintained (Y089).
**Evidence (the majority clause — false):** `Φ_ord` has **14** end nodes at 1444 —
`amazonas_node`, `rio_grande`, `james_bay`, `chengdu`, `philippines`, `australia`, `yumen`, `katsina`,
`basra`, `laplata`, `ragusa`, `safi`, `rheinland`, `white_sea` — of which **7** terminate no good at
all: `amazonas_node`, `rio_grande`, `james_bay`, `chengdu`, `yumen`, `basra`, `ragusa`. That is
**exactly half**, not a majority. (v5.0's "8 of 13" *was* a majority; the wealth-field change moved
both numbers and the quantifier did not follow.)
**Should say:** "half of them terminate no good at all".

### Y159 — v2.1 through v4.0 justified the adoption by "two vanilla-like ends at 1444"; that is not the argument and should not be revived even though the 1444 field again gives two ends, because the count is a property of the field, not of the operator

**Status:** CONFIRMED
**Method:** Grepped the three versions for the calibration wording; checked the count's dependence on
the field and on the operator.
**Evidence:** The two-sink calibration is verbatim in v2, v3.0 and v4.0 (Y072). The 1444 field does
again give two ends (Y075/Y137), so the warning is needed rather than hypothetical. And the count is
demonstrably a property of the field rather than of the operator: on the same operator it is 2, 3, 4,
2, 1 across European development factors and 6, 2, 1, 2, 3, 1 across α_Φ (Y069) — while the *other*
aggregate tested on the same field, `Φ_ord`, gives 14 ends (Y158), so neither operator has a
characteristic count. The reasoning is sound in both directions.

### Y160 — what the trade costs is self-coherence with the per-good graphs; what it buys is one operator, one set of guarantees, and ends that sit where the wealth is; the "7.8 points" figure is withdrawn

**Status:** CONFIRMED
**Method:** Verified the cost is real, checked each purchase against the document's own guarantees,
and grepped for the withdrawn figure.
**Evidence:** The cost is real and measured: 53.6% against 60.4% (Y089/Y158). The purchases are
verifiable: `Φ_w` is `run_drain` applied to `b_w`, the same function the per-good graphs use, so LP
feasibility, acyclicity, determinism and scan-invariance transfer verbatim — one operator, one set of
guarantees ✓; and its ends sit at `c_w` ranks 2 and 3 with node-wealth ranks 1 and 12 (Y075), which is
where the wealth is, against `Φ_ord`'s ends, none of which is a demand capital (Y158) ✓. `7.8 point`
appears **0 times** in the v6.0 spec. Stating the trade as a direction rather than a maintained gap is
consistent with §0's convention and loses nothing the argument needs.

---

## §3.10 — Why the engine's economy is overwritten

### Y161 — across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam on each node's real 1444 country table, the two income forms agree to a worst relative disagreement of 0 to 3.7e-16 — one to three units in the last place, not "at most one"

**Status:** CONFIRMED
**Method:** Parsed each of the five nodes' country tables out of the save's `trade={}` structure,
formed `powershare_C` from the `val` field, built a per-good `collected_share(n,g)` that is 1 at a
sink for `g` and a genuine per-good ratio otherwise, and compared `Σ_g v_g·cs_g·ps_C` against
`ps_C·Σ_g v_g·cs_g` for every collector (`m6.py`).
**Evidence:** worst relative disagreement per node — `sevilla` (6 collectors) **3.41e-16** = 1.54 ULP;
`genua` (13) 2.67e-16 = 1.20 ULP; `champagne` (22) 2.10e-16 = 0.94 ULP; `malacca` (25) 2.99e-16 =
1.35 ULP; `gulf_of_siam` (19) 2.06e-16 = 0.93 ULP. Worst over the five: **3.41e-16**, against the
document's 3.7e-16. One ULP of a double is 2.22e-16 and three is 6.66e-16, so "one to three units in
the last place" is the right characterisation and "at most one" would have been wrong — which is the
correction the claim makes. Recorded: the exact worst value depends on the `collected_share`
construction, which the spec does not pin, so 3.7e-16 is not a reproducible constant; the ULP
statement is what is reproducible, and it reproduces.

### Y162 — reading the one installed graph leaves the propagated term good-independent, so the identity holds by construction, and in doubles to within one to three units in the last place

**Status:** CONFIRMED
**Method:** Checked as a derivation, then numerically as Y161.
**Evidence:** With one graph, a node's downstream neighbour set is a single set, so §1.9's propagated
contribution to a country's power at that node carries no `g`. Every other term feeding collector
power — the merchant bonus, the off-home penalty, the caravan grant — is node-wide by §1.7/§1.8. So
`powershare_C(n)` has no `g` argument and factors out of `Σ_g`, making
`income_C(n) = powershare_C(n)·collect_pool(n)` an algebraic identity rather than an approximation.
The doubles check is Y161: 0.93 to 1.54 ULP over five real country tables.

### Y163 — gulf_of_siam's 29 goods leave it by seven distinct downstream sets

**Status:** CONFIRMED
**Method:** Collected `{v : (gulf_of_siam, v) ∈ directed_g}` for each of the 29 live goods and counted
distinct sets (`m2.py`).
**Evidence:** **7** distinct downstream sets. This is the concrete counterexample the paragraph needs:
per-good propagation would make the node's downstream neighbourhood good-dependent seven ways over,
so a country's propagated power there would differ by good.

### Y164 — per-good propagation does not break the identity: ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g, and collect_pool · ps̄_C = income_C follows algebraically, with Σ_C ps̄_C = 1

**Status:** CONFIRMED
**Method:** Checked the algebra, then verified it numerically on two real country tables with
genuinely per-good share vectors (`m6.py`).
**Evidence (the algebra):** with `collect_pool = Σ_g v_g·cs_g` — which is exactly what §2.6's table
writes — substituting the definition gives
`collect_pool · ps̄_C = Σ_g v_g·cs_g · (Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g) = Σ_g v_g·cs_g·ps_C(g)
= income_C`. And `Σ_C ps̄_C = Σ_g v_g·cs_g·(Σ_C ps_C(g)) / Σ_g v_g·cs_g = 1` whenever the per-good
shares sum to 1 across collectors, which they do by construction. Both steps are exact.
**Evidence (numerically):** with a distinct random per-good share vector for every good,
`pool·ps̄_C` reproduces `income_C` to a maximum relative error of **1.11e-16** at `gulf_of_siam` and
**0** at `sevilla`, and `Σ_C ps̄_C = 1.0` exactly at both. The identity holds under per-good
propagation, as claimed.

### Y165 — both inputs to ps̄_C already exist per good at write time, and §2.6 sums exactly them into collect_pool

**Status:** CONFIRMED
**Method:** Read §2.6's written-fields table against the definition of `ps̄_C`.
**Evidence:** §2.6 writes "Node collectible pool = `Σ_g value_g(n) · collected_share(n,g)`" — which is
`Σ_g v_g·cs_g`, the denominator of `ps̄_C`, term for term. And `v_g` and `cs_g` are per-good
quantities the solver has already computed by then (`value_g(n)` from item 4 and
`collected_share(n,g)` from §1.8), while `ps_C(g)` is the per-good power share the per-good
propagation variant would be computing anyway. So the numerator's inputs exist at write time too.
Both halves hold.

### Y166 — the real cost is that ps̄_C is not derivable from trade power alone: it is value-weighted, so installing it means writing a country a fictitious per-node trade power whose ratio happens to equal it, and every other consumer of that power field then reads the fiction

**Status:** CONFIRMED
**Method:** Checked as an argument.
**Evidence:** `ps̄_C` weights `ps_C(g)` by `v_g·cs_g` — collected value, not power — so two countries
with identical power in a node have different `ps̄_C` if their per-good shares differ across goods
carrying different value. Therefore no function of trade power alone equals it. The engine's data
model exposes a per-node, per-country *power* number and derives the collector split from it, so the
only way to install `ps̄_C` is to write a power whose ratio equals it. The consequence is real: §1.10
lists five threshold mechanics that read exactly that power field (trade-conflict casus belli target
and actor, privateer blocking, trade-company extra merchant, trade-company control), so all five would
read the fiction. The argument is valid and its consequence is concretely instantiated in the
document's own inventory.

### Y167 — that is a claim about what the engine exposes, not about a magnitude, and no figure of the document's own is quoted, because the identity holds and the objection is structural

**Status:** CONFIRMED
**Method:** Read the passage; checked which figures §3.10 prints and which are attributed to prior
versions.
**Evidence:** The structural claim is Y166, which is sound. And the scope of "no figure of my own"
is the *discrepancy magnitude*, which is right: the only magnitudes in that parenthetical are
attributed — v1–v4.0's 5.96, v4.0's 0.41%, v5.0's "single-digit percent", v6.0's first draft's "at
most 0.1%" — and none is asserted. Worth stating so the sentence is not over-read: §3.10 does print
figures of its own elsewhere (the 0–3.7e-16 residual and the seven downstream sets), so the claim is
about the discrepancy magnitude, not about the section.

### Y168 — every magnitude previous versions quoted was an artifact of substituting some other weighting: v1–v4.0's "5.96 ducats on a node paying ~250", v4.0's 0.41%, v5.0's "redistributive and single-digit percent", and v6.0's first draft's "at most 0.1%"

**Status:** PARTIAL
**Method:** Counted each figure's occurrences in every version's spec; located v6.0's first-draft
figure; checked v4.0's harness.
**Evidence (three of four attributions confirmed):** `0.41%` is v4.0's — `v4:1076`, "the node-scalar
model then overstates **every** collector's income by 0.41%" — and appears in no earlier spec.
`redistributive` is v5.0's — `v5:1210` — and appears in no earlier spec. "at most 0.1%" is v6.0's
first draft — `changes-v6.md:1088` and `:2587`, `fixes-agreed.md:142` — withdrawn in
`fixes-round2.md:53–54`. And the diagnosis is right in each case: each froze or reweighted the share
differently, so each measured its own construction, which is exactly why Y164's identity holds and
none of them should have been non-zero.
**Evidence (the first attribution — off by a version):** `5.96` appears in `v1:440`, `v2:708` and
`v3:986` and **0 times in v4.0's spec**. v4.0 removed it deliberately, and its own harness asserts the
removal: `v4-owner-agnostic/scripts/validate_v4.py:452` carries
`hasnt("3.10", "the 5.96-ducat figure", "off by 5.96 ducats on a node paying ~250")`, which **passes**
on re-run. v5.0 made the same one-version error first (`v5:1210`) and v6.0 inherited it.
**Should say:** "v1 through v3.0's '5.96 ducats on a node paying ~250'".

### Y169 — no node in the model has local trade value near 250; the "largest is 112.6" figure is no longer maintained

**Status:** CONFIRMED
**Method:** Summed per-node local trade value over `ROWS` and took the maximum; grepped the v6.0 spec.
**Evidence:** maximum node local trade value **112.6** at `english_channel` (the maximum node *total*
wealth is 316.6 at the same node), so nothing is near 250 — the largest is under half of it. `112.6`
appears **0 times** in the v6.0 spec, so the figure is genuinely not maintained. Recorded: v5.0's
withdrawn "the largest is 112.6" was itself **correct**, so this withdrawal is a convention choice
under §0's rule rather than a correction of an error.

---

## §3.13 — Open questions

### Y170 — the one open wealth question is now a design question, not a classification one: should any source beyond province condition be allowed to multiply goods_produced?

**Status:** CONFIRMED
**Method:** Checked the stipulation against §1.3's input surface.
**Evidence:** §1.3 reads development, the good and the four province-state modifiers and nothing else
(Y024), so there is no remaining question of the form "is this modifier local, and does it enter
wealth" — the classifier is gone (Y003). What is left is whether to *admit* a further source, which is
a decision rather than a determination. The re-typing from classification to design is correct, and
§3.13 carries no value for it, as the claim says.

### Y171 — trade_goods_size and trade_goods_size_modifier are granted in buildings, event modifiers, great projects, static and province-triggered modifiers, holy orders, state edicts and trade-company investments

**Status:** CONFIRMED
**Method:** Grepped each named directory under `common/` for the two keys.
**Evidence:** all eight classes carry at least one grant — `buildings/` 2 files
(`00_buildings.txt`, `01_nativebuildings.txt`), `event_modifiers/` 3 files, `great_projects/` 1,
`static_modifiers/` 1, `province_triggered_modifiers/` 1 (`00_modifiers.txt`), `holy_orders/` 1
(`00_holy_orders.txt`), `state_edicts/` 2 (`zzz_chinese_industrialization.txt`,
`zzz_urbanization.txt`), `tradecompany_investments/` 1 (`00_Investments.txt`, 2 occurrences). The
enumeration is complete for the classes it names; further classes also grant the keys
(`imperial_reforms/`, `religions/`, `ideas/`, `policies/`, `estate_privileges/`), which strengthens
rather than weakens the point the sentence makes about the maintenance surface.

### Y172 — v3.0 through v5.0 tried to admit the province-scoped subset by rule; that rule was wrong in both independent audits that examined it, which is why v6.0 drops it

**Status:** CONFIRMED
**Method:** Read each version's rule and the graded verdicts against it.
**Evidence:** All three versions did carry a rule for admitting a province-scoped subset — v3.0's
structural rule (`v3:160–164`) and v4.0's/v5.0's two-test classifier (`v4:184`) — so unlike Y027 this
sentence does not attribute the *same* rule to all three. And both audits that examined it found it
wrong: `validation-v3.md` W041 REFUTED (the enumeration) with W040 PARTIAL (the rule stated as if it
were general), and `validation-v5.md` X035 REFUTED ("the enumeration is incomplete and miscounts") with
X030 PARTIAL (the locality test's own attribute list does not cover the four province-state
modifiers it then admits). Two independent audits, both adverse.

### Y173 — re-admitting any of those sources re-admits the maintenance burden with it, so the question to settle first is whether the fidelity is worth it — the whole set was worth 105.30 ducats, about one percent of world wealth either way the ratio is taken

**Status:** CONFIRMED
**Method:** Checked the figure (Y004) and the "either way" arithmetic.
**Evidence:** 105.30 ducats; 105.30/10,712.70 = 0.983% and 105.30/10,607.40 = 0.993% — both round to
about one percent, so "either way the ratio is taken" is right and the framing does not depend on the
choice of denominator. The maintenance-burden inference is supported by Y171's eight source classes
and by the audit history in Y172: the surface is large and it failed twice.

### Y174 — under the calibration's α = 16 the cloves demand order is hangzhou, beijing, doab, and the sink lands on a high-demand node rather than a geographic accident

**Status:** CONFIRMED
**Method:** Built the cloves demand vector at α = 16 and read off its ranking; ran DRAIN on the
resulting balance (`m4.py`).
**Evidence:** demand order at α = 16, top six: **`hangzhou`, `beijing`, `doab`**, `canton`, `lahore`,
`genua` — the stated three, in the stated order. Sinks on that balance:
`['beijing', 'genua', 'gujarat', 'kongo', 'timbuktu']`, so demand rank 2 holds a sink — a
high-demand node, not a geographic accident. (This is the α-substitution alone; the §3.13 calibration
also moves ρ to 0.5 and adds a twig tolerance, which would narrow the set further. The claim's
content — the demand order and that the sink is demand-aligned — holds under the α substitution by
itself.) v5.0's "Deccan is demand rank 2 / Beijing rank 3" framing is indeed wrong on this field:
`beijing` is rank 2 and `doab` rank 3.

### Y175 — hangzhou, not Beijing, holds the richest single province; the 30.4-against-19.5 figures are no longer maintained

**Status:** CONFIRMED
**Method:** Maximum per-province wealth by node (`m2.py`); grepped the v6.0 spec.
**Evidence:** richest counted provinces: **1821 (hangzhou) 27.00**, 684 (hangzhou) 21.60,
**1816 (beijing) 19.50**, 685 (hangzhou) 19.20, 667 (canton) 18.00. So `hangzhou` holds the richest
and `beijing`'s best is 19.50. `30.4` appears **0 times** in the v6.0 spec, so the pair is genuinely
dropped — and it would now be wrong: the correct pair on this field is 27.00 against 19.50.

---

## §3.15 — Rejected

### Y176 — §3.15 does not maintain a copy of the supply/demand contrast measurement; §3.2 carries it, and the 4–97 against 211–20,400 figures are dropped from this entry

**Status:** PARTIAL
**Method:** Grepped the v6.0 spec for every rendering of the contrast figures; read both sections.
**Evidence (the de-figuring — confirmed):** `4–97`, `211`, `20,400` and `15,010` all appear **0
times** in the v6.0 spec, and §3.15's Laplacian entry now reads "the demand side is the wider of the
two, not the supply side — §3.2 carries the measurement, and this entry does not maintain a copy of
it."
**Evidence (the cross-reference — false):** §3.2 does **not** carry the measurement. Its text is
"On the contrast metric itself the demand side is the wider one, not the supply side" — a direction
with no numbers. So no section of v6.0 prints the contrast figures, and §3.15's pointer resolves to
nothing. (The figures are real and reproduce — supply 4–97 over 28 goods, demand 211–15,010, Y144 —
they are simply not in the document.)
**Should say:** "§3.2 carries the finding; neither section maintains a figure for it."

### Y177 — cloves has a single producer and so no contrast to measure at all, which is the sparsity point in miniature

**Status:** CONFIRMED
**Method:** Counted producing nodes per good on the v6.0 field (`m2.py`).
**Evidence:** `single-producer goods  ['cloves']` — exactly one good, and it is `cloves`; 28 of the 29
live goods have more than one producer. A max/min ratio over a single-element set is undefined, so
there is literally no contrast to measure, which is why the ratio metric cannot express what the
diagnosis needs. `spices` at 18 of 80 producing nodes is the same point less starkly.

### Y178 — v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio here while v4.0's own §3.2 was withdrawing it

**Status:** CONFIRMED
**Method:** Located the ratio in each version's §3.15 and §3.2.
**Evidence:** `v3:1109` and `v4:1200` both carry, in §3.15, "supply contrast (10⁷) drowns demand
contrast (10²–10³)". And `v4:837`, in §3.2, carries the withdrawal — "contrast 10⁷ against demand
contrast 10²–10³". That ratio was `max(s)` over the **ε floor** of v1's regularizer". So v4.0's §3.2
withdrew it while v4.0's §3.15 repeated it, exactly as claimed. The attribution is precise in a way
v5.0's was not: v5.0 wrote "v3.0 through v4.0 repeated it here while §3.2 was withdrawing it", but
v3.0's own §3.2 (`v3:754`) still *asserted* a version of the ratio ("supply contrast exceeds demand
contrast by four to five orders of magnitude"), so only v4.0 had the internal contradiction. v6.0's
narrower sentence is the correct one.

### Y179 — ranked orientation's win and loss are now stated as directions with no figures: it puts a far higher share of top-demand nodes in its sink sets than DRAIN does, strands a large share of world demand, leaves orphan sinks a good cannot reach, posts net-producer sinks where DRAIN, LAP and FLOW post none, and keeps several times DRAIN's sinks per good

**Status:** CONFIRMED
**Method:** Ran all four operators on the v6.0 field and measured each of the five clauses (`m7.py`).
**Evidence:**

| operator | mean demand reach | orphan sinks | net-producer sinks | sinks/good | sink rate, top-8 demand |
|---|---|---|---|---|---|
| DRAIN | 100.00% | 0/108 | **0** | 3.72 | 16.8% |
| LAP | 100.00% | 0/104 | **0** | 3.59 | 9.9% |
| RANK | **83.33%** | **32/387** | **8** | **13.34** | **49.1%** |
| FLOW | 100.00% | 0/933 | **0** | 32.17 | 31.5% |

Clause by clause: top-demand share **49.1% against DRAIN's 16.8%** — far higher ✓; world demand
stranded **16.67% against DRAIN's 0.00%** — a large share ✓; **32** orphan sinks of 387 against
DRAIN's 0 ✓; net-producer sinks **8** where DRAIN, LAP and FLOW each post **0** ✓; sinks per good
**13.34 against 3.72 = 3.59×** — several times ✓. All five directions hold, and no figure for any of
them appears in the v6.0 spec.

### Y180 — seeded basin growth leaves demand unserved at every tuning tried; the 88.4% best-tuning reach figure is dropped

**Status:** CONFIRMED
**Method:** Ran `basin.py`'s six phases over the 29 goods at seven tunings, taking each good's best
iterate and averaging the unserved fraction (`m7.py`).
**Evidence:** mean unserved demand — as-written **0.396**; sign-flipped **0.327**; γ = 1000 **0.217**;
γ = 1e6 **0.217**; K = 32, γ = 1000 **0.211**; λ = 0.1, R = 4 **0.227**; λ = 0.9, R = 1 **0.215**.
Every tuning leaves demand unserved, and the best reaches only about **78.9%** — so the direction
holds and, on this field, is worse than the 88.4% v5.0 quoted. `88.4` appears **0 times** in the v6.0
spec, so the figure is dropped, and dropping it is what lets the entry stay true across the wealth-field
change.

### Y181 — the 3-mass gravity kernel reproduces whatever end count it is seeded with while γ is small enough, and loses that property as γ approaches 1; no agreement percentages or end counts are maintained

**Status:** CONFIRMED
**Method:** Built `Φ(n) = max_m c_α(m)·γ^dist(n,m)` over the top-k pairwise-unconnected demanders for
k = 1…6, at seven γ values, orienting arrows toward higher `Φ` so the ends are the field's local
maxima (`m8.py`). Both orientation signs were tried; the downhill sign is a construction error and is
recorded below.
**Evidence:** end counts for seeds k = 1…6 —

| γ | k=1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 0.30 | 1 | 2 | 3 | 4 | 5 | 6 |
| 0.50 | 1 | 2 | 3 | 4 | 5 | 6 |
| 0.70 | 1 | 2 | 3 | 4 | 5 | 6 |
| 0.90 | 1 | 2 | 3 | 4 | 4 | 4 |
| 0.95 | 1 | 2 | 3 | 3 | 3 | 3 |
| 0.97 | 1 | 2 | 3 | 3 | 3 | 3 |
| 0.99 | 1 | 1 | 1 | 1 | 1 | 1 |

Exact seed reproduction at γ ≤ 0.70 for every k tested, degradation from γ = 0.90, and total collapse
to a single end at γ = 0.99. That is precisely "reproduces whatever count it is seeded with while γ is
small enough, and loses that property as γ approaches 1". At γ = 0.50 with k = 3 the ends are
`{english_channel, genua, hangzhou}`; at γ = 0.99 they are `{genua}`. No agreement percentage or end
count for this kernel appears in the v6.0 spec (`61%`, `97 of 159`, `110 of 159` → 0 hits each).
*Instrument note:* orienting arrows downhill instead — sinks at local minima — reports 28, 20, 18, 17,
16, 16 and never reproduces the seed count. The sign matters and only one of the two is the kernel the
entry describes.

### Y182 — pinned-count wealth fields are rejected on three grounds, none of which is numeric

**Status:** CONFIRMED
**Method:** Read the three grounds; checked each for a numeric dependency.
**Evidence:** The three as written are (1) the end count is pinned by fiat, so a world conquest could
never merge the world into one basin; (2) a second operator with its own reach knob γ is needed; and
(3) a pure `wealth^α` comparison with no reach term does not concentrate ends, because a local wealth
maximum survives every positive α. None carries a figure. (1) and (2) are structural. (3) is an
empirical statement but a qualitative one, and it is true for the reason given: `orient(wealth^α)`
compares endpoints, and `x ↦ x^α` is strictly increasing for every α > 0, so it preserves the
endpoint ordering and hence the entire orientation — every local maximum is an end at every positive α,
independent of α's value. So (3) needs no measurement either, and the withdrawn "≥10 ends at α up to
16" was decoration on a monotonicity argument. The claim is right, and the third ground is stronger
than the deleted figure suggested.

---

## §3.16 — Evidence standard

### Y183 — failure mechanism 3: implemented as written, the α = 1 identity's residual reached 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a solver bug

**Status:** CONFIRMED
**Method:** Reproduced the instantiation — ε applied to the per-good supply only and not to `φ₀`'s —
and measured the residual against the exact case; grepped v1–v5 for the comparison (`m4.py`).
**Evidence:** with ε = 1e-6 on `s` alone, `max |Φ − V_tot·φ₀| = 1.79e-4` absolute, which is
**1.24e-5** relative to `max |Φ|` — an order-of-magnitude 1e-5 residual, as stated. With ε = 0 the
same construction gives **6.57e-14**, i.e. the identity is exact up to accumulation, so the 1e-5 is
entirely the mis-applied regulariser. v1's ε is 1e-6 (`v1:46`, `s ← (1 − ε)·s + ε/N   ε ≈ 10⁻⁶`;
`flowop.py:EPS = 1e-6`), so the residual is ten times the perturbation that caused it — which is why
it would read as a solver bug rather than as a modelling artifact. The parenthetical is also right:
the identical sentence in v2 (`:910`), v3.0 (`:1222`), v4.0 (`:1312`) and v5.0 (`:1456`) says only
"the identity failed at 1e-5", and no comparison to ε appears in any of them — `1e-6` occurs once
each in v3.0, v4.0 and v5.0 and in an unrelated context (support-membership flow), and not at all in
v1's or v2's spec.

---

## Notes outside the inventory

Three things this pass found that no `Y` row covers. They are recorded because a later extraction
should pick them up, not as verdicts.

1. **§3.3's node-size figure is wrong.** §3.3 says "Node sizes run from **19** land provinces
   (`cape_of_good_hope`) to 77 (`girin`)". `cape_of_good_hope` has **20** members — verified twice,
   from `nodes.json` and directly from `common/tradenodes/00_tradenodes.txt` — and 20 is a three-way
   tie with `patagonia` and `chengdu`. `girin`'s 77 is right but ties with `mexico`. The derived
   ratios survive: `(77/20)^0.5 = 1.96`, still "≈ 2×". The claim is carried UNCHANGED from v3.0 and
   so has no Y ID.
2. **`changes-v6.md`'s harness figures are stale.** It reports "On v6.0: **22 checks**, 0 failed";
   `verify6.py` on the shipped spec now runs **29**. It also says "every needle now reads a computed
   figure rather than a typed literal", which is not true of three spec-path needles (Y012).
3. **The 580/580 and arc-permutation experiments live in no shipped script.** §2.4 attributes them to
   `measure6.py` and `validation-v5.md`; neither contains them (Y129). `scripts/preconfirm3.py`
   carries the `Φ_w` relabelling study only. If §2.4's figures are to stay, the experiment that
   produced them should ship with them.
