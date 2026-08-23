# Audit part B — X005–X017, X116, X117, X125, X128–X138, X139–X151, X184

Tooling: the author's `drain.py` / `toys.py` / `v5measure.py` / `final.py` / `drainrep.py` /
`audit_delta.py` / `audit_delta2.py`, re-run unmodified, plus audit-only files written for this pass:
`scripts/_audit_b_drain.py` (an independent §1.1 reimplementation written from the spec text —
validated two ways: it reproduces `toys.py`'s T1/T2/T3 exactly, and it reproduces `drain.py`'s
orientation with **0/29 disagreements** across all 29 goods of 1444), `_audit_b_reconcile.py`,
`_audit_b_odd.py`, `_audit_b_1444perm.py`, `_audit_b_lpmag.py`, `_audit_b_measure.py`,
`_audit_b_final.py`, `_audit_b_saves.py`.

**Counts: 30 CONFIRMED, 8 PARTIAL, 3 REFUTED.**

> This file was deleted once by a process outside the audit session and rewritten from the same
> measurements. X151's evidence is corrected relative to the first version, and systemic finding 6 is
> new — see both.

---

### X005 — Fallback branch: with no flow-terminal demander among the candidates, promote the highest-wealth candidate, ties by node index
**Status:** CONFIRMED
**Method:** Read the branch in both sweeps of `drain.py` (`sweep`, `sweep_priority`) and in `toys.py`;
checked it against §1.1's Phase-3 wording and the guard it sits behind.
**Evidence:** Both sweeps carry `s_star = max(gated, key=lambda v: (NODEW[v], -v))`, reached only when
`terminals = [u for u in gated if len(outs[u]) == 0 and inflow[u] > ZERO_TOL]` is empty — exactly "the
candidates hold no flow-terminal demander". `-v` resolves wealth ties to the *lowest* index; the spec
says only "ties by index", which the implementation satisfies. The guard does not test `b < 0` and does
not need to: a node with zero outflow and positive inflow has `b = -inflow < 0` by LP conservation, so
every "flow-terminal" is genuinely a demander.

---

### X006 — Node wealth is a good-independent input, so the fallback needs no bootstrap
**Status:** CONFIRMED
**Method:** Traced `NODEW` back to `solver.ROWS`; checked when it is computed and what it depends on.
**Evidence:** `NODEW[NIDX[r["node"]]] += r["tax"] + r["prod_income"]` over `solver.ROWS`, executed at
module import — before any solve, with no `g` in the expression (the per-good exponent `α(g)` is applied
to `C`, never to `NODEW`). Available when the fallback fires, and independent of the good being
oriented: no bootstrap. On 1444: 80 values, range 0.0 (`cape_of_good_hope`) … 316.6
(`english_channel`), **80 of 80 distinct**, min positive 1.50.
*Note (not a refutation):* in X009's per-good case the key is degenerate. `build_sc` puts no per-good
gate on demand, so `c_g(n) > 0` for every good at every node with an owned province; a per-good
component with no consumer is a component with no owned provinces, where `NODEW ≡ 0` and the wealth key
carries no information at all.

---

### X007 — Candidates are the unmarked nodes whose flow out-neighbours are all marked; the flow subgraph is acyclic, so at least one always exists and the sweep always advances
**Status:** CONFIRMED
**Method:** Proved it, then brute-forced it.
**Evidence:** Proof. (a) With unit arc costs a directed cycle in the support could be cancelled for
strictly lower cost, so *every* optimum has acyclic support — the premise is a theorem, not a solver
property. (b) The flow-arc subgraph induced on the unmarked set is a finite DAG and has a sink; that
sink has all its flow out-neighbours marked, i.e. `cnt == 0`, i.e. it is a candidate — so the candidate
set is non-empty whenever anything is unmarked. (c) At a stall the promoted/fallback node joins `Sset`
and is gated, hence `ready`, hence popped next iteration: progress is strict.
Brute force: 11,381 random connected graphs (n = 4–6, random zero-sum balances, random wealths) —
`NO_CANDIDATE` 0, `LIVELOCK` 0, cyclic flow support 0. I also checked the heap discipline in
`sweep_priority`: `ready` is monotone in the marked set, and every transition that can make a node ready
(`cnt` decrement, `Sset` growth, a free neighbour being marked) is followed by a push, so a reported
stall is never a missed wake-up.

---

### X008 — The fallback fires only when every candidate is support-isolated with zero balance — on a connected core, only when `b ≡ 0` across it
**Status:** PARTIAL
**Method:** Proved the intended statement, then attacked the literal one.
**Evidence:** Proof of the intended statement: at a fallback stall no unmarked node has a flow out-arc
(following flow arcs forward inside the unmarked set otherwise reaches a candidate with `inflow > 0`,
firing the *promotion* branch, or the node itself is `ready`), hence none has a flow in-arc either (its
source would then have an out-arc), hence every unmarked node is support-isolated and `β = 0` by
conservation. If any node were already marked, connectivity gives an edge from the unmarked set to the
marked set; that edge is free (its unmarked endpoint carries no flow), so its unmarked endpoint is
`ready` — contradiction. So the marked set is empty, the flow is empty, `β ≡ 0` across the core.
**The spec's stated "because" clause does not reach this conclusion** — it yields only "the candidates
are support-isolated"; the step to *the whole core* needs the connectivity + free-edge argument, which
§1.1 never gives.
Brute force agrees with the intended reading: 114 fallback firings in 11,381 instances, all on a
connected core, all with `β ≡ 0` on the core. But `b` is defined at the head of §1.1 as
`b_g(n) = s_g(n) − c_g(n)`, and under *that* reading the claim is false: **75 of the 114 firings had
`b ≢ 0`**. Minimal counterexample, reproduced in both implementations — nodes A,B,C,L; edges A–B, A–C,
B–C, A–L; `b = (A +1, B 0, C 0, L −1)`, an ordinary good with one producer and one consumer. Phase 0
peels L and folds −1 into A, so `β ≡ 0` on the connected triangle, the sweep stalls at `t = 0` with no
flow-terminal demander, and the fallback promotes A.
**Should say:** "…on a connected core, only when the **post-peel balance `β`** is identically zero
across it — which Phase 0's fold can produce from a `b ≢ 0` input", plus the missing step: any edge from
the unmarked set to a marked node is free, so on a connected core a stall with support-isolated
candidates can only occur before anything is marked.
*(Second order: `ZERO_TOL` is absolute (1e-11), so "support-isolated ⇒ β = 0" is exact only to
`deg × 1e-11`; §1.6 already records the scale coupling.)*

---

### X009 — That happens for the aggregate graph on a uniform-wealth map, and for a per-good graph on a component with no producer and no consumer
**Status:** REFUTED
**Method:** Tested both named cases against §1.6's definition of `b_w` and against the peel.
**Evidence:** *Case (a) is false as stated.* §1.6 sets `s_w(n) = 1/N` and
`c_w(n) = Σ_{p∈n} wealth(p)^{α_Φ} / Σ_world`, so `b_w ≡ 0` requires **equal `Σ_{p∈n} wealth(p)^{1.5}`
per node** — which "uniform wealth" does not deliver. Measured: three nodes with *identical node wealth*
2.0 but province splits (1+1)/(2)/(2) give `b_w = (+0.0721, −0.0361, −0.0361)`; no fallback fires.
Uniform *province* wealth with province counts 2/1/1 gives `b_w = (−0.1667, +0.0833, +0.0833)`, also
non-zero. Only one province of equal wealth per node gives `b_w ≡ 0` and fires the fallback — and there
the candidates carry wealth 2.0 each, not zero.
*Case (b) is not the family.* On a connected map it cannot arise at all (it needs a second component),
and it is not the only per-good way in: the peel fold produces firings on maps that have both a producer
and a consumer (the A/B/C/L example under X008). In the random search 75 of 114 firings were of that
kind and none were of the "no producer, no consumer" kind.
**Should say:** the reachable cases are "any graph whose **post-peel** core balance is identically zero:
the aggregate graph when every node carries the same `Σ_p wealth(p)^{α_Φ}`; a per-good component with no
producer and no consumer; and any map where Phase 0's fold cancels the core's balances exactly."

---

### X010 — In those cases the candidates are usually all *zero-wealth*, the wealth key ties, and the node index decides
**Status:** PARTIAL
**Method:** Evaluated the "zero-wealth" premise separately from the "ties → index decides" conclusion,
in each of X009's cases, on the 1444 map, and in the spec's own worked example.
**Evidence:** The conclusion holds wherever the wealth key ties — trivially. The premise does not.
(i) In the aggregate case the candidates carry **uniform positive** wealth (2.0 each in the worked
example above): the tie comes from uniformity, not from zero. (ii) In the spec's own **T3** the
candidates carry wealth **3, 2, 1** — distinct — and the wealth key decides the promotion outright, so
the spec's only worked instance of the branch does not exercise the tiebreak this claim says is
load-bearing. (iii) In the peel-fold family the candidates carry whatever the map gives: across the
random search, fallback stalls with **distinct** candidate wealths outnumbered tied ones **81 to 2**
(1 of the 2 all-zero). (iv) On the 1444 map the premise is maximally false: `NODEW` has **80 of 80
distinct values**, exactly one zero (`cape_of_good_hope`), the other 79 in [1.50, 316.60] — the wealth
key strictly orders every candidate set that could arise there. Only X009's case (b) genuinely gives
zero wealth, for a reason the spec does not state: in the reference model `c_g(n) > 0` at every owned
node for every good, so "no consumer" means "no owned province" means `NODEW = 0`.
**Should say:** "In those cases the wealth key often **ties** — at zero on an unowned component, at a
common positive value on a uniform-wealth aggregate map — and the index then decides." Drop
"zero-wealth" as the general characterisation: it is wrong for the aggregate case, for T3, and for the
whole of 1444.

---

### X011 — That is why §2.4 item 1 makes a canonical emitter node order a correctness requirement, and why §2.8 asserts containment over a set including the fallbacks
**Status:** PARTIAL
**Method:** Checked each half against the mechanism it names.
**Evidence:** Second half **confirmed**: T3's sink `A` lies in `{fallbacks}` and in neither
`{selected}` nor `{promoted}` (both empty there), so the narrow assertion would halt on correct
behaviour (X136/X149). First half: the *requirement* is right, the *reason* is not the operative one.
The node index is load-bearing wherever the priority key `(DEF, b, index)` ties, with or without a
fallback — 2,670 of 7,140 random instances changed orientation under relabelling with an identical LP
support and no fallback anywhere. In T3 itself the index decides through the priority key (B and C both
keyed `(0, 0, ·)`), not through the wealth key. And on 1444 the wealth key cannot decide anything at all
(80/80 distinct `NODEW`), while node order **does** decide the map through Phase 2's LP (finding 6:
mean 22.1 of 159 edges flip under a renumbering). So on the map the spec targets, the fallback branch is
not a rare reason for the requirement — it is not a reason for it.
**Should say:** "…because node order fixes the column order of Phase 2's degenerate min-cost flow, and
because §1.1's priority key breaks exact `(DEF, b)` ties by node index — with the fallback branch a
third place the index can decide, when the wealth key also ties."

---

### X012 — Every sink is a selected flow-terminal demand centre, a stall-promoted flow-terminal demander, a fallback-promoted highest-wealth node, or a Phase-0 pendant that absorbed a net-importing subtree
**Status:** CONFIRMED
**Method:** Proof plus exhaustive check on random graphs.
**Evidence:** Proof: a node is popped only when it is in `Sset`, has a flow out-arc, or has a free edge
to a marked node; the last two hand it an out-arc, so a core sink must have been popped as a member of
`Sset` = selected ∪ promoted ∪ fallback, and any core sink is automatically flow-terminal (a sink has no
out-arc of any kind). Phase 4 orients a peeled edge `(v,u)` as `v→u` when `β_v ≥ 0`, so a peeled node is
a sink only when `β_v < 0` — it absorbed a net-importing subtree. Brute force: 7,110 random connected
graphs, **0** sinks outside the four categories.

---

### X013 — Where Phase 0 is a no-op and no fallback fires, the sink set is exactly `{selected ∩ flow-terminal} ∪ {promoted}` — measured exact, 29/29 goods on 1444, 1–7 sinks per good, mean 3.6, zero fallbacks
**Status:** PARTIAL
**Method:** Reproduced every number, then tested the stated condition as a general conditional.
**Evidence:** Numbers reproduce exactly. `final.py` V029: "measured (sinks == {S0 cap ft} U promoted):
29/29 goods; mismatches: []". Independent recount: equality 29/29, containment 29/29, sinks/good min 1
max 7 **mean 3.5862** (→ 3.6), **fallbacks 0**; `v5measure.py` and `drainrep.py` agree.
The *condition* is not sufficient, and the spec's own **T2** is the counterexample: the five-cycle with
a chord has minimum degree 2 (`Plog` empty, Phase 0 peels nothing) and fires **no** fallback, and its
sink set is `{u2}` against a formula set `{u1, u2}`. So "where Phase 0 is a no-op and no fallback fires,
the sink set is exactly …" is false as written — two sentences later §1.1 says so itself ("that equality
is not a theorem in general") and then names T2 as one of the breakers.
**Should say:** "Where Phase 0 is a no-op and no fallback fires, the last two cases of the taxonomy are
empty, so the sink set is contained in `{selected} ∪ {promoted}`; that it is **equal** to
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
component is monotone in the marked set and in `Sset`, both of which only grow, so the marking closure
reached before each stall is order-independent and the candidate set (`unmarked ∧ cnt == 0`) is a
function of that closure. Both promotion rules read only that set. Measured: 7,110 random graphs × 8
random scan orders → **0** changes to the (promotions, fallbacks) sequence; 29 goods on 1444 × 6 random
scan orders → **0** changes.
*(Free-edge orientation is a different quantity and is not scan-invariant — 145 of 174 scan-order runs
on the non-priority sweep changed it — which is why §1.1 attributes free-edge determinism to the
priority key rather than to the closure. §1.1 states this correctly.)*

---

### X016 — Free-edge direction is deterministic by construction; that the node indexing never decides is measured, not proved, and holds exactly where the key has no exact ties
**Status:** PARTIAL
**Method:** Tested both directions of "exactly where".
**Evidence:** Sufficiency confirmed for the *priority key*: over 3,897 random instances, **0** cases of
"no exact `(DEF, b)` tie yet the orientation changed under relabelling with the same LP support" — with
one exception found in a larger sweep, which turned out not to be a priority-key effect at all but
Phase 1's undocumented `(β, index)` tiebreak (see X151). Necessity false: **714** instances had an exact
key tie and were still fully index-independent, against 2,669 that were index-dependent. So no-ties is
sufficient, not necessary, and "exactly where" claims an equivalence that does not hold.
**Should say:** "…and holds **wherever** the key has no exact ties" — a sufficient condition, not a
characterisation. (X150, the §3.2 twin of this row, already says "holds where" and is correct.)

---

### X017 — Measured: zero orientation changes under scheduler permutations, and zero exact `(DEF, b)` ties on free edges, 29/29 goods
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py`, recomputed the tie test independently over all 29 goods, measured how
close the keys come to tying, and checked what the permutation actually exercises.
**Evidence:** `v5measure.py`: "orientation flips, 2 index permutations x 29 goods 0"; "exact (DEF, b)
ties on free edges 0". Independent recount: 2,323 free-edge endpoint pairs over 29 goods, **0** exact
ties. The claim is **not** float-brittle: the smallest separation on any free edge is
`ΔDEF = 1.294e-05` (silk, `yumen`/`samarkand`) against a double-precision noise floor of ~3.4e-17 —
twelve orders of margin. Four free edges tie exactly on `DEF` and are separated by `b` (margins
4.9e-03 … 1.1e-01), so the second key component is genuinely used and is also nowhere near a tie.
*Scope note:* the permutation is of `pid` inside `sweep_priority`, so it exercises only the priority
key's tiebreak. `phase1` and the stall promotion read the true node index, and `phase2` builds its LP
columns in node order, so none of those is covered. I ran the missing test end to end (finding 6): on
1444 the sweep is index-invariant as claimed (0 of 580 same-support changes) and Phase 1 never ties
either (0 within-cluster β ties at an argmin, 0 tied cluster masses), so the claim's *conclusion* stands
on 1444 — but the measurement as run is narrower than the sentence it supports.

---

### X116 — Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: T2 and T3
**Status:** CONFIRMED
**Method:** Verified the Phase-0 independence of both cases, and proved the pair exhaustive inside the
core.
**Evidence:** T2: `Plog` empty (5-cycle + chord, min degree 2), `fallbacks = ∅`, sinks `{u2}` vs formula
`{u1, u2}`. T3: `Plog` empty (triangle), sinks `{A}` vs formula `∅`. Both inside the 2-core, both
independent of Phase 0. Exhaustiveness: inside the core a formula member can fail to be a sink only by
gaining a free out-arc to an earlier-marked node, and only a *selected* node can do that — a promoted or
fallback node is popped immediately on promotion, at a moment when it provably has no free edge to a
marked node (otherwise it would have been ready and there would have been no stall), so all its free
edges orient inward. And a core sink outside the formula must be a fallback, since core sinks ⊆ selected
∪ promoted ∪ fallbacks and a selected or promoted sink is automatically in the formula. Random search
agrees: equality-failure classes were pendant (2,385), formula-member-not-a-sink (1,942), fallback-sink
(97), **other: 0**.

---

### X117 — Free-edge determinism is proved as determinism and measured as index-independence; both halves are unaffected by peeling, which does not touch the priority key
**Status:** PARTIAL
**Method:** Checked what the priority key reads against what Phase 0 rewrites.
**Evidence:** The key is `(DEF, β, index)` and `β` is the **post-fold** balance — `phase0` returns
`beta` with each pendant's balance added to its parent, and `flow_def` is computed from that same
`beta`. So peeling changes the values the key reads and can create exact ties the input balances do not
have. Worked example: core 0–1–2–3 (edges 01, 03, 12, 13, 23) with input `b(1) = 0.5 ≠ b(2) = 1.0`, plus
a pendant on node 1 carrying `+0.5`. After the fold `β(1) = 1.0 = β(2)`, `DEF` is equal across the core,
the key ties exactly, and the free edge {1,2} is oriented by node index alone (five of the 120
relabellings flip it, LP support unchanged). Without the pendant there is no tie on that pair. The
determinism half is indeed unaffected by peeling; the *measured* half is not — it is a property of the
balances, and peeling rewrites them.
**Should say:** "…the determinism half is unaffected by peeling; the index-independence half is a
measurement on the **post-fold** balances, and Phase 0 can create exact `(DEF, β)` ties that the raw
balances do not have, so the 1444 measurement does not transfer to a peeled map."

---

### X125 — The node order itself is a correctness requirement: the priority key breaks exact ties by index, and on the fallback branch (T3) the wealth key ties and the index alone decides
**Status:** REFUTED
**Method:** Checked the cited example against the sentence that cites it, and checked the wealth key on
the 1444 map.
**Evidence:** §2.4 item 1's justification is false of T3. In T3 (as worked in §3.2 and as run in
`toys.py`) node wealth is **3, 2, 1** — the wealth key does **not** tie, and it decides the promotion
outright (A wins on wealth, not on index). What the index decides in T3 is the marking order of B
against C, through the `(DEF, b, index)` priority key, both keyed `(0, 0, ·)` — a different mechanism,
unrelated to the fallback branch. On 1444 the wealth key ties nowhere (80/80 distinct `NODEW`), so the
cited mechanism is not merely rare on the target map, it is absent. The requirement is sound — and on
1444 it is carried by a mechanism the sentence never mentions (finding 6: renumbering the nodes changes
the LP's optimal vertex and flips a mean of 22.1 of 159 edges). The fact offered as its ground is wrong.
**Should say:** see the suggested replacement under finding 6.

---

### X128 — Baseline: cloves sink at Venice, Kongo, Deccan, Australia, Brazil; under the §3.13 α-calibration spices sinks at Genoa alone and cloves moves to Deccan
**Status:** CONFIRMED
**Method:** Re-ran `drainrep.py` (baseline) and `final.py` Part B (calibration: α unclamped at exponent
2, ρ = 0.5, twig tolerance 3e-4).
**Evidence:** Baseline cloves DRAIN sinks `['deccan', 'venice', 'kongo', 'australia', 'brazil']` — the
five named. Calibration: `V107 spices sinks under calibration: ['genua']`; `V107 China nodes among
calibration spices sinks: []`; `V179 cloves alpha=16 sinks: ['deccan']`. Both halves hold; "cloves moves
to Deccan" is true in the sense that its sink set *collapses to* `{deccan}` (Deccan is already one of
its five baseline sinks, so "moves to" reads as a relocation when it is a collapse — worth a word).
*Adjacent defect in the same §2.8 row, outside this ID:* the row says spices "sink at Genoa **(demand
rank 1)**". Genoa is demand rank **2** for spices on both gross demand `c` (0.03438 against
`hangzhou`'s 0.03517) and net demand `−b`. `hangzhou` is rank 1, is the Phase-1 selection, and is not a
sink; Genoa reaches the sink set as a *stall promotion*.

---

### X129 — Sinks are 1 to 7 per good; sinks at 14.5% in the top demand decile against 6.9% in the bottom
**Status:** CONFIRMED
**Method:** Re-ran `drainrep.py`'s sink-demand correlation block and an independent sink census.
**Evidence:** `DRAIN sinks/g 3.6 | P(top10) 14.5% | P(bot10) 6.9%`; sinks/good min 1, max 7 over 29/29
goods (independent recount min 1, max 7, mean 3.5862). The barbell reproduces.

---

### X130 — Zeroing `hangzhou`-node development moves the `Φ_w` sinks to `{doab, english_channel, gulf_of_siam, sevilla}`, 22 of 159 edges flipping
**Status:** CONFIRMED
**Method:** Re-ran `audit_delta.py` for the sink set and computed the flip count independently (zero the
wealth of every province in the node, re-solve `Φ_w` at α_Φ = 1.5, count reversed edges).
**Evidence:** sinks `['doab', 'english_channel', 'gulf_of_siam', 'sevilla']`; **flips 22**, unchanged
137, total 159.

---

### X131 — `hangzhou`, not `beijing`, is China's wealth pole: `c_w` rank 1 vs 31, node wealth 245.0 vs 143.8, richest single province
**Status:** CONFIRMED
**Method:** Re-ran `audit_delta.py` and `audit_delta2.py`; recomputed node wealth and `c_w` ranks
independently.
**Evidence:** `hangzhou` `c_w` rank 1, node wealth 245.0; `beijing` `c_w` rank 31, node wealth 143.8;
richest single province pid 1821 (`hangzhou`) at 30.40 against Beijing's 19.5.

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
**Method:** Checked the model's inputs, then checked what the game's Mandate modifiers actually touch in
`common/static_modifiers/00_static_modifiers.txt`.
**Evidence:** `solver.province_table()` reads `base_tax`, `base_production`, the province's trade good,
its price and place-scoped local modifiers only — no owner field anywhere. The Mandate's modifier blocks
are `positive_mandate`, `negative_mandate` and `lost_mandate_of_heaven`; the only trade-quantity term in
any of them is `global_trade_goods_size_modifier = -0.5`, country-scoped, and that is exactly the
modifier §1.3/§3.13 classify as out-of-model. So the demand vector is provably unchanged on the day.
(The design cost is real and the spec owns it elsewhere: a −50% goods-produced hit across Ming is
deliberately invisible to the model until it reaches `base_tax`/`base_production`.)

---

### X134 — The 8.96% run-to-run drift spans the five node fields, and the three power-dependent fields inherit the randomised AI merchant placement
**Status:** CONFIRMED
**Method:** Independent — parsed `VANILLA_start.eu4` and `VANILLA2_start.eu4` directly (ZIP →
`gamestate` → `trade={ node={…} }`) with my own parser and recomputed all five fields, without reading
the v2 table for the numbers.
**Evidence:** `current` 49/77 differ, `local_value` 30/79, `outgoing` 37/66, `total` 1/79, `retention`
0/80; union of nodes differing on any field **49 of 80**. Worst relative difference **8.9593%** on
`local_value` at `siberia` (1.451 vs 1.581), reproducing 8.96% under the "relative to run 1" convention
— the same convention gives 7.20% and 7.19% on `current` and `outgoing`, matching the source's other two
figures. The three fields that move are exactly the power-dependent ones.

---

### X135 — `retention` identical on 80 of 80 nodes and `total` on 78 of 79, the exception `zambezi` drifting 0.012%
**Status:** CONFIRMED
**Method:** Same independent save parse.
**Evidence:** `retention` 0 of 80 differ; `total` 1 of 79 differ, and the one is **`zambezi`**, 147.384
vs 147.366 = **0.0122%**. All three figures exact. (v3's `validation-v3.md` phrases the same result as
"79 of 80"; the difference is only whether the one node carrying no `total` field is counted in the
denominator. X135's "78 of 79" matches the per-field table.)

---

### X136 — 2-core containment is asserted unconditionally against `{selected} ∪ {promoted} ∪ {fallbacks}`, because the narrower set would halt on T3
**Status:** CONFIRMED
**Method:** Proved the containment (X012/X147), then checked the design rationale against T3.
**Evidence:** Containment over the wide set held in 11,381 of 11,381 random instances and follows from
the readiness rule directly. On T3, `{selected} ∪ {promoted} = ∅` while the sink set is `{A}`, so the
narrow assertion halts on behaviour the spec elsewhere calls correct. The fallback set is doing
assertion work rather than escape-clause work: an escape clause would absorb *any* mismatch, whereas
`{fallbacks}` is a set the sweep maintains and can be checked against independently.

---

### X137 — Equality is monitored with T2 and T3 named as the two ways it can fail; measured exact on 1444, 29/29 goods, zero fallbacks
**Status:** CONFIRMED
**Method:** Reproduced the measurement and proved the two named failure modes exhaustive inside the
2-core.
**Evidence:** `final.py` V029 29/29 with `mismatches: []`, 0 fallbacks; independently recomputed 29/29.
Exhaustiveness: see X116 — a promoted or fallback-promoted node can never lose sinkhood, and a core sink
outside the formula must be a fallback, so the only failures are T2 and T3. Random search found no third
mode across 3,075 equality failures.

---

### X138 — Goal 1's worked example is a horde razing `hangzhou`, not Beijing
**Status:** CONFIRMED
**Method:** Read §3.1 Goal 1; checked the fact it rests on.
**Evidence:** §3.1 reads "A horde razing `hangzhou` moves the sink because the wealth moved." The
underlying fact holds (X130/X131).
*Minor:* the example is stated at node granularity while EU4's raze acts on one province, and the
measurement zeroes an entire node's wealth — directionally right, larger than one raze action.

---

### X139 — Supply is sparse where demand is dense: spices produced in 18 of 80 nodes and cloves in one, while every node with an owned province carries demand
**Status:** CONFIRMED
**Method:** Recounted from `build_sc` with no regularizer.
**Evidence:** spices produced in **18 of 80** nodes, cloves in **1 of 80**; both demanded in **79 of
80**. The single non-demanding node is `cape_of_good_hope`, also the only node with zero node wealth —
so "every node with an owned province carries demand" is exact rather than approximate.

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
sink rule compares against — the neighbour-`φ` spread — tracks supply geography rather than demand.
**Evidence:** (a) supply 4–97 against demand 211–20,400 across the 29 goods (X140). (b) producers 18/80
and 1/80 against demanders 79/80 (X139). (c) computing the v1 potential per good and correlating the
per-node neighbour spread `mean(φ_nbr) − min(φ_nbr)`: correlation with "has a producing neighbour" is
**0.787** for cloves and **0.357** for spices, against **0.128** and **0.172** for mean neighbour demand.
*Flagged for the author, not scored here (it belongs to the UNCHANGED §3.2 sentence, not to X141):* the
neighbouring claim "deleting demand variation entirely left the sink unmoved" did **not** reproduce in my
reconstruction — replacing `c` with a uniform `1/N` moved the LAP spices sink set from `{saxony}` to six
nodes and the cloves set from `{deccan, kongo, safi, wien}` to `{kongo, krakow, safi, white_sea}`. My
reconstruction of v1's ε machinery may differ from the original experiment; worth re-deriving before
that sentence is relied on again.

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
`xian` ×4.594 / 12.3%, `canton` ×4.855 / 17.8%. Both ranges are right individually. But the map from
multiplier to share is **not monotone** and the two ranges' endpoints belong to different nodes: the
×-maximum is `canton` at 4.86×, whose share is 17.8%, while the %-maximum is `hangzhou` at 21.4%, whose
multiplier is 3.83×. "i.e." asserts a restatement, so the sentence licenses the false inference
"4.9× ⇒ 21.4%".
**Should say:** "…needs **3.6–4.9×**, which across these four nodes corresponds to **9.3–21.4%** of all
world spice demand at one node — the two ranges are not aligned end to end, because the share a
multiplier buys depends on the node's starting demand."

---

### X144 — `girin`, `yumen`, `chengdu`, `lhasa` need 4.0× to 10.8×
**Status:** CONFIRMED
**Method:** Re-ran `v5measure.py` section F.
**Evidence:** girin ×3.972, yumen ×4.516, chengdu ×8.202, lhasa ×10.751 → 4.0× to 10.8× after rounding.

---

### X145 — Sink placement holds where Phase 0 is a no-op and no fallback fires; three constructed inputs break it, all run through a faithful implementation of §1.1
**Status:** PARTIAL
**Method:** Ran `toys.py`, re-ran T1/T2/T3 through an independent implementation written from the spec
text, then tested the antecedent.
**Evidence:** The second half is confirmed twice over: `toys.py` and the independent implementation
produce identical output on all three cases (T1 sinks `{C}` vs formula `{B}`, restored edge B→C; T2
`{u2}` vs `{u1,u2}`, free edge oriented u1→w; T3 `{A}` vs `∅`, with B→A, C→A, C→B). The first half fails
for the same reason as X013: **T2 itself satisfies "Phase 0 is a no-op and no fallback fires"** —
`Plog` empty, `fallbacks` empty — and breaks the equality. Two of the three named breakers sit inside
the antecedent's own scope; only T1 needs Phase 0.
**Should say:** "Sink placement is *measured* exact on 1444, where Phase 0 is a no-op and no fallback
fires; those two conditions are necessary, not sufficient — T2 satisfies both and still breaks the
equality. Three constructed inputs break it…"

---

### X146 — T3 worked: triangle with `b = 0` and wealth 3, 2, 1; fallback promotes A; free edges orient B→A, C→A, C→B; sinks `{A}`, formula empty
**Status:** CONFIRMED
**Method:** `toys.py` plus the independent implementation.
**Evidence:** Both give `S0 = ∅`, every edge free (zero flow), a stall with no flow-terminal demander,
`fallbacks = {A}`, directed edges `{B→A, C→A, C→B}`, actual sinks `{A}`, formula set `∅`, A in neither
`{selected}` nor `{promoted}` — every element reproduces.
*Cross-reference:* T3's wealths are **distinct**, which is what refutes X125 and X151 and weakens X010.
Within T3 the index does still decide one edge (C→B), through the priority key `(0, 0, index)`, not
through the wealth key.

---

### X147 — What survives unconditionally is the ⊆-direction within the 2-core over `{selected} ∪ {promoted} ∪ {fallbacks}`; pendant net-importers are the only sinks outside that set
**Status:** CONFIRMED
**Method:** Proof plus brute force.
**Evidence:** Proof: a node is popped only if it is in `Sset`, has a flow out-arc, or has a free edge to
an already-marked node; the second gives it a flow out-arc and the third orients that free edge outward
(later-marked → earlier-marked), so any core node with no out-arc was popped as a member of `Sset`.
Outside the core, Phase 4 makes a peeled node a sink iff its folded balance is negative. Brute force:
**0** containment violations in 11,381 random instances; **0** sinks outside the four-way taxonomy in
7,110 instances.

---

### X148 — Sink placement is checked at runtime as two checks: containment asserted unconditionally, equality monitored with T2 and T3 named as its legitimate failures
**Status:** CONFIRMED
**Method:** Read §2.8's "Sink set, 2-core" row and §2.9's assertion list against the claim.
**Evidence:** §2.8 states both checks with the split exactly as claimed ("halt only on a containment
miss"; "Report an equality miss with the node and the good"), and §2.9's solver-track list carries
"2-core sink containment in `{selected} ∪ {promoted} ∪ {fallbacks}`" plus "the per-tick sink-set equality
monitor". Both named failures are legitimate and reachable inside the 2-core, so monitoring rather than
asserting is the correct disposition for the equality.

---

### X149 — Written against the narrower containment set, T3 would halt the solver on correct behaviour
**Status:** CONFIRMED
**Method:** Evaluated the narrow assertion on T3's output.
**Evidence:** On T3, `{selected} ∪ {promoted} = ∅` and the sink set is `{A}`, so
`sinks ⊆ {selected} ∪ {promoted}` is **False** while `sinks ⊆ {selected} ∪ {promoted} ∪ {fallbacks}` is
**True** — printed directly by `toys.py` and reproduced independently.

---

### X150 — Free-edge direction is deterministic by construction; that the node indexing never decides is measured, not proved, and holds where the key has no exact ties — zero exact `(DEF, b)` ties, 29/29
**Status:** CONFIRMED
**Method:** Reproduced the measurement and tested the sufficiency direction on random graphs.
**Evidence:** 0 exact ties over 2,323 free-edge endpoint pairs on 1444 (independent recount), and no
instance of "no exact tie yet the priority key's index decided". Unlike X016 this row says "holds
**where**", which is the correct sufficient-condition form. (The one no-tie index-dependent instance I
found is a Phase-1 effect, not a free-edge effect — see X151 — so it does not bear on this row.)

---

### X151 — The one place the indexing is load-bearing is the fallback branch (T3), where the candidates are typically all zero-wealth and tied
**Status:** REFUTED
**Method:** Searched for index-decided orientations with no fallback, holding the LP support fixed so
the LP could not be the cause; then isolated every such instance that had **no** exact `(DEF, b)` tie,
to see whether the documented tiebreak explains all of them; then checked T3's wealths and 1444.
**Evidence:** Both halves of the claim fail, and the mechanism is broader than either the spec or my
first pass recorded.
(i) *"The one place"* — **2,670 of 7,140** random instances changed orientation under a node relabelling
with an **identical flow support and no fallback anywhere**. Minimal example: nodes 0..3, edges
{01, 03, 12, 13, 23}, `b = (−2, 1, 1, 0)`; nodes 1 and 2 key exactly `(DEF 2.0, b 1.0)`, so the free edge
{1,2} is oriented by index alone — five of the 24 relabellings flip it, support unchanged,
`fallbacks = ∅`.
(ii) *The tiebreak inventory is incomplete.* Of those 2,670, **2,669 sit on an exact `(DEF, b)` tie and
one does not**. The exception is a second, undocumented index tiebreak — Phase 1's
`S.add(min(comps[j], key=lambda v: (beta[v], v)))`: when two demanders inside one cluster have exactly
equal `β`, the heaviest-demander choice is made by node index. Isolated instance: n = 6, edges
{01,02,03,04,13,14,15,23,35}, `b = (−1, 0, −1, +1, +3, −2)`; clusters {0,2} and {5} both of mass 2,
HHI = 0.5, k = 2, and inside {0,2} `β(0) = β(2) = −1` exactly, so the index picks 0 in the base run and 2
under the permutation, flipping three edges with no `(DEF, b)` tie anywhere. The same `(β, index)` form
recurs in the stall promotion (`min(terminals, key=(β, v))`), and the top-k cluster cut breaks equal
cluster masses by enumeration order, which follows node order. §1.1 documents two index tiebreaks; there
are four.
(iii) *T3* — its candidates carry wealth **3, 2, 1**; the wealth key decides the promotion and does not
tie. On 1444 it cannot tie either: `NODEW` is 80-of-80 distinct.
(iv) *On 1444 none of the tiebreaks bite:* 0 exact `(DEF, b)` ties on free edges, 0 within-cluster β ties
at a Phase-1 argmin, 0 tied cluster masses at the top-k cut, across all 29 goods and `Φ_w`. The claim is
about the general case; 1444 itself is untouched by it — and node order still decides the 1444 map, by
the different route in finding 6.
**Should say:** see the suggested replacement under finding 6.

---

### X184 — The survival table is about 1.5 MB at double precision — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes — and the solver's residuals sit at 1e-16, one ULP of a double
**Status:** CONFIRMED
**Method:** Checked the arithmetic, the multiplier against §1.5 and §2.2, and the residual against
§3.10's measured figure.
**Evidence:** 29 × 80 × 80 × 8 = **1,484,800** exactly = 1.4848 MB decimal (1.416 MiB), so "about
1.5 MB" is fair, and half of it (single precision) is the 0.75 MB the claim attributes to v1/v2. The
multiplier 29 is the **live** goods count at 1444 (`GOODS` holds 30 including latent `coal`; `LIVE`
counts 29), and §1.5 explicitly gives a latent good "no survival-table entry", so 29 is the internally
consistent number here — §2.2 item 7's "30 goods × 80 BFS" is the row that disagrees with §1.5. At 30
goods the figure would be 1,536,000 bytes, still "about 1.5 MB".
*Slack, not error:* §3.10's measured worst relative disagreement is **0 to 3.7e-16**, not 1e-16; 3.7e-16
is ~1.7 ULP for values in [1,2) and more for smaller ones, so "1e-16, one ULP" rounds the measurement
down by roughly a factor of three. The conclusion (double, not single, precision) is unaffected.

---

## Systemic findings

1. **The fallback branch's reachability analysis (X008–X011) is written against the post-peel balance
   while §1.1 defines `b` as the input balance, and its case list misses the family the peel produces.**
   A triangle with a pendant, `b = (+1, 0, 0 | −1)`, fires the fallback on a connected core with a
   producer and a consumer; 75 of 114 firings in a random search are of that kind.
2. **"The fallback branch is where the index decides" is wrong three times over** (X010, X011, X125,
   X151, §2.4 item 1): the spec's own T3 uses distinct wealths 3/2/1; 1444's `NODEW` is 80-of-80 distinct
   so the wealth key can never tie there; and the index is load-bearing wherever the `(DEF, b)` key ties,
   with no fallback involved.
3. **"Phase 0 no-op ∧ no fallback ⇒ sink-set equality" is asserted twice (X013, X145) and refuted by the
   spec's own T2**, which satisfies both conditions and breaks the equality. §2.2a's table gets this
   right ("measured exact 29/29" rather than "holds"); §1.1's bullet and §3.2's item 1 do not.
4. **§1.1 documents two index tiebreaks; the implementation has four.** Beyond the priority key and the
   fallback's wealth key there are Phase 1's within-cluster `min(β, index)` heaviest-demander choice, the
   identical form in the stall promotion, and the top-k cluster cut's dependence on cluster enumeration
   order. Each is a place the node indexing can decide the map. None ties on 1444 (measured: 0, 0, 0).
5. **Everything that was measured, reproduced.** All the numerical figures in scope came back exact:
   29/29 equality and containment, 1–7 sinks, mean 3.5862, 0 fallbacks, 0 `(DEF, b)` ties, 14.5%/6.9%,
   22 and 17 flips, 245.0/143.8, ranks 1/31, 1.346%, ×1.720, the four China thresholds and the four
   outside them, 18/80 and 1/80 producers, 36 vs 482.2, 1,484,800 bytes — and the two ⚑ ENGINE rows
   (X134, X135) reproduced independently from the save files rather than from the v2 write-up. The "zero
   exact ties" measurement is also not float-brittle: smallest separation 1.3e-05 against a 3.4e-17 noise
   floor.
6. **The largest finding, and it is not a tiebreak at all: on 1444 the node order decides the map through
   Phase 2's LP.** `v5measure.py`'s permutation re-keys only `sweep_priority` (`pid`), so it never
   exercised `phase1`, the stall promotion, or the LP's column order. Permuting the node indexing end to
   end through every phase, 29 goods × 20 relabellings = 580 runs:

   | | |
   |---|---|
   | orientation changed | **580 of 580** |
   | …with the SAME LP support | **0** — the sweep is index-invariant on 1444, confirming X017 |
   | …with a DIFFERENT LP support | **580** — HiGHS returned a different optimal vertex |

   Magnitude: **mean 22.1 of 159 edges flip** per relabelling (max 45), the sink set moves by up to 8
   nodes, and the LP objective is identical to 8.9e-16 — all optimal, genuine degeneracy. `Φ_w` behaves
   the same, 20 of 20. So §2.4 item 1's conclusion ("the same world can produce two different maps") is
   **true on 1444** and is carried by the LP, not by any tiebreak — a mean of 22 flips is the same
   magnitude as the razed-China perturbation §2.8 treats as a major world event. This also reframes
   §3.13's "LP determinism across machines" open question: it is a same-machine, same-input concern the
   moment the emitter's node order changes.
   **Suggested replacement for §2.4 item 1's justification:** *"The node order itself is a correctness
   requirement, not a convention. It fixes the column order of Phase 2's min-cost flow, whose optimum is
   degenerate — renumbering the nodes on the 1444 data returns a different optimal vertex and flips a
   mean of 22 of 159 edges at identical cost — and it breaks the exact ties in §1.1's priority key, in
   Phase 1's heaviest-demander choice, and in the fallback's wealth key. The emitter must therefore fix
   one canonical node order and keep it stable across rebuilds, or the same world can produce two
   different maps."* Caveat to keep with it: the 580/580 result is HiGHS-specific in detail though not in
   kind — any simplex picks some vertex, and which one depends on column order.
7. **Two prose defects in §2.8/§3.2 outside this ID range but inside these sections:** §2.8's spices row
   calls Genoa "demand rank 1" when it is rank 2 (`hangzhou` is rank 1, is the Phase-1 selection, and is
   not a sink); and §3.2's "deleting demand variation entirely left the sink unmoved" did not reproduce
   in my reconstruction of the v1 operator.
