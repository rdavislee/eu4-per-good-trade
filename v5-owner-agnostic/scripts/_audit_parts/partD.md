# Audit part D — X001–X004, X118–X124, X152–X158, X175–X183, X185–X191

**Note on reproduction.** This audit's helper scripts were written to `scripts/` as `_audit_d_*.py`
and were deleted from that directory mid-session by a concurrent session (the `_audit_a_*` and
`_audit_e_*` files of other auditors went with them). Every method below is described in enough
detail to re-derive from `solver.py` / `drain.py` / `rankop.py` primitives without them.

---

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
- W124 → §1.1 Phase 3 fallback defined; `T3` labelled in §3.2.
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
   "stack overflow, twice", "reproduced twice", "×2". The third reproduction exists but comes from
   `validation-v3.md`, which the spec does not cite. And §2.7 of the v5 spec itself still says
   "1002 frames at one address, **twice**" — the document contradicts itself, so at least one of the
   two figures is unverified against anything the document points at.
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

### X152 — 13 of 30 goods can be pushed strictly below 2.0 by a single vanilla `change_price` event
**Status:** CONFIRMED
**Method.** Independent whole-install census (byte-level walk of every non-binary file, quote-aware
comment stripping, brace-matched block extraction — no `pdx.py`, no `w10.py`), then an independent
partition against an independently parsed `common/prices/00_prices.txt`. Semantics established from
shipped save data, not assumed.
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
extraction of every block; each block classified by whether an odd number of `"` precedes it.
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
strings*: `country_event_with_insight { effect_tooltip = " … " }` and
`country_event_with_effect_insight { effect = " … " }`. A quoted string is a single token to the
engine's parser; these are display text and are never executed. The seven, with line numbers:

| file | line | good | value | key |
|---|---|---|---|---|
| `missions/DOM_Britain_Missions.txt` | 919 | fur | +0.25 | `ENGLISH_FUR_TRADE` |
| `missions/KoK_Byzantine_Missions.txt` | 2070 | silk | +0.20 | `BYZ_growing_demand` |
| `missions/KoK_Persia_Missions.txt` | 3384 | silk | +0.25 | `PERSIAN_SILK` |
| `missions/KoK_Persia_Missions.txt` | 3390 | dyes | +0.50 | `PERSIAN_DYES` |
| `missions/KoK_Persia_Missions.txt` | 3396 | cloth | +0.35 | `PERSIAN_CLOTH` |
| `missions/KoK_Yemen_Missions.txt` | 954 | coffee | +0.25 | `YEM_coffee_price_boost` |
| `missions/WOC_Italian_Missions.txt` | 2841 | wine | +0.40 | `ITA_wine_upgrade` |

The seven executable mission blocks are `DOM_Chinese` L7015 (chinaware +0.50), `DOM_Japanese` L1466
(iron +0.25), `GC_Portuguese` L569 (slaves +0.50), `SCA_Polish` L2264 (grain +0.20) and
`WOC_Hisn_Kayfa` L1448/L1459/L1493 (grain +0.10 ×3).
Six of the seven display blocks are verbatim duplicates of a block already counted in `events/`
(`BYZ_growing_demand`, `PERSIAN_SILK`/`PERSIAN_DYES`/`PERSIAN_CLOTH`, `YEM_coffee_price_boost`,
`ITA_wine_upgrade`). The seventh, `ENGLISH_FUR_TRADE`, occurs nowhere in the install except that
tooltip string and four localisation files — the effect it previews is `flavor_gbr.7`
(`events/FlavorGBR.txt` l.466), which uses key `FUR_TRADE`. The count of **executable**
`change_price` blocks is therefore **154**, with **7 in `missions/`** — which is exactly what v4.0
said. §3.5 should say "161 textual occurrences, of which 154 are executable; 7 sit inside
`effect_tooltip` / insight strings and duplicate effects counted elsewhere." The partition
(X152/X153) is byte-identical under either census — all seven are positive.

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
2. **There is no per-file count assertion.** `w10.py` l.19–20 is
   `try: walk(pdx.load(os.path.join(dp,fn)),hits,r)` / `except Exception: pass`, and the file
   contains no `assert` and no count check of any kind. `validate_v5.py` l.238 accumulates a
   **per-tree** regex count (`raws[tree] += len(re.findall(...))`) and l.241 asserts the tree totals
   `(161, 93, 14, 1, 53)`; l.239–240 repeat the same `try: walk(pdx.load(fp), hits, tree)` /
   `except Exception: pass`, and `raws` is **never** compared against `hits`. The partition at
   l.242+ is computed from `hits`, which still holds 154 blocks. The guard as built cannot detect a
   per-file loss and does not detect this one. No other script in the toolchain contains a per-file
   guard (the only `assert`s are in `patch_lib.py`, `stats5.py` and `toys.py`, none about this).
3. **The conclusion is also wrong in substance** — the seven "recovered" blocks are tooltip strings
   (see X154), so 154 was the correct executable count and 161 is a regression.
   The one true half: the seven are all positive and the partition is unchanged.
**Should say:** "v4.0 said 154 and 7. Those seven blocks sit inside quoted `effect_tooltip`/insight
strings, which `pdx.py`'s string token swallows; they are display text duplicating effects declared
in `events/`, so 154 is the executable count and 161 the textual one. The scan now asserts a raw
per-tree count against the parser's recovery."

---

### X156 — `wool`'s largest single negative is `HAB - Austria.txt`'s `NEW_DRAPERIES` −0.25 → 1.875, against −0.20 for the same key in `events/PriceChanges.txt`
**Status:** CONFIRMED
**Method.** Extracted all eight shipped `wool` blocks; located the history date; read the event's
trigger.
**Evidence.** All eight wool blocks: `COTTON_IMPORTS` −0.10 and `NEW_DRAPERIES` −0.20,
`REGULATED_UNIFORMS` +0.10, `SELECTIVE_BREEDING` +0.35 in `events/PriceChanges.txt`;
`COTTON_IMPORTS` −0.10, `NEW_DRAPERIES` **−0.25**, `REGULATED_UNIFORMS` +0.10, `SELECTIVE_BREEDING`
+0.25 in `history/countries/HAB - Austria.txt`. The minimum is −0.25 and it is in the history file.
Under fractional semantics 2.5 × (1 − 0.25) = **1.875**, and the `events/` version gives
2.5 × 0.80 = 2.00 exactly. The history block is dated **1540.1.1**, and that same dated block sets
`new_draperies_happened`, which is precisely the global flag `prices.13`'s trigger tests
(`NOT = { has_global_flag = new_draperies_happened }`) — so past 1540 the −0.20 event can no longer
fire and, keys being keyed, 1.875 is what a campaign reaching 1540 holds.
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
per source over each good's directed edge set, unioning the reachability matrix.
**Evidence.** N = 80, N×(N−1) = **6320** = 80 × 79. The diagonal is never set (the accumulation
guards `t != s`), so self-pairs are excluded. Connected ordered pairs = **5825**, 92.1677% →
**92.2%**. For contrast, the unordered variant would be 3141/3160 = 99.4%, so the "ordered" reading
is load-bearing and is the one the spec uses.

---

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
boundary, so `global_trade_goods_size_modifier` and
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
**Evidence.** `history/provinces/213 - Barcelona.txt` has `trade_goods = glass`.
`common/tradegoods/00_tradegoods.txt` l.1947ff gives glass `province = { local_production_efficiency
= 0.1 }` — province-scoped, +10%. `common/technologies/adm.txt` grants `production_efficiency =
0.02` at the pre-1444 adm techs, so "From Technology: +2.0%" is the right value for a western
country at the 1444 start. The itemisation sums: 2.0 + 10.0 = 12.0, and the conclusion (that the
engine books glass's +10% under *Production Efficiency*, i.e. on production income, which wealth
does not compute) follows from the itemisation if the itemisation is as quoted.
**Should say:** nothing needs changing in substance; the claim rests on a **single unreproducible
tooltip observation**, as `claims-v5.md` already marks with `§`. It should not be promoted above that
without a second reading, since the whole glass/gems/incense classification in §1.3 turns on it.

---

### X178 — `TAX_COEFF` is 1.0 across the development range, with `GP_COEFF` linear at four levels
**Status:** PARTIAL
**Method.** Arithmetic on the quoted readings; province data verified from the install (see X118).
**Evidence.** 6.00/6 = 1.0 and 2.00/2 = 1.0; 0.40/2 = 0.60/3 = 0.80/4 = 1.00/5 = 0.2, with no
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
exponent 2, ρ = 0.5, twig tolerance 3e-4, `defasc_beta` sweep), independent of `final.py`'s
reporting.
**Evidence.** Sink counts per good run **1..5** with no good outside that span (1: cloves, cocoa,
coffee, dyes, spices, sugar, tobacco; 5: glass, iron, naval_supplies, silk). spearman(price, sinks)
= **−0.1985** → −0.20. `final.py` independently prints −0.199.

---

### X181 — under α = 16 Deccan is demand rank 2, hangzhou rank 1 acting as transit, Beijing rank 3, and Deccan becomes the cloves sink
**Status:** CONFIRMED
**Method.** Built the α = 16 demand vector directly from the wealth field and ranked it; ran the
calibration for cloves and read in/out degrees at the named nodes.
**Evidence.** cloves α = (8/2)² = **16.0000** exactly. Demand ranks: 1 `hangzhou` (c = 0.934873),
2 `deccan` (0.063198), 3 `beijing` (0.000739), 4 `canton`, 5 `doab`. Cloves sink under the
calibration: **`['deccan']`**. `hangzhou` in that graph has indeg 1 and outdeg 4 — a transit node,
not a sink. `beijing` indeg 1 outdeg 3.

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
below the 3e-4 = 0.03% tolerance (by construction, and confirmed empirically). Largest *total*
re-routed mass for one good: **0.001750** = **0.175%** ≈ 0.18%, attained on `cloves`. Cloves reach
under the calibration: **99.969%** → 99.97%, and it is the only good below 100%.
*Wording note:* `S` is normalised per good, so both percentages are of *that good's* supply. The
spec calls the first "world supply" and the second "a good's mass" for the same normalisation; the
second is the accurate name for both.

---

### X185 — with the ε floor removed the contrasts run 4–97 on supply against 211–20,400 on demand across the 29 goods
**Status:** REFUTED
**Method.** Computed max/min over strictly positive entries of `S[g]` and `C[g]` at eps = 0 for
every one of the 29 live goods, and cross-checked against the author's own `final.py` PART E.
**Evidence.** The demand half is right: **211.1** (`fur`, `livestock`, `naval_supplies`, `slaves`,
`tea`, `tropical_wood`) to **20411.5** (`cloves`) → "211–20,400". The supply half is not.
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
`drain.run_drain()` with my own sink/reach/orphan/correlation code.
**Evidence.** ρ_val (spearman of demand `c` against the sink indicator, pooled over 29 goods × 80
nodes): RANK **+0.281**, DRAIN **+0.054**, LAP +0.081, FLOW −0.137. Demand reach: RANK **83.0%**,
DRAIN/LAP/FLOW 100.0%. Orphan sinks (sinks unreachable from any producing node): RANK **31**,
DRAIN 0, LAP 0, FLOW 3; the 31 include all eight cloves sinks that cloves cannot reach, so the
"Genoa a cloves sink that cloves cannot reach" example verifies too.
*Definition note:* "top-decile" is the top **10** of 80 nodes (12.5%), which is what yields 43.8%
and 14.5% exactly. A literal decile (8 nodes) gives 45.7% and 16.8% — the same conclusion, wider gap.

---

### X188 — 8 net-producer sinks where DRAIN, LAP and FLOW post zero; 10–16 sinks/good against DRAIN's 1–7
**Status:** CONFIRMED
**Method.** Enumerated, for each operator and good, every sink `i` with `S[g][i] > C[g][i]`.
**Evidence.** RANK: **8** of 383 sinks net-produce their good — `cloth`/deccan, `fur`/james_bay,
`iron`/white_sea, `naval_supplies`/nippon, `naval_supplies`/white_sea, `silk`/basra,
`tropical_wood`/australia, `wool`/safi. DRAIN **0** of 104, LAP **0** of 101, FLOW **0** of 943.
Sinks per good: RANK min 10 max 16; DRAIN min 1 max 7 (independently confirmed by
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
**γ=1000 88.36%**, γ=1e4 88.29%, γ=1e6 88.29%. 88.36% → **88.4%**, and γ = 1000 is the maximum
over the sweep, so "at its best tuning" is justified. 0 of 29 goods reach 100%.

---

### X190 — the gravity kernel: exact counts for γ ≤ 0.7 up to six; four/five/six-mass fields collapse to three ends at γ = 0.9; best 61% = 97/159 at γ = 0.90–0.95; γ = 0.97 gives 93; every larger γ worse
**Status:** PARTIAL
**Method.** Rebuilt the kernel from `c_w(1.5)`, the BFS hop matrix and the top-k pairwise-unconnected
seeds, then swept γ at **0.005 resolution from 0.01 to 0.995** plus 0.996–0.9999 — the author's
`phiw3.py` samples only eight γ values, all ≥ 0.90.
**Evidence — three of the four halves hold.**
- γ ≤ 0.7: the end count equals the mass count exactly for every k in 1..6 at **every** γ on a
  0.01 grid from 0.01 to 0.70 (it also holds for k = 7; it first fails at k = 8, γ = 0.70).
- γ = 0.9: 4-mass → 3 ends, 5-mass → 3, 6-mass → 3.
- 97/159 = 61.0% is the **global maximum** over the whole fine sweep; γ = 0.97 → **93**;
  every γ > 0.97 is worse — the best is 90 at γ = 0.975, then 80 (0.98), 71 (0.99), 66 (0.995),
  63 (0.999). The negative half survives a fine sweep.
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
