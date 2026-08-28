# Re-validation of the v3.0 repairs in spec v4.0

**Scope.** The **29 graded claims** `validation-v3.md` left open — 10 REFUTED and 19 PARTIAL — plus
the **5 `validation-v2.md` partials** v3.0 counted in its ledger but never folded, plus the **4
systemic findings**. Claims v3.0 got right are not re-litigated here; the measured ones among them
were re-checked anyway, because the solver fix moved the wealth field underneath them (Part B).

**Method.** Two harnesses, both run against the 1.37.5.0 Inca install and the corrected reference
solver, both asserting a specific value or a specific presence/absence of text in
`v4-owner-agnostic/per-good-trade-spec.md`:

- `validate_v4.py` — **163 assertions**, one or more per repaired claim. Each names the v3 claim ID
  it clears. Where the repair is a fact, it re-derives the fact; where the repair is a wording, it
  asserts the new wording is present **and** the old wording is gone.
- `validate_v4b.py` — **40 assertions** over the spec's *untouched* measured figures, to catch
  anything that drifted with the wealth field and was not updated.

**Result: 203 assertions, 0 failed.** Every repaired claim is CONFIRMED and no untouched figure
drifted unnoticed.

---

# Summary

| Class | Count | Status after v4.0 |
|---|---|---|
| v3.0 REFUTED | 10 | **10 CONFIRMED** |
| v3.0 PARTIAL | 19 | **19 CONFIRMED** |
| v2 partials v3.0 did not fold | 5 | **5 CONFIRMED** |
| Systemic findings | 4 | **4 closed** |
| Untouched measured figures re-checked | 40 | **40 hold** |

No claim is left PARTIAL and none is REFUTED, and **no measured figure is left unverified**. The
last two markers were run rather than carried, and both failed — see Part E.

---

# Part A — the ten refutations

### W003 — CONFIRMED
**Was.** "Every refutation and partial in `validation-v2.md` is folded through" — five were not.
**Repair.** §0 now claims the fold-through over `validation-v2.md` **and** `validation-v3.md`, and
names the five it previously missed. Each of the five is repaired in place and separately validated
in Part C.
**Assertions.** The five repairs each assert new-text-present and old-text-absent: V071 (§1.8),
V075 and V076 (§1.10), V090 (§2.2), V223 (§1.6). All pass.

### W035 — CONFIRMED
**Was.** A production tooltip quoted as `+0.26 … yearly income of 3.25` against a window
`Trade Value` of 3.20 — none of which reproduces, because Granada's 1444 monarch rolls the
`Industrious` ruler personality (+10% `global_trade_goods_size_modifier`) at game start.
**Repair.** §1.3 now derives the time basis from the two invariants: the tax tooltip's
`Base: X (Yearly 12·X)` at two development levels, and the *ratio* between the window's annual
`Trade Value` and the monthly tooltip line (observed 3.52 → `+0.29`). The window figure is quoted
as one sample of a random variable and the confound is named. §2.3 reads both coefficients off the
`Base` lines only.
**Assertions.** `history/countries/GRA - Granada.txt` contains no `personality` entry (PASS);
`industrious_personality` grants `global_trade_goods_size_modifier = 0.1` (PASS); the ratio wording
is present and both unreproducible quotes are gone (PASS).

### W041 — CONFIRMED
**Was.** "In vanilla the income-relevant local modifiers are exactly three."
**Repair.** §1.3 replaces the structural shortcut with a two-test procedure — **local** (value
depends only on the province's own attributes) and **enters wealth** (modifies `goods_produced`,
`price`, or `tax_value`) — and tabulates every modifier live on a 1444 province with no owner
input, classified by both tests.
**Assertions, re-read from `00_tradegoods.txt` this session.** `local_tax_modifier` → exactly
`gems` 0.15; `trade_value_modifier` → exactly `incense` 0.1; `local_production_efficiency` →
exactly `glass` 0.1; **`local_autonomy` → exactly `chinaware` −0.1** (the fourth v3.0 missed); no
good carries a flat `trade_goods_size`. The `chinaware` row and the `bonus_from_merchant_republics`
row are both present in the spec table; "exactly three" is gone. All pass.

### W049 — CONFIRMED
**Was.** "`City` (+25%) … is constant across every province the model counts, so it cancels in the
normalised share." It does not cancel: `city` is `local_tax_modifier = 0.25`, so it multiplies only
the tax half of `tax + trade_value`.
**Repair.** §1.3 deletes the cancellation argument and replaces it with the correct account: the
engine's tax multiplier is the **sum** of the itemised percentages, `Core` 0.75 + `City` 0.25 =
1.00 is the reference condition a cored city province sits at, and that reference is what
`TAX_COEFF = 1.0` was measured at. Neither term is carried again.
**Assertions.** `city` static modifier is `local_tax_modifier = 0.25` (PASS); Garnatah's itemisation
sums 75+25+5+5+15 = 125 and Caceres's 75+25+5 = 105, matching their observed ×1.25 and ×1.05
multipliers (PASS); the cancellation sentence is gone and the absorbed-into-`TAX_COEFF` account is
present (PASS).

### W066 — CONFIRMED
**Was.** "efficiency also feeds the caravan-power and collection tooltips" — UNSOURCED, and false
for caravan power.
**Repair.** §1.7 replaces the clause with what the files support: two distinct modifier keys with
distinct ledger columns, granted separately where both appear together.
**Assertions.** `CARAVAN_POWER_DESC2` itemises "a third of your development" and "policies and
ideas" and nothing else (PASS); no English localisation line ties `trade_efficiency` to caravan
power (PASS); the clause is gone and the replacement is present (PASS).

### W124 — CONFIRMED
**Was.** "Pendant net-importers are the only sinks outside the set, and the free-edge race is the
only way a node inside it drops out." A third case exists inside the 2-core: the sweep's fallback.
**Repair.** §1.1's Phase 3 **defines** the fallback branch; the sink-placement bullet carries four
cases and names T1/T2/T3; §2.2a and §3.2 name T3 alongside T1 and T2.
**Assertions, on the constructed T3 input (`b ≡ 0` over the real 80-node map).** The fallback fires
and promotes `english_channel`, which is the highest-wealth node (PASS); the sink set is
`{english_channel}` (PASS); the orientation is complete (159/159) and acyclic (PASS); the fallback
pick is identical under five index permutations (PASS); Phase 3's definition and the `(**T3**)`
label are present in the spec (PASS).

### W144 — CONFIRMED
**Was.** "gems, silk, **wool** land exactly on 2.0."
**Repair.** §3.5 now says two — `gems` and `silk` — and records that `wool`'s largest single
negative is `history/countries/HAB - Austria.txt`'s `NEW_DRAPERIES` at −0.25, giving 1.875.
**Assertions.** Over all 154 shipped `change_price` blocks, exactly **2** goods land on 2.0 (PASS);
`wool`'s largest single negative is `(-0.25, history, NEW_DRAPERIES)` (PASS); 2.5 × 0.75 = 1.875
(PASS).

### W145 — CONFIRMED
**Was.** "three goods sit on [the boundary] exactly — the likely origin of v2's off-by-one." There
was no off-by-one to explain.
**Repair.** §3.5's parenthetical no longer diagnoses one; it states the scope that produced the
correct count and records that v2's 13 was right and v3.0's 12 came from parsing four of five trees.
**Assertion.** The invented diagnosis is gone; the scope statement is present (PASS).

### W146 — CONFIRMED
**Was.** "All 101 `change_price` blocks … were parsed; `history/` contributes only positive
entries."
**Repair.** §3.5 states **154** blocks across five trees, with the per-tree breakdown and the 13
negatives in `history/`.
**Assertions, from a fresh five-tree scan.** 154 blocks (PASS); 53 in `history/` (PASS); 13 of
those negative (PASS); the false clause is gone (PASS).

### W193 — CONFIRMED
**Was.** "2-core containment is a hard assertion, unconditional … every sink inside the 2-core lies
in `{selected} ∪ {promoted}`." On the T3 input that assertion halts on correct behaviour.
**Repair.** §2.8 and §2.9 assert containment in `{selected} ∪ {promoted} ∪ {fallbacks}` — the set
the sweep maintains — and §2.8 says explicitly why the narrower set would have halted on T3, so the
widening is part of the assertion rather than an escape clause on it.
**Assertions.** On T3, the v4 containment set has **zero** violations while the v3 set is violated
by `english_channel` (PASS, both directions); both spec sites carry the widened set (PASS).

---

# Part B — the nineteen partials

Each was narrowed to what the evidence supports, or had its evidence widened to match the claim.

| ID | Repair | Assertions |
|---|---|---|
| **W006** | Every script name updated to `v4measure.py`, and that script's sink-set comparison bug fixed so it can print the number the spec quotes. | No `v3measure` or `[unverified in v3.0]` string remains; `v4measure.py` prints `0/5` under a set comparison. PASS |
| **W027** | §1.3's formula gains the multiplicative local-modifier factor on all three terms. | Formula present; solver applies it; a gems province's tax is exactly 1.15 × `base_tax`. PASS |
| **W037** | The coefficient citation moves from one province to four, at four development levels. | Provinces 223, 1747, 212, 213 verified against `history/provinces` for `base_tax` and `base_production`; the four-province table is present. PASS |
| **W039** | "which is why they appear … as their own line" → "**consistent with** that and does not establish it". | New wording present. PASS |
| **W040** | The trade-good data model is demoted from *the* rule to *an instance* of it. | Two-test wording present; `bonus_from_merchant_republics` row present. PASS |
| **W045** | The terrain enumeration is replaced by the exact key set. | `map/terrain.txt` re-parsed: exactly the seven keys the spec now lists. PASS |
| **W086** | §1.1 and §2.2a split determinism (proved) from independence-of-indexing (measured). | Both wordings present; zero exact `(DEF, b)` ties measured across 29/29 goods; the fallback branch is scan-invariant over five permutations. PASS |
| **W101** | "1002 stack frames at a single return address" → 1002 recorded `eu4.exe` frames at a single **exception** address, three reproductions. | All three crash dumps carry 1002 `eu4.exe` frames, carry `0x00007FF6DDE6A8B4`, and carry **no** per-frame addresses. PASS |
| **W118** | "only `total` and `retention` are deterministic" → the field-level truth. | Re-derived from the two vanilla saves: `retention` identical 80/80, `total` differs on 1 of 79. PASS |
| **W121** | The 1.7× gains its measured value (×1.726). | Present. PASS |
| **W122** | "a Chinese spice sink" gains its node set — `beijing`, `xian`, `canton`, `hangzhou` — with each node's own multiplier and share. | Present, and the four China-region nodes outside the set are listed separately. PASS |
| **W131** | "two checks rather than one" is now true of three failure modes, because the containment set covers T3 rather than excluding it. | §2.8's row names T2 and T3 as the two legitimate equality failures. PASS |
| **W143** | 12 of 30 → **13 of 30**, from the five-tree scan. | 13 below 2.0, 2 on it, 4 above despite a negative event, 11 with none: 30 total. PASS |
| **W156** | Beijing (node-wealth rank 39) is replaced as the "rich non-sink" example by `genua`, `gulf_of_siam` and `sevilla`; "bends every edge" → "draws more edges in than it sends out". The same mis-cast is repaired in its three other sites — §2.8's "Razed China" row, §2.8's "Ming loses the Mandate" row and §3.9's / §3.1's razed-Beijing illustrations. | All three examples are ranks 3, 2 and 7 by node wealth, none is a `Φ_w` sink, each has in-degree > out-degree, and "Beijing, Champagne, Sevilla" is gone. Measured: zeroing `hangzhou` moves the sinks to `{doab, english_channel, gulf_of_siam}`; **zeroing `beijing` moves nothing**. PASS |
| **W158** | Rescoped from "do flat goods bonuses exist" to the question that actually matters: what else multiplies `goods_produced`, and which side of the owner line each source falls on. | New §3.13 entry present. PASS |
| **W160** | Settled and moved out of §3.13 into §1.3's table: glass's `local_production_efficiency` is local and does **not** enter wealth, because the engine books it on production income. | The classification row is present; the open question is gone. PASS |
| **W162** | Settled: `TAX_COEFF` is 1.0 at `base_tax` 2 and 6. | Both tooltips quoted in §2.3; the open question is gone. PASS |
| **W165** | §3.13's partition matched to §3.5: 13 / 11 / 2. | Present. PASS |
| **W190** | The gravity kernel's "hits any chosen end count exactly" gains its γ range. | "exactly for γ ≤ 0.7 and any count up to six" present, with the γ = 0.9 exception stated. PASS |


### W156 — the fourth site, and why it is one repair rather than four
`validation-v3.md` graded W156 on §3.9's example list. The same misidentification — Beijing as
China's wealth pole — is load-bearing in three more places, and one of them is a **falsifiable
validation expectation**: §2.8's *"Razed China | Zeroing Beijing-node development relocates the sink
in one solve"*. It does not: measured, the `Φ_w` sinks are unchanged at
`{english_channel, hangzhou}` when Beijing's node development is zeroed, and they move to
`{doab, english_channel, gulf_of_siam}` when `hangzhou`'s is. Under owner-agnostic wealth `hangzhou`
is the Chinese pole — a `Φ_w` sink, `c_w` rank 3, node-wealth rank 12, holder of the richest single
province at 27.0 — and `beijing` is node-wealth rank 39.

§2.8's *"Ming loses the Mandate | Beijing's pull collapses with its income"* fails for a second
reason and is repaired with it: the Mandate is an owner property, §1.3 reads none, so nothing moves
on the day it happens. That row is now the owner-agnosticism check it should always have been.

**Part B's second harness.** Because the solver fix moved the wealth field, `validate_v4b.py`
re-checked 40 figures v4.0 did *not* edit — the §1.1 properties, the whole `Φ_w` block, the map and
file facts, the land counts and price ratios, and the calibration's demand ranks. All 40 hold.

---

# Part C — the five v2 partials v3.0 counted but did not fold

### V071 — CONFIRMED
§1.8's universal negative — "no mechanic gates flow by range" — is replaced by the positive claim
the files support, widened to everything trade range actually gates (merchant reach, mercenary
hiring, one diplomatic precondition), and closed with an explicit statement that "no string, define
or modifier ties range to link flow" is a fact about the files and not a proof, naming the
observation that would settle it. Both the new wording and the absence of the old are asserted.

### V075 — CONFIRMED
§1.10's table row now records the ladder: maintain trails select by 5–10 points on all nine rungs
and the 5-flag carries no maintain share. Re-parsed from
`common/trading_policies/00_trading_policies.txt` this session — `{5: none, 10: 5, 15: 5, 20: 10,
25: 15, 30: 20, 35: 25, 40: 30, 45: 35}` — and asserted against the spec's list.

### V076 — CONFIRMED
"nothing absorbs threshold chatter on its own … Propagate Religion included" is replaced by the
scoped version: the flicker-risk set is every country at a single-valued limit plus **flagless**
countries at Propagate Religion's default and terminal branches. The over-broad sentence is gone.

### V090 — CONFIRMED
§2.2's unqualified "tens of milliseconds for all 29 goods" is replaced by the measured cost —
**5.7–7.3 ms per good, 0.17–0.21 s for all 29** on the reference — with the native-network-simplex
projection marked `[unverified in v4.0]` rather than asserted.

### V223 — CONFIRMED
§1.6 names the 22 European nodes. Re-measured on the corrected wealth field: ×2 gives sole sink
`genua`, ×3 reverses the Cape to `in ← {comorin_cape, malacca, zanzibar}`, `out → {ivory_coast}`,
and dev-stacking `hangzhou`'s top province ×30 gives sole sink `hangzhou`. All three land exactly,
and the 18-node reading's different thresholds are recorded in the same sentence.

*(V001, the sixth unaccounted partial, was already folded in v3.0 — the header's "final patch"
wording is gone. It is recorded in `changes-v4.md` so the ledger reconciles at 24 = 18 tabulated +
5 folded here + 1 folded silently.)*

---

# Part D — the four systemic findings

1. **The solver did not implement §1.3.** Fixed in the solver, not the spec: `solver.py` applies
   `gems` (+15% tax, 43 provinces) and `incense` (+10% trade value, 29 provinces). §2.2 item 4
   states both. World wealth 10,572.40 → **10,594.80**, and the fourteen dependent figures were
   regenerated and restated (`changes-v4.md`). Asserted: the solver's two modifier maps, the
   province counts, the 1.15× on a gems province, and the world total.
2. **`v3measure.py` could not print its own headline number.** The sorted-vs-index-ordered
   comparison is fixed in `v4measure.py`, which now prints `0 flips, 0/5 sink-set changes` — the
   figure §1.6 quotes. Asserted by re-running the check set-based.
3. **The supply-contrast premise was an ε artifact.** §3.2's "supply contrast exceeds demand
   contrast by four to five orders of magnitude" is replaced by the property that actually holds
   without v1's deleted regularizer: supply is **sparse** where demand is dense — spices are
   produced in 18 of 80 nodes and cloves in 1, while every node with an owned province carries
   demand. The old ratio is recorded as what it was. Asserted: 18 and 1 producing nodes.
4. **Stale diff statistics.** `changes-v4.md`'s statistics were computed after the last edit from
   the two files on disk: 36 paragraph groups replaced, 0 inserted, 0 deleted outright, no heading
   lost or gained, 104,457 → 114,612 bytes.

---

# Part E — the two figures §3.10 carried unverified

Both were run rather than carried forward. **Both failed**, and the first failed in kind rather
than in value. Construction: `gulf_of_siam`, 13 goods carrying local value, **12 of them sinking
there** (the "mixed sinks" the original text described, which Sevilla does not have), three
collectors with the off-home penalty on two, transfer eligibility varying per good. Script:
`scripts/factor.py`.

### The `5.7e-14` and `1.4e-14` agreements — REFUTED as measurements
`income_C(n) = Σ_g value_g(n)·collected_share(n,g)·powershare_C(n)`, and `powershare_C(n)` carries
no `g`. It factors out of the sum **algebraically**; there is nothing to measure. Measured residual:
**1.3e-16** — one unit in the last place of a double, not 5.7e-14. The quoted figures are float
residue from a construction no version of this document states, and reporting them as "verified
numerically" files a theorem as an experiment — precisely the confusion §1.1's three-way property
vocabulary was added to prevent, applied everywhere except here.
**Repair.** §3.10 now classes the factoring as true by construction and carrying no measurement,
quotes the one-ULP residual as evidence about the *implementation* rather than the property, and
records what the old figures were. §3.14's double-precision argument, which cited "its own 5.7e-14
and 1.4e-14 tolerances", is repaired with it and now states the table size in bytes.

### The `5.96 ducats on a node paying ~250` — REFUTED
No node in the model has local trade value near 250; the largest is `english_channel` at **112.6**.
The phenomenon is real, and it now has a structural cause rather than an anecdote: §1.9 reads a
node's **downstream neighbours**, and those are per good. `gulf_of_siam` has **eight distinct
downstream sets across the 29 goods** — twelve goods leave it with none at all, five drain to
`burma`, four to `{burma, canton, malacca}` — against `Φ_w`'s single `{canton}`. So per-good
propagation makes a country's power at the node stop being one number, and `powershare_C` stops
factoring out.
**What is actually true.** The node-scalar model then overstates **every** collector's income by
**0.41%** — 0.40 ducats on a node collecting 97.1 — against a 1e-16 residual in the exact case.
A systematic one-directional bias, thirteen orders of magnitude above float noise. That makes
§3.10's point better than the old figure did, and §3.15's rejection of per-good propagation keeps
its force.

**Assertions (13).** The 13/12 goods split at `gulf_of_siam`; the residual below 1e-15 and its
order of magnitude; the single-graph case preserving the identity; the 0.41% bias on all three
collectors; the 0.40-ducat total on a node collecting 97.1; `Φ_w`'s downstream `{canton}`; the
eight distinct per-good sets with their 12/5 breakdown; and the presence of the new text with the
absence of the three old figures as live claims. All pass.

**Provenance note.** These were inherited UNCHANGED claims — `claims-v3.md` files §3.10 under
C513–C530 with no delta row — so neither the v3 audit nor v4.0's first pass graded them. They were
found only because the two markers were treated as a to-do rather than a disclosure.

---

# What a claims delta for v4.0 should look like

Every proposition that changed is a replacement for a graded v3.0 claim. The paragraph-level diff
carries **0 outright insertions**, so an extraction against `claims-v3.md` should produce rows whose
`Replaces` column is never empty, covering exactly:

- the ten refuted IDs W003, W035, W041, W049, W066, W124, W144, W145, W146, W193;
- the nineteen partial IDs W006, W027, W037, W039, W040, W045, W086, W101, W118, W121, W122, W131,
  W143, W156, W158, W160, W162, W165, W190;
- the five v2 IDs V071, V075, V076, V090, V223;
- the figures the solver fix moved, which replace W057, W059, W060, W061, W062, W115, W153,
  W155, W166, W167, W168, W171, W172 without changing what any of them asserts;
- and §3.10's two figures plus §3.14's citation of them, which sit in `claims-v3.md`'s UNCHANGED
  C513–C530 and C586–C624 ranges and therefore have no v3 W-ID to name.

Two propositions in v4.0 are genuinely new rather than substitutions, and both exist because a
refutation required them: **Phase 3's fallback branch** (W124/W193/W131 could not be repaired
without defining the case the reference was already handling) and **the fallback's
scan-invariance** (§1.1's existing sentence already asserted it for "promotions and fallbacks"; the
branch it referred to now exists, and the assertion is measured over five index permutations).

**The one thing to hunt next.** Every measured figure in v4.0 now has a script behind it. What has
*not* been re-derived is the class the v1 audit never reached: §2.7's ten debugger probes, and
§2.8's rows that describe behaviour over a campaign rather than at the 1444 start
(colonisation pace, AI convergence, flip behaviour per decade). Those are the next frontier, and
none of them is checkable from files or from a start-state save.
