# Independent measurement of `fixes-round3.md`

Every value in `fixes-round3.md` — R01–R12 and T01–T07, 19 in all — computed or read from a primary
source by this pass. **Nothing in the specification, the claim inventory, the proposal file or any
existing script was modified.** Two files were added: `scripts/preconfirm3.py` (the measurement
script behind every numeric row here) and `scripts/preconfirm3-relabel.out` (its saved relabelling
output).

*One existing file was rewritten by a script rather than by me: `scripts/measure6.out` is written on
every import of `measure6.py`, so running `verify6.py`, `mutate6.py` and `coverage6.py` regenerated
it. The content came back identical to the copy that was on disk before this pass — same 60 labels,
same 60 values; only the mtime moved.*

**Primary sources.**

- Install: `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`, 1.37.5.0, Leviathan present.
- Save: `…\save games\VANILLA_start.eu4` → ZIP entry `gamestate`; province header at column 0, fields at two tabs.
- Reference implementation: `scripts/solver.py`, `scripts/drain.py`, `scripts/flowop.py`, `scripts/measure6.py`.
- Relabelling instrument: `../v5-owner-agnostic/scripts/_audit_b_drain.py`, a self-contained five-phase reimplementation parameterised by node order.
- Prior-version specs: `../v1-laplacian/`…`../v5-owner-agnostic/per-good-trade-spec.md`.
- Harness: `scripts/verify6.py`, `scripts/mutate6.py`, `scripts/coverage6.py`.

**One value needs a running game and did not get one:** R04's two tooltip readings (`Base: 0.49
(Yearly 6.00)` and `Base: 0.16 (Yearly 2.00)`). They are taken as given from the session record at
`../v3-owner-agnostic/validation-v3.md:179`; the *arithmetic* R04 asserts over them was checked here
and is settled without a game.

---

## Summary

| id | the spec says | measured | agree |
|---|---|---|---|
| R01 | max `base_tax` **15**, province 1821, total development 33 | 15.0, uniquely pid 1821; 15 + 15 + 3 = **33** | **yes** |
| R02 | razed-`hangzhou` edge flips **22** of 159 | **22** of 159 | **yes** |
| R03 | **105.30** ducats, 0.99% of 10,607.40, 0.98% of 10,712.70 | **105.30**; 0.9927% and 0.9829% of **10,607.40** / **10,712.70** | **yes** |
| R04 | `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)` | reproduces 0.49 and 0.16; `trunc(bt/12)` gives **0.50** at `base_tax` 6 | **yes**, two caveats |
| R05 | the 0.6125 attribution is **v4.0 and v5.0** | 0.6125 only in v4 spec:178 and v5 spec:185; v3 spec:158 says "giving 0.61" | **yes** |
| R06 | orientation changes **100 of 100** | **100/100**, at all five seeds (500/500) | **yes** |
| R07 | mean **26** of 159 edges move | **25.80** at the originating seed (24.45–25.80 over five seeds; pooled 25.10) | **yes** |
| R08 | baseline sink set returned **8 of 100** | **8/100** at the originating seed (5–12 over five seeds; pooled 44/500) | **yes**, sample-conditioned |
| R09 | `hangzhou` is an end **100 of 100** | **100/100** at the originating seed, but 97–100 elsewhere; pooled **494/500** | **yes as a sample**, no as a generalisation |
| R10 | `english_channel` is an end **40 of 100** | **40/100** at the originating seed (37–47; pooled 207/500 = 41.4%) | **yes** |
| R11 | `gulf_of_siam` 55, `wien` 37, `sevilla` 19 | **55, 37, 19** exactly, at the originating seed | **yes** |
| R12 | sink count 1 to 5, most often 2 | range **1–5** at every seed; mode **2** at three of five seeds and pooled | **yes**, weakly |
| T01 | `hangzhou` a world property, `english_channel` an ordering property; rest of §1.6 conditional | asymmetry confirmed (98.8% vs 41.4%); "rest of §1.6" true of four figures, false of four others | **yes**, qualified |
| T02 | the Europe table's direction is the claim, its membership is ordering-dependent | confirmed by measurement; the ×2.00 `genua` row is the exception — that membership *is* ordering-robust | **yes**, one over-reach |
| T03 | §2.4's end-flag list is a function of the node order | confirmed: 21–26 distinct sink sets per 100 relabellings, `english_channel` in ~41% | **yes**, one over-reach |
| T04 | §2.8's razed-China row is ordering-**robust** | confirmed, and more strongly than the stated reason: 300/300 relabellings relocate an end | **yes** |
| T05 | `verify6.py` under-covers; `mutate6.py` cannot fail | first and last clauses confirmed; "the rest rest on their script attribution alone" is overstated | **partial** |
| T06 | §3.15 keeps no copy of the contrast figures or RANK's stranded share | confirmed; §3.15's contrast numbers appear only as a quoted retraction | **yes**, note |
| T07 | §3.10 quotes no magnitude of its own for the per-good propagation error | confirmed | **yes** |

**Count: 19 values checked. 12 of 12 R-rows reproduce. 6 of 7 T-rows hold; T05 holds in two of its
three clauses. Two figures are true as stated but invite a generalisation that is false — R09 and,
downstream of it, §2.4 item 2's "under every ordering tried".**

---

## R01 — max `base_tax` 15, province 1821, total development 33

**Agree.** Over the 2,472 counted provinces (owner present and in a trade node, `solver.py`'s rule),
`max base_tax = 15.0`, reached at **exactly one** province, **1821**. That province is *Nanjing*, not
Beijing: `history/provinces/1821 - Nanjing.txt`. Its development is `base_tax` 15 + `base_production`
15 + `base_manpower` 3 = **33**, and 33 is also the maximum total development over the counted set
(next: 1816 at 31, 116 at 28).

Read from the save rather than from the parse: the `gamestate` record `-1821={` carries
`base_tax=15.000`, `base_production=15.000`, `base_manpower=3.000` (and, incidentally,
`original_tax=33.000`). A sweep of every counted province's record in `gamestate` gives the same top
four — `(15.0, 33.0, 1821), (13.0, 31.0, 1816), (12.0, 27.0, 684), (12.0, 27.0, 667)`.

*The superseded "runs up to 33" (introduced by `scripts/r21.py`, edit N14) conflated total
development with `base_tax`. 33 is the development at 1821; 15 is its `base_tax`.*

*Source:* `python scripts/preconfirm3.py a`; save `gamestate`; `scripts/prov1444.json`.

## R02 — razed-`hangzhou` edge flips, 22 of 159

**Agree: 22.** On the v6.0 field with `α_Φ = 1.5`, `b_w = 1/N − c_w`:

```
baseline sinks   ['english_channel', 'hangzhou']                 159/159 oriented
zero hangzhou    ['doab', 'english_channel', 'gulf_of_siam']     22 flips   node wealth 226.7
zero beijing     ['english_channel', 'hangzhou']                 15 flips   node wealth 143.0
```

Every adjacent figure in the same §2.8 row also reproduces: the razed sink set, the 15 flips for
`beijing`, and the 226.7-against-143.0 node wealths. *The previous value 23 does not reproduce on
this field.*

*Source:* `python scripts/preconfirm3.py b` — `run_drain` from `scripts/drain.py` on the wealth field
of `scripts/solver.py`.

## R03 — the deleted apparatus: 105.30 ducats, 0.99% / 0.98%

**Agree on all four numbers.** v5.0's apparatus reconstructed verbatim from
`../v5-owner-agnostic/scripts/solver.py:59-73` (`gems local_tax_modifier 0.15`, `incense
trade_value_modifier 0.10`, five `MON_FLAT`, one `MON_GPMOD`, four `MON_TVMOD`, ten `PERM_FLAT`) and
applied on top of the v6.0 province table:

```
apparatus off   10,607.40      (= measure6.out's "world wealth")
apparatus on    10,712.70
delta              105.30      0.9927% of the off total   ->  0.99%
                              0.9829% of the on total    ->  0.98%
touched                89      = 43 gems + 31 incense + 16 project/permanent - 1 overlap (pid 542)
```

*Source:* `python scripts/preconfirm3.py c`.

## R04 — `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`

**Agree.** As arithmetic:

```
base_tax 6    trunc(6 x 0.0833333) = 0.49      trunc(6 / 12) = 0.50
base_tax 2    trunc(2 x 0.0833333) = 0.16      trunc(2 / 12) = 0.16
```

So the adopted schema reproduces both recorded readings and the `/12` form fails at `base_tax` 6,
exactly as the "was" column says. Two caveats, neither of which changes the row:

1. **The multiplier is not pinned by the data.** Any `m` with `trunc(6m) = 0.49` and
   `trunc(2m) = 0.16` satisfies `m ∈ [0.0816667, 0.0833333)`. `0.0833333` is inside it; `1/12 =
   0.08333333…` is not, which is precisely why the two forms differ. No file in the install supplies
   the constant — `grep -rl "0\.0833" common/` returns nothing and `common/defines.lua` carries no
   monthly-tax constant — consistent with §2.3's statement that `TAX_COEFF` is measured, not read.
2. **The two tooltip readings themselves cannot be re-observed without a running game.** They are on
   record at `../v3-owner-agnostic/validation-v3.md:179`.

*Side note, unasked but adjacent:* `0.49 × 1.25 = 0.6125` truncates **and** rounds to 0.61, so the
observed 0.62 needs neither rule — it needs the untruncated `0.625`. §1.3's parenthetical is right
that "both cannot hold", and the stronger statement is that 0.6125 cannot produce 0.62 under either.

*Source:* `python scripts/preconfirm3.py d`.

## R05 — the 0.6125 attribution is v4.0 and v5.0

**Agree, both halves.** Grepping the five prior specs:

| | `0.6125` | `Base: X (Yearly 12·X)` | says |
|---|---|---|---|
| `../v1-laplacian/per-good-trade-spec.md` | absent | absent | — |
| `../v2-drain/per-good-trade-spec.md` | absent | absent | — |
| `../v3-owner-agnostic/per-good-trade-spec.md` | absent | absent | line 158: "**giving 0.61**" |
| `../v4-owner-agnostic/per-good-trade-spec.md` | line 178 | line 163 | "giving 0.6125, which the province window shows as 0.62" |
| `../v5-owner-agnostic/per-good-trade-spec.md` | line 185 | line 170 | same |

v3.0's claim inventory carries the same reading — `../v3-owner-agnostic/claims-v3.md:344`, W038,
"`Base 0.49` then `Tax Income Efficiency 125.0%`, giving 0.61". So "v3.0 through v5.0" was wrong on
both the arithmetic and the schema, and "v4.0 and v5.0" is right.

*Source:* `grep -n "0\.6125\|Yearly" */per-good-trade-spec.md`.

---

## R06–R12 — the relabelling rows

### The instrument, validated first

`drain.py` binds `N`, `ORDER`, `NIDX`, `UND`, `EDGES_UND` and `NODEW` into module state at import,
so it cannot be relabelled in place. I used `../v5-owner-agnostic/scripts/_audit_b_drain.py` —
peel, HHI-adaptive Phase 1, LP Phase 2, priority sweep with both the promotion and the fallback
branch, Phase 4 un-peel, all parameterised by node order.

**Validation on the identity permutation, on `Φ_w`, is exactly what `fixes-round3.md` asks for and it
passes on every count:**

```
drain.py    core 80  edges 159/159  promotions 2  fallbacks 0  sinks ['english_channel','hangzhou']
instrument  core 80  edges 159/159  promotions 2  fallbacks 0  sinks ['english_channel','hangzhou']
edges agreeing 159 of 159 ; orientation sets identical True
```

Two further checks, both confirming the file's own method warnings:

- **The LP objective does not move.** `sum |net|` = 0.712275977829 at the shipped order, and the
  maximum absolute difference over 30 relabellings is **2.22e-16**. The orientation moves by
  returning a different vertex of the same degenerate optimal face, not a different optimum.
- **`drain.py`'s `sweep_priority(pid=…)` hook sees none of it.** Run 30 times with a permuted `pid`
  map it changed the orientation **0 of 30** times and returned `{english_channel, hangzhou}` 30 of
  30. A test built on that hook would report perfect stability, exactly as `fixes-round3.md` warns.

**Protocol.** For a permutation `p`: rebuild the edge list as `sorted(set(tuple(sorted((p[u],
p[v])))))`, scatter `b_w`, `NODEW` and the names into the new labelling, run the full pipeline,
invert with `inv[p[i]] = i`, and only then compare orientations and sink sets. `α_Φ = 1.5` and the
wealth field untouched throughout. 100 trials per seed, five seeds, `numpy.random.default_rng`.

### Results

```
                                       seed 4242  seed 7  seed 999  seed 1  seed 20250821   pooled
R06 orientation changed                  100/100  100/100  100/100  100/100   100/100      500/500
R07 mean edges moving (of 159)             25.80    24.45    25.64    24.94     24.69         25.10
R08 returns {english_channel,hangzhou}       8        9        5       12        10           44/500
R09 hangzhou is an end                     100       99       97      100        98          494/500
R10 english_channel is an end               40       37       44       47        39          207/500
R12 sink-count mode (range 1-5 always)       2        3        3        2         2            2
    distinct sink sets                      22       26       22       21        26
    fallbacks fired                          0        0        0        0         0            0
R11 gulf_of_siam                            55       48       63       58        52          276
    wien                                    37       30       35       34        29          165
    sevilla                                 19       18       16       14        10           77
    rheinland                               12       16       14       13        16           71
    champagne                               10        6        9        9        10           44
    ganges_delta                             1        3        2        2         5           13
    genua                                    2        3        1        0         3            9
```

**Seed 4242 reproduces the spec's figures exactly** — R08 = 8, R09 = 100, R10 = 40, R11 = 55/37/19,
R12 mode 2, and R07 = 25.80 which is 26 to the nearest edge. The spec's numbers therefore came from
this protocol at this seed, and the arithmetic behind them is confirmed. Row by row:

- **R06 (100 of 100)** — **agrees and is seed-robust.** 500 of 500.
- **R07 (mean 26)** — **agrees.** 25.80 at seed 4242; the five-seed spread is 24.45–25.80 and the
  pooled mean is 25.10, so "26" is the top of the range. "About 25" would be the seed-independent
  form.
- **R08 (8 of 100)** — **agrees at seed 4242**; the quantity is a sample proportion, 5–12 per 100
  over five seeds, 8.8% pooled.
- **R09 (100 of 100)** — **agrees as a statement about one 100-run sample, and does not generalise.**
  Four of my five seeds produce a counterexample; there are **6 orderings in 500** where `hangzhou`
  holds no end. This is the one row where the figure as written reads as an exceptionless property,
  and §2.4 item 2's derived wording — "`hangzhou` is an end under **every ordering tried**" — is
  false once more than one seed is tried. The honest figure is **98.8%**, and it is still a strong
  asymmetry against `english_channel`'s 41.4%.
- **R10 (40 of 100)** — **agrees.** 37–47 over five seeds, 41.4% pooled; §2.4's "about 40%" is the
  seed-independent form and is right.
- **R11 (`gulf_of_siam` 55, `wien` 37, `sevilla` 19)** — **agrees exactly at seed 4242.** Worth
  noting that the same run has `rheinland` at 12 and `champagne` at 10, so `sevilla` 19 is not much
  above the nodes the sentence omits, and nine nodes hold an end at least once.
- **R12 (1 to 5, most often 2)** — **range agrees at every seed.** "Most often 2" holds at seeds
  4242, 7 and 20250821 and pooled (172 of 500 against 152 at three), and fails at seeds 999 and 1
  where the mode is 3. It is a weak plurality, not a robust mode.

*Source:* `python scripts/preconfirm3.py relabel`, saved at `scripts/preconfirm3-relabel.out`.

---

## T01 — one end is a world property, the other an ordering property; the rest of §1.6 is conditional

**Holds, with two qualifications.**

*The asymmetry is real and large.* `hangzhou` 494/500 (98.8%), `english_channel` 207/500 (41.4%).
But "a property of the world" is 98.8%, not exceptionless — see R09.

*"The rest of §1.6 is conditional on one canonical node order" is true of some of §1.6's figures and
false of others.* Measured over 60 relabellings at seed 4242:

| §1.6 figure | shipped order | over 60 relabellings |
|---|---|---|
| sink set | `{english_channel, hangzhou}` | 22 distinct sets; returned 8 times per 100 | 
| sources | **8** | 4–12; 8 in only 13 of 60 |
| source `c_w` rank range | **44–75** | 21 distinct ranges, envelope 43–79 |
| promotions | **2** | 1–5 |
| fallbacks | **0** | 0 in 60 of 60 — **invariant** |
| Phase-1 selection | `{genua}` | `{genua}` in 60 of 60 — **invariant** |
| edges oriented | 159/159 | 159/159 in 60 of 60 — **invariant** |
| acyclic | yes | yes in 60 of 60 — **invariant** |

So the sink set, the source count, the source rank range and the promotion count are all
order-conditional; Phase 1's selection, the zero fallbacks, the full orientation and acyclicity are
not, and are properties of the world alone. (`largest |b_w| = 0.0225`, the `c_w` ranks and the α-band
table are functions of the input field, so they cannot move under relabelling either.) The blanket
"read the rest of this section as conditional" over-covers.

*Source:* `python scripts/preconfirm3.py relabel` plus the §1.6-figure sweep in the same protocol.

## T02 — the Europe table's direction is the claim, its membership is not

**Holds as a measurement, with one over-reach.** 60 relabellings per factor, seed 4242, European
provinces from `map/continent.txt` (824 counted, matching `measure6.out`):

| European development | shipped order | mean non-European ends | Asia holds none | European end holders |
|---|---|---|---|---|
| ×1.00 | `english_channel`, `hangzhou` | 1.62 | 0/60 | `english_channel` 26, `wien` 22, `sevilla` 10 |
| ×1.02 | + `wien` | 1.37 | 0/60 | `wien` 32, `english_channel` 24, `sevilla` 12 |
| ×1.56 | `english_channel`, `rheinland` | 0.53 | 32/60 | `genua` 23, `rheinland` 23, `english_channel` 8 |
| ×2.00 | `genua` alone | 0.00 | 60/60 | `genua` 60, `rheinland` 12, `wien` 3 |

**The direction survives relabelling cleanly** — non-European ends fall monotonically 1.62 → 1.37 →
0.53 → 0.00, and by ×2.00 no ordering leaves Asia an end. **Membership is ordering-dependent at
×1.02 and ×1.56**, and strikingly so at ×1.56, where the shipped order's `english_channel` holds an
end in only 8 of 60 while `genua` and `rheinland` hold one in 23 each.

*The over-reach:* the spec lists `genua` at ×2.00 alongside the other two as "this ordering's
answers, not the world's". At ×2.00 `genua` holds an end in **60 of 60** and is the sole sink in 45
of 60. That row's membership is ordering-robust, and the sentence understates it.

*Source:* `python -c "import preconfirm3; preconfirm3.section_f()"`.

## T03 — §2.4's end-flag list is a function of the node order

**Holds.** §2.4 item 2 emits `end=yes` on every `Φ_w` sink, so the flag list *is* the sink set, and
the sink set takes 21–26 distinct values per 100 relabellings with `english_channel` present in only
~41% of them and the count ranging 1 to 5. Changing the order changes the emitted flags with nothing
in the world changing, which is what item 2 says.

One correction inside the same item: "on the 1444 field `hangzhou` is an end under **every ordering
tried**" is the R09 over-reach restated. 6 of 500 orderings are counterexamples. "About 40%" for
`english_channel` in the same sentence is correct (41.4%).

*Source:* as R06–R12, plus `per-good-trade-spec.md:921-928`.

## T04 — §2.8's razed-China row is ordering-robust

**Holds, and by a stronger route than the stated reason.** The same permutation applied to both the
baseline and the razed field, 100 trials at each of three seeds:

```
                                          seed 4242   seed 999   seed 7
hangzhou an end, baseline field             100/100     97/100    99/100
hangzhou an end, razed field                  0/100      0/100     0/100
sink set differs baseline vs razed          100/100    100/100   100/100
hangzhou held an end and then lost it       100/100     97/100    99/100
mean edge flips baseline -> razed              24.0       26.4      24.5
```

The row's content — zeroing `hangzhou`-node development relocates an end — holds in **300 of 300**
relabellings, including the handful where `hangzhou` was not a baseline end (the sink set still
moves). So the row is ordering-robust; the stated *reason* ("it turns on `hangzhou` holding an end")
is 98.8% rather than exceptionless, but the conclusion it supports is stronger than the reason.

*Source:* `python -c "import preconfirm3; preconfirm3.section_f()"` and the seed sweep beside it.

## T05 — `verify6.py` under-covers, `mutate6.py` cannot fail

**Two of three clauses confirmed; the middle one is overstated.**

*"does not cover every figure the document prints"* — **true.** `python coverage6.py`: 60 computed
figures, 10 uniquely locatable in the spec, **8 caught / 2 missed** (`ordered pairs connected` — the
6,320 denominator; `goods with more than one producer` — 28), and **23 further figures unscored**
because their rendering appears more than once in the document.

*"**Under half** of the figures it prints are guarded"* — **true on every denominator I can build.**
21 of the 60 labels `measure6.py` computes are referenced by `verify6.py` (35%); adding its
literal-anchored spec checks (devastation cost 13.40, max `base_tax` 15 at pid 1821, `change_price by
tree` 93) reaches about 24 of 60 (40%). `verify6.py ../per-good-trade-spec.md` runs **29 checks, 0
failed** — 21 value-bearing and 8 absence checks.

*"and the rest rest on their script attribution alone"* — **overstated.** The spec names a script 12
times in total (`measure6.py` ×7, `verify6.py` ×2, `europe.py`, `toys.py`, `pdx.py` ×1 each), against
roughly 36 unguarded figures. Several of the figures this very round introduces carry neither a guard
nor an attribution: §1.3's 105.30 / 0.99% / 10,712.70 / 89, the whole of §1.6's relabelling paragraph
(100, 26, 8, 100, 40, 55, 37, 19, 1–5), and §2.8's 22 flips and 226.7-against-143.0 node wealths.
"The rest rest on their script attribution alone" should read something closer to "the rest are
unguarded, and only some of them name the script that produced them".

*"`mutate6.py` cannot fail, because it plants errors only in figures already checked"* — **true.**
`python mutate6.py ../per-good-trade-spec.md` caught **12 of 12** with **0 skips**, and each of its 12
anchors (world wealth, counted provinces, both self-coherence figures, sinks-per-good mean, connected
pairs, largest `|b_w|`, the α band, European provinces, coal flips, coal delta, price census) is a
quantity `run_spec` already checks with `shows()`. Its acceptance bar of 9 of 10 cannot be missed
while that stays true.

*One caveat about how the pair reads.* `coverage6.py`'s headline line is "coverage: 8 of 10
uniquely-locatable spec figures are protected (**80%**)", which points the opposite way from "under
half". They are different denominators — mutation-testable single-site figures against everything the
document prints — and only the docstring says so. Anyone quoting the 80% as coverage repeats, in a
new place, the confusion the entry exists to retire.

*Source:* `python verify6.py ../per-good-trade-spec.md`; `python coverage6.py`;
`python mutate6.py ../per-good-trade-spec.md`; `grep -o "O\[\"[^\"]*\"\]" verify6.py` against
`measure6.out`'s labels.

## T06 — §3.15 keeps no copy of the contrast figures or RANK's stranded share

**Holds, with a literal-presence note.**

- **RANK's stranded-demand share:** §3.15's ranked-orientation entry (`per-good-trade-spec.md:1526`)
  says only "a large share of world demand is stranded". No figure. The one measurement sits in
  §3.2 at line 1080 — "one sixth of world demand became unreachable" — and occurs **exactly once**
  in the document.
- **The supply/demand contrast:** the numerals *do* appear inside §3.15 at line 1510 — "supply
  contrast 10⁷ against demand contrast 10²–10³" — but only as a quoted attribution of what v1 and v2
  said, in the same sentence that retracts it and says "§3.2 carries the measurement, and this entry
  does not maintain a copy of it". That is the same convention `verify6.py`'s R2 checks apply (a
  quoted retraction is not an assertion), so "maintains no copy" is right in the sense that matters,
  and the sentence is not a figure the document owns.
- **What §3.2 actually holds for the contrast is a direction, not a magnitude:** "On the contrast
  metric itself the demand side is the wider one, not the supply side" (line 1100). No numeric
  contrast appears anywhere in the spec. The direction is independently correct on the current
  field — `measure6.out` gives supply contrast range **(4, 97)** against demand contrast **(211,
  15010)**.

So: both entries are directional in §3.15; §3.2 holds the one *measurement* for the stranded share
and the one *statement* for the contrast.

## T07 — §3.10 quotes no magnitude of its own for the per-good propagation error

**Holds.** §3.10 states it outright — "**No figure of my own is quoted here**, because the identity
holds and the objection is structural" — and every magnitude in the passage is attributed to a
superseded version: 5.96 ducats (v1 through v4.0), 0.41% (v4.0), "redistributive and single-digit
percent" (v5.0), "at most 0.1%" (v6.0's first draft). The two numbers §3.10 does own are **0 to
3.7e-16**, the floating-point residual of the income identity across five nodes, and **seven**
distinct downstream sets at `gulf_of_siam` — a residual and a count, neither of them a magnitude of
the per-good propagation error.

*Source:* `per-good-trade-spec.md:1368-1386`.

---

## What this pass would change in the document

Nothing here was edited. For the record, three items:

1. **§1.6's "`hangzhou` was an end in 100 of 100"** and **§2.4 item 2's "under every ordering
   tried"** — true of the one sample that produced them, false as generalisations (494/500 = 98.8%
   pooled over five seeds). Both would be safer as a percentage.
2. **§1.6's blanket "read the rest of this section as conditional on one canonical node order"** —
   over-covers: Phase 1's `{genua}`, the zero fallbacks, 159/159 and acyclicity are all
   order-invariant across 60 relabellings.
3. **§1.6's Europe table note** lists `genua` at ×2.00 among the ordering's answers; that membership
   is ordering-robust (60/60), unlike the ×1.02 and ×1.56 rows.
