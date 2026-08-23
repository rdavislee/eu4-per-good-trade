# Independent measurement of `fixes-round4.md`

Every value in `fixes-round4.md` — Q01–Q12 and P01–P08, **20 in all** — computed or read from a
primary source by this pass. **Nothing in the specification, the claim inventory, the proposal file
or any existing script or output was modified**, and no file was added to the project tree: the
measurement scripts for this pass were written to a scratch directory outside the repository, and
`measure6.py` was deliberately *not* imported, because importing it rewrites `scripts/measure6.out`.
Its figures were re-derived from `solver.py` and `drain.py` directly instead.

**Result: 18 of 20 agree. Two do not — Q09 and the second half of Q10.** Two further agreements
carry a caveat worth reading (Q07 and Q12), and one line of the *prose* in "What to confirm" could
not be reproduced at all (the 16-sink figure; see the last section).

**Primary sources.**

- Install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`, 1.37.5.0, Leviathan present.
- Reference implementation: `scripts/solver.py`, `scripts/drain.py`, `scripts/flowop.py`.
- Relabelling instrument: `../v5-owner-agnostic/scripts/_audit_b_drain.py` (five-phase reimplementation, parameterised by node order).
- Shipped experiment: `scripts/relabel6.py`.
- Prior-version specs and audits: `../v1-laplacian/` … `../v5-owner-agnostic/`.
- Game files: `common/static_modifiers/00_static_modifiers.txt`, `common/defines.lua`, `common/tradenodes/00_tradenodes.txt`, `map/default.map`, `map/definition.csv`, `map/continent.txt`, `missions/*.txt`.

**Nothing here needed a running game.** Every Q-row is a property of the shipped files or of the
reference implementation. The one adjacent fact that *would* need one — that the engine applies the
`devastation` static modifier in proportion to the devastation level — is exactly what P07 says no
file states, and it is not asserted as measured here either.

---

## Summary

| id | the spec says | measured | agree |
|---|---|---|---|
| Q01 | orientation changed **800 of 800** | **800 of 800**, in each of three independent 800-trial runs | **yes** |
| Q02 | mean **25** of 159 edges move | **25.08 / 25.49 / 25.66** (three runs); median 25–26, range 5–44 | **yes** |
| Q03 | baseline sink set returned **64 of 800** | **67 / 62 / 60** | **yes**, within sampling |
| Q04 | `hangzhou` an end **786 of 800** | **789 / 784 / 771** | **yes**, within sampling |
| Q05 | `english_channel` an end **322 of 800** | **325 / 324 / 336** | **yes**, within sampling |
| Q06 | `gulf_of_siam` 459, `wien` 259, `rheinland` 122, `sevilla` 112 | 459/456/421, 260/261/269, 112/120/119, 117/93/108 | **yes**, within sampling |
| Q07 | LP objective deviation within **4.44e-16** | **4.4409e-16** exactly, in all three runs | **yes** (but §1.6 states 2.22e-16 for the same quantity) |
| Q08 | `Φ_ord` ends terminating no good **7 of 14** | **7 of 14** | **yes** |
| Q09 | Cape of Good Hope land provinces **20** | **19** land + 1 sea zone (province 1460) = 20 members | **NO** |
| Q10 | basin 18 → 28 by **×1.44**; end migrates to `genua` past **×1.70** | 18 at ×1.00 and 28 at ×1.44 — yes; `genua` sole end from **×1.64** — no | **half** |
| Q11 | `beijing` 3.63, `hangzhou` 4.13, `xian` 4.61, `canton` 4.78, `girin` 3.89, `yumen` 4.49 | 3.6264, 4.1253, 4.6056, 4.7754, 3.8876, 4.4928 | **yes** |
| Q12 | dev-scaled vs wealth-scaled, max difference **0.0** | **0.0** as the script prints it (12 dp); exact value 3.55e-15 | **yes**, with a note |
| P01 | per-seed ranges are themselves seed-dependent | three runs gave **97–100**, **95–100**, **93–99** per hundred | **yes** |
| P02 | wealth multiples, not demand; `girin` cheaper than three of the four | demand multiples are 6.91–10.44; `girin` 3.8876 < `hangzhou`, `xian`, `canton` | **yes** |
| P03 | two-test classifier is v4.0's; v3.0 used a block rule; sweep is v5.0's | v4 spec:184, v3 spec:162–166, v5 spec:17 / 201–202 | **yes** |
| P04 | the refuting ID is `validation-v5.md` X035 | X035 is REFUTED; X030 PARTIAL, X034 CONFIRMED | **yes** |
| P05 | 5.96 ducats spans v1–v3.0; v4.0 deleted it, its harness asserted it | v1/v2/v3 specs carry it, v4 spec has 0 hits, `validate_v4.py:452` asserts absence | **yes** |
| P06 | `verify6.py` matches totals only; `measure6.py` swallows parse failures | both hold; the total it validates over-counts by **7** | **yes** |
| P07 | every magnitude read from `00_static_modifiers.txt`; the scaling law is an assumption | all four rows verified at lines 433–467; no file states the scaling | **yes** |
| P08 | on the razed field `hangzhou` loses its end under every relabelling | **0 of 400** relabellings give `hangzhou` an end | **yes** |

---

## Instrument validation (required before Q01–Q07)

Run against the shipped `drain.py` on the identity permutation, exactly as `fixes-round4.md` asks:

```
--- shipped drain.py baseline -------------------------------------------
  N nodes                     : 80
  undirected edges            : 159
  Phase-0 core size           : 80
  Phase-1 selection S0        : ['genua']
  promotions / fallbacks      : 2 / 0
  promoted nodes              : ['english_channel', 'hangzhou']
  directed edges              : 159
  sinks                       : ('english_channel', 'hangzhou')
  LP objective (res.fun)      : 0.7122759778293255
--- instrument validation, identity permutation -------------------------
  edges agreeing with drain.py: 159 of 159
  sink set matches            : True
  core size                   : 80
  promotions / fallbacks      : 2 / 0
  objective sum|net|          : 0.71227597782932572
  |obj - drain.py res.fun|    : 2.220e-16
```

All four requested marks reproduce: **159 of 159 edges, a Phase-0 core of 80, 2 promotions, 0
fallbacks.** Two extra checks were needed because the LP objective (Q07) is not printed by
`relabel6.py`: the reimplementation exposes `net`, not `res.fun`, so the objective was taken as
`Σ|net|` and validated against `drain.py`'s `res.fun` on the identity permutation — they agree to
2.22e-16, one unit in the last place, so `Σ|net|` is a sound stand-in.

The three side-notes in "What to confirm" were also checked. **`drain.py`'s `sweep_priority(pid=…)`
hook does report no change at all:** over 20 random `pid` permutations the compiled orientation was
identical to the baseline **20 times out of 20**, because Phase 1, the stall promotion and Phase 2's
LP all still read the true index. **`solver.EDGES_UND` is a sorted list of a set**
(`EDGES_UND == sorted(set(EDGES_UND))` is `True`), so the re-sort inside the instrument is
load-bearing. The third note is the one that did not reproduce — last section.

`scripts/relabel6.py` exists, contains the experiment, performs this validation itself and calls
`sys.exit` on failure, so the mechanism-addition claim in the round-4 header is accurate.

---

## Q01–Q07 — node relabelling

The document's 800-trial figures come from an 8-seed set it does not name, so **three independent
800-relabelling runs** were made instead (8 seeds × 100 each) and every proportion is reported as a
range. Run A uses `relabel6.py`'s four default seeds plus `1 2 3 5`; runs B and C use disjoint seed
sets. Same construction as `relabel6.py`, plus the objective:

```
python q01_07.py "[[4242,7,999,20250821,1,2,3,5]]" 100
python q01_07.py "[[11,12,13,14,15,16,17,18],[101,202,303,404,505,606,707,808]]" 100
```

| quantity | run A | run B | run C | document |
|---|---|---|---|---|
| orientation changed | 800/800 | 800/800 | 800/800 | **800 of 800** |
| mean edges moving | 25.076 | 25.485 | 25.656 | **25** |
| edges moving, range | 5–42 | 6–41 | 7–44 | — |
| baseline sink set returned | 67 | 62 | 60 | **64** |
| `hangzhou` an end | 789 | 784 | 771 | **786** |
| `english_channel` an end | 325 | 324 | 336 | **322** |
| `gulf_of_siam` an end | 459 | 456 | 421 | **459** |
| `wien` an end | 260 | 261 | 269 | **259** |
| `rheinland` an end | 112 | 120 | 119 | **122** |
| `sevilla` an end | 117 | 93 | 108 | **112** |
| fully oriented 159/159 | 800/800 | 800/800 | 800/800 | (§1.6) |
| fallbacks fired | 0 | 0 | 0 | (§1.6) |
| sink-count range | 1–5 | 1–5 | 1–5 | 1 to 5, mostly 2–3 |
| max abs(objective − baseline) | 4.4409e-16 | 4.4409e-16 | 4.4409e-16 | **4.44e-16** |

**Q01 — 800 of 800: agrees.** All 2,400 relabellings measured moved at least one edge.

**Q02 — mean 25 of 159: agrees.** 25.08, 25.49, 25.66; medians 25, 26, 26.

**Q03, Q04, Q05, Q06 — agree within sampling.** These are sample proportions over an unnamed seed
set, so an exact re-hit is impossible and none is claimed. Every stated figure lies inside, or within
one standard error of, my three runs. Two remarks. `gulf_of_siam` **459** and `wien` **259/260** land
essentially on run A's values, which suggests run A's seeds overlap the document's set. `rheinland`
**122** is the one figure at or just above the top of my observed range (112–120); at n = 800 and
p ≈ 0.145 one standard error is about 10, so it is not out of family — but if any single figure in
this block is a transcription slip it is that one, and note that run A's pair is `rheinland` 112 /
`sevilla` 117 against the document's `rheinland` 122 / `sevilla` 112.

**Q07 — 4.44e-16: agrees exactly, and the spec contradicts itself elsewhere.** The maximum absolute
deviation of the LP objective from the baseline 0.7122759778293255 is **4.4409e-16** in all three
runs (2 units in the last place); the max−min spread within a run is 5.55e-16 to 6.66e-16.
**§1.6 (spec line 452) states the objective is "identical to 2.22e-16"** for the same experiment,
while §2.4 (line 914) and Q07 state 4.44e-16. The measured deviation reaches 4.44e-16, so Q07's
figure is the right one and the §1.6 sentence is the one to fix.

---

## Q08 — `Φ_ord` ends terminating no good: **7 of 14, agrees**

Built `Φ_ord = Σ_g V_g · order_g` from the per-good DRAIN marking orders on the current v6.0 field
(`V_g` = price × world goods produced, i.e. `measure6.py`'s `VAL`), oriented by descending `Φ_ord`,
and cross-referenced the ends against the per-good sink sets.

```
live goods                       : 29
goods whose order misses a node  : 0        (Phase 0 peels nothing, so the order is total)
edges oriented                   : 159 of 159
Phi_ord ends (out-degree 0)      : 14  ['amazonas_node','australia','basra','chengdu','james_bay',
                                        'katsina','laplata','philippines','ragusa','rheinland',
                                        'rio_grande','safi','white_sea','yumen']
Phi_ord sources                  : 4
ends terminating NO good         : 7 of 14
  they are                       : amazonas_node, basra, chengdu, james_bay, ragusa, rio_grande, yumen
top-5 demand capitals by c_w     : genua, english_channel, hangzhou, gulf_of_siam, champagne
any demand capital among ends    : []
```

**7 of 14 — exactly "half, not a majority".** The companion clause in the same §3.9 bullet ("none of
the demand capitals is among them") also holds. *For the record: an earlier note in my memory of this
project recorded 18 `Φ_ord` sinks with 9 terminating no good — that was the v5.0 wealth field. On the
corrected v6.0 field the counts are 14 and 7, so the change is expected rather than a discrepancy.*

---

## Q09 — Cape of Good Hope land provinces: document **20**, measured **19** — MISMATCH

`cape_of_good_hope`'s `members` list in `common/tradenodes/00_tradenodes.txt` holds **20 provinces**,
but one of them is a **sea zone**, not a land province:

```
cape members  : [1460, 789, 833, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182,
                 1173, 1800, 2856, 2864, 2880, 4781, 4782, 4783, 4784]
in sea_starts : [1460]      <- map/default.map line 14, inside the sea_starts block opening at line 5
in lakes      : []
```

Province **1460 is the sea zone "Cape of Good Hope"**: `map/definition.csv` names it, `default.map`
lists it in `sea_starts`, it is the trade node's own `location`, and its history file
(`history/provinces/1460 - Cape of Good Hope.txt`) contains nothing but two `discovered_by` lines —
no owner, no `base_tax`, no `base_production`. The node therefore has **19 land provinces plus its
sea location**.

Sweeping all 80 nodes: **minimum land count 19, uniquely `cape_of_good_hope`; maximum 77, `girin`**
(whose 77 members are all land). By *total members* the minimum is 20, shared by `cape_of_good_hope`
and `patagonia`. `champagne` has 33 land provinces, as §3.3 states.

This matters because §3.3's own arithmetic two sentences later uses **19**: "a 77-province node is
favoured over a **19**-province one by `(77/19)^0.5 ≈ 2×`". The paragraph currently carries both
numbers for the same node. **19 is the land count; 20 is the member count.** The distinction is
systematic, not a one-off: 37 of the 80 nodes have a member count above their land count, because
every coastal node includes at least one sea zone.

---

## Q10 — Channel basin under European growth: first half agrees, second half does not

European provinces from `map/continent.txt` (**824 counted**, agreeing with §1.6), `α_Φ` held at 1.5,
development scaled on European provinces only, basin = every node whose drainage reaches the node.

| European development | `english_channel` basin | `Φ_w` sinks |
|---|---|---|
| ×1.00 | **18** | `english_channel`, `hangzhou` |
| ×1.20 | 21 | + `gulf_of_siam`, `wien` |
| ×1.32 | 31 | `doab`, `english_channel`, `gulf_of_siam`, `hangzhou`, `wien` |
| ×1.40 | 28 | `english_channel`, `gulf_of_siam`, `hangzhou`, `rheinland` |
| ×1.44 | **28** | `english_channel`, `hangzhou`, `rheinland` |
| ×1.56 | 26 | `english_channel`, `rheinland` |
| ×1.63 | 26 | `english_channel`, **`genua`**, `rheinland` |
| **×1.64** | 25 | **`genua`** alone |
| ×1.70 | 20 | `genua` alone |

**"18 nodes to 28 by about ×1.44" — agrees as written.** The basin is 18 at ×1.00 and 28 at ×1.44.
One caveat for the reader: the growth is not monotone. The basin first reaches 28 at ×1.34 and peaks
at 31–33 around ×1.32 before settling back, so ×1.44 is a point where the basin *is* 28 rather than
the point where it first *becomes* 28.

**"the end migrates to `genua` past about ×1.70" — does not agree.** `genua` first holds an end at
**×1.63** (beside `english_channel` and `rheinland`) and is the **sole** sink from **×1.64**, staying
the sole sink continuously through ×2.00. The migration threshold is **×1.64**, not ×1.70. The
sentence is not false at ×1.70 — `genua` is the sole end there — but the figure quoted as the
threshold is 0.06 high. Note also that §1.6's later paragraph says scaling the **22 European nodes**
makes `genua` the sole sink "from about ×1.65"; the province-scaled threshold measured here is ×1.64,
so those two experiments are much closer together than the document's ×1.70 / ×1.65 pair suggests.

---

## Q11 — spice-sink wealth multiples: **all six agree**

Method, following `validation-v6` Y137's reading (b): the **v1 Laplacian** operator on `spices` (the
operator §3.2 is diagnosing), `α(spices) = price/P₀ = 3.0/2.0 = 1.5`, supply from goods produced,
demand `wealth^α` normalised over the world; multiply the target node's counted provinces' **wealth**
and bisect to 1e-12 until the node joins the sink set. Baseline LAP `spices` sink set on the v6.0
field: **`saxony` alone**. Spices are produced in 18 of 80 nodes.

| node | document | measured wealth multiple | as a demand multiple | sink set at that point | world demand share |
|---|---|---|---|---|---|
| `beijing` | 3.63× | **×3.6264** | ×6.91 | `{beijing, saxony}` | 9.5% (from 1.5%) |
| `hangzhou` | 4.13× | **×4.1253** | ×8.38 | `{hangzhou, saxony}` | 21.4% (from 3.2%) |
| `xian` | 4.61× | **×4.6056** | ×9.88 | `{saxony, xian}` | 12.3% (from 1.4%) |
| `canton` | 4.78× | **×4.7754** | ×10.44 | `{canton, saxony}` | 17.6% (from 2.0%) |
| `girin` | 3.89× | **×3.8876** | ×7.67 | `{girin, saxony}` | 9.8% (from 1.4%) |
| `yumen` | 4.49× | **×4.4928** | ×9.52 | `{saxony, yumen}` | 6.8% (from 0.8%) |

All six agree to the two decimals quoted, and §3.2's **3.6–4.8×** range is right. Two by-products for
the same paragraph: `chengdu` needs ×8.0876 and `lhasa` ×10.6697 (so the withdrawn "4.0–10.8×"
reproduces as 3.89–10.67), and `genua` becomes a LAP co-sink at **×1.7244**, confirming the "roughly
×1.7" in the sentence just above.

---

## Q12 — dev-scaled vs wealth-scaled: **0.0 as printed; the exact value is 3.55e-15**

Replicated `measure6.py`'s corrected form (lines 138–148): recompute wealth from **scaled
development** — `TAX_COEFF × base_tax × f + max(0, GP_COEFF × base_production × f × (1 + devastation))
× price` — and compare against the scaled-wealth array.

| k | max abs difference | sinks from dev-scaled | sinks from wealth-scaled |
|---|---|---|---|
| 1.02 | 3.5527e-15 | `english_channel`, `hangzhou`, `wien` | same |
| 1.44 | 3.5527e-15 | `english_channel`, `hangzhou`, `rheinland` | same |
| 1.56 | 3.5527e-15 | `english_channel`, `rheinland` | same |
| 2.00 | 0 (exactly) | `genua` | same |

**Agrees as the document means it:** `measure6.py` prints `round(…, 12)`, which is `0.0`, and the two
constructions give identical sink sets at every factor. The residual 3.55e-15 is float associativity
(multiplying `base_tax × f` before summing, versus scaling the summed wealth) — about 16 units in the
last place of a 30-ducat province, not a modelling difference. **The methodological half of Q12 is
satisfied:** the check does recompute from `PROV[...]["base_tax"]` and `["base_production"]` rather
than comparing `W·k` to `W·k`, so the tautology the row warns about is gone. If the spec wants a
literal figure it should either say "identical to 4e-15" or keep "0.0" with the rounding stated.

---

## P01 — pooled proportions, because a per-seed range is itself seed-dependent: **agrees**

Per-hundred `hangzhou` counts, three independent 800-trial runs:

- run A: 100, 99, 97, 98, 100, 98, 97, 100 → range **97–100**
- run B: 97, 99, 96, 100, 99, 100, 98, 95 → range **95–100**
- run C: 95, 99, 95, 99, 97, 95, 93, 98 → range **93–99**

Three honest runs, three different ranges — one of which (**97–100**) is exactly the first of the two
the document quotes, and the second (96–100) sits inside run B's spread. The claim's reasoning is
confirmed on new data, and pooling is the right presentation.

---

## P02 — wealth multiples, and `girin` is cheaper than three of the four: **agrees**

From the Q11 table: the quoted 3.6–4.8 figures are **wealth** multiples; the same interventions
expressed as demand multiples are **6.91–10.44×**, because `α(spices) = 1.5` and
`6.91^(1/1.5) = 3.63`. Describing 3.6–4.8 as demand multiples (v5.0's error) is wrong by exactly that
exponent. And `girin` at **×3.8876** needs less than **three** of the four named nodes — `hangzhou`
(4.1253), `xian` (4.6056), `canton` (4.7754) — while needing more than `beijing` (3.6264). "Less than
three of them" is precisely right.

---

## P03 — provenance of the classifier, the block rule and the sweep: **agrees, all three**

| claim | primary source |
|---|---|
| The two-test classifier is **v4.0's** | `../v4-owner-agnostic/per-good-trade-spec.md:184`: "**Which modifiers are local, and which of those enter wealth.** Two tests, and a modifier must pass both." The seven-row table and the "exactly **two** modifiers enter wealth" conclusion follow at :195–210. |
| **v3.0** used a structural rule about which block of a trade-good definition a modifier sits in | `../v3-owner-agnostic/per-good-trade-spec.md:162–166`: "The engine's own data model draws the line for us: a trade good's `province = { … }` block is province-scoped … its `modifier = { … }` block is country-scoped … Only the first kind is local." No "two tests" phrasing appears anywhere in the v3 spec. |
| The whole-install sweep is **v5.0's alone** | `../v5-owner-agnostic/per-good-trade-spec.md:17` ("the local-modifier classification is applied to the whole install rather than …") and :201–202 ("**The tests are applied to the whole install, not to one file.** v4.0 stated this rule and then swept only `common/tradegoods/`"). Searching the v4 spec for `whole install` / `whole-install` / `swept` returns **zero** hits. |

---

## P04 — the refuting ID is `validation-v5.md` X035: **agrees**

In `../v5-owner-agnostic/validation-v5.md`:

- **X035** (line 777) — "The vanilla set of local-and-entering modifiers is …" — **Status: REFUTED
  (the enumeration is incomplete and miscounts)**. Its method is the exhaustive install sweep; it
  finds six sources rather than four, and corrects "five province-state static modifiers" to four.
- **X030** (line 751) — the locality test itself — **PARTIAL**, not refuted.
- **X034** (line 772) — "v4.0 … swept only `common/tradegoods/`" — **CONFIRMED**, i.e. it confirms a
  statement *about* v4.0 rather than refuting the classifier.
- X033, the neighbouring row, is also PARTIAL and explicitly defers to X035 ("Ran the whole-install
  sweep myself (see X035)").

X035 is the only REFUTED verdict in the block, so the spec's citation at line 22 is the right one.

---

## P05 — the 5.96-ducat figure spans v1–v3.0, deleted in v4.0 with its own harness asserting it: **agrees**

| version | occurrences of `5.96` in that version's `per-good-trade-spec.md` |
|---|---|
| v1 | 1 — `../v1-laplacian/per-good-trade-spec.md:440` |
| v2 | 1 — `../v2-drain/per-good-trade-spec.md:708` |
| v3.0 | 1 — `../v3-owner-agnostic/per-good-trade-spec.md:986` (tagged "**[unverified in v3.0]**") |
| v4.0 | **0** |
| v5.0 | 0 (only the retraction parenthetical) |

`../v4-owner-agnostic/changes-v4.md:1450–1456` carries the deletion as entry `3.10-pergood`
("**Clears:** the 1.4e-14 and 5.96-ducat figures", with the sentence quoted under **Removed**), and
v4.0's own harness asserts it:

```
../v4-owner-agnostic/scripts/validate_v4.py:452
hasnt("3.10", "the 5.96-ducat figure", "off by 5.96 ducats on a node paying ~250")
```

So "v4.0 deleted it and its own harness asserted the deletion" is literally true, and the spec's
current attribution ("v1 through v3.0", spec line 1402) is the correct one — the "v1 through v4.0"
form still carried in `changes-v6.md` at lines 1082, 2587 and 2595 is the one that was wrong.

---

## P06 — the `change_price` census check and the swallowed parse failures: **agrees, and the gap is real**

**First half — confirmed.** `scripts/verify6.py` touches this census in exactly three places, none of
which reconciles per file:

- line 108 — `present(doc, "change_price census", "161 (events 93, missions 14, common 1, history 53, decisions 0)")`: a hard-coded string-presence check.
- lines 151–152 — `shows(doc, "spec: price census", "**{}** textual `change_price` blocks", O["change_price textual blocks"])`: the document's printed **total** against `measure6.py`'s computed total.
- lines 170–172 — the `events/` subtotal, likewise printed-versus-computed.

**Second half — confirmed as code.** `scripts/measure6.py:234–235` is

```python
try: walk(pdx.load(fp), tree)
except Exception: pass
```

so a file that fails to parse contributes nothing to `hits` and says nothing about it, while
`rawc[tree]` still counts its textual blocks from the regex on line 233.

**What the total hides.** Re-running both counts side by side over the five trees (7,911 `.txt`
files):

```
textual change_price blocks    : 161 {events 93, decisions 0, missions 14, common 1, history 53}
parsed change_price with tg+val: 154 {events 93, decisions 0, missions  7, common 1, history 53}
files that raised in the walker: 0
files whose text count != parsed count: 5
    missions\DOM_Britain_Missions.txt    1 textual, 0 parsed
    missions\KoK_Byzantine_Missions.txt  1 textual, 0 parsed
    missions\KoK_Persia_Missions.txt     3 textual, 0 parsed
    missions\KoK_Yemen_Missions.txt      1 textual, 0 parsed
    missions\WOC_Italian_Missions.txt    1 textual, 0 parsed
```

**The 161 that `verify6.py` validates over-counts the live effects by 7.** All seven sit inside
**quoted strings** — tooltip text in mission files, e.g. `missions/KoK_Persia_Missions.txt:3384–3401`,
where three `change_price = { … }` blocks lie inside a `"…"` literal that closes at line 3402. The
regex counts them; `pdx.py`'s quote-aware tokenizer correctly does not. One nuance worth stating
precisely: on this install **zero files raise**, so the bare `except` is a latent defect rather than
the cause of the 7-block gap — the loss happens inside a *successful* parse. Both halves of P06 are
true, and the census gap is the concrete consequence of the first half.

---

## P07 — the province-state table: **agrees, both halves**

Every magnitude and direction, read from
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\static_modifiers\00_static_modifiers.txt`:

| row | file line | text |
|---|---|---|
| `occupied` | 433–435 | `local_tax_modifier = -0.5`, `trade_goods_size_modifier = -0.5` |
| `under_siege` | 444–445 | `trade_goods_size_modifier = -0.25` |
| `devastation` | 453–454 | `trade_goods_size_modifier = -2` |
| `prosperity` | 464–466 | `trade_goods_size_modifier = 0.25` |

All four match the spec's §1.3 table at lines 264–268, including "only `occupied` touches the tax
term".

**The scaling law is indeed unstated.** `devastation`'s block carries the bare `-2` and nothing about
proportionality. The same file *does* document scaling wherever it exists — `# Multiplied by the
amount of papal influence` (line 966), `# Multiplied by the amount of Church Power` (970),
`# Multiplied by Development/COUNTRY_DEVELOPMENT_SCALE` (994), `# Scaled, multiplied by current
corruption / 100` (1052), plus a `development_scaled` block at 287 — so the absence of any such
comment at `devastation`, `prosperity`, `occupied` or `under_siege` is meaningful rather than
accidental. `common/defines.lua` has no define governing it either: its thirteen devastation entries
are all gain/decay rates (`PASSIVE_DEVASTATION_IMPACT`, `FORT_DEVASTATION_IMPACT`,
`DEVASTATION_DEVELOPMENT_SCALE`, …), none of which scales the static modifier. **`-2 × level/100` is
an assumption of the model, as P07 says.** Confirming the engine's actual behaviour would need a
running game; nothing here asserts it.

---

## P08 — `hangzhou` loses its end under every relabelling on the razed field: **agrees**

Razed field = the wealth of every province in the `hangzhou` node set to zero, `α_Φ` = 1.5, all other
inputs untouched. First the one-solve figures §2.8 quotes, as a construction check:

```
baseline sinks              : ('english_channel', 'hangzhou')
node wealth hangzhou/beijing: 226.7 / 143.0
richest province            : pid 1821, 27.00, in node hangzhou
razed hangzhou -> sinks     : ('doab', 'english_channel', 'gulf_of_siam')   22 edges flipped
razed beijing  -> sinks     : ('english_channel', 'hangzhou')               15 edges flipped
```

Every one of those matches §2.8's razed-China row, so the razed field is constructed the way the
document means it. Then 400 relabellings on that field (4 seeds × 100), with the instrument
re-validated on the identity permutation against `drain.py` first:

```
instrument on identity : sinks ('doab','english_channel','gulf_of_siam')  matches drain.py: True
relabellings           : 400
hangzhou an end        : 0 of 400
end holders            : gulf_of_siam 400, wien 155, english_channel 142, rheinland 93,
                         doab 80, sevilla 76, nippon 54, champagne 48, ganges_delta 24
```

**0 of 400.** The row's claim — that this is ordering-robust where §1.6's sink membership is not —
holds, and the contrast that makes it interesting is in the same table: `gulf_of_siam` holds an end in
**400 of 400** on the razed field, so the Asian end does not vanish, it moves.

---

## One prose figure in "What to confirm" that could not be reproduced

> "a reimplementation omitting Phase 0, Phase 1 or Phase 4 reports wild instability — 16 sinks on
> the identity permutation"

I could not reproduce 16 sinks by omitting any single phase, and two of the three named omissions are
**inert on this field**:

- **Phase 0 peels nothing.** `phase0(b_w)` returns a core of **80 of 80** with an empty peel log — the aggregate graph has no degree-1 node — so omitting Phase 0 cannot change anything on 1444.
- **Omitting Phase 1** (running the sweep with `S = ∅`) gives **2 sinks**, `{english_channel, hangzhou}`, and **0 edge flips**, because both ends arrive by stall promotion anyway (`genua`, Phase 1's pick, ends a transit node — exactly as §1.6 says).
- **Omitting Phase 4's free-edge orientation** (keeping only the 79 flow arcs and leaving 80 free edges undirected) gives **18** flow-terminal nodes, not 16.
- For completeness: omitting **Phase 2** (treating all 159 edges as free) gives **1** sink, `genua`; and the old scan-order sweep instead of the deterministic priority sweep gives the same 2 sinks with 28 flips.

The warning's *direction* is sound — a partial reimplementation is not a safe instrument, which is why
`relabel6.py` validates itself. But the "16 sinks" figure matches none of these constructions, and the
Phase 0 and Phase 1 clauses are vacuous on the 1444 aggregate field. If the sentence stays it needs
the construction that produced 16 recorded with it, or it should name Phase 2 and Phase 4 — the two
phases that actually carry the orientation here.
