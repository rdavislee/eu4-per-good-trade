# Claim Validation — Per-Good Trade Network Spec v5.0

Every claim in `claims-v5.md`, **X001–X196**, checked against the EU4 1.37.5.0 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (Leviathan present), the
vanilla 1444.11.11 save `VANILLA_start.eu4`, the reference solver in `scripts/`, and the spec text.
Nothing here is inherited from `validation-v2.md`, `validation-v3.md` or `validation-v4.md`; every
prior verdict was re-derived.

**Rules used.** ENGINE claims are settled from the shipped files wherever the files answer them,
reading the file rather than the spec's quotation of it; where only a running game could answer
(tooltip readings), the claim is graded on the evidence that exists and said to be unverifiable
rather than given a verdict. MODEL claims are split: derivations are attacked as arguments,
measurements are re-run. A proof that holds on the 1444 start but not in general is REFUTED, not
PARTIAL. DESIGN claims are checked for internal consistency and for whether the stated rationale
actually supports the choice — a choice justified by a false fact is REFUTED even where the choice
is defensible. No claim is CONFIRMED on plausibility, and none on a wiki.

Where a figure could be recomputed, it was recomputed from primary sources — a fresh parse of all
3,923 `history/provinces/` files and of the save's `gamestate`, not from the toolchain's
`prov1444.json` / `nodes.json` caches.

---

## Summary

| Status | Count | Share of 196 |
|---|---:|---:|
| CONFIRMED | **134** | 68% |
| REFUTED | **22** | 11% |
| PARTIAL | **39** | 20% |
| UNVERIFIABLE | **1** | 1% |
| **Total** | **196** | |

### Refutations

| ID | § | What is wrong |
|---|---|---|
| **X004** | §0 | "No figure in v5.0 is unverified" fails on its own terms — the document declines a number in three places, not one, and six of 1,503 lines carry a script attribution. |
| **X009** | §1.1 | The enumeration of reachable cases is incomplete and the aggregate case is misstated: the condition is on the *post-peel* balance, which Phase 0's fold can produce from a `b ≢ 0` input, and the aggregate case needs uniform `Σ wealth^α_Φ`, not uniform wealth. |
| **X021** | §1.3 | `Base: X (Yearly 12·X)` is arithmetically false on both of its own data points (12 × 0.49 = 5.88, not 6.00) and contradicts X120's truncation rule three claims later. |
| **X027** | §1.3 | 0.49 × 1.25 = 0.6125 truncates to 0.61, not the observed 0.62; the display is consistent only if the efficiency multiplies the *untruncated* base (0.625). |
| **X035** | §1.3 | The enumeration misses `provincial_production_size` and the two non-owner-gated `province_triggered_modifiers`, and counts five province-state static modifiers where there are four. |
| **X040** | §1.3 | `devastation` is **not** zero at 1444 — ten counted Bohemian provinces carry 20–50 — and three of the four modifiers enter `goods_produced` only, not `tax_value`. |
| **X050** | §1.3 | 88 of 138, not 85 of 130: 130 is the number of distinct start *provinces*, not of projects (eight provinces host two each). |
| **X058** | §1.3 | glass and chinaware are the whole of the tension only inside `common/tradegoods/`; at least seven further local-but-excluded cases sit elsewhere in the install. |
| **X065** | §1.6 | At fixed α_Φ = 1.5 the sink count takes the values 1, 2, 3, 4 and 5 across worlds — the count is not set by α_Φ, and X127 says so. |
| **X083** | §1.6 | Over α_Φ ∈ [1, 8] the widest band is [4.19, 6.73]; the stated rule selects ≈5.4, not 1.5, and the [1, 3] scan cap that makes 1.5 "widest" is undefended. |
| **X091** | §1.6 | `europe.py` scales **wealth**, not development; the difference changes two of the quoted sink sets. |
| **X097** | §1.6 | The Cape has in-degree 1 and out-degree 3 in the 1444 `Φ_w`; 115 ordered node pairs route through it, and §1.6 says so itself eleven lines later. |
| **X100** | §1.6 | The reversal occupies [2.82, 3.18] ∪ [3.24, 3.93], not [3, 3.75] — both edges wrong, and it is two bands, not one. |
| **X107** | §1.10 | Against the node totals the spec quotes, the cap of 50 is 9.4%–47.0% (median 21.9%); 8.6%–32.0% is the share *after* the grant is added to the denominator. |
| **X112** | §2.2 | 15 provinces, not 16, are "beyond the two trade goods": 542 (Golconda) is also one of the 43 gems provinces. |
| **X125** | §2.4 | "On the fallback branch the wealth key ties and the index alone decides" is false — in the spec's own T3 the wealths are 3, 2, 1. The emitter-order requirement is real; its stated reason is not. |
| **X151** | §3.2 | The fallback branch is not "the one place the indexing is load-bearing": the index decides wherever the `(DEF, b)` key ties, and on the fallback branch the candidates' wealths are generally distinct (79 of 80 nodes, no ties at 1444). |
| **X155** | §3.5 | No exception was hidden, the claimed per-file assertion does not exist, and **ten** blocks are display text (7 quoted `effect_tooltip`, 3 `tooltip = { }`) — so the executable count is 151, neither v5.0's 161 nor v4.0's 154. |
| **X169** | §3.10 | Seven distinct downstream sets, not eight, and the stated cause is not the one the measurement shows. |
| **X176** | §3.13 | Five of the seven named categories carry neither key — only the country-scoped `global_` form §1.3 already excludes — and six real carriers are omitted. |
| **X185** | §3.15 | The supply contrast runs 1–97, not 4–97: `cloves` has a single producing node, ratio 1.00, as the author's own `final.py` prints. |
| **X191** | §3.15 | Only v4.0 said both things; v2.1 and v3.0 quote a bare agreement figure with no γ and no mass-field statement. |

### Partials

Each is right in substance and wrong in a stated detail, or right on 1444 and not in general.

| ID | § | What is wrong |
|---|---|---|
| X008 | §1.1 | Right for an un-peeled core; the condition is on the *post-peel* balance β, and the step from "a candidate with inflow" to "a flow-terminal demander" is not supplied. |
| X010 | §1.1 | "Usually all zero-wealth" is false — 1444 has one zero-wealth node and 79 distinct positive ones with no exact ties; where the key does tie it ties at a common *positive* value. |
| X011 | §1.1 | The emitter-order requirement holds, but the index decides at `(DEF, b)` ties generally, not only on the fallback branch. |
| X013 | §1.1 | Phase-0-no-op plus no-fallback give *containment*, not equality; equality is a 1444 measurement. The four figures reproduce exactly (1–7 sinks, mean 3.586, 0 fallbacks, 29/29). |
| X016 | §1.1 | "Holds exactly where the key has no exact ties" states a sufficient condition as a characterisation; X150, its own §3.2 twin, words it correctly. |
| X018 | §1.3 | §1.3's expression puts the flat goods bonus outside the percentage multiply and §2.2's puts it inside; only §2.2 matches the solver. No 1444 consequence. |
| X030 | §1.3 | The locality test's enumerated attribute list excludes the four province-state modifiers the table then classifies as local, and its "no country's state" clause excludes `occupied` and `under_siege` outright. |
| X033 | §1.3 | The sweep is real but not whole-install — it misses `provincial_production_size`, a second DLC-gated PTM, the buildings row, non-zero start devastation, and two counts. |
| X043 | §1.3 | The near-miss is real and confirmed; the count is 363 (324 counted), not 361 — and no script in the toolchain computes it. |
| X045 | §1.3 | Classification right, provenance wrong: it is a shipped file value (`trade_goods_size_modifier = 0.5`) with an unmentioned trade-league sibling (+1.0), not a binary string. |
| X046 | §1.3 | The three named buildings are absent, but buildings are not empty at 1444: `fort_15th` on 251 counted provinces and one `shipyard`. Neither grants a wealth key. |
| X047 | §1.3 | The terrain half is exact; the climate half omits `migration_cost` and the two movement-speed keys. Conclusion holds. |
| X048 | §1.3 | Tiers are absolute, not cumulative (falun 3.0 / 6.0 / 9.0). Right answer at 1444 only because every tier-0 block is empty and all six projects sit at tier 1. |
| X055 | §1.3 | True for province 8, but `cerro_rico_modifier` (province 795) carries the identical `NOT has_dlc Leviathan` gate and appears nowhere in the document. |
| X056 | §1.3 | Both values verified from the files; "the project does not exist" without Leviathan is inference from a gate, not observation. |
| X059 | §1.3 | `iqta`'s +5% checks out exactly; the Clergy +5% is not traceable to the estate file, whose shipped values are +0.2 / +0.2 / −0.1. |
| X067 | §1.6 | The world state moves the sink *count* as well as the locations — which strengthens §3.1 goal 1 rather than weakening it. |
| X078 | §1.6 | The band reproduces exactly; "the widest band on this field" is true only inside the unstated [1.00, 3.00] scan cap. |
| X086 | §1.6 | 823 and the ×1.02 sink set reproduce, but the set is scaling-method dependent, the real threshold is ×1.010, and "a sink at every larger factor" holds only because testing stopped at ×1.60. |
| X087 | §1.6 | "Asia holds none" fails under development scaling — `hangzhou` is still a sink at ×1.56; Asia empties at ×1.57. |
| X099 | §1.6 | The 22-node ×2 result reproduces; the 18-node threshold is ×2.15, not ×2.5. |
| X106 | §1.10 | The banding classification holds, but banding is not the only damper — a shipped policy cooldown gates re-selection of both banded policies. |
| X114 | §2.2 | The figures reproduce as an interval but not as a stable one; a median over a stated run count would carry the claim, a min–max over unstated runs does not. |
| X117 | §2.2a | The index-independence half is measured on *post-fold* balances, and Phase 0 can create exact ties the raw balances lack, so the 1444 measurement does not transfer to a peeled map. |
| X124 | §2.4 | The dump evidence is real, but the cited source records **two** launches, the third comes from a different document, and §2.7 still says "twice". |
| X143 | §3.2 | "3.6–4.9×, i.e. 9.3–21.4%" pairs two ranges whose endpoints come from different nodes; the share a multiplier buys is not monotone in the multiplier. |
| X145 | §3.2 | Phase-0-no-op and no-fallback are necessary but not sufficient — T2 satisfies both and still breaks the equality. |
| X154 | §3.5 | 161 / 93 / 14 / 1 / 53 all reproduce exactly, but 7 of the 14 `missions/` blocks sit inside quoted display strings the engine never executes — the executable count is 154. |
| X160 | §3.9 | 13 / 8 / 11–17 all reproduce; "not a band containing its own baseline of 13" is false, since 9 ≤ 13 ≤ 17 — the sentence survived the regeneration of the numbers it was about. |
| X165 | §3.10 | The conclusion holds, but the enumeration of node-wide power terms is incomplete as stated; the load-bearing fact is that no trade-power modifier takes a good as an argument. |
| X166 | §3.10 | The residual reproduces in order of magnitude, but the construction that produces it is still not stated in the document — the same failing X167 charges against v1–v4. |
| X170 | §3.10 | The nine percentages are reproducible only under one unstated free parameter; the per-collector signs are specific to that choice. |
| X171 | §3.10 | "Thirteen orders of magnitude" is right for the largest effect and wrong for the smallest one quoted in the same paragraph (0.003% is eleven). |
| X172 | §3.10 | The construction has two free parameters, not the one the claim names. |
| X177 | §3.13 | Every file-checkable half verifies; the tooltip itself is a single unreproducible observation and should not be promoted above that. |
| X178 | §3.13 | The arithmetic is sound, but "across the development range" rests on two `base_tax` points (2 and 6) at the bottom of the range. |
| X179 | §3.13 | 13 + 11 + 2 = 26, not 30: the four goods with a non-reaching negative event are also unreachable and were dropped from the partition. |
| X186 | §3.15 | True of v4.0; v3.0's own §3.2 still asserted the ratio, so v3.0 was not "withdrawing it". |
| X190 | §3.15 | Every figure reproduces and "every larger γ worse" survives a 0.005 sweep, but the maximum is a plateau over γ ∈ [0.01, 0.95], not a peak at 0.90–0.95. |

### Unverifiable

- **X022** (§1.3) — Arithmetic consistent (3.52 / 12 = 0.29), but one tooltip reading on one province and a divisor inferred from a single point.

---

## Systemic findings

These are defect *classes*, each supported by several independent claims. They matter more than
any single refutation, because each one predicts where the next error will be.

### S1. The whole-install sweep is not whole-install — and it walked past one of the two constants §2.3 says is in no file

`common/static_modifiers/00_static_modifiers.txt` contains

```
provincial_production_size = {
	trade_goods_size = 0.2
	ship_recruit_speed = -0.01
}
```

and `localisation/EU4_l_english.yml:815` gives that block's display name as **`"Base Production"`** —
which is verbatim the tooltip line §2.3 cites as the *measurement* of `GP_COEFF`
("Garnatah (223) 4 → 0.80 with the itemisation `Base Goods Produced: 0.80 / Base Production: +0.80`").
The number the spec recovered by reading a tooltip four times is printed in a shipped data file, in
the same directory the §1.3 sweep visits for `devastation` and `occupied`. So:

- §1.3's "neither is a define (`defines.lua` was searched), so both are engine constants recovered
  by observation" and §2.3's "**the two wealth coefficients are hardcoded in the binary**" are
  **false for `GP_COEFF`**. It is a moddable file value.
- §2.3's own governing rule — "Read at runtime; never hardcoded" — is violated by the one wealth
  constant the install exposes. For a *mod* spec this is not cosmetic: any mod that edits
  `provincial_production_size` silently invalidates every wealth figure in the document.
- `TAX_COEFF` survives the same test (`provincial_tax_income` grants no tax key), but it too is
  file-derivable rather than only measurable: `core = 0.75` plus `city = 0.25` sums to exactly 1.00,
  which is X062's reference condition read straight off the file.

The same sweep also missed `cerro_rico_modifier` (X055), mis-stated the buildings row (X046),
under-enumerated terrain/climate keys (X047), never noticed that `devastation` is non-zero at the
1444 start (X040), and got the centre-of-trade and great-project counts wrong (X043, X050). The
rule §1.3 introduces is right; the sweep it licenses was not carried out to the rule's own standard.

### S1b. "At the 1444 start" is read from `history/provinces/`, and the game's 1444 start is not the same object

Two consequences, both found by comparing my history parse against the `gamestate` of
`VANILLA_start.eu4` (`meta`: `date=1444.11.11`, Leviathan enabled):

1. **`devastation` is non-zero on ten counted provinces at the start** — Bohemia's Hussite-war
   devastation, Prague at 50, Pardubice/Jindrichuv Hradec/Budejovice/Hradecko at 50, five more at 20.
   The word `devastation` appears in **zero** `history/provinces/` files. **The mechanism is
   `on_startup`**: `common/on_actions/00_on_actions.txt:33` calls `on_startup_effect`, defined at
   `common/scripted_effects/01_scripted_effects_for_on_actions.txt:4716`, which contains
   `if = { limit = { tag = BOH NOT = { has_country_flag = boh_hussite_aftermath_flag } } … country_event = { id = flavor_boh.15 } }`
   (line 4795), and `flavor_boh.15` — "The Aftermath of the Hussite Wars",
   `events/flavorBOH.txt:938` — carries
   `immediate = { hidden_effect = { bohemia_area = { add_devastation = 50 } erzgebirge_area = { add_devastation = 20 } moravia_area = { add_devastation = 20 } … } }`.
   The values and the areas match the save exactly. `on_startup` also fires six other events
   (`flavor_mng.42` for Ming's starting situation, `flavor_mos.1`, `flavor_geo.1`, …), at least one
   of which — `flavor_geo.1` — contains `add_base_tax`, `add_base_production` and `add_devastation`.
   **So the 1444 start state is `history/provinces/` *plus whatever `on_startup` does*, and a sweep
   of the history files is structurally incapable of seeing the difference.**
2. **Twenty owned provinces are dropped by the `is_city = yes` filter that the game does not drop.**
   In the save, *every* owned province is `is_city = yes` — 2,472 of them. The model counts 2,452.
   The twenty missing are the ones whose history file never writes the flag: nineteen native and
   small-tag provinces, and **province 265 (Brno)**, whose vanilla file carries the line commented
   out — `#is_city = yes` — while being a cored, HRE, `base_tax` 3 / `base_production` 3 Bohemian
   province. The omission is 34.75 ducats, 0.325% of world wealth. §1.3's stated *reason* for the
   filter is that "an unowned province produces nothing the trade system can move"; none of the
   twenty is unowned. The rule and its rationale have come apart, and reading the flag from the
   game state instead of the history file closes the gap exactly.
3. **Fourteen counted provinces carry `trade_goods = unknown` in history and a real trade good in
   the game.** The engine assigns a good at game start to every `unknown` province, rolling it from
   the `chance = { … }` blocks that every entry in `common/tradegoods/00_tradegoods.txt` carries —
   which is what those blocks are for. In this save they came out livestock, cotton, fur ×4,
   grain ×5, wool, naval supplies, and the model prices all fourteen at `unknown`, i.e. at zero
   trade value: 8.20 ducats missing, and fourteen provinces absent from the supply shares `s` of
   six goods. **This one is randomised**, so §1.3's own caution about the `Industrious` personality
   (X026 — "any window figure is one sample of a random variable") applies to the wealth field
   itself, and nothing in the document says so.
4. **`add_base_tax` in a pre-start dated block is not applied.** Province 1 (Uppland) has
   `base_tax = 5` undated and `1436.4.28 = { … add_base_tax = 1 }`; the game has 6, the model's
   cache has 5. Exactly one province is affected (I swept all three `add_base_*` keys over every
   dated block ≤ 1444.11.11), so this is worth one ducat — but it is a fourth instance of the same
   class, and the fix is one line in the province parser.

**Sizing the class.** Together these four cost the model 43.95 ducats of wealth it should have
(0.41% of 10,677.50, across 45 provinces) and give it 6.92–17.30 ducats it should not (the ten
devastated provinces, depending on how the engine scales `devastation`'s `trade_goods_size_modifier
= -2`, which the files do not settle). For scale: **that is between a third and a half of the entire
province-modifier apparatus §1.3 was rewritten to add**, which is worth 0.98% over 87 provinces.

### S2. Counts quoted against the wrong denominator

Six independent instances, each *nearly* right, which is why none was caught:

| Claim | Stated | Actual | What went wrong |
|---|---|---|---|
| X050 | 85 of **130** great projects | 88 of **138** | 130 is the number of distinct `start` **provinces**; eight provinces host two live projects each |
| X043 | **361** provinces carry a CoT | **363** (324 counted) | no script in the toolchain computes it at all — the number exists only in `q01.py`, the patch that wrote the sentence |
| X112 | 16 provinces **beyond** the two trade goods | 16 provinces, **15** beyond | province 542 (Golconda) is a modifier province *and* one of the 43 gems provinces |
| X035 | "the **five** province-state static modifiers" | **four** | `occupied` contributes two keys; values were counted as modifiers |
| X179 | 13 + 11 + 2 over **30** goods | sums to **26** | the four goods with a non-reaching negative event are also unreachable and were dropped from the partition |
| X169 | **eight** distinct downstream sets | **seven** | the eighth set is not realised by any live good |

### S3. Sampled points quoted as thresholds and band edges

X099 quotes ×2.5 where the threshold is ×2.15. X100 quotes "between ×3 and ×3.75" where the
reversal occupies **[2.82, 3.18] ∪ [3.24, 3.93]** — both edges wrong, two bands not one, 36 reversed
factors outside the quoted window and 5 non-reversed inside it; ×3.75 is produced by no script and
appears only in `q02.py`, the edit that wrote the sentence. X086's "×1.02" is the smallest factor
*tested*, not the threshold (×1.010). X101's dev-stack series samples ×10/×20/×30/×50 and reports
the ×10 split as "transient" without bracketing it.

The instructive part is the contrast: where refinement *was* run — the α_Φ band table, X082's
refinement to 0.001, X192/X193's eight-seed noise study — the work holds under re-measurement. The
defect is not sloppy measurement. It is that the refinement discipline was applied to the paragraph
under scrutiny and not to its neighbours in the same section.

### S4. A superlative relative to an unmotivated scan range, carrying the model's one free constant

The α_Φ band table is captioned "measured across α_Φ = 1.00…3.00 at 0.01", and "the widest band on
this field" is true inside that cap. Over α_Φ ∈ [1, 8] the widest band is **[4.19, 6.73]**, width
2.54. The spec gives no reason for the cap, and both §1.6 and §2.3 hang the *retention* of α_Φ = 1.5
on the superlative the cap produces (X083). A design decision resting on a range choice that is
itself undefended is the same defect §2.3 identifies in the calibration it withdraws.

### S5. Quantifier strength, not provenance, is where this document breaks

§3.16 nominates *provenance* as the risk signal ("anything that entered without a recorded source").
This audit says otherwise. Almost every refutation here landed on a claim with impeccable
provenance — a file value, a numerical test, an engine test — and landed because of its
**quantifier**. Universals and enumerations fail; the same facts stated existentially would have
survived:

- "**all** are zero at the 1444 start" (X040) — ten Bohemian provinces carry devastation 20–50
- "buildings … **empty** at 1444" (X046) — 251 provinces carry `fort_15th`
- "**nothing** routes through the Cape" (X097) — in-degree 1, out-degree 3, 115 ordered pairs
- "the **whole** of the rule-versus-vocabulary tension" (X058) — at least seven further cases
- "grant **only** [nine keys]" (X047) — `migration_cost` and two movement-speed keys omitted
- "**the** vanilla set … is" (X035) — two sources missing
- "**every** larger γ is worse" (X190) — survives, but the maximum is a plateau over [0.01, 0.95], not a peak at 0.90–0.95
- "the contrasts run **4**–97" (X185) — `cloves` has one producing node, ratio 1.00
- "the **one** place the document declines to project a number" (X004) — three places
- "the **one** place the indexing is load-bearing is the fallback branch" (X151) — 2,774 of 7,146
  random instances changed orientation under relabelling with no fallback anywhere in sight
- "holds **exactly** where the key has no exact ties" (X016) — sufficiency confirmed, necessity false
  on 408 tie instances; the section's own twin, X150, says "holds where" and is right
- "**That** happens for the aggregate graph on a uniform-wealth map, and for a per-good graph on a
  component with no producer and no consumer" (X009) — an enumeration of two where the truth is a
  family, and the first member is misstated

The rule the next revision needs is not "cite a source"; v5.0 does that everywhere. It is: **a
universal quantifier is a claim about the complement, and the complement has to be swept.**

### S6. Regeneration moved the numbers without re-reading the sentences built on them

X160 says v2's "9–17 ends" is "neither the right word for a range of 11–17 nor a band containing its
own baseline of 13" — but 9 ≤ 13 ≤ 17, so the second half is simply false. `changes-v5.md`
entries 37–38 show it was *true* in v4.0, where the numbers were 13–22 against a baseline of 18; the
sentence survived the v5.0 regeneration of the numbers it was about. X186 and X179 fail the same
way: a criticism of an earlier version that was accurate against that version and was carried
forward past the edit that falsified it.

### S7. Contradictions inside a single section

- **§1.3**: X021's `Base: X (Yearly 12·X)` and X027's `0.49 × 1.25 = 0.6125 → 0.62` both contradict
  X120's truncation rule, three claims later in the same section. 12 × 0.49 = 5.88; trunc(0.6125) = 0.61.
- **§1.6**: X097's "Nothing routes through the Cape" is contradicted eleven lines below by the same
  section's "1444's Atlantic→Cape→Indian-Ocean drainage".
- **§1.6 vs §2.4**: X065's "the count is set by α_Φ" against X127's "the count is not fixed — it
  follows the wealth field *and* α_Φ", and against X086/X101's own measurements of the count moving
  at fixed α_Φ.
- **§2.4 vs §2.7**: the cycle crash is "reproduced on **three** launches" in §2.4 and §3.6 and
  "twice" in §2.7.
- **§1.3 vs §2.2**: `goods_produced`'s flat term is inside the percentage multiply in §2.2 and
  outside it in §1.3 (X018).
- **§1.1 / §3.2 vs §2.2a**: §2.2a's table correctly makes sink-set equality a *measurement* that
  fails wherever T2 can fire; §1.1's bullet and §3.2 item 1 both present "Phase 0 is a no-op and no
  fallback fires" as the condition under which equality *holds*, and the spec's own T2 satisfies
  both and breaks it (X013, X145).
- **§2.2 vs §3.14**: the survival table is "30 goods × 80 BFS" in §2.2 item 7 and 29 goods in §3.14;
  §1.5's latent rule makes 29 the right number, so §2.2 is the outlier (X184).

Two further prose defects were found inside audited sections but attach to no X-row:

- **§2.8 calls Genoa "demand rank 1" for spices.** Genoa is demand rank **2**; `hangzhou` is rank 1,
  is the Phase-1 selection, and is not a sink. The row's argument is unaffected, but the parenthetical
  is wrong.
- **§3.2's "deleting demand variation entirely left the sink unmoved"** did not reproduce in an
  independent reconstruction of the v1 Laplacian operator: a uniform `c` moved both the spices and
  the cloves sink sets. This is inherited v1 diagnostic text and the reconstruction may differ from
  v1's ε handling, so it is flagged rather than scored — but it is the last unregenerated measurement
  in §3.2 and it should be re-run before it is quoted again.

### S8. `change_price` semantics are never stated, and every §3.5 figure depends on them

`change_price` values are **fractions of base price**, not ducat deltas — provable from the shipped
save (`paper` base 3.5 with one `value=0.250` reaches `current_price=4.375`, i.e. ×1.25). Every
figure in §3.5 is correct under that reading (`wool` 2.5 × 0.75 = 1.875; `grain` 2.5 × 0.25 = 0.625)
and unreadable without it: a reader computing 2.5 − 0.25 = 2.25 finds the section self-contradictory.
One sentence fixes it, and its absence is the reason the census has now been reopened three times.

### S9. Stale and hardcoded values inside the toolchain the spec cites as its evidence

`drainrep.py:276` prints `RANK 9/387` as a string literal (the true value, and the spec's, is 8).
`w10.py` still carries a bare `except Exception: pass` while §3.5 claims the scan "is now guarded by
a per-file count assertion" — there is no such assertion (X155). `wealthmodel.py`'s docstring
repeats X112's "beyond gems/incense" error. `drain.py`'s module docstring still describes the v3.0
fallback ("promotes the gate-true unmarked node with the most negative beta") while the code
implements the v4.0 one (`max(gated, key=lambda v: (NODEW[v], -v))`).

---

## Verdict on `scripts/validate_v5.py`

The harness does what it says: 135 result rows, 0 failed, 18–24 s. What it *checks* is not what the
brief for it implies.

**Classification of its 133 assertion sites** (83 `chk`, 32 `has`, 18 `hasnt`; one `chk` sits in a
`range(3)` loop, giving 135 executed):

| Bucket | Count | What it does |
|---|---|---|
| (a) text-presence | **51** | asserts a byte string is present in / absent from the spec |
| (b) self-confirming numeric | **66** | compares `solver.py`/`drain.py` output to a literal that was produced by the same code path |
| (c) genuine independent re-derivation | **13** | recomputes from the install or the save and compares against a literal the spec states |
| (d) tautological | **5** | e.g. `chk("1.10", "flag inland / derived inland", (26, 25), (26, 25))` — the "got" side is a hardcoded tuple; no code anywhere computes either number |

**The structural point.** `TXT` — the spec — is read by exactly three things: `has`, `hasnt`, and one
`chk` counting `[unverified in`. **Eighty-two of the eighty-three `chk` sites never open the spec.**
There is no assertion anywhere in the file that compares a number *printed in the document* to a
number *computed from the game*. The numeric half checks the solver against itself; the textual half
checks the prose against itself; the two halves never meet. `validate_v5.py` is `v5measure.py` with
`P(label, value)` replaced by `chk(sec, what, got, exp)` and the printed value pasted in as `exp`.

**Mutation test.** Ten factual errors were planted in a copy of the spec and the harness repointed at
it. **One of ten was caught** — and that one (`361` → `3,610`) only as a missing byte string, not as a
wrong fact. World wealth `10,677.50` → `12,345.67` and `2,452` → `9,999` both **passed**, while the
same run printed `got=10677.5 exp=10677.5`.

**What it does not check at all.** Every `engine test` claim (14 of them, including `GP_COEFF` and
`TAX_COEFF`). §1.3's install-sweep facts exist only as `has()` substrings — the centre-of-trade
count, `production_leader`, the Leviathan gate, the static-modifier row — and **buildings-empty-at-1444
and the terrain/climate key list are not checked even as strings**. No sweep for them exists anywhere
in the tree: `wealthmodel.py`, which `README.md` credits with "§1.3's whole-install modifier sweep",
contains none; the only other file naming them is `q01.py`, the patch script that types the table into
the spec. `PERM_FLAT`'s ten provinces are never re-derived. §3.10's nine propagation percentages are
covered by one `has()` on a phrase. §3.15's rejected-operator figures (ρ_val +0.281 / +0.054,
43.8% / 14.5%, 8 net-producer sinks, BASIN 88.4%) have **zero occurrences**. The 3-sink `[2.26, 2.71]`
band row lives only in a hardcoded `_BASE` dict. §3.5 is the one honourable exception: it is genuinely
re-swept from the install.

**The one thing it validates outright.** `edits5.json` holds exactly 68 records and `stats5.py`
replays them against the v4.0 spec asserting byte-identity with v5.0, with a per-anchor uniqueness
assert; it passes in 0.19 s. That is a real guarantee — that no undocumented edit slipped into v5.0.
It is a guarantee about the *edit list*, not about any fact.

**Verdict.** A well-built regression suite pointed at the wrong target. Roughly one check in ten
could have failed if the world were other than the spec says; the other nine pin the document and the
solver to each other. Read as evidence, it establishes that v5.0 is internally consistent with the
code that generated it, and nothing about whether either is right. Notably, **every one of this
audit's twenty-two refutations sits in the ninety percent** — not one was in a position to be caught.

---

## Per-claim findings

### X001 — v5.0 folds through every refuted and partial claim from all four audits, including v4.0's own
**Status:** CONFIRMED
**Method.** Enumerated the graded findings of `validation-v3.md` (10 REFUTED, 19 PARTIAL, plus the
five `validation-v2.md` partials v3.0 never folded) and `validation-v4.md` (Part E's two own
refutations), then grepped the v5.0 spec for each repair. Nine spot-checks, chosen to include the
hardest cases (the five unfolded v2 partials and v4.0's self-refutations).
**Evidence.** All nine are present in v5.0:
- V071 → §1.8 l.496–497 "What trade range gates is **reach, not flow**" (the flat universal negative is gone).
- V075/V076 → §1.10 l.542–549 carries the full nine-rung banded ladder (10→5, 15→5, 20→10, 25→15, 30→20, 35→25, 40→30, 45→35, 5-flag no maintain share).
- V090 → §2.2 l.645–647 quotes the measured 5.4–24 ms range and 7.3 ms average instead of "tens of milliseconds".
- V223 → §1.6 l.431–438 names "**the 22 European nodes**" and gives the ×3–×3.75 Cape band.
- W041 → §1.3's two-test table, with the `chinaware` `local_autonomy` row present and "exactly three" gone.
- W049 → §1.3's `Core` 0.75 + `City` 0.25 = 1.00 reference condition; the cancellation argument is gone.
- W124 → §1.1 Phase 3 fallback defined; `T3` labelled in §3.2 (verified by grep).
- W144 → §3.5 says two boundary goods, `gems` and `silk` (reproduced independently, below).
- v4.0's own Part E (`5.7e-14`/`1.4e-14`, `5.96 ducats`, and v4.0's own replacement `0.41%`) → §3.10 l.1210 supersedes all three with the per-collector redistribution figures and a 3.7e-16 residual.

No spot-check found an unfolded finding, so coverage is confirmed. Two folds nevertheless landed on
wrong numbers — see X154/X155 (the `change_price` census) and X124 (the launch count). Those are
defects in the fold, not gaps in coverage, and are graded there.

---

### X002 — v5.0's substantive change: §1.3's classification applied to the whole install, adding sixteen provinces
**Status:** CONFIRMED
**Method.** Read `solver.py`/`wealthmodel.py`'s modifier tables and counted the distinct province
ids; spot-checked each class against the install (`common/great_projects/01_monuments.txt`,
`history/provinces/*`, `common/event_modifiers/00_event_modifiers.txt`).
**Evidence.** `FLAT` carries 15 ids, `GPMOD` 1, `TVMOD` 4; the union is exactly **16** distinct
provinces: 8, 262, 684, 1821, 1822, 2145 (six great-project provinces) and 6, 362, 363, 370, 371,
387, 542, 2151, 2316, 4316 (ten permanent province modifiers). This is disjoint from the gems/incense
trade-good rows. Spot-check: province 362 (`362 - Rosetta.txt`) carries two permanent modifiers,
`nile_estuary_modifier` (grants only `province_trade_power_value = 5`, which wealth does not read)
and `granary_of_the_mediterranean` (`trade_goods_size = 2.0`, matching `FLAT[362] = 2.0`).
§3.13's cross-reference — "fifteen 1444 provinces carry a **flat** `trade_goods_size`, five from
great projects and ten from permanent province modifiers" — is consistent: of the six great-project
provinces, five carry a flat value and one (262, `krakow_cloth_hall`) carries a modifier.

---

### X003 — the change moves the aggregate graph from two 1444 sinks to one
**Status:** CONFIRMED
**Method.** Rebuilt the wealth field twice from `wealthmodel.wealth()` — once with the whole-install
tables, once with them emptied (the v4.0 trade-good-tables-only field) — and ran `Φ_w` at α_Φ = 1.5
on each.
**Evidence.** v4.0 field → sinks `['english_channel', 'hangzhou']` (two, matching v4.0 spec l.673–674
verbatim). v5.0 field → sinks `['hangzhou']` (one). The transition is caused by the sixteen
provinces, not by anything else in v5.0.

---

### X004 — no figure in v5.0 is unverified, and the one place the document declines to project a number says so in place
**Status:** REFUTED
**Method.** Grepped the spec for unverified/unsourced/TODO markers; grepped for every place that
declines a number; checked the claims inventory's provenance column; checked whether measured
figures carry script attribution in the document; and checked the one figure whose cited source I
could read against that source.
**Evidence.**
1. **"The one place" is at least three.** §3.10 l.1210: "so no single percentage is quoted as one."
   §3.13 l.1270: "One question, and it is a question rather than a number — §1.3 carries no value
   for it." §2.4 item 2: "The count is not fixed … so the emitter reads it from the solve rather
   than assuming a number." Three distinct declinations, not one.
2. **A figure that its own cited source does not support.** §2.4 and §3.6 both say the cyclic-file
   crash was "reproduced on **three** launches", and §2.4 attributes the passage "*(Both from
   `../v2-drain/game-session.md`.)*". That file says "reproduced on **two** independent launches",
   "stack overflow, **twice**", "reproduced **twice**", "**×2**". The third reproduction exists but
   comes from `validation-v3.md`, which the spec does not cite. And §2.7 of the v5 spec itself still
   says "1002 frames at one address, **twice**" — the document contradicts itself, so at least one of
   the two figures is unverified against anything the document points at.
3. **The supporting sentence is false as stated.** "Every measured number carries the script that
   produced it" — the spec contains exactly **6** `.py` references in 1,503 lines (l.82, 313, 361,
   400, 413, 978). §3.5's census, §3.8's 92.2%, §3.13's whole calibration block, §3.15's contrasts,
   RANK/BASIN figures and gravity kernel, and §2.8's tables carry no inline attribution; the mapping
   lives in `scripts/README.md` at section granularity only.
4. §3.5's `161` is a figure that is wrong, not merely unattributed — see X154.
**Should say:** "No figure in v5.0 is unattributed" is defensible only at section granularity via
`scripts/README.md`; and the document declines a number in three places (§2.4, §3.10, §3.13), not
one. §2.4/§3.6's "three launches" must either be re-attributed to `validation-v3.md` or reduced to
"twice", and §2.7 must be brought into line either way.

---

### X005 — Fallback branch: with no flow-terminal demander among the candidates, promote the highest-wealth candidate, ties by node index
**Status:** CONFIRMED
**Method:** Read the branch in both sweeps of `drain.py` (`sweep`, `sweep_priority`) and in
`toys.py`'s generic implementation; checked it against §1.1's Phase-3 wording; checked the guard it
sits behind.
**Evidence:** Both sweeps carry `s_star = max(gated, key=lambda v: (NODEW[v], -v))`, reached only when
`terminals = [u for u in gated if len(outs[u]) == 0 and inflow[u] > ZERO_TOL]` is empty — i.e. exactly
"the candidates hold no flow-terminal demander". `-v` resolves wealth ties to the *lowest* index; the
spec says only "ties by index", which the implementation satisfies. The guard does not test `b < 0`,
and does not need to: a node with zero outflow and positive inflow has `b = −inflow < 0` by LP
conservation, so every "flow-terminal" is genuinely a demander. Stipulation and reference
implementation agree.

---

### X006 — Node wealth is a good-independent input, so the fallback needs no bootstrap
**Status:** CONFIRMED
**Method:** Traced `NODEW` in `drain.py` back to `solver.ROWS`; checked when it is computed and what
it depends on.
**Evidence:** `NODEW[NIDX[r["node"]]] += r["tax"] + r["prod_income"]` over `solver.ROWS`, executed at
module import — before any solve, with no `g` in the expression (the per-good exponent `α(g)` is
applied to `C`, never to `NODEW`). So it is available when the fallback fires and carries no
dependence on the good being oriented: no bootstrap. Measured on 1444: 80 values, range 0.0
(`cape_of_good_hope`) … 316.6 (`english_channel`), **80 of 80 distinct**, min positive 1.50.
*Note (not a refutation):* in X009's per-good case the key is degenerate. `build_sc` puts no per-good
gate on demand, so `c_g(n) > 0` for **every** good at **every** node with an owned province; a
per-good component with no consumer is therefore a component with no owned provinces, where
`NODEW ≡ 0` and the wealth key carries no information at all. The input is good-independent and
available as claimed; it is simply uninformative in exactly that case.

---

### X007 — Candidates are the unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least one always exists and the sweep always advances
**Status:** CONFIRMED
**Method:** Proved it, then brute-forced it.
**Evidence:** Proof. (a) With unit arc costs a directed cycle in the support could be cancelled for
strictly lower cost, so *every* optimum has acyclic support — the premise is a theorem, not a solver
property. (b) The flow-arc subgraph induced on the unmarked set is a finite DAG and has a sink; a
sink of that induced sub-DAG has all its flow out-neighbours marked, i.e. `cnt == 0`, i.e. it is a
candidate — so the candidate set is non-empty whenever anything is unmarked. (c) At a stall the
promoted/fallback node joins `Sset` and is gated, hence `ready`, hence popped on the next iteration:
progress is strict.
Brute force: 11,381 random connected graphs (n = 4–6, random zero-sum balances, random wealths)
through the independent implementation — `NO_CANDIDATE` 0, `LIVELOCK` 0, cyclic flow support 0.
I also checked the heap discipline in `sweep_priority`: `ready` is monotone in the marked set and
every transition that can make a node ready (`cnt` decrement, `Sset` growth, a free neighbour being
marked) is followed by a push, so a reported stall is never a missed wake-up.

---

### X008 — The fallback fires only when every candidate is support-isolated with zero balance — on a connected core, only when `b ≡ 0` across it
**Status:** PARTIAL
**Method:** Proved the intended statement, then attacked the literal one.
**Evidence:** Proof of the intended statement: at a fallback stall no unmarked node has a flow
out-arc (following flow arcs forward inside the unmarked set otherwise reaches a candidate with
`inflow > 0`, which fires the *promotion* branch, or the node itself is `ready`), hence none has a
flow in-arc either (its source would then have an out-arc), hence every unmarked node is
support-isolated and `β = 0` by conservation. If any node were already marked, connectivity gives an
edge from the unmarked set to the marked set; that edge is free (its unmarked endpoint carries no
flow), so its unmarked endpoint is `ready` — contradiction. So the marked set is empty, the flow is
empty, and `β ≡ 0` across the core. **The spec's stated "because" clause does not reach this
conclusion** — it yields only "the candidates are support-isolated"; the step to *the whole core*
needs the connectivity + free-edge argument, which §1.1 never gives.
Brute force agrees with the intended reading: 114 fallback firings in 11,381 instances, all on a
connected core, all with `β ≡ 0` on the core — zero counterexamples.
But `b` is defined at the head of §1.1 as `b_g(n) = s_g(n) − c_g(n)`, and under *that* reading the
claim is false: **75 of the 114 firings had `b ≢ 0`**. Minimal counterexample, reproduced in both
implementations — nodes A,B,C,L; edges A–B, A–C, B–C, A–L; `b = (A +1, B 0, C 0, L −1)`, an ordinary
good with one producer and one consumer. Phase 0 peels L and folds −1 into A, so `β ≡ 0` on the
connected triangle, the sweep stalls at `t = 0` with no flow-terminal demander, and the fallback
promotes A. `b ≢ 0` across the core (A carries +1) and the branch fires anyway.
**Should say:** "…on a connected core, only when the **post-peel balance `β`** is identically zero
across it — which Phase 0's fold can produce from a `b ≢ 0` input", and the justification needs the
missing step: any edge from the unmarked set to a marked node is free, so on a connected core a stall
with support-isolated candidates can only occur before anything is marked.
*(Second order: `ZERO_TOL` is absolute (1e-11), so "support-isolated ⇒ β = 0" is exact only to
`deg × 1e-11`; §1.6 already records the scale coupling.)*

---

### X009 — That happens for the aggregate graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no consumer
**Status:** REFUTED
**Method:** Tested both named cases against §1.6's definition of `b_w` and against the peel.
**Evidence:** *Case (a) is false as stated.* §1.6 sets `s_w(n) = 1/N` and
`c_w(n) = Σ_{p∈n} wealth(p)^{α_Φ} / Σ_world`, so `b_w ≡ 0` requires **equal `Σ_{p∈n} wealth(p)^{1.5}`
per node** — which "uniform wealth" does not deliver. Measured: three nodes with *identical node
wealth* 2.0 but province splits (1+1) / (2) / (2) give `b_w = (+0.0721, −0.0361, −0.0361)`; no
fallback fires, an ordinary sink appears at B. Uniform *province* wealth with province counts 2/1/1
gives `b_w = (−0.1667, +0.0833, +0.0833)`, also non-zero. Only the variant with one province of equal
wealth per node gives `b_w ≡ 0` and fires the fallback — and there the candidates carry wealth 2.0
each, not zero (see X010).
*Case (b) is not the family.* On a connected map it cannot arise at all (it needs a second
component), and it is not the only per-good way in: the peel fold produces firings on maps that have
both a producer and a consumer (the A/B/C/L example under X008). In the random search 75 of 114
firings were of that kind and none were of the "no producer, no consumer" kind.
**Should say:** the reachable cases are "any graph whose **post-peel** core balance is identically
zero: the aggregate graph when every node carries the same `Σ_p wealth(p)^{α_Φ}`; a per-good
component with no producer and no consumer; and any map where Phase 0's fold cancels the core's
balances exactly."

---

### X010 — In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the node index decides
**Status:** PARTIAL
**Method:** Evaluated the "zero-wealth" premise separately from the "ties → index decides"
conclusion, in each of X009's cases, on the 1444 map, and in the spec's own worked example.
**Evidence:** The conclusion holds wherever the wealth key ties — trivially. The premise does not.
(i) In the aggregate case the candidates carry **uniform positive** wealth (2.0 each in the worked
example above): the tie comes from uniformity, not from zero. (ii) In the spec's own **T3** the
candidates carry wealth **3, 2, 1** — distinct — and the wealth key decides the promotion outright,
so the spec's only worked instance of the branch does not exercise the tiebreak this claim says is
load-bearing. (iii) In the peel-fold family the candidates carry whatever the map gives: across the
random search, fallback stalls with **distinct** candidate wealths outnumbered tied ones **81 to 2**
(1 of the 2 all-zero). (iv) On the 1444 map itself the premise is maximally false: `NODEW` has
**80 of 80 distinct values**, exactly one of them zero (`cape_of_good_hope`), the other 79 in
[1.50, 316.60] — so the wealth key strictly orders *every* candidate set that could ever arise there
and the index can never decide through it. Only X009's case (b) genuinely gives zero wealth, and it
gives it for a reason the spec does not state: in the reference model `c_g(n) > 0` at every owned
node for every good, so "no consumer" means "no owned province" means `NODEW = 0`.
**Should say:** "In those cases the wealth key often **ties** — at zero on an unowned component, at a
common positive value on a uniform-wealth aggregate map — and the index then decides." Drop
"zero-wealth" as the general characterisation: it is wrong for the aggregate case, for T3, and for
the whole of 1444.

---

### X011 — That is why §2.4 item 1 makes a canonical emitter node order a correctness requirement, and why §2.8 asserts containment over a set including the fallbacks
**Status:** PARTIAL
**Method:** Checked each half against the mechanism it names.
**Evidence:** Second half **confirmed**: T3's sink `A` lies in `{fallbacks}` and in neither
`{selected}` nor `{promoted}` (both empty there), so the narrow assertion would halt on correct
behaviour — the wide set is load-bearing (X136/X149). First half: the *requirement* is right, the
*reason* given is the weak one. The node index is load-bearing wherever the priority key
`(DEF, b, index)` ties, with or without a fallback: **2,774 of 7,146** random instances changed
orientation under a relabelling with an **identical LP support and no fallback anywhere**. And in T3
the index decides through the priority key (B and C both keyed `(0, 0, ·)`), not through the wealth
key. On 1444 the wealth key cannot decide anything at all (80/80 distinct `NODEW`), so on the map the
spec targets the fallback branch is not merely a rare reason for the requirement — it is not a reason
for it.
**Should say:** "…because §1.1's priority key breaks exact `(DEF, b)` ties by node index — and the
fallback branch is a second place the index can decide, when the wealth key also ties."

---

### X012 — Every sink is a selected flow-terminal demand centre, a stall-promoted flow-terminal demander, a fallback-promoted highest-wealth node, or a Phase-0 pendant that absorbed a net-importing subtree
**Status:** CONFIRMED
**Method:** Proof plus exhaustive check on random graphs.
**Evidence:** Proof: a node is popped only when it is in `Sset`, has a flow out-arc, or has a free
edge to a marked node; the last two hand it an out-arc, so a core sink must have been popped as a
member of `Sset` = selected ∪ promoted ∪ fallback, and any core sink is automatically flow-terminal
(a sink has no out-arc of any kind). Phase 4 orients a peeled edge `(v,u)` as `v→u` when `β_v ≥ 0`,
so a peeled node is a sink only when `β_v < 0` — it absorbed a net-importing subtree. Brute force:
7,110 random connected graphs, **0** sinks outside the four categories.

---

### X013 — Where Phase 0 is a no-op and no fallback fires, the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–7 sinks per good, mean 3.6, zero fallbacks
**Status:** PARTIAL
**Method:** Reproduced every number, then tested the stated condition as a general conditional.
**Evidence:** Numbers reproduce exactly. `final.py` V029: "measured (sinks == {S0 cap ft} U promoted):
29/29 goods; mismatches: []". Independent recount: equality 29/29, containment 29/29, sinks/good
min 1 max 7 **mean 3.5862** (→ 3.6), **fallbacks 0**; `v5measure.py` and `drainrep.py` agree.
The *condition* is not sufficient, and the spec's own **T2** is the counterexample: the five-cycle
with a chord has minimum degree 2 (`Plog` empty, Phase 0 peels nothing) and fires **no** fallback,
and its sink set is `{u2}` against a formula set `{u1, u2}`. So "where Phase 0 is a no-op and no
fallback fires, the sink set is exactly …" is false as written — two sentences later §1.1 says so
itself ("that equality is not a theorem in general") and then names T2 as one of the breakers.
**Should say:** "Where Phase 0 is a no-op and no fallback fires, the last two cases of the taxonomy
are empty, so the sink set is contained in `{selected} ∪ {promoted}`; that it is **equal** to
`{selected ∩ flow-terminal} ∪ {promoted}` is a measurement on 1444 (29/29 goods, 1–7 sinks, mean 3.6,
zero fallbacks) and is not implied by those two conditions — T2 satisfies both and breaks it."

---

### X014 — T3: a fallback promotion is a sink that is neither selected nor stall-promoted, so it breaks the equality inside the 2-core
**Status:** CONFIRMED
**Method:** Ran `toys.py` and the independent implementation on T3.
**Evidence:** Both give actual sinks `{A}`, formula set `∅`, `{selected} ∪ {promoted} = ∅`,
`fallbacks = {A}`; `sinks ⊆ {selected}∪{promoted}` False, `⊆ … ∪{fallbacks}` True. Core = all three
nodes (Phase 0 no-op), so the break is inside the 2-core.

---

### X015 — Ready-marking is a monotone closure, so the stall sequence and both promotion branches are provably scheduling-independent
**Status:** CONFIRMED
**Method:** Checked the monotonicity of `ready`, then measured with randomised scan orders on random
graphs and on 1444.
**Evidence:** `ready(u)` = `cnt[u] == 0 ∧ (u ∈ Sset ∨ outs[u] ≠ ∅ ∨ ∃ marked free neighbour)`: every
component is monotone in the marked set and in `Sset`, both of which only grow, so the marking
closure reached before each stall is order-independent and the candidate set (`unmarked ∧ cnt == 0`)
is a function of that closure. Both promotion rules read only that set. Measured: 7,110 random graphs
× 8 random scan orders → **0** changes to the (promotions, fallbacks) sequence; 29 goods on 1444 × 6
random scan orders → **0** changes.
*(Free-edge orientation is a different quantity and is not scan-invariant — 145 of 174 scan-order
runs on the non-priority sweep changed it — which is why §1.1 attributes free-edge determinism to the
priority key rather than to the closure. §1.1 states this correctly.)*

---

### X016 — Free-edge direction is deterministic by construction; that the node indexing never decides is measured, not proved, and holds exactly where the key has no exact ties
**Status:** PARTIAL
**Method:** Tested both directions of "exactly where".
**Evidence:** Sufficiency confirmed: over 3,897 random instances, **0** cases of "no exact
`(DEF, b)` tie yet the orientation changed under relabelling with the same LP support". Necessity
false: **408** instances had an exact key tie and were still fully index-independent (the tied nodes
were not adjacent over a free edge, or the tie fell where marking order did not matter), against
1,801 that were index-dependent. So no-ties is sufficient, not necessary, and "exactly where" claims
an equivalence that does not hold.
**Should say:** "…and holds **wherever** the key has no exact ties" — a sufficient condition, not a
characterisation. (X150, the §3.2 twin of this row, already says "holds where" and is correct.)

---

### X017 — Measured: zero orientation changes under scheduler permutations, and zero exact `(DEF, b)` ties on free edges, 29/29 goods
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py`, then recomputed the tie test independently from `run_drain` output
over all 29 goods, and measured how close the keys come to tying.
**Evidence:** `v5measure.py`: "orientation flips, 2 index permutations x 29 goods 0"; "exact (DEF, b)
ties on free edges 0". Independent recount: 2,323 free-edge endpoint pairs over 29 goods, **0** exact
ties. On the float-brittleness question the claim is **not** brittle: the smallest separation on any
free edge is `ΔDEF = 1.294e-05` (silk, `yumen`/`samarkand`), against a double-precision noise floor of
~3.4e-17 on quantities of this magnitude — twelve orders of margin. Four free edges tie exactly on
`DEF` and are separated by `b` (margins 4.9e-03 … 1.1e-01), so the second key component is genuinely
used and is also nowhere near a tie.
*Wording note:* what the measurement permutes is the index component of the priority key, not the
scan order. That is the only scheduling freedom the priority sweep has, so the measurement is the
right one — but "scheduler permutations" invites the stronger reading that the scan sweep is
orientation-invariant, which it is not (145 of 174 runs, above).

---

### X018 — `goods_produced(p) = GP_COEFF · base_production · (1 + Σ local gp modifiers)`, plus local flat goods bonuses
**Status:** PARTIAL
**Method:** Compared §1.3's code block, §2.2 item 4's expression and `scripts/solver.py:province_table()`.
**Evidence:** §2.2 item 4 and `solver.py` both compute `(GP_COEFF·base_production + flat) · (1 + gp_mods)` — flat inside the multiply. §1.3's line reads `GP_COEFF · base_production(p) · (1 + Σ …)` with `# + local flat goods bonuses` appended, which parses as flat added *after* the multiply; §1.3's prose only says flats add "before the price multiply", which is weaker than what the implementation does. The two forms differ whenever a province carries both a flat bonus and a goods-produced percentage. At 1444 they cannot differ: the only goods-produced percentage is `krakow_cloth_hall` (province 262), and 262 carries no flat bonus, so both forms give 10,677.50.
**Should say:** state §2.2's form in §1.3 too — `(GP_COEFF · base_production + flat goods bonuses) · (1 + Σ local goods-produced modifiers)`.

### X019 — `trade_value(p) = goods_produced · price · (1 + Σ local trade-value modifiers)`
**Status:** CONFIRMED
**Method:** Re-implemented the wealth pipeline from `common/prices/00_prices.txt` + a fresh parse of all 3,923 `history/provinces/` files to 1444.11.11, independent of `prov1444.json`.
**Evidence:** Reproduces `solver.py` exactly; world total 10,677.5000.

### X020 — `tax_value(p) = TAX_COEFF · base_tax · (1 + Σ local tax modifiers)`
**Status:** CONFIRMED
**Method:** Same re-implementation.
**Evidence:** Reproduces exactly. The only local tax modifier live at 1444 is `gems` +0.15 (43 provinces).

### X021 — ⚑ The tax tooltip reads `Base: X (Yearly 12·X)` — `Base: 0.49 (Yearly 6.00)` at `base_tax` 6, `Base: 0.16 (Yearly 2.00)` at 2
**Status:** REFUTED (as a schema; the two readings themselves are unchallenged)
**Method:** Arithmetic on the spec's own two data points, cross-checked against X120's truncation rule; province values verified in `history/provinces/223 - Granada.txt` and `1747 - Caceres.txt`.
**Evidence:** 12 × 0.49 = **5.88**, not 6.00. 12 × 0.16 = **1.92**, not 2.00. The parenthetical is not twelve times the displayed figure; it is `base_tax` itself, and the displayed figure is the *truncated* twelfth (X120). The schema `Base: X (Yearly 12·X)` is arithmetically false on both of the spec's own observations, and it contradicts X120 in the same section.
**Should say:** `Base: trunc(base_tax/12) (Yearly base_tax)` — the parenthetical is the untruncated annual value and the `Base` line is its truncated twelfth.

### X022 — ⚑§ The monthly production tooltip's `Trade Value` line is the window's annual `Trade Value` over twelve — 3.52 → `+0.29`
**Status:** UNVERIFIABLE (arithmetic consistent)
**Method:** Arithmetic; the tooltip cannot be re-read without running the game.
**Evidence:** 3.52 / 12 = 0.29333 → 0.29 under either truncation or rounding. Consistent, but one observation on one province, and the divisor 12 is inferred from a single point (any divisor in [12.00, 12.14] fits).

### X023 — ⚑ Measured on two provinces: Garnatah (223, bt 6, bp 4, silk, autonomy 0) and Caceres (1747, bt 2, bp 2, wool)
**Status:** CONFIRMED (province data)
**Method:** Parsed `history/provinces/223 - Granada.txt` and `1747 - Caceres.txt` to 1444.11.11.
**Evidence:** 223: `base_tax` 6, `base_production` 4, `trade_goods` silk, owner GRA. 1747: `base_tax` 2, `base_production` 2, `trade_goods` wool, owner CAS. Both match.

### X024 — ⚑ Only the tooltips' `Base` lines are used; a window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`
**Status:** CONFIRMED (mechanism corroborated from files)
**Method:** `common/ruler_personalities/00_core.txt`; `common/tradegoods/00_tradegoods.txt`.
**Evidence:** `industrious_personality` grants `global_trade_goods_size_modifier = 0.1`, a country-scoped key. The methodological rule follows.

### X025 — ⚑§ Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's monarch held `Industrious`, +10%
**Status:** CONFIRMED (files corroborate every link but the reading)
**Method:** `common/ruler_personalities/00_core.txt` (`industrious_personality` → `global_trade_goods_size_modifier = 0.1`); `common/prices/00_prices.txt` (silk 4.0); `history/countries/GRA - Granada.txt` (grep `personality` → 0 hits).
**Evidence:** 0.2 × 4 = 0.80 goods produced; × silk 4.0 = 3.20; × 1.10 = **3.52** exactly. Granada scripts no ruler personality, so one is rolled at start.

### X026 — ⚑ Ruler personalities are rolled at game start wherever country history scripts none
**Status:** CONFIRMED
**Method:** `history/countries/GRA - Granada.txt` contains zero `personality` tokens; other country files do carry `add_ruler_personality`.
**Evidence:** The premise holds. The engine's roll behaviour is not file-settleable but is not in dispute.

### X027 — ⚑§ `Base 0.49` then `Tax Income Efficiency 125.0%` gives 0.6125, which the window shows as 0.62
**Status:** REFUTED (the stated arithmetic does not produce the stated display)
**Method:** Arithmetic against X120's truncation rule.
**Evidence:** 0.49 × 1.25 = **0.6125**, and truncating to two places gives **0.61**, not 0.62. 0.62 requires *rounding* — but X120, three claims later, says the engine *truncates*. Both cannot hold on this data. The consistent account is that the engine never uses the truncated 0.49: 6 × 0.0833333 = 0.499998, × 1.25 = **0.6249975**, truncated → 0.62. The displayed 0.62 is therefore evidence that the efficiency multiplies a value the engine has *not yet* truncated — which is the opposite of what the sentence is offered to demonstrate ("the engine computes the base from development first and then applies a percentage").
**Should say:** `base_tax 6 → 6 × 0.0833333 = 0.4999… (displayed 0.49); × 125.0% = 0.6249…, displayed 0.62`. The example still supports "modifiers apply after the coefficient"; it does not support 0.6125.

### X028 — Flat goods bonuses add before the price multiply; the tooltip's shape is consistent with that and does not establish it
**Status:** CONFIRMED
**Method:** Read as an epistemic statement; checked it does not over-claim.
**Evidence:** Correctly labelled. Note the tooltip shape it cites also fails to distinguish X018's two orderings, which is the ambiguity X018 leaves open.

### X029 — ⚑ Fifteen 1444 provinces carry a flat goods bonus in the additive block
**Status:** CONFIRMED
**Method:** Independent sweep of `common/great_projects/` (tier ≤ `starting_tier`, empty `can_use_modifiers_trigger`) and of `history/provinces/` undated `add_permanent_province_modifier`, resolved against `common/event_modifiers/`.
**Evidence:** Flat `trade_goods_size` on exactly **15** counted provinces: 8, 684, 1821, 1822, 2145 (great projects) and 6, 362, 363, 370, 371, 387, 542, 2151, 2316, 4316 (permanent modifiers). Matches `solver.py`'s `MON_FLAT ∪ PERM_FLAT`.

### X030 — Locality test: local iff its value depends only on the province's own attributes — terrain, climate, trade good, development, buildings — and on no country's state
**Status:** PARTIAL
**Method:** Applied the test as written to every source §1.3 then classifies as local.
**Evidence:** The enumerated attribute list does not cover four of the sources the table classifies as **local**: `devastation`, `occupied`, `under_siege`, `prosperity` are none of terrain / climate / trade good / development / buildings. Worse, `occupied` and `under_siege` are facts about *which country's army holds the province*, so the test's second clause ("on no country's state") excludes them, while the table admits them ("yes, all are province state"). The test must therefore be read as "province state" rather than as its own enumerated list, and the two readings disagree on exactly the rows §3.3 and §2.8's war rows lean on.
**Should say:** define local as depending only on the province's own record — terrain, climate, trade good, development, buildings **and province status fields (devastation, occupation, siege, prosperity)** — and on no country's *attributes*; say explicitly that occupation status is treated as a province field.

### X031 — Wealth test: enters wealth iff it modifies `goods_produced`, `price` or `tax_value`; a modifier must pass both
**Status:** CONFIRMED
**Method:** Enumerated the operative keys and checked the model reads exactly them.
**Evidence:** The four keys are `trade_goods_size`, `trade_goods_size_modifier`, `trade_value_modifier`, `local_tax_modifier`; `solver.py` reads exactly these. One structural gap: the model has no flat *tax* term, so a local flat `tax_income` source could not be represented. I swept `tax_income` across the install — `common/colonial_regions` (1 file), `common/event_modifiers` (3), `common/province_triggered_modifiers` (1) — and none is live on a counted province with no owner input, so the gap costs nothing at 1444.

### X032 — The trade-good data model is one instance of the locality test, not the test itself
**Status:** CONFIRMED
**Method:** Parsed `common/tradegoods/00_tradegoods.txt` in full.
**Evidence:** All 30 goods carry a `province` block (province-scoped keys only) and a `modifier` block, and every one of the 30 `modifier` blocks is country-scoped (`global_*`, `prestige`, `legitimacy`, `trade_efficiency`, tech-cost, `num_accepted_cultures`, …). `coal`'s is `global_trade_goods_size_modifier = 0.1` — a wealth key in country scope, exactly the case the distinction exists for.

### X033 — The tests are applied to the whole install, not to one file
**Status:** PARTIAL
**Method:** Ran the whole-install sweep myself (see X035).
**Evidence:** The sweep is real and mostly right, but it is not whole-install: it misses `common/static_modifiers/`'s `provincial_production_size`, misses the second non-owner-gated `province_triggered_modifier`, gets the centre-of-trade count wrong, gets the great-project denominator wrong, and mis-states the buildings row. See X035, X040, X043, X046, X050, X055.

### X034 — v4.0 stated the rule and then swept only `common/tradegoods/`, concluded "exactly two", and missed sixteen provinces
**Status:** CONFIRMED
**Method:** `../v4-owner-agnostic/per-good-trade-spec.md:531`.
**Evidence:** v4.0 reads "the local modifiers that enter are exactly two — `gems` (+15% tax, 43 provinces) and `incense`…". Sixteen provinces gain a great-project or permanent-modifier term in v5.0. (But see X112: those sixteen are not all "beyond the two trade goods".)

### X035 — The vanilla set of local-and-entering modifiers is: `gems`, `incense`, great-project `province_modifiers`, `add_permanent_province_modifier`, and the five province-state static modifiers
**Status:** REFUTED (the enumeration is incomplete and miscounts)
**Method:** Exhaustive install sweep. For each of the four wealth keys I listed every directory in the install granting it at a word boundary (`grep -rlE "(^|[[:space:]{])KEY[[:space:]]*="` over all `*.txt` under the install root), then parsed each source and classified it against both tests.
**Evidence:** The complete set of directories granting a wealth key is `common/{buildings, event_modifiers, great_projects, holy_orders, province_triggered_modifiers, state_edicts, static_modifiers, tradecompany_investments, tradegoods}`. `holy_orders`, `state_edicts` and `tradecompany_investments` are owner actions. That leaves **six** sources that pass both tests, not four:
1. `gems` `local_tax_modifier = 0.15` — in the table
2. `incense` `trade_value_modifier = 0.1` — in the table
3. great-project `province_modifiers` — in the table
4. undated `add_permanent_province_modifier` — in the table
5. **`common/static_modifiers/`'s `provincial_production_size = { trade_goods_size = 0.2 }`** — a province-scaled static modifier, local by the test, entering `goods_produced` on *every* province. Not in the table. It is `GP_COEFF` itself (see X118/X119).
6. **`common/province_triggered_modifiers/`'s `cerro_rico_modifier` and `stora_kopparberget_modifier`** — the only 2 of 90 PTMs whose gate is not an owner condition (both `potential = { NOT = { has_dlc = "Leviathan" } }`, both with a true trigger). §1.3 discusses `stora_kopparberget` in its DLC paragraph, but the enumeration sentence carries no `province_triggered_modifiers` category at all, and `cerro_rico_modifier` (province 795, `trade_goods_size = 3.0`) appears nowhere in the document.
Also: "the **five** province-state static modifiers" counts *values*, not modifiers — there are **four** (`devastation`, `occupied`, `under_siege`, `prosperity`); `occupied` contributes two keys.
**Should say:** six sources — the two trade goods, great-project `province_modifiers`, undated `add_permanent_province_modifier`, `province_triggered_modifiers` not gated on an owner condition, and the **four** province-state static modifiers — plus `provincial_production_size`, which the model already carries as `GP_COEFF`.

### X036 — ⚑ `gems` `local_tax_modifier = 0.15` is live on 43 provinces at 1444
**Status:** CONFIRMED
**Method:** Independent parse of all 3,923 `history/provinces/` files to 1444.11.11; counted `trade_goods == gems` among owner-and-`is_city=yes` provinces.
**Evidence:** 43. Key value verified in `common/tradegoods/00_tradegoods.txt`.

### X037 — ⚑ `incense` `trade_value_modifier = 0.1` is live on 29 provinces at 1444
**Status:** CONFIRMED
**Method:** Same.
**Evidence:** 29.

### X038 — ⚑ Great-project `province_modifiers` where `can_use_modifiers_trigger` is empty: 6 provinces
**Status:** CONFIRMED
**Method:** Parsed both files in `common/great_projects/`, filtered to `date ≤ 1444.11.11` and empty `can_use_modifiers_trigger`, took `province_modifiers` at `starting_tier`.
**Evidence:** Exactly six projects on six provinces: `falun_copper_mine` (8), `grand_canal_1` (684), `grand_canal_2` (1822), `grand_canal_3` (2145), `grand_canal_4` (1821), `krakow_cloth_hall` (262). Values match `solver.py` exactly.

### X039 — ⚑ `add_permanent_province_modifier` in the undated province-history block: 10 provinces
**Status:** CONFIRMED
**Method:** Parsed every undated `add_permanent_province_modifier` in `history/provinces/` (~70 distinct names) and resolved each against `common/event_modifiers/`.
**Evidence:** Of ~70 names, exactly six grant a wealth key, on exactly **10** counted provinces. The other ~64 grant only `province_trade_power_value` (56 uses), `picture` (54), `prestige`, `legitimacy`, `tolerance_own`, `advisor_pool`, `devotion`, `harmonization_speed`, karma keys, `monthly_splendor`, `local_institution_spread` — none a wealth key. I also checked *dated* blocks ≤ 1444.11.11 (0 wealth-key hits) and `add_province_modifier` (0 hits), so restricting to the undated block loses nothing.

### X040 — ⚑ The static province-state modifiers are `devastation` −2, `occupied` −0.5 and −0.5, `under_siege` −0.25, `prosperity` +0.25; all local, all enter `goods_produced` **and** `tax_value`, all zero at 1444
**Status:** REFUTED
**Method:** (a) Read the four blocks in `common/static_modifiers/00_static_modifiers.txt` in full (lines 433–467). (b) Parsed the `provinces={…}` block of `VANILLA_start.eu4` (`meta` confirms `date=1444.11.11`, Leviathan enabled) for `devastation`, `unrest` and `prosperity` values.
**Evidence — two separate failures.**
*(1) "all are zero at the 1444 start" is false.* The shipped 1444 start carries **nonzero `devastation` on 11 provinces**, ten of them counted: Prague (266) 50, Eger (2967) 20, Budejovice (2968) 50, Hradecko (2970) 50, Erz (1771) 20, Olomouc (4237) 20, Pardubice (4724) 50, Jindrichuv Hradec (4725) 50, Ostrava (4726) 20, Plsen (267) 20 — Bohemia's Hussite-war devastation, plus Brno (265), which the model excludes for the separate reason in S1b. It is not in `history/provinces/` (0 files mention it): it is applied by `on_startup` → `on_startup_effect` (`common/scripted_effects/01_scripted_effects_for_on_actions.txt:4795`) → `country_event = { id = flavor_boh.15 }` (`events/flavorBOH.txt:938`), whose `immediate/hidden_effect` runs `bohemia_area = { add_devastation = 50 }`, `erzgebirge_area = { add_devastation = 20 }`, `moravia_area = { add_devastation = 20 }` — matching the save's values and provinces exactly. It is in the game state, which is what "at the 1444 start" means. `unrest` is likewise nonzero on 60 provinces (3–20). Only `prosperity` is genuinely zero everywhere. The model therefore prices ten Bohemian provinces at full `goods_produced` when the engine does not, and — more to the point — §1.3's sweep never looked at the start state, only at the files.
*(2) "all enter `goods_produced` and `tax_value`" is false.* **Only `occupied` carries a tax key**:
- `occupied` → `local_tax_modifier = -0.5` **and** `trade_goods_size_modifier = -0.5`
- `under_siege` → `trade_goods_size_modifier = -0.25` only
- `devastation` → `trade_goods_size_modifier = -2` only (no `local_tax_modifier` anywhere in the block)
- `prosperity` → `trade_goods_size_modifier = 0.25` only
So "all enter `goods_produced` and `tax_value`" is false for three of the four. This matters beyond bookkeeping: §3.3 and §2.8's "Major war in China" row both rest on these biting, and three of them bite on the production side only — a razed or besieged province keeps its full `tax_value` in the model *and* in the game.
Also worth a ruling the spec does not give: `unrest` (`local_tax_modifier = -0.02` per point) is a province field by exactly the reasoning that admits `devastation`, it is **nonzero on 60 provinces at 1444**, and it appears nowhere in §1.3.
**Should say:** all four enter `goods_produced`; only `occupied` also enters `tax_value`; and `devastation` is **not** zero at 1444 — ten counted Bohemian provinces carry 20–50.

### X041 — `glass` `local_production_efficiency = 0.1` is local but does not enter wealth
**Status:** CONFIRMED
**Method:** `common/tradegoods/00_tradegoods.txt`, glass `province` block.
**Evidence:** `local_production_efficiency = 0.1`; not one of the four keys wealth reads.

### X042 — ⚑ `chinaware` carries `local_autonomy = -0.1`; local, does not enter wealth
**Status:** CONFIRMED
**Method:** Same file.
**Evidence:** `chinaware` `province = { local_autonomy = -0.1 }`.

### X043 — ⚑ 361 provinces carry a centre of trade at 1444, and no CoT level grants any of the four keys
**Status:** PARTIAL — the substantive half is confirmed, the count is wrong
**Method:** (a) Parsed `common/centers_of_trade/00_centers_of_trade.txt` in full, including `province_modifiers`, `state_modifiers` and `global_modifiers` for all six levels. (b) Counted `center_of_trade` from `history/provinces/` to 1444.11.11, and independently from the `gamestate` entry of `VANILLA_start.eu4`.
**Evidence:** No CoT level grants any of the four keys — the six levels grant only `province_trade_power_value`, `local_development_cost`, `local_institution_spread`, `local_sailors_modifier`, `local_manpower_modifier`, `allowed_num_of_buildings`, `navy_tradition_decay`. The near-miss is real and worth recording. But the count is **363**, not 361, from both sources independently (237 level-1 / 121 level-2 / 5 level-3). Restricted to the 2,452 counted provinces it is **324**. 361 is neither figure.
**Should say:** 363 provinces carry a centre of trade (324 of them counted).

### X044 — ⚑ `production_leader` `trade_goods_size_modifier = 0.10` is not local
**Status:** CONFIRMED
**Method:** `common/static_modifiers/00_static_modifiers.txt:1256–1257`.
**Evidence:** `production_leader = { trade_goods_size_modifier = 0.10 }`. Which country leads a good's production is a country fact; correctly excluded.

### X045 — ⚑ `bonus_from_merchant_republics` (`eu4.exe:0x1cc7128`) is not local
**Status:** PARTIAL (classification right, provenance wrong)
**Method:** `common/static_modifiers/00_static_modifiers.txt:1265–1266`.
**Evidence:** The modifier is a **shipped file value**, not a binary string: `bonus_from_merchant_republics = { trade_goods_size_modifier = 0.5 }`, with a sibling the spec does not mention, `bonus_from_merchant_republics_for_trade_league_member = { trade_goods_size_modifier = 1 }`. The classification (not local — set by which neighbouring countries hold those government forms) is correct. Sourcing a file value to a binary address is exactly the provenance weakening §3.16 warns about, and it costs the value: the spec never says the bonus is +50%, live around every 1444 merchant republic, which is the largest single non-local goods-produced term on the map.
**Should say:** cite `common/static_modifiers/00_static_modifiers.txt`, give the value (+0.5), and name the trade-league sibling (+1.0).

### X046 — ⚑ Buildings are local by the test and empty at 1444 — no province's start state carries a temple, workshop or manufactory
**Status:** PARTIAL
**Method:** Parsed all 36 building types from `common/buildings/00_buildings.txt` and checked each against every province's 1444.11.11 state; cross-checked with `grep -rlE "^\s*NAME\s*=\s*yes" history/provinces/` and against the save.
**Evidence:** The three *named* buildings are absent (temple 0, workshop 0, manufactory 0 — also marketplace 0, courthouse 0, dock 0, cathedral 0, university 0). But buildings are **not empty at 1444**: `fort_15th` is present on **251 counted provinces** (256 history files, 502 raw occurrences in the save counting its history sub-block) and `shipyard` on province 112 (Venezia). Neither grants a wealth key (`fort_15th → fort_level = 2`; `shipyard → naval_forcelimit, ship_recruit_speed, local_ship_repair, …`), so the wealth conclusion survives untouched — but the stated fact does not. The three buildings that *would* enter are `temple` (`local_tax_modifier = 0.4`), `cathedral` (0.6) and `manufactory` (`trade_goods_size = 1.0`).
**Should say:** "no province's start state carries a building that grants a wealth key — the only 1444 buildings are `fort_15th` (251 provinces) and one `shipyard`, and neither does."

### X047 — ⚑ `terrain.txt` and the climate static modifiers grant only [nine listed keys], none of which wealth computes
**Status:** PARTIAL
**Method:** Parsed all 20 terrain categories in `map/terrain.txt` and all nine climate blocks in `00_static_modifiers.txt`, taking the union of every key granted.
**Evidence:** Terrain's union is exactly the listed set (`movement_cost` ×19, `supply_limit` ×16, `local_development_cost` ×16, `nation_designer_cost_multiplier` ×16, `defence` ×9, `allowed_num_of_buildings` ×3, `local_defensiveness` ×3). Climate's union adds three keys **not** in the spec's list: `migration_cost` (normal_winter 0.1, severe_winter 0.2) and `local_hostile_movement_speed` / `local_friendly_movement_speed` (the three monsoons); it also grants `supply_limit_modifier` rather than `supply_limit`. The conclusion — none of them is a wealth key — holds.
**Should say:** add `migration_cost` and the two movement-speed keys, or replace the enumeration with "no key wealth reads".

### X048 — ⚑ A great project contributes the `province_modifiers` accumulated up to its `starting_tier` when `can_use_modifiers_trigger` is empty
**Status:** PARTIAL — right answer, wrong rule
**Method:** Printed the full tier ladders of `falun_copper_mine`, `grand_canal_1`, `krakow_cloth_hall` and `tenochtitlan`.
**Evidence:** Tiers are **absolute, not cumulative**: `falun_copper_mine` gives `trade_goods_size` 3.0 at tier 1, **6.0** at tier 2 and **9.0** at tier 3 — 6.0 replaces 3.0, it does not add to it; `tenochtitlan` gives `trade_goods_size_modifier` 0.25 / 0.33 / 0.5. Accumulating gives the right answer here only because every tier-0 `province_modifiers` block is empty and all six qualifying projects have `starting_tier = 1`. Applied to a `starting_tier = 2` project — 24 of the 138 live projects are at tier 2 — the stated rule over-counts, and it would over-count on any modded map.
**Should say:** "contributes the `province_modifiers` **of** its `starting_tier`".

### X049 — Tiers reached after the start date are owner spending and are out of scope
**Status:** CONFIRMED (stipulation, coherent)
**Method:** Consistency check against X053.
**Evidence:** Coherent with the tier line and with the treatment of development.

### X050 — ⚑ 85 of the 130 great projects live at 1444 are gated on a country's culture, religion, government or flags
**Status:** REFUTED
**Method:** Parsed both `common/great_projects/` files independently; counted projects with `date ≤ 1444.11.11` and non-empty `can_use_modifiers_trigger`; then tried every alternative denominator I could construct.
**Evidence:** **141** great projects are defined; **138** are live at 1444 (the three excluded are `kiel_canal` 1895, `suez_canal` 1869, `panama_canal` 1914 — the whole of `00_great_projects.txt`). Of the 138, **88** have a non-empty `can_use_modifiers_trigger` and 50 are empty. **130 is not a project count — it is the number of distinct `start` provinces**: eight provinces host two live projects each (97, 112, 151, 183, 295, 361, 1821, 2690), and 138 − 8 = 130. On that per-province basis the gated count is 81 (one project per province, first- or last-wins alike) or 83 (any project on the province gated); restricting to projects on counted provinces gives 84 of 127. **No reading yields 85 of 130** — the numerator and denominator come from different denominators.
**Should say:** "88 of the 138 great projects live at 1444 are gated on a country's culture, religion, government or flags."

### X051 — ⚑ Six projects carry a key wealth reads: `falun_copper_mine` (8, `trade_goods_size` 3.0), `krakow_cloth_hall` (262, `trade_goods_size_modifier` 0.10), and the four Grand Canal provinces (684, 1821, 1822, 2145; `trade_goods_size` 0.5 and `trade_value_modifier` 0.1 each)
**Status:** CONFIRMED
**Method:** The sweep of X038.
**Evidence:** Exactly those six, with exactly those provinces and values. Three *gated* projects would otherwise qualify and are correctly excluded: `duomo_milano` (104, `local_tax_modifier` 0.25, religion-group gate), `swayambhunath` (557, 0.25, Buddhist gate), `tenochtitlan` (852, `trade_goods_size_modifier` 0.33 at tier 2, culture gate).

### X052 — Province 1821 is the richest single province in the game
**Status:** CONFIRMED
**Method:** Computed `wealth(p)` for all 2,452 counted provinces from my own province table.
**Evidence:** 1821 (Nanjing, silk, bt 15 / bp 15, Grand Canal): **30.400**. Next: 542 Golconda 25.750, 684 Hangzhou 24.760, 1816 Beijing 19.500, 685 Yangzhou 19.200.

### X053 — The `starting_tier` is the right line and "owner action" is not
**Status:** CONFIRMED
**Method:** Argument check.
**Evidence:** The reductio is sound: development is an owner action, so an "owner action" rule would exclude `base_production`, which is wealth's primary input.

### X054 — ⚑ The permanent province modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6), `icelanding_fisher_sea` (370, 371), `diamond_mines_of_golconda_modifier` (542), `jingdezhen_kilns` (2151), `coffea_arabica_modifier` (387), all flat `trade_goods_size`
**Status:** CONFIRMED
**Method:** The sweep of X039, resolving each name in `common/event_modifiers/00_event_modifiers.txt`.
**Evidence:** Exactly those six names on exactly those ten provinces, and each grants exactly one key, a flat `trade_goods_size`: granary 2.0, skanemarket 2.0, icelanding_fisher_sea 1.0, diamond_mines 4.0, jingdezhen_kilns 2.5, coffea_arabica 3.0. Matches `solver.py`'s `PERM_FLAT` value for value.

### X055 — ⚑ `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants `trade_goods_size = 5.0` on province 8
**Status:** PARTIAL — true, and not the only one
**Method:** Parsed all 90 blocks of `common/province_triggered_modifiers/00_modifiers.txt`, extracting `potential` and `trigger` for every block granting a wealth key; cross-referenced against `add_province_triggered_modifier` in `history/provinces/`.
**Evidence:** The claim is exactly right for province 8. But exactly **two** of the 90 PTMs are gated on something other than an owner condition, and both carry the same DLC gate:
- `stora_kopparberget_modifier` — `potential = { NOT = has_dlc "Leviathan" }`, `trigger = { always = yes }`, `trade_goods_size = 5.0`, attached in `history/provinces/8-Dalaskogen.txt`.
- **`cerro_rico_modifier`** — `potential = { NOT = has_dlc "Leviathan" }`, empty trigger, `trade_goods_size = 3.0`, attached in `history/provinces/795 - Potosi.txt` (owner CRA, `is_city = yes` — a counted province). Its Leviathan counterpart, the `potosi` monument, has `starting_tier = 0` with an **empty** tier-0 `province_modifiers`, so with Leviathan the province gets nothing.
The numerical effect of the omission is nil, but not for the reason the spec would give: province 795's trade good is `gold`, whose `base_price` is 0.0, so any `trade_goods_size` bonus there contributes exactly 0 to `trade_value`.
**Should say:** name both, and note that `cerro_rico`'s effect is annulled by gold's zero price rather than by the DLC.

### X056 — ⚑ With Leviathan the project applies and gives 3.0; without it the project does not exist and the modifier gives 5.0
**Status:** PARTIAL (files support the values; "does not exist" is an engine claim)
**Method:** `common/great_projects/01_monuments.txt` (`falun_copper_mine`, `starting_tier = 1`, tier-1 `trade_goods_size = 3.0`) and `common/province_triggered_modifiers/00_modifiers.txt`.
**Evidence:** Both values verified. Whether the monument system is inert without Leviathan is not settleable from the shipped files: the monument definitions ship in the base install and carry no `has_dlc` gate of their own — the gating is in the engine. The PTM's `NOT = has_dlc "Leviathan"` potential is strong circumstantial evidence (the two are plainly designed as alternatives), but it is inference, not observation, and §3.16's own rule ("an engine fact sourced to a string is settled only when something observes the behaviour") applies to it.

### X057 — Every wealth figure was measured with Leviathan installed
**Status:** CONFIRMED (stipulation, and materially true)
**Method:** `scripts/README.md` states it; `solver.py`'s `MON_FLAT[8] = 3.0` is the Leviathan branch.
**Evidence:** Consistent. The DLC axis is real: without Leviathan province 8 would carry 5.0 instead of 3.0, and province 795 would gain 3.0 (worth 0 ducats).

### X058 — glass and chinaware are the whole of the rule-versus-vocabulary tension
**Status:** REFUTED
**Method:** The X035 sweep.
**Evidence:** They are the whole of it *within `common/tradegoods/`* — which is precisely the file v5.0 says the rule exists to stop the author treating as the whole install. Outside it the same tension recurs and is never adjudicated: `provincial_production_size` is local and *does* enter, and is not in the table; `intolerance` grants both `local_tax_modifier 0.1` and `trade_goods_size_modifier 0.10` but is scaled by a country's religious tolerance; `unrest` grants `local_tax_modifier -0.02` off a province field driven by country state; `local_autonomy_multiplicative` and `local_autonomy_trade_company_multiplicative` each grant `local_tax_modifier -1.0`; `seat_in_parliament` grants 0.15; `native_assimilation` grants `trade_goods_size 0.05`; `expanded_infrastructure` grants both `local_tax_modifier 0.1` and `trade_goods_size_modifier 0.05`. Each needs the same "local but excluded / not local" ruling glass and chinaware get by name, and none gets one.
**Should say:** drop "the whole of", or scope the sentence to the trade-good tables.

### X059 — Excluded by the rule as not local: `Reform Iqta` (+5%, government), `Clergy` (+5%, estate), national ideas (+15%), production efficiency from technology (+2%), the owner's goods-produced modifiers
**Status:** PARTIAL
**Method:** `common/government_reforms/01_government_reforms_monarchies.txt` (`iqta`); `common/estates/01_church.txt`.
**Evidence:** `iqta = { vassal_income = 0.33, global_tax_modifier = 0.05 }` — the +5% and its country scope check out exactly. The Clergy/Church figure does not: the estate's shipped `global_tax_modifier` values are +0.2 / +0.2 / −0.1 by loyalty-and-influence band, not +5%; the +5% must come from a crown-land or privilege term the claim does not name. Every item is correctly classified as not local; one of the five figures is not traceable to the file the claim implies.

### X060 — ⚑ `Core` (+75%) and `City` (+25%) are the two that are not excluded, because they are already inside `TAX_COEFF`
**Status:** CONFIRMED
**Method:** `common/static_modifiers/00_static_modifiers.txt`: `city = { local_tax_modifier = 0.25 … }` (line 99), `core = { local_tax_modifier = 0.75 … }` (line 334).
**Evidence:** Exactly 0.25 and 0.75. Two siblings the spec does not mention, `colonial_core` and `territory_core`, are also 0.75 — harmless, since the model treats every counted province as cored, and `non_core` carries no tax key at all (`local_missionary_strength = -0.02` only).

### X061 — ⚑§ The tax multiplier is the sum of the itemised percentages: Garnatah 75+25+5+5+15 = 125%, Caceres 75+25+5 = 105%
**Status:** CONFIRMED (arithmetic and the two file-checkable terms)
**Method:** Arithmetic; `core` / `city` values from the file.
**Evidence:** Both sums are right and both are consistent with `core + city = 100%` being the identity multiplier. The engine reading itself still rests on one session.

### X062 — ⚑ A cored city carrying nothing else sums to exactly 1.00 and yields `base_tax` ducats a year — the reference condition `TAX_COEFF = 1.0` was measured at
**Status:** CONFIRMED
**Method:** File values plus the X061 arithmetic.
**Evidence:** 0.75 + 0.25 = 1.00 exactly, from the shipped file. Worth noting against §2.3: this makes `TAX_COEFF = 1.0` *derivable* from `00_static_modifiers.txt` plus the 1/12 monthly split, not only measurable from a tooltip.

### X063 — Every province the model counts is a city and is treated as cored; carrying either term again would double-count
**Status:** CONFIRMED (as stated — but the converse fails, see below)
**Method:** The province table (2,452 = owner ∧ `is_city = yes` from `history/provinces/`); the `non_core` block; compared against the save's live province records.
**Evidence:** All 2,452 counted provinces have `is_city = yes` by construction, so the claim as written holds. Treating them all as cored is a stipulation with no tax cost, since `non_core` grants no tax key (`local_missionary_strength = -0.02` only).
**Note the converse, which the section relies on and which fails.** In `VANILLA_start.eu4` every owned province is `is_city = yes` — **2,472** of them. The model counts 2,452. The twenty dropped are exactly those whose *history file* never writes the flag: nineteen native and small-tag provinces plus **province 265 (Brno)**, whose vanilla file carries the line **commented out** (`#is_city = yes`) while the province is a cored, HRE, `base_tax` 3 / `base_production` 3 Bohemian city. §1.3's stated reason for the filter is that "an unowned province produces nothing the trade system can move" — none of the twenty is unowned. Total omitted wealth 34.75 ducats, 0.325% of the world's 10,677.50.

### X064 — Repricing the 45 owned latent-coal provinces to coal flips 29 of 159 `Φ_w` edges
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py` section F; then re-derived independently in `_audit_a_main.py`
(own scan of `history/provinces/*` for `latent_trade_goods = { … coal … }`, own repricing, own
`Φ_w` solve). Also stress-tested the repricing formula: checked whether any of the 45 carries a
great-project flat `trade_goods_size`, `MON_TVMOD`, or `MON_GPMOD`, and recomputed with the
`gems` `local_tax_modifier` correctly *removed* on repricing (which `v5measure.py` leaves in).
**Evidence:** 58 latent-coal province files; 45 of them owned + `is_city` + in a trade node;
`Φ_w` edge flips = **29 of 159** under both the spec's formula and the gems-tax-corrected one.
All 58 are in a trade node; 0 of the 58 declare coal only inside a dated history block, so the
1444 reading is right. Coal `base_price = 10.0` is the unique maximum in `00_prices.txt`, so
§1.5's "highest in vanilla" also holds. None of the 45 carries a flat `trade_goods_size` or a
trade-value province modifier, so the simplified repricing is exact for 44 of 45 and the one
exception (pid 262, `krakow_cloth_hall`, +10% goods produced) is carried correctly through
`r["gp"]`. Post-activation sinks become `{english_channel, hangzhou, krakow, sevilla}`.

---

### X065 — The `Φ_w` sink count is set by `α_Φ`; only the sinks' locations are emergent
**Status:** REFUTED
**Method:** `_audit_a_misc.py` — held `α_Φ = 1.5` fixed and varied only the world, using the
same wealth-perturbation machinery the spec itself uses in §1.6.
**Evidence:** at fixed `α_Φ = 1.5` the sink **count** takes the values 1, 2, 3, 4 and 5:

| world (α_Φ = 1.5 throughout) | count | sinks |
|---|---|---|
| 1444 baseline | 1 | `hangzhou` |
| Europe ×1.02 | 4 | `doab, english_channel, hangzhou, wien` |
| Europe ×1.10 | 5 | `doab, english_channel, gulf_of_siam, hangzhou, wien` |
| Europe ×1.56 | 2 | `english_channel, rheinland` |
| `hangzhou` top province ×5 | 4 | `doab, genua, gulf_of_siam, hangzhou` |
| `hangzhou` top province ×10 | 3 | `genua, gulf_of_siam, hangzhou` |
| coal activation (X064) | 4 | `english_channel, hangzhou, krakow, sevilla` |

Every one of these is a measurement the spec itself reports (X086, X087, X101, X064), so the
claim is refuted by the section it lives in. It is also contradicted head-on by X127 ("the end
count … follows the wealth field **and** `α_Φ`") and by X085 ("one sink at 1444 is a snapshot …
holding α_Φ = 1.5 and moving nothing else").
**Should say:** the count is a step function of `α_Φ` *at a fixed world state*; it is **not**
determined by `α_Φ` alone — both the count and the locations move with the wealth field. The
correct contrast with v2.0–v4.0 is not "count stipulated / locations emergent" but "the count is
*sensitive* to a stipulated constant as well as to the world, which is why §2.3 must record `α_Φ`
as a design decision about end counts."

---

### X066 — v2.1 chose 1.5 with a target count in view; §2.3 withdraws that calibration
**Status:** CONFIRMED
**Method:** Read §2.3 of the spec (lines 730–737) directly; read §1.6 lines 342–348.
**Evidence:** §2.3 reads "**Its stated calibration is withdrawn.** v2.1 through v4.0 said 1.5 was
'calibrated so the 1444 start yields the two-sink hangzhou/english_channel map'; on the corrected
wealth field of §1.3 it does not yield that map". `audit_alpha.py` re-run confirms the historical
fact behind the withdrawal: on the v4.0 (uncorrected) field α = 1.5 gives
`['english_channel','hangzhou']`; on the corrected field it gives `['hangzhou']`.
*Note:* the second half of the claim ("the ground on which 1.5 is retained is the band table")
is an accurate description of what the document now says, but that ground is itself defective —
see X078 and X083.

---

### X067 — What the world state moves is *where* the sinks are and how the map drains to them
**Status:** PARTIAL
**Method:** Same measurements as X065; read §3.1 goal 1 (spec line 917).
**Evidence:** §3.1's first goal is "World responsiveness. Trade direction follows the world's
current state … A horde razing `hangzhou` moves the sink because the wealth moved." The
measurements do show locations moving (`hangzhou` → `english_channel`/`wien`/`rheinland`/`genua`
under Europe scaling). But the world state demonstrably moves the **count** too (1→2→3→4→5 at
fixed `α_Φ`), so the exclusive framing "*where* the sinks are and *how the map drains*" is false
as a contrast.
**Should say:** drop the implied exclusivity — "what the world state moves is where the sinks are,
how many there are, and how the map drains toward them." That is *more* supportive of §3.1 goal 1,
not less, so nothing in the design rests on the narrower wording.

---

### X068 — Identical orientation at ×1 and above; 16 edge flips at ×10⁻², 83 at ×10⁻⁶
**Status:** CONFIRMED
**Method:** `_audit_a_main.py` — solved `run_drain(b_w · s)` for s ∈ {10⁶, 10², 10, 1, 10⁻², 10⁻⁴, 10⁻⁶}
and diffed each orientation against the ×1 orientation.
**Evidence:** flips = 0 at ×10⁶, ×10², ×10 and ×1; **16** at ×10⁻²; 19 at ×10⁻⁴; **83** at ×10⁻⁶.
Sink set stays `['hangzhou']` at every scale, which is exactly the spec's own caveat ("the
orientation degrades while the sink set happens to survive").

---

### X069 — 1444's `b_w` has largest magnitude 0.0227
**Status:** CONFIRMED
**Method:** `_audit_a_main.py`, `b_w = 1/N − c_w(1.5)`.
**Evidence:** `max|b_w| = 0.022667` (attained at `hangzhou`, the most negative entry;
`min b_w = −0.022667`). Rounds to 0.0227.

---

### X070 — One sink `hangzhou`; `c_w` rank 1, raw node-wealth rank 10, `english_channel` 1st
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py` §D and `phiw3.py`; independently recomputed both rank vectors in
`_audit_a_main.py`.
**Evidence:** sinks `['hangzhou']`; `c_w(1.5)` rank 1 (0.03517); node wealth 245.0, rank **10**;
`english_channel` node wealth **316.6**, rank 1. Top-10 node wealth:
english_channel 316.6, gulf_of_siam 299.2, genua 296.0, malacca 295.9, mexico 294.4, nippon 293.6,
sevilla 266.5, rheinland 251.8, champagne 247.8, hangzhou 245.0 — consistent with X159's readings.

---

### X071 — v2–v4's two-sink result came from a field missing the sixteen §1.3 provinces
**Status:** CONFIRMED
**Method:** Ran `audit_alpha.py`, which solves the same α grid on both the v4.0 field
(`wealth(False)`, no great-project / permanent-modifier terms) and the corrected field.
**Evidence:** at α = 1.5 the v4.0 field gives `['english_channel','hangzhou']`; the corrected
field gives `['hangzhou']`. The difference set is 15 provinces carrying a flat `trade_goods_size`
(5 great projects, 10 permanent province modifiers) plus pid 262's `krakow_cloth_hall` goods
modifier = **16** provinces, matching §3.13's "fifteen … flat" plus the one multiplier.

---

### X072 — Phase 1 selects `hangzhou` directly: 0 promotions and 0 fallbacks
**Status:** CONFIRMED
**Method:** `v5measure.py` §D; re-derived the Phase 0/1/2 decomposition in `_audit_a_misc.py`.
**Evidence:** Phase-1 selection = `['hangzhou']`; promotions `[]`, fallbacks `[]`.
Phase 1 internals: HHI = 0.8179 over 4 demander clusters → k = 1, and the heaviest demander of the
dominant cluster is `hangzhou`. The stall branch never runs.

---

### X073 — Seven sources, all in the bottom half (`c_w` ranks 52–79), mean degree 3.0 vs 4.0
**Status:** CONFIRMED
**Method:** `v5measure.py` §D and `phiw3.py` V216 block.
**Evidence:** sources = `kongo, patagonia, james_bay, mississippi_river, chengdu, australia, tunis`
with `c_w` ranks **53, 79, 75, 70, 52, 66, 56** → min 52, max 79, all ≥ 41 of 80, so all are in the
bottom half. Mean degree of the seven = **3.00**; map mean degree = **3.98** (spec's "4.0").
The spec's own withdrawal of "cul-de-sacs" is also supported: only 3 of 7 have degree 2.

---

### X074 — Every node drains to the sink; acyclic; 159/159; 0 flips and 0 sink changes at ±1%, 5 seeds
**Status:** CONFIRMED
**Method:** `v5measure.py` §D (seeds 1000–1004), then a harder test in `_audit_a_misc.py` with a
different seed family and larger amplitudes.
**Evidence:** acyclic True, 159 of 159 edges oriented, order-descending violations 0.
Noise: 0 flips / 0 sink-set changes at ±1% over the spec's 5 seeds; **0 flips / 0 sink-set changes
at ±1% over 40 fresh seeds**, and still 0/0 at ±2% over 20 seeds. It only breaks at ±5%
(42 flips, 3 of 20 seeds change the sink set). The claim is if anything understated.

---

### X075 — Φ_w agreement 52.5% (51.5% value-weighted) vs Φ_ord's 60.3% — a gap of 7.8 points
**Status:** CONFIRMED
**Method:** `v5measure.py` §D; recomputed both operators' agreement under **both** weightings in
`_audit_a_main.py` so the like-for-like question could be settled.
**Evidence:** over the same 4611 edge-good pairs —

| | unweighted | value-weighted |
|---|---|---|
| `Φ_w` | **52.5%** (2421/4611) | **51.5%** |
| `Φ_ord` | **60.3%** (2779/4611) | 59.9% |

Gap unweighted = **7.76 pts** → "7.8 points", and it *is* like-for-like (60.3 unweighted against
52.5 unweighted). The value-weighted gap is 8.45 pts; the mixed pair 60.3 − 51.5 = 8.78 is not a
comparison the spec makes. *Presentational risk only:* because §1.6 and §3.9 print 52.5% and 51.5%
adjacently but give only one figure for `Φ_ord`, a reader can subtract the wrong pair. Adding
`Φ_ord`'s 59.9% would close that.

---

### X076 — `Φ_ord`'s edge-good agreement is 60.3% under the deterministic sweep
**Status:** CONFIRMED
**Method:** As X075; the `Φ_ord` orientation is `Σ_g V_g·order_g` compared pairwise, with all 29
per-good graphs produced by the deterministic `defasc_beta` sweep.
**Evidence:** 2779/4611 = **60.3%**.

---

### X077 — The sink count is a step function of `α_Φ`, measured 1.00…3.00 at 0.01
**Status:** CONFIRMED
**Method:** `_audit_a_bands.py` — independent 201-point scan; plus a 0.001-resolution scan of
[1.420, 1.940] in `_audit_a_cape.py` to look for oscillation inside a band.
**Evidence:** the sink set is piecewise constant on the grid, 10 distinct bands on [1.00, 3.00];
the 0.001 scan across [1.420, 1.940] shows three clean contiguous runs and no wobble.
It is a step function; it is **not** monotone (see X084).

---

### X078 — 1 sink `hangzhou` on [1.43, 1.93], width 0.50 — "the widest band on this field"
**Status:** PARTIAL
**Method:** `_audit_a_bands.py` (α ∈ [1.00, 3.00] at 0.01) and `_audit_a_bands_wide.py`
(α ∈ [1.00, 8.00] at 0.01, 701 solves). The spec places no upper bound on `α_Φ` anywhere —
§2.3 lists it as a design constant with no clamp, and X084 itself samples α_Φ = 8.
**Evidence:** the band figures reproduce exactly: sinkset `(hangzhou,)` at all 51 grid points of
[1.43, 1.93], contiguous, width 0.50; contiguous at 0.001 too ([1.425, 1.931], 507 points).
But the superlative is false. On [1.00, 8.00]:

| band | width | sinks |
|---|---|---|
| [4.19, 6.73] | **2.54** | `deccan, hangzhou` |
| [6.74, 8.00] | ≥1.26 (right-censored) | `hangzhou` |
| [3.39, 4.18] | 0.79 | `deccan, genua, hangzhou` |
| **[1.43, 1.93]** | **0.50** | `hangzhou` |
| [2.72, 3.20] | 0.48 | `doab, genua, hangzhou, venice` |

[1.43, 1.93] is only the 4th-widest band once the arbitrary right edge of the scan is lifted.
Two separate wider bands exist, one of them 5× wider, and one of them *also* a one-sink `hangzhou`
band — so even "the widest one-sink band" is false.
**Should say:** "the widest band **in the measured range α_Φ ∈ [1.00, 3.00]**". And the range
itself needs a stated reason, because on [1.00, 8.00] the widest band is [4.19, 6.73].

---

### X079 — 3 sinks `doab, genua, hangzhou` on [2.26, 2.71], width 0.45
**Status:** CONFIRMED
**Method:** `_audit_a_bands.py`; edge refinement from `audit_bands2.py`.
**Evidence:** exactly `doab+genua+hangzhou` on [2.26, 2.71], width 0.45; refined at 0.001 to
[2.253, 2.712], width 0.459.

---

### X080 — 2 sinks `genua, hangzhou` on [1.94, 2.25], width 0.31
**Status:** CONFIRMED
**Method:** As X079.
**Evidence:** `genua+hangzhou` on [1.94, 2.25], width 0.31; refined to [1.932, 2.252], width 0.320.

---

### X081 — 2 sinks `english_channel, hangzhou` on [1.41, 1.42], width 0.01
**Status:** CONFIRMED
**Method:** As X079.
**Evidence:** `english_channel+hangzhou` at exactly α = 1.41 and 1.42 and nowhere else on the
0.01 grid; width 0.01.

---

### X082 — That window is not a band: refined to 0.001 it spans [1.406, 1.424], 0.018 wide, against 0.506
**Status:** CONFIRMED
**Method:** Ran `audit_bands2.py` part (a) as shipped; independently re-derived the one-sink
band's 0.001 extent in `_audit_a_cape.py` by scanning [1.420, 1.940] at 0.001 (521 solves), which
also checks that `audit_bands2.py`'s ±10-step refinement window is not censoring any edge.
**Evidence:** narrow window refined = **[1.406, 1.424], width 0.018**. One-sink band refined =
**[1.425, 1.931], width 0.506** — 507 consecutive 0.001 grid points, one contiguous run, no
interior wobble. No refinement hit the 10-step cap (max steps used: 8), so none of the four
refined widths is censored.

---

### X083 — `α_Φ` retained at 1.5 because it sits inside the widest band; not because it was derived
**Status:** REFUTED
**Method:** `_audit_a_bands_wide.py`, as X078. This is a DESIGN claim, and the audit standard is
that a choice justified by a false fact is refuted even where the choice is defensible.
**Evidence:** the stated ground is "it sits inside the widest band". The widest band on this
wealth field is **[4.19, 6.73]** (2 sinks, `deccan`+`hangzhou`, width 2.54). 1.5 does not sit in
it. Applied as written, the "widest band" rule selects α_Φ ≈ 5.4, not 1.5. Note also that the
second-widest band, [6.74, 8.00] (≥1.26 wide), is itself a **one-sink `hangzhou`** band, so the
rule does not even select 1.5 among one-sink options. The retention of 1.5 is defensible on other
grounds (it is the band the previous value already sat in; it is near the middle of a band whose
edges move by ≤0.01 under ±1% noise; extreme α_Φ makes `c_w` a near-delta on one province), but
those grounds are not what §2.3 and §1.6 say.
**Should say:** either qualify the ground — "it sits inside the widest band **in the range
scanned**, and the range was capped at 3.0 because [reason]" — or replace the ground: "1.5 sits
0.07 from the nearest edge of a 0.50-wide band whose edges move by ≤0.01 under ±1% wealth noise,
which is a 7× margin; nothing now selects a different value."

---

### X084 — Sampled at v2's six values the count is non-monotone: 5 → 1 → 2 → 4 → 3 → 1
**Status:** CONFIRMED
**Method:** `v5measure.py` §D; cross-checked against the independent band table.
**Evidence:** α_Φ ∈ {1, 1.5, 2, 3, 4, 8} → counts **[5, 1, 2, 4, 3, 1]**. Band table agrees:
α=1 in [1.00,1.24] (5 sinks), 1.5 in [1.43,1.93] (1), 2 in [1.94,2.25] (2), 3 in [2.72,3.20] (4),
4 in [3.39,4.18] (3), 8 in [6.74,8.00] (1).

---

### X085 — One sink at 1444 is a snapshot, not a fixed feature; the map says so under load
**Status:** CONFIRMED
**Method:** Ran `europe.py` and `w9.py` as shipped; re-derived in `_audit_a_europe.py` and
`_audit_a_misc.py`.
**Evidence:** holding α_Φ = 1.5 and scaling nothing but the world, the sink set changes at a
1% European edge and takes 5 different counts across the tested loads. The claim is well
supported — and it is precisely what refutes X065, which sits eighteen lines above it in the
same section.

---

### X086 — At ×1.02 across Europe's 823 counted provinces the sinks are `{doab, english_channel, hangzhou, wien}`; `english_channel` is a sink at every larger factor tested
**Status:** PARTIAL
**Method:** Ran `europe.py`; independently recounted Europe in `_audit_a_europe.py` from
`map/continent.txt`; enumerated the factors `europe.py` actually tests (`range(0,61)` → ×1.00…×1.60
at 0.01, 61 values); ran the same experiment past that range; and re-ran the whole factor sweep
scaling `base_tax`/`base_production` instead of wealth.
**Evidence:**
- **823 is right.** `continent.txt` europe = 849 provinces; 823 survive §1.3's filter
  (25 unowned, 1 owned non-city, 0 owned-city outside a node). 25 trade nodes touched.
- **The ×1.02 sink set reproduces** under `europe.py`'s method: `{doab, english_channel, hangzhou, wien}`.
- **But that set is an artifact of scaling wealth rather than development.** Scaling
  `base_tax` and `base_production` by 1.02 and rebuilding wealth through §1.3's expression gives
  `{doab, english_channel, hangzhou}` — **`wien` is not a sink**. (The two methods differ because
  wealth's production term is `(0.2·base_production + flat)·price`, and the flat great-project /
  permanent-modifier addend does not scale with development.) Since the spec presents this row as
  "a 1–2% European **development** edge", the sink set it quotes is not the sink set that edge
  produces.
- **"a sink at every larger factor tested" is true only because testing stopped at ×1.60.**
  Tested factors are ×1.00 … ×1.60 (61 values); `english_channel` is a sink at all 60 of them
  above ×1.00. At ×1.80 and every larger factor I tried (×2, ×2.5, ×3, ×4, ×5, ×7, ×10, ×20, ×50)
  the sole sink is **`genua`** and `english_channel` is *not* a sink.
- Also: ×1.02 is not the threshold. At 0.001 resolution the first European sink appears at
  **×1.010** (identical under both scaling methods) — ×1.009 still gives the lone `hangzhou`.
**Should say:** "At ×1.02 across Europe's 823 counted provinces the sinks are
`{doab, english_channel, hangzhou}` (`{…, wien}` if wealth rather than development is scaled);
`english_channel` is a sink at every factor from ×1.01 to ×1.60, the range tested — above ×1.7 the
European mass consolidates and `genua` becomes the sole sink."

---

### X087 — At ×1.56 the sinks are `{english_channel, rheinland}` and Asia holds none
**Status:** PARTIAL
**Method:** As X086 — ran `europe.py`, then repeated at ×1.50…×1.60 under development scaling.
**Evidence:** under `europe.py`'s wealth scaling, ×1.56 → `{english_channel, rheinland}`,
Asia empty. **Under development scaling ×1.56 → `{english_channel, hangzhou, rheinland}`** — Asia
still holds `hangzhou`; Asia does not empty until ×1.57. The claim is true of the measurement that
was run and false of the thing that measurement is offered as evidence for.
**Should say:** "At ×1.56–×1.57 Asia holds no sink and the sinks are `{english_channel, rheinland}`"
— or fix `europe.py` to scale development and quote ×1.57.

---

### X088 — What the model claims is the threshold, not the size of the historical edge
**Status:** CONFIRMED
**Method:** Read §1.6 lines 402–406; measured the actual threshold at 0.001 resolution.
**Evidence:** both propositions hold. "2% is enough" is true (a European sink exists at ×1.02),
and nothing anywhere in the toolchain estimates the historical European development gain — I
grepped for it and there is no such measurement. The design stance is coherent.
*Note:* the number attached to the word "threshold" is not the threshold. The measured threshold
is **×1.010** (×1.009 → 1 sink, ×1.010 → 4 sinks), so the prose's "1–2%" band brackets it but
"×1.02" is 2× the true value. Quoting ×1.01 would be both more accurate and a stronger claim.

---

### X089 — Renaissance 1450.1.1 / 116 Florence; Colonialism 1500.1.1 / 224 Sevilla; Printing Press 1550.1.1 / 1876 Frankfurt
**Status:** CONFIRMED
**Method:** Read `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\institutions\00_Core.txt`
directly (not the spec's quotation of it), plus
`localisation\institutions_l_english.yml` for the `new_world_i` display name.
**Evidence:**
```
renaissance:     historical_start_date = 1450.1.1   historical_start_province = 116  # Florence
new_world_i:     historical_start_date = 1500.1.1   historical_start_province = 224  #Sevilla
printing_press:  historical_start_date = 1550.1.1   historical_start_province = 1876 #Frankfurt
```
`new_world_i:0 "Colonialism"` confirms the spec's naming. All three provinces are in
`map/continent.txt`'s europe list. The full file has 8 institutions; the next three
(`global_trade` 1600 Holland, `manufactories` 1650 Paris, `enlightenment` 1700 London) are also
European, so "all three the period is named for begin in Europe, inside this window" is
understated but correct.

---

### X090 — The Renaissance's embracement bonus is `development_cost = -0.05`
**Status:** CONFIRMED
**Method:** Read `00_Core.txt` lines 276–288 directly.
**Evidence:**
```
renaissance = {
	bonus = {
		development_cost = -0.05
		build_cost = -0.05
	}
	trade_company_efficiency = 0.4
```
The value is exactly as claimed. *Note:* the `bonus` block contains a second modifier,
`build_cost = -0.05`, which the spec does not mention; the omission does not affect the argument
(only `development_cost` bears on how fast development grows) but "the … bonus **is**
`development_cost = -0.05`" describes half of a two-line block.

---

### X091 — Those bonuses are country-scoped, excluded by §1.3, and reach the map only by changing development growth — the input `europe.py` scales directly
**Status:** REFUTED
**Method:** Read `europe.py` line by line.
**Evidence:** `europe.py` does **not** scale development. Its docstring claims it does
("multiplier on development -> both wealth terms scale with it") but the code is:
```python
BASE = np.array([r["tax"] + r["prod_income"] for r in ROWS])
def field(mult):
    return np.array([BASE[i] * mult.get(r["pid"], 1.0) for i, r in enumerate(ROWS)])
```
— a multiplier on **wealth**. The docstring's premise is false for every province carrying a flat
`trade_goods_size` bonus, because §1.3's production term is
`(GP_COEFF·base_production + flat)·(1+gpmod)·price·(1+tvmod)`: the additive `flat` does not scale
with development, so `wealth(f·dev) ≠ f·wealth(dev)`. Measured consequence, not hypothetical: at
×1.02 the two methods give different sink sets (`wien` present under wealth scaling, absent under
development scaling), and at ×1.56 they differ again (`hangzhou` absent under wealth scaling,
present under development scaling). The first three clauses of the claim (country-scoped,
excluded by §1.3) are correct.
**Should say:** either change `europe.py` to scale `base_tax` and `base_production` and requote
X086/X087 from that run, or change the claim to "…which is a close proxy for the input `europe.py`
scales; `europe.py` multiplies province wealth directly, which differs from a development
multiplier on the fifteen provinces carrying a flat `trade_goods_size`."

---

### X092 — The nine Lowland provinces by ×1.20 make `english_channel` a sink beside `hangzhou`, and it stays one through ×10
**Status:** CONFIRMED
**Method:** Ran `europe.py`'s Lowlands block (7 sampled factors), then a dense 32-point scan in
`_audit_a_europe.py` covering ×1.05 … ×10.00 including every 0.05 step from ×1.05 to ×2.00.
**Evidence:** ×1.20 → `['english_channel','hangzhou']` ✔. `english_channel` is a sink at **every**
factor from ×1.15 through ×10.00 with no gap — the claim survives the denser test that the 7-point
sample could not have shown. All nine pids (90, 92, 95, 96, 97, 98, 99, 100, 1744) are in
`english_channel`, as claimed. (The actual threshold is between ×1.10 and ×1.15, so ×1.20 is a
sampled point, but the claim does not present it as a threshold.)

---

### X093 — ±2% random noise leaves the 1444 sink set unchanged on three seeds; +2% systematic to Europe changes it
**Status:** CONFIRMED
**Method:** Ran `europe.py`'s noise block; independently repeated at ±2% over 20 fresh seeds in
`_audit_a_misc.py`.
**Evidence:** ±2% random, seeds 0/1/2 → `['hangzhou']` each time. Independently: ±2% over 20 new
seeds → 0 edge flips, 0 sink-set changes. +2% systematic to the 823 European provinces →
`['doab','english_channel','hangzhou','wien']`. The contrast is real and stronger than stated.

---

### X094 — The 1444 Europe→sink route is the Silk Road, `genua → … → hangzhou`
**Status:** CONFIRMED
**Method:** Ran `europe.py`'s route block; independently rebuilt the adjacency and re-ran BFS in
`_audit_a_main.py`, then printed the out-edge set of every node on the chain.
**Evidence:** the named chain reproduces exactly:
`genua → alexandria → aleppo → persia → lahore → doab → ganges_delta → burma → gulf_of_siam →
canton → hangzhou`. Every edge exists in the directed `Φ_w`.
*Note:* this is a BFS **shortest** path, not the unique drainage route — `genua` has 2 outlets
(`alexandria`, `ragusa`) and `alexandria` 3. The alternative via `ragusa → constantinople → aleppo`
rejoins the same chain. Calling it "the route" is a shortest-path reading, which is defensible;
the eight nodes from `aleppo` onward have out-degree 1 or 2 and are genuinely forced.

---

### X095 — From the north it is the Volga: `north_sea → white_sea → novgorod → kazan → astrakhan → persia → …`
**Status:** CONFIRMED
**Method:** As X094.
**Evidence:** reproduces exactly:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → lahore → doab → ganges_delta →
burma → gulf_of_siam → canton → hangzhou`. `north_sea` has 3 outlets
(`english_channel`, `lubeck`, `white_sea`); the Volga path is 12 hops and the alternative via
`english_channel` is 16, so BFS's choice is the genuine shortest and "the route" is fair.

---

### X096 — From the Channel it is the Hansa and the Danube
**Status:** CONFIRMED
**Method:** As X094.
**Evidence:** reproduces exactly: `english_channel → lubeck → saxony → wien → venice → ragusa →
constantinople → aleppo → persia → …`. `english_channel` has out-degree 1 (`lubeck`), so the first
hop is forced; `saxony`, `wien`, `venice`, `ragusa`, `constantinople` and `aleppo` all have
out-degree 1 as well, so this route is fully forced from `lubeck` onward except for `lubeck`'s
three outlets.

---

### X097 — Nothing routes through the Cape in `Φ_w`
**Status:** REFUTED
**Method:** `_audit_a_main.py` — enumerated `cape_of_good_hope`'s in- and out-edges in the 1444
`Φ_w` orientation, then computed its full upstream and downstream reachable sets.
**Evidence:** in the 1444 `Φ_w` the Cape has **in-degree 1 and out-degree 3**:
`ivory_coast → cape_of_good_hope → {malacca, comorin_cape, zanzibar}`.
Strictly upstream of the Cape: **5** nodes (`brazil`, `ivory_coast`, `kongo`, `laplata`,
`patagonia`). Strictly downstream: **23** nodes. That is **115 ordered node pairs joined by a
directed path through the Cape** — including every South-Atlantic node's entire drainage to the
sink. The Cape's `b_w` is `+0.0125` (it owns no provinces, so `c_w = 0`), which makes it a pure
supplier whose whole mass must leave through the Indian Ocean.
The claim is also contradicted **inside the same section**: §1.6's own Cape-reversal paragraph
says "1444's **Atlantic→Cape→Indian-Ocean drainage** becomes …", which is exactly the routing the
Cape sentence denies. And the parenthetical gloss ("The Cape is not idle — in the per-good graphs
it already carries …") reads as asserting that in `Φ_w` it *is* idle, which is false.
**Should say:** "None of the three Europe→sink routes passes through the Cape — Europe drains east
overland — although the Cape does carry the South Atlantic (`brazil`, `laplata`, `patagonia`,
`kongo`, `ivory_coast`) into the Indian Ocean, which is what a 1444 map should say."

---

### X098 — In the per-good graphs the Cape carries Asian spices to Europe
**Status:** CONFIRMED
**Method:** `_audit_a_main.py` — solved the spices graph and checked the named chain edge by edge
against the directed edge set (not by BFS, so a shortest-path artifact cannot save it).
**Evidence:** all five edges present:
`malacca → cape_of_good_hope` ✔, `cape_of_good_hope → zanzibar` ✔, `zanzibar → gulf_of_aden` ✔,
`gulf_of_aden → alexandria` ✔, `alexandria → genua` ✔. Spices sinks are
`['australia','brazil','genua']`, so the chain does terminate at a spices sink. In the spices
graph the Cape is `malacca → cape → {comorin_cape, ivory_coast, zanzibar}` — a conduit, matching
`v5measure.py`'s "cape is a conduit for 29/29 goods".

---

### X099 — 22 European nodes ×2 makes `genua` the sole sink; under the 18-node set alone sole-`genua` needs ×2.5
**Status:** PARTIAL
**Method:** Ran `w9.py` as shipped (it samples only ×1.5, ×2, ×2.5, ×3, ×4), then scanned both
node sets at 0.05 and then 0.01 resolution in `_audit_a_europe.py` / `_audit_a_cape.py`.
**Evidence:**
- 22-node ×2.0 → `['genua']` ✔ (in fact sole-`genua` already holds at ×1.90).
- The membership list is correct: 18 western/central nodes + `constantinople`, `crimea`, `kiev`,
  `kazan` = 22 nodes, 796 provinces.
- **"needs ×2.5" is false.** Under the 18-node set the sinks are `['genua','rheinland']` at
  ×1.95–×2.14 and become `['genua']` at **×2.15** and every step thereafter. ×2.5 is simply the
  smallest value `w9.py` sampled; the threshold is ×2.15 at 0.01 resolution.
**Should say:** "under the 18-node set alone sole-`genua` needs ×2.15."

---

### X100 — Between ×3 and ×3.75 the Cape reverses; outside that window it does not, so it is a band not a threshold
**Status:** REFUTED
**Method:** `_audit_a_cape.py` — scanned the 22-node factor at **0.01** over [2.50, 4.50] (201
solves), testing for the exact state the spec names: in ← `{comorin_cape, malacca, zanzibar}`,
out → `{ivory_coast}`. The 3.75 figure appears nowhere in the toolchain — `grep -rn 3.75 scripts/*.py`
matches only `q02.py`, which is the script that *inserts this sentence into the spec*. `w9.py`,
which produced the rest of this paragraph, samples only ×1.5, ×2, ×2.5, ×3, ×4, so neither edge of
"[3, 3.75]" was ever measured.
**Evidence:** the fully-reversed factors are

```
contiguous runs: [2.82, 3.18]  and  [3.24, 3.93]
gap inside:      [3.19, 3.23]  (5 sampled factors, NOT reversed)
```
- The lower edge is **×2.82**, not ×3 — the Cape is already reversed at 18 factors below ×3.
- The upper edge is **×3.93**, not ×3.75 — it is still reversed at 18 factors above ×3.75.
- 36 of the 107 reversed factors lie **outside** [3.00, 3.75], so "outside that window it does not"
  is false.
- 5 factors **inside** [3.00, 3.75] (×3.19–×3.23) are *not* reversed, so the quoted window is not
  even solidly reversed internally.
- It is not one band: it is **two** bands separated by a hole. The conclusion "the reversal is a
  band and not a threshold" survives in spirit (it is bounded above and below), but the specific
  window is wrong on both edges and the singular "a band" is wrong.
**Should say:** "between ×2.82 and ×3.93 the Cape of Good Hope reverses, with a narrow
non-reversed interval at ×3.19–×3.23; outside [2.82, 3.93] it does not, so the reversal is bounded
above as well as below and is not a threshold."

---

### X101 — Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at ×10
**Status:** CONFIRMED
**Method:** Ran `w9.py` as shipped (samples ×10, ×20, ×30, ×50), then a 21-point scan ×2…×100 in
`_audit_a_europe.py`.
**Evidence:** all four sampled points reproduce — ×10 → `['genua','gulf_of_siam','hangzhou']`
(three), ×20/×30/×50 → `['hangzhou']`. Top province is pid 1821, wealth 30.40.
*Note on completeness:* the split is wider and deeper than the four sampled points reveal —
×5–×7 give **four** sinks (`doab, genua, gulf_of_siam, hangzhou`), ×8–×10 three, ×11 three
(`genua, hangzhou, venice`), ×12 two, and sole-`hangzhou` only returns at ×14. So the phrase "a
transient split into three at ×10" is literally true but is a 4-point sample of a ×5–×13 excursion
that reaches four sinks. §1.6's following sentence ("extra sinks at intermediate boosts are
expected behaviour") covers this, so nothing in the argument breaks.

---

### X102 — `TRADE_MERCHANT_PRESENT = 0.1` is a flat income bonus, settled by its shipped comment
**Status:** CONFIRMED
**Method:** Read `common/defines.lua` directly (not the spec's quotation of it). Checked that trade
efficiency is a separate quantity, and swept the localisation for a merchant-present tooltip.
**Evidence:** `common/defines.lua:1201` reads verbatim
`	TRADE_MERCHANT_PRESENT = 0.1,					-- bonus on income if trade present`.
Neighbouring lines confirm §1.7's other constants: `:1197 MERCHANT_MAX_POWER_BONUS = 2.0` and
`:1200 TRADE_NON_CAPITAL_OFFICE = -0.50` (the −50% off-home penalty). Trade efficiency is a distinct
key (`TRADE_EFFICIENCY` / `TRADE_EFFICIENCY_LABEL` in localisation, `trade_efficiency` as a
modifier), so the two quantities are genuinely different. The only merchant-presence loc string is
`MERCHANT_PRESENT_EFFECT` (" Having a merchant present gives $VAL|1=+$ trade power."), which is
`MERCHANT_MAX_POWER_BONUS`, not this define — so the comment really is the only file evidence.
**Note (internal tension, not a refutation):** §3.16's own rule is that "an engine fact sourced to a
*string* is settled only when something observes the behaviour the string describes". X102 says a
shipped comment *settles* the semantics, and no §2.7 probe observes this bonus.

---

### X103 — every trade-range string/define/modifier is about reach, not flow (seven named)
**Status:** CONFIRMED (the universal claim survives); the enumeration is not exhaustive
**Method:** Verified each of the seven named strings by key, then swept independently: all of
`localisation/*english*`, `common/defines.lua` + `common/defines/*`, all of `common/**` for
`trade_range`, and the `eu4.exe` string table for `*TRADE_RANGE*|*TRADERANGE*|*trade_range*`.
**Evidence:** All seven exist and say what the spec says —
`EU4_l_english.yml:1353 TRADE_RANGE_IRO` ("Our merchants can reach trade nodes within this range."),
`hints_l_english.yml:230 HINT_TRADERANGE_TEXT` ("…how far away you may send a Merchant…"),
`EU4_l_english.yml:2847 TRADE_NODES_OUT_OF_RANGE`, `core_l_english.yml:325 MAPMODE_TRADE_DESC`,
`emperor_mercs_l_english.yml:15 MERCENARY_COMPANY_TOO_FAR`, `:17 MERC_RANGE_EXPLAINED`,
`domination_l_english.yml:2100 REQUIRES_CAPITAL_IN_TRADE_RANGE_TT`. Every additional hit is also
about reach, so the universal claim holds.
Not exhaustive — the sweep found at least: `IS_IN_TRADE_RANGE` / `IS_NOT_IN_TRADE_RANGE`
(text:5130-1), `REQUIRES_FROM_TO_BE_IN_TRADE_RANGE_TT` (domination:2101), `TRADE_THROUGH_TT`
(EU4:1279), `EStopMissionReason_OutOfTradeRange` (tmm:31), `TRADE_WIND_DESC` (nw:209),
`MODIFIER_TRADE_RANGE`, `TRADE_RANGE_LABEL`, `LEDGER_TRADE_RANGE`, `LEDGER_TC_TRADE_RANGE`,
`CV_RESEARCHED_TRADERANGE_TOOLTIP` / `CV_NOTRESEARCHED_…`,
`MODIFIER_MERCENARY_INDEPENDENT_FROM_TRADE_RANGE`; defines `MERCENARY_TRADE_RANGE_MODIFIER`
(defines.lua:1582) and `TRADING_CITY_TRADING_RANGE_BOOST` (:1125); modifiers `trade_range_modifier`
(the central key, ~40 uses across ideas, estate privileges, government reforms, event/mission
modifiers), `merc_independent_from_trade_range`, and the tech key `tech_trade_range`.
**Should say:** name `trade_range_modifier` and the two defines, or mark the list "for example".
The claim's substance is unaffected.

---

### X104 — no string, define or modifier ties range to link flow
**Status:** CONFIRMED
**Method:** The sweep above, extended: every `trade_range*` hit in `common/` classified by what it
modifies; every `*RANGE*` define in `defines.lua` read; the `eu4.exe` string table scanned for
`*supply_range*` and for every `*trade_power*` key.
**Evidence:** Every range construct found either (a) extends or reports a country's trade range
(`trade_range_modifier`, `tech_trade_range`, `TRADING_CITY_TRADING_RANGE_BOOST`, trade winds), or
(b) derives a hiring/diplomatic reach from it (`MERCENARY_TRADE_RANGE_MODIFIER`,
`merc_independent_from_trade_range`, `REQUIRES_*_IN_TRADE_RANGE_TT`). Nothing conditions the value
carried on a link. The companion sentence also holds: the only `*SUPPLY_RANGE*` strings in the
binary are `NAVAL_SUPPLY_RANGE` (`defines.lua:1365 = 150`), `SHIP_SUPPLY_RANGE` and
`update_supply_range` — all naval. The claim's own self-limitation ("a statement about the files,
not a proof") is the right one and is preserved.

---

### X105 — Propagate Religion: 50/50 default, 35/35 terminal, nine flag rungs banded 5–10 points
**Status:** CONFIRMED
**Method:** Read `common/trading_policies/00_trading_policies.txt` directly (the only file in that
directory); compared `can_select` (lines 285–295) against `can_maintain` (lines 336–345) rung by
rung.
**Evidence:** Nine `N_trade_power_for_propogate_religion` flags exist: 5, 10, 15, 20, 25, 30, 35,
40, 45. Select→maintain: 5→(no `trade_share` clause at all), 10→5, 15→5, 20→10, 25→15, 30→20,
35→25, 40→30, 45→35 — exactly the spec's ladder. **The count is right:** eight pairs in parentheses
plus the 5-flag stated separately makes nine rungs, and the trail is 5 points on the 10-flag and 10
points on the other seven, i.e. "5–10 points". The penultimate branch (no
`orm_easier_propagation_flag`, or held ≥5475 days) is `share = 50` in both blocks; the terminal
`else` is `share = 35` in both blocks. Neither is banded.
**Note (omission, folded into X106):** every branch of both blocks also requires
`FROM = { has_trader = ROOT is_node_in_trade_company_region = yes }`. §1.10's table presents
Propagate Religion as a bare power threshold; in the file it applies only where the country has a
merchant in a node inside a trade-company region.

---

### X106 — Improve Inland Routes is the one unconditionally banded mechanic; the flicker-risk set
**Status:** PARTIAL
**Method:** Swept every `can_maintain` block in the trading-policies file; read every threshold in
§1.10's table out of `common/defines.lua`; then looked for shipped hysteresis/cooldown on the same
mechanics.
**Evidence — the banding half is CONFIRMED.** The file contains exactly three `can_maintain` blocks
(lines 124, 170, 298): `improve_inland_routes` and `improve_inland_routes_upgraded` (both 50 to
establish / 40 to maintain, both gated by `NOT = { has_government_attribute =
free_improve_inland_routes }`, both also requiring `has_trader = ROOT`), and `propagate_religion`.
Every other §1.10 threshold is a single-valued define: `JUSTIFY_TRADE_CONFLICT_LIMIT = 0.2` (:164),
`JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT = 0.1` (:165),
`MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER = 0.2` (:367), `TRADE_COMPANY_STRONG_LIMIT = 0.51`
(:1213), `TRADE_COMPANY_CONTROL_LIMIT = 0.6` (:1211). No paired maintain value exists for any.
**Evidence — the derived conclusion is partly REFUTED.** §1.10 concludes "almost nothing absorbs
threshold chatter". Three shipped dampers on those same mechanics are unaccounted for:
`TRADING_POLICY_COOLDOWN_MONTHS = 12` (`defines.lua:1045`, "Cooldown until you can change Trading
Policy after selecting" — `cooldown = no` is set on only `maximize_profit` and
`maximize_profit_upgraded`, so **both banded policies carry the 12-month cooldown**);
`TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` (:1212) and `TRADE_COMPANY_COOLDOWN = 60` (:1214), which
damp the two trade-company limits. Also the Propagate Religion risk set is much narrower than
"flagless countries": every branch is gated on `has_trader = ROOT` **and**
`is_node_in_trade_company_region = yes`.
**Should say:** "Improve Inland Routes is the one unconditionally banded mechanic … but banding is
not the only damper: `TRADING_POLICY_COOLDOWN_MONTHS = 12` gates re-selection of both banded
policies, and `TRADE_COMPANY_DAYS_TO_SWAP_LEADER`/`TRADE_COMPANY_COOLDOWN` damp the two
trade-company limits. Propagate Religion reaches only a country with a merchant in a
trade-company-region node."

---

### X107 — the caravan cap of 50 is 8.6%–32.0% of an inland node's total trade power, median 17.9%
**Status:** REFUTED (as worded — the percentages are not of the totals quoted in the same sentence)
**Method:** Re-parsed the save's `trade{}` block with a recursive brace parser (not regex), summed
each node's country `val=` fields, took the flag's 26 `inland=yes` nodes from
`common/tradenodes/00_tradenodes.txt`, and computed the cap share under both possible denominators.
Also ran the author's own `audit_delta.py`, which the README names as the producer of this figure.
**Evidence:** The totals reproduce exactly: 106.4 at `xian`, 532.0 at `champagne` (531.98).
Against *those* totals, 50 is **9.40% to 47.01%**, median 21.57% (true) / 21.88% (element at index
n//2) — which is exactly what `audit_delta.py` prints:
`flag (26) … cap share 9.4%..47.0% median 21.9%`.
The spec's 8.6% / 32.0% / 17.9% are `50/(total+50)`: `50/582.0 = 8.591%`, `50/156.4 = 31.969%`,
index-median `17.949%` (true median 17.740%). Both endpoints match to three significant figures, so
the denominator is settled: the figures are the caravan holder's share of the node's power *after*
the grant, not "of an inland node's total trade power". The sentence therefore uses "total trade
power" in two incompatible senses 30 words apart: 8.6% of 532.0 is 45.7, not 50; 32.0% of 106.4 is
34.0, not 50. Secondary: 17.9 is a truncation of 17.949 (correct rounding is 18.0) and is the
element-at-index median of 26 values, not the median (17.74).
**Should say:** either "50 is **9.4% to 47.0%** of an inland node's existing total trade power
(median 21.9%)" or "a country at the cap holds **8.6% to 32.0%** of the node's trade power once the
grant applies (median 17.9%), against pre-grant totals of 106.4 to 532.0". As it stands the document
and its own re-measurement script disagree.

---

### X108 — on the derived 25-node inland basis only the median moves, to 17.5%
**Status:** CONFIRMED (given X107's undisclosed denominator), with one small slip
**Method:** Same parse; derived-inland set computed from `members` against a coastal set I re-derived
myself from `map/provinces.bmp` + `map/definition.csv` + `map/default.map`; both bases compared on
every quantity the claim names.
**Evidence:** flag 26 → derived 25 (drops `siberia` only). Range identical on both bases under
either denominator (8.59%–31.98%, or 9.40%–47.01%); largest-holder span identical (23.6 `ohio` to
143.2 `deccan`); the set of nodes where the cap wins is identical and has 7 members
(`african_great_lakes`, `katsina`, `kongo`, `lhasa`, `ohio`, `rheinland`, `zambezi`). Median moves
17.949% → **17.531%** ✓ on `50/(total+50)` (or 21.876% → 21.258% on `50/total`).
**Slip:** the *loss* count is not identical — §1.10's "outweighed in the other 19" becomes 18 on the
25-node basis, while the claim says everything but the median is unchanged.
**Inland-derivation check (§2.2, swept, not spot-checked):** over **all 80 nodes**, flag-only =
`['siberia']`, derived-only = `[]`, so "exactly one node" is correct, and `siberia`'s coastal members
are exactly 1781 and 1782 as stated. Caveat: the rule "no coastal province among its `members`" is
sensitive to what counts as coastal — counting *lake* adjacency (default.map's 125 `lakes`) gives 10
derived-inland nodes and 16 disagreements, not 25 and 1. The sea-only reading is clearly the intended
one (it matches the flag on 79/80), but §2.2 never says which.

---

### X109 — largest single incumbent holder 23.6–143.2; the cap outweighs it in 7 of 26
**Status:** CONFIRMED
**Method:** Per-node max of the country `val=` fields from my own brace parse, over the flag's 26.
**Evidence:** min **23.6** (`ohio`), max **143.2** (`deccan`); `50 > max holder` on exactly **7 of
26** nodes, outweighed on the other 19. Matches `audit_delta.py` and the spec exactly.

---

### X110 — `highest_power` is not the largest country's power: differs on 79 of 79
**Status:** CONFIRMED
**Method:** Independent recursive-descent parse of `gamestate`'s `trade{}` (no regex depth
assumptions), collecting every 3-letter sub-block's scalar fields per node.
**Evidence:** The save holds **80** `node={}` blocks. 79 carry `highest_power` and at least one
country with a `val=`; the 80th (`cape_of_good_hope`) carries neither (it does carry `retention`).
`highest_power == max(country val)` on **0 of 79** — differs on 79 of 79 ✓.
`venice`: `highest_power=53.200` against `VEN val=106.206` ✓ (spec's 53.2 / 106.2).
It matches no fixed share of any node field: hp/total 0.0193–0.6783, hp/max 0.0201–0.6830,
hp/p_pow 0.0779–1.0000, hp/collector_power 0.0199–1.2402 — none constant ✓. Nor is it the
second-largest country val (0 of 79).
**Node-count question resolved:** there is no inconsistency between §1.10's "79 of 79", §2.8's
"80 of 80" (`retention`) and "78 of 79" (`total`). The save has 80 nodes; `retention` is present on
80, `highest_power`/`total`/`p_pow`/`max` on 79, `collector_power` on 77. Each denominator is the
population that carries the field.

---

### X111 — solver item 4's wealth expression, with no autonomy/efficiency/ideas/owner terms
**Status:** CONFIRMED (DESIGN, internal consistency)
**Method:** Read `solver.py:province_table()` against the spec's formula, term by term.
**Evidence:** `gp = (0.2·base_production + FLAT[pid])·(1 + MON_GPMOD[pid])`;
`tax = base_tax·(1 + LOCAL_TAX_MOD[good])`;
`prod_income = gp·price·(1 + LOCAL_TV_MOD[good] + MON_TVMOD[pid])`. That is exactly
`TAX_COEFF·base_tax·(1+tax mods) + (GP_COEFF·base_production + flat goods bonuses)·(1+goods-produced
mods)·price·(1+trade-value mods)` with `TAX_COEFF = 1.0`, `GP_COEFF = 0.2`. No autonomy, efficiency,
idea or owner term appears in the value; `owner` is used only as an inclusion filter (`owner` set and
`is_city = yes`), consistent with §1.3's owner-agnostic value.

---

### X112 — gems 43, incense 29, six great projects + ten permanent modifiers = 16 provinces beyond
**Status:** REFUTED
**Method:** Recomputed the counts from `prov1444.json` and cross-read the province histories in
`history/provinces/` for every modifier province.
**Evidence:** gems = **43** ✓, incense = **29** ✓, great-project provinces = **6**
(`{8, 262, 684, 1821, 1822, 2145}`) ✓, permanent-modifier provinces = **10**
(`{6, 362, 363, 370, 371, 387, 542, 2151, 2316, 4316}`) ✓, and the two sets are disjoint, so 16
provinces carry a project/permanent modifier ✓.
**But one of the 16 is a gems province.** pid **542 = Golconda** (`history/provinces/542 -
Golconda.txt`): `trade_goods = gems` *and* `add_permanent_province_modifier = { name =
diamond_mines_of_golconda_modifier duration = -1 }`. It is inside the 43 gems provinces, so it is not
"beyond the two trade goods". No other of the 16 is gems or incense.
**Should say:** "six great projects and ten permanent province modifiers — 16 provinces, **15 of them
beyond the two trade goods** (`542` Golconda is also one of the 43 gems provinces)."

---

### X113 — world wealth 10,677.50 over 2,452 counted provinces
**Status:** CONFIRMED
**Method:** Two ways. (a) `solver.py`'s `ROWS` summed. (b) An independent recomputation
(`_audit_c_wealth.py`) that re-reads `common/prices/00_prices.txt` and re-applies the §1.3 formula
from scratch over `prov1444.json` + `nodes.json`, without importing `solver.py`.
**Evidence:** counted provinces **2452**, world wealth **10677.5000** — identical to four decimals by
both routes. Exclusions: 1451 unowned, 20 owned-but-not-`is_city`, 0 outside every node. Province
histories spot-checked against the install for pids 542 and 387 (base_tax / base_production /
trade_goods all agree with `prov1444.json`).

---

### X114 — 0.17–0.21 s for all 29 goods, mean 5.7–7.3 ms/good, individual goods 5.4–24 ms
**Status:** PARTIAL
**Method:** Re-timed on the same machine: 18 full 29-good solves (6 + 12) through the same code path
(`build_sc(eps=0)` + `drain.run_drain` per good), timing each good individually with `perf_counter`.
**Evidence (12-run batch):** all-29 total **0.100 – 0.274 s**, median 0.181 s; only **5 of 12** runs
fell inside the spec's [0.17, 0.21] s. Mean per good **3.44 – 9.45 ms** against the spec's 5.7–7.3.
Individual goods **3.06 – 21.03 ms** against the spec's 5.4–24 (the low end is below the stated
floor). The earlier 6-run batch agrees (0.144–0.225 s; per-good 3.16–21.74 ms; slowest good `wine` at
21.7 ms). So the central figures reproduce — median 0.181 s, median 6.4 ms/good, one good near 21 ms
— but the stated intervals do not bound repeated runs, and the claim presents them as ranges "across
runs" without saying how many.
**Should say:** quote a median and a run count, e.g. "median 0.18 s for all 29 goods over 12 runs
(0.10–0.27 s), individual goods 3–22 ms", or mark the interval typical rather than a range. The
load-bearing conclusion ("milliseconds each") is unaffected.

---

### X115 — "milliseconds each" holds with a generic LP; no projection is offered
**Status:** CONFIRMED (DESIGN)
**Method:** Checked the claim against my own timings and checked the spec text for a projection.
**Evidence:** every individual good solved in 3–22 ms across 18 runs, so "milliseconds each" holds
with scipy/HiGHS as shipped. §2.2 states "no measurement in this project supports a specific
projection, and none is offered", and none appears in §2.2 or §3.11 — the rationale supports the
abstention.

---

### X116 — Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: T2 and T3
**Status:** CONFIRMED
**Method:** Verified the Phase-0 independence of both cases, and proved the pair exhaustive inside the
core.
**Evidence:** T2: `Plog` empty (5-cycle + chord, min degree 2), `fallbacks = ∅`, sinks `{u2}` vs
formula `{u1, u2}`. T3: `Plog` empty (triangle), sinks `{A}` vs formula `∅`. Both inside the 2-core,
both independent of Phase 0. Exhaustiveness: inside the core a formula member can fail to be a sink
only by gaining a free out-arc to an earlier-marked node, and only a *selected* node can do that — a
promoted or fallback node is popped immediately on promotion, at a moment when it provably has no
free edge to a marked node (otherwise it would have been ready and there would have been no stall),
so all its free edges orient inward. And a core sink outside the formula must be a fallback, since
core sinks ⊆ selected ∪ promoted ∪ fallbacks and a selected or promoted sink is automatically in the
formula. Random search agrees: equality-failure classes were pendant (2,385),
formula-member-not-a-sink (1,942), fallback-sink (97), **other: 0**.

---

### X117 — Free-edge determinism is proved as determinism and measured as index-independence; both halves are unaffected by peeling, which does not touch the priority key
**Status:** PARTIAL
**Method:** Checked what the priority key reads against what Phase 0 rewrites.
**Evidence:** The key is `(DEF, β, index)` and `β` is the **post-fold** balance — `phase0` returns
`beta` with each pendant's balance added to its parent, and `flow_def` is computed from that same
`beta`. So peeling changes the values the key reads and can create exact ties the input balances do
not have. Worked example: core 0–1–2–3 (edges 01, 03, 12, 13, 23) with input `b(1) = 0.5 ≠
b(2) = 1.0`, plus a pendant on node 1 carrying `+0.5`. After the fold `β(1) = 1.0 = β(2)`, `DEF` is
equal across the core, the key ties exactly, and the free edge {1,2} is oriented by node index alone
(five of the 120 relabellings flip it, LP support unchanged). Without the pendant there is no tie on
that pair. The determinism half is indeed unaffected by peeling; the *measured* half is not — it is a
property of the balances, and peeling rewrites them.
**Should say:** "…the determinism half is unaffected by peeling; the index-independence half is a
measurement on the **post-fold** balances, and Phase 0 can create exact `(DEF, β)` ties that the raw
balances do not have, so the 1444 measurement does not transfer to a peeled map."

---

### X118 — `GP_COEFF` = 0.2, measured on four provinces at four development levels
**Status:** CONFIRMED (to the limit of what files can settle)
**Method.** Read the four province history files in the install; checked the arithmetic for
linearity; searched `defines.lua` and `common/defines/` for any 0.2 constant tied to production.
**Evidence.** `1747 - Caceres.txt`: `base_tax 2`, `base_production 2`, `trade_goods wool`.
`212 - Girona.txt`: 3, 3, `fish`. `223 - Granada.txt`: 6, 4, `silk`. `213 - Barcelona.txt`: 6, 5,
`glass`. All four match the spec exactly (including the trade goods, which the spec relies on
elsewhere). The four readings 2→0.40, 3→0.60, 4→0.80, 5→1.00 give 0.2 exactly at every level, with
no intercept. No define carries it: an exhaustive scan of `defines.lua` + `common/defines/*.lua`
(187 kB) found only `JUSTIFY_TRADE_CONFLICT_LIMIT`, `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`,
`TRADED_FRACTION_FOR_BONUS` and `TRADE_GOODS_ROTATE_SPEED` at 0.2, none of them production-related.
The tooltip readings themselves cannot be re-run; every checkable component checks out.

---

### X119 — `TAX_COEFF` = 1.0 ducat/year per `base_tax`, and neither coefficient is a define
**Status:** CONFIRMED (to the limit of what files can settle)
**Method.** Arithmetic on the two quoted readings; exhaustive grep of `defines.lua` and
`common/defines/`.
**Evidence.** `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 → 6.00/6 = 1.0; `Base: 0.16 (Yearly 2.00)`
at `base_tax` 2 → 2.00/2 = 1.0. Consistent at both levels. Premise verified: neither `0.083`,
`0.0833`, `GOODS_PRODUCED`, `BASE_PRODUCTION`, `MONTHLY_TAX`, `TAX_PER` nor `PRODUCTION_PER` occurs
anywhere in `defines.lua` or `common/defines/`; no define holds either value in a relevant key.

---

### X120 — the displayed monthly tax is the truncation of `base_tax × 0.083333`
**Status:** CONFIRMED
**Method.** Checked both readings under truncation and under rounding, and checked whether exact
1/12 can be made to fit.
**Evidence.** 6 × 0.083333 = 0.499998 → truncated 0.49 (displayed), rounded 0.50 (not displayed).
2 × 0.083333 = 0.166666 → truncated 0.16 (displayed), rounded 0.17 (not displayed). Truncation is
therefore the only reading consistent with both observations *for that coefficient*. Exact 1/12 is
excluded regardless of rounding mode: 6/12 = 0.5 displays as 0.50, not 0.49 — so the engine's
constant must itself be a truncated decimal. Caveat recorded, not a defect: two observations cannot
pin coefficient and rounding mode jointly (a coefficient in [0.0808, 0.0825) with rounding also
fits both), but no such coefficient is 1/12, so within the 1/12 family truncation is forced.

---

### X121 — both coefficients read off the tooltips' base lines, which carry no owner term
**Status:** CONFIRMED
**Method.** Verified each premise the rationale rests on from the install.
**Evidence.** `history/countries/GRA - Granada.txt` contains **0** occurrences of `personality`, so
Granada's 1444 ruler personality is rolled at game start — the window figure really is one sample of
a random variable. `industrious_personality` in `common/ruler_personalities/00_core.txt` l.1359–1406
grants `global_trade_goods_size_modifier = 0.1`, which is exactly the +10% that turns 0.80 × 4.00 =
3.20 into the observed window 3.52. `history/provinces/223 - Granada.txt` contains **0** occurrences
of `local_autonomy`, so the default 0 the spec asserts holds. The rationale is supported by every
fact it names.

---

### X122 — α_Φ's stated calibration is withdrawn
**Status:** CONFIRMED
**Method.** Verified the historical claim in all three prior specs; reproduced §1.6's band table
independently (α_Φ 1.00–3.00 at 0.01 on the corrected wealth field); checked §2.3's statement against
§1.6's.
**Evidence.** `v2-drain` l.372, `v3-owner-agnostic` l.558 and `v4-owner-agnostic` l.632 all read
"(calibrated so the 1444 start yields the two-sink hangzhou/english_channel map". On the corrected
field my sweep gives: `english_channel,hangzhou` only over **[1.41, 1.42]** (width 0.01 at 0.01
resolution), `hangzhou` alone over **[1.43, 1.93]** (width 0.50, the widest band), `genua,hangzhou`
[1.94, 2.25] (0.31), `doab,genua,hangzhou` [2.26, 2.71] (0.45). α_Φ = 1.5 → `['hangzhou']`, not the
two-sink map. Every number §2.3 states matches §1.6's, and §2.3's "narrower than the uncertainty in
its own edges under ±1% wealth noise" is consistent with §1.6's 0.018 width against edges moving up
to 0.02. The withdrawal is coherent and the retention ("sits inside the widest band, nothing selects
another value") follows from the same measurement.

---

### X123 — any future change to α_Φ is a design decision about how many ends the graph should have
**Status:** CONFIRMED
**Method.** Internal-consistency check against §2.3's own withdrawal and §1.6's band table.
**Evidence.** Once the calibration is withdrawn, nothing in the model selects 1.5 — my band sweep
confirms the sink count is a step function of α_Φ taking values 5, 6, 5, 2, 1, 2, 3, 4 across
[1.00, 3.00], so the knob's only effect is the end count. That is exactly what X123 says. It is
also consistent with §2.3's framing of α_Φ as "a constant like `P₀`; world-responsiveness flows
through wealth, never through this knob." No inconsistency found.

---

### X124 — the cyclic-file crash: single exception address, 1002 frames, three launches, vanilla + reversed-order controls
**Status:** PARTIAL
**Method.** Read the three crash dumps on disk directly (`Europa Universalis IV/crashes/*`), not the
spec's account of them; read `../v2-drain/game-session.md` and `../v3-owner-agnostic/validation-v3.md`.
**Evidence.** All four substantive facts verify from the artifacts. Three dumps
(`eu4_20260820_134250`, `_134617`, `_165621`), each `Mods: mod/pgt_cycle.mod`, each
`Unhandled Exception C00000FD (EXCEPTION_STACK_OVERFLOW) at address 0x00007FF6DDE6A8B4`, each with
exactly **1002** `eu4.exe` lines in `exception.txt`, each frame rendered
`eu4.exe (function-name not available) (+ 0)` with no per-frame address — so "the dump records no
per-frame addresses" is exactly right. Controls verified in `game-session.md`: vanilla 0/159
violations loads and runs; `pgt_permute` 159/159 violations, 0 cycles, loads and runs.
**Should say:** the count and its citation are wrong. §2.4 attributes the passage to
`../v2-drain/game-session.md`, which records **two** launches ("reproduced on two independent
launches", "stack overflow, twice", "reproduced twice", "×2"). The third reproduction is
`validation-v3.md`'s, run during that audit. And §2.7 of the v5 spec still says "1002 frames at one
address, **twice**", so the document asserts both three and twice. Either cite `validation-v3.md`
alongside `game-session.md` and fix §2.7, or drop to "twice" in §2.4/§3.6.

---

### X125 — The node order itself is a correctness requirement: the priority key breaks exact ties by index, and on the fallback branch (T3) the wealth key ties and the index alone decides
**Status:** REFUTED
**Method:** Checked the cited example against the sentence that cites it, and checked the wealth key
on the 1444 map.
**Evidence:** §2.4 item 1's justification is false of T3. In T3 (as worked in §3.2 and as run in
`toys.py`) node wealth is **3, 2, 1** — the wealth key does **not** tie, and it decides the promotion
outright (A wins on wealth, not on index). What the index decides in T3 is the marking order of B
against C, through the `(DEF, b, index)` priority key, both keyed `(0, 0, ·)` — a different
mechanism, unrelated to the fallback branch. On 1444 the wealth key ties nowhere (80/80 distinct
`NODEW`), so the cited mechanism is not merely rare on the target map, it is absent. The design
requirement is sound and is already carried by the first half of the same sentence; the fact offered
as its ground is wrong.
**Should say:** "…§1.1's priority key breaks exact `(DEF, b)` ties by node index — as in T3, where B
and C are both keyed `(0, 0, ·)` and the index alone orients the free edge between them — so the
emitter must fix one canonical node order…". Delete "the wealth key ties", or attach it to a
hypothetical whose candidates' wealths are actually equal, which T3's are not.

---

### X126 — `end=yes` on every `Φ_w` sink: 1444 has one end node, `hangzhou`, against vanilla's three
**Status:** CONFIRMED
**Method:** Read `common/tradenodes/00_tradenodes.txt` directly and counted `end=yes`
occurrences and their owning node blocks; ran `v5measure.py` §B and §D.
**Evidence:** the shipped file declares 80 nodes and exactly **3** `end=yes` blocks, at
`genua`, `venice`, `english_channel` (lines 2052, 2062, 2072). 1444 `Φ_w` at α_Φ = 1.5 has exactly
**1** sink, `hangzhou`. Both halves check out against the file, not against the spec's quotation.

---

### X127 — The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter reads it from the solve
**Status:** CONFIRMED
**Method:** Combined the α_Φ band scan (`_audit_a_bands*.py`) with the fixed-α_Φ world-perturbation
sweep (`_audit_a_misc.py`).
**Evidence:** the count varies 1…6 across α_Φ at a fixed world, and 1…5 across worlds at a fixed
α_Φ. Both dependencies are real, so an emitter that assumed any particular number would be wrong.
The engineering conclusion follows from the measurements.
*Cross-reference:* this claim is correct and X065 is not; they contradict each other on whether
the wealth field moves the count. X127 is the one to keep.

---

### X128 — Baseline: cloves sink at Venice, Kongo, Deccan, Australia, Brazil; under the §3.13 α-calibration spices sinks at Genoa alone and cloves moves to Deccan
**Status:** CONFIRMED
**Method:** Re-ran `drainrep.py` (baseline) and `final.py` Part B (calibration: α unclamped at
exponent 2, ρ = 0.5, twig tolerance 3e-4).
**Evidence:** Baseline cloves DRAIN sinks `['deccan', 'venice', 'kongo', 'australia', 'brazil']` —
the five named. Calibration: `V107 spices sinks under calibration: ['genua']`; `V107 China nodes among
calibration spices sinks: []`; `V179 cloves alpha=16 sinks: ['deccan']`. Both halves hold; "cloves
moves to Deccan" is true in the sense that its sink set *collapses to* `{deccan}` (Deccan is already
one of its five baseline sinks, so "moves to" reads as a relocation when it is a collapse — worth a
word in the text).
*Adjacent defect in the same §2.8 row, outside this ID:* the row says spices "sink at Genoa
**(demand rank 1)**". Genoa is demand rank **2** for spices on both gross demand `c` (0.03438 against
`hangzhou`'s 0.03517) and net demand `−b`. `hangzhou` is rank 1, is the Phase-1 selection, and is not
a sink; Genoa reaches the sink set as a *stall promotion*.

---

### X129 — Sinks are 1 to 7 per good; sinks at 14.5% in the top demand decile against 6.9% in the bottom
**Status:** CONFIRMED
**Method:** Re-ran `drainrep.py`'s sink-demand correlation block and an independent sink census.
**Evidence:** `DRAIN sinks/g 3.6 | P(top10) 14.5% | P(bot10) 6.9%`; sinks/good min 1, max 7 over 29/29
goods (independent recount min 1, max 7, mean 3.5862). The barbell (both tails above the mid-range)
reproduces.

---

### X130 — Zeroing `hangzhou`-node development moves the `Φ_w` sinks to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping
**Status:** CONFIRMED
**Method:** Re-ran `audit_delta.py` for the sink set and computed the flip count independently
(`_audit_b_measure.py`: zero the wealth of every province in the node, re-solve `Φ_w` at α_Φ = 1.5,
count edges whose direction reverses).
**Evidence:** sinks `['doab', 'english_channel', 'gulf_of_siam', 'sevilla']`; **flips 22**, unchanged
137, total 159.

---

### X131 — `hangzhou`, not `beijing`, is China's wealth pole: `c_w` rank 1 vs 31, node wealth 245.0 vs 143.8, richest single province
**Status:** CONFIRMED
**Method:** Re-ran `audit_delta.py` and `audit_delta2.py`; recomputed node wealth and `c_w` ranks
independently.
**Evidence:** `hangzhou` `c_w` rank 1, node wealth 245.0; `beijing` `c_w` rank 31, node wealth 143.8;
richest single province pid 1821 (`hangzhou`) at 30.40 against Beijing's 19.5. All four figures match.

---

### X132 — Zeroing `beijing` also moves the map — 17 flips, sinks `{doab, english_channel, hangzhou, sevilla}` — deleting 1.3% of world wealth; `hangzhou` survives there and does not survive the converse
**Status:** CONFIRMED
**Method:** Same construction as X130.
**Evidence:** sinks `['doab', 'english_channel', 'hangzhou', 'sevilla']`; **flips 17**; `beijing` node
wealth 143.8 of world 10,677.5 = **1.346%** → "1.3%". `hangzhou` is in the sink set when `beijing` is
zeroed and absent when `hangzhou` is zeroed, exactly as the row says.

---

### X133 — Ming losing the Mandate moves nothing on the day it happens: the Mandate is an owner property and §1.3 reads none
**Status:** CONFIRMED
**Method:** Checked the model's inputs, then checked what the game's Mandate modifiers actually touch,
in `common/static_modifiers/00_static_modifiers.txt`.
**Evidence:** `solver.province_table()` reads `base_tax`, `base_production`, the province's trade
good, its price and place-scoped local modifiers only — no owner field anywhere. The Mandate's
modifier blocks are `positive_mandate`, `negative_mandate` and `lost_mandate_of_heaven`; the only
trade-quantity term in any of them is `global_trade_goods_size_modifier = -0.5`, country-scoped, and
that is exactly the modifier §1.3/§3.13 classify as out-of-model. So the demand vector is provably
unchanged on the day and the row is an owner-agnosticism check. (The design cost is real and the spec
owns it elsewhere: a −50% goods-produced hit across Ming is deliberately invisible to the model until
it reaches `base_tax`/`base_production`.)

---

### X134 — The 8.96% run-to-run drift spans the five node fields, and the three power-dependent fields inherit the randomised AI merchant placement
**Status:** CONFIRMED
**Method:** Independent — parsed `VANILLA_start.eu4` and `VANILLA2_start.eu4` directly (ZIP →
`gamestate` → `trade={ node={…} }`) with my own parser and recomputed all five fields
(`_audit_b_saves.py`), without reading the v2 table for the numbers.
**Evidence:** `current` 49/77 differ, `local_value` 30/79, `outgoing` 37/66, `total` 1/79, `retention`
0/80; union of nodes differing on any field **49 of 80**. Worst relative difference **8.9593%** on
`local_value` at `siberia` (1.451 vs 1.581), reproducing 8.96% under the "relative to run 1"
convention — the same convention gives 7.20% and 7.19% on `current` and `outgoing`, matching the
source's other two figures, so the convention is consistent. The three fields that move are exactly
the power-dependent ones; `total` and `retention` are the structural pair.

---

### X135 — `retention` identical on 80 of 80 nodes and `total` on 78 of 79, the exception `zambezi` drifting 0.012%
**Status:** CONFIRMED
**Method:** Same independent save parse.
**Evidence:** `retention` 0 of 80 differ; `total` 1 of 79 differ, and the one is **`zambezi`**, 147.384
vs 147.366 = **0.0122%**. All three figures exact. (v3's `validation-v3.md` phrases the same result as
"79 of 80"; the difference is only whether the one node carrying no `total` field is counted in the
denominator. X135's "78 of 79" matches the underlying per-field table.)

---

### X136 — 2-core containment is asserted unconditionally against `{selected} ∪ {promoted} ∪ {fallbacks}`, because the narrower set would halt on T3
**Status:** CONFIRMED
**Method:** Proved the containment (X012/X147), then checked the design rationale against T3.
**Evidence:** Containment over the wide set held in 11,381 of 11,381 random instances and follows from
the readiness rule directly. On T3, `{selected} ∪ {promoted} = ∅` while the sink set is `{A}`, so the
narrow assertion halts on behaviour the spec elsewhere calls correct. The rationale is sound, and the
fallback set is doing assertion work rather than escape-clause work: an escape clause would be a
disjunct that absorbs *any* mismatch, whereas `{fallbacks}` is a set the sweep maintains and can be
checked against independently.

---

### X137 — Equality is monitored with T2 and T3 named as the two ways it can fail; measured exact on 1444, 29/29 goods, zero fallbacks
**Status:** CONFIRMED
**Method:** Reproduced the measurement and proved the two named failure modes exhaustive inside the
2-core.
**Evidence:** Measurement: `final.py` V029 29/29 with `mismatches: []`, 0 fallbacks; independently
recomputed 29/29. Exhaustiveness: see X116 — a promoted or fallback-promoted node can never lose
sinkhood, and a core sink outside the formula must be a fallback, so the only failures are "a selected
flow-terminal demander loses sinkhood to a free edge" (T2) and "a fallback promotion is a sink" (T3).
Random search found no third mode across 3,075 equality failures.

---

### X138 — Goal 1's worked example is a horde razing `hangzhou`, not Beijing
**Status:** CONFIRMED
**Method:** Read §3.1 Goal 1; checked the fact it rests on.
**Evidence:** §3.1 reads "A horde razing `hangzhou` moves the sink because the wealth moved." The
underlying fact holds (X130/X131): `hangzhou` is the `c_w` rank-1 node and zeroing it relocates the
sink set.
*Minor:* the example is stated at node granularity while EU4's raze acts on one province, and the
measurement zeroes an entire node's wealth — directionally right, larger than one raze action.

---

### X139 — Supply is sparse where demand is dense: spices produced in 18 of 80 nodes and cloves in one, while every node with an owned province carries demand
**Status:** CONFIRMED
**Method:** Recounted from `build_sc` with no regularizer.
**Evidence:** spices produced in **18 of 80** nodes, cloves in **1 of 80**; both demanded in **79 of
80**. The single non-demanding node is `cape_of_good_hope`, which is also the only node with zero node
wealth — i.e. the only node with no owned province, so "every node with an owned province carries
demand" is exact rather than approximate.

---

### X140 — With no regularizer the spices supply ratio over producing nodes is 36 against a demand ratio of 482.2
**Status:** CONFIRMED
**Method:** Re-ran `audit_delta.py` §3 and `v5measure.py` section E.
**Evidence:** "spices supply max/min over producing nodes **36.0** (18 nodes)"; "spices demand max/min
over demanding nodes **482.2** (79 nodes)". Over all 29 goods: supply contrast 4…97, demand contrast
211…2.04e+04 — the demand side is the wider one, which is the reversal the claim asserts.

---

### X141 — Sparsity is the asymmetry that survives the regularizer's deletion, and the diagnosis rests on it
**Status:** CONFIRMED
**Method:** Three measurements rather than an appeal to plausibility: (a) that the *contrast* asymmetry
reverses without the ε floor; (b) that the sparsity asymmetry does not; (c) that the quantity the v1
sink rule compares against — the neighbour-`φ` spread — actually tracks supply geography rather than
demand.
**Evidence:** (a) supply 4–97 against demand 211–20,400 across the 29 goods (X140). (b) producers 18/80
and 1/80 against demanders 79/80 (X139). (c) computing the v1 potential per good and correlating the
per-node neighbour spread `mean(φ_nbr) − min(φ_nbr)`: correlation with "has a producing neighbour" is
**0.787** for cloves and **0.357** for spices, against **0.128** and **0.172** for mean neighbour
demand. The threshold side is set by where supply is, as the diagnosis says.
*Flagged for the author, not scored here (it belongs to the UNCHANGED §3.2 sentence, not to X141):*
the neighbouring claim "deleting demand variation entirely left the sink unmoved" did **not** reproduce
in my reconstruction — replacing `c` with a uniform `1/N` moved the LAP spices sink set from
`{saxony}` to six nodes, and the cloves set from `{deccan, kongo, safi, wien}` to
`{kongo, krakow, safi, white_sea}`. My reconstruction of v1's ε machinery may differ from the original
experiment; worth re-deriving before that sentence is relied on again.

---

### X142 — Better wealth inputs plausibly deliver about 1.7× — measured, `genua` becomes a co-sink at ×1.720
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py` section F.
**Evidence:** "spice-sink threshold, genua ×1.720 (7.4% of world spice demand)".

---

### X143 — A spice sink at any of the four Chinese trade nodes needs 3.6–4.9×, i.e. 9.3–21.4% of world spice demand
**Status:** PARTIAL
**Method:** Reproduced all four node figures, then checked the "i.e." as a restatement.
**Evidence:** All four pairs reproduce exactly: `beijing` ×3.595 / 9.3%, `hangzhou` ×3.825 / 21.4%,
`xian` ×4.594 / 12.3%, `canton` ×4.855 / 17.8%. The multiplier range 3.6–4.9× is right and the
percentage range 9.3–21.4% is right. But the map from multiplier to share is **not monotone** and the
two ranges' endpoints belong to different nodes: the ×-maximum is `canton` at 4.86×, whose share is
17.8%, while the %-maximum is `hangzhou` at 21.4%, whose multiplier is 3.83×. "i.e." asserts a
restatement, so the sentence licenses the false inference "4.9× ⇒ 21.4%". (The per-node pairs follow
immediately in the same parenthesis, so a careful reader can recover the truth; a skimming one cannot.)
**Should say:** "…needs **3.6–4.9×**, which across these four nodes corresponds to **9.3–21.4%** of all
world spice demand at one node — the two ranges are not aligned end to end, because the share a
multiplier buys depends on the node's starting demand."

---

### X144 — `girin`, `yumen`, `chengdu`, `lhasa` need 4.0× to 10.8×
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py` section F.
**Evidence:** girin ×3.972, yumen ×4.516, chengdu ×8.202, lhasa ×10.751 → 4.0× to 10.8× after
rounding. Both endpoints check out.

---

### X145 — Sink placement holds where Phase 0 is a no-op and no fallback fires; three constructed inputs break it, all run through a faithful implementation of §1.1
**Status:** PARTIAL
**Method:** Ran `toys.py`, re-ran T1/T2/T3 through an independent implementation written from the spec
text, then tested the antecedent.
**Evidence:** The second half is confirmed twice over: `toys.py` and the independent implementation
produce identical output on all three cases (T1 sinks `{C}` vs formula `{B}`, with the restored edge
B→C; T2 `{u2}` vs `{u1,u2}`, with the free edge oriented u1→w; T3 `{A}` vs `∅`, with B→A, C→A, C→B).
The first half fails for the same reason as X013: **T2 itself satisfies "Phase 0 is a no-op and no
fallback fires"** — `Plog` empty, `fallbacks` empty — and breaks the equality. Two of the three named
breakers (T2, T3) sit inside the antecedent's own scope; only T1 needs Phase 0.
**Should say:** "Sink placement is *measured* exact on 1444, where Phase 0 is a no-op and no fallback
fires; those two conditions are necessary, not sufficient — T2 satisfies both and still breaks the
equality. Three constructed inputs break it…"

---

### X146 — T3 worked: triangle with `b = 0` and wealth 3, 2, 1; fallback promotes A; free edges orient B→A, C→A, C→B; sinks `{A}`, formula empty
**Status:** CONFIRMED
**Method:** `toys.py` plus the independent implementation.
**Evidence:** Both give `S0 = ∅` (no demander, so Phase 1 selects nothing), every edge free (zero
flow), a stall with no flow-terminal demander, `fallbacks = {A}`, directed edges `{B→A, C→A, C→B}`,
actual sinks `{A}`, formula set `∅`, and A in neither `{selected}` nor `{promoted}` — every element of
the worked example reproduces.
*Cross-reference:* T3's wealths are **distinct**, which is what refutes X125 and X151 and weakens
X010. Within T3 the index does still decide one edge (C→B), through the priority key `(0, 0, index)`,
not through the wealth key.

---

### X147 — What survives unconditionally is the ⊆-direction within the 2-core over `{selected} ∪ {promoted} ∪ {fallbacks}`; pendant net-importers are the only sinks outside that set
**Status:** CONFIRMED
**Method:** Proof plus brute force.
**Evidence:** Proof: a node is popped only if it is in `Sset`, has a flow out-arc, or has a free edge
to an already-marked node; the second gives it a flow out-arc and the third orients that free edge
outward (later-marked → earlier-marked), so any core node with no out-arc was popped as a member of
`Sset` = selected ∪ promoted ∪ fallbacks. Outside the core, Phase 4 makes a peeled node a sink iff its
folded balance is negative — a net-importer. Brute force: **0** containment violations in 11,381
random instances; **0** sinks outside the four-way taxonomy in 7,110 instances (X012).

---

### X148 — Sink placement is checked at runtime as two checks: containment asserted unconditionally, equality monitored with T2 and T3 named as its legitimate failures
**Status:** CONFIRMED
**Method:** Read §2.8's "Sink set, 2-core" row and §2.9's assertion list against the claim.
**Evidence:** §2.8 states both checks with the split exactly as claimed ("halt only on a containment
miss"; "Report an equality miss with the node and the good"), and §2.9's solver-track list carries
"2-core sink containment in `{selected} ∪ {promoted} ∪ {fallbacks}`" plus "the per-tick sink-set
equality monitor". Both named failures are legitimate (X014, X116) and both are reachable inside the
2-core, so monitoring rather than asserting is the correct disposition for the equality.

---

### X149 — Written against the narrower containment set, T3 would halt the solver on correct behaviour
**Status:** CONFIRMED
**Method:** Evaluated the narrow assertion on T3's output.
**Evidence:** On T3, `{selected} ∪ {promoted} = ∅` and the sink set is `{A}`, so
`sinks ⊆ {selected} ∪ {promoted}` is **False** while `sinks ⊆ {selected} ∪ {promoted} ∪ {fallbacks}`
is **True** — printed directly by `toys.py` and reproduced independently. The algorithm is behaving as
specified, so the narrow assertion would halt on correct behaviour.

---

### X150 — Free-edge direction is deterministic by construction; that the node indexing never decides is measured, not proved, and holds where the key has no exact ties — zero exact `(DEF, b)` ties, 29/29
**Status:** CONFIRMED
**Method:** Reproduced the measurement and tested the sufficiency direction on random graphs.
**Evidence:** 0 exact ties over 2,323 free-edge endpoint pairs on 1444 (independent recount), and 0
instances of "no exact tie yet index-dependent" over 3,897 random graphs. Unlike X016 this row says
"holds **where**", which is the correct sufficient-condition form.

---

### X151 — The one place the indexing is load-bearing is the fallback branch (T3), where the candidates are typically all zero-wealth and tied
**Status:** REFUTED
**Method:** Searched for index-decided orientations with no fallback, holding the LP support fixed so
the LP could not be the cause; and checked T3's own wealths and 1444's wealth field.
**Evidence:** Both halves fail. (i) "The one place": **2,774 of 7,146** random instances changed
orientation under a node relabelling with an **identical flow support and no fallback anywhere**.
Minimal example — nodes 0..3, edges {01, 03, 12, 13, 23}, `b = (−2, 1, 1, 0)`: nodes 1 and 2 key
exactly `(DEF 2.0, b 1.0)`, so the free edge {1,2} is oriented by index alone; five of the 24
relabellings flip it, support unchanged, `fallbacks = ∅`. This is the same mechanism X016/X150 already
concede ("exact `(DEF, b)` ties"), so X151 contradicts its own neighbours. (ii) "T3, where the
candidates are typically all zero-wealth and tied": T3's candidates carry wealth **3, 2, 1** — the
wealth key decides the promotion and does not tie. On 1444 it cannot tie either: `NODEW` is
80-of-80 distinct.
**Should say:** "The indexing is load-bearing wherever the priority key ties exactly — on 1444 it
never does (zero `(DEF, b)` ties, 29/29 goods) — and, additionally, on the fallback branch when the
candidates' wealths are also equal. §2.4 item 1 makes a canonical node order a correctness requirement
for the general case, not for the fallback branch specifically."

---

### X152 — 13 of 30 goods can be pushed strictly below 2.0 by a single vanilla `change_price` event
**Status:** CONFIRMED
**Method.** Independent whole-install census (`_audit_d_census.py`: byte-level walk of every
non-binary file, quote-aware comment stripping, brace-matched block extraction — no `pdx.py`, no
`w10.py`), then an independent partition (`_audit_d_partition.py`) against an independently parsed
`common/prices/00_prices.txt`. Semantics established from shipped save data, not assumed.
**Evidence.** **Semantics first:** `change_price` `value` is a **fraction of base price**, not a
ducat delta. `tutorial/eu4_tutorial_chapter10.eu4` (a save) has `paper { current_price=4.375,
change_price{ key="PAPER_IN_BUREAUCRACY" value=0.250 } }` — paper base 3.5, and 3.5 × 1.25 = 4.375,
not 3.5 + 0.25 = 3.75 — and `gems { current_price=5.000, value=0.250 }` with gems base 4.0 →
4.0 × 1.25 = 5.0. Both are decisive.
Partition under fractional semantics, denominator = the 30 goods with `base_price > 0` in
`00_prices.txt` (32 entries less `gold`, base 0/`goldtype = yes`, and `unknown`, base 0):
**13 below 2.0** — grain 0.625, wine 0.625 (both `HUAYNAPUTINA`, −0.75, 2.5 × 0.25), glass 1.05,
slaves 1.2, chinaware 1.5, copper 1.5, livestock 1.5, paper 1.75, coffee 1.8, spices 1.8, fish
1.875, incense 1.875, wool 1.875. The denominator does **not** include gold. The claim's other
premise also holds: the minimum tradeable base price is exactly 2.0, at exactly the six goods §3.5
names (`fur`, `livestock`, `naval_supplies`, `slaves`, `tea`, `tropical_wood`).

---

### X153 — two land exactly on 2.0 (`gems`, `silk`); four have a negative event not reaching 2.0; eleven have none
**Status:** CONFIRMED
**Method.** As X152; every bucket enumerated by name.
**Evidence.** **Exactly 2.0 (2):** `gems` (base 4, `BRAZILIAN_DIAMONDS` −0.50 → 2.0), `silk` (base 4,
`PERSIA_SILK_FLOOD` −0.50 → 2.0). **Negative but above 2.0 (4):** `cloth` (−0.15 → 2.55), `coal`
(−0.30 → 7.0), `dyes` (−0.25 → 3.0), `iron` (−0.15 → 2.55). Checked against stacking too: summing
*all* negatives per good leaves all four above 2.0 (dyes 4 × 0.60 = 2.4 the closest), so no reading
moves them. **No negative event at all (11):** `cloves`, `cocoa`, `cotton`, `fur`, `ivory`,
`naval_supplies`, `salt`, `sugar`, `tea`, `tobacco`, `tropical_wood`. Partition sums 13 + 2 + 4 + 11
= **30** exactly.

---

### X154 — all 161 `change_price` blocks parsed: 93 events, 14 missions, 1 common, 53 history of which 13 negative, all in `HAB - Austria.txt`
**Status:** PARTIAL
**Method.** Byte sweep of every non-binary file in the install (not just `.txt`); DLC `.zip`
archives opened and searched; per-file raw counts and comment-stripped counts compared; brace-matched
extraction of every block.
**Evidence — the counts all reproduce exactly.** events **93** (PriceChanges 65, FlavorPER 12,
FlavorSWE 6, flavorMAL 2, and 1 each in flavorBYZ, FlavorGBR, flavorHOL, flavorITA, flavorJOL,
FlavorTUR, flavorYEM, USADLC), missions **14**, common **1**
(`parliament_issues/01_english_parliament_actions.txt`), history **53** — total **161**, comment
stripping changes nothing. History negatives: **13**, and *every* history block, not just the
negatives, is in `history/countries/HAB - Austria.txt`. `decisions/` — the fifth of the "five trees"
the spec alludes to but never names — contains **0**. The 84 DLC `.zip` archives contain **0**. The
only other occurrences anywhere in the install are 1 in `patchnotes/1.8 Patchnotes.txt`
(documentation) and 14 in `tutorial/*.eu4` (save state, `current_price` records).
**Should say — 7 of the 14 "missions/" blocks are not effect blocks.** They sit inside *quoted
strings*: `country_event_with_insight { effect_tooltip = " … change_price = { … } " }` and
`country_event_with_effect_insight { effect = " … " }`. A quoted string is a single token to the
engine's parser; these are display text and are never executed. The seven are:
`DOM_Britain_Missions` (1), `KoK_Byzantine_Missions` (1), `KoK_Persia_Missions` (3),
`KoK_Yemen_Missions` (1), `WOC_Italian_Missions` (1). Six of the seven are verbatim duplicates of a
block already counted in `events/` (BYZ_growing_demand, PERSIAN_SILK/PERSIAN_DYES/PERSIAN_CLOTH,
YEM_coffee_price_boost, ITA_wine_upgrade). The seventh, `ENGLISH_FUR_TRADE`, occurs nowhere in the
install except that tooltip string and four localisation files — the effect it previews is
`flavor_gbr.7`, which uses key `FUR_TRADE`. The count of **executable** `change_price` blocks is
therefore **154**, with **7 in `missions/`** — which is exactly what v4.0 said. §3.5 should say
"161 textual occurrences, of which 154 are executable; 7 sit inside `effect_tooltip` / insight
strings and duplicate effects counted elsewhere." The partition (X152/X153) is unaffected either way.

---

### X155 — v4.0's 154 came from a bare `except` hiding five mission files; the scan is now guarded by a per-file count assertion
**Status:** REFUTED
**Method.** Ran `pdx.load` + the author's walker over every `change_price`-bearing file, recording
exceptions separately from recovery shortfalls; read `w10.py` and `validate_v5.py`.
**Evidence.**
1. **No exception is raised, so the bare `except` hid nothing.** `pdx.load` parses all five mission
   files without error; brace counts and quote counts are balanced in each. The blocks are lost
   because `pdx.TOK`'s first alternative is `"[^"]*"` — the whole multi-line `effect_tooltip = "…"`
   / `effect = "…"` string becomes one opaque token, so the walker never sees the block. Measured:
   0 files failed to parse; exactly 5 files recovered fewer blocks than they contain
   (DOM_Britain 1→0, KoK_Byzantine 1→0, KoK_Persia 3→0, KoK_Yemen 1→0, WOC_Italian 1→0 = 7 lost);
   total recovered 154.
2. **There is no per-file count assertion.** `w10.py` — the script `scripts/README.md` credits with
   producing §3.5's partition — still contains `except Exception: pass` and no assertion at all.
   `validate_v5.py` l.238–241 accumulates a **per-tree** regex count and asserts the tree totals
   `(161, 93, 14, 1, 53)`; that census is never compared against the `pdx` walk, whose `hits` list
   still holds 154 blocks and is what the partition is computed from. The guard as built cannot
   detect a per-file loss and does not detect this one.
3. **The conclusion is also wrong in substance, and so is v4.0's.** Classifying all 161 blocks by
   whether they sit inside a quoted string or inside a `tooltip = { … }` wrapper — EU4's explicit
   "display this, do not execute it" construct — gives **10 non-executable blocks, not 7**:
   - 7 inside quoted `effect_tooltip = "…"` strings: `DOM_Britain_Missions.txt:919` (fur 0.25),
     `KoK_Byzantine_Missions.txt:2070` (silk 0.2), `KoK_Persia_Missions.txt:3384/3390/3396`
     (silk 0.25, dyes 0.5, cloth 0.35), `KoK_Yemen_Missions.txt:954` (coffee 0.25),
     `WOC_Italian_Missions.txt:2841` (wine 0.4);
   - 3 inside `tooltip = { … }` blocks, which `pdx.py` parses and therefore counts:
     `WOC_Hisn_Kayfa_Missions.txt:1448` and `:1459` (grain 0.1 twice — the `if`/`else` display pair
     whose executable twin is at `:1493`), and `events/flavorMAL.txt:1736` (ivory 0.33, inside
     `option = { … tooltip = { … } }`).
   So `missions/` holds 14 blocks of which only **5** are executable, and the executable total
   across the install is **151** — neither v5.0's 161 nor v4.0's 154.
   **The partition is untouched:** all 10 non-executable blocks are positive (0.1–0.5), and all
   40 negative blocks in the install are executable — `events/PriceChanges.txt` 22,
   `events/FlavorPER.txt` 3, `events/FlavorSWE.txt` 2, `history/countries/HAB - Austria.txt` 13.
   Every §3.5 conclusion (13 goods below 2.0, 2 on 2.0, 4 non-reaching, 11 with no negative event)
   stands exactly as written.
**Should say:** "All **161** `change_price` blocks were parsed — 93 in `events/`, 14 in `missions/`,
1 in `common/` and 53 in `history/`, of which 13 are negative, all in
`history/countries/HAB - Austria.txt`. **Ten of the 161 are display text** — seven inside quoted
`effect_tooltip` strings and three inside `tooltip = { }` wrappers — so the executable count is
**151**. v4.0's 154 excluded the seven quoted ones (silently, through a bare `except`) and kept the
three wrapped ones; v5.0's 161 keeps all ten. All ten are positive, so the partition below is
unaffected either way."

---

### X156 — `wool`'s largest single negative is `HAB - Austria.txt`'s `NEW_DRAPERIES` −0.25 → 1.875, against −0.20 for the same key in `events/PriceChanges.txt`
**Status:** CONFIRMED
**Method.** Extracted all eight shipped `wool` blocks; located the history date; read the event's
trigger.
**Evidence.** All eight wool blocks: `COTTON_IMPORTS` −0.10 and `NEW_DRAPERIES` −0.20,
`REGULATED_UNIFORMS` +0.10, `SELECTIVE_BREEDING` +0.35 in `events/PriceChanges.txt`;
`COTTON_IMPORTS` −0.10, `NEW_DRAPERIES` **−0.25**, `REGULATED_UNIFORMS` +0.10, `SELECTIVE_BREEDING`
+0.25 in `history/countries/HAB - Austria.txt`. The minimum is −0.25 and it is in the history file
✓. Under fractional semantics 2.5 × (1 − 0.25) = **1.875** ✓, and the `events/` version gives
2.5 × 0.80 = 2.00 exactly. The history block is dated **1540.1.1** ✓, and that same dated block sets
`new_draperies_happened`, which is precisely the global flag `prices.13`'s trigger tests
(`NOT = { has_global_flag = new_draperies_happened }`) — so past 1540 the −0.20 event can no longer
fire and, keys being keyed, 1.875 is what a campaign reaching 1540 holds ✓.
*Presentation note (not a refutation):* the spec writes the value as "−0.25" with no unit, alongside
prices in ducats, and never states anywhere that `change_price` values are fractions. A reader doing
2.5 − 0.25 gets 2.25 and a contradiction. Every §3.5 figure is right under the fractional reading;
one sentence saying so would close the ambiguity.

---

### X157 — v2's 13 was right; v3.0 reached 12 by parsing four of the five trees
**Status:** CONFIRMED
**Method.** Re-ran my partition with `history/` removed, and read v3.0's own §3.5 text.
**Evidence.** Dropping `history/` moves exactly one good: `wool`'s deepest negative becomes −0.20 →
2.5 × 0.80 = 2.0 exactly, so the partition becomes **below 12 / exact 3 (`gems`, `silk`, `wool`) /
above 4 / none 11**. That is v3.0's published partition verbatim (`v3-owner-agnostic` l.860–863:
"**12 of 30 goods** … three more — `gems`, `silk`, `wool` — land *exactly on* 2.0"), and v3.0's own
parenthetical names the omission: "All 101 `change_price` blocks in `events/`, `decisions/`,
`missions/` and `common/` were parsed; `history/` contributes only positive entries" — four trees,
and the history claim is false. Dropping `missions/` or `common/` instead changes nothing, so
`history/` is the unique cause. And 13 is the correct figure.

---

### X158 — 92.2% (5825 of 6320) of ordered node pairs connected by at least one good
**Status:** CONFIRMED
**Method.** Rebuilt `S − C` from `solver.build_sc(eps=0)`, ran DRAIN per good, and did my own BFS
per source over each good's directed edge set, unioning the reachability matrix
(`_audit_d_conn.py`).
**Evidence.** N = 80, N×(N−1) = **6320** = 80 × 79 ✓. The diagonal is never set (the accumulation
guards `t != s`), so self-pairs are excluded ✓. Connected ordered pairs = **5825**, 92.1677% →
**92.2%** ✓. For contrast, the unordered variant would be 3141/3160 = 99.4%, so the "ordered" reading
is load-bearing and is the one the spec uses.

---

### X159 — `genua`, `gulf_of_siam` and `sevilla` rank 3rd/2nd/7th at 296.0/299.2/266.5 against `english_channel`'s 316.6, none a sink
**Status:** CONFIRMED
**Method:** `_audit_a_main.py` — recomputed node wealth from `solver.ROWS` and both rank vectors;
cross-checked against `phiw3.py`'s V215 block.
**Evidence:** `english_channel` 316.6 (rank 1), `gulf_of_siam` 299.2 (rank 2), `genua` 296.0
(rank 3), `sevilla` 266.5 (rank 7). None of the four is a sink — the only sink is `hangzhou`
(245.0, rank 10), so the readings are mutually consistent with X070. Directional check on the
"draws more edges in than it sends out" clause: `genua` has out-degree 2
(`alexandria`, `ragusa`) on a degree-≥4 node, and `english_channel` has out-degree 1 — both are net
in-drawers that nevertheless pass flow onward, as claimed.

---

### X160 — `Φ_ord`: 13 ends, 8 terminate no good, 11–17 across cloves-α 2…64; v2's "9–17" wording
**Status:** PARTIAL
**Method:** `v5measure.py` §D for the baseline; `_audit_a_main.py` and `_audit_a_clovesalpha.py`
for the α sweep. No script in the toolchain produces the 11–17 figure, so I reconstructed the
measurement: §3.13 fixes the parameterisation ("α unclamped at exponent 2 (cloves α = 16)"), i.e.
`α(g) = (price(g)/2)^e` with cloves' price 8.0, so cloves-α ∈ {2,4,8,16,32,64} ⇔ e ∈ {0.5,1,1.5,2,2.5,3}.
**Evidence:**
- 13 end nodes at 1444 ✔ (`amazonas_node, australia, basra, beijing, chengdu, deccan, james_bay,
  katsina, laplata, ragusa, rheinland, safi, white_sea`).
- 8 terminate no good ✔ (`amazonas_node, basra, beijing, chengdu, james_bay, katsina, ragusa,
  white_sea`).
- "none of the demand capitals is among them" ✔ — the top-5 `c_w` nodes
  (`hangzhou, genua, english_channel, gulf_of_siam, champagne`) are all absent from the 13.
- **11–17 reproduces exactly** under the unclamped-exponent family: ends = 16, 13, 15, 17, 15, 11
  at cloves-α = 2, 4, 8, 16, 32, 64 → range **11–17**, baseline 13 at e = 1. (Two rival readings
  fail: a global constant α gives 10–15; scaling only cloves' α gives a flat 13–13. The
  §3.13 reading is the right one and it lands on the quoted range.)
- **The final clause is false.** The spec says v2's "9–17 ends" is "neither the right word for a
  quantity that ranges 11–17 **nor a band containing its own baseline of 13**." But 9 ≤ 13 ≤ 17 —
  9–17 *does* contain 13. This is a regeneration artifact: `changes-v5.md` entry 38 shows the v4.0
  text read "a quantity that ranges 13–22 nor a band containing its own baseline of **18**", where
  the complaint was sound because 18 > 17. When the figures were regenerated on the corrected
  wealth field (range → 11–17, baseline → 13) the numbers were substituted but the argument was
  not re-checked, and it silently became false.
**Should say:** drop the second complaint. "v2 called this 'α-invariant … 9–17 ends', which is not
the right word for a quantity that ranges 11–17" is true and sufficient; if a second point is
wanted, the honest one is that v2's *range* (9–17) was measured on the pre-correction field and
does not reproduce (11–17 does).

---

### X161 — `Φ_w` is adopted for one operator, one set of guarantees, and ends that move with the world
**Status:** CONFIRMED
**Method:** `_audit_a_misc.py` — tested each named guarantee on `Φ_w` itself rather than on the
per-good graphs (`v5measure.py` only tests scan-invariance for the 29 goods).
**Evidence:** `Φ_w` is produced by `run_drain(b_w)`, the same §1.1 entry point the per-good graphs
use — no separate code path. Guarantees, measured on `Φ_w`:
- LP feasibility: Phase 2 solves; 159/159 edges oriented.
- Acyclicity: `has_cycle` → None.
- Determinism: 6 repeat solves give one orientation.
- Scan-invariance: **0 orientation flips over 20 random node-index permutations**; 0 exact
  `(DEF, b)` ties on free edges, so no tie-break is load-bearing.
- Correctness check: exact orientation equality is a set comparison, no tolerance (§2.8).
"Ends that move with the world" is separately established by X085/X086/X101.

---

### X162 — The "two vanilla-like ends at 1444" premise is withdrawn: there is one end, in China, matching none of vanilla's three
**Status:** CONFIRMED
**Method:** `audit_alpha.py` (old vs corrected field) plus the direct `00_tradenodes.txt` read.
**Evidence:** the old field at α_Φ = 1.5 gave `['english_channel','hangzhou']`, one of which
(`english_channel`) is a vanilla end — that is the premise being withdrawn. The corrected field
gives `['hangzhou']`, and vanilla's ends are `genua`, `venice`, `english_channel`, so `hangzhou`
matches none. The withdrawal is warranted and §3.9 states it plainly.

---

### X163 — The trade is 7.8 points of self-coherence for one operator and world-responsive ends
**Status:** CONFIRMED
**Method:** As X075 — recomputed both operators under both weightings so the 7.8 could be checked
for like-for-like construction.
**Evidence:** 60.3% − 52.5% = **7.76** points, both unweighted, same 4611-pair denominator. The
figure is stated against a matched pair. (The value-weighted equivalent is 8.45 points; the spec
does not quote it, and does not claim it.) The rest of the claim restates X161 and X085, both
confirmed.

---

### X164 — the income factoring is an identity, not a measurement
**Status:** CONFIRMED (as a derivation), on one premise that carries the whole claim
**Method:** Attacked the algebra under §1.8 as written, looking for any way to make either the
collector *set* or a collector's *power* depend on `g`; then checked the arithmetic in `audit_f4.py`.
**Evidence:** The identity is `Σ_g value_g·collected_share(n,g)·powershare_C(n) =
powershare_C(n)·Σ_g value_g·collected_share(n,g)` — distributivity, needing only that
`powershare_C(n)` carries no `g`. §1.8's per-good eligibility rule touches only `P_transfer(g)`,
i.e. the denominator *inside* `collected_share`, which is already inside the sum; it cannot move a
country between collector and non-collector. What makes `powershare_C` good-independent is §1.8's own
opening sentence, "Trade power and collect/transfer intent are node-wide": one intent per (country,
node), so the collector set is one set, not thirty. That is a stipulation of the model, not a fact
about the engine — so the property is true by construction, which is exactly what X164 claims.
Numerically the residual is 0 – 3.7e-16 across all five nodes, consistent with an identity in
doubles.
**Two gaps worth naming, neither fatal:**
1. The premise is load-bearing and is never cited in §3.10. §3.10's stated reason is the weaker
   "whether a country collects is a merchant-or-home property with no good dependence" — an argument
   about the *engine*; under §1.7 a home-node country that collects automatically and is also
   assigned to a newly-assignable incoming link would be a collector for some goods and a steerer for
   others. §1.8's node-wide-intent stipulation is what rules that out, and §3.10 should cite it.
2. At a sink where no country collects, `P_collect = 0` and `powershare_C` is 0/0: the scalar form is
   undefined where the per-good form pays 0. Immaterial at 1444, unstated.

---

### X165 — every term feeding a collector's power at a node is node-wide (four named)
**Status:** PARTIAL
**Method:** Tried to find a per-good power term. Read §1.7, §1.9, §1.10, §3.11 and §3.14; then swept
`eu4.exe`'s string table for every `*trade_power*` key and `defines.lua` for every trade-power
constant, checking whether any takes a trade-good argument.
**Evidence — the conclusion survives.** The engine's entire trade-power modifier vocabulary is
`global_trade_power`, `global_own_trade_power`, `global_foreign_trade_power`,
`global_prov_trade_power_modifier`, `global_ship_trade_power`, `province_trade_power_modifier`,
`province_trade_power_value`, `ship_trade_power_modifier`, `trade_power_in_fleet_modifier`,
`caravan_power`, plus `transfer_trade_power*`. **None takes a good argument**, so nothing can
reintroduce a `g` into a collector's power. The two terms the brief flagged are safe:
`TRADE_POWER_HOME_BONUS = 0.1` / `_MAX = 1` (defines.lua:1141-2) is a home-node property, and
`TRADE_ADDED_VALUE_MODIFER = 0.05` (:1204) — §3.14's "per-link multi-merchant boost" — multiplies
*value on a link*, not collector power at a node, so it lives inside `value_g(n)`, which is already
per-good in the identity.
**But the enumeration is not the set of terms.** The four named ("merchant bonus, off-home penalty,
propagation off the one installed graph, caravan grant") omit, among others: **provincial trade
power** (`p_pow` in the save — the dominant term at almost every node), `TRADE_CAPITAL_POWER = 5.0`
(:1195), `TRADE_POWER_HOME_BONUS`, light-ship power, privateer power (`PIRATES_TRADE_POWER_FACTOR`,
`PIRATES_MONOPOLY_BONUS`), embargo efficiency (`EMBARGO_BASE_EFFICIENCY`), the trading-policy
`power_modifier = 0.05/0.10` on `maximize_profit`, and the country modifiers listed above. A
four-item list standing in for "every term" is the wrong shape of warrant for a claim whose whole job
is completeness.
**Should say:** "No trade-power term in the engine takes a trade good as an argument — the modifier
vocabulary is `global_trade_power`, `province_trade_power_modifier`, `ship_trade_power_modifier`,
`caravan_power` and their siblings, all node- or country-scoped — so none can reintroduce a `g`",
with the four items as examples.

---

### X166 — the two forms agree to 0 to 3.7e-16 across five nodes on the real 1444 country tables
**Status:** PARTIAL
**Method:** Ran `audit_f4.py`; re-derived the same quantities at full precision in `_audit_c_f4.py`;
checked the ULP arithmetic; checked whether §3.10 states the construction.
**Evidence — the number reproduces exactly.** Single-graph worst relative disagreement: `sevilla`
0.0, `malacca` 2.1380e-16, `genua` 2.1712e-16, `champagne` 3.4985e-16, `gulf_of_siam` 3.6899e-16 →
"0 to 3.7e-16" ✓.
**Two defects.**
1. **The construction is not stated**, which is the exact failing X167 charges to v1–v4 ("produced by
   constructions none of those documents states"). §3.10 says only "using each node's real 1444
   country table". `audit_f4.py` additionally fixes: the three collectors are the top three tags by
   power; the transferrers are the next three; per-good transfer eligibility is drawn at random
   (`default_rng(11)`, p = 0.6); the propagated term is `Σ_downstream power / 5`; and the scalar
   form's powershare is frozen at `GL[0]` = **`chinaware`**, the alphabetically first live commodity.
   For X166 the choices do not matter (it is an identity), but the run is offered as evidence and the
   same construction carries X168–X172, where they matter a great deal.
2. **§3.10's gloss "at most one unit in the last place" is wrong.** `np.spacing(1.0) = 2.2204e-16`,
   so 3.6899e-16 is **1.66× the ULP spacing** — between roughly 1.7 and 3.3 ULP depending on the
   binade, never ≤ 1. (§3.14's "residuals sit at 1e-16, one ULP of a double" is loose the same way.)
**Should say:** "at most a few units in the last place", and state the construction (three collectors
= top three by power, randomised eligibility, powershare evaluated at one reference good) once.

---

### X167 - v1-v4's "5.7e-14" and "1.4e-14" are residuals of an exact identity, from constructions none of those documents states
**Status:** CONFIRMED
**Method:** Read all four earlier specs directly (`../../v1-laplacian/`, `../../v2-drain/`,
`../../v3-owner-agnostic/`, `../../v4-owner-agnostic/per-good-trade-spec.md`) and grepped each for
the two figures; checked whether any states a construction; checked whether either version shipped a
script that could have produced them; then asked the same question of v5.0 itself.
**Evidence:**
- Both figures are present in all four: v1 line 438 and v2 line 706 ("Verified numerically:
  agreement to **5.7e-14** across a node with mixed sinks, mixed collectors and the home-node penalty
  in play") and v1:440 / v2:708 ("reproduces per-good truth to **1.4e-14** ... off by 5.96 ducats on a
  node paying ~250"). v3 carries both verbatim, each tagged **[unverified in v3.0]** (v3:984, v3:986);
  v4.0 still carries both.
- **Construction stated: none.** "a node with mixed sinks, mixed collectors and the home-node penalty
  in play" names no node, no collectors, no eligibility rule. v1 and v2 ship no scripts directory at
  all, so nothing in either version could reproduce them; v3 has none either. So the figures are
  unreconstructable from the documents, exactly as claimed.
- **"Residuals of an exact identity" is right in kind.** The identity is exact (X164), so any honest
  run of it can only return a residual. The scale is consistent: v4.0's `factor.py` returns an
  absolute residual of 7.105e-15 ducats and a relative one of 1.295e-16 on a 97-ducat node, so an
  absolute figure of order 1e-14 on a larger construction is the same phenomenon. The strict
  magnitudes 5.7e-14 / 1.4e-14 cannot be reproduced (no producing code exists), but nothing about them
  can be evidence for anything either, which is the claim's point.
- **v5.0 repeats the failing, and this is the interesting part.** Sec 3.10 now names the five nodes
  (Sevilla, Genoa, Champagne, Malacca, Gulf of Siam) and says "each node's real 1444 country table" and
  "`collect_pool` built per good throughout" - genuinely more than v1-v4 said. It still does not state:
  which countries collect (`audit_f4.py`: the top three tags by `val`), which transfer (the next
  three), how eligibility is set (`default_rng(11)`, p = 0.6 per good), how the country table is built
  (the save's `val=` fields, not `province_power=` as v4.0's scripts used), or at which commodity the
  scalar powershare is evaluated (`GL[0]` = `chinaware`). For the 0-to-3.7e-16 residual none of that
  matters. For the 7.44% / 1.69% / 0.70% triples in the same paragraph all of it matters (X170, X172).
  So v5.0's own headline per-good figures are as unreconstructable from the document as v1's were.
**Note:** unlike v1-v3, v4.0 *did* ship the producing code (`../v4-owner-agnostic/scripts/factor.py`,
`audit_factor.py`, `audit_factor2.py`); X167's charge is about the documents, and holds for them.

---

### X168 — reading one installed graph leaves the identity untouched: same 0 to 3.7e-16
**Status:** CONFIRMED
**Method:** Same run; verified in the code that the single-graph propagated term is literally
`g`-independent (`prop(PHIW["directed"], c)` has no `g`), so no reference-good or seed sweep can move
it — checked by sweeping both anyway.
**Evidence:** identical figures to X166 (0.0 – 3.6899e-16). Note X166 and X168 quote **the same
measurement**: `audit_f4.py` computes exactly one "single graph" row per node and §3.10 reports it
twice, once as the identity check and once as the propagation check. Not an error, but the second
quotation adds no independent evidence.

---

### X169 — gulf_of_siam has eight distinct downstream sets and a 0.003% effect because its collectors hold almost nothing downstream
**Status:** REFUTED — on the count, on the mechanism, and on the figure
**Method:** Enumerated the downstream set of `gulf_of_siam` in each of the 29 live goods' directed
graphs; read the three collectors' power in `burma`, `canton`, `malacca` out of the save; compared
their share at the node with their share of the propagated increment.
**Evidence:**
1. **Seven, not eight.** The realised sets over the 29 live goods are `()` x9, `(burma, canton)` x7,
   `(burma, canton, malacca)` x4, `(burma,)` x4, `(canton,)` x2, `(burma, malacca)` x2,
   `(canton, malacca)` x1 — **7 distinct sets**, summing to 29. Eight is the size of the power set of
   its three neighbours; `(malacca,)` alone never occurs. (v4.0's breakdown — "twelve goods leave it
   with none at all, five drain to `burma`, four to `{burma, canton, malacca}`" — does not reproduce
   either: 9 / 4 / 4.) The solver carries 30 goods with `coal` latent, so 29 live is the right basis.
2. **The mechanism is false.** The three collectors are KHM / AYU / LXA. In `burma` they hold
   **9.839 / 9.783 / 6.485** — not "almost nothing": that is 3.7% / 3.7% / 2.4% of `burma`'s 267.35
   total, and their propagation increments (power/5) are 1.968 / 1.957 / 1.297 against node powers of
   54.172 / 53.897 / 37.403, i.e. about 3.6% of their own power each. In `canton` and `malacca` they
   hold exactly 0. The effect is tiny because of **proportionality, not smallness**: their share among
   the three collectors at the node is 0.372388 / 0.370497 / 0.257115 and their share of the `burma`
   holdings is 0.376872 / 0.374727 / 0.248401, so adding the `burma` term moves the share only from
   0.372388 to 0.372543. The stated driver — "whether its collectors hold differing power across the
   nodes those sets differ on" — is *satisfied* here (9.8 in `burma`, 0 in `canton`) and the effect is
   still 0.008%. The correct criterion is whether the downstream holdings are **non-proportional** to
   the node holdings.
3. **The figure understates.** Per collector the effect is +0.00269%, +0.00255%, -0.00759%; the worst
   is 0.0076% (about 0.008%), 2.8x the quoted 0.003%. Everywhere else in the same paragraph the spec
   quotes all three per-collector percentages; here it quotes the smallest. The effect is also an
   artifact of the collector count: 8.1e-7 at 2 collectors, 7.6e-5 at 3, 9.4e-2 at 4 (see X172).
**Should say:** "`gulf_of_siam` has **seven** distinct downstream sets and still shows only a
0.003%-0.008% effect, because its collectors' holdings in `burma` (9.8 / 9.8 / 6.5) are almost exactly
**proportional** to their holdings at the node and they hold nothing in `canton` or `malacca`, so the
propagation term barely moves the share."

---

### X170 — the error is redistributive, single-digit percent, sign varying by collector (nine figures)
**Status:** PARTIAL
**Method:** Reproduced `audit_f4.py`; then stressed the construction — reference good swept over all
29 live goods, eligibility seed swept over 20 values, collector count swept 2-5; checked whether
`Sum_c(b_c - a_c) = 0`; checked Champagne's apparent exact-negative pair at full precision.
**Evidence — the nine percentages reproduce exactly:** Sevilla -0.821 / -0.871 / **+7.439**;
Champagne -1.693 / +1.693 / +1.529; Genoa -0.232 / -0.218 / +0.701 (Malacca, unquoted, is +0.592 /
-0.529 / -0.285). Signs do vary by collector.
**"Redistributive" is stronger than a measurement — it is exact.** `Sum_c b_c = pool` and
`Sum_c a_c = Sum_g value*share = pool` identically, so the absolute errors sum to zero by construction
(measured `Sum(b-a)` = 3.6e-15 ... 2.1e-14, float noise). Worth stating as a theorem, not an
observation.
**Champagne's +/-1.693 is a near-coincidence, not a degenerate construction.** At full precision FRA
is -1.692985116% and BUR +1.692890558% — they differ in the fifth significant figure; incomes are
33.38 vs 23.88, so equal-and-opposite *relative* errors would contradict the exact zero-sum unless
ORL's error were zero (it is +1.529%). Nothing degenerate.
**But the specific triples are artifacts of the frozen reference good.** The scalar form must pick one
good at which to evaluate the powershare; `audit_f4.py` picks `GL[0]` = `chinaware`, the
alphabetically first live commodity. Sweeping that choice over all 29 goods: Sevilla's third collector
(MOR) ranges **-9.836% to +7.930%** and CAS -0.900% to +1.093%; Champagne's FRA ranges -2.505% to
+0.353% and BUR -0.631% to +3.196%; the worst-case relative error moves by up to **23x** (malacca
2.6e-4 ... 5.9e-3) and 7x (champagne). The sign pattern is not robust; the magnitudes broadly are. The
eligibility seed barely matters (20 seeds: worst case within +/-10%, one sign pattern per node) — so
the exposure is the reference good, not the seed.
**Should say:** quote the range over reference goods, or state that the powershare is evaluated at one
named reference commodity and that the per-collector signs are specific to that choice. As written the
nine numbers read as properties of the nodes.

---

### X171 — the error is thirteen orders of magnitude above the float residual
**Status:** PARTIAL (wrong at both ends of the set it is stated over)
**Method:** Arithmetic on the measured values against the 3.6899e-16 residual the same paragraph
quotes.
**Evidence:** `log10(worst_rel / 3.6899e-16)` per node — `gulf_of_siam` 7.59e-5 -> **11.31**;
`malacca` 5.92e-3 -> 13.21; `genua` 7.01e-3 -> 13.28; `champagne` 1.69e-2 -> 13.66; `sevilla`
7.44e-2 -> **14.30**. "Thirteen" is right only for malacca / genua / champagne. The paragraph states
it over the whole measured set — which explicitly includes `gulf_of_siam`'s 0.003% two sentences
earlier and Sevilla's +7.44% one sentence earlier — so it is two orders too high at one end and one
order too low at the other. ("Thirteen" is a survival from v4.0, where the only quoted effect was a
single 0.41% against a 1.3e-16 residual: 0.0041/1.3e-16 = 3.2e13.)
**Should say:** "eleven to fourteen orders of magnitude above the float residual".

---

### X172 — the size depends on which countries are collecting, a stated choice of the construction
**Status:** PARTIAL
**Method:** Swept the collector count 2-5 at each of the five nodes; swept the reference good;
searched Sec 3.10 and the whole spec for any statement of the construction.
**Evidence — the dependence is real and larger than implied:** at `gulf_of_siam` the worst relative
error goes 8.1e-7 (2 collectors) -> 7.6e-5 (3) -> 9.4e-2 (4) -> 1.0e-1 (5); at `sevilla`
3.0e-4 -> 7.4e-2 -> 7.3e-2 -> 3.8e-1; at `champagne` 2.0e-2 -> 1.7e-2 -> 3.9e-2 -> 3.3e-1 (and at 5
collectors one collector is at -32.7%, breaking "single-digit percent"). The caution is well founded.
**Two problems.**
1. **"a stated choice of the construction" is false — the choice is nowhere stated.** Sec 3.10 says
   only "using each node's real 1444 country table" and "`collect_pool` built per good throughout".
   Neither the collector selection (top three by power), nor the transferrer set, nor the randomised
   eligibility, nor the reference good appears anywhere in the spec. By Sec 3.16's own standard and by
   X167's own charge against v1-v4, this is the same defect one version later.
2. **The size also depends on a parameter the claim does not mention** — the reference commodity at
   which the powershare is frozen (X170: up to 23x on the worst case, sign reversal on individual
   collectors).
**Should say:** name the construction (or point at `audit_f4.py`) and list *both* free parameters.

---

### X173 — no node in the model has local trade value near 250; the largest is 112.6
**Status:** CONFIRMED
**Method:** Summed per-node production income two ways — from `solver.ROWS` inside the audit script,
and from the independent recomputation in `_audit_c_wealth.py`.
**Evidence:** largest local trade value **112.60** at `english_channel`; next `hangzhou` 103.98,
`gulf_of_siam` 103.60, `malacca` 102.45, `mexico` 101.40, `genua` 101.00. Nothing is within a factor
of two of 250. (For orientation: collected pools in the Sec 3.10 construction run 65-80, and the
largest node *total wealth*, tax included, is 316.6 at `english_channel`.)

---

### X174 - v4.0's 0.41% was an artifact of freezing one term at the alphabetically first commodity
**Status:** CONFIRMED (reproduced exactly)
**Method:** Found v4.0's own toolchain at `../../v4-owner-agnostic/scripts/` and ran it. `factor.py`
is the script that produced the figure; `audit_factor2.py` is v4.0's later re-attack.
**Evidence:** Running `../../v4-owner-agnostic/scripts/factor.py` reproduces v4.0's sentence to the
digit, on `gulf_of_siam`:
```
(2b) PROPAGATION PER GOOD (power varies by good)
     collect_pool(n) = 97.5216 ducats
     CAS  per-good 54.854184  scalar 55.078504  |diff| 0.2243 ducats (0.41%)
     POR  per-good 37.371788  scalar 37.524616  |diff| 0.1528 ducats (0.41%)
     GRA  per-good  4.898449  scalar  4.918481  |diff| 0.0200 ducats (0.41%)
     total per-good income 97.1244 vs scalar 97.5216 | total error 0.3972 ducats
```
i.e. "overstates **every** collector's income by 0.41%, a total of 0.40 ducats on a node collecting
97.1" - exactly v4.0's text, and uniform across collectors, hence v4.0's "systematic bias in one
direction".
**And the diagnosis is exactly right.** In `factor.py:incomes_scalar` the collect/transfer share is
built from `Pc = sum(collect_power(c, prop[c][GL[0]]) ...)` while `Pt` is per good - so the
*numerator of the retention share* is frozen at `GL[0]`, the alphabetically first live commodity
(`chinaware`), and the frozen term flows into `pool` (97.5216 against the true 97.1244). Since the
same frozen powershare then multiplies the pool for every collector, the relative error is identical
for all three: 97.5216/97.1244 - 1 = 0.409%. That is precisely "an artifact of freezing one term at
the alphabetically first commodity".
**Carry-over worth naming:** v5.0's `audit_f4.py` fixed half of this - `Pc` inside the share is now
per good, so the pool is right - but it still evaluates the scalar powershare at `GL[0]` =
`chinaware`. That surviving freeze is what makes v5.0's own per-collector percentages
construction-dependent (X170: MOR swings -9.84% to +7.93% across reference goods).

---

#### Cross-cutting findings (auditor note, carried from the per-claim pass)

1. **A live document/toolchain contradiction on the caravan figure.** `audit_delta.py` — named in the
   README as the producer of "the caravan cap on both bases" — prints 9.4%-47.0%, median 21.9% (flag)
   / 21.3% (derived). Sec 1.10 prints 8.6%-32.0%, median 17.9% / 17.5%. Both are correct arithmetic on
   different denominators (`50/total` vs `50/(total+50)`); the document keeps the v4.0-inherited
   numbers while the v5 script computes the other ones, and Sec 1.10's sentence quotes the totals that
   make its own percentages impossible. `validate_v5.py` misses it because it asserts on the *string*
   "median 17.9% over the **flag's** 26 inland nodes", not on the value.
2. **The Sec 3.10 per-good-propagation figures repeat the failing X167 names.** Their construction —
   three collectors chosen as the top three by power, transferrers as the next three, per-good
   eligibility drawn at `default_rng(11)`/p=0.6, powershare frozen at the alphabetically first live
   commodity `chinaware` — is stated nowhere in the spec, and every quoted percentage moves (sign
   included) when the last two are varied. X167 criticises v1-v4 for exactly this.
3. **Enumerations used as completeness arguments (X103, X165) are all short.** Both survive an
   independent sweep, but in both cases the sweep, not the list, is what supports the claim, and the
   lists omit the central item (`trade_range_modifier`; provincial trade power).
4. **Two arithmetic glosses are wrong in the same direction:** "at most one unit in the last place"
   for 3.7e-16 (it is 1.7-3.3 ULP), and "thirteen orders of magnitude" for a set spanning 11.3 to 14.3
   orders.
5. **The node-count question raised in the brief is a non-issue:** the save has 80 nodes; the
   differing denominators (79 for `highest_power`/`total`, 80 for `retention`, 77 for
   `collector_power`) are just the populations that carry each field.
6. **v4.0's toolchain still exists and still runs** (`../v4-owner-agnostic/scripts/factor.py`,
   `audit_factor.py`, `audit_factor2.py`). It reproduces the 0.41% figure to the digit, which turns
   X174 from an assertion into a reproduction — and shows that v5.0 fixed only half the defect it
   names: `audit_f4.py` builds `collect_pool` per good (v4's bug) but still evaluates the scalar
   powershare at `GL[0]` = `chinaware`. Note also that v4.0 measured country power from the save's
   `province_power=` field and v5.0 from `val=`; the two constructions are not comparable, and neither
   version says which it used.

### X175 — the wealth model has one open question, not three; two of v3.0's three are settled and moved into §1.3
**Status:** CONFIRMED
**Method.** Read v3.0's §3.13 "Open in the v3.0 wealth model" block and v5.0's, and traced each item.
**Evidence.** v3.0 listed exactly three (l.1049–1063): (a) do local flat goods bonuses exist at 1444
and apply before the price multiply; (b) is `local_production_efficiency` from a trade good inside or
outside wealth; (c) does `TAX_COEFF` stay 1.0 across the development range. v5.0's §3.13 carries
exactly **one** bullet, and its "Settled and moved" parenthetical names (b) and (c). (a) is also
settled — §1.3's whole-install sweep gives fifteen provinces with a flat `trade_goods_size` — and
v5.0's surviving question ("what *else* multiplies `goods_produced`") is the broadened successor to
it, which is the reading under which the accounting closes at three. The framing ("a question rather
than a number; §1.3 carries no value for it") matches v3.0's own framing of the same block.

---

### X176 — `trade_goods_size` / `trade_goods_size_modifier` appear in buildings, estate privileges, government reforms, church aspects, fervor, ages and event modifiers
**Status:** REFUTED
**Method.** Grepped each of the seven named directories for the two named keys with a left word
boundary (`(^|[^a-z_])trade_goods_size(_modifier)?\s*=`), so `global_trade_goods_size_modifier` and
`trade_goods_size_modifier_in_livestock_provinces` do not count; then swept all of `common/` and the
rest of the install for the same pattern, and enumerated every distinct key spelling in the install.
**Evidence — 5 of the 7 named categories carry neither key.**

| named category | hits for the two named keys |
|---|---|
| `common/buildings` | **2** (`00_buildings.txt:2216` `trade_goods_size = 1.0`; `01_nativebuildings.txt:252` `trade_goods_size_modifier = 0.5`) |
| `common/estate_privileges` | **0** |
| `common/government_reforms` | **0** |
| `common/church_aspects` | **0** |
| `common/fervor` | **0** |
| `common/ages` | **0** |
| `common/event_modifiers` | **272** |

The five zero rows carry only `global_trade_goods_size_modifier` (and one `global_trade_goods_size`
in `03_burgher_privileges.txt`), which §1.3 already classifies as country-scoped and **out** — so
the open question, as worded, points at five sources that are already settled and need no locality
test. Conversely the list **omits** every other carrier: the full set of `common/` subtrees holding
the province-scoped keys is `buildings` (2), `event_modifiers` (272), `great_projects` (38),
`holy_orders` (2), `province_triggered_modifiers` (6), `state_edicts` (2), `static_modifiers` (13),
`tradecompany_investments` (2), and nothing outside `common/`. §1.3 handles great projects, static
modifiers, province-triggered modifiers and buildings; `holy_orders`, `state_edicts` and
`tradecompany_investments` are named nowhere in the spec.
**Should say:** "`trade_goods_size` and `trade_goods_size_modifier` appear in **buildings, event
modifiers, great projects, static modifiers, province-triggered modifiers, holy orders, state edicts
and trade-company investments**; estate privileges, government reforms, church aspects, fervor and
ages carry only the country-scoped `global_trade_goods_size_modifier`, which §1.3 already excludes."

---

### X177 — `local_production_efficiency` from a trade good is outside wealth (Barcelona's production tooltip)
**Status:** PARTIAL
**Method.** Verified every file-checkable component; the tooltip itself cannot be re-read without
running the game.
**Evidence.** `history/provinces/213 - Barcelona.txt` has `trade_goods = glass` ✓.
`common/tradegoods/00_tradegoods.txt` l.1947ff gives glass `province = { local_production_efficiency
= 0.1 }` — province-scoped, +10% ✓. `common/technologies/adm.txt` grants `production_efficiency =
0.02` at the pre-1444 adm techs, so "From Technology: +2.0%" is the right value for a western
country at the 1444 start ✓. The itemisation sums: 2.0 + 10.0 = 12.0 ✓, and the conclusion (that the
engine books glass's +10% under *Production Efficiency*, i.e. on production income, which wealth
does not compute) follows from the itemisation if the itemisation is as quoted.
**Should say:** nothing needs changing in substance; the claim rests on a **single unreproducible
tooltip observation**, as `claims-v5.md` already marks with `§`. It should not be promoted above that
without a second reading, since the whole glass/gems/incense classification in §1.3 turns on it.

---

### X178 — `TAX_COEFF` is 1.0 across the development range, with `GP_COEFF` linear at four levels
**Status:** PARTIAL
**Method.** Arithmetic on the quoted readings; province data verified from the install (see X118).
**Evidence.** 6.00/6 = 1.0 and 2.00/2 = 1.0 ✓; 0.40/2 = 0.60/3 = 0.80/4 = 1.00/5 = 0.2 ✓, with no
intercept, so linearity is established over four points rather than assumed.
**Should say:** the arithmetic and the province data are sound, but "across the development range"
is established at **two** `base_tax` points (2 and 6) at the low end of a 1–50+ range, both on cored
city provinces at the 1.00 reference multiplier. The claim is fine as stated for the model's inputs;
it is not a measurement across the range, and, like X177, it is unreproducible from files.

---

### X179 — the sublinear regime is reachable for 13 of 30, unreachable for 11, on the boundary for 2
**Status:** PARTIAL
**Method.** Compared §3.13's restatement against §3.5's own four-bucket partition and against my
independent census.
**Evidence.** 13 + 11 + 2 = **26**, not 30. The four goods §3.5 puts in its "negative event that does
not reach 2.0" bucket — `cloth` (2.55), `coal` (7.0), `dyes` (3.0), `iron` (2.55) — are *also*
unreachable, and remain so even if every negative for a good is stacked. The true reading is
**13 reachable, 15 unreachable, 2 on the boundary**. This is not a v5.0 regression: the same
unclosed partition appears in `v3-owner-agnostic` l.1070 (12/11/3 = 26) and `v4-owner-agnostic`
l.1161 (13/11/2 = 26). §3.5 itself is correct; only §3.13's one-line restatement is wrong.
**Should say:** "reachable through vanilla price events for 13 of 30 goods, unreachable for 15
(eleven of which have no negative price event at all), and exactly on the boundary for 2."

---

### X180 — the calibration gives span exactly 1..5 with spearman(price, sinks) = −0.20
**Status:** CONFIRMED
**Method.** Reimplemented the calibration from the parameters the spec names (α unclamped at
exponent 2, ρ = 0.5, twig tolerance 3e-4, `defasc_beta` sweep) in `_audit_d_calib.py`, independent
of `final.py`'s reporting.
**Evidence.** Sink counts per good run **1..5** with no good outside that span (1: cloves, cocoa,
coffee, dyes, spices, sugar, tobacco; 5: glass, iron, naval_supplies, silk). spearman(price, sinks)
= **−0.1985** → −0.20 ✓. `final.py` independently prints −0.199.

---

### X181 — under α = 16 Deccan is demand rank 2, hangzhou rank 1 acting as transit, Beijing rank 3, and Deccan becomes the cloves sink
**Status:** CONFIRMED
**Method.** Built the α = 16 demand vector directly from the wealth field and ranked it; ran the
calibration for cloves and read in/out degrees at the named nodes.
**Evidence.** cloves α = (8/2)² = **16.0000** exactly. Demand ranks: 1 `hangzhou` (c = 0.934873),
2 `deccan` (0.063198), 3 `beijing` (0.000739), 4 `canton`, 5 `doab`. Cloves sink under the
calibration: **`['deccan']`** ✓. `hangzhou` in that graph has indeg 1 and outdeg 4 — a transit node,
not a sink ✓. `beijing` indeg 1 outdeg 3 ✓.

---

### X182 — `hangzhou` holds the richest single province, 30.4 against Beijing's 19.5
**Status:** CONFIRMED
**Method.** Computed the per-node maximum province wealth from the corrected wealth field.
**Evidence.** `hangzhou` 30.40 (pid **1821** — one of the four Grand Canal provinces, which is why
this figure moved with §1.3's whole-install sweep), `deccan` 25.75 (pid 542), `beijing` **19.50**
(pid 1816). 30.40 is the global maximum over all provinces. Both figures match to two decimals.

---

### X183 — the twig tolerance re-routes arcs individually carrying <0.03%, up to ~0.18% of a good's mass, dropping cloves to 99.97% reach
**Status:** CONFIRMED
**Method.** Recorded, per good, every free edge whose |net flow| exceeds the baseline tolerance
(1e-11) but falls below the calibration tolerance 3e-4, plus the resulting demand reach.
**Evidence.** Largest single re-routed arc over all 29 goods: **2.98e-4** = 0.0298%, i.e. strictly
below the 3e-4 = 0.03% tolerance ✓ (by construction, and confirmed empirically). Largest *total*
re-routed mass for one good: **0.001750** = **0.175%** ≈ 0.18%, attained on `cloves` ✓. Cloves reach
under the calibration: **99.969%** → 99.97% ✓, and it is the only good below 100%.
*Wording note:* `S` is normalised per good, so both percentages are of *that good's* supply. The
spec calls the first "world supply" and the second "a good's mass" for the same normalisation; the
second is the accurate name for both.

---

### X184 — The survival table is about 1.5 MB at double precision — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes — and the solver's residuals sit at 1e-16, one ULP of a double
**Status:** CONFIRMED
**Method:** Checked the arithmetic, the multiplier against §1.5 and §2.2, and the residual against
§3.10's measured figure.
**Evidence:** 29 × 80 × 80 × 8 = **1,484,800** exactly = 1.4848 MB decimal (1.416 MiB), so "about
1.5 MB" is fair, and half of it (single precision) is the 0.75 MB the claim attributes to v1/v2. The
multiplier 29 is the **live** goods count at 1444 (`GOODS` holds 30 including latent `coal`; `LIVE`
counts 29), and §1.5 explicitly gives a latent good "no survival-table entry", so 29 is the internally
consistent number here — §2.2 item 7's "30 goods × 80 BFS" is the row that disagrees with §1.5, not
this one. At 30 goods the figure would be 1,536,000 bytes, still "about 1.5 MB", so nothing downstream
turns on it.
*Slack, not error:* §3.10's measured worst relative disagreement is **0 to 3.7e-16**, not 1e-16;
3.7e-16 is ~1.7 ULP for values in [1,2) and more for smaller ones, so "1e-16, one ULP" rounds the
measurement down by roughly a factor of three. The order of magnitude and the conclusion (double, not
single, precision) are unaffected.

---

#### Systemic findings (auditor note, carried from the per-claim pass)

1. **The fallback branch's reachability analysis (X008–X011) is written against the post-peel balance
   while §1.1 defines `b` as the input balance, and its case list misses the family the peel
   produces.** One worked example — a triangle with a pendant, `b = (+1, 0, 0 | −1)` — fires the
   fallback on a connected core with a producer and a consumer. 75 of 114 firings in a random search
   are of that kind.
2. **"The fallback branch is where the index decides" is wrong three times over** (X010, X011, X125,
   X151, and §2.4 item 1): the spec's own T3 uses distinct wealths 3/2/1; 1444's `NODEW` is 80-of-80
   distinct so the wealth key can never tie there; and the index is load-bearing wherever the
   `(DEF, b)` key ties, with no fallback involved (2,774 of 7,146 random instances). The canonical
   node-order requirement is real; the reason given for it is not the reason that holds.
3. **"Phase 0 no-op ∧ no fallback ⇒ sink-set equality" is asserted in two places (X013, X145) and
   refuted by the spec's own T2**, which satisfies both conditions and breaks the equality. §2.2a's
   table gets this right ("measured exact 29/29" rather than "holds"); §1.1's bullet and §3.2's item 1
   do not.
4. **Everything that was measured, reproduced.** All 20 numerical figures in scope came back exact:
   29/29 equality and containment, 1–7 sinks, mean 3.5862, 0 fallbacks, 0 `(DEF, b)` ties, 14.5%/6.9%,
   22 and 17 flips, 245.0/143.8, ranks 1/31, 1.346%, ×1.720, the four China thresholds and the four
   outside them, 18/80 and 1/80 producers, 36 vs 482.2, 1,484,800 bytes — and the two ⚑ ENGINE rows
   (X134, X135) reproduced independently from the two save files rather than from the v2 write-up.
   The "zero exact ties" measurement is also not float-brittle: the smallest separation is 1.3e-05
   against a 3.4e-17 noise floor.
5. **Two defects in §2.8/§3.2 prose that sit outside this ID range but inside these sections:** the
   §2.8 spices row calls Genoa "demand rank 1" when it is rank 2 (`hangzhou` is rank 1, is the Phase-1
   selection, and is not a sink); and §3.2's "deleting demand variation entirely left the sink
   unmoved" did not reproduce in my reconstruction of the v1 operator.

### X185 — with the ε floor removed the contrasts run 4–97 on supply against 211–20,400 on demand across the 29 goods
**Status:** REFUTED
**Method.** Computed max/min over strictly positive entries of `S[g]` and `C[g]` at eps = 0 for
every one of the 29 live goods (`_audit_d_conn.py`), and cross-checked against the author's own
`final.py` PART E.
**Evidence.** The demand half is right: **211.1** (`fur`, `livestock`, `naval_supplies`, `slaves`,
`tea`, `tropical_wood`) to **20411.5** (`cloves`) → "211–20,400" ✓. The supply half is not.
`cloves` is produced in exactly **one** node, so its supply contrast is **1.000**, not 4. The range
across the 29 goods is therefore **1–97**, not 4–97. `4.00` is `glass`, the second-lowest and the
lowest among the 28 goods with more than one producing node. The author's own `final.py` prints the
counterexample directly: `cloves supply max/min+ = 1`.
**Should say:** "the contrasts run **1–97** on supply (1 at `cloves`, which has a single producing
node; 4–97 over the 28 goods with more than one) against 211–20,400 on demand." The argument is
strengthened, not weakened, by the correction — a supply contrast of 1 on the good with the widest
demand contrast is the sparsity point in its purest form.

---

### X186 — v3.0 through v4.0 repeated the 10⁷ / 10²–10³ ratio in §3.15 while §3.2 was withdrawing it
**Status:** PARTIAL
**Method.** Read §3.2 and §3.15 in both the v3.0 and v4.0 specs.
**Evidence.** The §3.15 half is true for both: `v3-owner-agnostic` l.1109 and `v4-owner-agnostic`
l.1200 both read "supply contrast (10⁷) drowns demand contrast (10²–10³)". The §3.2 half is true
only of **v4.0**, whose §3.2 (l.837–841) explicitly withdraws the ratio ("That ratio was `max(s)`
over the **ε floor** … which points the other way"). **v3.0's §3.2 asserts the ratio too**, at
l.754: "because supply contrast exceeds demand contrast by four to five orders of magnitude, the
right-hand side is set by supply geography." So in v3.0 there was no contradiction between the two
sections — both carried the wrong figure; the contradiction the claim describes existed only in v4.0.
**Should say:** "v3.0 and v4.0 both repeated the ratio in §3.15; v4.0's §3.2 withdrew it while its
own §3.15 kept it."

---

### X187 — ranked orientation: ρ_val +0.281 vs DRAIN +0.054, 43.8% vs 14.5% top-decile, 83.0% demand reachable, 31 orphan sinks
**Status:** CONFIRMED
**Method.** Recomputed all four figures for RANK, DRAIN, LAP and FLOW from `rankop.run()` and
`drain.run_drain()` with my own sink/reach/orphan/correlation code (`_audit_d_rank.py`).
**Evidence.** ρ_val (spearman of demand `c` against the sink indicator, pooled over 29 goods × 80
nodes): RANK **+0.281**, DRAIN **+0.054**, LAP +0.081, FLOW −0.137 ✓. Demand reach: RANK **83.0%**,
DRAIN/LAP/FLOW 100.0% ✓. Orphan sinks (sinks unreachable from any producing node): RANK **31**,
DRAIN 0, LAP 0, FLOW 3 ✓; the 31 are enumerated in my run and include all eight cloves sinks that
cloves cannot reach, so the "Genoa a cloves sink that cloves cannot reach" example verifies too.
*Definition note:* "top-decile" is the top **10** of 80 nodes (12.5%), which is what yields 43.8%
and 14.5% exactly. A literal decile (8 nodes) gives 45.7% and 16.8% — the same conclusion, wider gap.

---

### X188 — 8 net-producer sinks where DRAIN, LAP and FLOW post zero; 10–16 sinks/good against DRAIN's 1–7
**Status:** CONFIRMED
**Method.** Enumerated, for each operator and good, every sink `i` with `S[g][i] > C[g][i]`.
**Evidence.** RANK: **8** of 383 sinks net-produce their good — `cloth`/deccan, `fur`/james_bay,
`iron`/white_sea, `naval_supplies`/nippon, `naval_supplies`/white_sea, `silk`/basra,
`tropical_wood`/australia, `wool`/safi. DRAIN **0** of 104, LAP **0** of 101, FLOW **0** of 943 ✓.
Sinks per good: RANK min 10 max 16 ✓; DRAIN min 1 max 7 ✓ (independently confirmed by
`drainrep.py` and `v5measure.py`).
*Toolchain note (not a spec defect):* `drainrep.py` l.276 prints "RANK 9/387" as a **hardcoded
literal** rather than a computed value. The spec's 8 is the correct number; the script's 9 is stale
and will mislead anyone re-running it.

---

### X189 — seeded basin growth reaches 88.4% at its best tuning
**Status:** CONFIRMED
**Method.** Re-ran `leftovers.py`'s BASIN construction and swept γ over {1, 3, 10, 100, 1000, 1e4, 1e6}
to test "at its best tuning" rather than accepting γ = 1000 as given.
**Evidence.** Mean demand reach: γ=1 80.32%, γ=3 80.52%, γ=10 80.98%, γ=100 86.29%,
**γ=1000 88.36%**, γ=1e4 88.29%, γ=1e6 88.29%. 88.36% → **88.4%** ✓, and γ = 1000 is the maximum
over the sweep, so "at its best tuning" is justified. 0 of 29 goods reach 100%.

---

### X190 — the gravity kernel: exact counts for γ ≤ 0.7 up to six; four/five/six-mass fields collapse to three ends at γ = 0.9; best 61% = 97/159 at γ = 0.90–0.95; γ = 0.97 gives 93; every larger γ worse
**Status:** PARTIAL
**Method.** Rebuilt the kernel from `c_w(1.5)`, the BFS hop matrix and the top-k pairwise-unconnected
seeds, then swept γ at **0.005 resolution from 0.01 to 0.995** plus 0.996–0.9999
(`_audit_d_gamma.py`) — the author's `phiw3.py` samples only eight γ values, all ≥ 0.90.
**Evidence — three of the four halves hold.**
- γ ≤ 0.7: the end count equals the mass count exactly for every k in 1..6 at **every** γ on a
  0.01 grid from 0.01 to 0.70 ✓ (it also holds for k = 7; it first fails at k = 8, γ = 0.70).
- γ = 0.9: 4-mass → 3 ends, 5-mass → 3, 6-mass → 3 ✓.
- 97/159 = 61.0% is the **global maximum** over the whole fine sweep ✓; γ = 0.97 → **93** ✓;
  every γ > 0.97 is worse — the best is 90 at γ = 0.975, then 80 (0.98), 71 (0.99), 66 (0.995),
  63 (0.999) ✓. The negative half survives a fine sweep.
**Should say — the γ window is wrong.** 97/159 is not attained "at γ = 0.90–0.95"; it is a **plateau
over the entire range γ ∈ [0.01, 0.95]** — all 189 sampled γ values from 0.01 to 0.95 give exactly
97. Agreement then steps down to 93 at 0.955 and stays there through 0.97. Presenting 0.90–0.95 as
where the best lies implies a peak that does not exist and makes the kernel look tuned when it is
flat. It should read "61% (97 of 159) for every γ ≤ 0.95, stepping to 93 at γ = 0.955–0.97 and worse
above."

---

### X191 — v2.1 through v4.0 put the best agreement at γ = 0.97 and said the five- and six-mass fields give four ends at γ = 0.9; neither holds on the corrected field
**Status:** REFUTED
**Method.** Read the "Pinned-count wealth fields" paragraph in the v2.1, v3.0 and v4.0 specs.
**Evidence.** Only **v4.0** says either thing (l.1255–1259): "at γ = 0.9 the five- and six-mass
fields both give four ends — with **66%** vanilla-arrow agreement at its best (γ = 0.97, 105 of 159
arrows)". **v2.1** (l.856–858) says only "hits any chosen end count exactly and 69% vanilla-arrow
agreement" — no γ anywhere, no mass-field statement. **v3.0** (l.1166–1170) says "hits any chosen
end count exactly, with **66%** vanilla-arrow agreement in the reproduced construction" — again no γ
and no mass-field statement. The v5 spec's own adjacent parenthetical concedes this by saying v2.0
and v2.1 quoted 69%, which is not a γ = 0.97 figure. The second half of the claim (neither holds on
the corrected field) is verified: best is 97/159 = 61% at γ ≤ 0.95 and the 5-/6-mass fields give
**three** ends at γ = 0.9.
**Should say:** "**v4.0** put the best agreement at γ = 0.97 and said the five- and six-mass fields
give four ends at γ = 0.9; on the corrected wealth field neither holds. (v2.1 and v3.0 quoted a bare
agreement figure — 69% and 66% — with no γ.)"

### X192 — Under ±1% noise across 8 seeds the narrow window's edges move ≤0.02, widths range 0.00–0.03
**Status:** CONFIRMED
**Method:** Ran `audit_bands2.py` part (b) as shipped (8 seeds, `default_rng(4000+seed)`,
201-point α grid per seed).
**Evidence:** `english_channel+hangzhou`, baseline [1.41, 1.42] — "edges move at most **0.02** (lo)
/ 0.01 (hi) | widths **[0.0, 0.01, 0.02, 0.03]**". Width 0.0 means the window collapsed to a
single sampled α on at least one seed, as claimed.

---

### X193 — Over the same 8 seeds the three wide bands keep widths 0.28–0.51 with edges moving ≤0.03
**Status:** CONFIRMED
**Method:** As X192.
**Evidence:**
| band | widths across 8 seeds | max edge movement |
|---|---|---|
| `hangzhou` | 0.48, 0.49, 0.50, 0.51 | 0.01 lo / 0.01 hi |
| `genua+hangzhou` | 0.28, 0.29, 0.32, 0.33 | 0.01 lo / 0.03 hi |
| `doab+genua+hangzhou` | 0.43 … 0.48 | 0.03 lo / 0.01 hi |

Union of widths = 0.28 … 0.51 ✔; max edge movement 0.03 ✔.

---

### X194 — A constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges
**Status:** CONFIRMED
**Method:** Applied the principle symmetrically to every band the spec lists, using X192/X193's
measured edge uncertainties — this was the specific consistency attack the brief asked for.
**Evidence:** the principle is applied consistently, and it is not close:

| window | width | its own edge uncertainty (±1%, 8 seeds) | verdict under the principle |
|---|---|---|---|
| `english_channel+hangzhou` | 0.018 | up to 0.02 | rejected — width ≈ uncertainty ✔ |
| `hangzhou` | 0.506 | ≤ **0.01** | accepted — 50× the uncertainty ✔ |

The hypothetical that would have broken the argument — "the one-sink band's edges also move by
~0.03 and 1.5 sits 0.07 from an edge" — does not obtain: the one-sink band's own edges move by at
most **0.01**, and α_Φ = 1.5 sits 0.07 above the nearest edge (1.43) and 0.43 below the far one.
That is a 7× margin against the measured edge noise, not a 2× one. The principle also does real
work: it is what disqualifies v4.0's calibration target, and applying it to the retained value
does not disqualify 1.5.
*(Separate issue: the *other* half of §2.3's rationale — "the widest band" — is false; see X083.
X194's principle is sound and consistently applied; X083's superlative is not.)*

---

### X195 — At 8 seeds the narrow window disappears on none of them — it shrinks
**Status:** CONFIRMED
**Method:** Ran `audit_bands2.py` part (b); the script prints a "DISAPPEARS on N of 8 seeds" line
whenever a target sink set is absent from a seed's whole α grid.
**Evidence:** no `DISAPPEARS` line is emitted for any of the four bands, so the window is present
on all 8 seeds; its width falls as low as 0.00 (a single sampled α). The correction the spec makes
to its own earlier draft is right, and the weaker claim is indeed sufficient for the conclusion —
a window whose width can shrink to one grid point is disqualified by X194 whether or not it also
vanishes.

---

#### Systemic findings (auditor note, carried from the per-claim pass)

**S1 — Sampled points quoted as thresholds and as band edges.** Four separate claims report the
smallest value a *coarse sample* happened to catch as if it were a measured boundary:
X099's "18-node set needs ×2.5" (true value ×2.15, `w9.py` sampled only 1.5/2/2.5/3/4);
X100's Cape window "[×3, ×3.75]" (true region [2.82, 3.18] ∪ [3.24, 3.93] — and ×3.75 is produced
by **no script at all**, appearing only in the edit that wrote the sentence);
X088/X086's "2%" threshold (true value ×1.010);
X101's "transient split into three at ×10" (a ×5–×13 excursion reaching four sinks).
Where an edge is refined — the α_Φ band table, X082, X192/X193 — the work is careful and holds.
The defect is confined to figures that never got a refinement pass.

**S2 — A range-relative superlative stated as absolute, and a design rationale resting on it.**
The α_Φ scan stops at 3.00 for no stated reason. "The widest band on this field" (X078) is only
the widest below 3.00; on [1.00, 8.00] there is a 2.54-wide band at [4.19, 6.73] and a second
one-sink `hangzhou` band at [6.74, 8.00]. Because §2.3 and §1.6 both hang the retention of
α_Φ = 1.5 on that superlative (X083), a presentational shortcut has become the load-bearing
justification for the model's one free constant.

**S3 — Regeneration that updated numbers without re-checking the argument built on them.**
X160's "nor a band containing its own baseline of 13" was true in v4.0 (range 13–22, baseline 18,
against v2's 9–17) and became false when the figures were regenerated to 11–17 / 13, since
9 ≤ 13 ≤ 17. `changes-v5.md` entries 37–38 show the substitution. The same class of risk is what
`claims-v5-round1.md` was built to catch; this instance survived it.

**S4 — `europe.py` scales wealth while the prose claims a development edge.** The docstring
asserts the equivalence ("multiplier on development -> both wealth terms scale with it") and §1.3's
own wealth expression falsifies it, because the flat `trade_goods_size` addend does not scale.
This is not academic: the sink sets quoted at ×1.02 (X086) and ×1.56 (X087) both change under the
correct scaling. X091 states the false equivalence explicitly.

**S5 — A negative claim contradicted by its own section.** X097's "Nothing routes through the Cape
in `Φ_w`" is refuted by 115 ordered node pairs whose drainage path crosses the Cape, and is
contradicted eleven lines later by §1.6's own phrase "1444's Atlantic→Cape→Indian-Ocean drainage".
Absolute negatives in this spec are the highest-yield place to look: this is the only one in my
set and it failed.

**S6 — X065 vs X085/X101/X086/X127.** §1.6 asserts in its third paragraph that the sink count is
set by `α_Φ` with only locations emergent, then spends the next two pages measuring the count
changing at fixed `α_Φ`. §2.4's X127 states the correct version. The wrong sentence is the one
promoted to bold.

**On the checks that held.** Nothing in the α_Φ band-noise work (X192–X195), the agreement figures
(X075/X076/X163), the wealth-rank readings (X070/X159), the coal measurement (X064), the routes
(X094–X096, X098), the guarantees (X161), or the vanilla end-count (X126) broke under attack, and
several are stronger than stated — X074 survives 40 seeds at ±1% and 20 at ±2% with zero flips,
and X092 survives a 32-point dense scan the original 7-point sample could not have supported.

### X196 — what `highest_power` holds was not determined; the model does not read it
**Status:** CONFIRMED as written — but the field is now determined (see below)
**Method:** `grep highest_power scripts/*.py` (model files vs audit files); then a hypothesis sweep
over every country sub-field and node scalar, including the two node lists the spec's candidate list
omits (`top_provinces`/`top_provinces_values`, `top_power`/`top_power_values`).
**Evidence:** `solver.py` and `drain.py` never mention `highest_power`; only `audit_delta2.py`,
`validate_v5.py` and audit copies do ✓.
**Determination (supersedes "not determined"):** `highest_power` is the trade power of the single
strongest **province** in the node, not of any country. `highest_power ≤ max(top_provinces_values)`
on 79/79; where the top provincial-power country owns exactly **one** member province it equals that
country's provincial power on **17/17** (e.g. `african_great_lakes` 14.880 = BUG); where it owns
several it is strictly less on **62/62** (`venice` 53.2 < VEN's 99.637 provincial;
`gulf_of_siam` 16.8 < KHM's 49.445). The author's search failed because §1.10's candidate list
(`total`, `max`, `p_pow`, `collector_power`, country `val`) is entirely country-level.
**Should say:** replace "was not determined" with the province reading, or at least name the two
node lists (`top_provinces_values`, `top_power_values`) that were not tested.

---


---

## Appendix — what this audit ran

Primary sources, in order of how much weight they carry here:

1. **A fresh parse of the install.** An independent PDX-script parser (`scripts/_audit_x_pdx.py`)
   and province-state builder (`scripts/_audit_x_prov.py`) written for this audit, not derived from
   `scripts/pdx.py`. It reads all 3,923 `history/provinces/` files, applies the undated block and
   every dated block ≤ 1444.11.11 in order, and reproduces the model's counted set (2,452 provinces)
   and its world wealth (**10,677.5000**) to the last digit without touching `prov1444.json`.
2. **The save.** `VANILLA_start.eu4` — `meta` confirms `date=1444.11.11`, 22 DLC including Leviathan.
   Used for every "at the 1444 start" question the history files cannot answer: `devastation`,
   `unrest`, `is_city`, `center_of_trade`, per-node country power tables, `highest_power`.
3. **Whole-install key sweeps.** For each of the four keys `wealth` reads — `trade_goods_size`,
   `trade_goods_size_modifier`, `trade_value_modifier`, `local_tax_modifier` — every `*.txt` in the
   install was searched at a word boundary and every hit's enclosing block parsed and classified.
   Same for `tax_income` (the flat-tax key the model has no term for).
4. **Re-runs of the reference solver.** `solver.py`, `drain.py`, `wealthmodel.py` and the measurement
   scripts were re-run, and the key results re-derived from scratch where the script's own output
   would have been circular. Independent reproductions include: the one-sink / two-sink split
   (corrected field → `{hangzhou}`, Phase 1 selects `hangzhou`, 0 promotions, 0 fallbacks;
   uncorrected field → `{english_channel, hangzhou}`, Phase 1 selects `genua`, both by stall
   promotion); the 29-good sink statistics (min 1, max 7, mean 3.586, 0 fallbacks); the Cape's
   in-degree 1 / out-degree 3; and `drain.NODEW`'s 80 values (one zero, 79 distinct positives, no
   exact ties).
5. **Prior versions.** `../v3-owner-agnostic/` and `../v4-owner-agnostic/` spec text was read
   directly wherever a v5.0 claim is *about* what an earlier version said. Prior validations were
   not used as evidence.

No existing file in the mod tree was modified. Two new files remain in `scripts/` as the
reproduction path for the §1.3 findings — `_audit_x_pdx.py` (an independent PDX-script parser, not
derived from `scripts/pdx.py`) and `_audit_x_prov.py` (the 1444.11.11 province-state builder). All
other scratch produced during the audit has been removed.
