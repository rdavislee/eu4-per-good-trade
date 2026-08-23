# Claim Validation — Per-Good Trade Network Spec v6.0

Every claim in `claims-v6.md`, **Y001–Y143**, re-derived against primary sources: the EU4 1.37.5.0
install at `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` (all DLC enabled,
Leviathan among them), the vanilla 1444.11.11 save `…\save games\VANILLA_start.eu4` (a ZIP whose
`gamestate` is text; its `meta` reads `savegame_version 1.37.5.0`, `date=1444.11.11`), the reference
solver in `scripts/`, the shipped tutorial save `tutorial/eu4_tutorial_chapter10.eu4`, and the text
of the spec and of the four prior specs and four prior validations.

**Nothing is inherited.** No verdict was taken from `validation-v5.md`, `validation-v4.md`,
`validation-v3.md` or `validation-v2.md`. Where a prior audit's *measurement* appears below it is
cited as a document fact — what that audit recorded — never as evidence that a claim is true.

**Rules used.**

- For a claim about a file, the file was opened. The spec's quotation of a file is never the file.
- MODEL claims are split. A derivation is attacked as an argument; a measurement is re-run. The two
  verdicts are kept separate in the write-up.
- A derivation that holds on the 1444 start but not in general is REFUTED, and the breaking case is
  named.
- A stipulation is checked for internal consistency and for whether the rationale it states actually
  supports it. A choice justified by a false fact is REFUTED even where the choice is defensible.
- Where only a running game could settle a claim, that is said, and the claim is graded on the
  evidence that exists.
- Never CONFIRMED on plausibility, and never on a wiki.
- The scripts in `scripts/` are themselves claims. A claim that a check exists is settled by looking
  for the check.

**What was re-run.** `measure6.py` was re-executed and reproduces the committed `measure6.out` byte
for byte (57 labelled figures). `provinces.py` was re-executed and reproduces `prov1444.json` byte
for byte. `verify6.py` was re-executed against the spec (22 checks, 0 failed). `toys.py` reproduces
T1, T2 and T3. `phiw3.py` and `europe.py` were re-executed. Beyond the shipped toolchain this audit
built its own instruments: a `gamestate` province parser (4,941 province blocks, 2,472 owned), a
`gamestate` trade parser (80 node blocks with their per-country power tables), an independent
`change_price` census with a quote-aware pass and a block-ancestor pass, a self-contained DRAIN
parameterised by node labelling and arc presentation order, and an independent income-identity
harness. Figures marked *independent* below come from those, not from `scripts/`.

---

## Summary

| Status | Count | Share of 143 |
|---|---:|---:|
| CONFIRMED | **112** | 78% |
| PARTIAL | **28** | 20% |
| REFUTED | **3** | 2% |
| UNVERIFIABLE | **0** | 0% |
| **Total** | **143** | |

### Refutations

| ID | § | What is wrong |
|---|---|---|
| **Y011** | §0 | `verify6.py` does not re-derive each measured figure from the document. It runs 22 checks on the spec, 8 of them text presence/absence; of the 14 numeric needles at least five are hardcoded literals rather than computed values, and one of those literals — the coal-activation flip count `13` — is false: the install gives **10**. The harness therefore passes a figure that is wrong. Two figures also name a script that does not compute them (Y003, Y049). |
| **Y040** | §1.3 | `flavor_geo.1` carries no `add_base_tax`, `add_base_production` or `add_devastation`. Brace-matched blocks in `events/FlavorGEO.txt`: `flavor_geo.1` spans lines 8–46 and holds none of the five keys; all five sit in **`flavor_geo.3`** ("Sack of Sarai"), lines 98–150, which no on-action fires. `on_startup` **does** fire `flavor_geo.1` — directly, from its own `events = { }` list in `00_on_actions.txt`, not through `on_startup_effect` — so that half of the claim stands. And no development moves before the first tick: the history-file parse matches the save's `base_tax` and `base_production` on **2,472 of 2,472** owned provinces. |
| **Y049** | §1.5 | Repricing the 45 owned latent-coal provinces flips **10 of 159** `Φ_w` edges and adds **214.60** ducats, not 13 and 217. **Root cause located:** 13/217.00 comes from dropping the `devastation` factor on the repriced provinces while the baseline retains it. Province **4237** is both latent-coal and devastated (20, `base_production` 3) and alone accounts for the whole gap: 0.2 · 3 · 10 · (1 − 0.6) = 2.40 ducats, and the three extra flips follow from it. |

### Partials

| ID | § | What is wrong |
|---|---|---|
| **Y003** | §0 | 0.98% is right; the province count is **88 of 2,472** under v6.0's own counting rule — 87 is the count under the withdrawn `is_city` filter — and `measure6.py` computes neither figure. |
| **Y004** | §0 | `validation-v4.md` examined the classification and graded every repair CONFIRMED, so "wrong in every audit that examined it" fails as a universal — a violation of the document's own R2. |
| **Y013** | §1.1 | The condition is stated right; "which uniform *wealth* gives" is false — counted provinces per node run 0 to 72, and uniform wealth leaves max `|b_w|` = 0.0166 with all 80 nodes non-zero. |
| **Y014** | §1.1 | The index tiebreak is real; the reason given for §2.8's containment set is not — §2.8 and §3.2 both ground it on **T3**, which is independent of any tie, and on 1444 the wealth key never ties. |
| **Y020** | §1.3 | Same false universal as Y004. |
| **Y027** | §1.3 | The retraction of `Base: X (Yearly 12·X)` is right; the replacement schema `trunc(base_tax / 12)` is itself false at `base_tax` 6 — 6/12 = 0.50, observed 0.49. Only §2.3's `trunc(base_tax × 0.083333)` yields it. |
| **Y028** | §1.3 | v4.0 and v5.0 wrote that schema. **v3.0 did not** — it quotes the reading without generalising it to `12·X`. |
| **Y029** | §1.3 | The upper bound is right; one observation constrains the divisor to **(11.73, 12.14]**, so the 12.00 floor is assumed, not measured. |
| **Y032** | §1.3 | v4.0 and v5.0 read it that way; **v3.0 carries no 0.6125 at all**. |
| **Y034** | §1.3 | The four blocks and their values are exact; "scaled by the devastation level" is settled by no shipped file and by nothing in the save, and `prosperity` is the same kind of 0–100 province-state scalar but is not marked scaled. |
| **Y046** | §1.3 | Coherent as a stipulation, but the field every v6.0 figure is measured on does *not* read the game's state for the twenty: the solver excludes `unknown` at price 0. Reading the engine's own assignments gives world wealth **10,607.40**, a gap of 12.70. |
| **Y047** | §1.3 | The two-reading basis is right; "the development range runs past 50" is not a property of this start — max `base_tax` 15, max `base_production` 15, max total development 33. |
| **Y054** | §1.6 | The three flip counts are exact; the sink set does **not** survive at ×10⁻⁶ — it collapses to `{genua}`. |
| **Y068** | §1.6 | "Asia holds no end past a broad range of European growth" holds from about ×1.55; "the Channel's basin grows" is contradicted by the table's own ×2.00 row, where `genua` alone is a sink and the Channel is not. |
| **Y074** | §1.6 | The Volga holds. "From the Channel the Hansa and the Danube" does not: `english_channel` has out-degree **0** on this field, so no route leaves it. The Hansa/Danube chain runs from `lubeck`. |
| **Y082** | §1.10 | The three define values are exact; `TRADING_POLICY_COOLDOWN_MONTHS` governs **every** trading policy in `00_trading_policies.txt`, `propagate_religion` included — not just "both banded policies". |
| **Y083** | §1.10 | Its flicker-risk set keeps Propagate Religion exposed, but Propagate Religion is a trading policy and carries the same 12-month cooldown the claim credits with damping. |
| **Y084** | §1.10 | Range and totals exact; the median is **21.6%**, not 21.9% (21.88% is the 14th of 26 order statistics, not the median). |
| **Y085** | §1.10 | Range and the arithmetic critique exact; the median is **17.7%**, not 17.9%. |
| **Y090** | §2.2 | Total range and the ~20 ms outlier hold; the per-good average ran **3.7–9.7 ms** over twelve runs, outside the quoted 3–7 ms. |
| **Y091** | §2.2 | v5.0's quotation is right; twelve fresh runs put **6** inside [0.17, 0.21] s, not one. |
| **Y117** | §3.5 | 10 non-executing and 151 executable are exact; the mechanism split is not — **4** sit in `effect_tooltip = "…"`, **3** in `effect = "…"` strings consumed by `country_event_with_effect_insight` (which substitutes `$effect$` inside `tooltip = { }`), and 3 in literal `tooltip = { }` blocks. |
| **Y121** | §3.5 | No per-file count assertion exists anywhere in v5's toolchain — confirmed. But `verify6.py` does not carry the guard either: it checks a hardcoded literal `161`, and `measure6.py`'s per-tree regex count is printed and never asserted against the walker's hits. |
| **Y123** | §3.9 | The four node wealths are exact; the ranks are **4th, 3rd and 7th**, not 3rd, 2nd and 7th — `mexico` at 300.4 is rank 2. |
| **Y130** | §3.10 | The per-good factoring does fail, but "a single node scalar cannot reproduce every collector's income exactly" is false: the **collected-value-weighted** mean share is one scalar per (node, country), it sums to 1 over collectors, and it reproduces every collector's income to ~1e-14% at every node and under every collector set tried. What per-good propagation destroys is that the share be derivable from *trade power alone* — not the exactness. |
| **Y132** | §3.10 | Not reproducible. Under one natural reading of "value-weighted mean share" the error is identically **0**; under another it reaches **0.54%** at `gulf_of_siam` and 0.17% at `genua`. The construction is unstated — the defect Y135 says must not recur. |
| **Y133** | §3.10 | Inherits Y132: "within a tenth of a percent" is the bound that does not reproduce. |
| **Y143** | §3.16 | The failure is real (residual 1.15e-05 at v1's ε = 1e-6 reading the spec literally; 9.58e-06 on v2's re-measurement) and 1e-5 is no longer carried. But "at the tolerance v1 used" misdescribes 1e-5: that was the **residual**, and v1's ε was 1e-6. |

---

## Systemic findings

**S1. The verifier is the weakest link, and it is the one thing v6.0 stakes its credibility on.**
§0 promises that every measured figure is re-derived from the document text and that a disagreement
fails the run. `verify6.py` checks 14 numbers in a document quoting roughly fifty; five of those
fourteen are literals typed into the harness rather than values computed from the install; and one
literal — `13` coal flips — is wrong. `mutate6.py` plants twelve errors and catches twelve, but it
plants them in strings the harness already looks at, so 12/12 measures the harness's
self-consistency, not its coverage. The inversion v6.0 correctly identifies as v5.0's defect has
been performed on about a quarter of the surface and declared complete.

**S2. Attributions to scripts are not checked.** Y003's 0.98%/87 and Y049's 13 flips/217 ducats both
carry `(measure6.py)`; `measure6.py` computes neither. §2.4 attributes the 580/580 relabelling sweep
to `validation-v5.md`, which contains no such sweep — it records a 7,146-instance random sweep, a
24-relabelling minimal example and a 120-relabelling pendant case, none of them 29 goods × 20
relabellings on the 1444 map. The measurement is real; this audit reproduced it independently. The
citation is not.

**S3. Two figures in §1.6 were regenerated and the sentences built on them were not.** The field's
second sink is now `english_channel`, which makes the Channel an *end node*. So the
Hansa-and-Danube route "from the Channel" (Y074) cannot exist, and `europe.py` — the script §1.6
cites for the Europe table — **crashes on its own route section** for exactly that reason
(`" -> ".join(path(src, s[0]))` with `path` returning `None` because `s[0]` is `english_channel`).
The same regeneration is why the ×2.00 row shows `genua` alone while the prose above it says the
Channel's basin grows (Y068). This is v6.0's own diagnosed defect class — "patch what you touch and
the untouched neighbour keeps the old claim" — recurring one revision later.

**S4. R2 is violated by the sentences that introduce R2's rationale.** Y004 and Y020 assert the
classifier was "wrong in **every** audit that examined it". `validation-v4.md` examined it and graded
all ten of v3.0's refutations and all nineteen of its partials CONFIRMED. The universal is false, and
it is load-bearing for the decision R1 records.

**S5. The province-counting rule changed and one derived count did not.** v6.0 counts a province when
it has an owner and lies in a trade node — 2,472. The deleted apparatus touches **88** of those. 87
is its size under the `is_city = yes` filter v6.0 withdrew, and 87 is what §0 and §1.3 both print,
against the 2,472 total.

**S6. Two of the three tooltip-derived "engine test" claims are arithmetically self-inconsistent.**
§1.3's tax schema `trunc(base_tax / 12)` yields 0.50 at `base_tax` 6 against the observed 0.49;
§2.3's `trunc(base_tax × 0.083333)` yields 0.49. The document carries both and treats them as one
rule.

**S7. Where the construction behind a figure is not stated, the figure does not reproduce.** §3.10
says so explicitly (Y135) and then quotes +7.4%, a 17.8-point range and "at most 0.1%" without
stating which countries collect or how the mean share is weighted. Independent reconstruction lands
on +7.8% and 17.7 points (close) and on 0.00% or 0.54% for the mean-share bound (not close),
depending on a reading the document leaves open.

**S8. What the save settles, and how much it settles.** The 1444.11.11 save is the engine's own start
state and it confirms the three reads v6.0 adds: exactly 11 provinces devastated at exactly the areas
and levels `flavor_boh.15` grants; `base_tax` and `base_production` matching a history parse that
*accumulates* dated `add_base_*` on 2,472 of 2,472 provinces; and `is_city = yes` on all twenty
provinces whose history file omits or comments the line. That is the strongest part of v6.0 and it
holds without qualification.

---
# §0 — Front matter

### Y001 — v6.0 keeps v3.0's owner-agnostic wealth and makes it true by construction; wealth reads development, trade good and current condition, and nothing else
**Status:** CONFIRMED
**Method:** Read `per-good-trade-spec.md` lines 13–22 (§0) and 166–300 (§1.3) against
`scripts/solver.py` lines 55–116.
**Evidence:** §1.3's formula block reads `goods_produced = GP_COEFF · base_production · (1 + Σ
province-state goods modifiers)`, `trade_value = goods_produced · price`, `tax_value = TAX_COEFF ·
base_tax · (1 + Σ province-state tax modifiers)`. `solver.py`'s `province_table()` computes exactly
that: the only modifier applied is `STATE_GOODS_MOD["devastation"] * dev`, and `tmod = 0.0`. No
owner term, no trade-good modifier, no project, no building appears in either. The stipulation and
the implementation agree.

### Y002 — the two-test classifier and everything it governed are deleted, along with the whole-install sweep
**Status:** CONFIRMED
**Method:** Grepped the v6.0 spec for every artefact of the classifier and compared with
`v5-owner-agnostic/per-good-trade-spec.md`; read `solver.py`.
**Evidence:** Zero occurrences in v6.0 of `two tests`, `Local?`, `Enters wealth`, `centers_of_trade`,
`falun`, `krakow_cloth_hall`, `add_permanent_province_modifier`, `production_leader`,
`bonus_from_merchant_republics`, `has_dlc`, `Leviathan`. `great project` survives three times: the §0
deletion notice, §1.3's "what this gives up", and §3.13's list of key-granting sources — none of them
a classification. `solver.py` carries no `LOCAL_TAX_MOD`, `LOCAL_TV_MOD`, `MON_*` or `PERM_FLAT`
tables; v5's `solver.py` lines 62–76 carried all of them.

### Y003 — on the 1444 start the deleted apparatus was worth 0.98% of world wealth, 87 of 2,472 provinces (measure6.py)
**Status:** PARTIAL
**Method:** Reconstructed v5.0's modifier set (`v5-owner-agnostic/scripts/solver.py` lines 62–76) on
top of v6.0's province table and recomputed world wealth and the touched-province set; searched
`measure6.py` and `measure6.out` for either figure.
**Evidence:** Apparatus-on world wealth 10,699.85 against v6.0's 10,594.70 — a delta of 105.15,
which is **0.9827%** of the apparatus-on total and 0.9925% of the v6.0 field. So 0.98% is right on
the natural reading. The touched set is **88** provinces: 43 `gems` + 30 `incense` + 6
great-project + 10 permanent-modifier pids, less one overlap (pid 542, a `gems` province also
carrying `diamond_mines_of_golconda_modifier`). 87 is the same count under `is_city = yes` — incense
falls from 30 to 29 — which is the filter v6.0 withdrew in the same section. `measure6.py` prints
neither 0.98% nor 87; `measure6.out`'s 57 labels contain neither.
**Should say:** "worth 0.98% of world wealth over **88** of 2,472 provinces", and the figure needs a
script that computes it.

### Y004 — what the apparatus cost was an input surface whose classification was wrong in every audit that examined it
**Status:** PARTIAL
**Method:** Read the classification verdicts in `validation-v3.md`, `validation-v4.md` and
`validation-v5.md`.
**Evidence:** `validation-v3.md` refutes it (W041: "exactly three" local modifiers — at least a
fourth, `chinaware`'s `province = { local_autonomy = -0.1 }`, plus a whole further class,
`bonus_from_merchant_republics`). `validation-v5.md` refutes it twice (X030: the locality test's
enumerated attribute list excludes the four province-state modifiers the table then classifies as
local, and its "no country's state" clause excludes `occupied` and `under_siege` outright; X034:
v4.0 stated the rule and swept only `common/tradegoods/`). But `validation-v4.md` examined the
classification and graded every repair CONFIRMED — its own summary reads "No claim is left PARTIAL
and none is REFUTED", over 203 assertions, 0 failed, including W041's and W160's classification
repairs. An audit examined it and did not find it wrong.
*On what kind of audit v4.0's was.* It is structurally not the same instrument as the other two.
`validation-v3.md` and `validation-v5.md` each enumerate a claim inventory (W001–W195, X001–X196) and
grade every row adversarially, refuting 12 and 22 respectively. `validation-v4.md` grades no
inventory: its scope is "the 29 graded claims `validation-v3.md` left open", its instruments
`validate_v4.py` and `validate_v4b.py` ship inside **v4.0's own `scripts/` directory**, and it asserts
that v3.0's stated repairs are *present* rather than attacking whether they are right — returning 203
assertions, 0 failed, and "No claim is left PARTIAL and none is REFUTED". `validation-v5.md` then
refuted the very classifier that harness had passed (X034: v4.0 "stated the rule and then swept only
`common/tradegoods/`"). So a self-check's CONFIRMED is weak evidence and nothing should be built on
it — but it is still an audit that examined the surface and did not find it wrong, so the
unrestricted universal is false either way.
**Should say:** replace the quantifier with the count, which is both true and stronger: "wrong in both
independent audits that examined it — `validation-v3.md`'s W041 and `validation-v5.md`'s X030 and
X034 — and passed by v4.0's own repair harness, which v5.0 then refuted." R2 asks for a scoped
observation rather than a universal, and the self-audit's miss belongs *inside* the case for R1, not
outside it. The claim should be narrowed, not dropped.

### Y005 — three start-state reads are corrected: on_startup devastation, dated add_base_* accumulation, and the is_city filter the engine does not apply
**Status:** CONFIRMED
**Method:** All three checked against the 1444.11.11 save with an independent `gamestate` parser, and
against the history files.
**Evidence:** (i) The save carries `devastation` on exactly 11 provinces and on no others
(265:20, 266:50, 267:20, 1771:20, 2967:20, 2968:50, 2970:50, 4237:20, 4724:50, 4725:50, 4726:20); no
`history/provinces/` file records any of it. (ii) A history parse that *accumulates* dated
`add_base_*` matches the save's `base_tax` and `base_production` on 2,472 of 2,472 owned provinces —
0 mismatches. (iii) 2,472 owned provinces in the save; 2,452 of their history files carry
`is_city = yes`; the save shows `is_city=yes` for all 2,472, province 265 (Brno, `#is_city = yes`)
included. All three reads are real and all three are corrections.

### Y006 — a canonical node order is a correctness requirement because Phase 2's min-cost flow is degenerate
**Status:** CONFIRMED
**Method:** Built a self-contained DRAIN parameterised by node labelling and arc presentation order
and ran 29 goods × 20 random relabellings on the 1444 field, mapping each result back through the
inverse permutation.
**Evidence:** *independent* — orientation changed on **580 of 580** runs, and the LP's optimal
support changed on 580 of 580, so presentation order selects the optimum rather than a tiebreak
resolving it. Mean 21.62 of 159 edges moved (min 2, max 51); max objective difference 2.66e-15.

### Y007 — prose convention R2, no empirical absolutes
**Status:** CONFIRMED
**Method:** Read the stipulation for internal consistency and checked whether the document obeys it.
**Evidence:** The rule as stated is coherent and self-applying. The document mostly obeys it — the
Cape universal is now scoped ("checked from `genua`, `north_sea` and `english_channel`"), the α_Φ
band is presented as what the value buys rather than as a derivation, and `verify6.py` carries five
absence checks for the specific absolutes v5.0 asserted. Two violations survive and are graded
separately: Y004/Y020's "wrong in every audit that examined it", and Y082/Y083's implicit universal
that the cooldown reaches only the banded policies.

### Y008 — prose convention R3, no maintained figures for any rejected operator
**Status:** CONFIRMED
**Method:** Grepped the v6.0 spec for every figure the graveyard carried in v2.0–v5.0, and
re-measured the one load-bearing comparison the rule converts into a direction.
**Evidence:** Zero occurrences of `60.3`, `62.7`, `97 of 159 arrows`, `13 end nodes`, `88.4`,
`110 of 159`. §3.9's `Φ_ord` bullet and §3.15's `Φ_ord`, gravity, RANK and basin entries carry no
percentages. The direction that replaces the figure — `Φ_ord` "scores higher than `Φ_w` on
self-coherence" — is true: *independent* re-measurement on the v6.0 field gives `Φ_ord` 60.5%
edge-goods / 59.0% value-weighted against `Φ_w`'s 53.5% / 52.1%.

### Y009 — those rejected-operator numbers were re-measured and re-refuted in three successive audits and not one of the rejection arguments depends on them
**Status:** CONFIRMED
**Method:** Read the relevant sections of `validation-v2.md` and `validation-v5.md`; re-measured
`Φ_ord`'s self-coherence and the gravity kernel's vanilla-arrow agreement on the v6.0 field; checked
each rejection argument for numeric dependence.
**Evidence:** `validation-v2.md` refutes `Φ_ord`'s 62.7% (V062: 60.2% under the deterministic sweep
the spec itself adopts) and the gravity kernel's 69% (line 1989: "62% over most of the γ plateau —
not 69%"). `validation-v5.md` refutes the gravity entry's "every larger γ is worse" (X190).
*independent* on the v6.0 field: `Φ_ord` 60.5%, gravity best 105/159 = 66%. Three different values
for each across three fields. The rejection grounds are non-numeric in every case — `Φ_ord`'s ends
are scheduling artifacts, the gravity kernel pins the count by fiat and needs a second knob, RANK is
monotone, basins strand demand — and none of the four cites a figure.

### Y010 — every graded claim from validation-v5.md (22 refuted, 39 partial, 1 unverifiable) is folded through, and fixes-agreed.md maps each one
**Status:** CONFIRMED
**Method:** Parsed all `### Xnnn` / `**Status:**` pairs out of `validation-v5.md`; checked each open
ID against `fixes-agreed.md`.
**Evidence:** 196 graded sections, no duplicates, counts exactly 134 CONFIRMED / 39 PARTIAL / 22
REFUTED / 1 UNVERIFIABLE. The 62 open IDs (22 + 39 + 1) all appear in `fixes-agreed.md`; the set of
open IDs absent from it is empty.

### Y011 — measured figures carry the script that produced them, and scripts/verify6.py re-derives each one from the document text and fails if the two disagree
**Status:** REFUTED
**Method:** Read `verify6.py` in full; ran it against the spec; traced each needle back to whether
its value is computed or typed; counted the measured figures in the spec that it does not touch;
recomputed the one figure a literal asserts.
**Evidence:** `verify6.py` runs **22 checks** on the spec. Eight are `absent(...)` text checks (R2
and R3 needles). Of the remaining fourteen, five carry **hardcoded literals** rather than values from
`measure6.out`: `shows(..., "**{:.1f}%** ({:,} of {:,})", O["ordered pairs connected pct"], 5703,
6320)`, `shows(..., "**{} ordered pairs**", 132)`, `shows(..., "flips **{} of\n159 …**", 13)`,
`shows(..., "**{}** textual `change_price` blocks", 161)`, and `shows(..., "**{:.2f}** wide
([{:.2f}, {:.2f}]", 1.70, 3.51, 5.21)`. The `13` is false — *independent* recomputation of the coal
activation on the v6.0 field gives **10** flips (see Y049) — so the harness passes a figure the
install contradicts, which is precisely the failure mode it was written to prevent. Coverage: the
spec quotes on the order of fifty measured figures; fourteen are checked. Nothing checks the razed-
China flip counts, the demand-decile rates, the caravan percentages, the 580/580 sweep, the α scan's
non-monotone sample, the ULP figures, the spice multiples, the ×1.65/×2.15 node thresholds or the
Cape-reversal window. Finally, "measured figures carry the script that produced them" fails twice:
Y003's 0.98%/87 and Y049's 13/217 both cite `measure6.py`, which computes neither.
**Should say:** that a named subset of figures is re-derived from the document, with the subset
listed; and the coal-flip needle must be computed, not typed.

---

# §1.1 — Trade direction

### Y012 — the fallback fires only when every candidate is support-isolated with zero post-peel balance
**Status:** CONFIRMED (derivation)
**Method:** Checked the argument against `drain.py`'s `sweep_priority` (lines 202–258) and `phase0`
(lines 31–47).
**Evidence:** `ready(u)` returns true when `len(outs[u]) > 0`, so a candidate holding any flow
out-arc is already popped and cannot be at a stall. `terminals` is taken over gated nodes with
`len(outs[u]) == 0 and inflow[u] > ZERO_TOL`, so a candidate with flow inflow goes down the
promotion branch. The fallback therefore requires every candidate to carry no flow arc in either
direction. The LP's node-balance constraint forces `inflow − outflow = −β(v)`, so a support-isolated
node has `β(v) = 0` exactly. And `β` is the vector `phase0` returns, with each pendant's balance
added into its parent (`beta[u] += beta[v]`), so the condition is on the folded field and a map whose
raw `b` is nowhere zero can still reach the branch.

### Y013 — on a connected core the folded balance must vanish across the core; for the aggregate graph each node's Σ wealth^α_Φ equal, which uniform wealth gives but is not the same condition
**Status:** PARTIAL (derivation)
**Method:** Checked the stated condition against the definition of `c_w`, then instantiated "uniform
wealth" on the 1444 map and measured `b_w`.
**Evidence:** The condition is correctly derived: `b_w(n) = 1/N − c_w(n)` vanishes for all `n` iff
`c_w(n) = 1/N` for all `n` iff `Σ_{p∈n} wealth(p)^α_Φ` is equal across nodes. The parenthetical is
false. Under uniform wealth `w`, `Σ_{p∈n} w^α = |n| · w^α`, which is equal across nodes only if every
node holds the same number of counted provinces. *independent* — counted provinces per node run
**0** (`cape_of_good_hope`) to **72** (`mexico`), and setting every province's wealth to 1 leaves max
`|b_w|` = **0.01663** with all 80 nodes non-zero, at α_Φ = 1.0 and at 1.5 alike.
**Should say:** each node's `Σ wealth^α_Φ` equal — which uniform wealth gives only on a map whose
nodes hold equally many counted provinces, and vanilla is not such a map.

### Y014 — where the wealth key ties the node index decides, which is why §2.8 asserts containment over a set that includes the fallbacks
**Status:** PARTIAL (derivation)
**Method:** Read `drain.py`'s fallback line and §2.8's and §3.2's own statements of why the fallback
set is in the containment assertion.
**Evidence:** The first half is exact: `s_star = max(gated, key=lambda v: (NODEW[v], -v))` breaks a
wealth tie to the **lowest** index, matching §1.1's "ties by index". The causal half is wrong. §2.8
says "Asserting containment in `{selected} ∪ {promoted}` alone would halt on **T3**", and §3.2's T3
is a triangle with node wealth 3, 2, 1 — distinct wealths, no tie — where the fallback promotion is a
sink in neither set. The reason the fallbacks are in the containment set is T3, which holds whether or
not the key ties; on 1444 the key cannot tie at all, node wealth being 80-of-80 distinct.
**Should say:** "Where the wealth key then ties, the node index decides. Separately, a fallback
promotion can itself be a sink (T3), which is why §2.8 asserts containment over a set that includes
the fallbacks."

### Y015 — the fallback's index tiebreak is not the reason §2.4 requires a canonical node order; that requirement is stronger and is set by Phase 2
**Status:** CONFIRMED (derivation)
**Method:** Checked against the relabelling result.
**Evidence:** *independent* — 580 of 580 relabellings changed the orientation and 580 of 580 changed
the LP support, with zero exact `(DEF, β)` key collisions anywhere in any core (see Y102) and zero
fallbacks fired on any good. The orientation therefore moves under relabelling with no tie of any
kind available to decide it, which is exactly the claim.

### Y016 — on 1444 the fallback and pendant cases are empty and the sink set is exactly {selected ∩ flow-terminal} ∪ {promoted} — 29/29 goods, 1–8 sinks per good, mean 3.52, zero fallbacks
**Status:** CONFIRMED (measurement)
**Method:** For each of the 29 live goods, ran `run_drain`, computed the actual sink set from the
directed edges, and computed the formula set from `r["S0"]` intersected with the flow-arc-terminal
nodes, unioned with `r["promotions"]`.
**Evidence:** *independent* — equality holds on **29 of 29** goods, no misses. Sinks per good min 1,
max 8, mean 3.52. Fallbacks summed over goods: 0. Phase 0 is a no-op (minimum degree 2 on the vanilla
map, so `core` is all 80 nodes and `Plog` is empty). Matches `measure6.out` lines 21 and 23.

### Y017 — that equality does not become a theorem by attaching conditions, because T2 satisfies both and still breaks it
**Status:** CONFIRMED (derivation, with the counterexample re-run)
**Method:** Ran `toys.py`.
**Evidence:** T2 is the five-cycle `S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1` with chord `w–S1`. Every
degree is ≥ 2 so Phase 0 removes nothing, and the run reports no fallback. `S0 = {u1, u2}`, both
flow-terminal, and the actual sink set is `{u2}` against a formula set of `{u1, u2}` — the free edge
orients `u1→w` after `w` becomes ready via `u2`. The two stated conditions hold and the equality
fails, so they are necessary and not sufficient.

---
# §1.3 — Demand

### Y018 — wealth reads development, trade good and current condition; two provinces alike in those three have the same wealth whoever owns them
**Status:** CONFIRMED
**Method:** Read §1.3 and `solver.py`'s `province_table()`.
**Evidence:** The only inputs are `base_tax`, `base_production`, `trade_goods` (via `PRICES`) and the
devastation level. No owner tag, no country state, no autonomy, no efficiency appears anywhere in the
computation. Two provinces with equal `base_tax`, `base_production`, good and condition receive
identical `tax` and `prod_income` by construction.

### Y019 — owner-agnosticism is true by construction, not by a policed rule: base_tax, base_production and the trade good are bare attributes of the place
**Status:** CONFIRMED
**Method:** Checked the three inputs' provenance in `history/provinces/` and in the save.
**Evidence:** All three are keys of the province's own history block (`base_tax`, `base_production`,
`trade_goods`) and of the province's own save block; none is a function of the owner tag. Nothing in
the chain requires a locality test, because no modifier is consulted. The property is structural.

### Y020 — v3.0 through v5.0 stated the property and then defended it with a two-test classifier over an install sweep, wrong in every audit that examined it
**Status:** PARTIAL
**Method:** As Y004.
**Evidence:** The first half is exact — v3.0 §1.3, v4.0 §1.3 and v5.0 §1.3 all carry the two-test
rule and its table. The universal fails for the same reason as Y004: `validation-v4.md` examined the
classification and graded every repair CONFIRMED, and although it is a self-check rather than an
adversarial inventory audit, it is still an audit that looked and passed it.
**Should say:** as Y004 — the count over independent audits, not a universal.

### Y021 — what this gives up: gems' local_tax_modifier and incense' trade_value_modifier are genuinely province-scoped and are no longer read, along with great projects, permanent province modifiers and the DLC state
**Status:** CONFIRMED
**Method:** Opened `common/tradegoods/00_tradegoods.txt`; grepped the v6.0 spec and `solver.py`.
**Evidence:** `gems` (line 2015) carries `province = { local_tax_modifier = 0.15 }` and `incense`
(line 1890) carries `province = { trade_value_modifier = 0.1 }` — both inside the province-scoped
block, so both are genuinely province-scoped. Neither appears in `solver.py`. The great projects,
permanent modifiers and the Leviathan gate are gone from both the spec and the solver (Y002).

### Y022 — goods_produced = GP_COEFF · base_production · (1 + Σ province-state goods modifiers), with no local-modifier sweep term and no flat-bonus term
**Status:** CONFIRMED
**Method:** Compared §1.3's formula block with `solver.py` line 108.
**Evidence:** `gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))` where
`gmod = STATE_GOODS_MOD["devastation"] * dev`. No additive term and no sweep term.

### Y023 — trade_value = goods_produced · price, ducats per year, with no trade-value-modifier term
**Status:** CONFIRMED
**Method:** As Y022.
**Evidence:** `prod_income = gp * price` in `solver.py` line 111; §1.3's block reads
`trade_value(p) = goods_produced(p) · price(good(p))  # ducats / YEAR`. No multiplier.

### Y024 — tax_value = TAX_COEFF · base_tax · (1 + Σ province-state tax modifiers), ducats per year
**Status:** CONFIRMED
**Method:** As Y022.
**Evidence:** `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)` with `tmod = 0.0` at 1444 (only
`occupied` sets it, and no province is occupied at the start). Matches the spec's block.

### Y025 — ⚑ GP_COEFF is a shipped file value: 00_static_modifiers.txt carries provincial_production_size = { trade_goods_size = 0.2 … }, localised "Base Production"; it is moddable and read at runtime
**Status:** CONFIRMED
**Method:** Opened `common/static_modifiers/00_static_modifiers.txt` and
`localisation/EU4_l_english.yml`; read `solver.py`'s `_read_gp_coeff()`.
**Evidence:** Lines 251–254 of the static-modifier file:
`provincial_production_size = { trade_goods_size = 0.2  ship_recruit_speed = -0.01 }`.
`EU4_l_english.yml` line 815: ` provincial_production_size:0 "Base Production"` — the same label as
the tooltip line the coefficient was measured off (`Base Production: +0.80` at `base_production` 4,
and 0.2 × 4 = 0.8). `solver.py` reads the value from the file and raises if the block is missing, so
"read at runtime, not hardcoded" is true of the emitter. *Note on strength:* the file states the value
and the label; that this block **is** the engine's per-`base_production` coefficient is an inference
from the value matching 0.2 and the localisation matching the tooltip line, not a statement in any
file. The inference is strongly supported and is not proof.

### Y026 — TAX_COEFF is in no file that has been found
**Status:** CONFIRMED
**Method:** Searched `common/defines.lua`, all five files in `common/defines/`, and the whole of
`00_static_modifiers.txt`, including the tax analogue of the production block.
**Evidence:** No define in `defines.lua` or its overrides carries a per-`base_tax` coefficient (the
only tax-adjacent hits are `ALLOW_ZERO_BASE_VALUES`, `PS_RAISE_WAR_TAXES`,
`ENFORCE_CULTURE_TAX_MULTIPLIER`, `SCUTAGE_TAX_FRACTION`, `BASE_TAX_COST_MODIFIER`,
`FLAT_TAX_AMOUNT` — none of them it). `provincial_tax_income` exists at line 244 of the
static-modifier file and grants `regiment_recruit_speed`, `local_great_project_upgrade_time`,
`local_build_time` and `local_institution_spread` — no tax-value key at all. The asymmetry with
`provincial_production_size` is real and is what the claim asserts.

### Y027 — ⚑ the tax tooltip's schema is Base: trunc(base_tax / 12) (Yearly base_tax); the parenthetical is base_tax itself, not twelve times the displayed figure
**Status:** PARTIAL
**Method:** Arithmetic on the claim's own two data points, and comparison with §2.3's rule for the
same quantity.
**Evidence:** The retraction is correct: 12 × 0.49 = 5.88 ≠ 6.00 and 12 × 0.16 = 1.92 ≠ 2.00, so
`Base: X (Yearly 12·X)` is false on both points, and reading the parenthetical as `base_tax` itself
fixes both. But the replacement is false on the first point: `trunc(6 / 12) = trunc(0.5) = 0.50`,
against the observed **0.49**. `trunc(2 / 12) = 0.16` ✓. §2.3's own table states the rule that works —
"The displayed monthly is the truncation of `base_tax × 0.083333`" — giving 6 × 0.083333 = 0.499998 →
0.49 and 2 × 0.083333 = 0.166666 → 0.16. The document carries both forms and treats them as one.
*The tooltip readings themselves are engine tests from an earlier session and are not re-observable
here without running the game; the arithmetic internal to the claim is checkable and it fails.*
**Should say:** `Base: trunc(base_tax × 0.083333) (Yearly base_tax)`, matching §2.3.

### Y028 — v3.0 through v5.0 wrote that schema as Base: X (Yearly 12·X), which is false on both of its own data points
**Status:** PARTIAL
**Method:** Grepped `Yearly 12` in all three prior specs and read v3.0's own passage.
**Evidence:** v4.0 line 163 and v5.0 line 170 both write `Base: X (Yearly 12·X)`. v3.0 has zero
occurrences; its passage (lines 147–152) reads "the tax tooltip reads `Base: 0.49 (Yearly 6.00)` for
a province with `base_tax = 6` … Both monthly figures are the annual value over twelve". v3.0 carries
the same arithmetic defect implicitly but never states the `12·X` schema. The falsity on both data
points is confirmed.
**Should say:** "v4.0 and v5.0 wrote that schema as `Base: X (Yearly 12·X)`".

### Y029 — §  the monthly production tooltip's Trade Value line is consistent with the same annual-over-twelve relation on one observation, 3.52 → +0.29, which fixes the divisor only to within [12.00, 12.14]
**Status:** PARTIAL
**Method:** Inverted the truncation on the stated observation.
**Evidence:** A displayed 0.29 under truncation to two decimals means the true value lies in
[0.29, 0.30). With numerator 3.52 the divisor satisfies 3.52/0.30 < d ≤ 3.52/0.29, i.e.
**d ∈ (11.733, 12.1379]**. The upper end is right (12.1379 → "12.14"). The lower end, 12.00, is not
what the observation fixes — it is a prior that the divisor is at least twelve. As written the claim
attributes the whole interval to the observation.
**Should say:** "fixes the divisor only to within (11.73, 12.14], or to [12.00, 12.14] once the
divisor is assumed to be at least twelve."

### Y030 — both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the tax pair establishes it at two development levels
**Status:** CONFIRMED (derivation)
**Method:** Checked the argument.
**Evidence:** If tax and trade value are both displayed as annual/12, their annual forms are
commensurable and `wealth = tax_value + trade_value` needs no conversion — which is what the claim
asserts and it follows. The tax pair does establish the relation at `base_tax` 2 and 6, two distinct
development levels, under §2.3's `× 0.083333` reading. It does not repair Y027's schema, which is
graded there.

### Y031 — ⚑§ on Garnatah base_tax 6 with Tax Income Efficiency 125.0% displays Base 0.49 then 0.62; the engine multiplies the untruncated monthly value, and the example establishes the ordering and nothing finer
**Status:** CONFIRMED
**Method:** Arithmetic on both readings of the observation; checked against §2.3's truncation rule.
**Evidence:** 0.49 × 1.25 = 0.6125, which truncates to 0.61 — so the displayed 0.62 cannot come from
multiplying the shown figure. 6 × 0.083333 = 0.499998; × 1.25 = 0.6249975, which truncates to 0.62 ✓.
The claim's reasoning is exactly right, and its scope statement ("establishes the ordering … and
nothing finer") is the honest one: with only one percentage and one province the observation cannot
separate this from other multiply-then-truncate schemes. *The tooltip reading itself is a single
engine observation from a prior session; only a running game could re-observe it. Everything else in
the claim is arithmetic and it holds.*

### Y032 — v3.0 through v5.0 read that observation as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires truncation
**Status:** PARTIAL
**Method:** Grepped `0.6125` in all three prior specs.
**Evidence:** v4.0 line 178 and v5.0 line 185 both read "giving 0.6125, which the province window
shows as 0.62". v3.0 has **zero** occurrences of `0.6125` (its only `0.62`-family hit is `0.625`, a
price floor in §3.5). The incompatibility with §2.3's truncation rule is correctly diagnosed for the
two versions that carry it.
**Should say:** "v4.0 and v5.0 read this as …".

### Y033 — flat goods bonuses would add into goods_produced before the price multiply, but under §1.3 no source grants one, so the ordering is exercised by no province in the model
**Status:** CONFIRMED
**Method:** Checked `solver.py` for any additive goods term and the four condition modifiers for a
flat grant.
**Evidence:** `province_table()` has no additive term of any kind; the four province-state modifiers
are all multiplicative `trade_goods_size_modifier` values, and none is a flat `trade_goods_size`. So
no counted province receives a flat bonus, and the ordering statement is inert — exactly as claimed.
The tooltip-shape half ("an additive `Base Goods Produced` block above a multiplicative `Goods
Produced Efficiency` block") is a prior engine observation, not re-observable here, and the claim
already labels it as establishing nothing beyond the ordering.

### Y034 — ⚑ four static modifiers from 00_static_modifiers.txt describe province condition: devastation (trade_goods_size_modifier = −2, scaled by the devastation level), prosperity +0.25, under_siege −0.25, occupied −0.5 plus local_tax_modifier −0.5
**Status:** PARTIAL
**Method:** Opened the four blocks; searched the file for any statement of scaling; searched the save
for a per-province `goods_produced` or `trade_goods_size` field that would settle it.
**Evidence:** Every value is exact. `devastation` (line 453) `trade_goods_size_modifier = -2`;
`prosperity` (464) `trade_goods_size_modifier = 0.25`; `under_siege` (444)
`trade_goods_size_modifier = -0.25`; `occupied` (433) `local_tax_modifier = -0.5` **and**
`trade_goods_size_modifier = -0.5`. The scaling is not settled. The file marks scaled blocks with a
comment where it marks them at all (`# Multiplied with positive religious tolerance` above
`tolerance`); no such comment sits above `devastation` or `prosperity`. The save stores no
per-province `goods_produced` or `trade_goods_size` — province 266 (Praha, devastation 50) carries
`base_production=8.000`, `trade_goods=cloth`, `devastation=50.000` and no derived production field —
and province `trade_power` does not decompose cleanly enough to infer it (the ratio
`trade_power / (0.2·base_production·price)` has median 1.50 with a p10–p90 span of 0.97–4.26 across
undevastated provinces, so the eleven devastated ones sit inside the noise). Only a running game
settles this. Separately, `prosperity` is the same kind of 0–100 province-state scalar as
`devastation`, so if one scales the other does, and the table marks only one.
**Should say:** mark the scaling as an engine behaviour that the files do not state, and apply it to
`prosperity` as well as `devastation` or to neither.

### Y035 — only occupied touches the tax term; the other three reach goods_produced alone
**Status:** CONFIRMED
**Method:** Read all four blocks in full.
**Evidence:** `devastation` grants `trade_goods_size_modifier`, `supply_limit_modifier`,
`local_institution_spread`, `local_development_cost`, `local_manpower_modifier`,
`local_sailors_modifier` and two movement-speed keys — no tax key. `prosperity` grants
`local_development_cost`, `trade_goods_size_modifier`, `local_autonomy` — no tax key. `under_siege`
grants `trade_goods_size_modifier`, `province_trade_power_modifier`, `local_institution_spread`,
`local_monthly_devastation` — no tax key. `occupied` is the only one carrying `local_tax_modifier`.

### Y036 — those four are what make the map answer to war; §1.2's volatility, §3.3's besieged province and §2.8's war rows all rest on them
**Status:** CONFIRMED (derivation)
**Method:** Cross-read §1.2, §3.3 and §2.8 against the four modifiers.
**Evidence:** §1.2 names exactly these four as what moves `goods_produced`; §3.3's "a besieged
province genuinely produces less" is `under_siege`'s −0.25; §2.8's "Major war in China — corridors
shift for the duration, revert as devastation heals" is `devastation`. Under R1 they are the only
war-sensitive inputs left in the model, so the dependency is not merely stated but exclusive.

### Y037 — ⚑ eleven counted provinces begin the 1444 start devastated (Bohemia at 50, Erzgebirge and Moravia at 20) with no province-history file saying so; the chain is 00_on_actions.txt → on_startup_effect → 01_scripted_effects_for_on_actions.txt → flavor_boh.15
**Status:** CONFIRMED
**Method:** Parsed the save's province blocks; opened `common/on_actions/00_on_actions.txt`,
`common/scripted_effects/01_scripted_effects_for_on_actions.txt`, `events/flavorBOH.txt` and
`map/area.txt`.
**Evidence:** The save carries `devastation` on exactly eleven provinces and no others, at exactly
these values: 266, 2968, 2970, 4724, 4725 at 50.000 and 265, 267, 1771, 2967, 4237, 4726 at 20.000.
`area.txt`: `bohemia_area = { 266 2968 2970 4725 4724 }` (5), `erzgebirge_area = { 267 1771 2967 }`
(3), `moravia_area = { 265 4237 4726 }` (3) — eleven, matching exactly.
`events/flavorBOH.txt`'s `flavor_boh.15` has `immediate = { hidden_effect = { bohemia_area = {
add_devastation = 50 } erzgebirge_area = { add_devastation = 20 } moravia_area = {
add_devastation = 20 } … } }`. `00_on_actions.txt` line 4 `on_startup` calls `on_startup_effect = yes`;
`01_scripted_effects_for_on_actions.txt` line 4716 defines `on_startup_effect` and it contains
`if = { limit = { tag = BOH … } set_country_flag = boh_hussite_aftermath_flag country_event = { id =
flavor_boh.15 } }`. Every link in the chain is present and the outcome matches the engine's own start
state. X040's "all are zero at the 1444 start" is indeed refuted.

### Y038 — that start devastation costs 13.40 ducats across the eleven affected counted provinces (measure6.py)
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; and independently recomputed from the save's own `base_tax`,
`base_production`, `trade_goods` and `devastation` fields with and without the devastation term.
**Evidence:** `measure6.out` line 6: `devastation cost in ducats  13.4`. *independent* — world wealth
from the save with devastation 10,607.40, without devastation 10,620.80; difference **13.40**. Two
independent routes, same figure.

### Y039 — the start state is what the engine produces, not what the history files say
**Status:** CONFIRMED (derivation)
**Method:** Checked the general claim against all three instances.
**Evidence:** Each of the three reads is a case where the history files alone give the wrong answer:
devastation appears nowhere in `history/provinces/` yet eleven provinces carry it; `base_tax` needs
dated accumulation, not replacement; `is_city = yes` is absent from twenty owned provinces the engine
treats as cities. The generalisation is supported by all three of its own instances and by the save,
which is the engine's output.

### Y040 — ⚑ on_startup also fires flavor_mng.42, flavor_mos.1, flavor_geo.1 and others, and flavor_geo.1 carries add_base_tax, add_base_production and add_devastation, so development itself can move before the first tick
**Status:** REFUTED
**Method:** Read `on_startup`'s `events = { }` list in `00_on_actions.txt`; then **brace-matched every
`country_event = { … }` block in `events/FlavorGEO.txt`** with a scanner that skips quoted strings and
line comments, recorded each block's `id` and line span, and assigned every `add_base_*` /
`add_devastation` occurrence in the file to the block whose byte range contains it. Fixed-width windows
around each `id =` match are not safe here — the blocks run 39 to 53 lines and sit adjacent, so a 60-
or 80-line window straddles the next event and shows `.1` holding `.3`'s keys. Finally compared the
history-derived development against the save.
**Evidence:** The first half is right, and it is right for a reason worth stating precisely:
`on_startup` fires `flavor_geo.1` **from its own `events = { }` list** in
`common/on_actions/00_on_actions.txt` — `{ muslim_school_events.20, flavor_got.1, flavor_mng.42,
flavor_mos.1, flavor_fra.206, flavor_geo.1, flavor_mam.111 }` — not through `on_startup_effect`.
Grepping only `01_scripted_effects_for_on_actions.txt` finds neither `flavor_geo.1` nor `flavor_geo.3`
(both absent from it) and would wrongly suggest the event is never fired at all.
The second half is false. `events/FlavorGEO.txt` holds seven brace-matched event blocks —
`flavor_geo.1` lines 8–46, `.2` 49–95, `.3` 98–150, `.4` 153–195, `.5` 198–234, `.6` 237–271,
`.7` 274–324 — and **all five** `add_base_*` / `add_devastation` occurrences in the file fall inside
`.3`: `add_devastation = 100` (line 111), `add_devastation = 50` (131), `add_base_tax = 2` (135),
`add_base_production = 2` (136), `add_base_manpower = 1` (137). `flavor_geo.1`'s whole effect is
`add_legitimacy = -20`, `add_country_modifier = { name = "geo_powerful_nobles" duration = -1 }` and
`set_country_flag = geo_received_starting_event`, gated on `tag = GEO` and
`has_dlc = "King of Kings"`. The file's `add_devastation = 100`, `add_devastation = 50`,
`add_base_tax = 2` and `add_base_production = 2` (lines 111, 131, 135, 136) all belong to
**`flavor_geo.3`** ("Sack of Sarai"), which is not in `on_startup`'s list. `flavor_mng.42` grants a
country modifier and a flag; `flavor_mos.1` grants `the_tatar_yoke` country modifier. And the
conclusion fails on this start empirically: a history parse that accumulates dated `add_base_*`
matches the save's `base_tax` and `base_production` on **2,472 of 2,472** owned provinces, so nothing
`on_startup` fires moves development at 1444.
**Should say:** `on_startup` also fires `flavor_mng.42`, `flavor_mos.1` and `flavor_geo.1` — keep that
half, it is true and correctly sourced — none of which moves development or devastation;
`flavor_boh.15` is the only start-state mover found, and on this start development is unchanged from
the history files once dated grants are accumulated. Drop the "development itself can move before the
first tick" clause: no on-action in the install reaches an `add_base_*`, and the 2,472/2,472 match
settles it empirically for this start.

### Y041 — ⚑ add_base_* in a dated block before the start date accumulates: province 1 (Uppland) has base_tax = 5 undated plus 1 at 1436.4.28, and the game has 6
**Status:** CONFIRMED
**Method:** Opened `history/provinces/1-Uppland.txt`; read province 1 from the save; ran
`provinces.py` and diffed its output against the save for all 2,472 owned provinces.
**Evidence:** The history file carries `base_tax = 5` undated and
`1436.4.28 = { … add_base_tax = 1 }`. The save's province −1 reads `base_tax=6.000`,
`base_production=5.000`, `name="Stockholm"`. Accumulation is therefore right, and it is right
globally: 0 `base_tax` mismatches and 0 `base_production` mismatches across 2,472 provinces.
*Nomenclature note:* the parenthetical "(Uppland)" is the history filename; the province's in-game
name is Stockholm (`prov_names_l_english.yml`: ` PROV1:0 "Stockholm"`, and the save agrees). Not
graded against the claim, which is about the value.

### Y042 — v5.0 and earlier overwrote instead of adding such grants, silently dropping them
**Status:** CONFIRMED
**Method:** Read `v5-owner-agnostic/scripts/provinces.py` lines 37–41 and compared with v6.0's lines
37–55.
**Evidence:** v5's dated-block loop is `for k, v in blk: … state[k] = v` with no special case, so
`add_base_tax = 1` is stored under the key `"add_base_tax"` and `base_tax` stays 5. v6's loop carries
`ADD = {"add_base_tax": "base_tax", …}` and does `state[tgt] = float(state.get(tgt, 0) or 0) +
float(v)`. The drop was silent — nothing downstream reads `"add_base_tax"`.

### Y043 — ⚑ is_city = yes is not a filter the engine applies: 20 owned provinces omit or comment out the line, province 265 among them, and the engine treats them as cities
**Status:** CONFIRMED
**Method:** Ran `provinces.py`; read province 265's history file and its save block; listed the
twenty.
**Evidence:** `provinces.py` prints `owned at 1444.11.11: 2472` and `is_city=yes and owned: 2452` —
a difference of exactly **20**. The twenty are 265, 774, 857, 913, 958, 966, 1035, 1038, 1207, 2527,
2579, 2593, 2617, 2671, 2779, 2932, 4573, 4576, 4640, 4856. `history/provinces/265 - Brno.txt`
carries the line commented: `#is_city = yes`. The save's province −265 reads `is_city=yes`,
`owner="BOH"`, `devastation=20.000` — so it is a city, it is counted, and it is one of the devastated
eleven, exactly as the claim says.

### Y044 — the model counts a province when it has an owner and lies in a trade node — 2,472, not 2,452 — and treats every counted province as cored and settled
**Status:** CONFIRMED
**Method:** Counted owned provinces in the save and in the history parse; intersected with
`nodes.json` membership; read `province_table()`.
**Evidence:** 2,472 owned in the save, 2,472 owned in the history parse, identical sets (empty
symmetric difference both ways), and **all 2,472** lie in a trade node — so the node condition is
satisfied vacuously at 1444 and the count is 2,472. 2,452 is the `is_city = yes` subset. The solver
applies no coring or settlement term (`tmod = 0.0`, no `Core`/`City` factor), which is what "treats
every counted province as cored and settled" means.

### Y045 — ⚑ twenty counted provinces carry no trade good in their history file (trade_goods = unknown), and the engine assigns one at start from each good's chance = { } block
**Status:** CONFIRMED
**Method:** Counted `unknown` among owned provinces in the history parse; read the same provinces
from the save; opened `common/tradegoods/00_tradegoods.txt`.
**Evidence:** Exactly **20** owned provinces have `trade_goods = unknown` in history: 774, 862, 895,
897, 907, 966, 1809, 2014, 2503, 2510, 2571, 2593, 2596, 2669, 2671, 2932, 4856, 4901, 4902, 4923.
The save assigns each a real good — wool, wool, naval_supplies, grain, grain, fur, livestock, cotton,
fur, fur, fur, fur, grain, grain, fur, wool, incense, fur, livestock, grain — and those twenty are
the *only* provinces where the history parse and the save disagree on the good (20 of 2,472).
`00_tradegoods.txt` carries a `chance = { factor = … modifier = { … } }` block per good (e.g. `gems`
`factor = 5`, `incense` `factor = 25`), which is the assignment mechanism named.

### Y046 — the wealth field is therefore partly the result of one random draw, and the model does not predict the draw: it reads whatever state the game currently holds
**Status:** PARTIAL
**Method:** Checked the stipulation against the field every v6.0 figure is measured on.
**Evidence:** The stipulation is coherent and matches the design. It does not match the measurement.
`solver.py` sets `EXCLUDED = {"gold", "unknown"}` and `price = PRICES.get(g, 0.0)`, so an
`unknown`-good province contributes `tax` and **zero** production income — the field does not read
the game's state for those twenty, it prices them at nothing. *independent* — recomputing world
wealth with the engine's own assignments for the twenty gives **10,607.40** against the quoted
10,594.70, a gap of **12.70** ducats, and the twenty enter the per-good supply shares of six goods
they are currently absent from.
**Should say:** either that the reference implementation reads history and therefore treats the
twenty as valueless in production, quantifying the gap; or run the field off the save so the
stipulation and the measurement agree.

### Y047 — TAX_COEFF = 1.0 is a modelling choice with a known cost: two readings, both on cored city provinces at base_tax 2 and 6, and the development range runs past 50
**Status:** PARTIAL
**Method:** Read §2.3's coefficient table for the basis; computed the development range over the
2,472 counted provinces.
**Evidence:** The two-reading basis is exact — §2.3's table cites Garnatah `base_tax` 6 →
`Base: 0.49 (Yearly 6.00)` and Caceres `base_tax` 2 → `Base: 0.16 (Yearly 2.00)`, and nothing else.
*independent* — at the 1444 start max `base_tax` is **15**, max `base_production` is **15**, and max
total development (`base_tax + base_production + base_manpower`) is **33**; 66 provinces exceed
`base_tax` 6 and 5 exceed 10; **no** province exceeds development 50. So "the development range runs
past 50" is not a fact about this start. It is true of late-campaign states, which the claim does not
scope.
**Should say:** "the range the model must handle runs to `base_tax` 15 at the start and far higher
over a campaign", or scope the 50 to campaign states.

### Y048 — owner-agnostic wealth removes a large source of hidden owner-dependence — not "the single largest", as v3.0 through v5.0 had it
**Status:** CONFIRMED
**Method:** Grepped `single largest` in the three prior specs; read the v6.0 sentence.
**Evidence:** v3.0 line 180, v4.0 line 229 and v5.0 line 265 all read "It also removes the single
largest source of hidden owner-dependence"; v6.0 reads "a large source". The retraction is accurate
and the replacement is the weaker, unquantified form R2 asks for — no measurement is claimed, so none
is owed.

---

# §1.5 — Goods without a graph

### Y049 — repricing to coal the 45 owned latent-coal provinces flips 13 of 159 Φ_w edges and adds 217 ducats to world wealth (measure6.py)
**Status:** REFUTED
**Method:** Scanned all 3,923 `history/provinces/` files for `latent_trade_goods … coal`, took the
owned subset, repriced those provinces at coal's base price, and re-ran `Φ_w`. Cross-checked with the
v5 harness's own formula (`_w2[_i] = _r["tax"] + _r["gp"] * PRICES["coal"]`) and with the symmetric-
difference-over-two flip count v5 used. Searched `measure6.py` and `measure6.out` for either figure.
**Evidence:** *independent* — 58 latent-coal provinces in history, **45 owned** (both counts confirm
the claim's premises). Repricing gives world wealth 10,594.70 → **10,809.30**, i.e. **+214.60**
ducats, and **10 of 159** edges flip (identical under both flip metrics). The sink set is unchanged.
Without the devastation term the addition is 216.40 and the flip count is still 10. `measure6.py`
computes neither figure; `measure6.out` contains neither; `verify6.py` asserts the literal `13`
against the document, so the harness confirms a number the install contradicts.
**Root cause of the disagreement with 13/217.00.** The gap is one province and one inconsistency.
Province **4237** is in the latent-coal set *and* in the devastated eleven (devastation 20,
`base_production` 3). Repricing it while dropping its devastation factor — but leaving that factor in
the baseline — adds 0.2 · 3 · 10 · (1 − 0.6) = **2.40** ducats, which is exactly
217.00 − 214.60, and re-running the field that way yields exactly **13** flips. Verified both ways:
keep the factor → **+214.60 and 10 flips**; drop it → **+217.00 and 13 flips**; sink set
`{english_channel, hangzhou}` either way. So 13/217.00 measures repricing *plus* healing one
province's devastation, and 10/214.60 measures repricing alone. The latent set itself is not in
dispute: 58 by history file (the unbraced `latent_trade_goods = coal` form matches nothing extra), 45
owned and counted. The counterfactual has to be built from the history/model good rather than the
save's current good, because none of the 58 currently produces coal — so that candidate explanation
cannot bear on the gap either.
**Should say:** "flips **10 of 159** `Φ_w` edges and adds **214.60** ducats", with a script that
computes both and holds every non-repriced input fixed — province 4237's devastation included.
§2.8's latent-good row repeats the same 13 and needs the same correction.

### Y050 — coal's base price of 10.0 is the highest in the shipped price table, so a coal activation is near the upper end of what one good's activation can do
**Status:** CONFIRMED
**Method:** Parsed `common/prices/00_prices.txt` and sorted.
**Evidence:** 32 entries. `coal` 10.00 is the unique maximum; next is `cloves` 8.00, then four goods
at 4.00. `gold` and `unknown` are 0.00. The scoping to "the shipped price table" is the right
qualifier and the claim carries it.

---
# §1.6 — The aggregate graph

### Y051 — both the sink count and the sink locations move with the wealth field, and α_Φ sets how sharply concentration is read
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; read the Europe rows.
**Evidence:** At α_Φ = 1.5 held fixed, the 1444 field gives two sinks
(`english_channel`, `hangzhou`); Europe ×1.02 gives three (adds `wien`); Europe ×2.00 gives one
(`genua`). So with the constant fixed both the count and the placement move with the field — the
claim exactly. And with the field fixed, the count moves with α_Φ (6 → 2 → 1 → 2 → 3 → 1 across
α_Φ ∈ {1, 1.5, 2, 3, 4, 8}). Neither is a function of the other alone.

### Y052 — v2.0–v4.0's "the count emerges from concentration" and v5.0's "the count is set by α_Φ" are wrong the same way
**Status:** CONFIRMED
**Method:** Grepped the four prior specs.
**Evidence:** v2.0 line 154, v3.0 line 257 and v4.0 line 306 all read "Nothing pins their count; it
emerges from concentration exactly as per-good sink counts do." v5.0 line 342 reads "Their count is
set by `α_Φ`". Y051's measurement shows the count is a function of both, so each of the two prior
formulations drops one argument, which is the claim.

### Y053 — v2.1 chose the value with a target count in view — a calibration §2.3 withdraws without replacing
**Status:** CONFIRMED
**Method:** Grepped `calibrated` in `v2-drain/per-good-trade-spec.md`; read v6.0 §2.3.
**Evidence:** v2.0/v2.1 line 372: "the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444
start yields the two-sink …)". v6.0 §2.3 reads "**Every derivation previously offered for it is
withdrawn** … Neither is a reason" and offers no replacement derivation, only the stipulation. The
withdrawal is real and it is unreplaced.

### Y054 — scale: identical orientation at ×1 and above, 12 edge flips at ×10⁻² and 100 at ×10⁻⁶, so the orientation degrades while the sink set happens to survive
**Status:** PARTIAL (measurement)
**Method:** Scaled `b_w` by ×100, ×10, ×1, ×10⁻², ×10⁻⁴, ×10⁻⁶ and compared orientation and sink set
against the baseline.
**Evidence:** *independent* — flips 0 / 0 / 0 / **12** / 12 / **100**, matching all three quoted
counts. But the sink set is `{english_channel, hangzhou}` at ×100, ×10, ×1, ×10⁻² and ×10⁻⁴ and
**`{genua}`** at ×10⁻⁶. So the trailing clause is false at the very scale that produces the 100
flips.
**Should say:** "12 edge flips at ×10⁻², where the sink set survives, and 100 at ×10⁻⁶, where it
collapses to `{genua}` — so neither the orientation nor the sink set is safe once `b` is scaled below
the absolute tolerance."

### Y055 — 1444's b_w has largest magnitude 0.0226
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` line 17: `largest |b_w|  0.0226`. Reproduced on the rerun.

### Y056 — measured at α_Φ = 1.5: two sinks, english_channel and hangzhou — c_w ranks 2 and 3, node-wealth ranks 1 and 12
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; independently recomputed both rank vectors.
**Evidence:** `measure6.out` lines 9–11: sinks `['english_channel', 'hangzhou']`;
`english_channel (2, 1)`; `hangzhou (3, 12)`. *independent* — node-wealth order is
english_channel 316.6 (1), mexico 300.4 (2), gulf_of_siam 297.9 (3), genua 296.0 (4), malacca 295.2
(5), nippon 293.6 (6), sevilla 266.5 (7), rheinland 251.8 (8), champagne 247.8 (9), comorin_cape
241.0 (10), ganges_delta 234.6 (11), hangzhou 226.7 (12) — so ranks 1 and 12. `c_w` order at
α_Φ = 1.5 is genua, english_channel, hangzhou, gulf_of_siam, champagne — so ranks 2 and 3.

### Y057 — Phase 1 selects genua; both sinks arrive by stall promotion and genua ends a transit node, so 2 promotions and 0 fallbacks
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; checked `genua`'s degrees in the baseline orientation.
**Evidence:** `measure6.out` lines 12–13: `Phase-1 selection ['genua']`,
`promotions / fallbacks (2, 0)`. *independent* — `genua` has out-degree 2 (`alexandria`, `ragusa`)
and in-degree 3, so it is a transit node, not a sink.

### Y058 — eight sources, all in the bottom half of the wealth field (c_w ranks 44–75), mean degree 3.1 against the map's 4.0 — which is what v2's "cul-de-sacs" does not survive
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; independently listed the sources with their degrees and `c_w` ranks;
re-ran `phiw3.py`'s V216 block.
**Evidence:** *independent* — the eight are `kongo` (deg 3, rank 53), `james_bay` (2, 75),
`mississippi_river` (4, 70), `chengdu` (4, 52), `cuiaba` (5, 63), `australia` (2, 65), `yumen` (3, 51),
`safi` (2, 44). Rank range 44–75, all in the bottom half of 80. Mean degree 3.12 against the map's
3.98 — 3.1 vs 4.0 as quoted. Only **3 of 8** have degree 2, so "cul-de-sacs" is indeed not what these
are, and the claim's disavowal is supported by the degrees it cites.

### Y059 — every node drains to a sink; acyclic, 159/159 oriented; the sink set is unchanged under ±1% wealth noise on three seeds
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` lines 18–19: `edges oriented 159/159`, `acyclic True`; lines 40–42: all
three ±1% noise seeds give `['english_channel', 'hangzhou']`. Full orientation plus acyclicity is
exactly "every node drains to a sink" on a connected map. The claim scopes itself to three seeds and
does not generalise, which is the honest form.

### Y060 — per good on the same field: 29/29 acyclic, 0 fallbacks fired, and 90.2% of ordered node pairs (5,703 of 6,320) connected by at least one good's directed path
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; independently recomputed the acyclicity and fallback counts.
**Evidence:** `measure6.out` lines 22–23, 26–27: `acyclic goods 29`, `fallbacks fired across goods
0`, `ordered pairs connected 5703 of 6320`, `90.2`. *independent* re-derivation of the first two
agrees. 80 × 79 = 6,320 ✓.

### Y061 — agreement with the per-good graphs is 53.5% of edge-goods, 52.1% value-weighted
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; recomputed both figures in an independent harness.
**Evidence:** `measure6.out` lines 24–25: 53.5 and 52.1. *independent* — 53.5% edge-goods and 52.1%
value-weighted, same values.

### Y062 — the superseded marking-order aggregate scored higher on that measure, and no figure for it is maintained here
**Status:** CONFIRMED (derivation, with the direction measured)
**Method:** Built `Φ_ord = Σ_g V_g · order_g` on the v6.0 field, oriented it by descending `Φ_ord`,
and scored it against the same per-good graphs; grepped the spec for any `Φ_ord` percentage.
**Evidence:** *independent* — `Φ_ord` scores **60.5%** edge-goods and **59.0%** value-weighted against
`Φ_w`'s 53.5% / 52.1%, so "scored higher" is true on the current field. `Φ_ord` is fully oriented
(159/159) and acyclic. The spec carries no percentage for it: zero occurrences of `60.3`, `62.7` or
any `Φ_ord`-attached figure, and `verify6.py`'s `absent` check for "`Φ_ord`'s **60.3%" passes.

### Y063 — α_Φ = 1.5 is a stipulated design constant exactly as P₀ = 2.0 is — superlinear and round — and the document offers no derivation
**Status:** CONFIRMED
**Method:** Read §1.6 and §2.3 for consistency, and searched for any surviving derivation.
**Evidence:** §1.6: "**`α_Φ = 1.5` is a stipulated design constant, exactly as `P₀ = 2.0` is** … It
is **not** derived, and the document no longer offers a derivation". §2.3: "the aggregate-graph
exponent `α_Φ = 1.5` (a **stipulated** constant like `P₀`: superlinear, round, and chosen rather than
derived) … **Every derivation previously offered for it is withdrawn.**" The two sections agree, no
third passage offers a derivation, and 1.5 > 1 makes it superlinear as claimed. Internally consistent.

### Y064 — scanned over [1, 8] rather than [1, 3] the widest sink-count band is 1.70 wide ([3.51, 5.21], {doab, genua, hangzhou}) and 1.5's is not the widest by any margin
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`, which scans α_Φ = 1.00…8.00 at 0.01 and reports the widest band.
**Evidence:** `measure6.out` line 33: `widest band on [1,8]  ('doab+genua+hangzhou', 3.51, 5.21, 1.7)`.
Against 1.5's band width of 0.25 (line 32), 1.70 is 6.8× wider, so "not the widest by any margin" is
correct.

### Y065 — across α_Φ = 1.00…8.00 at 0.01 the sink set is a step function, and 1.5 sits in the band [1.38, 1.63], width 0.25, which gives {english_channel, hangzhou}
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` line 32:
`band containing alpha=1.5  ('english_channel+hangzhou', 1.38, 1.63, 0.25)`. The scan builds bands by
detecting changes in the sink set across 701 samples, which is what "step function" means
operationally.

### Y066 — sampled at the six values v2 used, the count is non-monotone: 6 → 2 → 1 → 2 → 3 → 1
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` line 34: `sink count at alpha 1,1.5,2,3,4,8  [6, 2, 1, 2, 3, 1]`. The
sequence falls, falls, rises, rises, falls — non-monotone as claimed.

### Y067 — a written warning against re-deriving 1.5 from the resemblance between the two-end 1444 map and vanilla's three authored ends
**Status:** CONFIRMED
**Method:** Read §1.6's warning paragraph and checked it against §2.3 and §3.9.
**Evidence:** §1.6 carries the italic paragraph "*A warning for anyone revising this, because the
mistake is available and has been made twice … Do not. That is the calibration §2.3 withdrew, and
§3.9's adoption argument does not rest on it.*" §2.3 does withdraw it (Y094) and §3.9's adoption
bullet argues from one operator / one guarantee set / ends where the wealth is, not from the count
(Y125/Y126). The warning is present and its two cross-references hold.

### Y068 — Europe becomes the centre of trade as it develops: the Channel's basin grows, Asia's pole fades, and past a broad range of European growth Asia holds no end at all
**Status:** PARTIAL
**Method:** Ran `europe.py`'s province-scaling scan (0% to +60% in 1% steps) and `measure6.py`'s
×2.00 row.
**Evidence:** *independent* — the sink set by scaling factor: ×1.00 `{english_channel, hangzhou}`;
×1.02 adds `wien`; ×1.09 adds `sevilla`; ×1.11–×1.34 various with `gulf_of_siam`/`hangzhou`/`doab`
present; ×1.36 `{english_channel, gulf_of_siam, hangzhou, rheinland}`; ×1.44
`{english_channel, hangzhou, rheinland}`; **×1.55 `{english_channel, rheinland}` — Asia holds none**,
and it holds none through ×1.60 (the scan's end) and at ×2.00. So the "Asia holds no end past a broad
range" half is confirmed from about ×1.55. The "Channel's basin grows" half is contradicted by the
claim's own table: at ×2.00 the sole sink is **`genua`** and `english_channel` is not a sink at all.
**Should say:** "as European development compounds a European node holds the map's end and Asia's
pole fades — the Channel through about ×1.5, `genua` beyond it." The directional statement about the
Channel specifically does not survive its own table.

### Y069 — the mechanism carries it: wealth is linear in development, so developing a region moves its c_w share directly and Φ_w's ends follow the wealth
**Status:** CONFIRMED (derivation)
**Method:** Checked linearity in the formula and verified it numerically.
**Evidence:** `wealth(p) = TAX_COEFF·base_tax + GP_COEFF·base_production·(1+gmod)·price` is linear and
homogeneous in `(base_tax, base_production)` — `gmod` depends on devastation only. *independent* —
scaling `base_tax` and `base_production` of the 824 European provinces by k and recomputing wealth
agrees with scaling their wealth by k to within 3.55e-15 at k = 1.02 and 1.56 and exactly at k = 2.00.
So a development change moves `c_w` through `wealth^α_Φ` with no other channel, and `Φ_w` reads only
`c_w`.

### Y070 — observed on the 1444 field at α_Φ = 1.5, scaling European development only (europe.py, 824 counted European provinces): ×1.00 → {english_channel, hangzhou}; ×1.02 → plus wien; ×1.56 → {english_channel, rheinland} with Asia holding none; ×2.00 → genua alone
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py` (which recomputes all three scaled rows) and `europe.py`.
**Evidence:** `measure6.out` lines 35–38: `European counted provinces 824`;
`Europe development x1.02 sinks ['english_channel', 'hangzhou', 'wien']`;
`x1.56 ['english_channel', 'rheinland']`; `x2.00 ['genua']`. `europe.py` independently reports
"Europe: 824 owned provinces in 25 nodes" and the same transitions. Every row reproduces exactly.

### Y071 — those rows are properties of this snapshot, not constants of the model
**Status:** CONFIRMED
**Method:** Checked the scoping against the evidence for Y068 and Y079.
**Evidence:** The scan is strongly non-monotone in the count (2 → 3 → 4 → 5 → 4 → 3 → 5 → 4 → 3 → 2
over ×1.00–×1.60), and the same scaling applied to nodes rather than provinces gives different
thresholds (Y079). A statement that these are snapshot properties is not merely defensible but
required by the data.

### Y072 — under the v6.0 wealth model scaling development and scaling wealth are the same operation — maximum difference 0.0 across the European set
**Status:** CONFIRMED (derivation and measurement), with a defect in the script's check
**Method:** Proved it from the formula; recomputed it properly; read the line in `measure6.py` that
claims to measure it.
**Evidence:** The proposition is true — wealth is homogeneous of degree 1 in `(base_tax,
base_production)`, so `wealth(k·dev) = k·wealth(dev)` exactly. *independent* — recomputing wealth from
scaled `base_tax`/`base_production` versus scaling wealth directly gives max |difference| 3.55e-15 at
k = 1.02 and 1.56, and exactly 0 at k = 2.00; "0.0" is right to double precision. **But
`measure6.py`'s own check is a tautology:** `a1 = W.copy(); a1[eur] *= 1.56` compared against
`devscale(eur, 1.56)`, which is `w = W.copy(); w[idx] *= k` — the same expression on both sides. It
cannot fail and it never touches development. The claim survives; its evidence does not.

### Y073 — the 1444 Genoa→Asian-sink route is the Silk Road: genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`; recomputed the BFS path independently.
**Evidence:** `measure6.out` line 49 gives exactly that eleven-node chain, and an independent BFS on
the baseline orientation reproduces it node for node.

### Y074 — from the north the route is the Volga and from the Channel the Hansa and the Danube — stated without node chains
**Status:** PARTIAL (measurement)
**Method:** Computed the directed out-degree of every node in the baseline orientation, then BFS'd
from `north_sea` and from `english_channel` toward the sinks.
**Evidence:** *independent* — the Volga half holds:
`north_sea → white_sea → novgorod → kazan → astrakhan → persia → lahore → lhasa → ganges_delta →
burma → gulf_of_siam → canton → hangzhou`. The Channel half does not. `english_channel` has
**out-degree 0** and in-degree 5 — it is one of the two sinks — so no route leaves the Channel at all
and `route("english_channel", "hangzhou")` returns nothing. The Hansa-and-Danube chain exists, from
`lubeck`: `lubeck → saxony → wien → venice → ragusa → constantinople → aleppo → …`. This is v5.0's
sentence surviving a change of field: under v5.0's one-sink map the Channel was a transit node.
`europe.py` — the script §1.6 cites here — **crashes** on this: `" -> ".join(path(src, s[0]))` raises
`TypeError: can only join an iterable` because `path` returns `None` for `english_channel`.
**Should say:** "From the north it is the Volga; the Hansa and the Danube feed the Channel from
`lubeck`, the Channel itself being an end node on this field."

### Y075 — no Europe→sink route passes the Cape of Good Hope, checked from genua, north_sea and english_channel
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` lines 46–48: all three checks return `False`. The scoping to three named
origins is exactly what was checked, and the claim asserts no more.

### Y076 — the Cape is a live conduit: in-degree 1, out-degree 3, with 132 ordered node pairs whose path runs through it
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`.
**Evidence:** `measure6.out` lines 43–45: `cape in-degree 1`, `cape out-degree 3`,
`ordered pairs routed through the cape 132`. The count is built as |{(a,b) : cape reachable from a,
b reachable from cape, b reachable from a}|, which is the stated quantity.

### Y077 — v5.0's "nothing routes through the Cape" is false as a universal and was only ever checked on the Europe→sink routes
**Status:** CONFIRMED
**Method:** Read v5.0's sentence in context; compared with Y076.
**Evidence:** `v5-owner-agnostic/per-good-trade-spec.md` line 426: "… `constantinople → aleppo → …`.
Nothing routes through the Cape, which is what a 1444 map should say." The surrounding paragraph
enumerates only the Europe-origin routes, so the check behind it was that narrow, and Y076's 132
routed pairs falsify the universal.

### Y078 — in the per-good graphs the Cape also carries Asian spices to Europe; Φ_w models power, not cargo
**Status:** CONFIRMED (measurement)
**Method:** Built the per-good spices graph on the v6.0 field and BFS'd `malacca → genua`; repeated
for all 29 goods.
**Evidence:** *independent* — spices route
`malacca → cape_of_good_hope → zanzibar → gulf_of_aden → alexandria → genua`, with the Cape's spices
in-arc from `malacca` and out-arcs to `zanzibar`, `ivory_coast`, `comorin_cape`. Seven of the 29 goods
route `malacca → genua` through the Cape. So a commodity graph uses the corridor the power graph does
not, which is the claim's point.

### Y079 — scaling the 22 European nodes rather than European provinces makes genua the sole sink from about ×1.65, and the 18-node western/central subset needs about ×2.15
**Status:** CONFIRMED (measurement)
**Method:** Scaled the wealth of every province in the 22 listed nodes (and separately in the
18-node subset) and swept the factor at 0.01 resolution for the first factor at which `genua` is the
sole sink, then confirmed it stays sole through ×4.00 at 0.05 resolution.
**Evidence:** *independent* — 22-node: sole `genua` first at **×1.63** and at every 0.05 step from
×1.65 to ×4.00. 18-node: sole `genua` first at **×2.14** and at every 0.05 step from ×2.15 to ×4.00.
"About ×1.65" and "about ×2.15" are both right, and the claim's hedge ("from about") is warranted —
the approach is not monotone, e.g. the 18-node set gives four sinks at ×1.60 after three at ×1.55.

### Y080 — somewhere inside roughly ×2.9–×3.5 the Cape reverses — Atlantic→Cape→Indian-Ocean becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast — bounded above as well as below, so a window and not a threshold
**Status:** CONFIRMED (measurement)
**Method:** Swept the 22-node scaling from ×1.00 to ×5.00 at 0.05 and recorded the Cape's in- and
out-neighbour sets at every change.
**Evidence:** *independent* — at ×1.00 the Cape is `in = {ivory_coast}`,
`out = {comorin_cape, malacca, zanzibar}` (Atlantic → Cape → Indian Ocean). From **×2.90** it is
`in = {comorin_cape, malacca, zanzibar}`, `out = {ivory_coast}` — the exact reversal described. At
**×3.50** it changes again to `in = {malacca}`, `out = {comorin_cape, ivory_coast, zanzibar}`, so the
fully-reversed configuration holds on [2.90, 3.45] at this resolution and is bounded above. "Roughly
×2.9–×3.5", "a window and not a threshold" and "its edges move with the field" are all supported.

### Y081 — dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate boosts are expected behaviour rather than noise
**Status:** CONFIRMED (measurement)
**Method:** Multiplied the wealth of the richest counted province of `hangzhou` (pid 1821) and of
`genua` (pid 101) by 2, 5, 10, 20, 30, 50 and recorded the sink set.
**Evidence:** *independent* — `hangzhou`'s top province: `{hangzhou}` at ×2, ×5, ×20, ×30, ×50, with
a transient `{genua, gulf_of_siam, hangzhou}` at ×10. `genua`'s top province:
`{english_channel, hangzhou}` at ×2 and ×5, `{doab, genua, gulf_of_siam, hangzhou}` at ×10,
`{doab, genua, hangzhou}` at ×20, `{genua}` at ×30 and ×50. Concentration on the boosted node at high
factors, extra sinks at intermediate ones — the claim's two halves both hold, and the transient split
is reproducible rather than seed-dependent.

---

# §1.10 — Direction-dependent systems

### Y082 — ⚑ three shipped defines rate-limit the mechanics carrying these thresholds: TRADING_POLICY_COOLDOWN_MONTHS = 12 (both banded policies), TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30 and TRADE_COMPANY_COOLDOWN = 60
**Status:** PARTIAL
**Method:** Read all three defines in `common/defines.lua` with their comments; checked
`common/defines/` for overrides; enumerated the top-level policies in
`common/trading_policies/00_trading_policies.txt`.
**Evidence:** The values are exact. `defines.lua` line 1045
`TRADING_POLICY_COOLDOWN_MONTHS = 12, -- Cooldown until you can change Trading Policy after
selecting.`; line 1212 `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30`; line 1214
`TRADE_COMPANY_COOLDOWN = 60`. No override in any of the five files in `common/defines/`. But the
scoping is wrong: the policy file's nine top-level entries are `maximize_profit`,
`maximize_profit_upgraded`, `hostile_trading`, `hostile_trading_upgraded`, `improve_inland_routes`,
`improve_inland_routes_upgraded`, `establish_communities`, `establish_communities_upgraded` and
**`propagate_religion`** — and the define's own comment scopes it to changing *Trading Policy*, i.e.
to all nine, not to "both banded policies". Propagate Religion is a trading policy, and §1.10's own
flicker-risk set (Y083) leaves it exposed. Two further limits on strength: the cooldown gates
*re-selection*, so a `can_maintain` failure still drops the effect immediately; and nothing in the
files ties `TRADE_COMPANY_COOLDOWN` or `TRADE_COMPANY_DAYS_TO_SWAP_LEADER` to
`TRADE_COMPANY_STRONG_LIMIT`/`TRADE_COMPANY_CONTROL_LIMIT` — that link is an inference from names.
**Should say:** "`TRADING_POLICY_COOLDOWN_MONTHS = 12` (every trading policy, the two banded ones and
Propagate Religion included)", and mark the trade-company attribution as inferred from the define
names.

### Y083 — banding absorbs very little chatter, cooldowns damp three mechanics, what is left exposed is everything without a cooldown, and the flicker-risk set stays "every country at a single-valued limit, plus flagless countries at Propagate Religion's 50/50 or 35/35"
**Status:** PARTIAL (derivation)
**Method:** Cross-read §1.10's threshold table against the policy file and against Y082's defines.
**Evidence:** "Banding absorbs very little chatter" is supported — of the seven listed thresholds only
Improve Inland Routes is banded (50 establish / 40 maintain) and Propagate Religion's flag ladder is
banded on the nine `N_trade_power_for_propogate_religion` rungs, which the file confirms
(`share = 5 … 45` in `can_select` against lower `can_maintain` shares). The internal inconsistency is
in the flicker-risk set: Propagate Religion is a trading policy in the same file as the two banded
policies, so the 12-month cooldown the claim credits with damping applies to it too, yet the claim
keeps flagless countries at its 50/50 and 35/35 in the exposed set.
**Should say:** either move Propagate Religion into the damped group, or state explicitly that the
cooldown gates re-selection only and therefore damps *re-establishment* rather than loss — in which
case the same qualification applies to the two banded policies and the claim's asymmetry disappears.

### Y084 — measured on the 1444 start: the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.9% over the flag's 26 inland nodes, whose totals run 106.4 at xian to 532.0 at champagne
**Status:** PARTIAL (measurement)
**Method:** Parsed the save's `trade={ node={ … } }` blocks for `definitions` and `total`; took the 26
nodes flagged `inland=yes` in `common/tradenodes/00_tradenodes.txt`; computed 50/total for each.
**Evidence:** *independent* — 26 flagged inland nodes, all present in the save with a `total`. Range
**9.40%** (`champagne`, total 531.980) to **47.01%** (`xian`, total 106.366) — both endpoints and both
node names exactly as quoted. The median of 26 values is the mean of the 13th and 14th order
statistics, `samarkand` 21.26% and `yumen` 21.88%, i.e. **21.57% → 21.6%**. 21.9% is the 14th value
alone.
**Should say:** "median **21.6%**" (or name 21.9% as the upper of the two middle values, which it is).

### Y085 — as a share of the node's total after the grant lands the same figures read 8.6%–32.0%, median 17.9%; v5.0 quoted those under the first description, which cannot be right since 8.6% of 532.0 is 45.8
**Status:** PARTIAL
**Method:** Recomputed 50/(total+50) over the same 26 nodes; read v5.0's sentence.
**Evidence:** *independent* — range **8.59%** (`champagne`) to **31.98%** (`xian`), i.e. 8.6%–32.0% as
quoted. Median is the mean of `samarkand` 17.53% and `yumen` 17.95% = **17.74% → 17.7%**, not 17.9%
(17.95% is again the 14th value alone). The critique of v5.0 is exact:
`v5-owner-agnostic/per-good-trade-spec.md` line 553 reads "the cap of 50 is **8.6% to 32.0% of an
inland node's total trade power** (median 17.9% over the **flag's** 26 inland nodes …)" — the
after-grant numbers presented as shares of the total — and 0.086 × 531.98 = 45.75, not 50.
**Should say:** "median **17.7%**".

### Y086 — on §2.2's derived 25-node inland basis only the median moves, to 21.3%
**Status:** CONFIRMED (measurement)
**Method:** Dropped `siberia` (the one node where the flag and the derivation disagree) and
recomputed.
**Evidence:** *independent* — over 25 nodes the range is unchanged at 9.40%–47.01% (`siberia`'s
39.28% is interior), and the median, now the 13th of 25 order statistics, is `samarkand`'s **21.26% →
21.3%**. Exactly as claimed, including "only the median moves".

---
# §2.2 — Solver

### Y087 — solver item 4 computes TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price, with no autonomy, efficiency, ideas or owner terms
**Status:** CONFIRMED
**Method:** Compared §2.2 item 4 with §1.3's formula block and with `solver.py`.
**Evidence:** The three statements agree term for term. `province_table()` produces
`tax = TAX_COEFF * base_tax * (1 + tmod)` and `prod_income = max(0, GOODS_PRODUCED_FACTOR *
base_production * (1 + gmod)) * price`, and `wealth` is their sum everywhere it is used. No autonomy,
efficiency, idea or owner term appears in the file.

### Y088 — the only modifiers the solver reads are the four describing the province's own condition, and at 1444 only devastation is live, on eleven provinces; GP_COEFF is read from 00_static_modifiers.txt rather than hardcoded
**Status:** CONFIRMED
**Method:** Read `solver.py` lines 56–116; checked the save for any live `occupied`, `under_siege` or
`prosperity` state at 1444.
**Evidence:** `STATE_GOODS_MOD = {"devastation": -2.0, "prosperity": 0.25, "occupied": -0.5,
"under_siege": -0.25}` and `STATE_TAX_MOD = {"occupied": -0.5}` are the only modifier tables in the
file. In `province_table()` only `devastation` is applied (`gmod = STATE_GOODS_MOD["devastation"] *
dev`, `tmod = 0.0`), on the eleven provinces of `ON_STARTUP_DEVASTATION`. The save carries no
`prosperity` field on any province, `controller == owner` on the counted set at the start, and no
siege. `GOODS_PRODUCED_FACTOR = _read_gp_coeff()` parses the static-modifier file and raises if the
block or the key is missing.

### Y089 — world wealth is 10,594.70 annual ducats over 2,472 counted provinces
**Status:** CONFIRMED (measurement of the model's own field)
**Method:** Re-ran `measure6.py`; independently recomputed from the save's `base_tax`,
`base_production` and `devastation`, both with the model's good assignment and with the engine's.
**Evidence:** `measure6.out` lines 3–4: `counted provinces 2472`, `world wealth 10594.7`. Reproduced.
*independent* — recomputing from the save with the model's rule (history goods, `unknown` at price 0)
gives 10,594.70; with the engine's own assignments for the twenty `unknown` provinces it gives
10,607.40. The quoted figure is the model's field exactly; the 12.70 gap against the engine's state is
graded at Y046.

### Y090 — measured on the reference implementation: of order 0.1 s for all 29 goods and single-digit milliseconds per good on average — repeated runs span roughly 0.09–0.27 s and 3–7 ms per good, with individual goods reaching about 20 ms
**Status:** PARTIAL (measurement)
**Method:** Timed twelve consecutive passes over the 29 per-good DRAIN solves using
`drain.run_drain` on the shared prebuilt LP structures, after a warm-up call; recorded total, mean and
max per run. Repeated with a self-contained implementation that rebuilds the LP per call.
**Evidence:** *independent*, reference implementation — totals 0.185, 0.194, 0.180, 0.177, 0.181,
0.181, 0.119, 0.108, 0.109, 0.275, 0.266, 0.281 s (range **0.108–0.281 s**); per-good means 6.4, 6.7,
6.2, 6.1, 6.2, 6.2, 4.1, 3.7, 3.8, 9.5, 9.2, 9.7 ms (range **3.7–9.7 ms**); largest single good 24.4
ms. "Of order 0.1 s", "single-digit milliseconds on average", "roughly 0.09–0.27 s" and "about 20 ms"
all hold. **"3–7 ms per good" does not** — three of twelve runs averaged above 9 ms. The claim's own
reasoning ("a two-significant-figure range is a statement about a machine and a scheduler") applies to
its own quoted band.
**Should say:** "roughly 0.1–0.3 s for the full set and 4–10 ms per good as an average, with
individual goods reaching about 25 ms" — or drop the two-figure bands entirely, as the sentence
already says it means to.

### Y091 — v5.0 quoted "0.17–0.21 s"; twelve fresh runs put only one inside that interval
**Status:** PARTIAL (measurement)
**Method:** Grepped v5.0's figure; counted the twelve totals from Y090 falling inside [0.17, 0.21].
**Evidence:** `v5-owner-agnostic/per-good-trade-spec.md` line 644 reads "**0.17–0.21 s for all 29
goods, a mean of 5.7–7.3 ms per good across runs**" — the quotation is exact. *independent* — of the
twelve totals, **6** fall inside [0.17, 0.21] (0.185, 0.194, 0.180, 0.177, 0.181, 0.181), not one. The
point the claim is making — that the interval is not a stable characterisation — survives: six runs
are outside it, spanning 0.108 to 0.281.
**Should say:** a count from a stated run, or better, the direction only: "half of twelve fresh runs
fell outside that interval."

---

# §2.2a — What map this is for

### Y092 — where Phase 0 acts, free-edge determinism weakens asymmetrically: the determinism half is unaffected, the index-independence half is not, because the key reads the post-fold balance β
**Status:** CONFIRMED (derivation)
**Method:** Checked the argument against `drain.py`'s `phase0` and `sweep_priority`.
**Evidence:** `sweep_priority`'s key is `(DEF[v], beta[v], pid[v])` with `beta` the vector `phase0`
returns after `beta[u] += beta[v]` for each peeled pendant. Determinism follows from the key being a
total order on a fixed candidate set regardless of what `beta` contains, so that half is untouched.
Index-independence requires no exact ties, and folding can manufacture them: `beta[u]` becomes a sum,
and sums of distinct reals collide where the reals themselves do not. The 1444 measurement (zero exact
ties) is taken on a map where Phase 0 removes nothing, so it says nothing about the folded case. The
asymmetry is correctly located.

---

# §2.3 — Constants

### Y093 — v3.0 through v5.0 said neither wealth coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block holding one of them
**Status:** CONFIRMED
**Method:** Read the corresponding paragraph in all three prior specs; checked what their sweep read.
**Evidence:** v3.0 line 544, v4.0 line 616 and v5.0 line 716 are byte-identical: "**Engine constants
that are not defines.** The two wealth coefficients of §1.3 are hardcoded in the binary —
`defines.lua` and `common/defines/` were searched and contain neither." And their sweep did read
`00_static_modifiers.txt`: v5.0's §1.3 classification table lists "`devastation` −2, `occupied` −0.5
and −0.5, `under_siege` −0.25, `prosperity` +0.25 (static modifiers)", all four of which live in that
file — 200 lines below `provincial_production_size = { trade_goods_size = 0.2 … }`. The sweep opened
the file and did not see the block.

### Y094 — every derivation previously offered for α_Φ is withdrawn: v2.1–v4.0's two-sink calibration fits a constant to one date, and v5.0's widest-band argument depended on where the α scan was truncated
**Status:** CONFIRMED
**Method:** Read the prior derivations; re-ran the band scan over both ranges.
**Evidence:** v2.1's derivation is at `v2-drain/per-good-trade-spec.md` line 372 ("calibrated so the
1444 start yields the two-sink …") — a fit to one date. v5.0's is the widest-band table
(`v5-owner-agnostic/per-good-trade-spec.md` §1.6, "**[1.43, 1.93]** … **0.50** — the widest band on
this field"). *independent* via `measure6.py`: over [1, 8] the widest band is 1.70 wide at
[3.51, 5.21] and 1.5's is 0.25, so the "widest" property is an artifact of stopping the scan at 3.
Both withdrawals are justified, and §2.3 offers nothing in their place, which is what the claim says.

---

# §2.4 — The tradenodes file

### Y095 — measured on 1444: relabelling the nodes and running end-to-end changed the orientation on 580 of 580 runs (29 goods × 20 relabellings), always by returning a different optimal vertex and never by a sweep tiebreak, with a mean of 22.1 of 159 edges moving and the objective identical to 8.9e-16
**Status:** CONFIRMED (measurement)
**Method:** Built a self-contained DRAIN taking the node labelling and the arc presentation order as
parameters, permuted the 80 node labels, rebuilt `EDGES_UND` and the LP equality matrix under the
permutation, solved, and mapped the orientation and the flow support back through the inverse
permutation before comparing. 29 goods × 20 permutations.
**Evidence:** *independent* — orientation changed on **580 of 580**; the LP's flow support changed on
**580 of 580**, so every change is a different optimal vertex, and since the `(DEF, β)` key has zero
exact collisions anywhere (Y102) no sweep tiebreak is available to cause one. Mean **21.62** of 159
edges moved (min 2, max 51); max |objective difference| **2.66e-15**. The mean and the objective
residual are properties of the permutation sample — 21.62 against the claim's 22.1 and 2.66e-15
against 8.9e-16 are both within sampling. *Provenance note:* the spec attributes the sweep to
`../v5-owner-agnostic/validation-v5.md`, which contains no 580/580 result — its relabelling work is a
7,146-instance random sweep, a 24-relabelling 4-node example and a 120-relabelling pendant case. The
measurement is right; the citation is not.

### Y096 — permuting only the arc presentation order with node labels held fixed changes the optimal support on 10 of 10 goods tested, with objective gaps ≤ 1.8e-15
**Status:** CONFIRMED (measurement)
**Method:** Held node labels fixed, shuffled the 159-edge presentation order five times per good,
rebuilt the LP, and compared the flow support. Ten goods.
**Evidence:** *independent* — the support changed on **10 of 10** goods (chinaware, cloth, cloves,
cocoa, coffee, copper, cotton, dyes, fish, fur). Max objective gap **2.22e-15**, against the claimed
≤ 1.8e-15 — same order, sample-dependent, and the conclusion (arc order alone selects the vertex) is
unaffected.

### Y097 — twenty-two flips is the same magnitude as the razed-China perturbation §2.8 treats as a major world event
**Status:** CONFIRMED (derivation)
**Method:** Compared the two measured counts.
**Evidence:** *independent* — relabelling moves a mean of 21.6 edges (claim: 22.1); zeroing
`hangzhou`-node development moves **23** (Y106). 21.6 ≈ 23 out of 159, so "the same magnitude" is
exact rather than rhetorical.

### Y098 — the canonical order must be the order Phase 2's LP input is built in, and everything §1.6 and §2.8 report about stability is measured at fixed node order
**Status:** CONFIRMED (derivation)
**Method:** Checked against Y095 and Y096 and against how `flowop.py` builds the program.
**Evidence:** `flowop.py` builds `ARCS` from `EDGES_UND` (which is `sorted(set(tuple(sorted(e))))`, so
a function of the node indices) and `AEQ` from the node indices directly, at import time. Both the arc
order and the row order are therefore fixed by the node labelling, and Y095/Y096 show each of them
independently selects the vertex. Every figure in §1.6 and §2.8 was produced at the one labelling
`nodes.json` fixes, so "measured at fixed node order" is a statement of fact about the toolchain, and
"re-order the same world and the map moves" is Y095.

### Y099 — the 580/580 result is HiGHS-specific in its detail but not in kind: any simplex returns a vertex of a degenerate optimal face
**Status:** CONFIRMED (derivation)
**Method:** Checked the argument.
**Evidence:** The program is `min Σf` subject to node balance with `f ≥ 0` and unit costs; on this map
many distinct spanning-tree bases attain the optimum, which the measured objective agreement to
~1e-15 across 580 differing supports demonstrates directly. A simplex method terminates at a basic
feasible solution, i.e. a vertex, and which vertex depends on the pivoting sequence, which depends on
the presentation order. Nothing in the argument is specific to HiGHS. The claim's scoping — detail
solver-specific, kind not — is the correct one.

### Y100 — making the orientation independent of presentation order would need a tie-breaking objective, which is a design change and is not adopted here
**Status:** CONFIRMED (derivation)
**Method:** Checked the argument and the spec's own record of what is adopted.
**Evidence:** Degeneracy is a property of the objective, not of the solver, so only changing the
objective (a lexicographic secondary cost, or a strictly convex perturbation) can make the optimum
unique. Both named remedies would do so. §2.4 states neither is adopted, §2.3 lists no such term
among the constants, and `flowop.py`'s `mincost_flow` passes `c = np.ones(A)` with no secondary
objective — so the "not adopted" half is true of the implementation as well as of the prose.

### Y101 — the priority key ties in more places than §1.1 documents: besides the free-edge sweep it decides Phase 1's within-cluster argmin, the stall promotion's identical form, and the top-k cut when two clusters carry equal mass
**Status:** CONFIRMED (derivation)
**Method:** Located every tiebreak in `drain.py`.
**Evidence:** All three sites are there. Phase 1's within-cluster argmin: line 99,
`S.add(min(comps[j], key=lambda v: (beta[v], v)))`. The stall promotion, identical form: line 242,
`s_star = min(terminals, key=lambda v: (beta[v], v))`. The top-k cut: line 96,
`top = sorted(range(len(comps)), key=lambda j: -M[j])[:k]` — Python's sort is stable, so equal cluster
masses are cut by cluster index, which is derived from node index. §1.1's text documents only the
free-edge sweep's tiebreak, so "more places than §1.1 documents" is right.

### Y102 — none of those tie sites fires on 1444 — zero exact (DEF, β) ties on free edges across 29/29 goods, zero within-cluster β ties, zero tied cluster masses
**Status:** CONFIRMED (measurement)
**Method:** For all 29 live goods: built the Phase-0 core and β, computed `DEF` on the flow-arc
subgraph, and counted exact `(DEF, β)` collisions over the whole core (a superset of the free-edge
endpoints); separately rebuilt Phase 1's demander clusters and counted exact β collisions within each
cluster and exact collisions among cluster masses.
**Evidence:** *independent* — **0** exact `(DEF, β)` collisions summed over all 29 cores, **0**
within-cluster β ties, **0** tied cluster masses. All three at zero, as claimed.

### Y103 — end flags: 1444 has two end nodes, english_channel and hangzhou, against vanilla's three
**Status:** CONFIRMED
**Method:** Parsed `common/tradenodes/00_tradenodes.txt` for `end = yes`; read the computed sink set.
**Evidence:** The shipped file declares 80 nodes and exactly **three** with `end = yes`: `genua`,
`venice`, `english_channel`. `measure6.out` line 9 gives the computed sink set as
`['english_channel', 'hangzhou']` — two. Both halves exact.

---

# §2.7 — Probes

### Y104 — § probe 15: §1.9's "every immediately upstream node" is consistent with the observation rather than confirmed by it — one observation on one node
**Status:** CONFIRMED (on the recorded evidence)
**Method:** Read the probe record in `../v2-drain/game-session.md`; checked what the observation can
and cannot support.
**Evidence:** The session records, verbatim, France's Sevilla breakdown: `Current Trade Power: 3.3 /
Transfers from traders downstream: +3.1 / And multiplied by 1.05 due to +5.10% Trade Power modifier in
this node`, with the note "Every point of France's power in Sevilla is propagated from downstream.
There is no base term, no merchant term, no provincial term." That falsifies the tooltip's "where it
already has power" qualifier at one node, and the corroborating Castile-in-Safi reading in the same
section is not a clean case (Castile holds provinces upstream). So the observation retires the
cautionary case and cannot establish "every immediately upstream node", which is exactly the
epistemic scoping the claim adopts. *This is an engine observation from a prior session; re-observing
it requires running the game, which this audit did not do.*

---

# §2.8 — Validation

### Y105 — most goods, 1444: sinks are 1 to 8 per good, and high-demand nodes are sinks at 16.8% in the top demand decile against 6.9% in the bottom
**Status:** CONFIRMED (measurement)
**Method:** For each of the 29 goods, ranked nodes by that good's `c`, took the top and bottom deciles
(8 nodes each), and counted how many were sinks for that good.
**Evidence:** *independent* — top decile 39 of 232 = **16.8%**; bottom decile 16 of 232 = **6.9%**.
Sinks per good 1 to 8 (Y016). Both figures exact.

### Y106 — razed China: zeroing hangzhou-node development moves the Φ_w sinks from {english_channel, hangzhou} to {doab, english_channel, gulf_of_siam}, with 23 of 159 edges flipping
**Status:** CONFIRMED (measurement)
**Method:** Set the wealth of every counted province in the `hangzhou` node to a floor of 1e-12,
re-ran `Φ_w`, and compared orientation and sink set with the baseline.
**Evidence:** *independent* — new sink set `['doab', 'english_channel', 'gulf_of_siam']`, **23** of
159 edges flipped. Both exact.

### Y107 — hangzhou, not beijing, is China's wealth pole under §1.3 — node wealth 226.7 against 143.0 — and it holds the richest single province the model counts
**Status:** CONFIRMED (measurement)
**Method:** Summed counted-province wealth per node; found the argmax over provinces.
**Evidence:** *independent* — `hangzhou` **226.7**, `beijing` **143.0**. The richest counted province
is pid **1821** at **27.00**, in the `hangzhou` node; the next four are 684 (21.60, hangzhou), 1816
(19.50, beijing), 685 (19.20, hangzhou), 507 (18.00, lahore). `measure6.out` line 7 agrees
(`richest single province pid 1821 27.00`). The qualifier "the model counts" is load-bearing and
present.

### Y108 — zeroing beijing also moves the map — 15 flips — because deleting a percent of world wealth renormalises c_w everywhere; the asymmetry is which node keeps its end
**Status:** CONFIRMED (measurement)
**Method:** As Y106, on the `beijing` node.
**Evidence:** *independent* — **15** of 159 edges flipped, and the sink set is unchanged at
`['english_channel', 'hangzhou']`. So `hangzhou` survives as a sink when `beijing` is zeroed and does
not when `hangzhou` is (Y106) — exactly the asymmetry described, and the map moves in both cases.

---
# §3.2 — Why a flow and a drainage sweep

### Y109 — what the contrast-ratio metric cannot see is sparsity: spices in 18 of 80 nodes, cloves in exactly one, so (c−s)/deg is dominated by where supply exists; on the contrast metric itself the demand side is the wider one
**Status:** CONFIRMED (derivation, with both counts measured)
**Method:** Counted producing nodes per good on the v6.0 field; re-ran `measure6.py` for the contrast
ranges.
**Evidence:** *independent* — spices are produced in **18 of 80** nodes, cloves in **1**, grain in 64.
`measure6.out` lines 28–31: supply contrast range (4, 97), goods with more than one producer 28,
single-producer goods `['cloves']`, demand contrast range (211, 15010) — so the demand side is the
wider one by two orders of magnitude, as claimed. The argument that a max/min ratio over *producing*
nodes cannot see how many nodes produce nothing is correct by construction: the ratio's domain is the
support of `s`, and sparsity is a statement about the complement of that support.

### Y110 — better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of placement
**Status:** CONFIRMED (measurement)
**Method:** This is a claim about the v1 Laplacian's sink placement (§3.2's subject), so it was
measured with `solve_phi` + `orient` on the v6.0 field: scaled the wealth of `genua`'s counted
provinces and bisected for the first factor at which `genua` becomes a spices sink under LAP.
**Evidence:** *independent* — the baseline LAP spices sink is `['saxony']`; `genua` joins the sink set
at **×1.721**. "Roughly ×1.7" is right, and it is a *co*-sink threshold, not a sole-sink one — at
×1.721 `saxony` is still a sink.

### Y111 — moving the spice sink to a Chinese node takes a multiple of that node's demand in the region of 3.6–4.9× — beijing 3.61×, hangzhou 4.12×, xian 4.60×, canton 4.77×
**Status:** CONFIRMED (measurement)
**Method:** As Y110, bisecting per node for the first factor at which that node becomes a spices sink
under LAP; and separately for the first factor at which it becomes the *sole* sink.
**Evidence:** *independent* — `beijing` **3.619×**, `hangzhou` **4.122×**, `xian` **4.603×**, `canton`
**4.772×**. All four match the quoted figures under truncation to two places (3.61, 4.12, 4.60, 4.77),
and all four lie inside "3.6–4.9×". For reference the sole-sink thresholds are far higher — 16.9×,
18.6×, 19.5× and 196× — which is why the claim's "moving the spice sink to" is the co-sink reading.

### Y112 — the multiple a node needs and the share of world demand it then buys do not line up end to end, because the share depends on where the node started, and other nodes in the region need more still
**Status:** CONFIRMED (derivation, with the measurement behind it)
**Method:** At each node's threshold factor, computed that node's share of world spice demand.
**Evidence:** *independent* — `beijing` at ×3.62 holds **9.5%** of world spice demand (baseline 1.5%);
`hangzhou` at ×4.12 holds **21.4%** (baseline 3.2%); `xian` at ×4.60 holds **12.3%** (baseline 1.4%);
`canton` at ×4.77 holds **17.6%** (baseline 2.0%). The orderings genuinely disagree: `hangzhou` needs a
smaller multiple than `xian` and ends with a much larger share, because its baseline is larger. That
is exactly the non-alignment claimed, and it is why v2's "1.7× where 4–5× is needed" compressed two
quantities into one comparison.

### Y113 — the node indexing is load-bearing wherever the key ties, which is not only the fallback branch, and none of those sites is why §2.4 requires a canonical node order
**Status:** CONFIRMED (derivation)
**Method:** Combined Y101 (the four tie sites) with Y095 and Y102.
**Evidence:** Y101 locates four tie sites in `drain.py`, of which the fallback branch is one. Y102
shows none fires on 1444. Y095 shows the orientation nonetheless moves on 580 of 580 relabellings with
the LP support changing every time. So the canonical-order requirement cannot come from any tie site,
and does come from Phase 2's degeneracy. Both halves hold.

---

# §3.4 — Why supply is pre-modifier

### Y114 — in v1, substituting production income broke the α = 1 identity, with orientation agreement collapsing to well under half the map — the 159/159 → 68/159 figures are no longer carried
**Status:** CONFIRMED
**Method:** Located the original measurement in `v1-laplacian/validation.md`; grepped the v6.0 spec
for the figures.
**Evidence:** `v1-laplacian/validation.md` line 4517: "`rel.residual with production-income supply:
1.512e+00` against `1.959e-15` with trade-value supply … Orientation agreement collapses from
**159/159 to 68/159**." 68/159 = 42.8%, which is "well under half the map". The v6.0 spec contains
zero occurrences of `68/159` or `159/159` in this context — the §3.4 sentence reads "measured as
orientation agreement collapsing to well under half the map". *This is a historical measurement on an
operator v2 deleted; it is not re-derivable on the v6.0 model, which has no α = 1 identity. The claim
is graded as a faithful restatement of what the v1 audit recorded, plus the verifiable fact that the
figures are no longer carried.*

---

# §3.5 — Why α is anchored absolutely

### Y115 — ⚑ change_price values are fractions of the good's base price, not ducats, settled by the shipped save tutorial/eu4_tutorial_chapter10.eu4: paper at current_price = 4.375 on a base of 3.5, gems at 5.000 on a base of 4.0
**Status:** CONFIRMED
**Method:** Opened `tutorial/eu4_tutorial_chapter10.eu4` (plain text, not a ZIP) and read its
`change_price={ … }` block; cross-checked the base prices in `common/prices/00_prices.txt`.
**Evidence:** The save's block contains
`paper={ current_price=4.375  change_price={ key="PAPER_IN_BUREAUCRACY" value=0.250
expiry_date=1821.1.2 } }` and
`gems={ current_price=5.000  change_price={ key="FACETING" value=0.250 expiry_date=1821.1.2 } }`.
Base prices are `paper` 3.50 and `gems` 4.00. Multiplicative: 3.5 × 1.25 = 4.375 ✓ and
4.0 × 1.25 = 5.000 ✓. Additive would give 3.75 and 4.25 ✗. The consequences hold too: a −0.25 event
takes a 2.5 good to 2.5 × 0.75 = 1.875, and *independent* census confirms grain's and wine's worst
negatives take both to exactly **0.625**.

### Y116 — the install carries 161 textual change_price blocks — 93 in events/, 14 in missions/, 1 in common/, 53 in history/ of which 13 are negative (all in HAB - Austria.txt) — and none in decisions/
**Status:** CONFIRMED
**Method:** Independent census: walked `events/`, `decisions/`, `missions/`, `common/` and `history/`,
stripped comments, counted `change_price\s*=\s*\{` textually, brace-matched each block and extracted
its `trade_goods`, `value` and `key`.
**Evidence:** *independent* — **161** total: events **93**, missions **14**, common **1**, history
**53**, decisions **0**. All 53 history blocks are in `history/countries/HAB - Austria.txt`, and **13**
of them are negative — and that file is the only history file containing any negative block. Every
number in the claim reproduces.

### Y117 — ⚑ ten of the 161 never execute: seven sit inside quoted effect_tooltip = "…" strings and three inside tooltip = { } display wrappers, so 151 are executable
**Status:** PARTIAL
**Method:** Two independent passes. (i) A quote-parity pass flagging blocks whose opening brace sits
inside an odd number of preceding double quotes. (ii) A forward block-ancestor scan (skipping quoted
strings) flagging blocks whose enclosing block chain contains `tooltip` or `effect_tooltip`. Then
resolved each flagged block's enclosing assignment by name, and read the scripted effect that consumes
the string ones.
**Evidence:** *independent* — 7 blocks sit inside quoted strings and 3 inside literal `tooltip = { }`
blocks, disjoint sets, so **10 non-executing and 151 executable** are both exact. The mechanism split
is not. Resolving the enclosing assignment for each of the seven gives **four** inside
`effect_tooltip = "…"` (`DOM_Britain_Missions.txt` ENGLISH_FUR_TRADE; `KoK_Persia_Missions.txt`
PERSIAN_SILK, PERSIAN_DYES, PERSIAN_CLOTH) and **three** inside `effect = "…"`
(`KoK_Byzantine_Missions.txt` BYZ_growing_demand; `KoK_Yemen_Missions.txt` YEM_coffee_price_boost;
`WOC_Italian_Missions.txt` ITA_wine_upgrade). Those three are arguments to
`country_event_with_effect_insight`, whose definition at
`common/scripted_effects/00_scripted_effects.txt` line 6588 substitutes `$effect$` **inside a
`tooltip = { }` block** — so they are display-only too, and the verdict "never execute" is right for
all seven. The three literal `tooltip = { }` ones are `flavorMAL.txt` (ivory 0.33, `flavor_mal.27`)
and two in `WOC_Hisn_Kayfa_Missions.txt` (grain 0.1, in an `if` and an `else`).
**Should say:** "seven sit inside quoted strings — four in `effect_tooltip = "…"` and three in
`effect = "…"` arguments to `country_event_with_effect_insight`, which wraps them in `tooltip = { }` —
and three inside literal `tooltip = { }` blocks."

### Y118 — six of the seven quoted blocks duplicate a block already counted in events/, and the seventh names a price key no event in the install ever sets
**Status:** CONFIRMED
**Method:** Searched `events/`, `missions/`, `decisions/`, `common/` and `history/` for each of the
seven keys.
**Evidence:** *independent* — `BYZ_growing_demand` also at `events/flavorBYZ.txt:1923`; `PERSIAN_SILK`
at `events/FlavorPER.txt:1465`; `PERSIAN_DYES` at `:1471`; `PERSIAN_CLOTH` at `:1477`;
`YEM_coffee_price_boost` at `events/flavorYEM.txt:91`; `ITA_wine_upgrade` at
`events/flavorITA.txt:450` — six. `ENGLISH_FUR_TRADE` appears exactly once in the whole install, at
`missions/DOM_Britain_Missions.txt:921`, inside the quoted `effect_tooltip` — so no event ever sets it.
Both halves exact.

### Y119 — all ten non-executing blocks are positive and every negative block in the install is executable, so the sublinear-reachability partition is identical under either census
**Status:** CONFIRMED
**Method:** Read the ten blocks' values; recomputed the partition over the executable set and over the
full textual set.
**Evidence:** *independent* — the seven quoted values are +0.25, +0.2, +0.25, +0.5, +0.35, +0.25,
+0.4; the three tooltip-wrapped are +0.33, +0.1, +0.1. All ten positive. The install holds 40 negative
blocks and none of them is in the non-executing set. Partition **13 below / 2 exactly on / 4 above /
11 no negative event**, identical either way; `measure6.out` line 54 agrees `(13, 2, 4, 11)`.

### Y120 — v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about which number was the executable one
**Status:** CONFIRMED
**Method:** Read the census sentence in v4.0 and v5.0.
**Evidence:** `v4-owner-agnostic/per-good-trade-spec.md` line 949: "All **154** `change_price` blocks
were parsed — 93 in `events/`, 7 in `missions/`, 1 in `common/` and 53 in `history/`" — 14 − 7 = 7
missions blocks missing, exactly the quoted seven. `v5-owner-agnostic/per-good-trade-spec.md`
(E31/§3.5): "All **161** … 14 in `missions/`". Neither is 151, which Y117 establishes as the executable
count. Both halves exact.

### Y121 — v5.0's claim that the scan was "guarded by a per-file count assertion" was false — no assertion existed anywhere in its toolchain — and verify6.py now carries the guard
**Status:** PARTIAL
**Method:** Grepped every `change_price` scanner in `v5-owner-agnostic/scripts/` for an assertion;
read `verify6.py` and `measure6.py`'s census code.
**Evidence:** The first half is confirmed. v5's four scanners — `w10.py`, `leftovers.py`,
`audit_delta2.py`, `validate_v5.py` — none carries a per-file count assertion: `w10.py` and
`audit_delta2.py` use bare `try: walk(...) except Exception: pass`, `leftovers.py` prints `PARSEFAIL`
without failing, and `validate_v5.py`'s only check is a **per-tree** raw census
(`chk("3.5", "change_price blocks, raw census", (sum(raws.values()), raws["events"], …), (161, 93, 14,
1, 53))`) — a soft check at tree granularity, not a per-file assertion, and in the audit harness rather
than the spec's toolchain. The second half fails. `verify6.py` has no per-file check either: it does
`shows(doc, "spec: price census", "**{}** textual `change_price` blocks", 161)` — the literal 161,
typed in, not `O["change_price textual blocks"]`. `measure6.py` does compute a per-tree textual count
(`rawc[tree] += len(re.findall(r"change_price\s*=\s*\{", body))`) but never asserts it against the
walker's `hits`, which is the comparison that would catch a silent parse failure.
**Should say:** "no assertion existed anywhere in its toolchain, and none exists here either — the
per-tree textual count is computed and printed, and nothing compares it to the walker's yield."

### Y122 — the mechanical reason a plain parse misses those blocks: pdx.py tokenises a quoted string as one opaque unit, so a change_price inside a tooltip string is invisible to the walker
**Status:** CONFIRMED
**Method:** Read `pdx.py`.
**Evidence:** Line 9: `TOK = re.compile(r'"[^"]*"|[{}=]|[^\s{}=]+')`. The first alternative matches a
whole double-quoted run, newlines included (a negated character class matches `\n`), so a multi-line
`effect_tooltip = "… change_price = { … } …"` becomes a single token. `parse()` then stores it as a
string value (`node.append((key, toks[pos].strip('"')))`), and both `measure6.py`'s and v5's walkers
recurse only into `pdx.Node` values. The block is therefore structurally invisible. Exactly as stated.

---

# §3.9 — Why Φ_w is the installed graph

### Y123 — rich non-sink nodes on the corrected field: genua, gulf_of_siam and sevilla rank 3rd, 2nd and 7th by node wealth at 296.0, 297.9 and 266.5 against english_channel's 316.6, which is a sink
**Status:** PARTIAL (measurement)
**Method:** Summed counted-province wealth per node and ranked all 80.
**Evidence:** *independent* — the four values are exact: `genua` **296.0**, `gulf_of_siam` **297.9**,
`sevilla` **266.5**, `english_channel` **316.6**, and `english_channel` is a sink. The ranks are not.
The top eight are english_channel 316.6 (1), **mexico 300.4 (2)**, gulf_of_siam 297.9 (3), genua 296.0
(4), malacca 295.2 (5), nippon 293.6 (6), sevilla 266.5 (7), rheinland 251.8 (8). So `genua` is 4th and
`gulf_of_siam` is 3rd; rank 2 belongs to `mexico`, which the claim does not mention and which is also a
rich non-sink node.
**Should say:** "`genua`, `gulf_of_siam` and `sevilla` rank 4th, 3rd and 7th … `mexico` at 300.4 is
2nd and is also a non-sink."

### Y124 — Φ_ord scores higher than Φ_w on self-coherence, but its ends are scheduling artifacts, a majority terminate no good at all, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates; no figure is maintained for it
**Status:** CONFIRMED (all four claims measured)
**Method:** Built `Φ_ord = Σ_g V_g · order_g` on the v6.0 field from the 29 per-good marking orders,
oriented it by descending `Φ_ord`, scored it against the same per-good graphs, enumerated its ends,
counted how many of them terminate no good, ranked nodes by value-weighted demand, and swept cloves-α
over 2…64 recomputing the end count.
**Evidence:** *independent* — self-coherence **60.5%** edge-goods / 59.0% value-weighted against
`Φ_w`'s 53.5% / 52.1%, so "scores higher" holds. `Φ_ord` has **15 ends** (amazonas_node, rio_grande,
james_bay, chengdu, philippines, australia, beijing, katsina, basra, kazan, laplata, ragusa, safi,
rheinland, white_sea) and **9 of the 15 terminate no good at all** — a majority. The top five nodes by
value-weighted demand are genua, english_channel, hangzhou, gulf_of_siam, malacca, and **none** is a
`Φ_ord` end. End count across cloves-α ∈ {2, 4, 8, 16, 32, 64}: 15, 15, 15, 14, 15, 15 — flat, so it
does not concentrate as demand concentrates. And the spec carries no figure for any of it.

### Y125 — v2.1–v4.0's "two vanilla-like ends at 1444" is not the adoption argument and should not be revived even though the 1444 field again gives two ends
**Status:** CONFIRMED
**Method:** Grepped the phrase in the three prior specs; read v6.0 §3.9's adoption bullet.
**Evidence:** `v2-drain` line 685, `v3-owner-agnostic` line 963 and `v4-owner-agnostic` line 1053 are
identical: "- `Φ_w`, adopted: two vanilla-like ends at 1444 that move with the world, from the same
operator". v6.0's bullet reads "**one operator, one set of guarantees, and ends that move with the
world**" and then explicitly disowns the old ground: "*v2.1 through v4.0 justified the adoption by
'two vanilla-like ends at 1444' … That is not the argument, and it should not be revived even though
the 1444 field again gives two ends.*" The disavowal is present, accurate about the prior text, and
consistent with §1.6's warning (Y067) and §2.3's withdrawal (Y094).

### Y126 — what the trade costs is self-coherence with the per-good graphs and what it buys is one operator, one set of guarantees, and ends that sit where the wealth is — stated without a points figure
**Status:** CONFIRMED
**Method:** Read §3.9's bullet and searched for any surviving points figure; checked whether the cost
and the benefit are both real.
**Evidence:** No figure appears in the bullet or anywhere in §3.9. The cost is real and measured
(Y124: 60.5% against 53.5%). The benefit is structural: `Φ_w` is the §1.1 operator on a different
`b`, so LP feasibility, acyclicity, determinism and scan-invariance transfer without a second proof,
and the cross-implementation check stays one combinatorial comparison (§2.2, §2.8). "Ends that sit
where the wealth is" is supported by Y056 (`c_w` ranks 2 and 3) and by Y068/Y070 (the ends move with
the field).

---

# §3.10 — Why the engine's economy is overwritten

### Y127 — the two income forms agree to a worst relative disagreement of 0 to 3.7e-16 — one to three units in the last place
**Status:** CONFIRMED (derivation exact; measurement reproduced to the same magnitude)
**Method:** The derivation was checked as algebra. The measurement was rebuilt independently: for each
of `sevilla`, `champagne`, `genua`, `malacca` and `gulf_of_siam`, took the node's real country power
table from the save, split it into collectors and transferrers, built a per-good
`collected_share(n,g)` from the per-good graphs, and evaluated
`Σ_g v_g·cs_g·ps_C` against `ps_C · Σ_g v_g·cs_g` in doubles.
**Evidence:** The identity is exact: `powershare_C(n)` carries no `g`, so it factors out of the sum,
and every term feeding a collector's power at a node is node-wide. *independent* — worst relative
disagreement per node: sevilla 2.54e-16, champagne 3.37e-16, genua 1.66e-16, malacca 1.88e-16,
gulf_of_siam 2.71e-16; worst overall **3.37e-16**, which is 1.52 ULP of a double
(eps = 2.2204e-16). The quoted 0 to 3.7e-16 traces to `validation-v5.md`'s node-by-node figures
(sevilla 0.0, malacca 2.1380e-16, genua 2.1712e-16, champagne 3.4985e-16, gulf_of_siam 3.6899e-16) and
sits in the same place as my own. "One to three units in the last place" is right — a relative error of
3.7e-16 is between 1.7 and 3.3 ULP depending on where the mantissa sits. *Caveat: the exact bound
depends on which countries collect, which the document does not state; the magnitude is robust to that
choice, the last digit is not.*

### Y128 — propagation is kept on a single graph: reading the one installed graph leaves the propagated term good-independent and the identity survives it, at 0 to 3.7e-16 — one to three ULP, not the single ULP v5.0 claimed
**Status:** CONFIRMED
**Method:** Checked the derivation; reused Y127's measurement; read v5.0's wording.
**Evidence:** Propagation under §1.9 adds, to a country's power at `n`, a share of its power in each
node downstream of `n`. If "downstream" is read off the single installed graph, that set is the same
for every good, so the added term carries no `g` and `powershare_C(n)` remains one number — the
identity is untouched. The magnitude is Y127's. v5.0's line 1210 quotes the same "0 to 3.7e-16" and
describes it elsewhere as a single ULP; 3.7e-16 exceeds one ULP (2.22e-16), so the correction is
right.

### Y129 — gulf_of_siam's 29 goods leave it by seven distinct downstream sets
**Status:** CONFIRMED (measurement)
**Method:** Built all 29 per-good graphs on the v6.0 field and collected the distinct out-neighbour
sets of `gulf_of_siam`.
**Evidence:** *independent* — exactly **7** distinct sets: `{}`, `{burma}`, `{burma, canton}`,
`{burma, canton, malacca}`, `{burma, malacca}`, `{canton}`, `{canton, malacca}`. (v5.0 said eight, on
its own field; the field changed.)

### Y130 — per-good propagation destroys the exactness: once downstream sets differ, a country's power at the node is no longer one number, powershare_C no longer factors out, and a single node scalar cannot reproduce every collector's income exactly — a claim about exactness, not magnitude
**Status:** PARTIAL (derivation)
**Method:** Checked the argument against Y129 and against the algebra of Y127; then tested the final
clause constructively by building the collected-value-weighted mean share and asking whether it
reproduces income and whether it is a legal share vector.
**Evidence:** The first two clauses hold. The factoring in Y127 needs `ps_C` free of `g`; under
per-good propagation
`ps_C(n,g) = (base_C(n) + Σ_{m ∈ down(n,g)} pow_C(m)/DIVIDER) / Σ_collectors(…)`, which depends on `g`
whenever `down(n,g)` varies — and it does vary, seven ways at `gulf_of_siam` (Y129) — so the sum does
not collapse term by term. **The third clause is false as stated.** Define
`ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`, the mean share weighted by *collected* value. Then
`collect_pool · ps̄_C = income_C` identically, and `Σ_C ps̄_C = 1` because `Σ_C ps_C(g) = 1` for every
`g` — so it is a legal share vector, not a fudge. *independent* — measured across `sevilla`,
`champagne`, `genua`, `malacca` and `gulf_of_siam` and under five different collector sets (all
countries, top half, bottom half, top three, top one): worst relative error **1e-14 %** or below in
every one of the 25 cases, and `Σ_C ps̄_C = 1.000000000000` in every case. Both quantities the
weighting needs — `v_g` and `cs_g` — are computed per good at write time already (§2.6's table sums
them into `collect_pool`), so no extra state is required. So a single scalar per (node, country) does
reproduce every collector's income exactly. What per-good propagation actually destroys is that this
scalar be **derivable from trade power alone**: `ps̄_C` is a value-weighted quantity, not a power
ratio, so installing it means writing a country a fictitious per-node power whose ratio equals it —
and the real cost is whatever else in the engine reads that power field, not the identity.
**Should say:** "… and `powershare_C` no longer factors out of the per-good sum. A single node scalar
still reproduces every collector's income exactly — the collected-value-weighted mean share does, and
sums to 1 — but it is no longer the country's power ratio, so the engine's power field would have to
carry a derived quantity instead of a measured one. That, not the exactness, is what per-good
propagation costs." This also makes Y132's bound unnecessary: with the right scalar the error is zero.

### Y131 — substituting the share at one arbitrarily chosen reference commodity gives per-collector errors up to +7.4% at sevilla, and sweeping which commodity is chosen moves that collector's error across a 17.8-point range
**Status:** CONFIRMED (measurement, to the precision the stated construction allows)
**Method:** Built per-good propagated power at each of the five nodes from the save's country tables
and the per-good graphs (`TRADE_PROPAGATE_DIVIDER = 5`), computed each collector's exact per-good
income, then replaced its share with the share at a single reference commodity and swept the reference
over all 29 goods.
**Evidence:** *independent* — at `sevilla` the reference-commodity substitution gives a maximum
per-collector error of **+7.76%** and a minimum of −9.98%, with the worst single collector's error
spanning **17.7 points** across the 29 choices. Against the claimed +7.4% and 17.8 points that is a
match within the freedom the construction leaves (which countries collect is not stated; I took the
top half by power). v5.0's own §3.10 records "Sevilla −0.82%, −0.87%, **+7.44%**", so the figure is
traceable. The claim's point — that these numbers measure the arbitrary choice, not the design — is
strongly supported: the same sweep at `champagne` spans 68.8 points and at `gulf_of_siam` 66.6.

### Y132 — substituting the value-weighted mean share across the node's goods keeps the error at at most 0.1% at every node measured
**Status:** PARTIAL (measurement)
**Method:** Two readings of "value-weighted mean share", both on the same construction as Y131.
**Evidence:** *independent* — weighting each good's share by `v_g · collected_share_g` makes the
substitution reproduce the exact income identically, error **≤ 4e-14 %** at every node, because that
weighted mean *is* `income_C / collect_pool` by construction (Y130). Weighting by trade value `v_g`
alone — which is what "value-weighted mean share across the node's goods" most naturally reads as —
gives, under a top-half collector set, sevilla 0.036%, malacca 0.037%, champagne 0.153%, genua 0.173%,
**gulf_of_siam 0.544%**: three of the five above 0.1%. And that reading is not merely
weighting-sensitive, it is **collector-set-sensitive by two orders of magnitude**. Sweeping the
collector set over five choices: all countries collect → 0.0000% everywhere (the shares become the
full power shares and the weighting cancels); top three → ≤ 0.036%; top one → 0.0000% trivially;
top half → ≤ 0.544%; bottom half → champagne 0.416%, genua 0.870%, gulf_of_siam 2.089%,
**sevilla 4.573%**. So under the v_g reading the honest statement is a range spanning 0% to about 4.6%
depending on two unstated choices, not a bound of 0.1%. The document names neither choice, so the
figure is not re-derivable from it — the exact defect Y135 identifies and demands be fixed.
**Should say:** state the weighting and the collector set, and prefer the defensible weighting over the
flattering number. The quantity an implementation would actually store is the collected-value-weighted
share — both of its inputs are already computed per good at write time — and under it the error is
**identically zero**, which is a stronger and simpler claim than "at most 0.1%". If the gross-value
weighting is meant instead, the figure is not a bound at all: it runs 0% to 4.6% across collector
sets, and should be stated as a range with the construction beside it.

### Y133 — the honest statement: per-good propagation costs the exact identity and buys a per-node error that a reasonable scalar keeps within a tenth of a percent, and the identity is what Goal 7 is stated in terms of
**Status:** PARTIAL (derivation)
**Method:** Checked each half.
**Evidence:** The third clause holds: Goal 7 ("The game's own numbers are the model's numbers. Anything
reading trade income reads the real one") is indeed stated as an identity. The first clause is now in
doubt for the reason Y130 gives — the exact identity survives per-good propagation if the stored
scalar is the collected-value-weighted share; what is lost is that the scalar be a power ratio. The
middle clause inherits Y132's bound, which does not reproduce: the error is identically zero under the
defensible weighting and runs to 4.6% under the other, not "within a tenth of a percent".
**Should say:** "per-good propagation costs the *power-ratio reading* of `powershare_C`, not the
identity: the collected-value-weighted share reproduces every collector's income exactly, and it is
the quantity an implementation already has at write time. What has to be justified is writing a
derived share into a field the engine treats as power." That is a different and better argument than
a tenth of a percent, and it is the one the measurement supports.

### Y134 — v1–v4.0's "off by 5.96 ducats on a node paying ~250" has no node with local trade value near 250 behind it, and the 112.6 figure v5.0 added is no longer carried
**Status:** CONFIRMED
**Method:** Computed node local trade value on the v6.0 field; read the save's `local_value` fields;
grepped the v6.0 spec for `112.6`.
**Evidence:** *independent* — the largest node local trade value in the model is `english_channel`
**112.60**, then mexico 103.40, gulf_of_siam 102.90, malacca 102.20, genua 101.00. No node exceeds 113,
let alone approaches 250. (The engine's own `local_value` at 1444 is smaller still — max 9.68 at
malacca — because it is monthly and per-node in the vanilla economy.) The spec has **zero**
occurrences of `112.6`. Both halves exact.

### Y135 — v4.0's 0.41% and v5.0's "redistributive and single-digit percent" were both artifacts of freezing the share at one commodity, and the construction behind any such figure has to be stated with it, which none of those documents did
**Status:** CONFIRMED
**Method:** Read v5.0's §3.10 paragraph and its retraction of v4.0; compared its numbers with Y131's.
**Evidence:** `v5-owner-agnostic/per-good-trade-spec.md` line 1210 reports "the error is
**redistributive and single-digit percent, with the sign varying by collector** — Sevilla −0.82%,
−0.87%, **+7.44%**", and retracts v4.0's figure: "v4.0's own replacement figure, 0.41%, was an
artifact of freezing one term at the alphabetically first commodity." v5.0's own +7.44% at Sevilla is
the reference-commodity substitution figure — the same construction it diagnosed in v4.0 — which is
exactly what Y135 asserts. And neither document states which countries collect: v5.0 says only "Its
size depends on which countries are collecting, which is a stated choice of the construction", without
stating it. The demand that the construction accompany the figure is therefore both correct and,
per Y132, not yet met by v6.0 itself.

---
# §3.13 — Open questions

### Y136 — the one open wealth question is now a design question: should any source beyond province condition multiply goods_produced? The two keys are granted in many places, v3.0–v5.0 tried to admit the province-scoped subset by rule, that rule was wrong in every audit that examined it, and re-admitting any source re-admits the maintenance burden for 0.98% of world wealth
**Status:** CONFIRMED
**Method:** Grepped `trade_goods_size` and `trade_goods_size_modifier` across `common/` for each of
the eight source classes the claim names; checked the framing against §1.3 and Y003.
**Evidence:** All eight grant one of the two keys: `common/buildings/` (`00_buildings.txt`,
`01_nativebuildings.txt`), `common/event_modifiers/` (`00_event_modifiers.txt`,
`01_mission_modifiers.txt`, `02_test_modifiers.txt`), `common/great_projects/` (`01_monuments.txt`),
`common/static_modifiers/` (`00_static_modifiers.txt`), `common/province_triggered_modifiers/`
(`00_modifiers.txt`), `common/holy_orders/` (`00_holy_orders.txt`), `common/state_edicts/`
(`zzz_chinese_industrialization.txt`, `zzz_urbanization.txt`), and trade-company investments
(`common/tradecompany_investments/00_Investments.txt`, two occurrences — note the directory is
`tradecompany_investments`, not `trade_company_investments`). "Many places" is exact and the
enumeration is complete for the keys named. The reframing from classification to design is consistent
with §1.3, which reads only the four condition modifiers. The 0.98% is Y003's figure — right as a
percentage; its province count is Y003's PARTIAL, and the "wrong in every audit" universal is Y004's
PARTIAL. Neither defect is in this claim's own assertion, which cites the percentage only.

### Y137 — under the calibration's α = 16 the cloves demand order is hangzhou, beijing, doab, and the sink lands on a high-demand node; v2's "Beijing holds the richest single province" is wrong — that is hangzhou
**Status:** CONFIRMED (measurement)
**Method:** Computed `c` at α = 16 over the counted provinces and ranked nodes; located the richest
single counted province.
**Evidence:** *independent* — at α = 16 the demand order is **hangzhou, beijing, doab**, canton,
lahore, genua. The unclamped calibration exponent does give α = 16 for cloves
(`(price/P₀)² = (8/2)² = 16`). The richest single counted province is pid 1821 at 27.00, in the
`hangzhou` node, not `beijing` (whose best is pid 1816 at 19.50) — so v2's attribution is indeed
wrong and hangzhou is the correct answer.

---

# §3.15 — Rejected

### Y138 — with v1's ε floor removed the contrasts run 4–97 on supply against 211–15,010 on demand over the 28 goods produced in more than one node; cloves has a single producer and no contrast to measure
**Status:** CONFIRMED (measurement)
**Method:** Re-ran `measure6.py`, which computes max/min over the positive entries of `s` and of `c`
per good and restricts the supply ratio to goods with more than one producing node.
**Evidence:** `measure6.out` lines 28–31: `supply contrast range (4, 97)`;
`goods with more than one producer 28`; `single-producer goods ['cloves']`;
`demand contrast range (211, 15010)`. Every figure and the scoping both reproduce, and the scoping is
the repair v5's audit asked for (`"the contrasts run 4–97" — cloves has one producing node, ratio
1.00`).

### Y139 — v3.0 and v4.0 repeated the 10⁷ / 10²–10³ ratio in §3.15 while v4.0's own §3.2 was withdrawing it
**Status:** CONFIRMED
**Method:** Grepped `10⁷` in v3.0 and v4.0 and located each hit by section.
**Evidence:** `v3-owner-agnostic/per-good-trade-spec.md` line 1109 (§3.15): "supply contrast (10⁷)
drowns demand contrast (10²–10³)". `v4-owner-agnostic/per-good-trade-spec.md` line 1200 (§3.15): the
same sentence. And `v4-owner-agnostic/per-good-trade-spec.md` line 837 (§3.2): "That ratio was
`max(s)` over the **ε floor** of v1's regularizer" — the withdrawal, in the same document. The claim's
attribution (both sections, one document) is exact.

### Y140 — ranked orientation wins the sink–demand alignment statistics and loses delivery — a sixth of world demand stranded, orphan sinks, net-producer sinks where DRAIN/LAP/FLOW post none, several times DRAIN's sinks per good — all stated without figures
**Status:** CONFIRMED
**Method:** Located each element in the source documents; checked the v6.0 text for figures.
**Evidence:** `v1-laplacian/ranked-orientation.md` line 476 records "sixth of world demand ends up
unreachable, and the flagship result — Genoa as a cloves sink —"; `v2-drain/drain-orientation.md`
line 99 records "RANK achieved it and stranded a sixth of world demand". The v6.0 §3.15 entry carries
no percentage, no sink count and no alignment figure — only the directions — and §3.2's independent
statement of the same failure ("demand had to increase at every hop, so one sixth of world demand
became unreachable and Genoa was crowned a cloves sink that cloves could not reach") is consistent
with it. The R3 requirement is met and the disavowal of v2's "wins every sink statistic" is accurate:
alignment and delivery are different statistics and the entry now says which is which.

### Y141 — seeded basin growth leaves demand unserved at every tuning tried; the 88.4% reach figure is dropped
**Status:** CONFIRMED
**Method:** Grepped `88.4` in v5.0 and in v6.0.
**Evidence:** `v5-owner-agnostic/per-good-trade-spec.md` line 1359 carries "88.4% reach at its best
tuning"; the v6.0 spec has **zero** occurrences of `88.4`. The surviving statement — flow converges to
the chosen seeds and starves everything off a supply→seed path — is the structural reason and needs no
figure, and it is the same reason §3.2 gives for why conservation-imposing operators serve 100% and
non-imposing ones do not.

### Y142 — the 3-mass gravity field reproduces whatever end count it is seeded with while γ is small enough and loses that property as γ approaches 1; no figures are maintained, and the three rejection grounds are non-numeric
**Status:** CONFIRMED
**Method:** Re-ran `phiw3.py`'s V225 block on the v6.0 field; grepped the v6.0 spec for the entry's
old figures.
**Evidence:** *independent* — seeding 1 to 6 masses and reading the end count at
γ ∈ {0.1, 0.3, 0.5, 0.7, 0.9}: 1 mass → 1,1,1,1,1; 2 → 2,2,2,2,2; 3 → 3,3,3,3,3; 4 → 4,4,4,4,4;
5 → 5,5,5,5,**4**; 6 → 6,6,6,6,**4**. So the count follows the seeds up to γ = 0.7 and breaks down at
0.9 — "while γ is small enough … loses that property as γ approaches 1", exactly. Pushing further, the
3-mass field itself collapses from 3 ends to 1 at γ = 0.98. The spec carries none of the entry's old
numbers (zero occurrences of `97 of 159 arrows`, `110 of 159`, `61%`, `≥10 ends at α up to 16`), and
the three rejection grounds as stated — pins the count by fiat, needs a second operator with its own
reach knob, and a pure `wealth^α` comparison with no reach term does not concentrate ends — contain no
figures and none is needed for any of them.

---

# §3.16 — Evidence standard

### Y143 — v1's ε instantiation failed the α = 1 identity at the tolerance v1 used; the 1e-5 figure is no longer carried
**Status:** PARTIAL
**Method:** Located the original measurement in `v1-laplacian/validation.md` and its restatement in
`v2-drain/validation-v2.md`; grepped the v6.0 spec.
**Evidence:** The underlying fact holds. `v1-laplacian/validation.md` line 4921: reading the spec
literally, `eps=0 → rel.residual 1.959e-15`; **`eps=1e-6 → 1.151e-05`**; `eps=1e-3 → 1.157e-02`. And
applying ε to `φ₀`'s supply as well restores exactness at every ε. `v2-drain/validation-v2.md` line
643 re-measures it at **9.58e-06** and calls it "the ~1e-5 failure". The v6.0 spec has zero
occurrences of `1e-5`, so the figure is indeed dropped. But the replacement phrase misdescribes it:
1e-5 was the **residual magnitude**, not a tolerance, and the ε v1 used was **1e-6**. "Failed … at the
tolerance v1 used" reads as though 1e-5 were an acceptance threshold.
**Should say:** "implemented as written, the identity failed — a residual five orders of magnitude
above the exact case at v1's own ε of 1e-6 — and would have been diagnosed as a solver bug", which
drops the number without misnaming it.

---

# Appendix — what this audit could not settle

Three propositions in the delta rest on engine behaviour that no shipped file and no field of the
1444 save records. Each is graded above on the evidence that exists; they are listed together here so
the next revision knows which three need a running game rather than another parse.

1. **Whether the `devastation` static modifier is scaled by the devastation level** (Y034). The file
   states `-2` and nothing about scaling; the save stores no per-province `goods_produced` or
   `trade_goods_size`; province `trade_power` does not decompose finely enough to infer it. The same
   question applies to `prosperity`, which the spec's table does not mark as scaled.
2. **The three tooltip readings** — Garnatah's `Base: 0.49 (Yearly 6.00)` and `0.62` at 125%, Caceres's
   `Base: 0.16 (Yearly 2.00)`, and the production tooltip's `3.52 → +0.29` (Y027, Y029, Y031). The
   *arithmetic* built on them is checkable and one of the three schemas fails it (Y027); the readings
   themselves are single observations from a prior session.
3. **Probe 15's propagation observation** (Y104). One node, one country, recorded in
   `../v2-drain/game-session.md`. The claim's own scoping is the right one and the observation cannot
   be strengthened without another session.

Two further propositions are historical measurements on operators the model has deleted, so they are
not re-derivable on the v6.0 field and were graded against the record that produced them:
**Y114** (v1's production-income substitution, 159/159 → 68/159) and **Y143** (v1's ε residual).
