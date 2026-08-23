# Independent measurement of `fixes-round5.md`

Every value in `fixes-round5.md` — V01–V12 and T01–T08, **20 in all** — computed or read from a
primary source by this pass. **Nothing in the specification, the claim inventory, the proposal file,
or any existing script or output was modified.** The spec's md5 is still
`f597de9d10ade20b0e69c5089932e8b4`, and `scripts/measure6.out` is still
`09c5281fa3f309a2cae5d0f6d9464a1f`. All measurement scripts for this pass were written to a scratch
directory outside the repository (`%TEMP%\pgt5`), and where a figure needed `measure6.py` or
`verify6.py` — both of which rewrite `scripts/measure6.out` on import — the whole `scripts/` tree was
copied to scratch first and run there, so the shipped output file was never touched.

**Result: 15 of 20 agree. Four do not — V08, T04, T05 and T07 — and one (V06) agrees only at the
seed `relabel6.py` hardcodes, and is a change of units rather than a change of value.** Three
agreements carry a provenance note worth reading (V01/V02, V11, V12).

**Primary sources.**

- Install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`, 1.37.5.0, Leviathan present.
- Save: `…\Europa Universalis IV\save games\VANILLA_start.eu4` (ZIP; `gamestate` is `EU4txt`).
- Reference implementation: `scripts/solver.py`, `scripts/drain.py`, `scripts/flowop.py`.
- Relabelling instrument: `../v5-owner-agnostic/scripts/_audit_b_drain.py`, plus the shipped sweep `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`.
- Shipped experiments and harness: `scripts/relabel6.py`, `scripts/verify6.py`, `scripts/measure6.py`.
- Game files: `common/static_modifiers/00_static_modifiers.txt`, `common/prices/00_prices.txt`, `events/PriceChanges.txt`, `history/countries/HAB - Austria.txt`, `history/provinces/*`, `map/continent.txt`.
- Prior versions: `../v1-laplacian/` … `../v5-owner-agnostic/`.

**Instrument validation, run before any relabelling trial.** `_audit_b_drain.drain` on the identity
permutation of the `Φ_w` field returns **exactly** what `drain.py` returns: Phase-0 core **80**,
**159 of 159** edges oriented and *identical as a set* (not merely equal in count), **2** promotions,
**0** fallbacks, sinks `{english_channel, hangzhou}`. `relabel6.py`'s own self-check prints the same
("edges agreeing with drain.py : 159 of 159 / sink set matches : True / validated."). Separately,
`_audit_b_1444perm.py`'s sanity pass reports **0 of 29** goods where the reimplementation disagrees
with `drain.py`. Every trial below re-sorts the arc list after permuting, so the relabelling is
genuine and not merely a row permutation of the LP.

---

## Summary

| id | proposed | measured | agree |
|---|---|---|---|
| V01 | 21 provinces with `unrest` > 0 | **21** (save); 16 from `history/provinces` alone | **yes** (save) |
| V02 | 4.834×1, 7.834×3, 9.834×6, 14.834×11 | **identical** (save); history gives 5×1, 8×3, 10×6, 15×6 | **yes** (save) |
| V03 | 12.23 ducats, 0.115% | **12.230680 ducats, 0.115303%** | **yes** |
| V04 | 0 edge flips | **0**, sink set unchanged; **0** under the history-integer variant too | **yes** |
| V05 | LP objective 0.712275977829 | **0.7122759778293255** → prints `0.712275977829` | **yes** |
| V06 | max relative deviation 6.235e-16 over 40 permutations | **6.2348e-16** at seed 20260821; **7.7935e-16** at 2 of 8 seeds; **1.09e-15** at 200 trials. The same run's *absolute* deviation is **4.4409e-16** — the "now" figure | **at that seed only; see below** |
| V07 | 40 of 40 different optimal support | **40/40 at all 8 seeds; 200/200 at 3 more** | **yes** |
| V08 | spec prints 303 distinct numeric figures | **286** under the tokenisation that reproduces every companion figure; 279–326 over 62 tokenisations; **no** tokenisation gives 1,148 total with 303 distinct | **no** |
| V09 | `verify6.py` pins 35, across 29 checks | **35 distinct values across 29 checks, 0 failed** (38 as printed strings; 32 if the `absent` needles are excluded) | **yes** |
| V10 | 7 of 14 `Φ_ord` ends terminate no good | **7 of 14**, exactly half; self-coherence 60.36% | **yes** |
| V11 | `NEW_DRAPERIES` floor for `wool` = 1.875 | **1.875** = 2.5 × (1 − 0.25) — but the −0.25 is the *history file's*, not the event's (−0.20 → 2.00) | **yes**, with a provenance note |
| V12 | between 1.625 and 1.6875, composition unknown | **1.625 / 1.6875** exactly for the two rules on −0.25 and −0.10; unsettleable from any readable save | **yes**, with a scope note |
| T01 | `unrest` is a fifth province-state modifier; its per-point scaling is in the file | file lines confirmed | **yes** |
| T02 | `devastation` is the only unverified scaling law in §1.3 | confirmed as scoped to §1.3 | **yes** |
| T03 | 580-of-580 is real, from a script in the tree | **580 of 580**, script runs | **yes** |
| T04 | count 9 → 10 → 8 → 7; end count moved 13 → 14 | numerator confirmed; end count moved **18 → 13 → 14** | **no** |
| T05 | ×1.00 basin 16–75; shipped 33 at ×1.53 falls **outside** 24–29 | ×1.00 maxima 32–80 across 7 seeds; at ×1.53 **33 is inside** the relabelled range in 3 of 7 seeds | **no** |
| T06 | basin size is missing from §1.6's conditional list | confirmed, and it *is* ordering-conditional | **yes** |
| T07 | two checkable counts; the ratio has moved four times | 35 checkable, 303 not; **three** recorded edits, four successive forms | **no** |
| T08 | `relabel6.py` computes the LP objective and says so when it cannot | both halves confirmed | **yes** |

---

## The values

### V01 — provinces with `unrest` > 0 at 1444, counted

**Proposed 21. Measured 21.** Agree.

Primary source: `VANILLA_start.eu4`, `gamestate`. Of **4,941** province records, **21** carry a
non-zero `unrest=` field, and all 21 are inside the model's counted set (owner + trade node,
2,472 provinces). None is negative and none is excluded by the counting rule.

```
python unrest.py     # scratch; parses gamestate the way solver._rolled_trade_goods() does
  province records in save        : 4941
  records with nonzero unrest     : 21
  of those, in the counted set    : 21
```

Citable instance: record `-1075={` sits at column 0 on `gamestate` line **330804**, and its
`\t\tunrest=14.834` field is on line **330833**.

**Provenance note, and it matters for V02/V03.** The 21 is a *save* fact, not a file fact. Resolving
`history/provinces/*` to 1444.11.11 the way `provinces.py` does gives **16** provinces with a
non-zero `unrest` key. The five extra — 1071 (Tara), 1074 (Sibir), 1076 (Kurgan), 4689 (Om), 4690
(Ishim), all SHY-owned — carry no `unrest` key in history at any date ≤ 1444.11.11 and get their
value at runtime. `prov1444.json` carries no `unrest` field at all, so admitting `unrest` to the
model means reading it from either the save or a re-parse of history, and the two disagree.

### V02 — their unrest values

**Proposed 4.834 ×1, 7.834 ×3, 9.834 ×6, 14.834 ×11. Measured identical.** Agree.

`{4.834: 1, 7.834: 3, 9.834: 6, 14.834: 11}` from the save, and the same histogram over all records
as over the counted ones. Min 4.834, max 14.834.

The 16 provinces that carry `unrest` in history carry the integers **5 ×1, 8 ×3, 10 ×6, 15 ×6** —
each save value is exactly 0.166 below the history integer, and the five runtime-only provinces all
land at 14.834. So the proposed row is right as a save reading and would be four different numbers
over sixteen provinces as a file reading.

### V03 — tax forgone to `unrest` at −0.02 per point

**Proposed 12.23 ducats, 0.115% of world wealth. Measured 12.230680 ducats, 0.115303%.** Agree.

Computed as `Σ TAX_COEFF · base_tax(p) · 0.02 · unrest(p)` over the 21, with `base_tax` from
`prov1444.json` and `unrest` from the save; world wealth 10,607.40 from `solver.ROWS`. Worst single
province is 1075 (unrest 14.834, `base_tax` 4) at −1.18672 ducats. No province reaches
`0.02 × unrest > 1`, so no tax term is clamped. Under the history-integer reading the figure would be
**8.64 ducats, 0.0815%**.

### V04 — `Φ_w` edge flips caused by admitting `unrest`

**Proposed 0. Measured 0.** Agree — and this is the row the proposal flags, so it was measured twice.

Rebuilt the wealth vector with `tax = base_tax · (1 − 0.02·unrest)` and re-ran `drain.py` on
`b_w = 1/N − c_w` at `α_Φ = 1.5`:

- save reading (21 provinces, fractional): wealth delta −12.230680, **0 flips**, sinks `['english_channel', 'hangzhou']` — unchanged.
- history reading (16 provinces, integers): wealth delta −8.64, **0 flips**, sinks unchanged.

So the fidelity correction moves no arrow on either reading of the input. Nothing about the
orientation depends on which source the values come from.

### V05 — LP objective, identity permutation

**Proposed 0.712275977829. Measured 0.7122759778293255.** Agree; that prints as `0.712275977829`
at twelve decimals.

Measured two independent ways, which is the check that matters here:

1. An independently written Phase-2 LP (318 arcs, `A_eq` divergence rows, `linprog(method="highs")`, unit costs) → `0.7122759778293255`, support 79 arcs.
2. `drain.py`'s own `phase2()` on the same `b_w` → cost `0.712275977829`, and the total |flow| on its 79 flow arcs is the same value. Core 80, 79 flow arcs, 80 free edges.

`relabel6.py` prints the same figure from its own `lp_objective()`.

### V06 — LP objective, max relative deviation under relabelling

**Proposed 6.235e-16 over 40 permutations. Measured 6.2348e-16 at the seed `relabel6.py` hardcodes
(20260821) — but this is the *same measurement* as the "now" figure 4.44e-16, in different units, and
it moves under reseeding.** This is the one row where the numbers agree and the row still misleads.

`ulp(0.7122759778293255) = 1.1102230246251565e-16`. At seed 20260821 the maximum *absolute*
deviation over 40 permutations is **4.4409e-16 = exactly 4 ULP**; divided by the objective that is
**6.2348e-16**. The spec's current 4.44e-16 is the absolute form and round four's own pass measured
it as "4.4409e-16 exactly, in all three runs". So replacing 4.44e-16 with 6.235e-16 changes the
normalisation, not the finding.

Reseeding, 40 permutations each (my own LP, not `relabel6.py`'s):

| seed | max abs | ULP | max rel |
|---|---|---|---|
| 20260821 | 4.4409e-16 | 4 | 6.2348e-16 |
| 1, 3, 7, 4242, 20250821 | 4.4409e-16 | 4 | 6.2348e-16 |
| 2, 999 | 5.5511e-16 | 5 | 7.7935e-16 |

At 200 permutations per seed it grows again: 6.6613e-16 abs / 9.3522e-16 rel (seeds 11, 13) and
7.7716e-16 abs / 1.0911e-15 rel (seed 12). It is a sample maximum over a discrete ULP ladder, so it
increases with trial count and is not a bound. The safe form is the one Y086 already reached — a few
units in the last place — with the unit named.

### V07 — permutations returning a different optimal support

**Proposed 40 of 40. Measured 40 of 40 at every seed tried.** Agree, and this one is stable.

40/40 at seeds 20260821, 1, 2, 3, 7, 999, 4242, 20250821; 200/200 at seeds 11, 12, 13. The support
is 79 arcs and the symmetric difference against the identity support averages ~23 arcs (range
10–36), so these are substantially different vertices, not marginal ones.

### V08 — distinct numeric figures the spec prints

**Proposed 303. Measured 286.** **Do not agree.**

The source of the 303 is `validation-v6.md:217`, which states five figures in one sentence: 1,148
numeric tokens, 303 distinct, 483 decimal-bearing, 163 distinct decimals, 70 percentages, 41 distinct
percentages. The tokenisation `(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])` on the frozen spec reproduces
**four of the five exactly** — total **1,148**, decimal-bearing **483** / distinct **163**,
percentages **70** / distinct **41** — and gives **286** distinct, not 303.

Sweeping 62 tokenisations (optional sign, optional trailing `%`, single- vs multi-dot, optional
e-notation, two left and two right boundary rules) the distinct count ranges **279 to 326** and the
total ranges 1,050 to 1,244. **No tokenisation produces 1,148 total and 303 distinct together**; the
only one giving 303 has a total of 1,057. Values as floats rather than as printed strings give 246.

So the quantity is not 303, and more importantly it is not defined: "distinct numeric figure" has no
operational meaning in the document, and the answer swings by ±8% on choices as small as whether
`1.37.5.0` is one token or two and whether `53.6%` is the same figure as `53.6`. This is a poor
candidate for a "directly checkable count" (see T07).

### V09 — distinct numeric figures `verify6.py` pins

**Proposed 35, across 29 checks. Measured 35 across 29 checks.** Agree.

Ran `verify6.py` against the frozen spec inside the scratch copy of the tree:
**`RESULT: 29 checks, 0 failed`**. Extracting the numbers from the needles each check builds:

- distinct numeric **values** across all 29 checks: **35**
- distinct numeric **strings** as printed: **38** (this is validation-v6's "roughly 38")
- distinct values over the 27 value-pinning checks alone, excluding the numbers inside the three
  `absent()` needles (60.3, 97, 13): **32**

So 35 is exact under the natural reading of the row as written ("across 29 checks"). Worth knowing
that three of the 35 come from needles the harness requires to be *absent* rather than figures it
pins to a computed value; if the row is meant to count only what is pinned, it is 32.

The 32 pinned values: 0.0225, 0.25, 1, 1.38, 1.63, 1.71, 2, 3, 3.50, 3.72, 5.21, 6, 8, 10, 13.40,
15, 44, 52.3, 53.6, 75, 89.6, 93, 132, 159, 161, 214.60, 824, 1821, 2472, 5663, 6320, 10607.40.

### V10 — `Φ_ord` ends terminating no good

**Proposed 7 of 14. Measured 7 of 14.** Agree, and exactly half.

`Φ_ord = Σ_g V_g · order_g` over the 29 live goods, orders taken from `run_drain`'s own marking order
per good (core = 80, so every node has one), `V_g = price(g) · Σ_m goods_produced(m,g)`. Edges
oriented by descending `Φ_ord`: 0 exact ties across an edge, 159/159 oriented, acyclic, **14 ends**
and 4 sources.

Ends: `amazonas_node, australia, basra, chengdu, james_bay, katsina, laplata, philippines, ragusa,
rheinland, rio_grande, safi, white_sea, yumen`.

The **seven** that are a sink for no good: `amazonas_node, basra, chengdu, james_bay, ragusa,
rio_grande, yumen`. The other seven terminate between 1 and 9 goods. Self-coherence with the per-good
graphs is **60.36%**, matching the figure Y092 reports, so the object measured here is the same one.

### V11 — `NEW_DRAPERIES` single-event floor for `wool`

**Proposed 1.875. Measured 1.875.** Agree arithmetically, with a provenance correction.

`wool` base price **2.5** (`common/prices/00_prices.txt:14-16`). The install carries eight
`change_price` entries for `wool`, four in `events/PriceChanges.txt` and four in
`history/countries/HAB - Austria.txt`:

| value | key | file |
|---|---|---|
| −0.25 | `NEW_DRAPERIES` | `history/countries/HAB - Austria.txt:316` |
| −0.20 | `NEW_DRAPERIES` | `events/PriceChanges.txt:792` (event `prices.13`) |
| −0.10 | `COTTON_IMPORTS` | `events/PriceChanges.txt:358` (event `prices.6`) |
| −0.10 | `COTTON_IMPORTS` | `history/countries/HAB - Austria.txt:298` |
| +0.10 / +0.10 | `REGULATED_UNIFORMS` | events / history |
| +0.35 / +0.25 | `SELECTIVE_BREEDING` | events / history |

2.5 × (1 − 0.25) = **1.875**. But the −0.25 is the *history file's* value; the event that bears the
name `NEW_DRAPERIES` applies **−0.20**, so the floor from the event alone is **2.00** exactly.
Calling 1.875 "the `NEW_DRAPERIES` single-event floor" is true of the key and false of the event.

The parenthetical checks out: the 13/2/4/11 partition reproduces exactly (below 13, exactly-2.0 2,
above 4, no-negative 11 — the two on the anchor being `gems` and `silk`), and it **does** require the
history value. Dropping `history/` from the census moves `wool` from "below" to "exactly on the
anchor" and the partition becomes **12/3/4/11**.

### V12 — `wool` in a campaign reaching 1540

**Proposed between 1.625 and 1.6875, composition rule unknown. Both bounds measured exactly; the
"unknown" is confirmed; but which pair of values applies is a scope question the files do not
settle.** Agree on the arithmetic and on the premise.

The two live negative keys at 1540 are `NEW_DRAPERIES` −0.25 and `COTTON_IMPORTS` −0.10, both
`duration = -1`, both inside the **`1540.1.1 = {`** block of `history/countries/HAB - Austria.txt`
(block opens at line 290; the two entries at lines 295–299 and 313–317). On those values:

- additive: 2.5 × (1 − 0.25 − 0.10) = **1.625**
- multiplicative: 2.5 × 0.75 × 0.90 = **1.6875**

**The premise the proposal asks to be tested holds: no readable save in the install carries a good
with two live keys.** Checked every readable save on this machine:

- `VANILLA_start.eu4` — `change_price={ … }` gives `current_price` per good with no key list; every one of the 32 goods sits at its base price.
- the eight shipped text saves `tutorial/eu4_tutorial_chapter*.eu4` (dates 1444.12.1 – 1492.2.6) — five have every good at base; the three at 1492 have exactly two goods off base, `gems` 4.0 → **5.000** and `paper` 3.5 → **4.375**, both ×1.25 and both explicable by a *single* +0.25 key (`gems` has only two keys in the whole install, `FACETING` +0.25 and `BRAZILIAN_DIAMONDS` −0.5, and no combination of `paper`'s keys other than one +0.25 gives ×1.25).

A single key composes identically under both rules, so nothing here separates them. The 16 remaining
readable saves are ironman `EU4bin` from versions 1.24–1.35 and are not usable for this. **So the
composition rule cannot be settled from files, saves, or code, and should be stated as unknown.**

**One scope caveat on "a campaign reaching 1540".** Both keys become live *through a country-history
dated block*, which builds the start state for a game begun at or after 1540.1.1. Whether a campaign
begun in 1444 and played to 1540 ever applies that block is a question about the engine, not about
the files; if it does not, the two keys live at 1540 in such a campaign are the *event* values −0.20
and −0.10, giving **1.75** (additive) and **1.80** (multiplicative). Both of the proposed bounds
presuppose the −0.25. I cannot settle which reading is right without a running game, and say so
rather than picking one.

---

## The statements

### T01 — `unrest` is a fifth province-state modifier, and its scaling is stated in the file

**Confirmed.** `common/static_modifiers/00_static_modifiers.txt`:

- `unrest = {` at line **487**, closing at **491**; `regiment_recruit_speed = 0.1   #10% longer time to build troops for each rr` at **488**, `ship_recruit_speed = 0.1` at **489**, `local_tax_modifier = -0.02` at **490**.
- `nationalism = {` at **493**–**495**, with `local_unrest = 0.5   #for each year revolt risk!`.

So `local_tax_modifier = -0.02` is there verbatim, the "for each rr" convention is there verbatim,
and `nationalism` uses the same convention two lines below. `unrest` describes province state and is
not among §1.3's four (`devastation`, `prosperity`, `under_siege`, `occupied`), so "fifth" is right.

*One interpretive step to flag:* the "for each rr" comment sits on `regiment_recruit_speed`, not on
`local_tax_modifier` and not on the block header. Reading it as governing the block is an inference —
a well-supported one, since a per-key scaling law would be incoherent inside a single static
modifier, but the file does not say "each key in this block" anywhere.

### T02 — `devastation` is therefore the only unverified scaling law in §1.3

**Confirmed as scoped.** §1.3's modifier table (spec lines 262–267) applies a scaling law to exactly
one entry: `devastation`, "`trade_goods_size_modifier = -2`, scaled by the devastation level", with
its own row flagging `-2 × level/100` as an assumption rather than a file value. `prosperity`,
`under_siege` and `occupied` are stated as flat grants with no scaling law at all, and all three are
inert on the 1444 field (`solver.province_table` applies only devastation). The `devastation` block
is at lines **453–462** of `00_static_modifiers.txt` and carries **no comment of any kind**, while
the convention exists 25 lines below it. So admitting `unrest` with a file-sourced per-point law
leaves `devastation` as the only scaling law in §1.3 that no file states.

*Caveat, not a contradiction:* in the engine `prosperity` is also a 0–100 level, so §1.3's flat
reading of it is an unstated modelling choice as well. It is not an *unverified scaling law* in §1.3
because §1.3 asserts no scaling law for it — the claim holds as worded, and would not hold if
reworded to "the only province-state modifier whose real scaling is unstated".

### T03 — the 580-of-580 sweep is real and its script is in the tree

**Confirmed.** `python ../v5-owner-agnostic/scripts/_audit_b_1444perm.py`:

```
sanity: goods where the independent impl disagrees with drain.py: 0 /29
1444, 29 goods x 20 full node relabellings = 580 runs
  orientation changed            : 580
     ...with the SAME LP support : 0
     ...with a DIFFERENT support : 580
  Phi_w: 20/20 relabellings changed the orientation (same-support: 0)
```

29 × 20 = 580, orientation changed 580 of 580, every one by a different LP vertex and none by a
sweep tiebreak. The spec's ground for withdrawing it (line 918: "whose scripts were never shipped")
is false for this half.

**Two things the proposed correction does not cover.** First, the arc-permutation half of that same
sentence *is* correct — no script in any tree computes it — so the sentence cannot simply be
reversed. Second, its other premise is also false and T03 does not mention it: "580" has **zero**
hits in all five v1–v5 spec files. It appears only in `../v5-owner-agnostic/fixes-agreed.md` and
`../v5-owner-agnostic/scripts/_audit_parts/partB.md`, so "*Earlier versions* quoted" is wrong in the
same sentence in which "never shipped" is wrong.

### T04 — §3.9's figure and its history

**Half confirmed, half wrong.** **Do not agree.**

Confirmed: the v6.0 field gives **7 of 14** (V10), 7/14 is **exactly** half, so "a majority" is false
and the previous round's fix and this one genuinely cannot both be taken. Confirmed: the numerator
history is 9 → 10 → 8 → 7 —

| version | line | ends | terminate no good |
|---|---|---|---|
| v2 | 681–682 | **18** | 9 |
| v3.0 | 957–958 | **18** | 9 |
| v4.0 | 1047–1048 | **18** | 10 |
| v5.0 | 1174–1175 | **13** | 8 |
| v6.0 | 1365 | **14** | 7 |

**Wrong:** "while the end count moved 13 → 14". The end count moved **18 → 13 → 14**. It stood at 18
for three versions, so the denominator has moved further and earlier than T04 says, and the
fractions were 9/18, 9/18, 10/18, 8/13, 7/14 — which also means the earlier ones were *not* all
majorities (9/18 is exactly half, twice). Any sentence built on "the fractions were all majorities
before" is unsafe; a bound of the form "at least half" is true at all five.

### T05 — no basin figure is quotable

**The conclusion holds. Both figures offered in support of it do not.** **Do not agree.**

Shipped ordering, `drain.py` direct, basin = nodes with a directed path to `english_channel`,
counting the node itself, scanned at every 0.01 from ×1.00 to ×2.00:

- ×1.00 → **18** (matches the "shipped 18")
- ×1.44 → **28**
- ×1.53 and ×1.54 → **33**, the maximum over the whole scan (matches the "shipped 33")
- `english_channel` holds an end up to ×1.63; `genua` first holds an end at **×1.63** and is the **sole** end contiguously from **×1.64** through **×2.00**
- the sequence 18, 19, 18 … 21, 24, 27, 24, 23, 31, 28 … 33, 26 has **7** direction changes, so "widens non-monotonically" is right and neither endpoint describes the path

Relabelled, seven independent sets of 60 through the validated five-phase instrument:

| factor | `english_channel` an end, per 60 | basin range per seed |
|---|---|---|
| ×1.00 | 16, 20, 22, 22, 23, 29, 34 | 17–62, 16–74, 16–32, 17–80, 16–63, 16–80, 17–66 |
| ×1.53 | 3, 3, 4, 4, 4, 7, 8 | 24–35, 26–28, 23–29, 26–33, 23–29, 24–33, 23–33 |

- **"the ×1.00 basin ranges 16–75"** — not reproducible. The lower end is stable (16 or 17 in all seven sets); the upper end is 32, 62, 63, 66, 74, 80, 80. Pooled over 420 relabellings: **16–80**. 75 is one draw's maximum.
- **"at ×1.53 the shipped 33 falls outside the 24–29 range the orderings produce"** — **refuted.** 33 is *inside* the relabelled range in three of the seven sets, and pooled over 420 relabellings the range is **23–35** and contains 33. The reason one draw produced 24–29 is visible in the table: at ×1.53 `english_channel` holds an end in only 3–8 of 60 trials, so each "range" is the min and max of three to eight observations.

So the sentence T05 proposes to write is the right sentence — the basin is not quotable — but the two
specific figures it advances as evidence are themselves single draws, which is the defect the
proposal is trying to remove. The claim that survives reseeding is: on the shipped ordering the basin
is 18 at ×1.00 and non-monotone thereafter, peaking at 33 near ×1.53; under relabelling the size
spans 16–80 at ×1.00 and 23–35 at ×1.53, and `english_channel` holds an end in only about a third of
orderings at ×1.00 and under a sixth at ×1.53. The parts of §1.6 T05 wants to keep — non-monotone
widening, and the migration to `genua` — both measure out.

### T06 — basin size belongs on §1.6's conditional list

**Confirmed, on both halves.** §1.6's split currently reads "Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, and which European node holds an
end in the table below." Basin size is not named there or anywhere else in the section, and §1.6 does
print basin figures ("the Channel's basin grows from 18 nodes to 28 by about ×1.44"). And it is
ordering-conditional by a wide margin: 16–80 against a shipped 18 at ×1.00. So the omission is real
and the addition is warranted.

### T07 — replace the ratio with two checkable counts

**Partly confirmed; the two supporting facts split, and the "four times" is wrong.** **Do not agree.**

§0 line 47 currently reads "a script is named about a dozen times against roughly three times that
many unguarded figures". Of the two counts proposed to replace it:

- **35** pinned by the harness across 29 checks is exactly reproducible (V09) — a genuinely checkable count.
- **303** distinct figures printed is **not** reproducible and has no definition that makes it come out (V08: 286 under the tokenisation that reproduces all four companion figures, 279–326 across 62 tokenisations). Swapping an unmaintainable ratio for a count with an undefined denominator does not remove the maintenance problem; it relocates it.

**"The ratio has moved four times inside this version"** — I find **three** recorded edits to that
clause in `changes-v6.md`: entry **130** (`Y011`, §0) introduced "5 of 11 uniquely-locatable figures
are protected … roughly half of what is locatable is guarded"; entry **131** (`Y011b`, §0) replaced
it with "**Under half** of the figures it prints are guarded"; entry **135** (`T05`, §0, from
`scripts/r25.py:57`) added "about a dozen times against roughly three times that many unguarded
figures". Before entry 130 the clause carried no ratio at all. So it is three replacements / four
successive forms, and only three of those forms are ratios. The fourth §0 numeric edit nearby
(entry **119**, `Y003a`) changed a different quantity — the classifier's 105.30 ducats — and the two
other §0 entries in that stretch (68 `R19-r3`, 92 `S05a`) touch neither.

### T08 — `relabel6.py` computes the LP objective, and says so when it cannot

**Confirmed, both halves.**

The first half: `relabel6.py` contains `lp_objective(perm)` (lines 79–92), which builds Phase 2's LP
directly under each permutation with `scipy.optimize.linprog` and returns objective and support. Its
output block prints the three figures V05–V07 are drawn from:

```
LP degeneracy, measured on Phase 2 directly
  identity objective           : 0.712275977829
  max relative deviation       : 6.235e-16 over 40 permutations
  permutations with a different optimal support : 40 of 40
```

The second half: the per-trial objective it tries to lift out of the five-phase reimplementation
comes back empty, and the script prints exactly that rather than letting an attribution stand —

```
  LP objective deviation     : not available - the implementation exposes no flow map,
                               so no figure here may be attributed to this script
```

*Mechanism note.* The reimplementation *does* expose `flow_arc`, but as `{edge index: (u, v)}`, so
`sum(abs(v) for v in fa.values())` raises `TypeError` on a tuple and the bare `except` sets the value
to `None`. The disclosure is therefore reached by a swallowed exception rather than by a capability
check — the printed statement is true and the behaviour is the desired one, but it would also fire if
the extraction were merely buggy, which is a weaker guarantee than the sentence implies.

---

## What was not settleable

- **V12's composition rule.** No readable save on this machine carries a good with two live `change_price` keys; the only off-base prices in any readable save are two single-key ×1.25 cases at 1492. Stated as unknown above rather than estimated.
- **Whether a 1444 campaign ever applies `history/countries/HAB - Austria.txt`'s `1540.1.1` block.** This decides whether the pair of live values at 1540 is (−0.25, −0.10) → 1.625/1.6875 or (−0.20, −0.10) → 1.75/1.80. It is an engine-behaviour question and no file in the install answers it.
- **`devastation`'s proportionality**, unchanged from prior rounds: no file states it, and nothing here asserts it as measured.
