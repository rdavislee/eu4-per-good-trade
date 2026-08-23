# Preconfirmation of `fixes-round6.md`

Every figure in `fixes-round6.md` measured independently from primary sources — the 1.37.5.0 install,
the mod's scripts, the four readable saves, and the frozen spec. Nothing was read out of
`measure6.out`, the validation reports, or any other cached artefact except where a cache was itself
the object under test.

**Spec MD5 at start:** `59c84a97799db9db97fe889b6e3c6776`
**Spec MD5 at finish:** `59c84a97799db9db97fe889b6e3c6776` — unchanged; nothing was applied.

`scripts/measure6.out` was re-generated and byte-compared against the copy on disk before it was
taken as a baseline: identical (`a0b376c07244605a86c098489730c55f`). Probe scripts were written to a
temp directory outside the tree; the only file any of them touched inside the tree was
`measure6.out`, restored identical.

Game version confirmed from `launcher-settings.json`: `v1.37.5.0`. scipy 1.18.0, numpy 2.4.6,
CPython 3.12.10.

---

## A. The wealth model

### A1 — CONFIRMED

**Method.** Read `common/static_modifiers/00_static_modifiers.txt` for the `unrest` block; read
§1.3 L220–225 of the frozen spec for the exclusion list the row proposes to join.

**Value.** The row states no figure. Its two factual premises hold. `unrest` grants
`local_tax_modifier = -0.02` (with the shipped comment `#10% longer time to build troops for each
rr`, so per point), which is what the §1.3 table says. The exclusion list exists at L222–223 and is
headed by autonomy: *"No autonomy, no production efficiency, no national ideas, no estate or
government modifiers, no technology."* Moving `unrest` there is coherent with that list's stated
criterion (owner-side terms), since revolt risk in play carries separatism, unaccepted culture and
nationalism — all owner relations. This is a design ruling, not a measurable quantity.

### A2 — CONFIRMED (and the retirement is better founded than the row claims)

**Method.** Parsed the `provinces={}` block of `VANILLA_start.eu4` for every province record's
`unrest` field; cross-referenced each against `history/provinces`, resolving the undated block plus
every dated block with date ≤ 1444.11.11, matching **both** the `unrest` and `revolt_risk` spellings.
Computed the wealth cost as `Σ TAX_COEFF·base_tax(p)·0.02·rr(p)` over counted provinces. Re-ran
DRAIN at α_Φ = 2.0 and 1.5 with unrest admitted to `tax_value` and diffed the edge sets.

**Value.** Six items, measured one at a time:

| item | spec says | measured | verdict |
|---|---|---|---|
| ducat cost, save values | 12.23, 0.115% | **12.2307, 0.1153%** | correct |
| ducat cost, "authored 16" | 9.40, 0.089% | **9.40 exactly** — but see below | arithmetically right, premise false |
| edges moved | 4 of 159 | **4 of 159** at α_Φ=2.0; **0** at α_Φ=1.5 | correct, incl. the parenthetical |
| sink set after admitting | `{genua, hangzhou}` unchanged | unchanged | correct |
| authored/runtime split | 16 authored / 5 runtime | **21 authored / 0 runtime** | **wrong** |
| "the other five are all Shirvan-owned" | 5 Shirvan, at runtime | **10** Shirvan-owned, **all authored** | **wrong** |

All 21 counted provinces carrying revolt risk at the start are authored in `history/provinces` at
integer 5/8/10/15 (save values are those integers minus 0.166). None receives its risk at runtime.

The 16/5 split is a **parsing artefact of spelling**, not of authoring: 16 of the 21 files spell it
`unrest`, and 5 spell it `revolt_risk` — and those 5 (`1071 Tara`, `1074 Sibir`, `1076 Kurgan`,
`4689 Om`, `4690 Ishim`) are all Shirvan-owned. A parser looking only for `unrest` finds 16 and
attributes the residue to runtime. That also explains 9.40 exactly: the 16 `unrest`-spelled
provinces at their authored integers cost 9.40, and the 5 `revolt_risk`-spelled ones cost
`0.02 × 15 × (2+2+3+2+1) = 3.00`, summing to 12.40 — the all-21 authored figure. So 12.23 (save
basis) and 9.40 (authored basis) are two different bases quoted as one comparison.

The Sofala citation is also unsound: `1186 - Sofala.txt` carries no revolt risk at 1444 at all. The
quoted comment *"expansion of Shona into Sofala region causes major disruptions"* sits on a
**1515.1.1** dated block, seventy-one years after the start date.

Retiring the lot is the right call.

### A3 — CONFIRMED

**Method.** Read `solver.py:145,148`.

**Value.** `tmod = 0.0` unconditionally, then `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)`. The
`(1 + Σ province-state tax modifiers)` factor is already an identity multiply, so
`tax_value(p) = TAX_COEFF · base_tax(p)` is exactly what the reference solver computes today.
Dropping the factor changes no computed value. Verified behaviourally: `r["tax"] ==
TAX_COEFF·base_tax(r)` on **2,472 of 2,472** counted provinces, 0 failures.

### A4 — CONFIRMED

**Method.** `grep -rn "STATE_TAX_MOD" scripts/ --include=*.py`, plus a grep of the spec.

**Value.** `STATE_TAX_MOD` is defined once (`solver.py:79`) and **read by nothing**. The only other
occurrences are in `v61n.py` and `v61r.py`, which are prose-editing scripts that merely quote its
name. The spec mentions it once, at L317. Setting it to `{}` therefore moves no number. (Contrast
`STATE_GOODS_MOD`, which *is* read — `solver.py:144` and `apparatus6.py:40`.)

### A5 — CONFIRMED, with one caveat on the site count

**Method.** Read the five `trade_goods_size_modifier` / `local_tax_modifier` blocks from
`00_static_modifiers.txt`. Parsed the start save for `prosperity`, `occupied`, `controller≠owner`
and for top-level war blocks. Counted spec sites with `grep -n unrest`.

**Value.**
- **Four rows all reaching `goods_produced`:** confirmed from the file. `devastation`
  (`trade_goods_size_modifier = -2`), `prosperity` (`+0.25`), `under_siege` (`-0.25`), `occupied`
  (`-0.5`). `occupied` also carries `local_tax_modifier = -0.5`, but with A3 dropping the tax factor
  its only live path is `goods_produced`, so "all four reach `goods_produced`" holds.
- **"On the 1444 start only `devastation` is live":** confirmed. `devastation > 0` on **11** counted
  provinces; `prosperity > 0` on **0**; the `occupied` flag on **0**; `controller ≠ owner` on only
  **3** provinces, all controlled by `REB`; and the save contains **zero** `active_war` blocks, so
  no siege can be in progress. (The `siege=` matches in the save are general siege pips inside
  `rebel_faction` blocks, not province sieges.)
- **"Eight sites edited":** the word `unrest` occurs at exactly **8** lines of the spec — 295, 301,
  305, 307, 308, 312, 327, 907. That is a clean match. Caveat: at least one further site carries the
  count without the word and would also need editing — **L1742** (§3.13, *"four of the five"*).
  L317 and L905 also carry counts but sit inside blocks that already contain `unrest`.

---

## B. The operator and its figures

### B1 — CONFIRMED (deletion is right; the paragraph is wrong by three orders of magnitude)

**Method.** Located the paragraph by `grep -n '^\*\*Scale\.\*\*'`. Re-ran DRAIN on `b_w` scaled by
10⁰ … 10⁻¹², at α_Φ = 2.0 and 1.5, diffing edge sets against the ×1 baseline.

**Value.** L487–497 is the correct deletion range: L488–497 is the paragraph and L487 the blank line
before it, so removing 487–497 leaves exactly one blank line between L486 and L498. §2.3's
cross-reference exists at L1025–1026 (*"See §1.6's scale-invariance note and §3.13"*) and would need
editing with it.

The paragraph's figures do not reproduce:

| claim | measured at α_Φ = 2.0 |
|---|---|
| identical orientation ×1 → ×10⁻² | identical ×1 → **×10⁻⁶** |
| **22** flips at ×10⁻⁴, sinks `{english_channel, hangzhou}` | 0 flips at ×10⁻⁴; **22** flips with exactly that sink set at **×10⁻⁷** |
| **96** flips at ×10⁻⁶, sinks `{hangzhou}` | 0 flips at ×10⁻⁶; **96** flips with exactly that sink set at **×10⁻⁹** |

The flip counts and both sink sets are right; the **exponents are wrong by 10³** throughout. (At
α_Φ = 1.5 the corresponding figures are 43 flips at ×10⁻⁸ and 103 at ×10⁻⁹, so the error is not an
α mismatch either.) "Largest magnitude 0.0347" is correct, and normalising into (−1, 1) does scale
up (by ×28.8). "Seven measured attempts failed the same way" is process history and is
**unmeasurable** from any source here.

### B2 — CONFIRMED, every clause

**Method.** Called `scipy.optimize.linprog(method="highs")` on the aggregate LP at
`dual/primal_feasibility_tolerance` ∈ {1e-7 … 1e-14, 0}, capturing warnings and `res.success`.
Separately ran `copper` under four LP column permutations at each tolerance and counted edge-slot
sign changes. Computed `max|b|` for `b_w` at several α_Φ and for all 29 `b_g`.

**Value.**
- **Below 1e-10 HiGHS rejects with `Invalid option value`:** confirmed. At 1e-11, 1e-12, 1e-14 and
  0 the call emits two `Invalid option value.` warnings; at 1e-10 and above, none.
- **`success` stays true:** confirmed. `res.success == True`, `res.status == 0`, and the message is
  `Optimization terminated successfully` in every rejected case.
- **It silently reverts to 1e-7:** confirmed, and this is the decisive test. `copper`'s edge-slot
  flips over four permutations:

  | tolerance | flips |
  |---|---|
  | unset (scipy default) | 2, 2, 4, 0 |
  | 1e-7 | 2, 2, 4, 0 |
  | 1e-8 | 0, 0, 0, 0 |
  | 1e-10 (shipped) | 0, 0, 0, 0 |
  | **1e-11 (rejected)** | **2, 2, 4, 0** |
  | **1e-14 (rejected)** | **2, 2, 4, 0** |

  A rejected value reproduces the unset/1e-7 behaviour exactly, so "scaling the tolerance is not
  available" holds.
- **Hazard unreachable since `|b|max ≥ 1/N`:** confirmed. `1/N = 0.0125`. Aggregate `max|b_w|` =
  **0.0347** at α_Φ = 2.0 and **0.0173** at its smallest over α_Φ ∈ [1, 8]; the smallest per-good
  `max|b_g|` over the 29 goods is **0.0368** (`grain`). Structurally, exactly one node
  (`cape_of_good_hope`) has `c_w = 0`, so `b_w` there is `1/N` exactly and the bound is attained.

### B3 — CONFIRMED

**Method.** Ran `final.py` PART B (the §3.13 calibration: `k_exp = 2` unclamped, ρ = 0.5,
tol = 3e-4). Independently recomputed the α = 16 cloves demand ordering from the wealth table.

**Value.** Under the calibration `cloves` sinks at **`['beijing']`** — not Deccan. `spices` sinks at
`['genua']` alone, and no Chinese node holds a *spices* sink. The α = 16 cloves demand order is
`hangzhou, beijing, doab`, matching §3.13. So:
- `Deccan` → **`beijing`**: correct.
- The v2 retraction should go: correct. Under the calibration a Chinese node (`beijing`) does hold a
  spice-**class** sink (`cloves`), so v2's *"China holds a spice sink only under the calibration"* is
  true when `spice` names the class and the parenthetical names the member.
- "not recovered by the calibration" → **no single good**: correct. `spices` → Genoa (Europe only),
  `cloves` → Beijing (China only); no single good holds both, but the class holds one of each.

Baseline sinks are as §2.8 states: `spices` `{brazil, genua}` at demand ranks 73 and 1; `cloves`
`{brazil, genua, kongo}` at ranks 72, 2, 55. *(Incidental, outside this row: §2.8's "`spices` from
`the_moluccas` and `kongo`" is wrong — 18 nodes produce `spices`. `cloves` from `the_moluccas`
alone is right.)*

### B4 — CONFIRMED

**Method.** Zeroed the wealth of every province in the `hangzhou` node (then `beijing`), rebuilt
`c_w` at α_Φ = 2.0, re-ran DRAIN and symmetric-differenced the edge sets against the baseline.

**Value.** Razing `hangzhou`: sinks move `{genua, hangzhou}` → `{genua, gulf_of_siam}`, with
**32 of 159** edges flipping. The spec's **30 is wrong; 32 is right.** Razing `beijing`: **8** flips
(spec's 8 stands), sinks unchanged, `hangzhou` surviving as a sink. Node wealth `hangzhou` 226.7 vs
`beijing` 143.0, ranks 12 and 39 of the 79 nodes holding counted provinces — all as stated.
"v4.0 alone" rather than "v2 through v4.0" is a provenance claim about superseded documents and is
not independently checkable here.

### B5 — CONFIRMED

**Method.** For each of the 29 live goods, ranked all 80 nodes by `c(·,g)` descending, took the top
8 and bottom 8, and counted how many are sinks of that good's DRAIN graph. Pooled over goods
(29 × 8 = 232 per arm). Repeated with the `build_sc` S/C construction as a cross-check — identical.

**Value.** Top eight: **45 of 232 = 19.4%**. Bottom eight: **17 of 232 = 7.3%**. The spec's
46/16 → 19.8%/6.9% is wrong; **45/17 → 19.4%/7.3%** is right. Sinks per good: min 2, max 8,
mean 3.69 — so "1–8 → 2–8" is right, though §2.8 L1279 already reads "2 to 8" and no site in the
frozen spec still says 1–8.

### B6 — CONFIRMED, both readings

**Method.** Built four arc-cost vectors — unit; first-order only; shipped
(`+ TIE_EPS2·frac(lo·hi·7919)`); structured (`+ TIE_EPS2·|w[u]−w[v]|`) — and counted distinct
per-edge costs under each. Then, for each, solved the aggregate and all 29 per-good LPs and counted
zero-reduced-cost arcs outside the support; and separately re-solved each per-good LP under 8 column
permutations and counted supports that moved.

**Value.**

| cost | distinct edge costs | equal pairs |
|---|---|---|
| unit | 1 of 159 | — |
| first-order only | **156** of 159 | **3** |
| shipped | **159** of 159 | **0** |
| structured `\|w[u]−w[v]\|` | **159** of 159 | **0** |

So **both costs make all 159 arc costs distinct** — the spec's "the shipped cost leaves 3 pairs
equal" is describing the *first-order* cost, not the shipped one. B6's correction is right, and the
contrast really is mechanism rather than distinctness.

"11 of 29 goods against 0" holds under both available readings, and is the cleaner statistic either
way:

| cost | zero-rc arcs outside support | supports moving under permutation |
|---|---|---|
| shipped | 1 arc on **1** good (`paper`) | **0** of 232 runs, **0** of 29 goods |
| structured | 17 arcs on **11** of 29 goods | 48 of 232 runs, **11** of 29 goods |

The relabelling reading gives exactly "**11 of 29 goods against 0**". (The zero-rc reading gives
11 against 1, not 0.) The spec's existing "72 of 232" is seed-dependent — my 8 permutations give 48
of 232 — which is itself an argument for quoting the goods count.

### B7 — CONFIRMED, including both cautions

*The row carries a specific warning. I checked the failure mode described before measuring, and it
is real.*

**Method.** Built five candidate normalisations of node wealth and asserted pairwise distinctness
**first**. Then, for each, rebuilt `TIE_COST`, re-ran DRAIN on the aggregate `b_w` and on all 29
`b_g`, and diffed against the shipped min-max baseline — once with `LP_OPTS` pinned at 1e-10 and once
with `LP_OPTS` cleared.

**Value.** The distinctness assertion the warning demands:

| pair | max abs difference |
|---|---|
| min-max (shipped) vs `w/max` | **0 — IDENTICAL** (because `min(NODEW) = 0`) |
| `w/mean` vs `N·w/sum` | **4.4e-16 — IDENTICAL** |
| `w/max` vs `w/mean` | 1.39 |
| `w/max` vs `w/sum` (world total) | 0.970 |
| `w/mean` vs `w/sum` | 2.36 |

Both defects the warning names are confirmed: `N·w/sum` *is* `w/mean` to float precision, and the
shipped min-max normalisation *is* `w/max`, so a {min-max, max, mean, N·w/sum} panel tests only two
genuinely distinct vectors and never touches world-total — the only one that moves the aggregate.

Results with `LP_OPTS` pinned:

| alternative | aggregate edges differing | per-good graphs differing |
|---|---|---|
| `w/max` | 0 of 159 | 0 of 29 |
| `w/mean` | 0 of 159 | 9 of 29 |
| **`w/sum` (world total)** | **7 of 159** | 10 of 29 |
| `N·w/sum` | 0 of 159 | 9 of 29 |

- **7 of 159 aggregate under world-total:** confirmed exactly.
- **13 of 29 per-good:** confirmed as the *union* over the alternatives —
  `{copper, cotton, fish, gems, glass, grain, paper, wine, wool}` (mean, 9) ∪
  `{cloves, cocoa, copper, cotton, gems, grain, naval_supplies, paper, salt, wool}` (world total, 10)
  = **13 distinct goods**.
- **An unpinned solver undercounts (5 against 9, a subset):** confirmed exactly. Unpinned, `w/mean`
  gives `{copper, fish, gems, grain, paper}` — **5**, and a strict subset of the pinned **9**.
- The frozen spec's "0 of 159 edges differ, 5 of the 29 per-good graphs do" is precisely the
  0-and-5 the warning describes: 0 is what the three non-world-total normalisations give, and 5 is
  the unpinned count.

### B8 — CONFIRMED

**Method.** Ran the full per-good battery under each of `drain.sweep_priority`'s three key modes,
built `Φ_ord = Σ_g V_g·order_g` from each, oriented every edge by `Φ_ord` descending and counted
sinks; ran `Φ_w` under the same three keys.

**Value.**

| sweep key | `Φ_ord` ends | `Φ_w` ends |
|---|---|---|
| `defasc_beta` (shipped) | **14** | 2 |
| `def_beta` | **8** | 2 |
| `def_absb` | **8** | 2 |

**14/8/8 against `Φ_w`'s 2** — exact. `Φ_ord`'s end *set* moves too (14-node set includes
`african_great_lakes, aleppo, amazonas_node, beijing, burma, doab, …`; the 8-node set is
`astrakhan, burma, genua, hangzhou, krakow, mexico, …`), while `Φ_w` returns `{genua, hangzhou}`
under all three. All three `Φ_ord` orientations are acyclic. "Relabelling cannot separate the
operators because the tie-break made both stable" is consistent with §1.6's own 180-relabelling
result and with B7's pinned-solver finding.

### B9 — CONFIRMED

**Method.** Ran `phase2` on the aggregate `b_w`, accumulated per-node flow in and out over the
flow-arc support, and compared `flow_in − flow_out` to `−b_w` at every net-demanding node. Counted
nodes with positive out-degree in the compiled DAG but zero outgoing flow.

**Value.** Nodes with `b_w < 0`: **36**. The identity `flow_in − flow_out = −b_w` holds on
**36 of 36** with max absolute residual **5.204e-17** (mean 1.54e-18) — the row's 5.2e-17 exactly.
`−b_w > 0` at all 36 by construction. Nodes with out-degree > 0 and zero outgoing flow: **18 of 80**.
The named rich non-sinks check out: `english_channel` (wealth 316.6, in-degree 2, out-degree 3,
flow_out **0**), `mexico` (300.4, 4/1, flow_out 0), `gulf_of_siam` (297.9, 2/1, flow_out 0),
`sevilla` (266.5, 2/3, flow_out 0.0201), `genua` (296.0, 5/0). This shows why the degree clause
needed replacing: `english_channel` has out-degree 3 and in-degree 2, so "draws more edges in than it
sends out" is simply false there — the flow identity is the claim that holds.

### B10 — CONFIRMED

**Method.** For each of the 29 goods, summed flow into and out of `cape_of_good_hope` over that
good's Phase-2 flow-arc support. Grepped the spec for the Cape's in/out sets.

**Value.** The Cape carries flow **in and out on 28 of 29 goods**; the single exception is **`paper`**
(flow in 0, flow out 0). Degree-based counting hides this: `V129` in `final.py` reports 29/29 on
in-degree/out-degree, because on `paper` the Cape's edges are free edges oriented by the sweep rather
than flow arcs. So the evidence really does have to be flow, not degree.

`cape_of_good_hope → malacca` is stated **twice** in §1.6 — L647 (*"passes it to `comorin_cape` and
`malacca`"*) and L657–658 (*"1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca`
drainage"*). Both are correct: on `Φ_w` the Cape takes from `{zanzibar, ivory_coast}` and passes to
`{comorin_cape, malacca}`.

### B11 — CONFIRMED

**Method.** For each solve, took the LP duals and computed the minimum **positive** reduced cost over
arcs outside the support — the margin by which the optimum is unique. Computed on the peeled core
exactly as `drain.phase2` solves (peeling made no difference).

**Value.** Aggregate margin: **7.52656e-06 at α_Φ = 2.0** (row says 7.53e-06 ✓) and
**1.2672e-07 at α_Φ = 1.5** (row says 1.267e-07 ✓). Per-good, exactly **two of 29** solves sit inside
the 1e-7 default — `copper` **3.765e-08** and `paper` **8.915e-08** — and **27** are above, the next
being `cotton` at 1.177e-07. This also locates §3.6's "3.8e-8 at worst": it is the per-good worst
(`copper`), not the aggregate, which at the operating α_Φ is two orders larger.

**Site inventory for the margin figure** (added after the coordinator asked whether seven sites were
all of them). Sweeping *every* scientific-notation token in the spec rather than a pattern for this
one figure, **eight** sites carry it numerically:

| line | § | text | scoping |
|---|---|---|---|
| L32 | §0 | "as small as 3.8e-8" | unscoped |
| L863 | §2.1 | "**3.8e-8** worst per good, **7.5e-6** on the aggregate" | asserts a worst case |
| L888 | §2.2 | "orientation margins above are 3.8e-8 to 7.5e-6" | a two-battery range |
| L1071 | §2.3 | "**3.8e-8** on some per-good solves" | **correct already** |
| **L1080** | §2.3 | "`copper`'s **3.765e-8** margin" | **correct already** |
| L1268 | §2.7 | "§2.1's orientation margins are 3.8e-8 to 7.5e-6" | a two-battery range |
| L1299 | §2.8 | "a **worst-case margin** of 3.8e-8" | asserts a worst case |
| L1568 | §3.6 | "a margin of 3.8e-8 **at worst**" | asserts a worst case |

**L1080 renders the figure as `3.765e-8`**, so a pattern written as `3.765e-08` cannot find it. It
needs no scope change — it names `copper` — but it means the document already carries two renderings
of one quantity, and writing a third (`3.765e-08`) at the rescoped sites would create exactly the
differently-worded-copy defect `every_site()` exists to catch and `shows()` cannot see.

**A ninth site carries the derived claim with no figure in it:** L1779 (§3.13), *"unique with a margin
8 to 10 orders above float noise"*. No numeric pattern can find it. It survives the change —
2.498e-08 is 8.05 orders above double-precision unit roundoff, 3.8e-8 is 8.23 and 7.5e-6 is 10.53, so
"8 to 10" holds on every reading — but it is a dependent site and belongs in the sweep.

**Incidental, at L888 and L1268:** *"three to five orders below a 1e-3 grid"* is right only by
exponent difference (−3 vs −8 = 5; −3 vs −6 = 3). By ratio it is **4.42 and 2.12 orders** — "two to
four". Both readings are defensible; flagging it because the sentence sits next to figures being
edited.

### B12 — CONFIRMED

**Method.** Read §3.10 L1675–1679 and §3.15 L1887.

**Value.** The two sections contradict each other today. §3.15 L1887 reads *"**Per-good propagation.**
Breaks the income factoring and with it Goal 7."* §3.10 L1677 reads *"**What that does not do is
break the identity.**"* and then derives `collect_pool · ps̄_C = income_C` algebraically with
`Σ_C ps̄_C = 1`. Dropping "breaks the income factoring" while keeping the verdict and grounding
Goal 7 in the fictitious-power-field argument (§3.10 L1679) resolves a live contradiction. Y183's
residual is the *"worst relative disagreement of **0 to 3.7e-16**"* at L1675, in a paragraph that
already calls itself *"an identity, not a measurement"* — so dropping the figure entirely is
internally consistent with what the paragraph says about itself.

### B13 — CONFIRMED (and all three figures are wrong today, not merely unmaintained)

**Method.** Ran `final.py` PART B at the §3.13 configuration and recomputed span, spearman, reach
and pruned mass. Read `../v5-owner-agnostic/changes-v5.md` §§39–41.

**Value.**

| §3.13 figure | spec | measured on the v6 field |
|---|---|---|
| span | "exactly 1..5" | **1..6** |
| spearman(price, sinks) | −0.20 | **−0.395** |
| cloves reach | 99.97% | **99.9975%** |
| pruned twig mass | "up to about 0.18%" | **0.147%** |

The configuration and the qualitative costs are correct and worth keeping: α unclamped at exponent 2
with `cloves α = 16`, ρ = 0.5, tol 3e-4; the α = 16 cloves demand order really is
`hangzhou, beijing, doab`; and `hangzhou`, not `beijing`, really does hold the richest single
province (pid 1821 at 27.00).

The `changes-v5.md` §39–41 provenance is exact: §39 replaced spearman −0.53 with −0.20, §40 replaced
"silk to 99.97%" with "cloves to 99.97%", §41 replaced 0.15% with 0.18% — all three flagged
*"Figure regenerated on the v5 wealth field"* and never re-measured on v6's. (Note the v5 value §41
replaced, 0.15%, is closer to the v6 field's 0.147% than the replacement is.)

### B14 — **WRONG** on the interval

**Method.** Scaled the wealth of all 824 counted European provinces by k over
k ∈ {1.000, 1.001, …, 2.600} — 1,601 DRAIN solves — recording the sink set at each grid point, then
took maximal runs where the set is exactly three European nodes with none in Asia. Confirmed the two
boundaries by direct evaluation at ×1.970–×1.975 and ×2.454–×2.459.

**Value.** The widest uniform run is grid points **×1.973 through ×2.456**, width 0.483, set
`{english_channel, genua, rheinland}`.

The row's **×1.974–×2.457 is wrong at both ends**, shifted by exactly one grid step:

| k | sink set |
|---|---|
| ×1.972 | `english_channel, genua, hangzhou, rheinland` |
| **×1.973** | `english_channel, genua, rheinland` ← run starts here |
| ×1.974 | `english_channel, genua, rheinland` |
| ×2.456 | `english_channel, genua, rheinland` ← run ends here |
| **×2.457** | `genua, rheinland` — only **two** ends |

At ×2.457 the set is not three European ends at all, so the stated upper endpoint asserts something
false. The width (0.483), "uniform on a 0.001 grid", "three European ends" and "none in Asia" are all
correct.

**Dropping the table is well founded, and for a reason stronger than the row gives.** Its widest row,
×1.38–×1.95, is **not** uniform at 0.001 resolution: it carries **four** distinct sink sets
(`{english_channel, genua, rheinland}`, `{english_channel, genua, hangzhou, rheinland}`,
`{doab, english_channel, genua, rheinland}`, `{genua, gulf_of_siam}`). The ×1.97–×2.46 row carries
three. The bisected boundaries hide sub-intervals, so the table's headline claim — that ×1.38–×1.95
is the widest interval over which the set is constant — is an artefact of coarse bisection.

**Correct value: ×1.973–×2.456.**

### B15 — **WRONG** on the count

**Method.** Enumerated 22 quantities §1.6 quotes that a sweep key could move, and recomputed all 22
under the shipped key (`defasc_beta`) and under `def_beta`.

**Value.** **10 of 22** change, not seven:

| quantity | shipped | `def_beta` |
|---|---|---|
| sources | 5 | **10** |
| source `c_w` rank range | 55–79 | **40–76** |
| source mean degree | 2.4 | **2.6** |
| per-good sinks | 2–8, mean 3.69 | **1–8, mean 3.66** |
| connectivity | 5,723 (90.6%) | **5,759 (91.1%)** |
| self-coherence | 55.1 / 54.8 | **54.8 / 53.3** |
| Cape ordered pairs | 81 | **42** |
| Europe→sink pairs | 26 | **25** |
| northern long route | 12 hops via `samarkand…gulf_of_siam` | **7 hops via `girin, beijing`** |
| Iberian long route | 12 hops via `safi…canton` | **no route** |

Unchanged: sink set, Phase-1 selection, promotions/fallbacks, 159/159 oriented, acyclicity, Cape
in/out degree, `genua` degrees, `english_channel → champagne → genua`, the ±1% noise sink sets, the
Europe-table rows sampled, and the 18-node ×1.52 onset.

**The substantive claim is confirmed:** both long routes change, and **the Iberian one ceases to
exist** — `sevilla` reaches no Asian end at all under `def_beta` or `def_absb`. "Unprompted" (§1.6
L630) should indeed go, since the routes are a property of the sweep key and not of the field alone.

The count is individuation-sensitive — bundling *"Five sources … `c_w` ranks 55–79, mean degree
2.4"* as one figure gives 8 — but no bundling I can construct reaches seven while covering all ten
quantities. **Correct value: 10 of 22 tested (8 if the three source figures are counted as one
sentence).**

### B16 — split: **425 CONFIRMED**, **~2,249 UNMEASURABLE**

**Method.** Walked every `.txt` under `common/`, `missions/`, `decisions/`, `events/` (2,624 files),
stripped comments, and counted uses of the four structural families named in §1.10 L793–795.
Separately counted candidate denominators for "uses".

**Value.** The four families total **425** across those four trees — exact, provided
`*_trade_node_member_province` is read as including `all_`:

| token | uses |
|---|---|
| `any_active_trade_node` | 90 |
| `any_trade_node_member_province` | 80 |
| `random_trade_node_member_province` | 75 |
| `random_active_trade_node` | 66 |
| `highest_value_trade_node` | 38 |
| `home_trade_node` | 36 |
| `all_trade_node_member_province` | 16 |
| `every_trade_node_member_province` | 16 |
| `every_active_trade_node` | 9 |
| **total** | **425** |

Also confirmed: **nothing names a node** — measured, not assumed. Scanning `common/`, `missions/`,
`decisions/`, `events/` for `trade_node = <node key>` assignments gives **0 of 80 nodes, 0 uses**.
Scanning for bare occurrences of any of the 80 node keys as a token gives 239 uses — **all 239 in
`common/tradenodes/00_tradenodes.txt`, the file that defines the nodes, and zero anywhere else.** No
trading policy in `00_trading_policies.txt` tests upstream/downstream either, so **nothing tests
direction**.

**What lies outside the four families is measurable, and it is small.** Keys containing
`trade_node` total **617** uses over 36 distinct tokens in those four trees. The four families are
425 of them, so every other node-scoped construct together comes to **192 uses over 27 keys —
0.45× the families, not a multiple of them.** The largest are `every_trade_node_member_country`
(44), `add_trade_node_income` (28), `home_trade_node_effect_scope` (21), `trade_node_value` (20),
`any_trade_node_member_country` (16) and `agenda_trade_node` (15); the remaining 21 keys contribute
48 between them.

**~2,249 is not reproducible.** Candidate denominators measured over the same four trees: 617 (all
keys containing `trade_node`), 2,033 (all `trade`-bearing keys not in the modifier vocabulary),
2,661 (`trade_node` + trade-power keys), 3,151 (adding trade-company keys), 5,148 (all `trade` keys in
`events`+`decisions`+`missions`), 10,264 (all `trade` keys in all four trees). The closest is 2,033,
under one particular definition of "modifier vocabulary"; the figure moves by hundreds under any
neighbouring definition. **The source that would settle it is the instrument that produced the
figure — no script in `scripts/` computes it.**

### B17 — CONFIRMED

**Method.** Scaled the provinces of the 18 named western/central European nodes (652 provinces) over
×1.00–×4.00 at 0.01, and the 22-node set (797 provinces) over ×1.00–×25.00 at 0.05, recording sink
sets.

**Value.**
- **18-node: sole sink `genua` from ×1.52** — exact. It is continuous from ×1.52 all the way to
  ×4.00, my sweep's upper bound, so "continuous to ×3.20" is true and conservative. The spec's
  "about ×1.55" is wrong; ×1.52 is right.
- **22-node: no sole sink below ×20** — confirmed, and stronger: **no sole sink anywhere up to ×25**.
  The set settles at `{genua, rheinland}` from ×3 and stays there.
- **"the eastern four keeping ends of their own" is invented** — confirmed. Across every multiplier
  tested (×1, 1.5, 2, 3, 4, 6, 10, 20, 25), **not one** of `constantinople`, `crimea`, `kiev`, `kazan`
  ever holds a sink. The reason there is no sole sink is that `rheinland` keeps one, not the east.

### B18 — CONFIRMED on the substance; **my own first bracket was wrong and is corrected here**

**Method (threshold).** Read `TRADE_PROPAGATE_DIVIDER` and `TRADE_PROPAGATE_THRESHOLD` from
`common/defines.lua`. Then worked the save two ways. **First pass:** for each clean single-source
case (a country with power in exactly one downstream neighbour of the target node and no own presence
in the target) checked whether it appears upstream at 1/5 of that power. **Second pass, after the
first was challenged:** dropped the presence test entirely and used the sending node's own
`already_sent` field, which is a property of the sender and does not depend on whether the target is
colonised. Tabulated all **766** (country, node) pairs carrying `province_power`.

**Value.** `TRADE_PROPAGATE_DIVIDER = 5`, `TRADE_PROPAGATE_THRESHOLD = 2`, so
**THRESHOLD × DIVIDER = 2 × 5 = 10** — confirmed from the shipped file.

**Correction to my first pass.** I reported a bracket of (9.840, 10.080] from the presence test. The
upper bound is wrong. `already_sent` finds a propagating case my single-source filter had excluded:

| | power | evidence |
|---|---|---|
| largest that did **not** propagate | **9.840** | `ALS` in `rheinland`, `KUB` in `kongo` — no `already_sent` |
| smallest that **did** | **10.038** | `MAI` in `rheinland`, `already_sent = 4.014 = 0.2 × 10.038 × 2` |

**Corrected bracket: (9.840, 10.038].** It contains 10.

**The confound is real and is now evidenced rather than assumed.** `CCQ` in `cuiaba` carries
province power **10.038 — the same value as `MAI`** — and has no `already_sent`. Identical power,
opposite outcome, so province power alone cannot be the whole gate. Testing "already_sent present iff
power ≥ 10" over all 720 pairs whose node has at least one upstream neighbour gives **16
inconsistencies**, every one in the same direction (power ≥ 10, nothing sent) and concentrated in
four nodes: `girin` (5), `australia` (5), `bordeaux` (3), `cuiaba` (2) — plus `FRA`, `BRI` and `ENG`
at `bordeaux` with power 24–39. There is **not one** counterexample in the other direction: no pair
below 9.87 sends anything.

The `already_sent` magnitudes locate the second gate precisely. `already_sent = 0.2 × province_power
× (number of upstream nodes the sender actually reaches)` is exact on 169 of 215 senders, and every
one of the 46 residuals resolves once the unreached upstream nodes are dropped from the count:
`BUR` at `english_channel` sends `0.2 × 10.887 × 3`, not × 5; `GRA` at `sevilla` sends
`0.2 × 11.600 × 2`, not × 4; `ENG` at `bordeaux`, power 38.921, reaches **0 of 3** and so carries no
`already_sent` at all. So the share is pinned at **exactly 1/5** without any judgement.

**The gate is sender-relative, and it is not target colonisation.** Every unreached node is
colonised and busy: `ivory_coast` carries 90.56 province power across 6 countries, `chesapeake_bay`
43.89 across 16, `polynesia_node` 46.98 across 16, `california` 30.69 across 9, `st_lawrence` 39.23
across 8. Only `cape_of_good_hope` has no holder at all, and it is not involved. The same node is
reached by some senders and not others — `ivory_coast` is unreached by both `BUR` and `GRA`, two
European powers in 1444, while six African countries hold power in it. The pattern fits a discovery
or trade-range gate on the *sender*, but nothing in the fields read here decides which, so the
mechanism is observed and not identified.

Sweeping the threshold, the misclassification count is flat at 16 over **T ∈ [9.87, 10.38]**, which
contains 10 and excludes 2, 5 and "no threshold".

**On superseding the validation agent's (5.01, 10.04].** I cannot certify independence: I never saw
their construction. But both of their endpoints sit on values in this save — `BOH` in `wien` at
**5.014** (nothing sent) and **10.038** (`MAI` sends, `CCQ` does not) — which makes it likely we read
the same save and the same field, and that their sweep simply did not reach as far up the
non-propagating side. On that reading neither of us has a construction error: **their upper bound is
right and mine was wrong; my lower bound is right and theirs is loose.** The two intervals are
consistent, not in conflict.

**What this does and does not license.** It does not license "= 10, measured". The bracket still
depends on classifying the 16 outliers as target-eligibility failures rather than threshold failures
— now evidenced by the `already_sent` arithmetic, but still a model of a second gate the defines do
not describe. Stating it as **one observation** remains right.


**Method (Y099).** Recomputed `Φ_ord` and `Φ_w` self-coherence against the 29 per-good graphs, both
unweighted and value-weighted.

**Value.** `Φ_ord` **59.8 / 59.6** against `Φ_w`'s **55.1 / 54.8** — exact. (`final.py` V062
independently reports 2758/4611 = 59.8%.)

### B19 — CONFIRMED on the values; the change is a no-op

**Method.** Recomputed connectivity and self-coherence from a fresh DRAIN run; grepped every site in
the frozen spec.

**Value.** Connectivity **90.6% (5,723 of 6,320)** and self-coherence **55.1 / 54.8** — both correct.
But the frozen spec **already carries these values at every site**: 90.6% and 5,723 at L552 (§1.6) and
L1612 (§3.8); 55.1 at L554 and L1312; 54.8 at L554 and L1311. The "from" values — 90.5%, 55.2, 55.0 —
appear nowhere in the document (`grep` returns nothing for any of them). So the row's target values
are right and the edit has nothing to change.

---

## C. Provenance and instruments

### C1 — CONFIRMED (one wording caveat)

**Method.** Ran `apparatus6.py`; read `../v5-owner-agnostic/scripts/solver.py:55–76`.

**Value.** `apparatus6.py` prints world wealth apparatus-off **10,607.40**, apparatus-on
**10,712.70**, delta **105.30**, provinces touched **89**, and self-checks `RESULT: 4 checks,
0 failed`. Reproduction is exact. The constants are verbatim from v5's `solver.py` at the cited
lines. No classification happens in the script — it applies a fixed table.

Caveat on "twenty frozen constants": the table holds **22** entries — `LOCAL_TAX_MOD` (1),
`LOCAL_TV_MOD` (1), `MON_FLAT` (5), `MON_GPMOD` (1), `MON_TVMOD` (4), `PERM_FLAT` (10). "Twenty" is
right only if the two trade-good-keyed entries are excluded, leaving the 20 province-keyed ones.
The relative path `../v5-owner-agnostic/scripts/solver.py` resolves correctly from the v6 root.

"W041 and X035 refuted the rule, never these values" is a claim about two prior audits' scope; I did
not attempt to re-grade those audits, and the substantive point — that nothing in `apparatus6.py`
classifies anything — is confirmed by reading it.

### C2 — CONFIRMED exactly

*The row carries a specific warning. The failure mode it describes is real: I reproduced it before
running the acceptance test.*

**Method.** Confirmed the two line numbers by `sed -n '169p;237p;245p' final.py`. Copied `final.py`,
changed line 245's `mincost_flow(b + 0, np.zeros(N))` to pass `cost=TIE_COST`, and ran both versions.
Separately, re-implemented `final.py`'s PART-B machinery at baseline knobs (Phase 1 with ρ = 1.0,
`ZERO_TOL = 1e-11`) and compared its output to `drain.run_drain` on all 30 b-vectors.

**Value.**
- `final.py:169` is `flow_arc, free, net, cost = phase2(core, beta)` — inside V035's per-good loop
  but **outside** the `for perm in range(2)` permutation loop, and `drain.phase2` already passes
  `TIE_COST`. So the LP is solved once, with the tie-break, before any permutation. **`V035` reads 0
  before and after the repair** — measured 0 both times. The warning is correct: V035 cannot
  discriminate.
- `final.py:245` is the uncosted `mincost_flow` call; `TOL = 3e-4` is at line 237 and is untouched by
  the change.
- **Acceptance test: `V107` moves `['genua']` → `['doab', 'genua']`.** Confirmed exactly. (Side
  effects of the same patch, for completeness: V177 spearman −0.395 → −0.473; max pruned twig mass
  0.00147 → 0.00142; V179 cloves stays `['beijing']`; acyclicity 29/29 both ways.)
- **Validated at baseline knobs against `drain.run_drain` on all 30 b-vectors:** with
  `cost=TIE_COST`, **30 of 30** reproduce `run_drain`'s orientation exactly. Without it, **0 of 30**
  (the aggregate differs on 30 edges, per-good on 10–32). The validation is meaningful and it passes.

### C3 — CONFIRMED

**Method.** `grep -rn "final.out" scripts/`; `ls scripts/final.out`.

**Value.** `final.py` writes **no** output file — `final.out` does not exist and nothing in the tree
references it. `verify6.py` contains no check reading it. So the proposal creates a producer and two
consumers that do not exist today. The "identity, not age" guard is a design choice; no figure to
check. Precedent for the hard-failure requirement exists: `coverage6.py:15-16` already exits when
`measure6.out` is missing.

### C4 — CONFIRMED

**Method.** `ls scripts/fingerprint6.py`; read `final.py:152–159`; grepped the spec for the
fingerprint claim.

**Value.** **`fingerprint6.py` does not exist.** The nearest instrument is `p3_fp.py`, whose docstring
says *"Determinism fingerprint: Phi_w + all 29 per-good graphs, sinks, sources, promotions, fallbacks
and the Phase-2 objective, hashed. spec 2.1 table row 1 / 2.8 'Determinism'."* The two spec sites that
would cite it — L862 (§2.1) and L1298 (§2.8) — currently cite **no script at all** for a claim about
separate processes and five `PYTHONHASHSEED` values.

`V037` is exactly as described: `final.py:153–159` calls `run_drain` **six times in one process** on
`spices` and compares orientations. It is blind to between-process variation by construction.

### C5 — CONFIRMED

**Method.** Read `val5_pergood.py` end to end and grepped it for `permutation`/`shuffle`; ran it.

**Value.** The docstring (line 8) claims the script measures *"free-edge determinism under scheduler
permutation"*. The word `permutation` appears **once in the whole file — in that docstring**. There
is no permutation loop, no RNG, and no `prio=` argument anywhere in it. The script's actual output
carries no scheduler-permutation figure. Grepping the tree, only `drain.py` (which defines the `prio`
parameter) and `drainrep.py` mention scheduler priority at all; `final.py`'s V035 permutes the
priority key's *index* tiebreak, not the scan order. **The figure lives nowhere in the tree** —
confirmed. It must be built before §1.1 can cite it.

### C6 — CONFIRMED

**Method.** Read `drain.phase0` and `drain.compile_dirs`.

**Value.** `phase0` appends `(v, u, beta[v])` to `Plog` and emits nothing; the pendant's direction is
*determined* there by the sign of the absorbed balance. `compile_dirs` — Phase 4 — walks `Plog` in
reverse and emits `(v, u) if bv >= 0 else (u, v)`. So Phase 0 determines and Phase 4 un-peels **and
emits**, exactly as the row says; §1.1 L90–92 currently attributes the orientation to Phase 0 and
L144 gives Phase 4 only the un-peel. (The "zero → toward core" rule is faithful: `bv == 0` takes the
`>=` branch, pendant → parent.)

### C7 — CONFIRMED on the figures; already present in the frozen spec

**Method.** Ran `val5_pergood.py`, which sums `|core|` over the 29 per-good solves and counts exact
`(DEF, β)` key collisions, Phase-1 within-cluster argmin ties, and top-k cut ties. Cross-checked the
2,320 arithmetically.

**Value.** Core nodes summed over goods: **2,320** — and this is `29 × 80`, i.e. every good's core is
the whole graph, because the vanilla map has minimum degree 2 and Phase 0 peels nothing. Exact
`(DEF, β)` key collisions: **0**. Phase-1 within-cluster argmin ties: **0**. Top-k cut ties: **0**.

All four figures are right. But the change is already applied: §1.1 L181–184 of the frozen spec
reads *"zero exact `(DEF, b)` key collisions across **all 2,320 core nodes** of the 29 per-good
solves — not merely on the free edges, which is where earlier versions measured it. Phase 1's
within-cluster argmin and its top-k cluster cut are untied on the same field."* Nothing to edit.

### C8 — CONFIRMED; already applied

**Method.** Read §0 L57–75 and grepped for "well under half".

**Value.** "Well under half" survives in the spec only inside its own retraction, at L68–69:
*"An earlier draft of this paragraph asserted 'well under half' two sentences before refusing to give
a ratio; the refusal is the part that survives."* It is nowhere asserted. The paragraph already
declines both a count and a proportion, and gives two distinct reasons (the count moves with the
prose; the denominator is ill-defined — "anywhere from 279 to 326 depending on how a numeric token is
delimited"). Rewriting to P1's wording is a style decision with no figure attached.

### C9 — CONFIRMED

**Method.** Read `drain.phase1`, `drain.run_drain`, `final.phase1_q`, and `drain.py`'s module
docstring; grepped the spec for `ρ`.

**Value.** `drain.phase1(core, beta, dilate_r=0)` has **no ρ parameter** and no quantile logic
anywhere. The only implementation of ρ in the tree is `final.py:219 phase1_q(core, beta, rho)`, which
belongs to the §3.13 calibration harness, not to the shipped operator. So §1.1 L98–99 ("Knobs: a
demand-mass quantile `ρ` … default 1.0") and §2.3 L1024 describe a knob the reference implementation
does not have. Deleting it from those two sites is right; §3.13 L1770 legitimately keeps ρ = 0.5 as a
calibration setting, and the row does not touch it.

`r` does exist: `phase1`'s `dilate_r` branch is fully implemented (union-find merge of clusters within
`r` hops). That makes `drain.py`'s docstring wrong as written — *"Phase 1's optional dilation (merge
clusters within graph distance r) is **NOT applied**"* — the dilation is implemented and simply
defaults to off. Correcting it is right.

### C10 — CONFIRMED, with one caller to fix

**Method.** `grep -rn "build_sc(\|solve_all(" scripts/ --include=*.py` and inspected each of the 42
call sites.

**Value.** Every **external** caller of `build_sc` already passes `eps=` as a keyword — 40 sites
across `flowop.py`, `measure6.py`, `final.py`, `verify.py`, the 15 `p3_*` probes, and the rest. Both
callers of `solve_all` (`verify.py:66,81`) pass `eps=` too.

One caller does not, and the row's "every shipped caller already passes it" glosses over it:
**`solver.py:235`**, inside `solve_all` itself, calls `build_sc(alpha_of_good, eps)` **positionally**.
Making `eps` a required keyword-only parameter would raise `TypeError` there unless that line is
changed to `build_sc(alpha_of_good, eps=eps)` in the same edit. A one-line addition, but it is not
optional.

### C11 — CONFIRMED that the count must go; the current one is wrong on both numbers

**Method.** Ran `measure6.py` unmodified (α_Φ = 2.0) and again with `A_PHI = 1.5`, writing to separate
output files, then diffed the two label→value maps.

**Value.** `measure6.py` prints **60** labelled figures at α_Φ = 2.0 and 59 at 1.5 (one fewer
per-sink rank line, since the 1.5 field has one sink). The spec's L42 denominator of **59 is wrong**.

Figures that move between the two fields: **18** of the 57 keys common to both, plus 3 keys that exist
only at 2.0 and 2 only at 1.5 — **21 of 60** on the most natural counting. The spec's **29 is wrong**.
The movers are: `Phi_w sinks`, `Phase-1 selection`, `sources` (7→5), `source c_w rank range`,
`source mean degree`, `largest |b_w|` (0.0225→0.0347), both self-coherence figures, all three Europe
scaling rows, all three noise seeds, cape in-degree (1→2), cape out-degree (3→2), cape routed pairs
(144→81), coal edge flips (22→16), plus the per-sink rank lines and the band key.

Replacing the count with a partition of what moves versus what holds is well founded — and, as the
row says, survives the next operator change, which a count does not. *(`fixes-agreed.md` §7 carries a
third stale value for the same quantity: "57 labelled figures".)*

### C12 — CONFIRMED

**Method.** Computed the shipped `TIE_COST` vector and compared its range to
`[1, 1 + TIE_EPS + TIE_EPS2]`.

**Value.** Shipped costs run **[1.000009690729, 1.000937280025]**, strictly inside
`[1, 1.001001]` = `[1, 1 + 1e-3 + 1e-6]`. The interval claim is correct. The percentage the row drops
is also correct — the spread is **0.0928%** of the base cost, so §1.1 L188's "under a tenth of a
percent" is true — so this is a presentation choice (a bound that follows from the constants versus a
figure needing maintenance), not a repair. Y309 ending at "nothing in the model reads that field" is
editorial; §1.5 L420–423 already carries that clause.

### C13 — **WRONG** on the row count

**Method.** Counted the rows and distinct IDs in `fixes-agreed.md` §5 ("Every graded-open claim,
mapped"); read its own header and its action tally; checked both harnesses' default targets.

**Value.** §5 contains **62** rows and **62** distinct `X###` ids, its own preamble states
*"62 items"*, and its action tally — MOOT 15, DROP 4, SOFT 4, VALUE 19, ARG 12, GAME 5, MECH 3 —
sums to **62**. The spec's Y012 site (§0 L57–58) is consistent: 22 refuted + 39 partial + 1
unverifiable = 62. **There are 62 v5 rows, not 63.**

Everything else in the row checks out. `fixes-agreed.md` is currently the default target of **both**
harnesses — `verify6.py:217` and `mutate6.py:9` — so "out of both harness defaults" is a real change.
Its header does not currently mark it frozen.

**Correct value: 62.**

---

## D. Harness defects

### D1 — CONFIRMED, exactly

**Method.** Ran `python mutate6.py ../per-good-trade-spec.md` and `python mutate6.py` with no
argument; read `measure6.A_PHI`.

**Value.** The spec path raises, verbatim:

```
  File "...\mutate6.py", line 31, in _spec_mutations
    band = O["band containing alpha=1.5"]
KeyError: 'band containing alpha=1.5'
```

The key `measure6.py` actually emits is `band containing alpha=2`, because `measure6.A_PHI = 2.0` and
line 125 builds the label as `"band containing alpha=%g" % A_PHI`. Deriving `BANDKEY` from `M.A_PHI`
is the right fix — `verify6.py:121–122` already does exactly that and is why the verifier does not
have the same bug.

The no-argument path prints `caught 10 of 10 planted errors` and exits 0, scoring **10/10 against
`fixes-agreed.md`** — a document that is complete and not being edited. Both halves confirmed.

### D2 — CONFIRMED

**Method.** Read `mutate6.py:60` and `verify6.py:222–233`.

**Value.** `mutate6.py` routes on filename:
`MUTATIONS = _spec_mutations() if os.path.basename(DOC).startswith("per-good-trade-spec") else CHECKLIST`.
`verify6.py` routes on content, via `SPEC_MARK = "Per-Good Trade Network"` and
`CHECKLIST_MARK = "implementation checklist"`, and its own comment records that filename routing was
the bug it fixed — *"mutate6.py, which writes its candidate to `_mutated.md`, was scoring every
planted error as 'caught' when in fact nothing was being checked."* The inconsistency is exactly as
stated, and `mutate6.py` still writes to `_mutated.md`, so it still relies on `verify6.py`'s
content routing to work at all.

### D3 — CONFIRMED, live today

**Method.** Read `verify6.py:30–48`; ran `verify6.py ../per-good-trade-spec.md`.

**Value.** When `_pattern(template)` matches nothing, `hits` is empty, `bad` is empty, and line 48
appends `(True, …)` — a pass. Live on `spec: sources`, whose needle is built from
`WORD.get(O["sources"])` = `"Five"`, a word the `NUMPAT` wildcard cannot match. Verbatim from the
run:

```
  [PASS] spec: sources     **Five sources** (present; consistency scan found 0 sites - the template has n
```

So the consistency half of that check — the whole point of `shows()` — is inert, and the note says so
while still passing. Adding `0: "Zero"` to `WORD` and making both the scan and the comparison
case-insensitive is coherent; shipping it **before** A5 matters, because A5 changes a spelled count
(five → four) that this mechanism is supposed to police.

### D4 — CONFIRMED empirically

**Method.** Built three mutants of the spec and ran `verify6.py` on each.

**Value.**

| mutant | result | exit |
|---|---|---|
| marker phrase reworded | `30 checks, 0 failed` → **28 checks, 0 failed** | 0 |
| marker reworded **and** the `unrest` row deleted | **28 checks, 0 failed** | 0 |
| marker kept, `unrest` row deleted (control) | `30 checks, **2 failed**` | 1 |

The check is gated on `if _i >= 0:` at `verify6.py:196`, so a missing marker drops two checks and
reports nothing. In the second mutant a genuinely inconsistent document — a four-row table under
prose saying "five" — **passes**. That is precisely the state A5 would create if its rewrite touched
the marker sentence. Locating the table structurally and failing closed is the right fix.

### D5 — CONFIRMED

**Method.** Counted `absent()` calls in `verify6.run_spec`.

**Value.** Exactly **five phrases** — "the widest band on this field", "Nothing routes through the
Cape", "exactly **two** modifiers enter wealth", "no figure in v6.0 is unverified", "So almost
nothing absorbs threshold chatter" — and exactly **three dead-operator figures** — "`Φ_ord`'s
**60.3%**", "97 of 159 arrows", "13 end nodes". The counts match the row exactly. The weakness is
real: `absent()` tests string non-membership only, so any rewording satisfies it. Boundary-anchored
value checks for 12.23 and 9.40 are the right shape of replacement — though note A2 retires those two
figures rather than repairing them, so those checks would be guarding against their *return*.

### D6 — CONFIRMED on the defect and on "4 of 7"; **WRONG** on "unscored 23 → 25"

**Method.** Read `coverage6.py:74`. Demonstrated that a crashed script exits non-zero. Ran
`coverage6.py`. Then re-ran its mutation loop myself, capturing `verify6.py`'s `RESULT:` line and
the identity of every failing check for each of the 9 targets.

**Value.**
- **"Any non-zero exit scores as a catch":** confirmed. Line 74 is
  `(caught if res.returncode != 0 else missed).append(...)`. An uncaught exception exits 1; a missing
  target exits 2 with `RESULT: 0 checks ran`. Both are credited as CAUGHT, so a crashed harness would
  score 100%.
- **Current state:** `coverage: 6 of 9 uniquely-locatable spec figures are protected (67%)`, with
  **25** further figures unscored.
- **"Coverage becomes 4 of 7":** confirmed. No target crashes today, so scoring on
  `RESULT: N checks, M failed` with `M > 0` alone changes nothing. Crediting by `OUT` key does: of the
  6 CAUGHT, only **4** fail a check keyed to the figure that was mutated — `devastation cost in
  ducats`, `band containing alpha=2`, `coal activation wealth delta`, `change_price by tree`. The
  other two are mis-credits: mutating `widest band on [1,8]` corrupts the same "1.65" site that
  `band containing alpha=2` owns, and mutating `richest single province` trips `spec: max base_tax
  province`, a check keyed to `ROWS_MAXPID`, not to that figure. Dropping those two from the
  denominator leaves **4 caught + 3 genuinely missed = 4 of 7**. Exact.
- **"unscored 23 → 25" is wrong.** The unscored (ambiguous) count is **already 25 today** — printed
  by `coverage6.py` itself and reproduced by my own re-implementation of its target/ambiguous
  partition. The two figures the fix removes from the denominator must go somewhere, so the fix takes
  it **25 → 27**.

**Correct value: unscored 25 → 27.**

### D7 — CONFIRMED

**Method.** Read `coverage6.py:14–23` and `verify6.py:17–18`.

**Value.** `coverage6.py` reads `measure6.out` from disk (`OUTF = os.path.join(HERE, "measure6.out")`,
then parses tab-separated lines) and exits if it is missing. `verify6.py` does
`import measure6 as M`, recomputing in-process — its own comment says *"importing runs the
measurement pass"*. The two can silently disagree whenever `measure6.out` is stale: `coverage6.py`
would aim its mutations at figures from an old field while `verify6.py` checks against the current
one. Importing `measure6` in `coverage6.py` removes the divergence, at the cost of one extra
measurement pass per run. Nothing else in the tree reads `measure6.out`, so the file read can go.

### D8 — CONFIRMED

**Method.** Read `solver.py:79` and `solver.py:145,148`; evaluated the proposed behavioural assertion
over the whole province table.

**Value.** After A4, `STATE_TAX_MOD == {}`, so `for k in STATE_TAX_MOD: …` executes **zero**
iterations and asserts nothing — the defect is real by construction. The proposed replacement holds:
`r["tax"] == TAX_COEFF · base_tax(r)` on **2,472 of 2,472** counted provinces, **0** failures. It is
also the right shape of test, because it reads the value the solver actually produced rather than the
declaration it was produced from.

### D9 — CONFIRMED on the branches; the floor value reproduces, its denominator does not

**Method.** Computed, for every solve, the count of zero-reduced-cost arcs outside the support, the
max flow on the relevant arcs, and the minimum **positive** reduced cost. Swept a 300-solve battery:
ten wealth fields (baseline, razed `hangzhou`, razed `beijing`, coal-repriced, Europe ×1.02/×1.56/
×2.00, three ±1% noise seeds) × (1 aggregate + 29 per-good).

**Value.**
- **"Would halt on `paper` today, on correct behaviour":** confirmed. Under the shipped `TIE_COST`,
  `paper` is the **one** good carrying a zero-reduced-cost arc outside the support (1 arc). A check
  written as "halt if the minimum reduced cost ≤ tolerance" reads 0 ≤ 1e-10 and halts, on a solve
  that is behaving correctly. The three-branch form — halt if the minimum *positive* rc ≤ tolerance;
  report if rc = 0 with zero max-flow; halt if rc = 0 with positive max-flow — distinguishes the
  degenerate-but-unused arc from a genuine alternative optimum, which is the right distinction.
- **Floor 2.498e-08:** reproduces. The minimum over my battery is **2.49792e-08**, on
  `Europe ×1.56 / wool`. **Its scope is load-bearing and is not the obvious one.** Over the 30
  baseline b-vectors the floor is **3.76481e-08** (`copper`); over the 701-point α_Φ grid it is also
  3.76481e-08; over the three ±1% noise seeds it is again 3.76481e-08. **2.498e-08 is produced only
  by the European-development-scaled fields.** A scope statement naming the α sweep, the per-good
  solves and the noise seeds without naming the Europe-scaled fields attributes the floor to a
  battery that does not yield it.
- **"over 124 solves" is unmeasurable.** My natural battery is 300 solves; the baseline battery is
  30; the α grid is 701. I could not construct a 124-solve battery, and no script in `scripts/`
  enumerates one. The source that would settle it is the instrument that produced the figure. The
  *value* is sound; the denominator should be replaced with the battery actually run, or dropped.

### D10 — CONFIRMED as a gap

**Method.** Grepped the tree for negative fixtures; read §2.9's build order (L1318–1327).

**Value.** Nothing in the tree tests that the harness goes red when it must. `mutate6.py` and
`coverage6.py` both test that a **wrong figure** is caught; neither tests that a **broken check** is
caught — which is precisely the class D1, D3, D4 and D6 all belong to, and all four were found by
reading rather than by running. §2.9's build order lists per-tick assertions for the solver and the
§2.7 probe session for memory, and contains no harness-self-test item.

The four proposed fixtures each map onto a defect confirmed above and each would have caught it:
unscannable needle → **D3** (`spec: sources` passes with 0 scan sites); removed locator → **D4**
(demonstrated: 28 checks, 0 failed, exit 0); RESULT-less stub → **D6** (a crash scores as a catch);
cross-figure mutation → **D6** (`widest band` credited for `alpha band`'s failure). No figure to
check.

---

## Summary

**47 rows. 41 CONFIRMED · 4 WRONG · 2 split (one half CONFIRMED, one half UNMEASURABLE).**

| verdict | count | rows |
|---|---|---|
| CONFIRMED | 41 | A1–A5, B1–B13, B17–B19, C1–C12, D1–D5, D7, D8, D10 |
| WRONG | 4 | **B14, B15, C13, D6** |
| CONFIRMED / UNMEASURABLE split | 2 | **B16** (425 confirmed, ~2,249 unmeasurable), **D9** (2.498e-08 confirmed, "124 solves" unmeasurable) |

### The WRONG rows, with correct values

| row | row claims | measured |
|---|---|---|
| **B14** | Europe scaling uniform over **×1.974–×2.457** | **×1.973–×2.456**. At ×1.973 the set is already the three European ends; at ×2.457 it is `{genua, rheinland}` — two ends, so the stated upper endpoint is false. Width 0.483 and every other clause are right. |
| **B15** | **seven** of §1.6's figures change under a different sweep key | **10 of 22** tested (8 if the three source figures count as one sentence): sources, source `c_w` ranks, source mean degree, per-good sinks, connectivity, self-coherence, Cape ordered pairs, Europe→sink pairs, and both long routes. |
| **C13** | all **63** v5 rows are present in `fixes-agreed.md` | **62.** §5 says "62 items", has 62 rows and 62 distinct `X###` ids, and its action tally sums to 62. Y012's own arithmetic (22 + 39 + 1) also gives 62. |
| **D6** | unscored **23 → 25** | **25 → 27.** The unscored count is already 25 today; the fix moves two mis-credited targets out of the denominator, so it rises to 27. "Coverage becomes 4 of 7" is right. |

### Unmeasurable, with the source that would settle each

- **B16's ~2,249.** Candidate denominators I measured span 617 to 10,264 and none lands on 2,249; the
  closest reconstruction is 2,033. Settled by the instrument that produced it — no script in
  `scripts/` computes it.
- **D9's "124 solves".** The floor value 2.498e-08 reproduces exactly (Europe ×1.56 / `wool`), but no
  battery I can construct has 124 solves. Settled by the instrument that produced it.
- **B1's "seven measured attempts failed the same way"** and **B4's "v4.0 alone"** are claims about
  process and superseded documents, not about the world.

### Correction to my own first-pass figure

**B18's bracket.** My first pass reported (9.840, 10.080] from an upstream-presence test. The upper
bound was wrong: the sender-side `already_sent` field finds `MAI` in `rheinland` propagating at
province power **10.038**, a case the single-source filter had excluded. **Corrected bracket:
(9.840, 10.038]**, which contains 10. Both endpoints of the validation agent's (5.01, 10.04] sit on
values in this same save, so the two are most likely the same evidence swept to different depths
rather than independent measurements — their upper bound is right and mine was wrong, my lower bound
is right and theirs is loose. The bracket still rests on a second gate (target eligibility) that the
defines do not describe, so "= 10, measured" remains the wrong thing to write.

### Rows where the correction is right but the change is already applied

- **B19.** 90.6% (5,723 of 6,320) and 55.1 / 54.8 are correct, and the frozen spec already carries
  them at all four sites. The "from" values 90.5, 55.2, 55.0 appear nowhere in the document.
- **C7.** 2,320 / 0 / 0 / 0 all correct, and §1.1 L181–184 already says exactly this.
- **C8.** "Well under half" survives only inside its own retraction; it is nowhere asserted.
- **B5's "1–8 → 2–8".** §2.8 L1279 already reads "2 to 8"; no site still says 1–8.

### Rows better founded than they claim

- **B1.** The Scale paragraph's exponents are wrong by 10³ — 22 flips occur at ×10⁻⁷, not ×10⁻⁴;
  96 at ×10⁻⁹, not ×10⁻⁶. The flip counts and sink sets are right.
- **A2.** The 16/5 split is a *spelling* artefact: 16 of the 21 provinces spell it `unrest` and 5
  spell it `revolt_risk`, and those 5 are the Shirvan ones. All 21 are authored; none is runtime; 10
  are Shirvan-owned. The Sofala comment is from a 1515 dated block. 9.40 is arithmetically exact but
  is the authored-basis cost of the `unrest`-spelled 16, quoted against 12.23's save basis.
- **B13.** All four §3.13 calibration figures are wrong on the v6 field, not merely unmaintained:
  span 1..6 (not 1..5), spearman −0.395 (not −0.20), cloves reach 99.9975% (not 99.97%), pruned mass
  0.147% (not 0.18%).
- **B14.** The table's widest row, ×1.38–×1.95, is not uniform at 0.001 resolution — it carries four
  distinct sink sets. Its headline claim is an artefact of coarse bisection.
- **B17.** The 22-node scaling produces no sole sink up to ×25, not merely ×20; and the eastern four
  hold a sink at no multiplier tested, so the clause is invented as the row says — the reason there
  is no sole sink is `rheinland`.

### Sites a rendering-grep cannot reach

Swept every scientific-notation token and every rendering of each figure the batch touches, rather
than grepping per figure. Three failure classes, each with a live instance in this document.

**1. Non-ASCII rendering.** §3.13's spearman is written **`−0.20` with U+2212 MINUS SIGN**, not an
ASCII hyphen. `grep -- "-0.20"` returns nothing, and ASCII `-0.20` appears **nowhere** in the spec. My
own first sweep reported it ABSENT for exactly this reason. B13 *drops* that figure, so a sweep that
cannot find it leaves it standing. The margin figure is the same class: L1080 renders it `3.765e-8`
where a pattern written `3.765e-08` cannot match.

**2. The same digits belonging to a different figure.** L1612 carries `6320` **without a comma**,
inside a retraction of v1's superseded Laplacian figure `6245/6320` — on the *same line* as the live
`(5,723 of 6,320)`. A sweep for `6320` returns two hits on one line and one of them must not be
touched: it is a quoted retraction whose point is that it is wrong. `verify6.py`'s `every_site`
pattern `([\d,]+) of 6,320` happens to dodge this by requiring the comma, which is luck rather than
design. Same trap on **`232`**: it is B5's barbell denominator (L1279) *and* B6's supports denominator
(L1064) — two independent claims. B6 removes its 232; B5 keeps its own.

**3. Derived figures on an adjacent line.** C1's `105.30` occupies L21, L235 and L1751, but the
percentages derived from it — `0.98%` and `0.99%` — sit on **L22** and **L236**, and the `89`
decomposition on **L238–L240**. A line-oriented grep for `105.30` finds three lines and none of the
four dependent numbers. *(All of them check out: `apparatus6.py` gives 0.98% and 0.99%, and
43 `gems` + 31 `incense` + 16 province-keyed − 1 overlap = **89**, the overlap being province **542**
at `gems` and province **4856** rolling `incense`, exactly as L238–L240 state. Measured: 20 counted
provinces carry an unknown good and all 20 resolve from the save; 43 gems and 31 incense counted; the
16 province-keyed apparatus pids are all counted.)*

**Two more dependent sites in this batch.** B14's table has a **prose restatement** at L604–606 —
*"the widest single interval in the table — ×1.38 to ×1.95 — is three European ends with nothing in
Asia"*, plus `hangzhou` leaving at ×1.19 and returning at ×1.95 — which carries the *old* interval and
must go with the table; no grep for the new ×1.973–×2.456 can find it, because those digits are not
in the document yet. And C11's *"29 of the 59"* (L42) is a single site whose figures describe
`measure6.py`'s **output**, so no sweep of the spec can validate it — only re-running the harness can,
which is how both numbers were found wrong.

### Caveats worth carrying into the edit

- **C10.** `solver.py:235` calls `build_sc(alpha_of_good, eps)` **positionally** from inside
  `solve_all`. A keyword-only `eps` breaks it unless that line changes in the same edit.
- **C1.** The frozen table holds **22** constants, not twenty — 20 province-keyed plus 2
  trade-good-keyed.
- **A5.** Eight lines contain `unrest`, but **L1742** (§3.13) carries "four of the five" without the
  word and needs editing too.
- **B6.** The spec's "72 of 232" is permutation-seed-dependent (my 8 permutations give 48 of 232),
  which is an independent argument for the goods count the row substitutes.
- **B3, incidental.** §2.8's "`spices` from `the_moluccas` and `kongo`" is wrong — 18 nodes produce
  `spices`. `cloves` from `the_moluccas` alone is right. Outside this row's scope.
