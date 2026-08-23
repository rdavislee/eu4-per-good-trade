# Independent pre-confirmation of `fixes-round2.md`

Every proposed value in `fixes-round2.md` (N01–N20, S01–S14) measured from a primary source before
any of it is applied. **Nothing in the specification, the claim inventory, the proposal file or any
script was modified by this pass.** `scripts/measure6.out` was backed up before running
`measure6.py`, the run reproduced it byte-for-byte (md5 `d36934f0dd1abaccaec0a75a178c1500`), and the
backup was restored.

**Primary sources used.**

- Install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`, 1.37.5.0, Leviathan present.
- Save: `…\save games\VANILLA_start.eu4` → ZIP entry `gamestate`, province records at column 0, fields at two tabs.
- Reference implementation: `scripts/solver.py`, `scripts/drain.py`, `scripts/measure6.py`, `scripts/verify6.py`.

**Independence note.** Rather than trust `prov1444.json`, the province table was rebuilt straight
from the save's `gamestate` (owner, `base_tax`, `base_production`, `trade_goods`, `devastation`) with
node membership from `common/tradenodes/00_tradenodes.txt` and prices from
`common/prices/00_prices.txt`. That table's per-province wealth equals `solver.ROWS`' wealth **to
zero difference on all 2,472 provinces**, so every solver-derived figure below rests on the save.
Where a figure is re-derived a second time with code written for this pass, it is marked
*(re-derived independently)*.

**Nothing here needed a running game.** N15/N16 are timing measurements and are machine- and
load-dependent rather than game-dependent; that is stated in their rows.

---

## The two mechanism fixes

### M-a — the solver reads the good the engine rolled for the `trade_goods = unknown` provinces

**CONFIRMED, and the count "twenty" is exact.**

An independent date-gated parse of `history/provinces/*.txt` (brace-depth walk, base block plus every
dated block ≤ 1444.11.11) finds exactly **20** counted provinces whose history good is `unknown`:
774, 862, 895, 897, 907, 966, 1809, 2014, 2503, 2510, 2571, 2593, 2596, 2669, 2671, 2932, 4856,
4901, 4902, 4923. For each one the good the save records matches what `solver.ROLLED` supplies —
wool, wool, naval_supplies, grain, grain, fur, livestock, cotton, fur, fur, fur, fur, grain, grain,
fur, wool, **incense**, fur, livestock, grain. `solver.py:93-122` reads them from the save's
`gamestate`; `solver.py:139-141` substitutes them; `measure6.out` line 8 confirms
`provinces with trade_goods unknown  0`.

The production income those twenty now contribute totals **12.70 ducats**, which is exactly the
10,594.70 → 10,607.40 shift in N01.

*Source:* `history/provinces/`; save `gamestate`; `scripts/solver.py:89-151`.

### M-b — the coal counterfactual holds every non-repriced input fixed

**CONFIRMED, and the arithmetic behind it checks out.**

Province **4237** is the sole member of `latent-coal ∩ ON_STARTUP_DEVASTATION` (58 latent-coal
provinces in history, 45 owned and counted; devastated set = 11). Its `base_production` is 3.0 and
`PRICES["coal"]` is 10.0, so the devastation multiplier is worth
`0.2 × 3 × 10 × (1 − 0.6) = 2.40` ducats.

Running both variants on the v6.0 field:

| variant | wealth delta | edge flips |
|---|---|---|
| devastation **retained** (M-b as applied) | **214.60** | **10** |
| devastation dropped (the mixed counterfactual) | 217.00 | 13 |

The difference is exactly 2.40 ducats and 3 flips, matching the comment at `measure6.py:179-182`.

*Command:* re-ran the block from `measure6.py:171-191` with the devastation multiplier switched on and off.

---

## Numeric values

| id | quantity | proposed | measured | agree | primary source / command |
|---|---|---|---|---|---|
| N01 | world wealth | 10,607.40 | **10,607.40** (10607.4000000000) | **yes** | save `gamestate` + `00_tradenodes.txt` + `00_prices.txt`, summed independently; matches `measure6.out` line 4 |
| N02 | counted provinces | 2,472 | **2,472** | **yes** | save: provinces with an `owner` lying in a trade node = 2,472 |
| N03 | provinces the apparatus was worth | 88 | **89** (87 under the withdrawn `is_city` filter) | **no** | reconstructed `v5-owner-agnostic/scripts/solver.py:59-73` on the v6.0 field — see note N03 |
| N04 | largest \|b_w\| | 0.0225 | **0.0225** (0.022531, at `genua`) | **yes** | *(re-derived independently)* `b_w = 1/N − c_w`, `c_w ∝ Σ(w/w_max)^1.5` on the save-derived field |
| N05 | sinks per good | 1–8, mean 3.72 | **1–8, mean 3.72** | **yes** | *(re-derived independently)* 29 per-good DRAIN runs; also `measure6.out` line 21 |
| N06 | `Φ_w` self-coherence, edge-goods | 53.6% | **53.6%** (2,473 of 4,611) | **yes** | *(re-derived independently)*; `measure6.out` line 24 |
| N07 | `Φ_w` self-coherence, value-weighted | 52.3% | **52.3%** | **yes** | *(re-derived independently)*; `measure6.out` line 25 |
| N08 | ordered pairs connected | 89.6%, count from the run | **89.6% — 5,663 of 6,320** | **yes** | *(re-derived independently)* 29 goods × 80 BFS; `measure6.out` lines 26–27 |
| N09 | widest α band on [1, 8] | 1.71 wide, [3.50, 5.21] | **[3.50, 5.21], width 1.71** (`doab+genua+hangzhou`) | **yes** | *(re-derived independently)* 701-point sweep at 0.01; `measure6.out` line 33 |
| N10 | coal activation, edge flips | 10 of 159 | **10 of 159** | **yes** | `measure6.out` line 53; reproduced in the M-b table above |
| N11 | coal activation, wealth delta | 214.60 ducats | **214.60** | **yes** | `measure6.out` line 52; reproduced in the M-b table above |
| N12 | caravan cap share, median, flag basis 26 nodes | 21.6% | **21.57% → 21.6%** | **yes** | save `trade={}` node `total`s + `inland = yes` flag — see note N12/N13 |
| N13 | caravan cap share, median, derived basis 25 nodes | 17.7% | **21.3%** on that basis; 17.7% belongs to the *flag* basis after-grant reading | **no** | same; the proposal's own hedge is right — see note N12/N13 |
| N14 | max development at 1444 | 33 | **33** (pid 1821, `base_tax` 15 + `base_production` 15 + `base_manpower` 3) | **yes** | save `gamestate`, province `-1821`; also the richest province at 27.00 |
| N15 | solve cost, per good, average | 3.7–9.7 ms | **3.5–10.5 / 3.5–10.8 / 3.1–4.7 ms** over three replicates of the 12-run experiment | **not reproducible as a band** | `drain.run_drain` × 29 goods × 12 passes, warm-up first — see note N15/N16 |
| N16 | runs inside 0.17–0.21 s | 6 of 12 | **1 of 12, then 0 of 12, then 0 of 12** | **no** | same three replicates — see note N15/N16 |
| N17 | non-executable `change_price` blocks | 4 `effect_tooltip` + 3 insight `effect = "…"` + 3 `tooltip = { }` | **exactly that: 4 + 3 + 3 = 10 of 161** | **yes** | quote-and-brace-aware sweep of `events/ decisions/ missions/ common/ history/` — see note N17 |
| N18 | §3.9 node-wealth ranks | genua 4th, gulf_of_siam 3rd, sevilla 7th; `mexico` 2nd | **genua 4 (296.00), gulf_of_siam 3 (297.90), sevilla 7 (266.50), mexico 2 (300.40), english_channel 1 (316.60)** | **yes** | *(re-derived independently)* node wealth from the save-derived field |
| N19 | scale test, sink set at ×10⁻⁶ | collapses to `{genua}` | **`{genua}`**, 100 flips | **yes** | *(re-derived independently)* `run_drain(b_w × s)` for s ∈ {100, 10, 1, 1e-2, 1e-4, 1e-6} |
| N20 | v1 identity residual | 1e-5 was the residual; v1's ε was 1e-6 | **both confirmed** | **yes** | `v1-laplacian/per-good-trade-spec.md:46`; `v1-laplacian/validation.md:4921` — see note N20 |

### Note N03 — 89, not 88

Reconstructing v5.0's deleted apparatus (`v5-owner-agnostic/scripts/solver.py:59-73`:
`gems local_tax_modifier 0.15`, `incense trade_value_modifier 0.10`, five `MON_FLAT`, one
`MON_GPMOD`, four `MON_TVMOD`, ten `PERM_FLAT`) on top of the v6.0 province table:

```
v6.0 field (apparatus off)   10,607.40
apparatus on                 10,712.70
delta                           105.30   = 0.9829% of the apparatus-on total, 0.9927% of the v6.0 field
touched provinces                    89   = 43 gems + 31 incense + 16 project/permanent − 1 overlap (pid 542)
touched under is_city = yes           87   = 43 gems + 29 incense + 16 − 1
```

The audit's 88 used **30** incense provinces. **M-a is what moves it to 31**: province 4856
(Barunggam) is one of the twenty `unknown`-history provinces and the engine rolled it **incense**, so
the apparatus' `trade_value_modifier` now touches it. The count under v6.0's own counting rule *and*
M-a is therefore **89**. 87 remains the count under the `is_city = yes` filter v6.0 withdrew, and
**0.98% still holds** (0.9829%).

Cross-checks on the apparatus set: 43 `gems` and 31 `incense` counted provinces; the ten
`add_permanent_province_modifier` pids are a subset of the 73 provinces whose *undated* history block
carries that effect (independent sweep of `history/provinces/`).

*Commands:* apparatus reconstruction over `solver.ROWS`; undated-`add_permanent_province_modifier` sweep of `history/provinces/`.

### Note N12/N13 — the two bases, all four readings

From the save's `trade={}` block (each node's `total=`), against `inland = yes` in
`common/tradenodes/00_tradenodes.txt` (26 nodes) and against §2.2's derivation "no coastal member"
using `scripts/coastal.json` (25 nodes; the one dropped node is `siberia`):

| basis | reading | range | median |
|---|---|---|---|
| flag, 26 nodes | `50/total` | 9.40% (`champagne`) – 47.01% (`xian`) | **21.57% → 21.6%** |
| flag, 26 nodes | `50/(total+50)` | 8.59% – 31.98% | **17.74% → 17.7%** |
| derived, 25 nodes | `50/total` | 9.40% – 47.01% | **21.26% → 21.3%** |
| derived, 25 nodes | `50/(total+50)` | 8.59% – 31.98% | **17.53% → 17.5%** |

So **N12 is confirmed** (21.6%) and **N13's label and value do not go together**: 17.7% is the
after-grant median on the *flag's* 26 nodes — it replaces the spec's "median 17.9%", not its
"21.3%". The derived 25-node basis still gives **21.3%** on the `50/total` reading the spec's
sentence is about, and the proposal's own note ("the two bases may have been swapped") is correct.

Supporting figures all reproduce: node totals 106.4 at `xian` to 532.0 at `champagne`; two middle
order statistics `samarkand` 21.26% / `yumen` 21.88% (so 21.9% is the upper of the two, not the
median); largest single incumbent 23.6–143.2 from the country sub-blocks; cap outweighs it in 7 of 26.

### Note N15/N16 — timing

Method as described in the audit: 29 per-good DRAIN solves on prebuilt balance vectors, one warm-up
call, then twelve consecutive passes; repeated three times.

| replicate | total range | per-good mean range | largest single good | inside [0.17, 0.21] s |
|---|---|---|---|---|
| 1 | 0.100–0.303 s | **3.5–10.5 ms** | 17.2 ms | **1 of 12** |
| 2 | 0.101–0.314 s | **3.5–10.8 ms** | 22.3 ms | **0 of 12** |
| 3 | 0.091–0.137 s | **3.1–4.7 ms** | 16.2 ms | **0 of 12** |

N15's **3.7–9.7 ms** sits inside the union of my three bands but is not itself reproducible as a
band — replicate 3 never reached 9.7 and replicates 1–2 exceeded it. N16's **6 of 12** does not
reproduce at all here: I measured 1, 0, 0. Both quantities are exactly what the spec's own sentence
says they are — "a statement about a machine and a scheduler rather than about the algorithm" — so
neither should be installed as a figure. This is a machine limitation, not a game-dependence.

### Note N17 — the ten non-executable blocks, itemised

Quote-and-brace-aware scan of all `*.txt` under `events/ decisions/ missions/ common/ history/`
(comments stripped `#`-outside-quotes; brace stack keyed by the identifier before each `{`; quoted
strings keyed by the identifier before the opening `"`). Total **161** textual blocks — events 93,
missions 14, common 1, history 53, decisions 0 — of which ten never execute:

| kind | count | file : line |
|---|---|---|
| quoted `effect_tooltip = "…"` | **4** | `missions/DOM_Britain_Missions.txt:919`; `missions/KoK_Persia_Missions.txt:3384, 3390, 3396` |
| quoted `effect = "…"` inside `country_event_with_effect_insight` | **3** | `missions/KoK_Byzantine_Missions.txt:2070`; `missions/KoK_Yemen_Missions.txt:954`; `missions/WOC_Italian_Missions.txt:2841` |
| `tooltip = { }` display wrapper | **3** | `events/flavorMAL.txt:1736` (`country_event → option → tooltip`); `missions/WOC_Hisn_Kayfa_Missions.txt:1448, 1459` (`effect → if/else → tooltip`) |

The three `effect = "…"` cases were read in place: each sits directly inside
`country_event_with_effect_insight = { id = … effect = " … " }`, so "insight" is the right name for
them. 161 − 10 = **151 executable**, unchanged.

### Note N20 — the residual and the ε

- `v1-laplacian/per-good-trade-spec.md:46` states the regulariser as `s ← (1 − ε)·s + ε/N   ε ≈ 10⁻⁶`. **v1's ε was 1e-6.**
- `v1-laplacian/validation.md:4921` records, reading the v1 spec literally: `eps=0 → 1.959e-15`, `eps=1e-6 → 1.151e-05`, `eps=1e-3 → 1.157e-02`. **1e-5 is the residual magnitude at ε = 1e-6**, not a tolerance.
- Reproduced on the v6.0 field with `solver.solve_all(α ≡ 1, eps)` against `solver.solve_phi0()` (which applies no ε, as the v1 spec reads): `eps=0 → 1.60e-15`, `eps=1e-6 → `**`9.11e-06`**, `eps=1e-3 → 9.13e-03`, `eps=1e-1 → 0.80`. First order in ε, ~1e-5 at 1e-6 — the same shape, on a different field. (v2 re-measured 9.58e-06.)

---

## Statements

### S01 — "`verify6.py` re-derives each figure from the document" — **PARTLY confirmed**

Read `scripts/verify6.py` in full and ran it against the spec.

- **`run_spec()` (the spec path): all 15 numeric needles now take their values from `measure6`'s computed `OUT` dict.** The five hardcoded literals the audit named are gone: connectivity now parses `O["ordered pairs connected"]` (`verify6.py:118-120`), Cape pairs come from `O` (:121-123), coal flips from `O["coal activation edge flips"]` (:124-125), the price census from `O["change_price textual blocks"]` (:130-131). The fifth — the widest-band needle `1.70, 3.51, 5.21` — was **removed rather than converted**; `run_spec` no longer checks the widest band at all.
- **`sources` is still a spelled-out-word needle.** `WORD.get(O["sources"], …)` at :107 does derive the word from the computed integer, so the *value* is computed; but the run prints `[PASS] spec: sources  **Eight sources** (x0 consistent)` — `NUMPAT` cannot match a word, so the internal-consistency half of `shows()` is inert on that needle.
- **Two literals remain baked into needle text**: `159` inside the coal-flip template (:124) and the `WORD` map itself (:56-57).
- **The `run()` path — `fixes-agreed.md`, not the spec — still carries typed values**: `13.40` (:66), `5703, 6320` (:73), `0.0227` in the template (:74), `8` (:75), `1.70, 3.51, 5.21` (:80), `132` (:83), `27.00` (:84), plus five literal `present()` strings.
- **Attributions.** `measure6.py` now computes both coal figures (`measure6.out` lines 52–53), so the coal figures' `(measure6.py)` attribution is **earned**. It still computes **neither** 0.98% nor the province count — grepping `measure6.py` and `measure6.out` for `0.98` and for `87` returns nothing — so that attribution is **not yet earned**.
- Current state of the harness against the unedited spec: **23 checks, 8 failed** — world wealth, sinks per good (×2), self-coherence, largest `b_w`, connectivity, coal flips, coal wealth delta — i.e. precisely the figures round 2 proposes to change. Note the coal-delta needle formats as `{:.0f}` → `adds 215 ducats`, which will not match a spec that prints "214.60".

*Command:* `python verify6.py ../per-good-trade-spec.md`.

### S02 — `on_startup` fires `flavor_geo.1`; the `add_base_*` clause is wrong — **CONFIRMED**

- `common/on_actions/00_on_actions.txt:30` — `flavor_geo.1 # Disaster info`, inside `on_startup`'s `events = { }` list (lines 23–32). **Keep that half.**
- `events/FlavorGEO.txt:8-46` — `flavor_geo.1`'s whole effect is `add_legitimacy = -20`, `add_country_modifier = { name = "geo_powerful_nobles" duration = -1 }` and `set_country_flag = geo_received_starting_event` (in `immediate = { hidden_effect = { … } }`), plus a display-only `tooltip = { }` restating them in its single option. **No `add_base_*`, no `add_devastation`.**
- The keys are in `flavor_geo.3` (`events/FlavorGEO.txt:98-149`): option b carries `capital_scope = { add_base_tax = 2 add_base_production = 2 add_base_manpower = 1 }`, and options a/b carry `466 = { add_devastation = 100 / 50 }`.
- `flavor_geo.3` is fired from exactly one place in the install — `missions/KoK_Georgian_Missions.txt:2043` (`country_event = { id = flavor_geo.3 }`) — **not** from `on_startup`.

The spec's §1.3 item 1 (line 264) is therefore wrong in both of its clauses.

### S03 — "development can move before the first tick": delete — **CONFIRMED, 2,472 / 2,472**

Comparing the date-gated history parse (`prov1444.json`, built by `provinces.py`) field by field
against the save's `gamestate` over the 2,472 counted provinces:

| field | matches | mismatches |
|---|---|---|
| `base_tax` | **2,472 / 2,472** | none |
| `base_production` | **2,472 / 2,472** | none |
| `base_manpower` | **2,472 / 2,472** | none |
| total development (t+p+m) | **2,472 / 2,472** | none |
| `owner` | **2,472 / 2,472** | none |
| `trade_goods` | 2,452 / 2,472 | exactly the 20 M-a `unknown` provinces |

No province's development differs between the history parse and the engine's own start state. The
only field that moves is the trade good, on the twenty provinces M-a addresses.

### S04 — no route leaves `english_channel` — **CONFIRMED**

On the `Φ_w` graph (re-derived independently from the save-derived field):

- `english_channel`: **out-degree 0**, in-degree 5, out-neighbours `[]`. The set of nodes reachable from it is **empty**.
- `route('english_channel','hangzhou')` → **no route exists**. `route('genua','english_channel')` → no route exists either.
- So "from the Channel it is the Hansa and the Danube" describes nothing on this graph, and the Cape check "checked from … `english_channel`" is vacuous there.
- The other two routes are as the spec states: `genua → alexandria → aleppo → persia → lahore → lhasa → ganges_delta → burma → gulf_of_siam → canton → hangzhou` (the Silk Road), and from the north `north_sea → white_sea → novgorod → kazan → astrakhan → persia → …` (the Volga). Neither passes the Cape.
- **`measure6.py`'s route check still does not distinguish the two cases in its output.** `measure6.py:167` reads `P(..., (r_ is not None) and ("cape_of_good_hope" in r_))`, which guards against a crash but prints the same `False` for "no route" as for "a route that avoids the Cape" — `measure6.out` line 48 is that `False`.

### S05 — replace the universal with the count — **CONFIRMED, with two status refinements**

| audit | id | what it says | status as filed |
|---|---|---|---|
| `v3-owner-agnostic/validation-v3.md` | **W041** (line 68, 644) | "exactly three" local modifiers is wrong — `chinaware`'s `province = { local_autonomy = -0.1 }` is a fourth, and `bonus_from_merchant_republics` is a whole further class | **REFUTED** (one of v3's ten) |
| `v5-owner-agnostic/validation-v5.md` | **X030** (line 751) | the locality test's enumerated attribute list excludes the four province-state modifiers, and "on no country's state" excludes `occupied` / `under_siege` | **PARTIAL** |
| `v5-owner-agnostic/validation-v5.md` | **X034** (line 772) | v4.0 stated the rule and swept only `common/tradegoods/`, missing sixteen provinces | **CONFIRMED** |
| `v4-owner-agnostic/validation-v4.md` | **W041** (line 61) | the classification repair | **CONFIRMED** — and the run's own summary reads "203 assertions, 0 failed" / "No claim is left PARTIAL and none is REFUTED" (lines 18, 33) |

So three audits examined the classification and one of them passed it: "wrong in every audit that
examined it" is false, and the proposed replacement matches the files. The only refinement worth
carrying is that X030 is graded **PARTIAL**, not refuted; the flat refutation in v5.0 is X035
("REFUTED (the enumeration is incomplete and miscounts)"), alongside X034's confirmation.

### S06 — both halves go — **CONFIRMED on the algebra**

Take `income_C = Σ_g v_g · cs_g · ps_C(g)` and `collect_pool = Σ_g v_g · cs_g`, and define
`ps̄_C = income_C / collect_pool = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g`.

- `collect_pool · ps̄_C = income_C` is then true by substitution, for arbitrary `v_g`, `cs_g` and `ps_C(g)`. It is an **identity, not a measurement** — no tolerance, no field dependence.
- `Σ_C ps̄_C = Σ_g v_g·cs_g·(Σ_C ps_C(g)) / collect_pool = collect_pool / collect_pool = 1`, given only that per-good power shares sum to 1 across collectors — which is what makes them shares. So `ps̄_C` is a legal share vector.

Both halves of the spec's sentence therefore fail: a single node scalar **does** reproduce every
collector's income exactly, so "per-good propagation breaks the income identity" is wrong; and
"the error is ≤ 0.1%" is bounding a quantity that is identically zero under this weighting. The
real cost the proposal names is also correct as stated: `ps̄_C` is built from `v_g` and `cs_g`, so it
is a value-weighted quantity and **not** a ratio of trade power — installing it means writing a
country a per-node "power" that is a derived figure, and anything else reading that field reads it.

The "≤ 0.1%" figure is not re-derivable as a bound: it depends on a weighting (`v_g·cs_g` versus
`v_g` alone) and on a collector set, neither of which the spec states. I did not re-run that sweep;
the algebra above is what settles S06, and it settles it without one.

### S07 — uniform wealth does not equalise a per-node sum — **CONFIRMED**

Counted provinces per node on the 1444 field: **minimum 0, maximum 72**. The 0 is
`cape_of_good_hope` (79 of 80 nodes hold provinces; its node wealth is exactly 0); the 72 is
`mexico`. With uniform per-province wealth `w`, `Σ_{p∈n} w^{α_Φ}` is `count(n) · w^{α_Φ}`, which
varies by a factor of 72 across nodes (and is 0 at the Cape), so it is not equalised.

*Source:* save-derived province→node map; *(re-derived independently)*.

### S08 — the tax tooltip schema — **CONFIRMED**

Truncating to two decimals:

| form | at `base_tax` 6 | at `base_tax` 2 | reproduces the observations (0.49, 0.16)? |
|---|---|---|---|
| `trunc(base_tax / 12)` | **0.50** | 0.16 | **no** — 0.50 ≠ 0.49 |
| `trunc(base_tax × 0.083333)` | **0.49** (raw 0.49999800) | **0.16** (raw 0.16666600) | **yes, both** |
| `Yearly = 12 × Base` | 5.88 | 1.92 | no (parenthetical reads 6.00 / 2.00) |

So `trunc(base_tax/12)` is false on its own first data point, and only the ×0.083333 truncation
reproduces both readings.

### S09 — the divisor interval — **CONFIRMED: (11.73, 12.14]**

From the one production observation, annual 3.52 displayed monthly as `+0.29` and truncated at two
decimals: `0.29 ≤ 3.52/d < 0.30` ⟺ `3.52/0.30 < d ≤ 3.52/0.29` ⟺ **`d ∈ (11.733333, 12.137931]`**
→ **(11.73, 12.14]**. The spec's `[12.00, 12.14]` has the wrong lower bound: 11.80 satisfies the
observation and is excluded by it.

### S10 — the devastation scaling is an assumption — **CONFIRMED**

`common/static_modifiers/00_static_modifiers.txt:453-462`:

```
devastation = {
	trade_goods_size_modifier = -2
	…
}
```

and `:464-468` `prosperity = { … trade_goods_size_modifier = 0.25 … }`. The **−2 and the +0.25 are
file values**; **the scaling is not stated anywhere in the file.** Neither block carries a scaling
comment — and the file annotates scaling explicitly wherever it means it: `:475` "# Multiplied with
positive religious tolerance", `:1052` "# Scaled, multiplied by current corruption / 100", `:994`
"# Multiplied by Development/COUNTRY_DEVELOPMENT_SCALE", `:999` "# Multiplied by current
Legitimacy - 50", and a dozen more. So the spec's table row "`trade_goods_size_modifier = -2`,
**scaled by the devastation level**", under a preamble saying all four are "read from
`00_static_modifiers.txt`", attributes to the file something the file does not say. `defines.lua`
carries no devastation→goods scaling either (its `*_DEVASTATION_*` entries are all about devastation
accrual and decay).

The `prosperity` row likewise carries neither a scaling nor a direction annotation in the spec, while
`devastation` carries one — so the asymmetry the proposal points at is real.

### S11 — "it covers every trading policy" — **NOT confirmed; the file exempts two**

`common/trading_policies/00_trading_policies.txt` has nine top-level policies: `maximize_profit`
(:3), `maximize_profit_upgraded` (:29), `hostile_trading` (:55), `hostile_trading_upgraded` (:78),
`improve_inland_routes` (:101), `improve_inland_routes_upgraded` (:146), `establish_communities`
(:192), `establish_communities_upgraded` (:218), `propagate_religion` (:239). `defines.lua:1045`
reads `TRADING_POLICY_COOLDOWN_MONTHS = 12, -- Cooldown until you can change Trading Policy after
selecting.`

But the file carries a **`cooldown` key**, and it appears exactly twice — `:25` and `:52`, both
`cooldown = no`, at the policies' own top level (single tab, alongside `center_of_reformation` and
`button_gfx`), inside **`maximize_profit`** and **`maximize_profit_upgraded`**. `cooldown` occurs
nowhere else in `common/`.

So the measured statement is: the 12-month cooldown covers **seven of the nine** policies —
`propagate_religion` **included**, which is the part of the proposal that holds and is the part the
spec's "the two banded policies" gets wrong — while the two `maximize_profit` variants are exempted
by name in the policy file. The universal "**every** trading policy" is contradicted by the install.
(The key's meaning is read from its name and value; no file states it in prose.)

### S12 — v3.0 carries neither — **CONFIRMED**

`v3-owner-agnostic/per-good-trade-spec.md`: **0 occurrences** of `0.6125` and **0 occurrences** of
`12·X`. Its only tooltip readings are `Base: 0.49 (Yearly 6.00)` (line 149) and the same string in
the coefficient table (line 552), with no schema written around them.

Both constructions belong to v4.0 and v5.0 only:

| document | `Base: X (Yearly 12·X)` | `0.6125` |
|---|---|---|
| `v3-owner-agnostic/per-good-trade-spec.md` | absent | absent |
| `v4-owner-agnostic/per-good-trade-spec.md` | line 163 | line 178 |
| `v5-owner-agnostic/per-good-trade-spec.md` | line 170 | line 185 |

So the v6.0 spec's two "v3.0 through v5.0" attributions (lines 210 and 230) should name v4.0 and v5.0.

### S13 — §2.8's containment set is grounded on T3 — **CONFIRMED**

- §2.8's own row (spec line 962) says it: "Asserting containment in `{selected} ∪ {promoted}` alone would halt on **T3** (§3.2), which is correct behaviour, so the fallback set is part of the assertion".
- §3.2's T3 (spec lines 1070-1074) is a triangle with `b = 0` at all three nodes and node wealth **3, 2, 1** — three distinct values, **no tie** — where the fallback promotion is a sink in neither `{selected}` nor `{promoted}`. T3 holds whether or not the key ties.
- The tie could not be the ground on this field anyway: node wealth is **80 of 80 distinct** on 1444 (only `cape_of_good_hope` sits at exactly 0), so `drain.py:173/244`'s tiebreak `max(gated, key=(NODEW[v], -v))` never fires on a tie here.

### S14 — the Europe table does not show the Channel's basin growing — **CONFIRMED**

Re-derived independently (824 counted European provinces from `map/continent.txt`), scaling European
province wealth only, α_Φ = 1.5. Basin size = nodes that can reach the sink, the sink included:

| European development | `Φ_w` sinks (basin size) |
|---|---|
| ×1.00 | `english_channel` (18), `hangzhou` (78) |
| ×1.02 | `english_channel` (18), `wien` (47), `hangzhou` (61) |
| ×1.56 | `english_channel` (26), `rheinland` (78) — Asia holds none |
| ×2.00 | **`genua` (80) — alone; `english_channel` is not a sink at all** |

What the table shows is: **Asia's pole fading** (`hangzhou` 78 → 61 → gone), the Channel's basin
growing only over the first three rows (18 → 18 → 26), and at the top of the range **the single
European end moving off the Channel to `genua`**, which absorbs the whole map. "The Channel's basin
grows" is not what the last row says.

---

## Summary

**34 proposed values checked (N01–N20, S01–S14). 28 agree. 4 disagree. 2 cannot be installed as stated.**

| verdict | ids |
|---|---|
| agree | N01, N02, N04, N05, N06, N07, N08, N09, N10, N11, N12, N14, N17, N18, N19, N20, S02, S03, S04, S05, S06, S07, S08, S09, S10, S12, S13, S14 |
| disagree | **N03** (88 → measured **89**), **N13** (17.7% is the flag basis, not the derived one; derived = **21.3%**), **N16** (6 of 12 → measured **1, 0, 0 of 12**), **S11** ("every" → **seven of nine**; two policies carry `cooldown = no`) |
| not installable as stated | **N15** (band not reproducible: 3.5–10.5 / 3.5–10.8 / 3.1–4.7 ms), **S01** (true of `run_spec` only; `sources` consistency scan inert; `run()` still typed; the 0.98%/87 `(measure6.py)` attribution still unearned) |

Both mechanism fixes (M-a, M-b) do what they say, and every figure that depends on them reproduces.
