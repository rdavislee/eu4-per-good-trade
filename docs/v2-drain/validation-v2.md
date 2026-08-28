# Validation of `claims-v2.md` against EU4 1.37.5 and the reference solver

**Scope.** The 211 v2.0 delta claims V001–V211 **and the 19-claim v2.1 addendum V212–V230**
(the installed aggregate's change from `Φ_ord` to `Φ_w`). UNCHANGED claims.md IDs keep their
status from `../v1-laplacian/validation.md` and are not re-validated here. MODEL claims are
validated now (derivations as arguments, measurements by re-run); ENGINE from files where
possible; WORLD against the named artifact; DESIGN is OUT_OF_SCOPE; OUTCOME is DEFERRED.

**Install audited.** `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`,
**`EU4 v1.37.5.0 Inca (491d)`** (`launcher-settings.json`; `eu4.exe` 38,462,504 bytes, modified
2026-08-10). Every file value below is relative to this install.

**Documents validated.** `per-good-trade-spec.md` v2.1 (74,860 bytes) and `claims-v2.md`
(66,048 bytes), both as of 2026-08-20 12:44. Neither was edited by this pass.

**Nothing inherited.** All game data was re-extracted from the install this session (`nodes.py`,
`provinces.py`, `coastal.py`, `strings.py` re-run; fresh JSONs byte-identical to the prior
session's, SHA-256 checked). Every numerical claim was re-run from that data: `verify.py`
(33/33 pass), `drainrep.py`, `detrep.py`, `draintune.py`, `t_model4.py`, plus new scripts
`final.py`, `toys.py`, `t3b.py`, `v159chk.py`, `leftovers.py`, `graphchk.py`, `namegrep.py`,
`phiw.py`, `phiw2.py`, `phiw3.py` (session scratchpad `scratchpad/v/`). No number below is
quoted from a prior document unless the claim itself is *about* that document.

## Summary

### Counts by status

| Status | V001–V211 | V212–V230 | Total |
|---|---|---|---|
| CONFIRMED | 127 | 6 | **133** |
| REFUTED | 10 | 1 | **11** |
| PARTIAL | 17 | 7 | **24** |
| NEEDS_GAME | 7 | 0 | **7** |
| OUT_OF_SCOPE | 47 | 5 | **52** |
| DEFERRED | 3 | 0 | **3** |
| **Total** | **211** | **19** | **230** |

By type, the 175 in-scope claims are 102 MODEL, 60 ENGINE and 13 WORLD; the 52 DESIGN claims are
OUT_OF_SCOPE and the 3 OUTCOME claims DEFERRED, per the brief.

The v2.1 addendum is the more fragile of the two: **8 of its 14 in-scope claims are PARTIAL or
REFUTED**, against 34 of 161 in the v2.0 body. It is newer and less audited, and every one of its
numerical claims rests on a single 1444 snapshot of a field with a hand-calibrated exponent.

### Refuted claims, with blast radius

| ID | Claim | What is actually true | Blast radius |
|---|---|---|---|
| **V004** | Every file-settleable claim-audit correction is folded into v2. | Four tabulated corrections are still not folded, verified against the v2.1 text: **C070** (§1.7 line 180 still says "+10% trade efficiency"; the shipped comment calls `TRADE_MERCHANT_PRESENT = 0.1` a bonus on income), **C135** (§1.10 line 272 still says caravan power "is a step function on raw power" — contradicting v2's own §3.11/V167, which has it right), **C389** (§3.3 line 564 still says "negligible development but large production income"; measured gap is 1.2–1.6×), **C594** (§3.14 line 788 still says "about 0.75 MB"; at the double precision the spec's own tolerances imply, 1.5 MB). | v2.1 §1.7, §1.10, §3.3, §3.14; C070, C135, C389, C594 ride along as UNCHANGED with their v1 PARTIAL statuses still live. §1.10 vs §3.11 is now an internal contradiction. |
| **V029** | Final sinks are **exactly** `{selected ∩ flow-terminal} ∪ {promoted}` (derivation). | Not a theorem. Two counterexample classes run through a faithful generic §1.1 implementation (`toys.py`): **T1** — a pendant net-importing leaf is a sink *outside* the set and strips the selected sink of sinkhood via the Phase-4 pendant edge (actual {C}, formula {B}); **T2**, entirely inside the 2-core — a selected flow-terminal demander that pops late under DEF-ascending gains an out-arc over a free edge to an earlier-marked conduit (actual {u2}, formula {u1,u2}). Holds 29/29 on 1444 because Phase 0 is a no-op and no such race occurs. | §1.1 property 2, §3.2 claim 1, §2.8 sink row; V125, V126, C384. The runtime assertion would catch a violation, but the spec presents the identity as proved for any input while its stated target is map-agnostic. |
| **V062** | `Φ_ord` agrees with its own per-good graphs on 62.7% of edge-goods. | **60.2%** (2774/4611) under the deterministic sweep the spec itself adopts. 62.7% (2891/4611) is the superseded scan-order sweep's number, which `drain-orientation.md` §6 replaced without regenerating. v1's 52.6% (2426/4611) reproduces exactly. | **Grew under v2.1**: 62.7% now appears at §1.6 line 165, §3.9 line 679 and §3.15 line 852, and inside **V219**'s comparator. The `Φ_ord`-vs-`Φ_w` coherence gap is 60.2 vs 53.4, not 62.7 vs 53.4 — the design trade §3.9 records is ~7 points, not ~9. |
| **V107** | China holds a spice sink only under the §3.13 α-calibration. | Under the calibration, `spices` sinks at **Doab and Genoa** — no Chinese node (fresh re-run). Beijing holds the **cloves** sink, as the claim's own parenthetical says. China holds a spices-good sink in neither configuration. | §2.8 row 1 (line 452, unchanged in v2.1); V179's measured half unaffected. |
| **V125** | Sinks are the selected demand centres plus the forced flow-terminal drains (derivation). | Same failure as V029, both directions (T1, T2). The *contrast* with v1 — placement no longer set by field flatness — survives; the "exactly these and nothing else" formulation does not. | §3.2 line 541 ff.; C384. |
| **V126** | Nothing outside that set can be a sink: every other node is given an out-arc by the sweep. | Sound for the 2-core; false when Phase 0 acts. A pendant net-importing leaf (T1) is outside the set, never touched by the sweep, and has no out-arc — a sink by construction. | §3.2 claim 1's parenthetical; all modded-map behaviour. |
| **V127** | v1 never stated the four claims: sink placement, free-edge direction, reachability, aggregate acyclicity. | v1 **did** state aggregate acyclicity — **C061**: "`Φ` is a potential, so orienting edges by it is acyclic" (§1.6, extracted and CONFIRMED in v1) — and v1's ε-machinery (C453–C462) stated what decides dead-branch/free-edge direction. Genuinely unstated: the sink-placement determinant and any reachability guarantee. | §3.2 line 541; §3.16's repair narrative (V209/V210) keeps force for the two genuine gaps. V207 (the narrower claim) is CONFIRMED and is the one to keep. |
| **V134** | At α = 1.5 a 77-province node beats a 19-province node of equal total wealth by 2× purely on slicing. | Under node-level α with equal totals the two **tie** — `(ΣW)^α` is count-blind. The real distortion: node-level α overweights the 77-province node *relative to the per-province form the model defines* by `(77/19)^(α−1)` = 2.01× at α = 1.5, at equal per-province wealths. | §3.3 line 574; V133 survives under the corrected reading; V136 (DEFERRED) inherits the corrected direction. |
| **V145** | 13 of 30 goods can be pushed below 2.0 by a single vanilla `change_price` event. | **12 of 30** strictly below 2.0 — all 101 `change_price` blocks across `events/`, `decisions/`, `missions/`, `common/` parsed (`history/` adds only positive entries). Three more — **gems, silk** (−0.50 on 4.0) and **wool** (−0.20 on 2.5) — land *exactly on* 2.0, i.e. α exactly 1, which is the likely off-by-one. Grain and wine reach 0.625 ✓. | §3.5 line 598 and §3.13 line 771; V176's embedded number. V146 (11 goods with no negative event) is exactly right. |
| **V159** | Measured: 98.8% of ordered node pairs connected by ≥1 good on 1444 data. | **90.9%** (5743/6320) under DRAIN with the deterministic sweep; 90.3% under the old sweep. **98.8% (6245/6320) is v1's LAP measurement**, byte-exact — validation.md quantified C492 with the same 6245/6320. Inherited into v2 unre-measured: the exact failure mode this audit was told to hunt. | §3.8 line 658 (still present in v2.1, now phrased around `Φ_w`); C492/C498 lineage. §3.8's argument survives at 90.9%. |
| **V230** | A latent good leaves `Φ_w` unaffected: `Φ_w` reads wealth, not goods. | **The derivation is invalid and the conclusion fails.** `Φ_w` reads wealth; `wealth = tax_income + production_income`; production income reads the province's *good and its price*. A latent good activating replaces the province's trade good (`is_latent = yes`), so wealth moves. Measured: repricing the 45 owned latent-coal provinces to coal (`base_price` 10) shifts world wealth 10,572 → 10,789 and **flips 10 of 159 `Φ_w` edges**. The two sinks happen to survive. | §1.6/§2.8's "Latent good" row under v2.1; V212's independence-from-goods framing. Under v2.0's `Φ_ord` the claim was true (`V_g = 0` ⇒ no contribution); the operator change silently broke it. |

### Derivations that failed as proofs while their paired measurements passed

The §1.1 discipline — never let a measurement stand for its derivation — produced these splits.

- **V029 refuted / V030 confirmed.** The sink-set identity holds 29/29 on 1444 and fails as a
  theorem on two constructed inputs (pendant importer; DEF-ascending free-edge race).
- **V031 partial / V032 confirmed.** 100.0% reach, 29/29, zero orphans reproduces; but "the LP
  imposes node balance" proves feasibility only on a **connected** graph (or with per-component
  balance). v2 orphaned v1's per-component machinery (C013–C018) with no replacement — its own
  orphan note concedes "component handling is unstated in v2" — while targeting "map-agnostic".
  On a disconnected map with per-component imbalance the LP is infeasible outright (`toys.py` T4,
  HiGHS "model_status is Infeasible"). Vanilla is one component (measured), so 1444 hides it.
- **V016 partial** (measured support 78–79 edges ✓). "The support **is** a spanning-tree basis"
  holds only for basic/vertex optima; an optimum splitting flow across equal-length parallel
  paths has an undirected cycle in its support. Unstated premise: the solver returns a vertex
  solution (simplex family does; interior-point without crossover does not).
- **V060 partial** (order-comparison reproduces the DAG 29/29 ✓). Pendant nodes never enter the
  sweep and have no marking order, so on any map where Phase 0 acts the claim fails — and
  `Φ_ord` is undefined on pendant edges. Premise (no pendants) unstated.
- **V125 / V126 refuted** while the same formula measured exact on 1444 (V030, V108).
- **V151 partial.** "An alternating link carries near-nothing" is asserted with no argument, and
  v1's continuity argument does not port to LP supports. Empirically it held: zero
  support-membership changes moving >1e-6 flow under 1e-9 demand nudges (29 goods × 6 trials).
  In general the map b → support is discontinuous at degenerate equal-cost alternatives, so the
  claim rests on an unstated solver-selection-stability premise — the same one V183 files as open.
- **V114 partial.** Family 1 (monotone) fails by theorem ✓. Family 2's *rule* is an exact
  algebraic identity (re-verified 2320/2320), but its *failure* additionally needs the measured
  contrast gap (2.5×10⁷ vs 471) — an empirical 1444 fact. "Both failures are theorems" overstates
  the second.
- **V214 partial / V217 confirmed** *(new in v2.1)*. Scale-invariance is true in exact
  arithmetic and false in the implementation: the zero-flow tolerance is **absolute** (1e-11), so
  scaling `b` down moves flow arcs into the free set — measured 13 edge flips at ×1e-2 and 100
  flips with the sink set collapsing to `{genua}` at ×1e-6. The claim's own application
  (normalizing into (−1,1), which scales the 1444 `b_w` *up* by ~44×) is safe.
- **V230 refuted** *(new in v2.1)* — the only addendum claim where the derivation is not merely
  under-premised but points the wrong way; see the table above.

### Systemic findings (not attached to a single claim)

1. **The reference solver does not implement §1.3's autonomy floors.** `solver.py` computes
   `wealth = base_tax + 0.2·base_production·price` with no autonomy term, while §2.2 item 4
   (V087) specifies regime-dependent floors. Every measured number the spec cites — per-good sink
   sets, k-values, the barbell, 60.2%, 90.9%, the calibration table, **and now the whole `Φ_w`
   field including its two sinks and α_Φ = 1.5 calibration** — is computed on floor-less wealth.
   No claim is refuted *by* this (each claims what the reference measured), but the spec nowhere
   discloses that its "1444 data" bypasses its own §1.3 pipeline, and `Φ_w` is far more exposed
   than the per-good graphs were: it is *nothing but* the wealth field.
2. **Two stale-sweep numbers survived the deterministic-sweep switch, and v2.1 propagated one.**
   62.7% (V062) is now quoted at three spec sites and inside V219's comparator.
3. **v1's own bookkeeping is imperfect where v2 cites it**: validation.md's refuted table lists
   24 IDs while its summary says 23, and no partition of the refuted ENGINE claims yields V205's
   denominator of "fourteen" (16 typed ENGINE; 13 excluding the three derivation-provenance rows).
   The numerator (nine UNSOURCED) is exact.
4. **The addendum's measurements are reproducible but under-specified.** Three separate v2.1
   claims turn on a definition the spec never gives: "wealth rank" (V215 — matches the α_Φ-weighted
   field, not node wealth, where hangzhou is rank 12), "European node wealth" (V223 — the stated
   ×2 and ×3 thresholds land only under a 22-node reading), and which α values the sink-count
   sequence samples (V224 — reproduces exactly at α ∈ {1, 1.5, 2, 3, 4, 8}). All three are
   fixable with one sentence each.

### NEEDS_GAME items, grouped by the setup that unblocks the most at once

**A. One non-ironman save, node windows and tooltips — 3 claims.** The highest-value session:
**V054** (open one gold province's Production tooltip → settles §1.5's residual), **V067** (click
an incoming `TradeNodeLink` entry → does `NextNodeButton` accept a merchant assignment or only
navigate), **V105** (country with above-threshold power in X and zero in upstream Y: does it
appear in Y — the §3.16 cautionary case).

**B. One hand-edited `00_tradenodes.txt`, one fresh load — 2 claims.** Probe 13: author a
two-node cycle, read `logs/error.log` and the trade mapmode. Settles **V149** (engine behaviour
on a cyclic file) and **V096** (whether topological declaration order is required).

**C. One hydrated save file, no gameplay — 1 claim.** **V084** (ironman saves binary-encoded):
hydrate any ironman `.eu4` from OneDrive and read its header. Supporting but indirect: the
binary's own string "Allows local Ironman games to be saved in text format" implies a non-text
default. All 577 saves on this machine are OneDrive placeholders.

**D. Historical sources, not this machine — 1 claim.** **V043** (the 75% overseas rule is
pre-Common-Sense): settled only by the official 1.12 "Common Sense" patch notes. The 1.37.5 files
prove the rule is absent *now* (V042); they cannot prove it once existed.

*(V001's "final patch" is graded PARTIAL, not NEEDS_GAME: the install is verifiably 1.37.5.0
Inca; finality needs a Paradox end-of-support statement, which a web search did not produce.)*

---

# Part 1 — UNSOURCED claims (highest provenance risk)

### V001 — PARTIAL
**Claim.** EU4's final patch is 1.37.5 ("Inca"). *(ENGINE / UNSOURCED)*
**Method.** Read `launcher-settings.json` in the install root; checked `eu4.exe` mtime; web
search for any later patch or end-of-development announcement.
**Evidence.** `"version": "EU4 v1.37.5.0 Inca (491d)"`, `"rawVersion": "v1.37.5.0"`; exe modified
2026-08-10. Search surfaced 1.37.4 hotfix coverage (Sep 2024) and no statement that 1.37.5 is
final ([Steam news](https://store.steampowered.com/news/app/236850/view/4708039771668550388),
[Paradox forum](https://forum.paradoxplaza.com/forum/threads/eu4-hotfix-1-37-4-is-now-live-checksum-7450.1704100/)).
**What is true.** The install is on 1.37.5 Inca; that this is the *final* patch is a claim about
Paradox's future conduct that no file can confirm. Settling source: an official Paradox EOL
statement. The spec's header "Target: EU4 (final patch, 1.37.5 Inca)" is correct as a version pin
either way.

### V043 — NEEDS_GAME
**Claim.** The 75% overseas rule is pre-Common-Sense. *(ENGINE / UNSOURCED)*
**Method.** Confirmed the 1.37.5 files carry no such rule (see V042); the historical half is not
on this disk and not observable in the current game.
**Evidence.** No `overseas` autonomy modifier and no 75 floor anywhere in
`common/static_modifiers/00_static_modifiers.txt` or `defines.lua`.
**What settles it.** The official patch notes for 1.12 "Common Sense" (June 2015), which
introduced the state/territory system. Nothing on this machine can date the old rule's removal.

### V054 — NEEDS_GAME
**Claim.** Whether the per-province production-income field carries the gold figure is unknown
(§2.7 item 12). *(ENGINE / UNSOURCED)*
**Method.** File sweep for a per-province gold booking; none exists on disk either way
(`GOLD_MINE_SIZE` and `INCOMEGOLD` are country-side; `base_price = 0` kills the trade-value
path). The claim itself — that this is open — is accurate.
**What settles it.** Probe 12: one gold province's Production income tooltip in a running game.

### V067 — NEEDS_GAME
**Claim.** Whether `NextNodeButton` already accepts a merchant assignment is unknown (§2.7
item 14). *(ENGINE / UNSOURCED)*
**Method.** `interface/tradeinterface.gui` defines the widget (line 30, inside `TradeNodeLink`,
line 18) but a `.gui` file carries no behaviour.
**What settles it.** Probe 14: click an incoming-link entry in the vanilla node window.

### V071 — PARTIAL
**Claim.** Trade range gates merchant placement, not value flow — no mechanic gates flow by
range. *(ENGINE / UNSOURCED, ⚑ fix that arrived without a source)*
**Method.** Localisation and hint sweep for every trade-range string; defines sweep for range
keys; exe string sweep.
**Evidence.** `HINT_TRADERANGE_TEXT`: "Trade Range determines how far away you may send a
Merchant." `TRADE_RANGE_IRO`: "Our merchants can reach trade nodes within this range."
`TRADE_NODES_OUT_OF_RANGE`, `MAPMODE_TRADE_DESC` ("provinces … NOT in trade range") — all
placement-framed; no string, define, or modifier ties range to link flow.
**What is true.** The positive half (range gates merchant placement) is now file-evidenced. The
universal negative ("no mechanic gates flow by range") cannot be proven from files. Settling
observation: value arriving at a node chain beyond every country's trade range in a running game.

### V072 — CONFIRMED
**Claim.** There is no trade "supply range" in the engine; the only supply-range constructs are
naval. *(ENGINE / UNSOURCED, ⚑)*
**Method.** Swept `defines.lua`, all localisation, and the full exe string table (137,820
strings, re-extracted this session) for supply-range constructs.
**Evidence.** `NAVAL_SUPPLY_RANGE = 150` ("Supply range for ships") is the only define; the only
matching strings are `(Not in supply range)`, `NAVAL_SUPPLY_RANGE`, `SHIP_SUPPLY_RANGE`,
`update_supply_range` — all naval. Consistent with validation.md's refutation of C101.

### V084 — NEEDS_GAME
**Claim.** Ironman saves are binary-encoded. *(ENGINE / UNSOURCED)*
**Method.** Exe string sweep; attempted save inspection (all 577 saves are OneDrive placeholders).
**Evidence (indirect).** Binary strings "Allows local Ironman games to be saved in **text
format**" and "Local Ironman games are now saved in" imply the default ironman format is
non-text. No `EU4bin` magic found as a contiguous exe string; no save readable to check.
**What settles it.** Hydrate one ironman `.eu4` and read its leading bytes (expected `EU4bin`).

### V096 — NEEDS_GAME
**Claim.** Whether the engine requires topological declaration order is open (§2.7 item 13's
companion). *(ENGINE / UNSOURCED)*
**Method.** File fact established fresh: the shipped file is sorted, 0/159 violations (V095) —
consistent with a requirement but not proof of one (validation.md's C234 said the same).
**What settles it.** Probe 13's file edit: reorder two nodes against topological order, load,
read `logs/error.log` and the trade mapmode.

### V105 — NEEDS_GAME
**Claim.** Whether power appears upstream where the country holds none is unknown (§2.7 item 15).
*(ENGINE / UNSOURCED)*
**Method.** The receiving-side qualifier exists in the engine's own tooltip (V073, verbatim);
what it *does* is not on disk.
**What settles it.** Probe 15: a country with above-threshold power in X and zero provincial
power in upstream Y — does it appear in Y's power list?

### V149 — NEEDS_GAME
**Claim.** The engine's behaviour on a cyclic node file is unverified and load-bearing. *(ENGINE
/ UNSOURCED)*
**Method.** The format half is settled (V148: the file is a list of named directed links with no
acyclicity constraint — a cycle is expressible). The engine's reaction is not on disk.
**What settles it.** Probe 13: hand-author a two-node cycle in `00_tradenodes.txt`, load fresh,
read `logs/error.log` and the trade mapmode. Settles V096 in the same run.


---

# Part 2 — Claims sourced to a prior document or a numerical test (re-derived, not inherited)

All numbers in this part were recomputed this session from freshly extracted install data.

### V002 — CONFIRMED
**Claim.** v1's sink placement was topological rather than economic. *(MODEL / numerical test)*
**Method.** Re-ran the entire diagnosis chain from source: `verify.py` (fresh) reproduces the
exact sink criterion on 2320/2320 (good, node) pairs, CF1 (uniform demand → saxony still a
sink), CF2 (uniform supply → sinks jump to top demand nodes), the D-threshold bisection
(f = 1.725), and the contrast gap (V117).
**Evidence.** All 33 verify.py checks pass on fresh data; see V116–V121 for the pieces.

### V003 — CONFIRMED
**Claim.** The orientation core was replaced by DRAIN after a four-operator bake-off. *(WORLD)*
**Method.** Checked the artifacts: `flow-orientation.md`, `ranked-orientation.md`,
`basin-orientation.md` (v1 dir) and `drain-orientation.md` (v2 dir) — four candidates tested
against the Laplacian incumbent, scorecard in drain-orientation §4, verdict adopting DRAIN.
**Evidence.** The four documents exist and carry the recorded bake-off; their headline numbers
re-verify fresh (verify.py 33/33).

### V004 — REFUTED
**Claim.** Every claim-audit correction from validation.md settleable from files is folded into
v2. *(WORLD / stipulated)*
**Method.** Walked validation.md's REFUTED table (24 rows) and its PARTIAL table (25 rows with
quoted spec changes); checked each correction against the v2 spec text.
**Evidence.** Folded: C037/C038 (autonomy floors), C049/C050 (gold), C101, C128, C129, C130/C131/
C132, C139, C407, C433/C434, C447, C486, C487/C488, C532, C537, C538, C542, C549–C555, C550,
C158, C176, C234, C671, C676 — all present in v2. **Not folded, though file-settled and
tabulated with quoted corrections:**
- **C070**: v2 §1.7 still reads "A merchant present gives +2 trade power and **+10% trade
  efficiency**"; the audit found the shipped comment describes `TRADE_MERCHANT_PRESENT = 0.1` as
  a bonus on income, and efficiency-vs-income is a real mechanical difference.
- **C135**: v2 §1.10 still reads "It is a **step function on raw power**"; the audit found caravan
  power is not a function of trade power at all (dev/3 + modifiers, clamped [2,50] — which v2's
  own §3.11/V167 states correctly, so §1.10 now contradicts §3.11).
- **C389**: v2 §3.3 still reads "a sugar island has **negligible development but large production
  income**"; the audit measured the price gap at 1.2–1.6× grain, not multiples.
- **C594**: v2 §3.14 still reads "about **0.75 MB**"; at the double precision the spec's own
  tolerances imply, the table is 1.5 MB.
**Blast radius.** v2 §1.7, §1.10, §3.3, §3.14; the four C-IDs ride along as UNCHANGED with their
v1 statuses (PARTIAL) still applicable.

### V013 — CONFIRMED
**Claim.** k = 1 for 27 of 29 goods at defaults. *(MODEL / numerical test)*
**Method.** Fresh baseline run (`final.py`, `drainrep.py`): k per good from Phase 1.
**Evidence.** k=1 for 27 goods; k=2 for livestock (8 clusters, HHI 0.64) and salt (7 clusters,
HHI 0.53).

### V028 — CONFIRMED
**Claim.** Measured: acyclic 29/29 goods on 1444 data. *(MODEL / numerical test)*
**Method/Evidence.** Fresh run: `has_cycle` returns none for all 29 per-good orientations
(deterministic sweep). This is the measurement for property 1; the derivation is V026/V027.

### V030 — CONFIRMED
**Claim.** Measured: 1–8 sinks per good, mean 3.6. *(MODEL / numerical test)*
**Method/Evidence.** Fresh run: min 1 (cocoa), max 8 (livestock), mean 3.59 ≈ 3.6. Promotions
1–8 per good, zero fallback promotions (the stall lemma held empirically again, 0/29).

### V032 — CONFIRMED
**Claim.** Measured: 100.0% of demand reachable from supply, 29/29 goods, zero orphan sinks.
*(MODEL / numerical test)*
**Method.** Fresh run: demand-weighted BFS reach from each good's supply nodes over its final
orientation; orphan = sink with demand not reached.
**Evidence.** Reach ≥ 1 − 1e-12 on 29/29; orphan sinks 0. Measurement only — the paired
derivation V031 is PARTIAL (connectivity premise), and this pass does not repair it.

### V035 — CONFIRMED
**Claim.** Measured: zero orientation changes under scheduler permutations; zero exact key ties.
*(MODEL / numerical test)*
**Method.** Two independent tests, fresh: (a) `detrep.py` — old scan sweep flips 767/501
edge-good orientations under two scan permutations; the priority sweep flips 0 under permuted
index tie-breaks; (b) `final.py` — 2 random permutations of the index key × 29 goods: 0 flips;
exact (DEF, b) ties on free edges: 0.
**Evidence.** As stated. The index key never decides on 1444.

### V037 — CONFIRMED
**Claim.** The LP is deterministic — six identical solves produced one orientation. *(MODEL /
numerical test)*
**Method/Evidence.** Six back-to-back `run_drain` calls on identical spices input: one
orientation (tuple-identical edge set). Same-machine determinism only; cross-machine is V183's
open question (OUT_OF_SCOPE here).

### V041 — CONFIRMED
**Claim.** Exactly one node has b = 0 exactly at 1444: `cape_of_good_hope`. *(MODEL / numerical
test)*
**Method/Evidence.** Fresh scan of b = s − c over all 29 goods × 80 nodes: cape is b == 0.0 for
all 29 goods; no other node hits exact zero for any good.

### V062 — REFUTED
**Claim.** `Φ_ord` agrees with its own per-good graphs on 62.7% of edge-goods, against 52.6% for
v1's Φ. *(MODEL / numerical test)*
**Method.** Recomputed both sides fresh: `Φ_ord = Σ V_g·order_g` from the deterministic sweep's
orders, compared per (edge, good) against the per-good orientations; v1's Φ from the Laplacian
pipeline against its own per-good graphs.
**Evidence.** DRAIN deterministic: **2774/4611 = 60.2%**. v1: 2426/4611 = 52.6% ✓. The cached
pre-deterministic output shows 2891/4611 = 62.7% — the old scan-sweep number, which
`drain-orientation.md` §6 superseded without regenerating §1.6/§3.9.
**What is true.** 60.2% under the spec's own adopted sweep; still better than v1's 52.6%.
**Spec text to change.** §1.6: "agrees with its own per-good graphs on 62.7% of edge-goods";
§3.9: "agrees with its own per-good graphs on 62.7% of edge-goods on 1444 data".
**Blast radius.** V062 only; C509/C510 (measure-don't-assume) unaffected.

### V106 — CONFIRMED
**Claim.** Baseline: spices sink at Genoa (demand rank 1) + Australia, Brazil; cloves at Venice,
Kongo, Australia, Brazil. *(MODEL / numerical test)*
**Method/Evidence.** Fresh run: spices sinks = genua (c rank 1 of 80), australia (65), brazil
(73); cloves = venice (7), kongo (55), australia (63), brazil (71). Exact match, including
Genoa's demand rank.

### V107 — REFUTED
**Claim.** China holds a spice sink only under the §3.13 α-calibration option (which puts cloves
at Beijing). *(MODEL / numerical test)*
**Method.** Re-ran the calibration configuration (k_exp = 2, α unclamped, ρ = 0.5, tol = 3e-4,
deterministic sweep) for all 29 goods.
**Evidence.** Calibration spices sinks: **doab, genua** — no Chinese node. Beijing is the sink
for **cloves** (α = 16), exactly as the parenthetical says. Baseline spices sinks contain no
Chinese node either (V106).
**What is true.** Under the calibration a Chinese node (Beijing) holds the *cloves* sink; the
good `spices` sinks at Genoa and Doab; China holds a spices-good sink in neither configuration.
**Spec text to change.** §2.8: "**China holds a spice sink only under the §3.13 α-calibration
option** (which puts cloves at Beijing)" → "Beijing holds the cloves sink under the §3.13
α-calibration option; the spices good itself sinks at Genoa and Doab there."
**Blast radius.** §2.8 row 1; V179's measured half unaffected.

### V108 — CONFIRMED
**Claim.** Sinks are `{selected ∩ flow-terminal} ∪ promoted`, 1–8 per good; 14% top demand
decile vs 7% bottom — a barbell. *(MODEL / numerical test)*
**Method/Evidence.** Fresh: sink set equals the formula 29/29 *on this data*; counts 1–8;
P(sink | top demand decile) = 14.1%, P(sink | bottom decile) = 6.9% — "14% vs 7%" ✓. (As a
measurement this is sound; the formula's general proof is V029, refuted.)

### V115 — CONFIRMED
**Claim.** The tested s − c operator: demand had to increase at every hop, one sixth of world
demand unreachable, Genoa a cloves sink cloves could not reach. *(MODEL / numerical test)*
**Method.** Fresh verify.py RANK block + direct cloves check (`leftovers.py`).
**Evidence.** Mean reach 83.29% (unreachable 16.7% ≈ one sixth); 34/387 orphan sinks; genua is a
RANK cloves sink and is unreachable from the sole cloves source (the_moluccas). Monotonicity is
C370's theorem (unchanged).

### V116 — CONFIRMED
**Claim.** v1's sink rule is exactly `(c−s)/deg > mean(neighbour φ) − min(neighbour φ)`,
verified on every (good, node) pair. *(MODEL / numerical test)*
**Method.** Re-derived the identity (it is algebra: the Laplacian row gives
φ(n) = mean(nbr φ) + (s−c)/deg, and sink ⟺ φ(n) < min(nbr φ)) and re-verified numerically.
**Evidence.** verify.py fresh: "sink criterion exact — 2320/2320". Both the derivation and the
measurement stand.

### V117 — CONFIRMED
**Claim.** Supply contrast (10⁷) exceeds demand contrast (10²–10³) by four to five orders.
*(MODEL / numerical test)*
**Method.** Recomputed on the v1 solve's actual inputs: ε-floored supply (ε = 1e-6 ⇒ floor
ε/N = 1.25e-8) vs demand over demand-positive nodes.
**Evidence.** Spices: supply max/min = **2.52×10⁷**; demand max/min⁺ = **471.5** (matches the
diagnosis α-table's 471.5 at α = 1.5). Gap ≈ 5.3×10⁴ — four to five orders. ✓

### V118 — CONFIRMED
**Claim.** v1's sinks landed where the field was locally flat, not where demand was. *(MODEL /
numerical test)*
**Method/Evidence.** Follows from V116 + V117, both re-verified, plus CF1/CF2 fresh: deleting
demand variation leaves saxony a sink (CF1); flattening supply moves sinks onto top demand nodes
(doab, gulf_of_siam, hangzhou, wien — CF2). The mechanism reproduces end to end.

### V119 — CONFIRMED
**Claim.** Under v1, the highest-demand node in the game was never a spices sink. *(MODEL /
numerical test)*
**Method.** Fresh v1 solve: genua holds the highest spices demand (c = 0.03508, rank 1); sink is
saxony. Diagnosis's α-ladder: within v1's admissible clamp (α ≤ 3.0) sinks are saxony/rheinland —
never genua.
**Evidence.** As stated. Note: at the *unclamped* diagnostic α = 6, genua does appear as a spices
sink — outside v1's model space (α_max = 3.0), so "never" holds where v1 can actually operate.

### V120 — CONFIRMED
**Claim.** Under v1, a node with literally zero demand outranked Genoa and Beijing. *(MODEL /
numerical test)*
**Method/Evidence.** Fresh: cape_of_good_hope has c = 0 exactly (no owned provinces) and its
spices φ = +0.0618 sits above 66 of 80 nodes — above beijing (+0.0349) and genua (−0.0585). The
potential v1 treats as "flow toward demand" ranks a zero-demand node above the two richest
markets.

### V121 — CONFIRMED
**Claim.** Deleting demand variation entirely left the v1 sink unmoved. *(MODEL / numerical
test)*
**Method/Evidence.** CF1 fresh (verify.py): uniform demand ⇒ sinks {amazonas_node, baltic_sea,
patagonia, saxony, valencia, white_sea} — saxony, the spices sink, persists (five flat-field
nodes join it; the claim's point — demand variation is not what places the sink — stands).

### V123 — PARTIAL
**Claim.** Better wealth inputs move v1's threshold by 1.7× where 4–5× is needed. *(MODEL /
numerical test)*
**Method.** Re-derived the D-threshold bisection (verify.py fresh: f = 1.725 for Genoa to become
a co-sink) and re-read diagnosis §5–6 for the input-plausibility bound.
**Evidence.** f(genua co-sink) = 1.725 ✓; autonomy corrections plausibly deliver 1.4–2×; Chinese
nodes need **3.6–4.8×** (9.5–21.4% of world spice demand at one node); displacing saxony needs
4×; genua-sole-sink 10×.
**What is true.** The compression drops two things: (a) the measured China requirement is
3.6–4.8×, not "4–5×"; (b) diagnosis §5 concludes better inputs *can plausibly deliver* the 1.725×
that makes Genoa a co-sink — i.e., inputs could have bought the flagship European sink under v1;
what they cannot buy is demand-determined placement or a Chinese sink. V122's conclusion
survives; this sentence overstates it.
**Spec text to change.** §3.2: "better wealth inputs move the threshold by 1.7× where 4–5× is
needed" → "better wealth inputs plausibly deliver ~1.7× — enough to make Genoa a co-sink, not
enough for demand to determine placement: a Chinese sink needs 3.6–4.8×."

### V127 — REFUTED
**Claim.** v1 never stated the four claims now stated and checkable: sink placement, free-edge
direction, reachability, aggregate acyclicity. *(WORLD / stipulated)*
**Method.** Searched v1's spec and claims.md for each of the four properties.
**Evidence.** v1 stated aggregate acyclicity outright — **C061: "`Φ` is a potential, so orienting
edges by it is acyclic"** (§1.6; extracted, validated CONFIRMED in v1) — and v1's ε-claims
(C453–C462) stated what decides dead-branch/free-edge orientation. v1 did lack a sink-placement
determinant (it stated only the max-principle necessary condition, orphaned C380/C381) and any
reachability guarantee.
**What is true.** Two of the four were genuinely unstated (sink placement determinant,
reachability); two were stated in some form (aggregate acyclicity fully; free-edge direction as
the ε mechanism).
**Spec text to change.** §3.2: "The four claims v1 never stated, now stated and checkable" →
name only sink placement and reachability as unstated; credit C061 for the aggregate.
**Blast radius.** §3.2 list; §3.16's repair narrative (V209/V210) keeps its force for the two
genuine gaps; V207 unaffected.

### V128 — CONFIRMED
**Claim.** The 1444 Cape has s = c = 0 exactly. *(MODEL / numerical test)*
**Method/Evidence.** Fresh: cape_of_good_hope is the only node with s = 0 and c = 0 for **all**
29 goods (it holds zero owned city provinces at 1444.11.11). Replaces C367/C368's "almost no
wealth" with the exact statement — fix landed.

### V129 — CONFIRMED
**Claim.** A conduit node (s = c = 0) carries flow through: Cape in- and out-degree nonzero for
all 29 goods. *(MODEL / numerical test)*
**Method/Evidence.** Fresh: cape in-degree > 0 and out-degree > 0 in all 29 final orientations.

### V131 — CONFIRMED
**Claim.** The flow routes 24% of world spice supply through the Cape. *(MODEL / numerical test)*
**Method/Evidence.** Fresh verify.py: malacca→cape spices flow arc carries **0.242959** of world
supply (the LP certificate's arc value). v1's potential never used the Cape at all (V120's φ
ranking; diagnosis).

### V138 — CONFIRMED
**Claim.** In v1, substituting production income broke the α = 1 identity: agreement collapsed
from 159/159 to 68/159. *(MODEL / numerical test)*
**Method.** Re-ran `t_model4.py` (the original C424 test): rebuilds φ₀'s supply with a realistic
owner-dependent factor `(1 + production_efficiency) × (1 − autonomy)` per province and compares
against Φ at α = 1.
**Evidence.** rel. residual **1.512e+00** (vs 1.959e-15 with trade-value supply); orientation
agreement **68/159**. Note the substitution must model the owner factors: in the proxy dataset
raw production income ≡ trade value (gp × price), and substituting *that* changes nothing
(159/159, checked) — the 68/159 is the owner-factor experiment, as validation.md C424 records.

### V143 — CONFIRMED
**Claim.** Both of v1's figures (grain 1.25, livestock 1.00) were price/P₀ ratios misread as
prices. *(WORLD / derivation)*
**Method.** v1 spec line 389 ("grain lands near 1.25") and C433/C434 checked against the shipped
prices (V140–V142).
**Evidence.** grain 2.5/2.0 = 1.25; livestock 2.0/2.0 = 1.00 — both figures are exactly
`base_price / P₀`. The pattern validation.md identified reproduces from the files.

### V156 — CONFIRMED
**Claim.** v1's Propagate-Religion claim was wrong and was one of only three claims carrying
`verified (method unstated)` provenance. *(WORLD / derivation)*
**Method.** Counted the provenance in v1 claims.md; checked C486's fate in validation.md.
**Evidence.** claims.md's provenance table: `verified (method unstated) | 3`; the three rows are
C485, C486, C487. C486 is REFUTED in validation.md (the gating has at least four further
conditions — reconfirmed from the shipped policy file this session, V155).

### V159 — REFUTED
**Claim.** Measured: 98.8% of ordered node pairs are connected by at least one good on 1444
data. *(MODEL / numerical test, REVISED from C498)*
**Method.** Recomputed union any-good directed reachability over ordered node pairs (80×79)
under three orientations: v1 LAP, DRAIN old scan sweep, DRAIN deterministic sweep.
**Evidence.** LAP: **6245/6320 = 98.8%** — the claimed number, byte-exact, and it belongs to
**v1's orientations** (validation.md line 5251 quantified C492 with exactly 6245/6320). DRAIN
deterministic: **5743/6320 = 90.9%**; DRAIN old sweep: 5708/6320 = 90.3%.
**What is true.** Under the v2 operator the figure is 90.9%. The v2 claim inherited v1's LAP
measurement without re-running it — the exact "inherited number" failure mode (cf. the stale
autonomy floor). §3.8's argument (any-good scopes ≈ an enormous buff) survives at 90.9%.
**Spec text to change.** §3.8: "measured, 98.8% of ordered node pairs are connected by at least
one good on 1444 data" → "measured, 90.9% (5743/6320) of ordered node pairs under DRAIN".
**Blast radius.** §3.8 final sentence; C492/C498 lineage.

### V162 — CONFIRMED
**Claim.** The value-weighted net flow `Σ_g V_g·net_g` is a flow, flows circulate, and it
measurably contains directed cycles — it cannot be installed. *(MODEL / numerical test)*
**Method/Evidence.** Fresh: orienting each edge by the sign of `Σ_g V_g·net_g` orients 159/159
and contains a directed cycle (verify.py "value-weighted aggregate net flow cyclic: True";
drainrep aggregate (a) cyclic: True).

### V177 — CONFIRMED
**Claim.** A calibration exists making sink counts track price: span exactly 1..5,
spearman(price, sinks) = −0.54. *(MODEL / numerical test)*
**Method.** Re-ran the chosen configuration (k_exp = 2, α unclamped, ρ = 0.5, tol = 3e-4) under
the deterministic sweep, all 29 goods (`final.py` Part B — the configuration is not in the
`draintune.py` grid and was rebuilt from its published settings).
**Evidence.** Sink counts span exactly 1..5; spearman(price, sink count) = **−0.539** ≈ −0.54;
acyclic 29/29; zero fallbacks. ✓

### V179 — PARTIAL
**Claim.** Unclamped α² is a demand-model decision: luxuries become court goods — Beijing,
holding the richest single province, becomes the cloves sink. *(MODEL / numerical test)*
**Method.** Re-ran the calibration (Beijing is the sole cloves sink at α = (8/2)² = 16 ✓);
ranked all provinces by the wealth proxy.
**Evidence.** The richest single province is **pid 1821 (silk, hangzhou node, wealth 27.0)**,
then pid 684 (hangzhou, 21.6); Beijing's best is pid 1816 at **19.5 — rank 3**. Under the
calibration α, hangzhou is the rank-1 cloves demander and Beijing rank 2 (drain-orientation §5's
own table says "beijing(2)"); Beijing lands the sink through the sweep because hangzhou is a
transit node, not because it holds the richest province.
**What is true.** Measurement right (Beijing = cloves sink, α = 16); mechanism clause wrong.
**Spec text to change.** §3.13: "Beijing, holding the richest single province, becomes the
cloves sink" → "Beijing — demand rank 2 under α = 16, with the rank-1 demander hangzhou serving
as a transit node — becomes the cloves sink."

### V180 — PARTIAL
**Claim.** The twig tolerance sacrifices min-cost routing on <0.03% of mass and drops one good's
reach to 99.97%. *(MODEL / numerical test)*
**Method.** Re-ran the calibration; measured pruned-arc flow mass and per-good reach.
**Evidence.** Silk reach **99.9703%** ✓ (`ohio`, silk demand share 2.97e-4, unreachable). But
(a) cloves also dips below 100% (99.9969%), so strictly two goods lose reach; (b) "<0.03% of
mass" is the **per-arc** pruning threshold (tol = 3e-4) — the *total* mass moved off min-cost
routes reaches **0.149%** of world supply on the worst good (~5.8 pruned arcs/good stack).
**Spec text to change.** §3.13: "the tolerance sacrifices min-cost routing on <0.03% of mass" →
"the tolerance re-routes arcs individually carrying <0.03% of world supply (up to ~0.15% of a
good's mass in total) and drops silk's reach to 99.97% (cloves to 99.997%)".
**Blast radius.** V197's "bounded, measured exception" wording inherits the corrected bound.

### V187 — CONFIRMED
**Claim.** Pure MCF's value-weighted aggregate contains directed cycles. *(MODEL / numerical
test)*
**Method/Evidence.** Same measurement as V162, fresh: cyclic. ✓

### V189 — CONFIRMED
**Claim.** Ranked orientation rejected: monotone, 83% of demand reachable, 34 orphan sinks,
Genoa a cloves sink cloves cannot reach. *(MODEL / numerical test)*
**Method/Evidence.** Fresh: mean reach 83.29%; orphans 34/387; genua is a RANK cloves sink and
unreachable from the_moluccas (the only cloves source). Monotonicity theorem is C370
(unchanged). ✓

### V190 — PARTIAL
**Claim.** Ranked orientation wins every sink statistic and fails the one that matters. *(MODEL
/ numerical test)*
**Method.** Recomputed the scorecard's sink statistics fresh (verify.py + drainrep).
**Evidence.** RANK wins the demand-alignment statistics against DRAIN: ρ_val +0.281 vs +0.053;
P(sink|top decile) 46.6% vs 14.1%; P(sink|bottom decile) 1.0% vs 6.9%. But RANK **loses**
net-producer sinks (9, vs 0 for LAP/DRAIN/FLOW — nine sinks that net-produce their own good) and
sink-count scale (11–17 per good vs 1–8).
**What is true.** "Wins every sink statistic" should be "wins every sink–demand alignment
statistic"; it fails reachability *and* posts nine net-producer sinks.
**Spec text to change.** §3.15: "Wins every sink statistic and fails the one that matters."

### V191 — CONFIRMED
**Claim.** Seeded basin growth rejected: 88.5% reach at its best tuning. *(MODEL / numerical
test)*
**Method.** Re-ran BASIN at its best tuning (γ = 1000, sign-corrected, 8 refinement iterations,
LAP-matched sink counts) for all 29 goods; demand-weighted reach from supply.
**Evidence.** Mean demand reach **88.5%**, goods at 100%: 0/29. (Unserved at the same tuning:
0.2206, verify.py fresh.) ✓

### V193 — CONFIRMED
**Claim.** DEF-descending free-edge priority rejected: on the certificate unmet demand is zero,
so DEF is total demand; pointing free edges into already-served subtrees strands greedy flow;
adopted key is DEF-ascending. *(MODEL / numerical test)*
**Method.** Fresh detrep.py + drainrep.py.
**Evidence.** Shared Phase-4 evaluator: old sweep 0.1206 → DEF-descending **0.1415** (strands
more) → adopted DEF-ascending **0.1252**. The argument's premise is sound: the LP certificate
serves all demand, so downstream *unmet* demand is identically zero and DEF can only be total
demand. ✓ (`run_drain(deterministic=True)` uses `defasc_beta` — the adopted key, in code.)

### V200 — CONFIRMED
**Claim.** The claim audit refuted v1's evidence standard itself. *(WORLD / derivation)*
**Method/Evidence.** v1 §3.16 carried the standard verbatim ("Every retraction ... traced to a
premise that entered through prose ... Nothing built on adjacency data, file values, or the
model's own equations failed" — the pre-patch text preserved in `v2patch5.py`'s anchor);
validation.md REFUTES C676 with the counter-evidence. The v2 quotation is accurate.

### V201 — CONFIRMED
**Claim.** At least fifteen non-prose claims failed, by three distinct mechanisms. *(WORLD /
derivation)*
**Method.** Pulled type/provenance for all 24 rows of validation.md's refuted table from
claims.md.
**Evidence.** Provenances of the refuted set: UNSOURCED 10, derivation 9, file value 3,
verified-method-unstated 1 — none prose-sourced; ≥15 holds with room. The three mechanisms
(stale patch value; transformed value reported raw; algebra instantiated unchecked) are V202–V204,
each independently re-verified below.

### V202 — CONFIRMED
**Claim.** Failure mechanism 1: file values remembered from an older patch — the 75% floor is
pre-Common-Sense; 1.37 has regime floors of 90/50/20/0. *(WORLD / derivation)*
**Method/Evidence.** The 1.37.5 floors re-verified from `00_static_modifiers.txt` this session
(V044–V047: 90/90, 50, 20, none); no 75% floor exists (V042). The "pre-Common-Sense" dating
itself remains UNSOURCED (V043, NEEDS_GAME) — v2 correctly files it as such.

### V203 — CONFIRMED
**Claim.** Failure mechanism 2: file values transformed and reported as raw — v1's grain and
livestock prices are exactly `price / P₀`. *(WORLD / derivation)*
**Method/Evidence.** See V143: 1.25 = 2.5/2.0 and 1.00 = 2.0/2.0, against the shipped
`00_prices.txt` re-read this session.

### V204 — CONFIRMED
**Claim.** Failure mechanism 3: ε preserved the α = 1 identity only if applied to φ₀'s supply as
well; implemented as written, the identity failed at 1e-5. *(MODEL / numerical test)*
**Method.** Re-ran both variants (`final.py` Part C): (a) ε = 1e-6 on each per-good s, φ₀'s
supply raw (the spec-as-written instantiation); (b) ε applied to φ₀'s supply too.
**Evidence.** (a) rel. residual **9.58e-06** — the ~1e-5 failure, which would indeed read as a
solver bug against §2.8's 1e-14 working tolerance; (b) rel. residual **1.72e-15** — identity
restored. Orientation agreement stays 159/159 in both (the residual sits on near-flat edges).

### V205 — PARTIAL
**Claim.** Nine of the fourteen refuted engine facts were UNSOURCED. *(WORLD / derivation)*
**Method.** Counted type and provenance for every refuted ID (claims.md rows, pulled fresh).
**Evidence.** Refuted ENGINE-typed claims: **16** (C037, C038, C049, C050, C101, C128, C130,
C131, C139, C407, C433, C434, C447, C486, C532, C538). Of these, UNSOURCED: **9** (C037, C049,
C101, C128, C130, C139, C447, C532, C538) ✓. Excluding the three derivation-provenance rows
(C038, C050, C131) gives 13. No partition yields 14.
**What is true.** "Nine" is exact; the denominator should be "sixteen refuted ENGINE claims"
(or "thirteen non-derivation engine facts"). Note validation.md's own summary also miscounts
(24 IDs tabulated, 23 claimed).
**Spec text to change.** §3.16: "nine of the fourteen refuted engine facts were UNSOURCED".

### V207 — CONFIRMED
**Claim.** v1 never stated what determines sink placement, so the inventory had nothing to
extract and the flaw was structurally uncatchable by claim-checking. *(WORLD / derivation)*
**Method/Evidence.** Searched v1 spec: the only sink-placement statement is the max-principle
necessary condition ("local minima occur only where c > s", line 367 — orphaned C380/C381),
which the audit validated and which did not constrain *which* c > s node wins. The determinant
(the flatness rule, V116) appears nowhere in v1's spec; diagnosis.md derived it post-hoc by
running the solver. Consistent with V127's correction: this narrower claim is the true one.

### V208 — CONFIRMED
**Claim.** The audit found the flaw only by running the solver and asking why the output looked
wrong. *(WORLD / derivation)*
**Method/Evidence.** diagnosis.md is that record (spices sink at saxony → mechanism hunt → sink
criterion → CF1/CF2); its every headline number re-verifies fresh (verify.py). The claim
accurately describes the artifact.

### V211 — CONFIRMED
**Claim.** §1.9 still does not carry the tooltip's second qualifier ("where it already has
power"), pending §2.7 item 15. *(WORLD / derivation)*
**Method/Evidence.** v2 §1.9 read in full: "A country whose provincial trade power in a node
meets the threshold receives a share of it in **every** immediately upstream node" — no
receiving-side qualifier. The engine string carries it verbatim (V073). The cautionary case is
accurately reported as open.


---

# Part 3 — Derivations, checked as arguments

A derivation passes only if the stated reasoning establishes the claim for **any** input; a proof
that holds on 1444 and not in general is refuted, and its paired measurement cannot stand for it.

### V008 — CONFIRMED
**Claim.** Phase 0 is exact, not heuristic: every removed edge is a bridge, and flow on a tree is
determined by conservation. *(MODEL / derivation)*
**Argument check.** An edge on a cycle has both endpoints kept at degree ≥ 2 by the cycle's own
edges, so iterative degree-1 peeling never removes a cycle edge — every peeled edge is a bridge,
for any graph. The flow across a bridge equals the net balance of the side it cuts off
(conservation), so the folded residual and the flow value are exact. One footnote: for a subtree
with balance exactly 0 the *flow* is determined (zero) but the *orientation* is not — "zero →
toward core" (V007) is a stipulated convention, not a consequence. Sound with that reading.

### V016 — PARTIAL
**Claim.** The flow support is a spanning-tree basis of ≤ N−1 edges. *(MODEL / derivation)*
**Argument check.** True for **basic (vertex) optima**: the network matrix is totally unimodular
and basic solutions are forests. Not true of arbitrary optima: with unit costs, two
equal-length parallel routes admit an optimum splitting flow across both — an undirected cycle in
the support, more than a forest. The claim as stated names no basicness premise; §2.2's "network
simplex or LP" makes it natural but an interior-point solve without crossover would violate it.
**Measured.** Fresh support sizes 78–79 of 159 (N−1 = 79) on all 29 goods — the premise holds for
HiGHS on this data.
**Spec text to change.** §1.1: "The support is a spanning-tree basis (≤ N−1 edges)" → add "for
the basic optimum a simplex-family solver returns".
**Blast radius.** V021's "total downstream demand" reading and V186's "~79-edge support" both
inherit the same (true-in-practice) premise.

### V017 — CONFIRMED
**Claim.** The support is acyclic by theorem: with all costs 1, any directed cycle could be
cancelled for strictly lower cost. *(MODEL / derivation)*
**Argument check.** Sound for any input: cancelling the minimum flow around a directed cycle in
the support reduces the objective by (cycle length × amount) > 0, contradicting optimality. This
excludes *directed* cycles from every optimum (undirected cycles are V016's separate issue).

### V021 — CONFIRMED
**Claim.** The flow-arc subgraph is acyclic and fixed before any free edge, so DEF has no
circularity. *(MODEL / derivation)*
**Argument check.** Given V017 the flow subgraph is a DAG, and it is fully determined by the LP
before Phase 3 touches a free edge — DEF recursion terminates and is well-defined. Note: DEF
equals *total downstream demand* exactly when the support is a forest (V016's premise);
on a non-forest DAG the recursion would double-count shared descendants.

### V026 — CONFIRMED
**Claim.** Property 1 derivation: every arc points from later-marked to earlier-marked, so
reversed marking order is a topological order. *(MODEL / derivation)*
**Argument check.** Flow arcs: the ready gate requires every flow out-neighbour marked before a
node is marked, so u→v implies order(v) < order(u). Free edges: oriented later→earlier by rule.
Promotions and the documented fallback both mark only gated nodes (cnt = 0), preserving the
invariant. So all core arcs point later→earlier — a topological order for any input. Pendant
edges are V027's case.

### V027 — CONFIRMED
**Claim.** Pendant edges are bridges and cannot close a cycle. *(MODEL / derivation)*
**Argument check.** Peeled edges are bridges (V008); any cycle would have to cross a bridge
twice, impossible. Adding the pendant edges to the acyclic core graph therefore keeps it acyclic,
for any input. Sound. (This does *not* make the sink formula exact — see V029/V126.)

### V029 — REFUTED (derivation; its measurement V030 passes)
**Claim.** Property 2 derivation: the final sinks are exactly
`{selected ∩ flow-terminal} ∪ {stall-promoted flow-terminal demanders}`. *(MODEL / derivation)*
**Argument check.** The spec argues only the ⊆ direction ("Nothing else can be a sink — every
other node is given an out-arc by the sweep", §3.2) and asserts equality. Both directions fail
in general; both counterexamples were run through a faithful generic implementation of §1.1
(`toys.py`, deterministic sweep, scipy LP):
- **T1 (Phase 0 active).** Triangle A(+5), B(−3), D(0) with leaf C(−2) on B. Actual sinks
  **{C}**; formula set **{B}**. The pendant importer C is a sink outside the set, and the
  selected sink B loses sinkhood to the Phase-4 pendant edge B→C.
- **T2 (2-core only).** 5-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 plus chord w–S1. Both u1 and
  u2 are selected flow-terminal demanders (two clusters, k = 2). Under the adopted key
  (DEF ascending) u2 (DEF 2) pops first, the conduit w becomes ready via its free edge to u2 and
  pops (DEF 0) before u1 (DEF 3, deliberately late). Free edge u1–w then orients u1→w. Actual
  sinks **{u2}**; formula set **{u1, u2}**. The heaviest demander in the game loses its sink to
  the sweep's own priority — demand still 100% served, placement not as claimed.
**Why the 1444 measurement passes anyway.** Phase 0 is a no-op on the vanilla map (no T1), and no
selected sink happens to have a free edge to an earlier-marked node under 1444's balances (no
T2). The identity is a property of this dataset, not of the algorithm.
**Spec text to change.** §1.1: "the final sinks are exactly `{selected ∩ flow-terminal} ∪
{stall-promoted flow-terminal demanders}`" and §3.2 claim 1 — either scope to "on maps where
Phase 0 is a no-op and no selected sink is free-edge-adjacent to an earlier-marked node", or
state it as the measured 1444 result plus the runtime assertion.
**Blast radius.** V125, V126 (same identity), C384 (consumption-at-line-end, OUTCOME), the §2.8
"sink placement" row's wording; V030/V108's measurements stand as measurements.

### V031 — PARTIAL
**Claim.** Property 3 derivation: the orientation contains a flow serving 100% of every good's
demand, because the LP imposes node balance. *(MODEL / derivation)*
**Argument check.** On a **connected** graph with globally balanced b (guaranteed: s and c are
world shares), the uncapacitated LP is feasible and its certificate is embedded in the
orientation — sound. On a disconnected graph the LP is feasible only if every component balances
separately, which shares-normalisation does not provide: demonstrated infeasible on a two-
component toy with ±0.2 cross-component imbalance (`toys.py` T4, HiGHS "model_status is
Infeasible"). v1 carried per-component renormalisation (C013–C018); v2 orphaned it with no
replacement (claims-v2's own orphan note: "component handling is unstated in v2") while
targeting "map-agnostic".
**Measured.** Vanilla is one component (fresh BFS), so V032's 100.0% stands on 1444.
**Spec text to change.** §1.1 property 3: name the premise ("on each connected component,
balances renormalised per component") and §2.2 item 5 should say what the solver does on
disconnected maps.
**Blast radius.** V110's assertion design (out of scope) still catches it at runtime; V124, V185
inherit the same premise.

### V033 — CONFIRMED
**Claim.** Ready-marking is a monotone closure, so the stall sequence, promotions and fallbacks
are provably independent of scheduling. *(MODEL / derivation)*
**Argument check.** Every gate condition (all flow out-neighbours marked; selected; has flow
out-arc; free edge to a marked node) is monotone in the marked set, and marking never unmarks —
so the saturated set before each stall is the unique least fixed point regardless of pop order,
and the promotion choice (min-β terminal of that set) is a function of the set. Induction over
stalls gives scheduler-invariance of the stall sequence, promotions, and fallbacks, for any
input. Empirical: promotions identical across scan permutations, 29/29 (fresh detrep). Note the
*marking order* (and hence free-edge orientation) is not covered by this argument — that is
V034's job, which the spec correctly separates.

### V034 — CONFIRMED
**Claim.** The priority key makes the remaining freedom (free-edge direction) a function of the
graph and the balances alone. *(MODEL / derivation)*
**Argument check.** (DEF, b, index) is a total order — index breaks all ties — so the heap pop
sequence is deterministic given the graph, balances, and node indexing. The index is part of the
input (the node file's declaration order), so the claim holds as stated; on 1444 it is stronger —
zero exact (DEF, b) ties measured, so the index never even decides (V035).

### V036 — CONFIRMED
**Claim.** Property 5: unit costs make the certificate flow a fewest-hop routing. *(MODEL /
derivation)*
**Argument check.** With unit arc costs the objective is Σ(flow × hops), so the optimum is the
minimum total flow-hop routing — "fewest-hop" in the aggregate (individual units may detour when
sink assignment demands it; no per-unit shortest-path claim is made). Sound. Note this is the
one §1.1 property with no paired measurement; under the §3.13 calibration it deliberately
degrades (V180).

### V040 — CONFIRMED
**Claim.** A node with b = 0 exactly is handled as an ordinary conduit. *(MODEL / derivation)*
**Argument check + code check.** b = 0 contributes nothing to the LP's right-hand side; the node
is not a Phase-1 demander candidate (β < 0 required); the sweep gates treat it like any node.
`drain.py` contains no zero special-case; the only reachable edge case (a β = 0 flow-terminal
promoted when no demander terminal exists) is the documented fallback, which fired 0 times in
29 goods (fresh). Measured: cape conduit for 29/29 (V129).

### V048 — CONFIRMED
**Claim.** The wealth pipeline applies the applicable floor per province — a territory province
contributes ~10% of its development's income, a colonial core ~50%. *(MODEL / derivation)*
**Argument check.** Autonomy multiplies province income by (1 − autonomy); floors of 90% and 50%
(V044, V045 — file-verified) give 10% and 50% contributions. Arithmetic sound.
**Caveat (systemic finding 1).** The reference solver that produced every measured number in this
spec does **not** implement these floors — `solver.py` computes wealth with no autonomy term.
The claim describes the specified pipeline, which no measurement has yet exercised.

### V049 — CONFIRMED
**Claim.** Gold excludes itself from demand entirely under `wealth = tax + production_income`.
*(MODEL / derivation)*
**Argument check.** Given V052 (gold `base_price = 0`), a gold province's production income is
`goods_produced × 0 = 0`; given V050/V051, mine income is its own category (`INCOMEGOLD`,
`GOLD_MINE_SIZE`), never booked as production income. So no gold ducat enters `wealth`,
diverted or not — sound, with the per-province *field* question honestly left open (V054).

### V053 — CONFIRMED
**Claim.** Excluding gold from the networks costs nothing. *(MODEL / derivation)*
**Argument check.** `base_price = 0` ⇒ `V_gold = 0` (no aggregate weight) and zero trade value;
c-side contribution is zero by V049. Removing a good with zero weight and zero value changes no
output. Sound given V052.

### V060 — PARTIAL
**Claim.** Each good's marking order is a per-node scalar whose descending comparison reproduces
that good's DAG. *(MODEL / derivation)*
**Argument check.** For core edges, sound: flow arcs and free edges both point later→earlier
(V026), so descending order-comparison reproduces them exactly. But pendant nodes never enter
the sweep and have **no marking order**; pendant edges are oriented by subtree sign (V007), which
order-comparison cannot express. On any map where Phase 0 acts, the claim fails as stated — and
`Φ_ord` (V059) is undefined on pendant edges. Unstated premise: Phase 0 is a no-op.
**Measured.** 29/29 goods reproduce exactly on 1444 (fresh), where the premise holds.
**Spec text to change.** §1.6: define order values (or the Φ_ord orientation) for un-peeled
pendants, or scope the sentence to the 2-core.

### V061 — CONFIRMED
**Claim.** The value-weighted sum of marking orders is a potential, so orienting edges by it is
acyclic for free. *(MODEL / derivation)*
**Argument check.** Orienting every edge by strict descending comparison of any per-node scalar
cannot create a directed cycle (a cycle needs a strict descent returning to its start). Exact
ties would leave edges unoriented — never cyclic; measured zero exact Φ_ord ties across the 159
edges on 1444 (fresh). Sound. (Coverage of pendant edges is V060's caveat, not an acyclicity
issue.)

### V063 — CONFIRMED
**Claim.** The v1 diagnostic identity does not survive the operator change: DRAIN performs no
linear solve, so no linearity argument exists. *(MODEL / derivation)*
**Argument check.** The Φ ≡ k·φ₀ identity was linearity of `L⁻¹` in the right-hand side plus
α = 1 collapsing the demand vectors; marking orders are outputs of a combinatorial sweep with no
additive structure in b. Sound; V064's replacement check is the design consequence (out of
scope).

### V076 — PARTIAL
**Claim.** The banding is the reverse of what v1 recorded: Improve Inland Routes is the one
banded mechanic, Propagate Religion has no band, every other listed threshold is single-valued —
nothing absorbs threshold chatter on its own. *(ENGINE / derivation)*
**Method.** Full read of `00_trading_policies.txt` (fresh) + the five defines.
**Evidence.** IIR: select 50 / maintain 40 — banded ✓. The other five thresholds are single
defines ✓ (`JUSTIFY_TRADE_CONFLICT_LIMIT 0.2`, `_ACTOR_LIMIT 0.1`,
`MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER 0.2`, `TRADE_COMPANY_STRONG_LIMIT 0.51`,
`TRADE_COMPANY_CONTROL_LIMIT 0.6`). PR's **default** branch is 50/50, no band ✓ — but its
country-flag ladder is **banded**: maintain thresholds lag select by two rungs (select 25 →
maintain 15; select 10 → maintain 5; the 5-flag has *no* maintain share at all).
**What is true.** For flagless countries the claim holds exactly; for ladder-flag holders PR
does absorb chatter. "Propagate Religion has no band" needs the default-branch scope everywhere
it appears.
**Spec text to change.** §1.10: "Propagate Religion | 50% to establish **and 50% to maintain** in
the default branch (a country-flag ladder runs 5–50; the terminal fallback is 35/35) — no band"
→ note the ladder's maintain values trail its select values.
**Blast radius.** V075 (same finding), V077 (DEFERRED).

### V080 — CONFIRMED
**Claim.** What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers
are evaluated against a reoriented graph. *(MODEL / derivation)*
**Argument check.** Given V078 (no name references — re-verified, 0 hits in 2,623 files) and V079
(structural accessors exist — all found in the exe), scripted content can only see nodes through
values and structure the mod changes; a mission written against vanilla flow can change sense
without breaking. Sound.

### V086 — PARTIAL
**Claim.** DRAIN's bit-reproducibility exposure: the min-cost-flow solve must pivot identically
given identical input, and the sweep is already integer/combinatorial. *(MODEL / derivation)*
**Argument check.** The LP half is right and is the narrow exposure v1's dense algebra lacked.
The sweep half is wrong as written: the priority key compares **floating-point** DEF and b (DEF
is a float accumulation whose structure comes from the LP support), so the sweep is deterministic
float arithmetic, not integer arithmetic — its cross-machine reproducibility rides on fixed
operation order and on the LP support being identical, i.e., exactly the LP question again.
**Spec text to change.** §2.1: "the sweep is already integer/combinatorial" → "the sweep is
deterministic given the LP's support and fixed accumulation order (its comparisons are of
input-derived floats, not solver residuals)".
**Blast radius.** V153, V183 (same distinction).

### V089 — CONFIRMED
**Claim.** `unserved` and `stranded` must be equal by conservation. *(MODEL / derivation)*
**Argument check.** s and c are world shares (each sums to 1), so Σb = 0 identically; any flow
assignment conserves mass, so demand left unserved equals supply left stranded in total. Sound.
**Measured.** Extended the Phase-4 evaluator to return both: equal to <1e-9 on 29/29 (fresh).

### V090 — PARTIAL
**Claim.** Cost per good is one uncapacitated MCF on 80 nodes / 318 arcs plus an O(V+E) sweep —
milliseconds each with network simplex, tens of milliseconds for all 29 goods per tick. *(MODEL /
derivation)*
**Method.** Timed the full 29-good reference solve (LP via scipy/HiGHS + deterministic sweep).
**Evidence.** 0.17 s total, **5.9 ms per good** including Python overhead — "milliseconds each"
holds already with a generic LP. "Tens of milliseconds for all 29" was **not** achieved by the
reference (170 ms) and rests on the untested network-simplex-in-native-code premise; plausible,
unverified. Structure (one MCF + O(V+E) sweep, 318 arcs) verified in code and file (V091).
**Spec text to change (if precision wanted).** §2.2: quote the measured reference numbers and
mark the all-29 figure as a projection.

### V114 — PARTIAL
**Claim.** Two families of orientation fail before this one, and both failures are theorems, not
taste. *(MODEL / derivation)*
**Argument check.** Family 1 (local comparison): monotonicity is a theorem (C370–C372 unchanged)
and the Malacca–Cape dip is a map fact — sound. Family 2 (global potential): the sink *rule* is
a theorem (algebraic identity, re-verified 2320/2320, V116), but the *failure* — sinks placed by
supply geometry, not demand — additionally requires the measured contrast gap (2.5×10⁷ vs ~471,
V117), which is a property of EU4's data, not of the operator. The spec's own provenance for
those lines is numerical test.
**Spec text to change.** §3.2: "both failures are theorems, not taste" → "one failure is a
theorem; the other is an exact rule whose failure is measured".

### V122 — CONFIRMED
**Claim.** No parameter fixes v1: α strong enough to matter destroys §1.4's regime split.
*(MODEL / derivation)*
**Argument check.** To let demand beat supply geometry, demand contrast must close a 4–5
order-of-magnitude gap (V117 ✓ fresh); contrast scales as (wealth ratio)^α, and the diagnosis
α-ladder (re-verified) shows sinks move only at α ≥ 4–6 for spices, i.e. k ≥ ~3–5; the same k
puts cloves (price 8) at α = 4^k — hundreds to thousands — and the clamp then flattens every
good to α_max, erasing the three-regime split. Sound, with premises V117 (fresh) and C442
(unchanged).

### V124 — CONFIRMED
**Claim.** Operators that impose node balance somewhere serve 100% of demand as a theorem;
operators that don't, strand it. *(MODEL / derivation)*
**Argument check.** Balance-imposing: the v1 solve (L φ = s − c) and the b-flow LP both encode
conservation, and their certificates serve all demand — with V031's connectivity premise, which
this claim inherits. Non-imposing: rank (83.29%) and basins (88.5%) measured stranding, fresh.
Sound as stated, one premise noted.

### V125 — REFUTED (see V029)
**Claim.** DRAIN takes sink placement out of field geometry entirely: sinks are the selected
demand centres plus the flow-terminal drains any acyclic drainage orientation is forced to have.
*(MODEL / derivation)*
**Evidence.** The equality behind this fails in general on both sides (T1: a pendant importer is
a forced sink that is neither; T2: a selected demand centre that is not a sink). On 1444 the
identity holds (29/29). The *contrast* with v1 (placement no longer set by field flatness)
survives; the "exactly these and nothing else" formulation does not.
**Blast radius.** C384; §3.2 claim 1.

### V126 — REFUTED (see V029, T1)
**Claim.** Nothing outside that set can be a sink: every other node is given an out-arc by the
sweep. *(MODEL / derivation)*
**Evidence.** Sound for the 2-core (every unselected, unpromoted core node is marked via a flow
out-arc or a free edge to an earlier-marked node — both yield out-arcs). False globally: a
pendant net-importing leaf (T1) is outside the set, is never touched by the sweep, and has no
out-arc — it is a sink. On 1444 Phase 0 is a no-op, so the measurement never sees it.
**Spec text to change.** §3.2: "Nothing else can be a sink (every other node is given an out-arc
by the sweep)" → scope to the 2-core, and state pendant net-importers as sinks by construction.

### V133 — CONFIRMED
**Claim.** Raising a node's aggregate wealth to a power rewards node size, so luxuries would
drain toward whichever node the map authors sliced coarsest. *(MODEL / derivation)*
**Argument check.** Relative to the per-province form (the model's own definition of true
demand), node-level α multiplies a k-province node's demand by `k^(α−1)` at fixed per-province
wealths — strictly increasing in province count for α > 1. So node-level aggregation overweights
many-province ("coarsely sliced") nodes by pure slicing. Sound under that reading — which is the
only reading that survives V134's correction.

### V134 — REFUTED
**Claim.** At α = 1.5 a 77-province node beats a 19-province node of equal total wealth by 2×
purely on slicing. *(MODEL / derivation)*
**Method.** Direct algebra on both demand forms.
**Evidence.** Node-level: c ∝ (ΣW)^α — with equal totals the two nodes **tie**; nothing beats
anything. Per-province with uniform provinces: the 19-node gets `(77/19)^0.5 = 2.01×` the
77-node. The correct statement of the distortion: switching from per-province to node-level α
shifts relative demand toward the 77-province node by `(77/19)^(α−1) = 2.01×` at α = 1.5,
independent of totals.
**Spec text to change.** §3.3: "at α = 1.5 a 77-province node beats a 19-province node of equal
total wealth by 2× purely on slicing" → "at α = 1.5, node-level α overweights a 77-province node
against a 19-province node by (77/19)^0.5 ≈ 2× relative to the per-province demand the model
defines, purely on slicing."
**Blast radius.** V133 (survives under the corrected reading), V136 (DEFERRED, inherits), §3.3.

### V137 — CONFIRMED
**Claim.** Substituting production income for trade value makes `V_g` depend on owners' idea
groups and autonomy. *(MODEL / derivation)*
**Argument check.** Production income = quantity × price × (efficiency, autonomy terms) by the
engine's own construction (C421–C423, unchanged); trade value = quantity × price only. Sound —
and V138's owner-factor experiment (fresh, 68/159) shows the sensitivity is large, not
theoretical.

### V144 — CONFIRMED
**Claim.** The sublinear regime is entered only when a price event pushes a good beneath the
anchor. *(MODEL / derivation)*
**Argument check.** Minimum tradeable base price is exactly 2.0 = P₀ (V140, fresh), so α ≥ 1 at
base prices for every good; prices move only through `change_price` effects (C046 unchanged;
all 101 shipped blocks enumerated this session), so α < 1 requires an event-driven price below
2.0. Sound. (How many goods can get there is V145/V146.)

### V151 — PARTIAL
**Claim.** A link whose flow-support membership alternates month to month carries near-nothing
either way. *(MODEL / derivation)*
**Argument check.** No argument is given in §3.6, and v1's continuity argument (near-flat
potential ⇒ near-zero flow, C450/C451) does not port: LP support membership is a discrete
selection, and at degenerate inputs (two exact-equal-hop corridors) the map b → chosen support is
discontinuous — a month-to-month ε-change *can* in principle swap corridors carrying O(1) flow.
Whether it ever does depends on the solver's tie selection — precisely the unstated premise, and
the same stability question V183 files as open for multiplayer.
**Measured (holds on 1444 with HiGHS).** 29 goods × 6 random 1e-9 demand nudges: **zero**
support-membership changes moving more than 1e-6 of flow; the ±1% wealth-noise flips (grain,
0.8 edges/159) all sit on near-zero-flow edges. A mirrored-ε K2,2 toy also failed to induce a
swap — HiGHS's selection was stable everywhere tested.
**Spec text to change.** §3.6: state it as measured behaviour plus the tie-selection premise,
not as a consequence.
**Blast radius.** C449 ("nothing needs to stop churn") leans on this; it survives empirically.

### V152 — CONFIRMED
**Claim.** v1's ε is deleted because the problem it patched no longer exists. *(MODEL /
derivation)*
**Argument check.** v1 oriented dead branches by comparing solved potentials that were equal in
exact arithmetic (documented, C453–C462, now orphaned); DRAIN orients free edges by the priority
sweep — a discrete rule with no comparison of solver residuals. The failure mode ε patched
(machine-dependent ties on mathematically-equal reals) cannot occur in the sweep. Sound; the
different, narrower cross-machine exposure is correctly re-filed (V086/V183).

### V153 — PARTIAL
**Claim.** DRAIN's priority key is computed from exact input data. *(MODEL / derivation)*
**Argument check.** The key's *values* (DEF sums, b) derive from input data — but DEF's
*structure* (which nodes are downstream) is the LP support, i.e. solver output. The intended
contrast with v1 (no comparisons of noise-dominated solved reals) is correct; the letter of
"exact input data" is not, and the residual dependence is exactly what V183's cross-machine
question tracks.
**Spec text to change.** §3.6: "the priority sweep's key (DEF, b, index) is computed from exact
input data" → "…from input data over the LP's support structure".

### V160 — CONFIRMED
**Claim.** `Φ_ord` is the value-weighted aggregate of the real per-good drainage orders rather
than an invented baseline. *(MODEL / derivation)*
**Argument check.** Immediate from the definition (V059) — the weights are the goods' trade
values and the orders are the per-good sweep outputs; nothing synthetic enters. Verified in code.

### V165 — CONFIRMED
**Claim.** The exposure surface is either the ~26 inland nodes (tooltip reading) or every node
adjacent to one (v1 reading) — smaller and differently shaped under the first. *(MODEL /
derivation)*
**Method/Evidence.** Inland flag count re-derived: 26 (`inland=yes`; derivation-from-members
gives 25, V092). Both readings correctly carried; the tooltip text supporting the first is
verbatim (V069). The disjunction is honest pending probe 11.

### V170 — CONFIRMED
**Claim.** v1's bistability argument is deleted: gold income never enters `wealth`, so neither
granting nor denial moves the demand vector — no direct feedback. *(MODEL / derivation)*
**Argument check.** Given V049–V052 (file-verified fresh), the treasury destination of gold has
no term in `wealth = tax + production_income`; the demand vector is unchanged by the gate in the
month it acts. Sound — and it correctly *deletes* a v1 argument the audit refuted (C549–C555).

### V172 — CONFIRMED
**Claim.** A slow second-order version survives — kept gold spent on development raises base_tax
and base_production years later — but is not a bifurcation and does not carry the decision.
*(MODEL / derivation)*
**Argument check.** Development purchases raise base values (engine premise C405-adjacent,
unchanged); the loop runs through player/AI spending decisions over years — no month-scale
self-reinforcement, hence no bistable gate. The design weight it carries is §3.12's problem
(out of scope); the mechanism statement is sound.

### V173 — CONFIRMED
**Claim.** Static string-table analysis leans against a colonization gate. *(ENGINE /
derivation)*
**Method/Evidence.** Fresh string table: the only direction-refusal strings are
`DIPLO_SELLPROV_NOT_UPSTREAM` and `TREASURE_FLEET_TOOLTIP_CANT_REACH(_DELAYED)`; none of the 308
COLONI* strings is a direction refusal (V098/V100). "Leans" is the right strength — absence of a
string is not absence of a gate, and the spec keeps the caller enumeration able to return
"no gate" as success.

### V185 — CONFIRMED
**Claim.** What the Laplacian guaranteed — 100% reachability via conservation, exact conduit
behaviour — DRAIN keeps by construction. *(MODEL / derivation)*
**Argument check/Evidence.** Reachability: LP feasibility (V031's argument, same connectivity
premise both operators share — v1's solve also needed per-component handling). Conduit: V040 +
measured cape 29/29 (V129). Both reproduce fresh; sound with the shared premise noted.

### V186 — CONFIRMED
**Claim.** Pure MCF orients only the ~79-edge support, leaving half the map undirected. *(MODEL /
derivation)*
**Method/Evidence.** Fresh: support sizes 78–79 of 159 edges (49–50% oriented); verify.py's FLOW
block confirms 79 on every good under the targeted-ε variant. "~79" and "half the map" both
hold. (Inherits V016's basic-solution premise.)

### V188 — CONFIRMED
**Claim.** DRAIN is exactly pure MCF plus the drainage completion that fixes both defects.
*(MODEL / derivation)*
**Method/Evidence.** Code structure: `phase2` *is* the MCF (same LP as flowop); phases 1/3/4 add
selection, the gated sweep (orients the remaining 80–81 edges), and un-peel. Fixes verified
fresh: 159/159 oriented (vs 79) and the order-aggregate acyclic (vs the net-flow aggregate's
cycles, V162/V187).

### V199 — CONFIRMED
**Claim.** "The aggregate map is not a DAG" is still an error, with v1's reason corrected: the
aggregate is a DAG because `Φ_ord` is a per-node scalar; v1's net-flow-gradient defense was
false. *(MODEL / derivation)*
**Method/Evidence.** The scalar-potential argument is V061 (sound, ties measured zero); the
falsity of v1's defense is V162's fresh measurement (value-weighted net flow contains directed
cycles). Both halves check.


---

# Part 4 — file values (lowest provenance risk, all re-read from the 1.37.5 install)

Every value below was read from the install this session, not from validation.md. Paths are
relative to `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV`.

## §1.2 / §1.3 — static modifiers and autonomy floors

### V038 — CONFIRMED
**Claim.** `00_static_modifiers.txt` carries `trade_goods_size_modifier` on `devastation`,
`occupied`, `under_siege`, and `prosperity`. *(ENGINE / file value, ⚑)*
**Method.** Parsed `common/static_modifiers/00_static_modifiers.txt` and listed every block
carrying the key.
**Evidence.** `occupied −0.5`, `under_siege −0.25`, `devastation −2`, `prosperity 0.25` — all four
present. (Also present on `intolerance`, `left_trade_company`, `production_leader`,
`trade_company_bonus`, `bonus_from_merchant_republics`(`_for_trade_league_member`),
`expanded_infrastructure` — the claim does not say "only these four", and §1.2's argument only
needs the four it names.)

### V042 — CONFIRMED
**Claim.** There is no flat 75% overseas autonomy floor in 1.37; autonomy floors are
regime-dependent. *(ENGINE / file value, ⚑, replaces C037)*
**Method.** Enumerated every `min_local_autonomy` in `00_static_modifiers.txt`; grepped the file
and `defines.lua` for `overseas` and for a 75 floor.
**Evidence.** Exactly four floors exist — `pasha_state 20`, `colonial_core 50`,
`territory_core 90`, `territory_non_core 90`. The only `overseas` hits in the file are
`average_overseas_subject_liberty_desire` and its reverse — unrelated to autonomy. No 75
anywhere. **The v1 fix landed correctly.**

### V044 — CONFIRMED
**Claim.** A province in a territory is floored at 90% local autonomy (`territory_core` /
`territory_non_core`). *(ENGINE / file value, ⚑)*
**Evidence.** `territory_core: min_local_autonomy = 90`, `territory_non_core:
min_local_autonomy = 90`. Both named blocks exist with the stated value.

### V045 — CONFIRMED
**Claim.** A colonial core is floored at 50% local autonomy. *(ENGINE / file value, ⚑)*
**Evidence.** `colonial_core: min_local_autonomy = 50`, corroborated by
`defines.lua: COLONY_MIN_AUTONOMY = 50` ("Colonial cores always have at least this much
autonomy").

### V046 — CONFIRMED
**Claim.** A pasha state is floored at 20% local autonomy. *(ENGINE / file value, ⚑)*
**Evidence.** `pasha_state: min_local_autonomy = 20`.

### V047 — CONFIRMED
**Claim.** A stated core is floored at 0 local autonomy. *(ENGINE / file value, ⚑)*
**Method/Evidence.** Evidenced by **absence**: the four `min_local_autonomy` blocks above are the
only ones in the file, and none applies to a stated core — so a stated core carries no floor,
i.e. 0. Corroborated positively by `defines.lua: CAPITAL_MAX_AUTONOMY = 0`. Worth noting the
provenance is an exhaustive-absence argument over one file rather than a positive value read;
it is sound here because the modifier system has no other place to put a floor.

## §1.5 — gold and coal

### V050 — CONFIRMED
**Claim.** Gold-mine income is its own income category in the engine — `INCOMEGOLD`, with
`gold_income` a distinct scriptable field. *(ENGINE / file value, ⚑)*
**Method.** Localisation sweep for `INCOMEGOLD`; `common/` sweep for `gold_income`.
**Evidence.** `localisation/core_l_english.yml: INCOMEGOLD:0 "Gold"` — an income-category label
alongside the other `INCOME*` keys. `gold_income` appears as a scriptable field in
`common/achievements.txt` (`gold_income = 10`) and as `gold_income_percentage` in
`common/estate_privileges/03_burgher_privileges.txt` and
`common/ruler_personalities/00_core.txt`.

### V051 — CONFIRMED
**Claim.** Gold income is computed from mine value with its own constants (`GOLD_MINE_SIZE`) and
is not booked as production income. *(ENGINE / file value, ⚑)*
**Evidence.** `defines.lua: GOLD_MINE_SIZE = 40` ("Base income from gold mines") and
`GOLD_MINE_SIZE_PRIMITIVES = 4` — a dedicated gold-income formula that does not reference price
or `goods_produced`. Combined with V050's separate income category and V052's `base_price = 0`,
"not booked as production income" holds **at the country level**, which is what §1.5's argument
needs.
**Note.** The per-province half is deliberately left open by the spec itself (V054, probe 12) and
this validation does not close it. The two claims are consistent, not contradictory: V051 is
about which country-level category the ducats land in; V054 is about what the per-province
display field shows.

### V052 — CONFIRMED
**Claim.** Gold is inert in vanilla trade value: `base_price = 0`, `goldtype = yes`. *(ENGINE /
file value, ⚑)*
**Method.** Parsed all 32 entries of `common/prices/00_prices.txt`.
**Evidence.** `gold: base_price = 0.0, goldtype = yes`. It is the only `goldtype` good, and one
of only two entries at price 0 (the other is `unknown`, which carries no `goldtype`).

### V055 — CONFIRMED
**Claim.** Coal produces nowhere at the 1444 start, and its default trigger fires on
Enlightenment — the Manufactories branches require special flags. *(ENGINE / file value, ⚑,
replaces C057)*
**Method.** Scanned all 3,923 `history/provinces` files for `trade_goods = coal`; parsed the
`coal` block of `common/tradegoods/00_tradegoods.txt`.
**Evidence.** Zero provinces carry `trade_goods = coal` at any date ≤ 1444.11.11 (and none at
all in history). The trigger's branch structure:

| branch | condition to enter | institution requirement |
|---|---|---|
| `if` (default) | no `GER_specific_coal` province flag **and** owner lacks `earlier_coal_available` | **enlightenment** progress 100 + owner has enlightenment |
| `else_if` | province has `GER_specific_coal` | manufactories + `adm_tech = 21` |
| `else` | owner has `earlier_coal_available` | manufactories + `adm_tech = 23` |

The ordinary case — no province flag, no country flag — is the Enlightenment branch ✓, and both
Manufactories branches are reachable only via a flag ✓. **The v1 fix landed correctly** (v1's
C057 named Manufactories).

### V056 — CONFIRMED
**Claim.** The coal trigger's per-province conditions: `development_discounting_tribal = 20` or
owner innovativeness 20, that province's own institution progress at 100, and the owner having
the institution. *(ENGINE / file value, ⚑)*
**Evidence.** Verbatim from the parsed block: outer
`OR = { development_discounting_tribal = 20  owner = { innovativeness = 20 } }`, then per branch
`provincial_institution_progress = { which = … value = 100 }` and
`owner = { has_institution = … }`. All three conditions present and per-province as stated.

### V057 — CONFIRMED
**Claim.** There are 58 latent-coal provinces. *(ENGINE / file value, ⚑)*
**Method.** Scanned every `history/provinces` file for a `latent_trade_goods` block containing
`coal`.
**Evidence.** 58 files carry `latent_trade_goods`, and **all 58** name coal. Exact.
(Of these, 45 are owned at 1444.11.11 — the figure V230's counterexample uses.)

## §1.7 / §1.12 / §3.11 — UI and caravans

### V066 — CONFIRMED
**Claim.** The vanilla node window already renders both an incoming and an outgoing link list as
clickable entries — `incoming_nodes_listbox` / `outgoing_nodes_listbox` in `tradeinterface.gui`,
both populated by the `TradeNodeLink` widget. *(ENGINE / file value, ⚑)*
**Method.** Read `interface/tradeinterface.gui`.
**Evidence.** Two `OverlappingElementsBoxType` blocks named `incoming_nodes_listbox` (line 90)
and `outgoing_nodes_listbox` (line 110), repeated for the second window layout at lines 519/528.
A single `windowType` named `TradeNodeLink` (line 18) is the file's only link element and
contains a `guiButtonType` named `NextNodeButton` (line 30) — hence clickable.
**Note.** That `TradeNodeLink` is the element type instantiated into *both* listboxes is a
structural reading (it is the only candidate in the file); the binding itself is engine-side and
not written in the `.gui`. The load-bearing half — both lists exist and their entries are
buttons — is directly file-evidenced. **The v1 fix landed correctly** (C532 refuted).

### V068 — CONFIRMED
**Claim.** The engine's caravan grant conditions are `merchant_present_inland` and
`merchant_steering_to_inland`, with nothing checking whether value moves. *(ENGINE / file value,
⚑, replaces C537)*
**Evidence.** `localisation/text_l_english.yml`:
`MERCHANT_PRESENT_INLAND:0 "Merchant present inland"` and
`MERCHANT_STEERING_TO_INLAND:0 "Merchant steering towards inland"` — the two grant conditions,
named exactly. Neither identifier nor any adjacent string references value, flow, or goods
carried; `MERCHANT_INLAND_DESC` describes the same disjunction ("collecting in an inland trade
node, **or** steering towards an inland trade node"). The negative half is an
argument-from-absence over the caravan string family, which is the strongest form available
without a debugger.

### V069 — CONFIRMED
**Claim.** The engine's tooltip reads as granting the caravan bonus in the inland node, not the
adjacent one. *(ENGINE / file value, ⚑, replaces C538)*
**Evidence.** `localisation/tradenodes_l_english.yml: TRADEMAP_INLAND_DESC:0 "Having a merchant
present that collects in an inland trade node, or steers towards an inland trade node, will give
you extra trade power **in that node** based on your trade efficiency."` The referent of "that
node" is the inland node in both arms of the disjunction. The claim's hedge — "reads as" — is
exactly right: the English is genuinely ambiguous, and the spec correctly routes the decision to
probe 11 rather than asserting it.

### V163 — CONFIRMED
**Claim.** The engine's own hint states steering is outgoing-only: "You can never steer trade
upstream or past your Main Trade City". *(ENGINE / file value, ⚑)*
**Evidence.** `localisation/hints_l_english.yml: HINT_TRADESTEERING_TEXT` — the sentence appears
verbatim as the hint's closing line.

### V164 — CONFIRMED
**Claim.** The *display* is not outgoing-only: the node window already lists incoming links as
clickable entries. *(ENGINE / file value, ⚑, replaces C532)*
**Evidence.** Same as V066 — `incoming_nodes_listbox` exists and its entries are `NextNodeButton`
buttons. The v1 error (C532: "the vanilla node map shows only the paths leaving a node") is
corrected.

### V167 — CONFIRMED
**Claim.** Caravan power is total country development ÷ 3 **plus policy and idea modifiers**,
clamped to [2, 50]. *(ENGINE / file value, ⚑, replaces C542)*
**Evidence.** `defines.lua`: `CARAVAN_FACTOR = 3.0` ("Development is divided by this factor"),
`CARAVAN_POWER_MAX = 50`, `CARAVAN_POWER_MIN = 2`. The additive term is named by the engine's own
tooltip, `powers_and_ideas_l_english.yml: CARAVAN_POWER_DESC2` — "Inland caravans provide a total
of $VALUE$ trade power, **base of it coming from a third of your development($BASE$) and
$MODIFIER$ from policies and ideas**." Every element of the claim (÷3, additive modifiers, both
clamp ends) is file-evidenced. **The v1 fix landed correctly** (C542 omitted both the additive
term and the floor).

### V168 — CONFIRMED
**Claim.** Nineteen countries are at the caravan cap from raw 1444 development alone; Burgundy,
Korea, the Timurids and Portugal start 2–10% short and reach it with any caravan modifier.
*(ENGINE / file value, ⚑, replaces C543)*
**Method.** Summed `base_tax + base_production + base_manpower` per owner over the reconstructed
1444.11.11 province set; the cap is reached at development ≥ 150 (since 150/3 = 50).
**Evidence.** **19** countries at or above 150 — MNG, ENG, TUR, CAS, LIT, VIJ, FRA, MAM, ARA,
JNP, BAH, MOS, SHY, POL, BNG, HUN, VEN, HAB, QAR. The four named near-misses:

| tag | dev | dev/3 | short of cap by |
|---|---|---|---|
| BUR | 147.0 | 49.00 | 2.0% |
| KOR | 145.0 | 48.33 | 3.3% |
| TIM | 142.0 | 47.33 | 5.3% |
| POR | 136.0 | 45.33 | 9.3% |

All four fall in the stated 2–10% band, and they are exactly the four countries in it.

### V171 — CONFIRMED
**Claim.** The engine's own denial branch confirms what denial does: "They will keep their gold
income instead." *(ENGINE / file value, ⚑, replaces C550)*
**Evidence.** `localisation/eldorado_l_english.yml: TREASURE_FLEET_TOOLTIP_CANT_REACH_DELAYED:0
"§RThey will keep their gold income instead.§!\n\nIf we would move our Trade capital to a node
downstream to theirs, we would receive Treasure Fleets."` Verbatim.

### V081 — CONFIRMED
**Claim.** The node window carries several node-level value fields (incoming / local / total /
outgoing), but none takes a commodity argument — zero per-good fields, where thirty would be
needed. *(ENGINE / file value, ⚑, replaces C158)*
**Evidence.** `tradeinterface.gui` defines `incoming_value`, `local_value`, `total_value`,
`outgoing_value` (plus their `_label` partners), `piracy_value`, `light_ships_in_node_value` and
`goods_produced_value` — all node-scalar text boxes. No field name is parameterised by a good,
and there is no repeated-per-good element anywhere in the file. **The v1 fix landed correctly**
(C158 said the UI had no value fields; it has several, just none per-good).

## §1.9 / §1.10 — propagation, thresholds, scripted content

### V073 — CONFIRMED
**Claim.** The engine's propagation tooltip carries a receiving-side qualifier §1.9 does not:
power transfers upstream "to trade nodes where it already has power". *(ENGINE / file value, ⚑)*
**Evidence.** `localisation/tradenodes_l_english.yml: TRADE_POWER_UPSTREAM_DESC:0 "A nation can
Transfer Trade Power back upstream to trade nodes **where it already has power**."` Verbatim, and
the qualifier is indeed absent from §1.9 (V211). Both strings also present in the exe table
(`TRADE_POWER_UPSTREAM` at 0x01ce8058, `_DESC` at 0x01d4f1e0).

### V074 — CONFIRMED
**Claim.** Improve Inland Routes requires 50% trade power to establish and 40% to maintain, plus a
merchant present in the node, and is waived entirely by the `free_improve_inland_routes`
government attribute. *(ENGINE / file value, ⚑, replaces C128)*
**Method.** Read `common/trading_policies/00_trading_policies.txt` in full.
**Evidence.** `improve_inland_routes.can_select`: `FROM = { has_trader = ROOT }` plus
`if = { limit = { NOT = { has_government_attribute = free_improve_inland_routes } } FROM = {
trade_share = { country = ROOT share = 50 } } }`; `can_maintain` is identical with `share = 40`.
All four elements — 50, 40, merchant, waiver — present exactly. The `_upgraded` variant carries
the same numbers. **The v1 fix landed correctly** (C128 said 33%).

### V075 — PARTIAL
**Claim.** Propagate Religion requires 50% to establish and 50% to maintain in the default branch
— a country-flag ladder runs 5–50, terminal fallback 35/35 — with no band. *(ENGINE / file value,
⚑, replaces C129, C130)*
**Method.** Read every branch of `propagate_religion`'s `can_select` and `can_maintain`.
**Evidence.** Default branch **50 select / 50 maintain** ✓ (no band). Terminal `else` **35/35** ✓
(no band). The flag ladder does run 5–50 ✓. **But every rung of that ladder is itself banded** —
`can_maintain`'s share trails `can_select`'s by one or two rungs:

| country flag | select | maintain |
|---|---|---|
| `5_trade_power_…` | 5 | *(no share requirement at all)* |
| `10_…` | 10 | 5 |
| `15_…` | 15 | 5 |
| `20_…` | 20 | 10 |
| `25_…` | 25 | 15 |
| `30_…` | 30 | 20 |
| `35_…` | 35 | 25 |
| `40_…` | 40 | 30 |
| `45_…` | 45 | 35 |
| default | 50 | 50 |
| terminal `else` | 35 | 35 |

**What is true.** "With no band" holds for the two branches that set the 50/50 and 35/35 figures —
which is the case a flagless country is in — and fails for the nine ladder rungs the same
sentence introduces. A country holding any `N_trade_power_for_propogate_religion` flag *does* get
band hysteresis, of 5–10 points.
**Spec text to change.** §1.10's table row: "Propagate Religion | 50% to establish **and 50% to
maintain** in the default branch (a country-flag ladder runs 5–50; the terminal fallback is
35/35) — no band" → note that the ladder rungs are banded (maintain trails select by 5–10) even
though the default and terminal branches are not.
**Blast radius.** V076 (graded PARTIAL for the same reason) and V077 (DEFERRED) — the flicker-risk
set is "flagless countries", not "all countries".

### V078 — CONFIRMED
**Claim.** No mission, decision, event, or trade company in 1.37.5 names a trade node — zero
non-comment references across `common/`, `missions/`, `decisions/`, `events/`; trade companies
are bare province lists. *(ENGINE / file value, ⚑, replaces C139, C141)*
**Method.** Whole-word regex for all 80 node names over **2,623** `.txt` files in the four trees,
comments stripped line-by-line, `common/tradenodes/` excluded (`namegrep.py`). Whole-word
matching means area/region tokens like `saxony_area` correctly do **not** count.
**Evidence.** **0 hits.** `common/trade_companies/00_trade_companies.txt` carries only the keys
`name`, `names`, `provinces`, `color`, `primary_culture`, `tag`, `trigger` — province lists, no
node reference. (Its 68 entries are *named* after nodes, e.g. `trade_company_genua`, but those
are the block identifiers, not node references — which is exactly why whole-word matching on the
value side returns nothing.) **The v1 fix landed correctly**, and the conclusion is indeed
stronger than v1's.

### V079 — CONFIRMED
**Claim.** Scripted content reaches nodes only structurally: `home_trade_node`,
`any/random/every_active_trade_node`, `*_trade_node_member_province`, and
`highest_value_trade_node`. *(ENGINE / file value, ⚑)*
**Method.** Exe string-table sweep for the named accessors.
**Evidence.** All present in the binary: `home_trade_node` (0x021aab7c), `any_active_trade_node`
/ `all_active_trade_node` / `random_active_trade_node` / `every_active_trade_node`,
`any_/all_/random_/every_trade_node_member_province`, `highest_value_trade_node` (0x0213c03c),
plus `same_home_trade_node_as` and `home_trade_node_effect_scope`. Combined with V078's zero
name references, structural access is the only channel that exists.

### V082 — CONFIRMED
**Claim.** Achievements are off with any mod — `ACHIEVEMENTS_DISABLED_MODIFIED_GAME`. *(ENGINE /
file value, ⚑, replaces C176)*
**Evidence.** `localisation/core_l_english.yml: ACHIEVEMENTS_DISABLED_MODIFIED_GAME:0 "§Y- EU4 is
running a mod or is altered in other ways.§!"`, one of the reasons listed under
`ACHIEVEMENTS_DISABLED_BECAUSE`. Also in the exe table (0x01c37428 region).

### V083 — CONFIRMED
**Claim.** The engine itself will load an ironman save in a modded game — "Loading ironman in
modded game" is a shipped code path. *(ENGINE / file value, ⚑)*
**Evidence.** Exe string at **0x01c8bf10: `Loading ironman in modded game`** — a log/trace string
inside the load path, adjacent to `Game state not ironman, shouldn't happen.` (0x01c8bce0) and
`SAVEITEM_IRONMAN`. **The v1 fix landed correctly** (C176 conflated achievements-off with
ironman-unavailable).

### V098 — CONFIRMED
**Claim.** Static string-table analysis yields three named direction call sites:
`DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH`, `TRADE_POWER_UPSTREAM`.
*(ENGINE / file value, ⚑)*
**Method.** Re-extracted the full string table from `eu4.exe` this session (137,820 strings) and
searched for `upstream` / `downstream` case-insensitively.
**Evidence.** The complete upstream/downstream inventory is four keys:
`DIPLO_SELLPROV_NOT_UPSTREAM` (0x01c85f18), `MERCHANT_DOWNSTREAM_BONUS` (0x01ce7f00),
`TRADE_POWER_UPSTREAM` (0x01ce8058), `TRADE_POWER_UPSTREAM_DESC` (0x01d4f1e0); plus
`TREASURE_FLEET_TOOLTIP_CANT_REACH` (0x01d42528) and its `_DELAYED` partner, which name the
relation without using the word. The three the claim names are exactly the three *direction-gate*
sites; `MERCHANT_DOWNSTREAM_BONUS` is a bonus label, not a gate.

### V099 — CONFIRMED
**Claim.** Both nation-pair direction gates compare trade capitals. *(ENGINE / file value, ⚑)*
**Evidence.** `TREASURE_FLEET_TOOLTIP_CANT_REACH`: "…because our Trade capital $OURNODE$ is not
downstream from their Trade capital $THEIRNODE$." `DIPLO_SELLPROV_NOT_UPSTREAM`: "$WHO$ doesn't
have their **Main Trading Port** downstream of $PROV$". Both compare a trade capital / main
trading port, and neither compares provinces or countries generally.

### V100 — CONFIRMED
**Claim.** No colonisation refusal string exists in the binary. *(ENGINE / file value, ⚑)*
**Method.** Intersected the 308 `COLONI*` strings in the exe table with the direction vocabulary.
**Evidence.** The only `COLONI*` strings mentioning trade or nodes are
`unknown tradegoods in colonial regions:` and `MAPMODE_COLONIALANDTRADECOMPANYREGIONS` — neither
a refusal. The full upstream/downstream inventory (V098) contains no colonisation key. An
argument from absence, correctly hedged as "leans against" where it is used (V173).

### V155 — CONFIRMED
**Claim.** The shipped policy file gates Propagate Religion on the trade share AND the node being
in a trade company region AND a merchant present AND a religion-group/flag disjunction AND
`dominant_religion`, with `unique = yes` per node. *(ENGINE / file value, ⚑, replaces C486)*
**Evidence.** From `propagate_religion.can_select`: `unique = yes # Only one country can select
this in a certain node.`; the religion disjunction (`religion_group = muslim` /
`zoroastrian_group` / dharmic-with-mission / two `custom_trigger_tooltip` flag arms);
`dominant_religion = ROOT` inside its own `if`; and every share branch carrying
`FROM = { has_trader = ROOT  is_node_in_trade_company_region = yes  trade_share = {…} }`. All five
conjuncts plus `unique` present exactly as claimed. **The v1 fix landed correctly** (C486's "and
nothing else" was the wrong half).

### V157 — CONFIRMED
**Claim.** What the trade-policy family shares is the absence of any direction test: no trading
policy anywhere in `00_trading_policies.txt` tests upstream/downstream. *(ENGINE / file value, ⚑,
replaces C487, C488)*
**Method.** Full read of the file (all nine policy blocks).
**Evidence.** No occurrence of `upstream`, `downstream`, or any node-relation trigger in any
`potential`, `can_select`, or `can_maintain` block. The only node-scoped triggers used are
`has_trader`, `is_node_in_trade_company_region`, and `trade_share`.

### V158 — CONFIRMED
**Claim.** Three of the five trading policies have no trade-share threshold at all
(merchant-present only). *(ENGINE / file value, ⚑)*
**Evidence.** The file defines nine blocks, which are five policies plus four `_upgraded`
variants. Of the five: `maximize_profit`, `hostile_trading`, `establish_communities` gate on
`FROM = { has_trader = ROOT }` and nothing numeric — **three** ✓; `improve_inland_routes` (50/40)
and `propagate_religion` (the ladder) are the two with thresholds.

## §2.1–§2.4 — map, graph, and file structure

### V009 — CONFIRMED
**Claim.** On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. *(ENGINE /
file value)*
**Method.** Built the undirected node graph from `common/tradenodes/00_tradenodes.txt` and ran
Tarjan bridge-finding (`graphchk.py`).
**Evidence.** Minimum degree **2** (attained at `african_great_lakes`, `zambezi`, `patagonia`,
`james_bay`, `australia`); degree-1 nodes **0**; bridges **0** — the graph is 2-edge-connected.
Phase 0 therefore removes nothing and Phase 4 orients nothing.

### V091 — CONFIRMED
**Claim.** The vanilla node graph presents 318 arcs to the flow solve. *(ENGINE / file value)*
**Evidence.** 159 declared directed links, 159 distinct undirected pairs (zero duplicated or
bidirectional declarations), and the LP builds two arcs per undirected edge → **318** ✓,
matching `flowop.ARCS`.

### V092 — CONFIRMED
**Claim.** The `inland` flag and the coastal-member derivation disagree at exactly one node:
`siberia` carries `inland=yes` but has two Arctic-coast members (1781, 1782), so derivation gives
25 inland nodes against the flag's 26. *(ENGINE / file value, ⚑, replaces C210)*
**Method.** Re-derived coastal provinces from `map/provinces.bmp` + `map/definition.csv` +
`map/default.map` sea starts (4-neighbour adjacency, `coastal.py`), then compared per node.
**Evidence.** 1,161 coastal land provinces, 0 unmapped pixels, 0 `force_coastal` entries.
`inland=yes` count **26**; derived-inland count **25**; **mismatches: 1** — `siberia`, whose
coastal members are exactly **[1781, 1782]**. Every other flagged node has 0 coastal members.

### V095 — CONFIRMED
**Claim.** The shipped vanilla `00_tradenodes.txt` is itself topologically sorted sources-first —
0 of 159 links violate declaration order. *(ENGINE / file value, ⚑)*
**Method.** For each declared `outgoing` link, compared the declaration indices of the two nodes.
**Evidence.** **0 of 159** links point backwards in declaration order.

### V130 — CONFIRMED
**Claim.** The corridor runs through the Cape because it is the short route to Atlantic Europe —
3 hops to the Channel against 7 via Alexandria. *(ENGINE / file value)*
**Method.** Unweighted BFS on the node adjacency (`graphchk.py`), independently re-checked by
`verify.py`.
**Evidence.** `malacca → english_channel` via `cape_of_good_hope` = **3** hops; via `alexandria`
= **7** ✓. (Cape → Channel alone is 2: `cape → ivory_coast → english_channel`; Alexandria →
Channel is 3.) The figures are geometry, not an artifact of the operator.

### V132 — CONFIRMED
**Claim.** Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4×
spread with no structural rule behind it. *(ENGINE / file value, ⚑, replaces C407)*
**Method.** Counted `members` per node excluding `sea_starts` and `lakes` from `map/default.map`.
**Evidence.** Minimum **19** at `cape_of_good_hope` ✓ (20 total members, 1 sea); maximum **77** at
`girin` ✓ (`mexico` 76, `california` 74). 77/19 = 4.05 ✓. **The v1 fix landed correctly** (C407's
"forty versus four" overstated the spread by an order of magnitude).

### V135 — CONFIRMED
**Claim.** Nippon has 68 land provinces; the Paris node (`champagne`) has 33. *(ENGINE / file
value, ⚑)*
**Evidence.** `nippon` 68 land of 69 members ✓; `champagne` 33 land of 33 ✓. Note the land-vs-
member distinction matters for Nippon (69 raw members) and the spec's figure is the land count,
which is the right one for §3.3's argument.

### V148 — CONFIRMED
**Claim.** The node-file *format* represents cycles perfectly well: it is a list of named directed
links with no acyclicity constraint. *(ENGINE / file value, ⚑, replaces C447)*
**Method.** Structural read of `00_tradenodes.txt`: node-level keys and the shape of `outgoing`.
**Evidence.** The only node-level keys in the entire file are `location`, `members`, `outgoing`,
`color`, `inland`, `end`, `ai_will_propagate_through_trade`. Each `outgoing` block carries a
`name` naming another node — a free-form directed edge list with no ordering key, no rank, and
nothing that could express or enforce acyclicity. A two-node cycle is expressible by writing two
`outgoing` blocks. **The v1 fix landed correctly**; what remains open is the engine's reaction
(V149), which the spec correctly separates.

## §3.5 — prices

### V140 — CONFIRMED
**Claim.** At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base
price is exactly 2.0. *(ENGINE / file value, ⚑, replaces C432, C433, C434)*
**Method.** Parsed all 32 entries of `common/prices/00_prices.txt`.
**Evidence.** Sorted ascending: `gold 0.0` (`goldtype = yes`, excluded by configuration and inert
per V052), `unknown 0.0` (not a tradeable good), then **fur / naval_supplies / slaves / tea /
tropical_wood / livestock at exactly 2.0**, rising to `cloves 8.0` and `coal 10.0`. The minimum
over tradeable goods is exactly 2.0 ✓, so α ≥ 1 for every good at base prices.

### V141 — CONFIRMED
**Claim.** Fur, naval supplies, slaves, tea, tropical wood, and livestock have base price exactly
2.0, sitting on the anchor at α = 1 exactly. *(ENGINE / file value, ⚑)*
**Evidence.** Exactly those six goods carry `base_price = 2.0`, and no others. At
`α = (2.0/2.0)^1 = 1` they are on the anchor exactly ✓.

### V142 — CONFIRMED
**Claim.** Grain's base price is 2.5, not the 1.25 v1 recorded. *(ENGINE / file value, ⚑)*
**Evidence.** `grain: base_price = 2.5` ✓ (sharing 2.5 with wine, wool, fish, incense). **The v1
fix landed correctly**; the misreading mechanism is V143 (2.5/2.0 = 1.25).

### V145 — REFUTED
**Claim.** 13 of 30 goods can be pushed below 2.0 by a single vanilla `change_price` event; grain
and wine reach 0.625. *(ENGINE / file value, ⚑)*
**Method.** Parsed every `change_price` block in `events/`, `decisions/`, `missions/` and
`common/` — **101 blocks** — recorded the most negative `value` per good, and applied it to that
good's base price (`leftovers.py`). `history/` contributes one file (HAB) with two `value = 0.25`
entries, both positive, so it cannot lower any floor.
**Evidence.** **12** goods reach a price strictly below 2.0:

| good | base | worst event | single-event floor |
|---|---|---|---|
| grain | 2.5 | −0.75 | **0.625** |
| wine | 2.5 | −0.75 | **0.625** |
| glass | 3.0 | −0.65 | 1.05 |
| slaves | 2.0 | −0.40 | 1.2 |
| chinaware | 3.0 | −0.50 | 1.5 |
| copper | 3.0 | −0.50 | 1.5 |
| livestock | 2.0 | −0.25 | 1.5 |
| paper | 3.5 | −0.50 | 1.75 |
| coffee | 3.0 | −0.40 | 1.8 |
| spices | 3.0 | −0.40 | 1.8 |
| fish | 2.5 | −0.25 | 1.875 |
| incense | 2.5 | −0.25 | 1.875 |

Grain and wine at 0.625 ✓ — that half is exact. But the count is 12, not 13.
**What is actually true.** Three further goods land **exactly on** 2.0 rather than below it —
`gems` (4.0, −0.50), `silk` (4.0, −0.50) and `wool` (2.5, −0.20) — giving α exactly 1, the anchor,
not the sublinear regime. This is the likely source of the off-by-one: a `< 2.0` versus `≤ 2.0`
boundary on a set where three goods sit on the boundary exactly. The next-largest floors are
`cloth` and `iron` at 2.55, so 12 is not close to 13 by any other route.
**Spec text to change.** §3.5: "**13 of 30 goods** can be pushed below 2.0 by a single vanilla
`change_price` event (grain and wine reach 0.625)" → "**12 of 30**… with three more (gems, silk,
wool) reaching exactly 2.0". §3.13 repeats the figure: "reachable through vanilla price events
for 13 of 30 goods and unreachable for 11".
**Blast radius.** V176 embeds the same 13; V147's "bounded question" framing is unaffected in
kind. V146's 11 is exact, and 12 + 11 = 23 of 30 accounted for — the remaining 7 have negative
events too small to cross the anchor.

### V146 — CONFIRMED
**Claim.** 11 goods have no negative price event at all and can never go sublinear in vanilla.
*(ENGINE / file value, ⚑)*
**Method.** Parsed every `change_price` block in `events/`, `decisions/`, `missions/` and
`common/` (101 blocks) and grouped by good and sign; separately confirmed `history/` contributes
only positive entries (one file, HAB, both `value = 0.25`).
**Evidence.** Exactly **11** goods have no `change_price` with a negative value: cloves, cocoa,
cotton, fur, ivory, naval_supplies, salt, sugar, tea, tobacco, tropical_wood ✓. With no negative
event they cannot be pushed below their base price, all of which are ≥ 2.0 (V140), so they can
never go sublinear ✓.

---

# Part 5 — MODEL stipulations (§1.1's phase definitions)

These twelve claims are the algorithm's definition. A stipulation cannot be true or false against
the world; what it can be is **complete, unambiguous, and faithfully implemented**. Each was
checked on all three counts against `drain.py`, which is the reference the spec's measurements
come from, and each is CONFIRMED on all three.

### V005 — CONFIRMED
**Claim.** For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`. *(MODEL / stipulated)*
**Evidence.** `solver.build_sc` returns S and C as world shares; every operator call site computes
`S0m[gi] - C0m[gi]`. Both terms are normalised shares, so `Σ_n b_g(n) = 0` identically — the
premise V089's conservation argument needs, and the premise V031's feasibility argument needs
(per component).

### V006 — CONFIRMED
**Claim.** Orientation per good is by DRAIN — peel, select, route, sweep. *(MODEL / stipulated,
replaces C007, C008)*
**Evidence.** `run_drain` executes exactly `phase0` → `phase1` → `phase2` → `sweep_priority` →
`compile_dirs`, matching the four named stages plus the un-peel. The four-word summary is
faithful and the phases below fill it in with no gaps.

### V007 — CONFIRMED
**Claim.** Phase 0 repeatedly removes degree-1 nodes down to the 2-core, orienting each pendant
edge by the sign of its absorbed subtree balance (net exporter → toward core; net importer → fed
from core; zero → toward core) and folding the residual into the parent. *(MODEL / stipulated)*
**Evidence.** `phase0` loops while any alive node has degree 1, logs `(v, u, beta[v])` and folds
`beta[u] += beta[v]`; `compile_dirs` replays the log in reverse with
`(v, u) if bv >= 0 else (u, v)` — exporter and zero toward the core, importer fed from it,
exactly as stipulated including the tie convention. Complete and unambiguous.
**Note.** The zero case is a *convention*, not a consequence of conservation (V008's argument
determines the flow, which is zero, but not the arrow). The spec is right to stipulate it here
rather than derive it.

### V011 — CONFIRMED
**Claim.** Phase 1 takes the connected clusters of net demanders in the core, computes the
Herfindahl index of their demand masses, sets `k = clamp(round(1/HHI), 1, n_clusters)`, and
selects the heaviest demander of each of the top-k clusters. *(MODEL / stipulated)*
**Evidence.** `phase1` builds components of `{v ∈ core : beta[v] < 0}` under the node adjacency,
sets `q_j = M_j/D`, `HHI = Σ q_j²`, `k = min(max(round(1/HHI), 1), len(comps))`, and adds
`min(comp, key=(beta, index))` for each of the top-k clusters by mass. Every element specified,
including the index tie-break the spec leaves implicit but which `k`'s determinism needs.

### V015 — CONFIRMED
**Claim.** Phase 2 solves the uncapacitated min-cost flow with unit arc costs serving `b_g` and
orients every support edge by its net flow. *(MODEL / stipulated)*
**Evidence.** `phase2` calls `mincost_flow(b, 0)`, which is
`linprog(c = ones(318), A_eq, b_eq = c − s, bounds = (0, None), method = "highs")` — uncapacitated
(no upper bound), unit-cost, node-balance-constrained. `net_per_edge` reduces the 318 arc flows to
159 signed edge nets and `phase2` orients by sign. Faithful.

### V018 — CONFIRMED
**Claim.** Edges with zero net flow are free and deferred to Phase 3. *(MODEL / stipulated)*
**Evidence.** `phase2` classifies `|net| ≤ ZERO_TOL` into `free` and leaves them unoriented until
`compile_dirs` reads the sweep's marking order. Measured on 1444: 80–81 of 159 edges are free per
good (the complement of V186's 78–79-edge support).
**Note.** "Zero" is implemented as an **absolute** tolerance of 1e-11, which §2.3 calls "numerical
only". V214 shows it is not purely numerical — it is the reason DRAIN is not scale-invariant
downward.

### V019 — CONFIRMED
**Claim.** Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is
already marked and it is a selected sink, has a flow out-arc, or has a free edge to a marked node.
*(MODEL / stipulated)*
**Evidence.** `sweep_priority.ready(u)` is exactly
`u not in marked and cnt[u] == 0 and ((u in Sset) or (len(outs[u]) > 0) or any(w in marked for w
in freeadj[u]))`, where `cnt[u]` counts unmarked flow out-neighbours. The conjunction and the
three-way disjunction match the stipulation term for term — and its monotonicity is what V033's
scan-invariance proof rests on.

### V020 — CONFIRMED
**Claim.** Ready nodes pop by the deterministic priority key (DEF ascending, b ascending, index),
where `DEF(v)` is total downstream demand on the flow-arc subgraph. *(MODEL / stipulated)*
**Evidence.** `run_drain(deterministic=True)` selects `key_mode="defasc_beta"`, i.e.
`keyfn = (DEF[v], beta[v], pid[v])` — ascending on all three ✓. `flow_def` computes
`DEF[v] = max(0, −beta[v]) + Σ_{u ∈ outs[v]} DEF[u]` over a reverse-topological pass on the
flow-arc subgraph only ✓. The adopted key is the one `drain-orientation.md` §6 selected, and the
rejected DEF-descending variant survives in the same file behind a different `key_mode` (V193).

### V022 — CONFIRMED
**Claim.** On a stall, the heaviest flow-terminal demander is promoted into the sink set — the
self-correction that supplies the real sink count. *(MODEL / stipulated)*
**Evidence.** On an empty ready-heap, `sweep_priority` collects gated unmarked nodes, filters to
`len(outs[u]) == 0 and inflow[u] > ZERO_TOL` (flow-terminal with inflow), and promotes
`min(terminals, key=(beta, index))` — most negative balance, i.e. heaviest demander ✓. The
"supplies the real sink count" half is measured: 1–8 promotions per good, mean 2.9, against Phase
1 selecting one node for 27 of 29 goods (V013, V030).
**Note.** `drain.py` carries a documented fallback for the case where the gated set contains no
flow-terminal demander — a case the spec's lemma does not cover. It fired **0 times** across 29
goods on 1444, at every α tested, and in the `Φ_w` solve. The gap is real but empirically inert;
it is the same lemma-coverage gap that makes V029 refutable in principle.

### V023 — CONFIRMED
**Claim.** Free edges orient from later-marked to earlier-marked. *(MODEL / stipulated)*
**Evidence.** `compile_dirs`: `(u, v) if order[u] > order[v] else (v, u)` — higher marking order
(later) is the tail ✓. This is the rule V026's DAG argument and V060's potential argument both
consume.

### V024 — CONFIRMED
**Claim.** Phase 4 un-peels the Phase-0 pendants in reverse. *(MODEL / stipulated)*
**Evidence.** `compile_dirs` iterates `reversed(Plog)`, so pendants are restored in exact reverse
peel order ✓. Inert on the vanilla map (V009), which is why V126's counterexample needed a
constructed graph.

### V059 — CONFIRMED (superseded by V212)
**Claim.** `Φ_ord = Σ_g V_g · order_g`, where `order_g(v)` is `v`'s marking order in `g`'s
drainage sweep. *(MODEL / stipulated, replaces C060)*
**Evidence.** Well-defined and implemented as written; reproduces the aggregate the v2.0 spec
measured (its agreement figure is V062, REFUTED at 60.2%). **Superseded by the v2.1 addendum** —
`Φ_ord` is no longer the installed graph (V212), and §3.15 retains it as a rejected entry and a
coherence ceiling.
**Note.** The definition has one gap the v2.0 text never closed: on a map where Phase 0 acts,
pendant nodes have no marking order, so `Φ_ord` is undefined there (V060). The move to `Φ_w`
inherits the same gap through V218 rather than fixing it.


---

# Part 6 — the v2.1 addendum: `Φ_ord` → `Φ_w` (V212–V230)

**Reference implementation used.** `Φ_w = DRAIN(b_w)` with `s_w(n) = 1/N`,
`c_w(n) = Σ_{p∈n} wealth(p)^1.5 / Σ_world wealth^1.5`, `b_w = s_w − c_w`, run through the same
`run_drain` (deterministic sweep) the per-good graphs use — the spec's "30th solve, same code
path" taken literally (`phiw.py`). The `wealth` vector is the reference solver's, which does
**not** apply §1.3's autonomy floors (systemic finding 1). `Φ_w` is the claim family most exposed
to that gap: it is nothing but the wealth field.

**Superseded v2.0 claims.** V059, V061, V088, V160, V161, V196, V199 and C499 are replaced by
this addendum. Their Part 2/3 verdicts above stand as validations of the v2.0 text; they no
longer describe the installed graph. **V062 is explicitly retained** by the claims file as a
measurement of the superseded `Φ_ord` — and it is REFUTED (60.2%, not 62.7%), which now also
lands on V219 and on three v2.1 spec sites.

### V212 — CONFIRMED
**Claim.** `Φ_w = DRAIN(b_w)` with `s_w = 1/N`, `c_w = wealth^α_Φ` shares, `b_w = s_w − c_w` —
the §1.1 operator run once more with wealth as the good; `Φ_w` is the graph installed in the
game. *(MODEL / stipulated)*
**Method.** Implemented exactly as written and run through the unmodified `run_drain`.
**Evidence.** The definition is complete and executable with no free choices: it produces a
single orientation, 159/159 edges, acyclic, and reproduces every §1.6 measurement the spec states
(V215–V219 below). As a stipulation it is CONFIRMED in the sense that matters — it is
well-defined, implementable, and the artifact it names is the one the other addendum claims
measure. Note `α_Φ` must be supplied (V213); with it, nothing else is underdetermined.

### V213 — OUT_OF_SCOPE
**Claim.** `α_Φ = 1.5` is a stipulated design constant like `P₀`, calibrated once so the 1444
start yields the hangzhou/english_channel two-sink map; world-responsiveness flows through the
wealth field, never through the knob. *(DESIGN / stipulated)*
**Note (supporting, not a verdict).** The calibration story checks out arithmetically: α_Φ = 1.5
is the only integer-or-half-integer value in 1…8 giving exactly the stated two-sink
hangzhou/english_channel map (α = 1 → 5 sinks, α = 2 → 1 sink; see V224). The "world-
responsiveness flows through wealth, never the knob" half is a design assertion, and V223's
dynamics are its evidence.

### V214 — PARTIAL
**Claim.** DRAIN orientation is scale-invariant in `b`: only the sign pattern and proportions
matter, so any (−1, 1) normalization of node wealth yields the same graph. *(MODEL / derivation)*
**Argument check.** In exact arithmetic the claim is sound for any λ > 0: Phase 0 reads only the
*sign* of subtree balances; Phase 1's HHI is built from mass *shares* (`q_j = M_j/D`), so k and
the heaviest-demander choice are scale-free; Phase 2's LP scales its optimum by λ with identical
net-flow signs; Phase 3's key (DEF, b) is order-isomorphic under positive scaling. **But the
implementation's free-edge test is an absolute tolerance** (`ZERO_TOL = 1e-11`), not a relative
one, so scaling `b` down pushes genuine flow arcs into the free set and re-orients them by the
sweep instead.
**Evidence (measured, `phiw2.py`).**

```
scale 1e-09 flips=100 sinks=['genua']                     scale 1e-04 flips=13 sinks=[ec,hangzhou]
scale 1e-06 flips=100 sinks=['genua']                     scale 1e-02 flips=13 sinks=[ec,hangzhou]
scale 1e-05 flips=29  sinks=['genua','hangzhou','saxony'] scale 1..1e4 flips=0  sinks=[ec,hangzhou]
```

**What is true.** Scale-invariance holds for scaling **up** and fails for scaling down past the
absolute tolerance — at ×1e-6 the sink set collapses from two to one. The claim's own
application is safe: 1444's `max |b_w| = 0.0226`, so normalizing into (−1, 1) scales *up* by ~44×.
**Spec text to change.** §1.6: "DRAIN orientation is scale-invariant, so any (−1, 1)
normalization of node wealth yields the same graph" → add the premise, e.g. "…provided the
zero-flow tolerance is scaled with `b` (it is absolute, `1e-11`); normalizing into (−1, 1) scales
1444's `b_w` up and is safe."
**Blast radius.** V212's implementation contract; §2.3's "zero-flow tolerance (numerical only)"
parenthetical — it is not purely numerical, it is a scale-coupled semantic threshold.

### V215 — PARTIAL
**Claim.** Measured at α_Φ = 1.5: exactly two sinks — `hangzhou` (wealth rank 3) and
`english_channel` (rank 2); Phase 1 selects `genua`; both sinks arrive by stall promotion;
`genua` ends a transit node. *(MODEL / numerical test)*
**Method/Evidence (fresh).** Sinks exactly `{hangzhou, english_channel}` ✓. Phase 1 selects
`{genua}` ✓. Both sinks arrive by stall promotion, zero fallbacks ✓. `genua` ends with
outdeg 2 / indeg 3 — a transit node ✓.
**What is not true as written.** The parenthetical ranks. Measured:

| node | node wealth | rank | `c_w(α=1.5)` | rank |
|---|---|---|---|---|
| english_channel | 316.6 | **1** | 0.03412 | **2** |
| hangzhou | 226.7 | **12** | 0.03156 | **3** |
| genua | 296.0 | 3 | 0.03508 | 1 |

"Ranks 3 and 2" match the **α_Φ-weighted field `c_w`**, not node wealth — under which hangzhou is
rank **12**, not 3. A reader takes "wealth rank 3" to mean the third-wealthiest node.
**Spec text to change.** §1.6: "two sinks, `hangzhou` and `english_channel` (wealth ranks 3 and
2 …)" → "(ranks 3 and 2 in the α_Φ-weighted demand field `c_w`; by raw node wealth they are 12th
and 1st)".

### V216 — PARTIAL
**Claim.** 8 sources, all cul-de-sacs; every node drains to a sink; acyclic; 159/159 edges
oriented; 0 fallback promotions. *(MODEL / numerical test)*
**Method/Evidence (fresh).** Sources (indeg 0): **8** ✓ — `kongo`, `james_bay`,
`mississippi_river`, `chengdu`, `cuiaba`, `australia`, `yumen`, `safi`. Every node drains to a
sink: **80/80** ✓. Acyclic ✓. 159/159 oriented ✓. Fallback promotions **0** ✓.
**What is not supported.** "All cul-de-sacs." Their degrees are 3, 2, 4, 4, 5, 3, 2, 2 — only
**3 of 8** are degree-2; mean 3.12 against the map's 3.98. They are uniformly *poor* (c_w ranks
44–75 of 80), which is the real and much stronger pattern: `Φ_w` sources are the wealth field's
troughs, not the graph's dead ends.
**Spec text to change.** §1.6: "Eight sources, all cul-de-sacs" → "Eight sources, all in the
bottom half of the wealth field (c_w ranks 44–75); mean degree 3.1 against the map's 4.0."

### V217 — CONFIRMED
**Claim.** 0 edge flips and 0 sink-set changes under ±1% province-wealth noise across 5 seeds —
stabler than any per-good graph. *(MODEL / numerical test)*
**Method/Evidence.** Five seeds, each perturbing every province's wealth by U(−1%, +1%), full
re-solve: **flips [0, 0, 0, 0, 0], sink-set changes 0/5** ✓. The comparison holds too: under the
same noise the per-good graphs move (grain 0.8 edges/159 and 1/5 sink-set changes, fresh).

### V218 — CONFIRMED
**Claim.** The installed graph is a legal DAG: `Φ_w` is a DRAIN orientation, acyclic by the
marking-order argument, and its own marking order is a per-node scalar whose descending
comparison reproduces the DAG (0 violations measured). *(MODEL / numerical test, replaces C499
and V061)*
**Argument check.** Inherits V026's argument, which is sound for any input: every arc points
later-marked → earlier-marked, so reversed marking order is a topological order. The
potential-reconstruction half is V060's argument restricted to a single orientation, and the
pendant caveat that made V060 PARTIAL cannot bite here for a different reason worth stating: it
would bite on a modded map where Phase 0 acts, exactly as for the per-good graphs.
**Evidence (fresh).** Order-descending violations **0**; exact order ties across an edge **0**;
acyclic ✓; 0 edges without an order (Phase 0 is a no-op on vanilla).
**Note.** This is a genuine improvement over the v2.0 pairing: `Φ_ord` needed the
value-weighted-sum-of-potentials argument (V061) to be acyclic, whereas `Φ_w` is a DRAIN
orientation directly and gets acyclicity from the operator it already ships.

### V219 — PARTIAL
**Claim.** `Φ_w` agrees with the per-good graphs on 53.4% of edge-goods (52.1% value-weighted) —
lower than the superseded `Φ_ord`'s 62.7%. *(MODEL / numerical test)*
**Method/Evidence (fresh).** `Φ_w`: **2462/4611 = 53.4%**, value-weighted **52.1%** — both exact ✓.
**What is not true.** The comparator. Under the deterministic sweep the spec adopts, `Φ_ord`
agrees on **60.2%**, not 62.7% (V062). The coherence sacrificed by moving to `Φ_w` is **6.8
points**, not 9.3.
**Spec text to change.** §1.6 line 165, §3.9 line 679, §3.15 line 852 — all three quote 62.7%.
**Why it matters.** §3.9's and §3.15's argument is that self-coherence was *knowingly traded* for
legible ends, and §3.15 keeps `Φ_ord` as "the measured coherence ceiling any future aggregate
should be compared against". A ceiling quoted 2.5 points too high mis-prices every future
comparison against it.

### V220 — OUT_OF_SCOPE
**Claim.** Why `Φ_w` is installed: the direction-dependent systems model power, not commodity
logistics; vanilla's authored arrows encode empires pointing at the biggest cities; `Φ_w`
computes that intent from world state, and self-coherence was knowingly traded for legible,
wealth-anchored, world-responsive ends. *(DESIGN / stipulated)*
**Note.** The factual premises it rests on are validated separately and mostly hold: V221
(three authored ends) ✓, V222 (`Φ_ord`'s ends are not places) largely ✓, V223 (ends move with
wealth) ✓ under one reading. The magnitude of the trade is mis-stated by V219/V062.

### V221 — CONFIRMED
**Claim.** Vanilla's `00_tradenodes.txt` declares exactly three end nodes: `genua`, `venice`,
`english_channel`. *(ENGINE / file value)*
**Method/Evidence.** Re-parsed the shipped file this session: `end=yes` count **3** —
`['genua', 'venice', 'english_channel']`; the same three are the only nodes with zero `outgoing`
blocks. Exact.

### V222 — PARTIAL
**Claim.** `Φ_ord`'s ends are sweep-scheduling artifacts, not places: of its 18 end nodes at
1444, 9 terminate no good and none of the demand capitals is among them; and its end count is
α-invariant under the adopted key (9–17 measured across α up to 16). *(MODEL / numerical test)*
**Method/Evidence (fresh).** `Φ_ord` end nodes: **18** ✓ — of those, terminating no good at all:
**9** ✓ (`amazonas_node`, `basra`, `chengdu`, `james_bay`, `kiev`, `ohio`, `ragusa`,
`rio_grande`, `yumen`). Top-5 demand capitals (`genua`, `english_channel`, `hangzhou`,
`gulf_of_siam`, `malacca`): **none** is among them ✓. Three exact hits.
**What does not reproduce.** The α range. Sweeping the per-good exponent (cloves α = 2 … 64)
gives end counts **16, 18, 15, 22, 17, 13** — a measured range of **13–22**, not 9–17. The
claim's own baseline figure (18) already sits outside the band it quotes.
**What is true.** The load-bearing point holds *more* strongly than stated: across every α tested
the end count never approaches vanilla's 3 — the minimum observed is 13. "α-invariant" is also
the wrong word for a quantity ranging 13–22; "never concentrates" is the accurate one.
**Spec text to change.** §3.9: "its end count is essentially un-steerable (α-invariant under the
adopted key; measured 9–17 ends across α up to 16)" → "…never concentrates: 13–22 ends measured
across cloves α = 2…64, never approaching vanilla's three."

### V223 — PARTIAL
**Claim.** Dev-stacking `hangzhou`'s top province ×30 makes it the sole world sink; scaling
European node wealth ×2 makes `genua` the sole sink; at ×3 the Cape of Good Hope reverses —
Atlantic→Cape→Indian-Ocean drainage becomes malacca/comorin_cape/zanzibar→Cape→ivory_coast.
*(MODEL / numerical test)*
**Method.** Re-ran each shock through the full `Φ_w` solve. The baseline Cape is
`in ← ivory_coast`, `out → {comorin_cape, malacca, zanzibar}` — the Atlantic→Cape→Indian-Ocean
drainage the claim describes ✓.
**Evidence.**
- **Dev-stack ×30 → sole sink `hangzhou`** ✓ exactly (also at ×20 and ×50; at ×10 the sink set is
  still three).
- **European ×2 and the ×3 reversal are set-dependent.** The spec never says which nodes count as
  European. Under a 22-node set (18 western/central European nodes plus `constantinople`,
  `crimea`, `kiev`, `kazan`) both stated thresholds land exactly: ×2 → sinks `{genua}` ✓, and
  ×3 → Cape `in ← {comorin_cape, malacca, zanzibar}`, `out → {ivory_coast}` — the claimed
  reversal, verbatim ✓. Under the 18-node western set, ×2 gives three sinks
  (`{english_channel, genua, rheinland}`) and sole-`genua` needs ×2.5, while the Cape reversal
  arrives early, at ×2.
**What is true.** Every qualitative dynamic reproduces — the sink follows dev-stacked wealth, a
richer Europe collapses the map onto Genoa, and a richer-still Europe flips the Cape corridor.
The stated multipliers are exact under one reading of "European node" and off by half a step
under another.
**Spec text to change.** §1.6: name the node set, e.g. "scaling the 22 European node's wealth
(the 18 western/central nodes plus Constantinople, Crimea, Kiev, Kazan) ×2 …".

### V224 — CONFIRMED
**Claim.** The `Φ_w` sink count is emergent and non-monotone in α_Φ (5→2→1→2→3→1 across
α = 1…8): it tracks how many world-class wealth poles the flow separates, not α itself. *(MODEL
/ numerical test)*
**Method/Evidence (fresh).** The six quoted values reproduce **exactly** at
α ∈ {1, 1.5, 2, 3, 4, 8}:

| α_Φ | 1 | 1.5 | 2 | 3 | 4 | 8 |
|---|---|---|---|---|---|---|
| sinks | 5 | **2** | 1 | 2 | 3 | 1 |

Filling in the integers the sequence skips: α = 5 → 3, α = 6 → 2, α = 7 → 1. Non-monotone under
either sampling ✓, and the sinks are recognisable wealth poles throughout (`hangzhou` at every
α ≥ 2, joined by `genua` and `doab` in the middle band).
**Note for the reader.** "across α = 1…8" gives six numbers for eight integers; the sample points
are {1, 1.5, 2, 3, 4, 8}. Worth stating, since the α = 1.5 entry is the design's own operating
point and is not an integer.

### V225 — PARTIAL
**Claim.** A pure `wealth^α` edge comparison can never concentrate ends: a local wealth maximum
survives every positive α (measured ≥10 ends at all α up to 16); a 3-mass gravity kernel over
the top-3 pairwise-unconnected demanders hits any chosen count exactly with 69% vanilla-arrow
agreement. *(MODEL / numerical test)*
**Argument + evidence, three parts.**
1. **"A local wealth maximum survives every positive α" — sound and general.** Orienting each
   edge toward the higher `wealth^α` is a monotone rule, and monotone transforms preserve the
   local-maximum set exactly: the ends are the local maxima of the *wealth field*, a set α cannot
   touch. This is a theorem, not a measurement, and the spec could claim it as one.
2. **"≥10 ends at all α up to 16" — CONFIRMED.** Measured 15, 15, 14, 11, 10, 12 at
   α = 0.5, 1, 2, 4, 8, 16.
3. **The gravity kernel — count confirmed, agreement not.** Implementing
   `Φ(n) = max_m c_α(m)·γ^dist(n,m)`, the end count equals the number of masses exactly and
   robustly: 1→1, 2→2, 3→3, 4→4, 5→5, 6→6 across γ ∈ [0.1, 0.7] (merging only past γ ≈ 0.9).
   That is the sense in which it "hits any chosen count exactly", and it is precisely why V226
   rejects it as pinned by fiat. **Vanilla-arrow agreement peaks at 66% (105/159, γ = 0.97)** in
   my construction — 62% over most of the γ plateau — not 69% (which would be 110/159). My seed
   selection (the top-3 pairwise-non-adjacent nodes by `c_w(1.5)`: genua, english_channel,
   hangzhou) and tie-breaks may differ from the original run; I report the gap rather than
   asserting the original is wrong.
**Spec text to change.** §3.15: either re-derive the 69% with the original construction recorded,
or quote the reproducible 66%. Part 1's structural claim would be stronger stated as the theorem
it is.

### V226 — OUT_OF_SCOPE
**Claim.** Pinned-count wealth fields (top-k seeding, gravity kernels) are rejected: they pin the
end count by fiat — a world conquest could never merge the world into one basin — and need a
second operator with its own reach knob γ; the emergent-count wealth good replaced them.
*(DESIGN / stipulated)*
**Note.** Its factual premise is confirmed by V225 part 3: the end count tracks the seed count
exactly and independently of γ, so the count is indeed set by fiat rather than by the world.

### V227 — OUT_OF_SCOPE
**Claim.** `φ₀` as the installed graph, graveyard entry updated: the installed graph is `Φ_w`
(v2.0 briefly used `Φ_ord`) and its correctness check is cross-implementation orientation
equality. *(DESIGN / stipulated)*

### V228 — CONFIRMED
**Claim.** "The aggregate map is not a DAG" is still an error: the aggregate is a DAG because
`Φ_w` is a DRAIN orientation (marking-order argument) whose own marking order is a per-node
scalar reproducing it. *(MODEL / derivation, replaces V199)*
**Argument check.** Sound, and structurally cleaner than the claim it replaces. V199 needed two
steps (Φ_ord is a per-node scalar; orientation-by-scalar cannot cycle). V228 needs only V026's
argument — every arc points later-marked → earlier-marked — which is a property of the operator
and holds for any input. The potential-reconstruction half (V218, 0 violations measured) is a
bonus for consumers that need a scalar, not a load-bearing step in the acyclicity proof.
**Note.** The v1 error being corrected (net flow is the gradient of Φ) remains false by
measurement, re-verified fresh (V162: the value-weighted net flow contains directed cycles).

### V229 — OUT_OF_SCOPE
**Claim.** Solver item 5 closes with `Φ_w`: one more DRAIN run with wealth as the good — the
30th solve, same code path. *(DESIGN / stipulated)*
**Note.** Taken literally in the reference implementation and it works unmodified: `Φ_w` is
`run_drain(b_w)` with no special-casing, and the whole `Φ_w` battery above runs through the same
function as the 29 goods. The cost claim is also comfortable — one more solve on a 29-solve
budget measured at 5.9 ms each (V090).

### V230 — REFUTED
**Claim.** A latent good leaves `Φ_w` unaffected: `Φ_w` reads wealth, not goods. *(MODEL /
derivation)*
**Argument check — the derivation is invalid.** `Φ_w` reads `wealth`, and §1.3 defines
`wealth(p) = tax_income(p) + production_income(p)`, where production income is
`goods_produced(p) × price(good(p))`. Wealth is therefore a *function of the province's good and
its price*. "Reads wealth, not goods" is a false dichotomy: reading wealth **is** reading goods,
one layer down. A latent good is not inert in that layer — `is_latent = yes` goods *replace* the
province's trade good when their trigger fires (verified in `00_tradegoods.txt`, coal block), and
coal's `base_price = 10` against a typical incumbent of 2.0–3.0 is a large repricing.
**Evidence (measured, `phiw.py`).** Flipping the 45 owned latent-coal provinces of the 58
(V057) to coal at `base_price = 10`: world wealth 10,572.4 → 10,788.8, and **`Φ_w` flips 10 of
159 edges**. The two sinks survive this particular shock, so the installed graph does not change
character — but it does change, and the claim says it does not.
**What is true.** While a good is latent (zero world production) it is invisible to `Φ_w`,
because no province carries it. The moment it activates — the exact event §1.5 and §2.8's
"Latent good" row are about — it moves the wealth field and therefore the installed graph.
**Spec text to change.** The §2.8 "Latent good" row and §1.6's independence framing: "A good with
zero world production has no graph, no `Φ_w` contribution…" → say instead that a latent good is
invisible to `Φ_w` *only while latent*, and that activation reprices its provinces and perturbs
`Φ_w` through wealth (measured: 10 of 159 edges for vanilla's 58 latent-coal provinces).
**Blast radius.** V212's framing of the wealth good as good-independent; the §2.8 latent-good
row; any future claim that separates "the wealth field" from "the goods economy" — under
`wealth = tax + production_income` they are not separable. Note this is a **regression introduced
by v2.1**: under v2.0's `Φ_ord` the same proposition was true, because a latent good's `V_g = 0`
gave it literally zero weight in the aggregate.


---

# Part 7 — OUT_OF_SCOPE and DEFERRED

## DESIGN — OUT_OF_SCOPE (52)

Per the brief, DESIGN claims are decisions rather than propositions about the world and are not
graded. Listed for completeness, with a note where this validation produced evidence bearing on
one.

**§1.1–§1.6:** V010, V012, V014, V025, V039, V064.
**§1.7–§2.4:** V065, V070, V085, V087, V088, V093, V094.
**§2.7–§2.9:** V097, V101, V102, V103, V104, V109, V110, V111, V112, V113.
**§3.x:** V139, V147, V150, V154, V161, V166, V169, V174, V175, V176, V178, V181, V182, V183,
V184, V192, V194, V195, V196, V197, V198, V206, V209, V210.
**v2.1 addendum:** V213, V220, V226, V227, V229.

Evidence produced in passing that a future pass should attach to these:

- **V025** ("all five §1.1 properties … all verified on 1444 data") — true as stated for the
  *measurements*; three of the five paired **derivations** do not hold in general (V029 refuted;
  V031, V016/V060 partial). The design claim is about the verification discipline, and the
  discipline worked: it is what surfaced the split.
- **V087** (solver item 4 applies the §1.3 floors) — the reference solver **does not**; see
  systemic finding 1. This is a DESIGN claim about what the solver should compute, so it is not
  graded, but the gap between it and `solver.py` is the single largest unstated caveat on every
  measured number in the spec.
- **V093 / V094** (design constants) — re-read fresh: `P₀ = 2.0` ✓, `ρ = 1.0` ✓, `r = 0` ✓,
  zero-flow tolerance `1e-11` ✓, and v2.1 adds `α_Φ = 1.5` ✓. The "numerical only" description of
  the tolerance is contradicted by V214.
- **V109** (acyclicity asserted on every per-good graph, on the aggregate, and on the emitted
  file's declaration order) — all three are checkable and all three pass on 1444 (V028, V218,
  V095's ordering convention).
- **V110 / V111 / V112** (per-tick assertions) — each is implementable and each passes now:
  reachability 29/29 (V032), conservation `unserved == stranded` to <1e-9 on 29/29 (V089),
  determinism 0 flips under permuted keys (V035) and one orientation over six solves (V037).
  These assertions are also what would catch V029's and V031's general-case failures at runtime,
  which is the strongest argument in the spec's favour on those two refutations.
- **V178** (calibration settings) — reproduced exactly: α unclamped at exponent 2 (cloves α = 16),
  ρ = 0.5, twig tolerance 3e-4 (V177).
- **V183** (the cross-machine question replaces the ε-magnitude question) — correctly identifies
  the live risk; V151 and V214 both reduce to it.
- **V196** — superseded by V227 in the v2.1 addendum.

## OUTCOME — DEFERRED (3)

Per the brief, OUTCOME claims are deferred. Each is one step from settleable and carries the note
below.

- **V058** — "The latent-coal provinces convert province-by-province over years, not in a single
  tick; the graph grows as they do." *Its file premises are confirmed* (V055's per-province
  trigger, V056's conditions, V057's 58 provinces): the trigger is evaluated per province against
  that province's own institution progress, so simultaneity would require 58 provinces to reach
  100% progress on the same tick. Settling observation: an observer run past 1700.
- **V077** — "A power share oscillating across any of these limits flickers the mechanic,
  Propagate Religion included." *Now narrower than stated*: V075/V076 show the flagless default
  branch (50/50) and the terminal fallback (35/35) have no band and do flicker, but the nine
  country-flag ladder rungs are banded by 5–10 points and absorb chatter. The claim holds for
  flagless countries.
- **V136** — "Under node-level α, Nippon would out-consume the Paris node on province count."
  *Direction confirmed, magnitude corrected by V134*: with 68 vs 33 land provinces (V135), the
  node-level form overweights Nippon relative to the per-province form by `(68/33)^(α−1)` = 1.44×
  at α = 1.5 — not by the "equal total wealth" comparison V134 refutes.

---

## Closing note on the audit's own standard

The brief asked whether finding v2 wrong was achieved and, if not, why I would believe the
document. It was: **11 refutations and 24 partials across 230 claims**, against v1's 23 and 37
across 685 — a comparable rate per in-scope claim, on a document that had already absorbed one
full audit.

Three patterns are worth carrying into the next pass.

1. **The inherited number is still the dominant failure mode.** V159's 98.8% is v1's LAP
   measurement carried into a document whose operator changed; V062's 62.7% is v2.0's own
   pre-deterministic-sweep number carried past the sweep change and then propagated into v2.1's
   V219 and three spec sites. Both survived because they were *plausible* and *previously
   measured* — exactly the profile of the stale autonomy floor that survived four versions. The
   mechanical fix is cheap: every measured figure in the spec should carry the script and the
   operator revision that produced it.
2. **Measurements verify; derivations do not.** Every one of the twelve claims stating a
   derivation and a measurement as a pair had a passing measurement, and six of the twelve had a
   derivation that does not hold for general input (V029, V031, V016, V060, V151, plus V214 in the
   addendum). Not one was catchable by re-running the solver; all six needed either a constructed
   counterexample or an audit of an unstated premise. §1.1's two-statement discipline is what made
   them findable at all, and it is the single most valuable structural change from v1.
3. **The newest text is the weakest.** The v2.1 addendum is 8% of the claims and 30% of the
   defects, including the only claim whose derivation points the wrong way — V230, a proposition
   that was *true* under `Φ_ord` and silently became false under `Φ_w`. Operator swaps do not just
   invalidate measurements; they invalidate propositions whose truth depended on the old
   operator's structure, and those are much harder to spot because nothing about them looks
   numeric.

Answering §3.16's own closing question — "which property of the output does this spec still not
state?" — for v2.1 specifically: **it does not state what `Φ_w` depends on.** It says "wealth, not
goods", and under `wealth = tax_income + production_income` that separation does not exist. The
installed graph is a function of every province's trade good and every good's price, which is why
a latent good moves it (V230) and why the missing autonomy floors (systemic finding 1) reach it
too. That dependency is now the single largest unstated property of the model's principal output.
