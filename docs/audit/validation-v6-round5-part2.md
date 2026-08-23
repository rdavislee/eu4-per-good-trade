# Validation — v6.1 spec, round 5, part 2 (§1.6 – §1.12)

**Target document:** `per-good-trade-spec.md`, MD5 `59c84a97799db9db97fe889b6e3c6776`
(computed before the audit and again after it — **unchanged**; the document did not move under me).

**Inventory under test:** `claims-v6.md` (MD5 `b95f98345e1679f49a03581fac8778f7`), the rows in §1.6,
§1.7, §1.8, §1.9, §1.10, §1.11, §1.12 — **162 claim IDs**. Rows marked `(v5)` / `REMOVED` are out of
scope and are not verdicted.

---

## Instruments

Every confirmation below comes from a source outside the document. Five kinds of source were used.

**(a) Shipped scripts, re-run.** `scripts/measure6.py` was re-run from scratch; its 60 labelled
figures came back **byte-identical** to the `measure6.out` already in the tree (`diff
measure6.out.round5part2 measure6.out` → identical). I read the script before trusting it and
confirmed it computes what its labels say: `cv(a,w)` builds `Σ_p w_p^α / Σ_q w_q^α` (its
`(w/w.max())**a` normaliser cancels in the ratio, so it is the spec's `c_w` exactly), `ph()` calls
`run_drain(1/N − c_w)` = `DRAIN(b_w)`, and "sinks" are the out-degree-0 nodes of the returned
orientation. `scripts/relabel6.py 60 4242 7 999` was re-run and reproduces 180 relabellings; it does
validate its reimplementation against `drain.py` on the identity permutation before counting a trial,
as the document says (`edges agreeing with drain.py: 159 of 159`).

**(b) Shipped scripts that do not do what they are cited for.** Two failures, both material:

- `scripts/epsilon6.py` — cited at L570 for the `TIE_EPS` bands — **crashes**. It monkey-patches
  `drain.mincost_flow` with a two-argument `mcf(s, c)`, but `drain.phase2` calls
  `mincost_flow(b, np.zeros(N), cost=TIE_COST)`. Actual output: `TypeError:
  solve.<locals>.mcf() got an unexpected keyword argument 'cost'`, at the first non-zero grid point.
  Its `eps = 0` validation branch passes only because it restores `flowop.mincost_flow`, which
  applies `TIE_COST` — so that check compares the shipped map to itself.
- `scripts/europe.py` — cited at L586 for the European-development table — computes a **different
  experiment**: `sinks(w, a=1.5)` (α_Φ = 1.5, not 2.0), a loop `for k in range(0, 61)` (×1.00 to
  ×1.60, not ×2.50), a fixed 0.01 grid, and **no bisection** anywhere in the file.

**(c) Instruments I wrote, each validated before use.** All are built on the same v5 five-phase
reimplementation `relabel6.py` uses (`../v5-owner-agnostic/scripts/_audit_b_drain.py`), with only the
Phase-2 objective and the LP tolerance as variables, or else drive the shipped `drain.py` with only a
named constant replaced:

- `/tmp/aud_pergood.py` — per-good relabelling under four Phase-2 configurations. **Validated: config
  D (the shipped objective, tolerance pinned at 1e-10) reproduces `drain.py` exactly on the identity
  permutation for 29 of 29 goods** before any trial is counted.
- `/tmp/aud_altopt.py` — alternative optima of the per-good Phase-2 LP, by reduced cost of zero-flow
  arcs. Validated by reproducing `flowop.py`'s own documented figure (40 zero-reduced-cost arcs on
  the aggregate under unit cost → 0 under the first-order term).
- `/tmp/aud_scale_eps.py`, `/tmp/aud_scale2.py`, `/tmp/aud_scale3.py` — the b-scaling sweep and the
  `TIE_EPS`/`TIE_EPS2` sweeps, driving the **shipped** `drain.py` with only `drain.TIE_COST` and the
  LP options replaced. Validated: the baseline reproduces `{genua, hangzhou}` / 159 edges / 1
  promotion / 0 fallbacks.
- `/tmp/aud_europe.py`, `/tmp/aud_europe2.py` — the European-development table at α_Φ = 2.0 with
  bisection, plus an order-invariance test at every interval. Validated against `measure6.out`'s
  three published spot values (×1.02, ×1.56, ×2.00), all three of which it reproduces.
- `/tmp/aud_geo.py`, `/tmp/aud_cape.py`, `/tmp/aud_cape2.py`, `/tmp/aud_eunodes.py`,
  `/tmp/aud_nodes.py`, `/tmp/aud_misc.py`, `/tmp/aud_batch.py` — routes, the Cape, European node
  sets, node scaling, and the remaining per-node measurements, all on the shipped orientation.
- `/tmp/aud_save.py`, `/tmp/aud_prop.py`, `/tmp/aud_prop2.py`, `/tmp/aud_prop3.py`,
  `/tmp/aud_steer.py`, `/tmp/aud_steer2.py`, `/tmp/aud_steer3.py`, `/tmp/aud_split.py`,
  `/tmp/aud_gate.py` — save parsers. Validated where possible against `measure6.out`'s own
  save-derived figures and against the shipped topology (the `incoming` blocks' `from` index
  resolves to a real upstream node for 159 of 159 links).

**(d) The install.** `C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` —
`common/defines.lua`, `common/trading_policies/00_trading_policies.txt`,
`common/institutions/00_Core.txt`, `common/trade_companies/`, `common/subject_type_upgrades/`,
`interface/tradeinterface.gui`, `localisation/*_l_english.yml`, and a comment-stripped 2,624-file
sweep of `common/`, `missions/`, `decisions/`, `events/`.

**(e) Saves.** `VANILLA_start.eu4` (1444.11.11) and `Castile1444_12_22.eu4` (later in 1444), read as
ZIP → `gamestate`, with province and trade records parsed at their own brace depth.

**One structural fact used throughout:** the mod has **no build**. `mod/` holds only four probe mods
(`pgt_cycle`, `pgt_flip`, `pgt_flip_ordered`, `pgt_permute`), each of which rewrites only
`common/tradenodes`. There is no per-good-trade DLL, descriptor or emitter. Every claim that
describes the mod's own runtime behaviour is therefore `UNTESTABLE` — nothing exists to observe — and
is marked so rather than waved through as "design".

---

## §1.6 — The aggregate graph

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y323 | CONFIRMED | Re-derived `V_g` from `solver.py:build_sc` and asserted `V[g] == PRICES[g]*world[g]` for every good, in `/tmp/aud_misc.py`. | `V[g] == price(g) * Σ_m goods_produced(m,g) for every good: True`. Top three by `V`: grain 514.0, cloth 429.6, livestock 276.8. The "used for display, link values and AI" half is a design stipulation about an unbuilt emitter and is not settleable. |
| Y324 | CONFIRMED | Read `measure6.py:ph()` and `relabel6.py`; both build `b` as `np.full(N, 1.0/N) − c_w`. | `s_w(n) = 1/N` is what the implementation uses, with N = 80. |
| Y325 | CONFIRMED | Read `measure6.py:cv()`: `(w/w.max())**a` accumulated per node then divided by its own sum equals `Σ_p w_p^α / Σ_q w_q^α`, the max-normaliser cancelling. | Algebraically identical to L469. Reproduced independently in my own instruments, which match `measure6.out` (`largest |b_w| 0.0347`). |
| Y326 | CONFIRMED | Grepped the constant in every instrument: `measure6.py:A_PHI = 2.0`, `relabel6.py: t = (W/W.max())**2.0`, `epsilon6.py: ALPHA = 2.0` default. | α_Φ = 2.0 throughout. My own scripts recompute `b_w` at 2.0 and reproduce every published figure. |
| Y327 | CONFIRMED | Read `measure6.py:ph()` → `run_drain(...)`, and `drain.py:run_drain` → phase0 / phase1 / phase2 / sweep_priority / compile_dirs, the §1.1 five-phase operator. | `Φ_w` is literally `DRAIN` applied to `b_w`; there is no separate code path for it. |
| Y328 | UNTESTABLE | Searched `mod/` for a build. | Only four probe mods exist, each rewriting `common/tradenodes` alone. Nothing installs `Φ_w`. Settling this needs a built mod whose emitted `00_tradenodes.txt` matches the reference orientation. |
| Y329 | PARTIAL | `/tmp/aud_misc.py`: over the 159 oriented edges, counted how many point toward the higher `c_w` and the higher node wealth; and checked whether every net demander has above-average `c_w`. | The premise holds exactly: **every net demander has `c_w > 1/N`**, 36 demanders / 44 suppliers. The intermediate gloss does not: only **97 of 159** edges point toward the higher `c_w` (95 of 159 toward the higher node wealth) — **62 edges point the other way**. "Arrows point from wealthy nodes toward the wealthiest" is false for 39% of the map. The final clause ("the sinks are wherever the wealth flow terminates") is definitional. |
| Y078 | CONFIRMED | Combined the α_Φ grid from the `measure6.py` rerun with my European-development sweep. | Count and location both move: over α_Φ ∈ [1,8] the sink count runs 3→1→2→2→1→1; over European development the sink set takes at least 13 distinct values, from `{genua,hangzhou}` to `{genua,rheinland}`. |
| Y079 | CONFIRMED | `measure6.out` for α_Φ = 2.0 on the 1444 field; `/tmp/aud_europe.py` for the grown-Europe sets. | 1444 gives 2 sinks. A modestly grown Europe gives 2, 3, 4 and 5 — the document's "two, three or five" is a subset of what actually occurs (my scan also finds 4-sink rows at ×1.14–×1.16 and ×1.95–×1.97). Neither count nor placement is fixed by the constant. |
| Y080 | CONFIRMED | Grepped the prior spec files directly. | v2.0 L154-155, v3.0 L257, v4.0 L306 all read "Nothing pins their count; it emerges from concentration exactly as per-good sink counts do". v5.0 L342: "Their count is set by `α_Φ`". v2 L372: "the aggregate-graph exponent `α_Φ = 1.5` (calibrated so the 1444 start yields the two-sink …" — a target count in view, confirmed. (Note: there is no separate v2.1 file; the calibration sentence is in `v2-drain/per-good-trade-spec.md`.) |
| Y330 | UNTESTABLE | — | A statement about what §3.1's goal asks for: a design intention, not a measurable. |
| Y331 | CONFIRMED | Read each phase in `drain.py` against the claim, then tested empirically by scaling `b_w` **up**. | Phase 1's `q = M/D` and `HHI` are pure mass shares (scale-free); `k = round(1/HHI)` and the `min(..., key=(beta[v],v))` argmin are unchanged under positive scaling; the LP `b_eq` scales linearly against a fixed cost vector so `x` scales and net signs are identical; `sweep_priority`'s key `(DEF, beta, index)` is order-isomorphic under positive scaling since `DEF` is a non-negative linear functional of `beta`. Empirically: ×10, ×28.8, ×100 and ×10⁴ all give **0 edge flips**. One small mis-attribution: `drain.phase0` does not read signs — it peels by degree; the sign of `beta` is read in `compile_dirs` (Phase 4). |
| Y332 | REFUTED | `/tmp/q2_mech.py` and `/tmp/q2c.py`: set `ZERO_TOL` to 1e-14, 1e-17, 1e-20 and **exactly 0** at every scale, and separated the LP's primal and dual feasibility tolerances. | The premise is true — `flowop.py:ZERO_TOL` is an absolute 1e-11. **The causal claim is false.** At ×10⁻⁷ (22 flips, free 80) and at ×10⁻⁹ (96 flips, free 159), setting `ZERO_TOL` to **0** changes nothing: same flip count, same free-set size, same sink set. Nothing is being pushed into the free set by the tolerance. What happens at ×10⁻⁹ is that `|b_w|max = 3.5e-11` falls below the **primal** feasibility tolerance of 1e-10, so the all-zero flow is already primal-feasible and HiGHS returns it — every edge then has net **exactly** zero and is free at any tolerance, including zero. Confirmed by separation: at ×10⁻⁷, loosening the primal tolerance to 1e-7 collapses the run to 96 flips / free 159, while loosening the *dual* tolerance to 1e-7 changes nothing (22 flips, free 80). See the addendum for the rewritten mechanism. |
| Y081 | PARTIAL | `/tmp/aud_scale2.py` and `/tmp/aud_scale3.py`: scaled `b_w` under five solver configurations, counting edge flips and sink sets against the baseline. | Under the **shipped** configuration (`TIE_COST`, `LP_OPTS` pinned to 1e-10): 0 flips and `{genua,hangzhou}` from ×1 down to **×10⁻⁶**; **22 flips and `{english_channel, hangzhou}` at ×10⁻⁷**; 24 flips at ×10⁻⁸; **96 flips and `{hangzhou}` at ×10⁻⁹**. The counts and sink sets are exactly the document's, but at scales **three orders of magnitude lower** than it states. The document's ×10⁻⁴ / ×10⁻⁶ figures reproduce only under scipy's *default* LP tolerance (1e-7) — i.e. they are pre-tolerance-pinning measurements, and §1.6 itself (L533) records that pinning as a later change. "Identical orientation from ×1 down to ×10⁻²" also understates by four orders. |
| Y333 | REFUTED | Same runs as Y081, reading the sink set at every scale under both configurations. | Under the shipped solver the first scale at which anything degrades is ×10⁻⁷, and **the sink set degrades there too** (`{english_channel, hangzhou}`, 22 flips). Under the default-tolerance configuration the document's own numbers show the same coincidence at ×10⁻⁴. The orientation does not degrade *before* the sink set. The trailing conclusion is nevertheless supported by ×10⁻⁸, where the sink set is back at `{genua, hangzhou}` while 24 edges are wrong — so the sink set is indeed not the quantity to watch; the reason given for it is false. |
| Y082 | CONFIRMED | `measure6.py` rerun, and independently `/tmp/aud_scale_eps.py`. | `largest \|b_w\| = 0.034664`, which rounds to 0.0347. |
| Y334 | CONFIRMED | `/tmp/aud_scale_eps.py`: scaled `b_w` up by ×10, ×28.8 (= 1/0.0347, the (−1,1) normaliser), ×100 and ×10⁴ under the shipped configuration. | 0 edge flips at every upward scale; sink set `{genua, hangzhou}` throughout. Downward scaling breaks (Y081). "Either scale up, or scale the tolerance with it" is sound on this evidence. |
| Y083 | CONFIRMED | `measure6.py` rerun (output byte-identical to the tree's), and the same sink set re-derived from my own instrument. | `Phi_w sinks ['genua','hangzhou']`; `genua c_w / node-wealth rank (2, 4)`; `hangzhou c_w / node-wealth rank (1, 12)`. The script computes ranks by `argsort(-c_w)` and `argsort(-node_wealth)`, which is what the labels claim. |
| Y084 | PARTIAL | `relabel6.py` (180 relabellings) plus `/tmp/aud_batch.py` (40 more, also checking promotions, fallbacks and Phase-1 selection). Searched `mod/per-good-trade/` for a v6.0 snapshot. | The substantive half is CONFIRMED: 0 of 159 edges moved in 220 relabellings, sink set `{genua, hangzhou}` in 180 of 180. The "change from v6.0, whose argument turned on the opposite" half is **untestable**: the tree holds v1–v5 plus the current v6.1, and there is no v6.0 file to compare against. Settling it needs the v6.0 snapshot. |
| Y335 | CONFIRMED | `relabel6.py`'s `lp_objective(perm, tie=False)` — Phase 2's LP solved directly under 40 permutations with unit arc costs. | `unit cost (former): objective 0.789420000928, max rel deviation 5.626e-16; permutations returning a DIFFERENT optimal support: 40 of 40`. Degenerate exactly as described. |
| Y085 | CONFIRMED | Same run. | **40 of 40** different optimal supports, objective identical to 5.626e-16 relative — "a few units in the last place" for a double. |
| Y087 | PARTIAL | As Y085, plus the search for a v6.0 file. | "The old sink set was partly an artifact of the node order" is CONFIRMED (40 of 40 supports differ under the old objective). "and v6.0 said so" is untestable — no v6.0 file exists in the tree. |
| Y986 | CONFIRMED | Read `flowop.py:TIE_COST`. | `TIE_COST = 1.0 + TIE_EPS*(w[u]+w[v])/2 + TIE_EPS2*frac(min(w)·max(w)·7919)`, with `w` the min-max-normalised **node wealth**. Both terms are symmetric in `(u,v)` (`+` and `min`/`max` are), and both read node wealth only — no good, no direction. |
| Y987 | CONFIRMED | `relabel6.py`'s `lp_objective(perm, tie=True)`, 40 permutations. | `tie-break cost: permutations returning a DIFFERENT optimal support: 0 of 40`; objective 0.789746281866, max rel deviation 7.029e-16. |
| Y086 | CONFIRMED | `python relabel6.py 60 4242 7 999`. | `instrument validation on the identity permutation: edges agreeing with drain.py 159 of 159; sink set matches True`. Then `pooled over 180 relabellings — orientation changed: 0 of 180; edges moving: mean 0.00, range 0-0; baseline sink set returned: 180 (100.0%); sink-count distribution {2: 180}; most frequent end holders [('genua', 180), ('hangzhou', 180)]`. Every figure the claim states, including the instrument-validation gate. |
| Y988 | CONFIRMED | `/tmp/aud_pergood.py`: built the same reimplementation with a **unit-cost** Phase 2 and diffed its identity-permutation orientation against `drain.py`'s. | `AGGREGATE: unit-cost reimplementation vs shipped drain.py on identity: 26 of 159 edges differ` — exactly the document's figure. With the first-order term restored: 0 of 159. And `relabel6.py` does abort on this: its `if not ok: sys.exit("INSTRUMENT FAILED VALIDATION …")` runs before any trial. |
| Y989 | CONFIRMED | `/tmp/aud_batch.py`: solved Phase 2's LP with `c(u,v) = 1 − ε(w[v] − w[u])` at ε ∈ {1e-3, 1e-1, 1}, decomposed the objective, and compared total flow against the unit-cost optimum. | At every ε the ε-part of the objective equals the predicted constant to full precision (ε=1e-3: −1.980e-04 measured, −1.980e-04 predicted; ε=1: −1.980e-01 both), and the total flow under the directional cost equals the unit-cost optimum exactly (0.7894200009 both, `equal: True`). The directional term adds a constant and cannot select among unit-cost optima. |
| Y091 | CONFIRMED | `relabel6.py` (180) plus `/tmp/aud_batch.py` (40, comparing edges, promotions, fallbacks and Phase-1 selection). | 0 of 159 edges moved in any of 220 relabellings; `40 of 40 relabellings gave identical edges, promotions, fallbacks and Phase-1 selection`. |
| Y093 | CONFIRMED | `/tmp/aud_batch.py`, using the reimplementation's `promos`/`fbs`/`S` outputs mapped back through the inverse permutation. | Identity: promotions `['genua']`, fallbacks `[]`, Phase-1 `S = ['hangzhou']`. Then **40 of 40** relabellings returned identical edges, promotions, fallbacks and Phase-1 selection. |
| Y990 | CONFIRMED | `/tmp/aud_altopt.py`: counted goods whose per-good Phase-2 LP admits an alternative optimum (a zero-flow arc with zero reduced cost) under the first-order term alone. | Aggregate `b_w`: 40 zero-reduced-cost arcs under unit cost → **0** under the first-order term. Per good: **18 of 29** still admit an alternative optimum under the same term (1–5 arcs each: chinaware 1, cloth 2, cocoa 2, copper 5, cotton 2, fish 1, gems 2, glass 4, …). A wealth-weighted cost does separate the aggregate optimum and does not separate the per-good ones. |
| Y991 | CONFIRMED | `/tmp/aud_pergood.py`, config B (first-order term only, default LP tolerance), 29 goods × 10 relabellings = 290 runs, repeated over five seeds. | Runs moving an edge: **89, 95, 91, 86, 81** across seeds 20260821, 4242, 7, 999, 1 (goods affected 14 of 29 in every case). The document's **84** sits inside that spread; the seed is not recorded, so the figure is a legitimate draw rather than an exactly reproducible one. Config A (unit cost) gives 290 of 290 for reference. |
| Y1007 | CONFIRMED | `/tmp/aud_pergood.py` config C for the run count; `/tmp/aud_altopt.py` for the alternative-optimum count. | Runs moving an edge with the second-order term added: **12, 12, 12, 14, 12** across the five seeds — the document's **13** is inside the spread. Goods admitting an alternative optimum: **18 of 29 → 1** (`paper`), reproduced **exactly** at both reduced-cost tolerances tried (1e-12 and 1e-9). |
| Y1008 | CONFIRMED | `/tmp/aud_pergood.py` config D (shipped objective, `LP_OPTS` dual/primal feasibility 1e-10), same 290-run design. | **0 of 290** on every one of the five seeds; goods affected 0 of 29; 0 failures. Exact. |
| Y1009 | CONFIRMED | Same run. | Per-good orientations are invariant across all 50 permutations × 29 goods tried, as `Φ_w` is across 220. The document's own hedge ("over the orderings tried") is the right one: this is measured, not proved. |
| Y336 | UNTESTABLE | Searched for an emitter. | No emitter exists to fix an order in. The reasoning it offers (both guarantees measured, not proved) is independently CONFIRMED — see Y1009. |
| Y993 | CONFIRMED | `/tmp/aud_misc.py`: verified `V[g] == price(g)·Σ_m goods_produced(m,g)`, a sum with no arc and no direction in it. | `True` for all 30 goods. `V_g` is a function of a node-indexed sum only; relabelling permutes the summands, not the sum. |
| Y094 | CONFIRMED | `measure6.py` rerun, and independently `/tmp/aud_batch.py`'s reimplementation. | `Phase-1 selection ['hangzhou']`; `promotions / fallbacks (1, 0)`. The reimplementation independently returns promotions `['genua']`, fallbacks `[]`. |
| Y095 | CONFIRMED | `measure6.py` rerun. | `sources 5`; `source c_w rank range (55, 79)`; `source mean degree vs map (2.4, 4.0)`. With N = 80, ranks 55–79 are all in the bottom half. The script computes sources as in-degree-0 nodes and degrees from `solver.UND` — what the labels claim. |
| Y337 | CONFIRMED | Grepped v2 and v5 for the phrasing; degrees from `measure6.out`. | v2 L160: "Eight sources, all cul-de-sacs". v5 L369: "v2 called them 'cul-de-sacs', which their degrees do not support" — the CHANGED note in the inventory is right. Degrees 2.4 against 4.0, five nodes on one field. |
| Y096 | CONFIRMED | `measure6.py` for the three seeds; `/tmp/aud_batch.py` for six seeds (9000–9005), counting moved edges as well as the sink set. | Three seeds: `sinks under +/-1% wealth noise seed 0/1/2 → ['genua','hangzhou']`. Six seeds: sink set `genua, hangzhou` and **edges moved 0** in every one. Both halves exact. |
| Y338 | CONFIRMED | `/tmp/aud_misc.py`: took `R["order"]` from `run_drain` and tested `order[u] > order[v]` on all 159 directed edges. | `core nodes: 80 of 80; order defined on 80; core-core edges tested 159; violations 0; edges with a peeled endpoint 0`. Nothing is peeled on this graph, so the "pendants have no marking order" caveat the document raises at L970 does not bite here. |
| Y097 | CONFIRMED | `measure6.py` rerun. | `sinks per good min/max/mean (2, 8, 3.69)`; `acyclic goods 29`; `fallbacks fired across goods 0`; `ordered pairs connected 5723 of 6320`; `ordered pairs connected pct 90.6`. 6320 = 80 × 79. |
| Y098 | CONFIRMED | `measure6.py` rerun, plus an independent recomputation in `/tmp/aud_batch.py:coh()`. | `Phi_w self-coherence edge-goods 55.1`; `value-weighted 54.8`. My independent implementation returns `Phi_w self-coherence: 55.1% edge-goods, 54.8% value-weighted`. |
| Y099 | CONFIRMED | Built `Φ_ord = Σ_g V_g·order_g` from the per-good `order` maps in `/tmp/aud_batch.py`, oriented by descending `Φ_ord`, and measured its self-coherence on the **current** field; then grepped v6.1 for any maintained `Φ_ord` figure. | `Phi_ord self-coherence: 59.8% edge-goods, 59.6% value-weighted` against `Φ_w`'s 55.1% / 54.8% — the superseded aggregate does score higher, on today's field and not just v5's. And the document maintains no figure: no "59.8", "60.3" or equivalent appears anywhere; §3.9 L1654 states the comparison qualitatively only. (For reference, v5 L374 recorded 52.5% against Φ_ord's 60.3%.) |
| Y100 | CONFIRMED | Grepped the three constants in the shipped code. | `measure6.py: A_PHI = 2.0`; `flowop.py: TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6`, each commented "a hyperparameter". No derivation appears anywhere in the scripts. The self-description is accurate. |
| Y102 | UNTESTABLE | — | A statement about how to read the section, not a proposition with a truth value. Its factual precondition — that the figures describe the field around the chosen values — is borne out by the sensitivity runs. |
| Y103 | CONFIRMED | `measure6.py` rerun: 701 DRAIN runs over α_Φ = 1.00…8.00 at 0.01, banded. | `band containing alpha=2 ('genua+hangzhou', 1.63, 3.28, 1.65)`, and `widest band on [1,8]` is the same band. Exact. |
| Y104 | CONFIRMED | `measure6.py` rerun. | `sink count at alpha 1,1.5,2,3,4,8 [3, 1, 2, 2, 1, 1]`. Non-monotone as stated. |
| Y992 | PARTIAL | `/tmp/aud_scale_eps.py` and `/tmp/aud_scale2.py`: swept `TIE_EPS` from 1e-13 to 1e5 against the shipped `drain.py`, under both the shipped `TIE_EPS2 = 1e-6` and `TIE_EPS2 = 0` (epsilon6.py's formula), and under both the pinned and the default LP tolerance. Also ran the cited script. | Three findings. (1) The cited instrument **crashes** — `epsilon6.py` raises `TypeError: mcf() got an unexpected keyword argument 'cost'`; it cannot report bands or bisect their edges, and its `eps=0` check compares the shipped map to itself. (2) The band is on the **orientation**, not the sink set. Under the shipped configuration the sink set is `{genua, hangzhou}` at **every** `TIE_EPS` from 1e-13 to 1e5 and at 0 — my bisection reports "no lower boundary above 1e-16, no upper boundary below 1e8" — while edge flips run 16 (≤1e-7), 14 (1e-6), 12 (1e-5), **0 (1e-4 … 1)**, 24–25 (≥10). (3) The lower edge does reproduce for the sink set under `TIE_EPS2 = 0` with the default LP tolerance — exactly epsilon6.py's configuration — where the sink set is `{hangzhou}` below 1e-6 and `{genua, hangzhou}` from 1e-6 up. So "1e-6" is a real number from a superseded configuration; "to about 1" bounds the orientation, not the sink set; and both stated mechanisms are CONFIRMED (pinning the tolerance to 1e-10 moves the lower edge down to ~1e-9/1e-8, and at `TIE_EPS ≥ 10` the term exceeds the base cost of 1 and the orientation breaks). |
| Y1010 | CONFIRMED | `/tmp/aud_scale_eps.py` part 3: rebuilt `TIE_COST` at `TIE_EPS2` ∈ {1e-7, 1e-6, 1e-5, 1e-4, 1e-3} and counted goods with an alternative optimum plus aggregate edge flips. | 1e-7, 1e-6 and 1e-5 all leave exactly **one** good — `paper` — with an alternative optimum, and 0 aggregate edge flips. At 1e-4 and 1e-3 the aggregate orientation starts to move (12 and 14 flips). So it behaves like `TIE_EPS`: a switch with a plateau, not a dial. |
| Y105 | CONFIRMED | Grepped v2–v5 for the withdrawn justifications and v6.1 for their absence. | v2 L372 justifies α_Φ = 1.5 by calibration to a target count; v5 L364-366 by band width. v6.1 asserts neither and warns against both. The warning is present and its factual premises check out. |
| Y106 | UNTESTABLE | — | A design claim about intent. Its measurable proxy (Y107) is verdicted separately. |
| Y107 | CONFIRMED | `/tmp/aud_europe.py` and `/tmp/aud_europe2.py`: α_Φ = 2.0, European wealth scaled ×1.00–×2.50, boundaries bisected. | At ×1.00 the ends are `genua` and `hangzhou`. By ×2.46–×2.50 they are `genua` and `rheinland` — two European ends, none in Asia; over ×1.38–×1.70 and ×1.71–×1.95 they are `english_channel, genua, rheinland` — three European, none in Asia. Europe gains ends and Asia loses its one, as a direction. |
| Y108 | CONFIRMED | Read `measure6.py:_from_dev`, which rebuilds wealth from **scaled `base_tax` and `base_production`** (not from a scaled wealth array — the script's own comment flags the earlier tautology) and compares against the scaled-wealth field; then re-ran it. | `dev-scaled vs wealth-scaled (max diff) 0.0`. Wealth is linear in development, so scaling development moves `c_w` directly. The mechanism is exactly as stated. |
| Y109 | PARTIAL | `/tmp/aud_europe.py` (0.005 grid plus bisection) and `/tmp/aud_europe2.py` (0.002 grid), α_Φ = 2.0, 824 counted European provinces, shipped `drain.py`. Also read the cited script. | Two things hold, two do not. **Holds:** 824 counted European provinces (`measure6.out: European counted provinces 824`); eight of the ten rows reproduce with boundaries within 0.001 of the stated ones (×1.1396, ×1.1585, ×1.1865, ×1.3502, ×1.9479, ×1.9726, ×2.4567). **Fails, row 6:** ×1.36–×1.38 is not one interval — ×1.3618–×1.3690 is `{genua, gulf_of_siam, hangzhou}` and only ×1.3690–×1.3817 is `{genua, gulf_of_siam}`. **Fails, row 7:** ×1.38–×1.95 is not `{english_channel, genua, rheinland}` throughout — ×1.7017–×1.7090 adds **`doab`**, so "Asia holds none" is false over part of the widest row. The 0.002 grid finds a third missed interval, ×1.288–×1.290, carrying the five-node set. A 0.0002 re-scan of the three disputed regions (`/tmp/q3_fine.py`) narrows the missed interval to ×1.2868–×1.2882, width **0.0014**, and finds no further structure inside two 0.06-wide samples of the long runs. There are at least **15** intervals, not 10, and the claim that "boundaries are bisected, so each row is the interval over which the set is constant" is therefore false of rows 6 and 7: bisecting only the boundaries a 0.01 grid detects cannot find intervals narrower than the grid, and the three missed ones are 0.007, 0.007 and 0.002 wide. **Provenance also fails:** `europe.py` runs α_Φ = 1.5 over ×1.00–×1.60 on a fixed 0.01 grid with no bisection — it cannot have produced this table. |
| Y110 | CONFIRMED | `measure6.out` for the province count; `ls` of the save directory and each readable save's `date=` field for the availability claim. | `European counted provinces 824` ✓. The four readable saves are three 1444.11.11 starts and `Castile1444_12_22.eu4` (1444.12.22) — no save later than 1444 exists to test against ✓. The uniform-multiplier caveat is exactly right, and my own measurement (Y109) shows the row boundaries are an artefact of one synthetic experiment even more than the document admits. |
| Y111 | PARTIAL | `/tmp/aud_europe2.py`: 0.002 grid over ×1.00–×2.50, plus 8 relabellings at a representative point inside every interval, using the config-D-validated reimplementation. | **Fails:** "`hangzhou` leaves at ×1.19" — `hangzhou` holds an end continuously to **×1.370**; what happens at ×1.19 is that `gulf_of_siam` is *added*. This contradicts the document's own table row 4 (`×1.19 – ×1.35 \| genua, hangzhou, gulf_of_siam`) as well as my measurement. **Fails:** "two intervals narrower than ×0.03 carry sets that appear once" — the document's own table has three (rows 2, 5, 8; widths 0.02, 0.01, 0.02) and my finer scan has five (0.019, 0.012, 0.007, 0.007, 0.026). **Holds:** "`gulf_of_siam` holds an end across ×1.19–×1.38 and nowhere else" — measured ×1.1865–×1.3817, and in no other interval up to ×2.50. **Holds:** "returns at ×1.95 and leaves again" — ×1.9479–×1.9726. **Holds, and this is the load-bearing part:** "the orientation is order-invariant at every row" — at a representative point in all 15 intervals, **0 of 8 relabellings moved an edge and 0 of 8 moved the sink set**, with the instrument reproducing `drain.py` on the identity at every point (`valid=True` ×15). |
| Y340 | CONFIRMED | Implied by Y109 and Y111: the sets are a function of the field, and the field is one snapshot under one scaling. | The instability my finer scan exposes — three intervals the document missed, two rows misstated — is itself the strongest available evidence for this caution. |
| Y112 | CONFIRMED | Read `measure6.py:_from_dev` (it rebuilds wealth from `PROV[pid]["base_tax"]` and `base_production` scaled by `k`, retaining the devastation multiplier) and re-ran it. | `dev-scaled vs wealth-scaled (max diff) 0.0`. The harness is not the tautology it replaced: it computes the two quantities by different routes and they agree to 12 decimal places. |
| Y341 | CONFIRMED | Read `common/institutions/00_Core.txt` at lines 276-290, 541-552 and 835-844. | `renaissance`: `historical_start_date = 1450.1.1`, `historical_start_province = 116 # Florence`. `new_world_i`: `1500.1.1`, `224 #Sevilla`. `printing_press`: `1550.1.1`, `1876 #Frankfurt`. All three in Europe, all between 1450 and 1550. Exact. |
| Y342 | PARTIAL | Read the `renaissance` block, lines 278-282. | The value is exact: `development_cost = -0.05`. But the block is `bonus = { development_cost = -0.05  build_cost = -0.05 }` — the embracement bonus is **two** modifiers, not one, and the institution also carries `trade_company_efficiency = 0.4` outside it. "The Renaissance's embracement bonus **is** `development_cost = -0.05`" understates what the file grants. |
| Y343 | CONFIRMED | Read all three `bonus` blocks; read `solver.py:province_table` and `build_sc` for what enters wealth. | The bonuses are country-scoped modifiers (`development_cost`, `build_cost`, `global_prov_trade_power_modifier`, `stability_cost_modifier`). `solver.py`'s wealth reads `base_tax`, `base_production`, `PRICES[good]` and one province-state multiplier (`devastation`) — no institution input at any point. They reach the map only through development. |
| Y344 | CONFIRMED | `/tmp/aud_geo.py`: enumerated every directed path from each named source to `hangzhou` in the shipped `Φ_w`. | Both historical corridors appear with no prompting — see Y345 and Y113. Nothing in the input names a route. |
| Y345 | CONFIRMED | `/tmp/aud_geo.py`, BFS plus full path enumeration on the shipped orientation. | `white_sea -> novgorod -> kazan -> siberia -> samarkand -> lahore -> lhasa -> ganges_delta -> burma -> gulf_of_siam -> canton -> hangzhou`, 11 hops. Character-for-character the document's chain. (Ten directed paths exist in total, lengths 11 and 12; the shortest is the quoted one.) |
| Y113 | CONFIRMED | Same run. | `sevilla -> safi -> timbuktu -> katsina -> ethiopia -> gulf_of_aden -> comorin_cape -> ganges_delta -> burma -> gulf_of_siam -> canton -> hangzhou` — the quoted prefix exactly, and **11 hops** exactly. |
| Y114 | PARTIAL | `/tmp/aud_geo.py`: degrees of `genua` and the full list of its in-neighbours. | Degrees exact: `genua out-degree 0 in-degree 5`, and no route leaves it. But the in-neighbours are `['alexandria', 'champagne', 'ragusa', 'tunis', 'valencia']`. The gloss "the western Mediterranean, the Adriatic and the Rhône" covers `tunis`/`valencia`, `ragusa` and `champagne` — it omits **`alexandria`**, the eastern Mediterranean, which is one of the five. |
| Y994 | CONFIRMED | Same run. | `english_channel -> genua: ['english_channel','champagne','genua']` — two hops through `champagne`. `english_channel -> hangzhou: NO ROUTE`. `english_channel` is not a sink at α_Φ = 2.0 (out-neighbours `champagne, lubeck, north_sea`). |
| Y115 | CONFIRMED | `/tmp/aud_eunodes.py`: enumerated Europe→sink pairs and Cape-transiting paths under six candidate definitions of "European node", since the document states none. | Under "a node a majority of whose provinces are European": **23 nodes, 27 connected Europe→sink pairs, 0 with a Cape-transiting path** — all three figures exact (identical under "majority of owned counted provinces European"). The count is definition-sensitive: "any European province" gives 25 nodes / 30 pairs / 0 via Cape; §1.6's own 22-node list (Y347) gives 22 / 25 / 0. The **0** holds under every definition tried, which is the load-bearing part. The unstated definition is a documentation gap, not an error. |
| Y346 | CONFIRMED | The Y115 enumeration is exhaustive by construction: all node × sink pairs, with Cape reachability computed from the full transitive closure. | The universal is asserted over an enumerated set, and it holds. |
| Y116 | CONFIRMED | `measure6.py` rerun and, independently, `/tmp/aud_geo.py` and `/tmp/aud_cape.py`. | `cape in-degree 2` from `['ivory_coast','zanzibar']`; `cape out-degree 2` to `['comorin_cape','malacca']`; `ordered pairs routed through the cape 81`. Both scripts agree. |
| Y117 | CONFIRMED | `/tmp/aud_cape.py` and `/tmp/aud_cape2.py`: computed the pair count under six readings. | The loose reading gives exactly **81** (a reaches Cape, Cape reaches b, a reaches b, Cape excluded as an endpoint). The strict reading gives exactly **69** under "the Cape lies strictly interior to the single BFS shortest path" (insertion-order adjacency). Both figures land on the nose. Other strict readings give 60 (every shortest path transits) and 71 (some shortest path transits), so 69 is implementation-dependent — but it is the number the natural single-path reading produces. |
| Y118 | CONFIRMED | `/tmp/aud_geo.py`: ran DRAIN on the `spices` and `cloves` per-good fields and computed the Cape's in/out sets and the Europe reachable from it. | For `spices` the Cape takes flow **from `malacca`** and passes it to `comorin_cape, ivory_coast, zanzibar`, and all 25 European nodes are reachable from it (sinks `brazil, genua`). Same for `cloves`. Cargo runs the other way from power, exactly as claimed. |
| Y119 | PARTIAL | `/tmp/aud_nodes.py`: scaled the wealth of every province in the named node sets, α_Φ = 2.0, and bisected the sole-sink onset. | **Off by 0.03:** the 18-node scaling makes `genua` the sole sink from **×1.51845** (bisected to five decimals), not "about ×1.55"; and it stays the sole sink continuously from there to ×3.20. **Holds, and very understated:** scaling all 22 produces no sole sink below ×4 — and none below **×20** (still `{genua, rheinland}` at ×20). **Fails:** "the eastern four keeping ends of their own" — `constantinople`, `crimea`, `kiev` and `kazan` hold **no end at any multiplier from ×1.00 to ×9.00** (`eastern-four ends: none` on every row). What blocks the sole sink is `english_channel` (to ×3) and then `rheinland` (to ×20 and beyond), not the eastern four. |
| Y120 | CONFIRMED | `/tmp/aud_nodes.py`: tracked the Cape's in- and out-sets across the 22-node scaling from ×1.00 to ×3.00 at 0.02. | At ×1.00: `in = ivory_coast, zanzibar; out = comorin_cape, malacca`. **At ×1.60: `in = comorin_cape, malacca, zanzibar; out = ivory_coast`** — the stated reversal, at the stated multiplier. And it is not a single window: nine distinct (in, out) configurations occur across ×1–×3 (changes at ×1.08, ×1.16, ×1.20, ×1.22, ×1.26, ×1.28, ×1.60, ×2.48), with the in-degree passing through 0 twice and the orientation changing again at ×2.48. A function of development, not a threshold. |
| Y347 | CONFIRMED | Counted the list against the node names in `nodes.json`. | 18 named western/central nodes (`english_channel, north_sea, baltic_sea, white_sea, novgorod, lubeck, rheinland, saxony, wien, krakow, pest, venice, ragusa, genua, champagne, bordeaux, valencia, sevilla`) plus 4 (`constantinople, crimea, kiev, kazan`) = 22. Internally consistent, and all 22 are real node names. (Note the tension with Y115's "23 European nodes": the two sets are defined differently and neither definition is stated.) |
| Y121 | CONFIRMED | `/tmp/aud_nodes.py`: multiplied the single highest-wealth province of four nodes by ×1 … ×500. | `english_channel` (pid 1744): sole sink from ×20. `venice` (pid 112): from ×10. `hangzhou` (pid 1821): from ×10. `north_sea` (pid 248): from ×20. And intermediate boosts do produce extra sinks — `hangzhou` ×5 gives three (`genua, gulf_of_siam, hangzhou`) — so the pattern the claim calls expected is what happens. |
| Y348 | CONFIRMED | Grepped `drain.py` and `flowop.py` for a linear solve. | `'linalg.solve' in drain.py: False`; `'solve_phi' imported: False`; the only solver reached is `scipy.optimize.linprog` plus a combinatorial sweep. `solver.solve_phi` (the v1 Laplacian) is never called on the `Φ_w` path. With no linear solve there is no linearity to lean on. |
| Y349 | UNTESTABLE | Searched for a DLL implementation. | There is no DLL, so the reference-vs-DLL comparison cannot be run. The check as specified (exact orientation equality, no tolerance band) is well defined, and the reference side exists. |

## §1.7 — Merchants

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y350 | PARTIAL | Grepped `common/defines.lua` for a per-node merchant cap; inspected the save's schema. | No define caps merchants per node. Structural evidence in the save supports the claim: each country's sub-block inside a trade node carries a boolean `has_trader=yes`, not a count — the engine's own data model admits at most one merchant per country per node. "Placement, range and the collect/steer choice are vanilla" is a statement about an unbuilt mod and cannot be checked. Settling the cap properly needs an in-game attempt to place a second merchant in an occupied node. |
| Y351 | CONFIRMED | Read `common/defines.lua` lines 1197 and 1201. | `MERCHANT_MAX_POWER_BONUS = 2.0,  -- MERCHANT_MAX_POWER_BONUS` and `TRADE_MERCHANT_PRESENT = 0.1,  -- bonus on income if trade present`. Both values and the quoted comment are exact. |
| Y352 | CONFIRMED | Grepped v1 and v2 for the wording; read the define's comment. | v1 L93 and v2 L180 both read "+2 trade power and +10% trade efficiency". The shipped comment is "bonus on income if trade present", and EU4 keeps trade efficiency as a separate modifier with its own ledger column (`modifers_l_english.yml`, `LEDGER_TRADE_EFFICIENCY`). The define's own comment does settle which quantity this is. |
| Y353 | CONFIRMED | Grepped `common/defines.lua` for the penalty. | `common/defines.lua:1200: TRADE_NON_CAPITAL_OFFICE = -0.50,  -- TRADE_NON_CAPITAL_OFFICE` — the −50% for collecting outside the home (capital) node, as a shipped define. The document does not name it; the value it states is right. |
| Y354 | UNTESTABLE | — | Describes the mod's node window. No build exists. The vanilla precondition it relies on is CONFIRMED under Y355. |
| Y355 | PARTIAL | Read `interface/tradeinterface.gui`. | Both identifiers exist and are clickable list containers: `incoming_nodes_listbox` (L90, L519) and `outgoing_nodes_listbox` (L110, L528), both `OverlappingElementsBoxType`. `TradeNodeLink` exists as a `windowType` (L18) containing a `guiButtonType` named `NextNodeButton` and one label. What the file does **not** record is that either listbox is populated by `TradeNodeLink` — the `.gui` declares the containers and the item template separately, and the binding is engine-side. That half is inference, not file evidence. |
| Y356 | UNTESTABLE | — | A statement of what the mod must change. No build exists. |
| Y357 | CONFIRMED | Read the `TradeNodeLink` widget definition, L17-49 of `interface/tradeinterface.gui`. | The widget contains exactly one interactive element — `guiButtonType { name = "NextNodeButton" … tooltip = "" tooltipText = "" delayedTooltipText = "" }` — and one text label. There is no second button and no dispatch target. The widget's only affordance is navigation, so the file corroborates the §2.7 item 14 observation independently of re-running it, and "a new interaction on an existing widget" follows. |
| Y358 | UNTESTABLE | — | Mod semantics; no build. |
| Y359 | UNTESTABLE | — | Mod semantics; no build. |
| Y360 | UNTESTABLE | — | Mod semantics; no build. |
| Y361 | UNTESTABLE | — | Mod semantics; no build. |
| Y362 | UNTESTABLE | — | Mod semantics; no build. The vanilla grant conditions it constrains are CONFIRMED under Y364. |
| Y363 | CONFIRMED | Read the two engine grant conditions and the collection path. | The grant keys are `MERCHANT_PRESENT_INLAND` and `MERCHANT_STEERING_TO_INLAND`; only the second is a steering condition — the first is a *collect*-at-inland condition. A constraint on steering therefore cannot touch collect-as-main-trading-port. The derivation is sound given Y364. |
| Y364 | CONFIRMED | Grepped the install for the identifiers; read the tooltip. | `localisation/text_l_english.yml:7859: MERCHANT_PRESENT_INLAND:0 "Merchant present inland"` and `:7860: MERCHANT_STEERING_TO_INLAND:0 "Merchant steering towards inland"`; both strings also appear in `eu4.exe`. Tooltip: `tradenodes_l_english.yml TRADEMAP_INLAND_DESC:0 "Having a merchant present that collects in an inland trade node, or steers towards an inland trade node, will give you extra trade power in that node based on your trade efficiency."` — "that node" is the inland one, so the tooltip does read as granting it in the inland node. Also `MERCHANT_MAX_POWER_INLAND` / `MERCHANT_MAX_POWER_STEERS_TO_INLAND` for the itemisation. The document lower-cases the identifiers; the shipped keys are upper-case. |
| Y365 | UNTESTABLE | — | A cross-reference to §2.7 and §3.11, both outside this slice. |

## §1.8 — Collection and transfer

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y366 | UNTESTABLE | — | Mod design; no build. |
| Y367 | UNTESTABLE | — | The mod's collection formula; no build. |
| Y368 | UNTESTABLE | — | The mod's per-good eligibility rule; no build. |
| Y369 | UNTESTABLE | — | The mod's per-good remainder rule; no build. The vanilla two-case rule it invokes is tested under Y370–Y373. |
| Y370 | PARTIAL | `/tmp/aud_steer3.py` and `/tmp/aud_split.py`: reconstructed every link's realised value from the receiving node's `incoming = { add= value= from= }` blocks in `Castile1444_12_22.eu4` (159 blocks, one per link; `from` resolves 1-based against the node order — verified against the shipped topology, 159 of 159 resolving to a real upstream node), then compared the split against steerer counts. | The direction of the claim holds: of 56 nodes with ≥2 discovered outgoing links, every one carrying steerers splits **unevenly** (`champagne` [4.964, 0.0] with 6 steerers; `rheinland` [3.337, 0.187] with 11). But the save records `steer_power` only per country per **node**, never per link, so "in proportion to the modified trade power steering toward each link" cannot be verified as a proportion. Settling it needs the node window's per-link tooltip read in-game with controlled merchant placement. |
| Y371 | CONFIRMED | `/tmp/aud_gate.py`: for all 159 links, classified by realised value and by whether any country holds power at both endpoints. | 50 links carry zero value. 33 of those have **no** country holding power at both ends (Y375's gate). The remaining **17 carry zero while 1–9 countries hold power at both ends** — `champagne → genua` = 0.0 with 9 both-ends holders while `champagne → english_channel` carries 4.964; `tunis → genua` = 0.0 with 8; `canton → hangzhou` = 0.0 with 8; `hangzhou → malacca` = 0.0 with 7. The both-ends gate cannot explain these, and the only remaining vanilla mechanism is the absence of a steerer on that link. Exactly the claim: an outgoing link with no steerer receives nothing even when siblings are steered. |
| Y372 | CONFIRMED | `/tmp/aud_split.py`: isolated nodes with exactly one steering merchant and measured the largest link's share of that node's outgoing value. | Two such nodes exist in the save and both are unanimous. `hangzhou`: 1 steerer, values `[0.0, 10.629, 0.0]` — **largest link share 1.0000**. `timbuktu`: 1 steerer, values `[0.0, 0.677]` — **largest link share 1.0000**. A single steerer takes all of it. |
| Y373 | PARTIAL | Same run, restricted to nodes with zero steering merchants and ≥2 discovered outgoing links. | Confirmed on 4: `cuiaba` [0.085, 0.085, 0.085], `james_bay` [0.049, 0.049], `rio_grande` [0.129, 0.129, 0.129], `siberia` [0.168, 0.168] — even to three decimals. Fails on 5, all American: `lima` [0.046, 0.0], `mexico` [0.0, 0.081, 0.0], `mississippi_river` [0.0, 0.061], `patagonia` [0.031, 0.0], `california` [0, 0, 0.012, 0]. Each failure has a link receiving exactly 0, which Y375's both-ends gate would also produce, and the save cannot separate "ineligible link" from "uneven split". So the even split is confirmed among eligible links and unconfirmed as stated. |
| Y374 | UNTESTABLE | — | The mod's sink rule; no build. |
| Y375 | CONFIRMED | `/tmp/aud_gate.py`, as Y371. | Of the 50 zero-value links, **33 have no country holding power at both ends**; of the 109 value-carrying links, only 3 lack one. The both-ends rule is visible in the realised flow. Trade range is CONFIRMED separately at Y376. |
| Y376 | CONFIRMED | Grepped each named string in `localisation/`. | All seven exist, and all seven are about reach: `hints_l_english.yml:230 HINT_TRADERANGE_TEXT` "Trade Range determines how far away you may send a Merchant"; `EU4_l_english.yml:1353 TRADE_RANGE_IRO` "Our merchants can reach trade nodes within this range"; `EU4_l_english.yml:2847 TRADE_NODES_OUT_OF_RANGE` "The following known nodes are outside your trade range"; `core_l_english.yml:325 MAPMODE_TRADE_DESC` "Checkers indicate provinces which are NOT in trade range"; `emperor_mercs_l_english.yml:15/17 MERCENARY_COMPANY_TOO_FAR` / `MERC_RANGE_EXPLAINED` (mercenary hiring); `domination_l_english.yml:2100 REQUIRES_CAPITAL_IN_TRADE_RANGE_TT` (a diplomatic precondition). |
| Y377 | CONFIRMED | Grepped every `trade_range` occurrence in `common/` and reduced to the unique token set. | Only two tokens exist across the whole tree: `trade_range` and `trade_range_modifier`; every occurrence in `common/` is a country, estate or event modifier value (custom ideas, burgher and Jain privileges, event and mission modifiers). Nothing ties range to link flow. The claim's own scope note — this is about the files, not a proof — is the right one, and the experiment it names (value arriving beyond every country's range) is the right test. |
| Y378 | CONFIRMED | Grepped the install for supply-range constructs. | Exactly two exist and both are naval: `common/defines.lua:1365 NAVAL_SUPPLY_RANGE = 150, -- Supply range for ships.` and `localisation/text_l_english.yml:6147 SHIP_SUPPLY_RANGE:0 "Supply ships reach"`. No trade supply range anywhere in `common/`, `interface/` or the English localisation. |

## §1.9 — Trade power propagation

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y379 | CONFIRMED | `/tmp/aud_prop2.py` and `/tmp/aud_prop3.py`: parsed every country sub-block of all 80 trade-node records in `VANILLA_start.eu4`, built the vanilla downstream map from `common/tradenodes/00_tradenodes.txt`, and predicted each country's propagated power from its downstream `province_power`. | Over 52,517 entries where a country holds no local province or ship power, `\|val − predicted\|` has **median 0.000000**. On the 414 entries carrying a `prev` (the propagation basis) the threshold-aware model is exact to 0.0014 — the save's own three-decimal rounding. And the "no condition on the receiving node" half is directly visible: **France holds 0 of Sevilla's 52 provinces** (owners `CAS 31, POR 13, GRA 4, MOR 4`) and still receives power there. |
| Y380 | CONFIRMED | Found the tooltip string, then contradicted it from the save. | `localisation/tradenodes_l_english.yml:150 TRADE_POWER_UPSTREAM_DESC:0 "A nation can Transfer Trade Power back upstream to trade nodes where it already has power."` — the quoted qualifier, verbatim. It is false: FRA has no provinces, no merchant and no prior power in `sevilla`, and receives 3.319 there. |
| Y381 | CONFIRMED | Read the `sevilla / FRA` sub-block of `VANILLA_start.eu4` and traced the source. | `val=3.319` (→ 3.3), `prev=3.158`, `max_pow=3.158`; the sub-block carries no `province_power` and no `has_trader`. `localisation/tradenodes_l_english.yml:149 MERCHANT_DOWNSTREAM_BONUS:0 "Transfers from traders downstream: $VAL$"` is the itemisation string, and 3.158 truncates to the quoted +3.1. The source is exact: Sevilla's only downstream neighbour is `valencia`, where FRA's `province_power = 15.792`, and 15.792 / 5 = **3.1584**. Nothing else contributes. |
| Y382 | UNTESTABLE | — | A statement about §3.16's bookkeeping, outside this slice. The underlying line (Y379–Y381) does close in favour of the spec. |
| Y383 | PARTIAL | Read the defines, fitted the share against the save, then **bisected the threshold** over twenty candidate values in `/tmp/q56.py` (414 propagated entries). | `common/defines.lua:1205-1206: TRADE_PROPAGATE_DIVIDER = 5, TRADE_PROPAGATE_THRESHOLD = 2`. **Share = 1/5 is exact** (FRA 15.792/5 = 3.1584 = `prev`; median error 0.000000 over 52,517 entries). **The threshold is bounded, not pinned.** Every candidate in `(5.014, 10.038]` fits identically — max error 0.0014, 414 of 414 entries exact — because the observed downstream `province_power` values have a gap there (largest below: 5.014; smallest above: 10.038). Candidates ≤ 5.014 are excluded (max error 1.0032) and > 10.038 are excluded (≥ 2.016). So the save **decisively excludes the no-threshold reading** and is **consistent with** `2 × 5 = 10`, but cannot distinguish 10 from 6, 7, 8 or 9. Settling it needs a save containing a downstream holder with power inside (5.014, 10.038]. |
| Y384 | PARTIAL | `/tmp/aud_steer3.py`: found the 186 entries with `ship_power > 0` in `Castile1444_12_22.eu4` and tested whether ship power enters the propagated total; then traced every source of the modifier in the install. | The gate is CONFIRMED: over 209 entries with a downstream ship-power source, `\|prev − province_power/5\|` has max **0.0014**, while `\|prev − (province+ship)/5\|` has max **6.1602** and mean 1.6982 — ship power propagates **not at all**. And no country can have the modifier at 1444: `ship_power_propagation` comes only from `power_to_the_smugglers_reform` (pirate republics), the age_of_reformation ability `ab_ship_power_propagation`, custom ideas and mission modifiers. So "only where the country has a ship-propagation modifier" is consistent with everything observable. The **compounded rate** (share × modifier) is untestable from available saves: no save exists in which any country holds both ship trade power and the modifier. |
| Y385 | CONFIRMED | `/tmp/aud_prop2.py`: computed the one- and two-hop-upstream sets of every node where FRA holds province power, and looked for FRA in each. | FRA holds province power in `bordeaux, champagne, valencia`. One hop up: `bordeaux 39.174, rheinland 13.673, sevilla 3.319, tunis 3.319` (plus `carribean_trade, ivory_coast, st_lawrence`, undiscovered). Two hops up — `amazonas_node, brazil, cape_of_good_hope, chesapeake_bay, james_bay, katsina, kongo, mexico, mississippi_river, ohio, panama, safi, saxony, timbuktu, wien` — FRA is absent from **all 15**. Strictly one hop. |
| Y386 | CONFIRMED | `/tmp/aud_prop3.py`: isolated entries fed by more than one downstream neighbour and summed the qualifying contributions. | `alexandria/NAP`: parts [0, 12.47, 31.015] → (12.47 + 31.015)/5 = **8.6970** = `prev` exactly. `deccan/VIJ`: [13.369, 124.453] → 27.5644 against `prev` 27.563 (0.0014, save rounding). Contributions from all downstream neighbours are summed. |
| Y387 | UNTESTABLE | — | The mod reads direction from `Φ_w`; no build. |

## §1.10 — Direction-dependent systems

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y388 | UNTESTABLE | — | Mod design; no build. |
| Y389 | UNTESTABLE | — | Mod design; no build. |
| Y390 | UNTESTABLE | — | The mod's three-rung fallback ladder; no build. Its rung-2 precondition (per-good graphs exist and connect most pairs) is CONFIRMED at Y097: 90.6% of ordered pairs. |
| Y391 | CONFIRMED | The mechanism the derivation depends on is Y379 / Y385 / Y386, all confirmed against the save. | Propagation is direction-dependent (a share to *upstream* neighbours only) and summed over neighbours, so flipping a link necessarily moves propagated power at both ends and changes the fan-out. The inference is sound given the confirmed propagation rule. |
| Y392 | CONFIRMED | Read each mechanic's shipped definition (defines and trading policies) for any patched-in-the-mod marker, and checked their evaluation cadence. | None of the mechanics in the table is redefined anywhere in the mod, which ships no `common/` overrides at all — only the four probe mods, which touch `common/tradenodes`. Trade power shares are recomputed monthly by the engine, so all of it moves monthly. |
| Y393 | CONFIRMED | Read `common/defines.lua` lines 164-165. | `JUSTIFY_TRADE_CONFLICT_LIMIT = 0.2, -- How big share of the trade power needed on the target …` and `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT = 0.1, -- … on the actor …`. Names, values and the target/actor assignment all exact. |
| Y394 | CONFIRMED | Read `common/defines.lua` line 367. | `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER = 0.2, -- Minimum trade power needed for a country that won a war to block privateer from the country that lost the war`. |
| Y395 | CONFIRMED | Read `common/defines.lua` lines 1211 and 1213. | `TRADE_COMPANY_CONTROL_LIMIT = 0.6` and `TRADE_COMPANY_STRONG_LIMIT = 0.51`. Both exist and both are single-valued. |
| Y396 | CONFIRMED | Read `common/trading_policies/00_trading_policies.txt` lines 101-145, and 146-190 for the `_upgraded` twin. | `can_select` requires `has_trader = ROOT` plus `trade_share = { country = ROOT share = 50 }`; `can_maintain` requires `has_trader = ROOT` plus `share = 40`. Both share tests sit inside `if = { limit = { NOT = { has_government_attribute = free_improve_inland_routes } } … }`, so the attribute waives them entirely. 50/40, merchant present, waived by that attribute — all four elements exact, and identical in the upgraded twin. |
| Y397 | CONFIRMED | Read the `propagate_religion` `can_select` and `can_maintain` blocks, lines 239-350. | The `orm_easier_propagation_flag` branch requires `share = 50` in both `can_select` and `can_maintain`; the terminal `else` requires `share = 35` in both. 50/50 and 35/35, neither banded. |
| Y398 | CONFIRMED | Read the nine `has_country_flag = N_trade_power_for_propogate_religion` rungs in both blocks and paired select against maintain. | Nine rungs (5, 10, 15, 20, 25, 30, 35, 40, 45). Select → maintain: **5 → (no share at all)**, 10 → 5, 15 → 5, 20 → 10, 25 → 15, 30 → 20, 35 → 25, 40 → 30, 45 → 35. The document's eight pairs match one for one; the 5-rung's `can_maintain` really is `has_trader` + `is_node_in_trade_company_region` with no `trade_share`; and the trail is 5 points at the 10-rung and 10 points at the other seven — "5–10 points" exact. |
| Y399 | CONFIRMED | Cross-read Y393–Y398 plus v1's version of the table. | Improve Inland Routes is the only unconditionally banded mechanic (50/40, in both branches). Every other listed threshold is a single value — 0.2, 0.1, 0.2, 0.51, 0.6, plus Propagate Religion's 50/50 and 35/35. Propagate Religion is banded only on its flag ladder. |
| Y400 | CONFIRMED | Derived from Y393–Y399, all file-confirmed. | Six of the seven table rows are single-valued, and the two Propagate Religion branches covering flagless countries are 50/50 and 35/35 — no hysteresis. A share oscillating across any of them flickers the mechanic. Both the v5 wording the inventory records as CHANGED and the v6 wording are consistent with the files; v6's is the more precise. |
| Y401 | CONFIRMED | Read the three defines. | `TRADING_POLICY_COOLDOWN_MONTHS = 12` (L1045), `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` (L1212), `TRADE_COMPANY_COOLDOWN = 60` (L1214). Three shipped defines, rate-limiting exactly the mechanics in the table's lower rows. |
| Y122 | CONFIRMED | Enumerated the top-level entries of `common/trading_policies/00_trading_policies.txt` and their `cooldown` keys. | Nine entries: `maximize_profit`, `maximize_profit_upgraded`, `hostile_trading`, `hostile_trading_upgraded`, `improve_inland_routes`, `improve_inland_routes_upgraded`, `establish_communities`, `establish_communities_upgraded`, `propagate_religion`. Only the first two carry `cooldown = no` (L25, L52), so **7 of 9** entries are rate-limited. Five families, four with an `_upgraded` twin, `propagate_religion` with none — so **4 of the 5 families**. Every count exact. |
| Y123 | CONFIRMED | Same file. | `maximize_profit` L25 `cooldown = no`; `maximize_profit_upgraded` L52 `cooldown = no`. `propagate_religion` (L239-350) carries no `cooldown` key, so the 12-month default applies — it is inside the cooldown. |
| Y124 | CONFIRMED | Read the two defines and the mechanics they gate. | `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30`, `TRADE_COMPANY_COOLDOWN = 60`. Together with the 12-month policy cooldown these damp three mechanics (the two trade-company rows and the policy ladder), so a flickering share does not flicker the effect there. |
| Y125 | CONFIRMED | Counted which table rows have a cooldown against which do not. | Cooled: the trading-policy rows (Improve Inland Routes, Propagate Religion, and the other policies) and the two trade-company rows. Uncooled: both trade-conflict casus belli thresholds and privateer blocking. Of the seven-row table the two casus belli rows and privateer blocking are exposed; "most of the ladder" slightly overstates 3 of 7, but the direction — the exposed set is exactly what has no cooldown — is right. |
| Y402 | CONFIRMED | Derived from Y393–Y399. | The single-valued limits are 0.2, 0.1, 0.2, 0.51, 0.6; the flagless Propagate Religion branches are 50/50 and 35/35. Improve Inland Routes and the flag ladder are banded and so excluded. The set is the one the document names, not "every country". |
| Y403 | CONFIRMED | From Y393 (no banding, no cooldown on either casus belli threshold) plus the monthly recomputation. | Both casus belli thresholds are single-valued and neither is inside any of the three cooldowns, so their availability is the one thing that can appear and vanish month to month. |
| Y404 | CONFIRMED | Read `common/defines.lua` lines 1220-1222 and the grant conditions. | `CARAVAN_FACTOR = 3.0, -- Development is divided by this factor, do not set to zero!`, `CARAVAN_POWER_MAX = 50`, `CARAVAN_POWER_MIN = 2`. The shipped comment confirms development ÷ factor; the clamp names are exact; the merchant gate is `MERCHANT_PRESENT_INLAND` / `MERCHANT_STEERING_TO_INLAND` (Y364). Not a threshold on raw power at any point. |
| Y405 | CONFIRMED | Follows from Y126 and Y406, both measured. | The cap is 9.4%–47.0% of an inland node's total power (median 21.6%) and exceeds the largest incumbent in 7 of 26 nodes — enough to move shares by itself and so to push others across the thresholds. |
| Y126 | CONFIRMED | `/tmp/aud_save.py`: parsed the 26 `inland = yes` nodes from `common/tradenodes/00_tradenodes.txt` and each node's `total` from `VANILLA_start.eu4`. | `inland=yes: 26` nodes. `totals: min 106.4 at xian ; max 532.0 at champagne`. `50/total: 9.4% - 47.0%  median 21.6%`. Every figure exact. |
| Y127 | CONFIRMED | Same run for the post-grant figures; grepped v5.0 for how it framed them; checked the arithmetic. | `50/(total+50): 8.6% - 32.0%  median 17.7%` — exact. v5.0 L553 states "the cap of 50 is **8.6% to 32.0% of an inland node's total trade power**", i.e. under the first description, exactly as v6.1 says. And the internal check holds: 8.6% × 532.0 = 45.75 → 45.8, not 50. |
| Y128 | CONFIRMED | Same run, dropping `siberia`. | `dropping siberia (25 nodes): median 50/total 21.3% ; median 50/(total+50) 17.5%`. Both exact. |
| Y406 | CONFIRMED | Same run: the maximum per-country `val` inside each inland node's sub-blocks. | `range 23.6 to 143.2`; `cap 50 outweighs the largest incumbent in 7 of 26 ; outweighed in 19`. All three exact. |
| Y407 | CONFIRMED | `/tmp/aud_save.py`: compared each node's `highest_power` against the largest country `val` in its own sub-blocks, and against every ratio to `total`, `max`, `p_pow` and `collector_power`. | `nodes tested 79 ; highest_power != largest val on 79`. At `venice`: `highest_power = 53.2` against `VEN`'s own `val = 106.206` — the document's 53.2 / 106.2 exactly. And it matches no fixed share of anything: `highest_power/total` gives 78 distinct ratios over 79 nodes (0.0193–0.6783), `/max` 79 distinct, `/p_pow` 75, `/collector_power` 76. I also verified v4.0 L460's inverted conclusion ("largest single incumbent holder of 9.6 to 20.7 — so one country at the cap outweighs every incumbent in every inland node"). |
| Y408 | CONFIRMED | Grepped the mod's scripts for any read of `highest_power`. | `solver.py`, `drain.py`, `flowop.py` and `measure6.py` read only `base_tax`, `base_production`, `owner` and `trade_goods` from provinces, and nothing at all from a save's trade block. The field is not read — and my own ratio sweep did not determine what it holds either. |
| Y409 | CONFIRMED | Grepped v1 and v2. | v1 L169 and v2 L272 both read "It is a step function on raw power". Both files also carry a §3.11 ("Why caravan power needs a condition added", v1 L444, v2 L712) whose whole premise is a gated, development-scaled bonus — the contradiction the document names. |
| Y410 | CONFIRMED | Wrote a comment-stripping sweep over `common/`, `missions/`, `decisions/`, `events/` — 2,624 `.txt` files — matching all 80 trade-node names as whole tokens. | 239 hits, and **all 239 are inside `common/tradenodes/00_tradenodes.txt` itself**, the definition file. `hits outside common/tradenodes: 0`. Zero non-comment references in scripted content. One caveat worth recording: 63 trade-company *identifiers* embed node names (`trade_company_genua`, `trade_company_english_channel`, …), which the whole-token match correctly excludes because they are not node references the engine resolves — but node names do appear in `common/trade_companies/` in that form. |
| Y411 | PARTIAL | Enumerated every key used in `common/trade_companies/00_trade_companies.txt`. | The operative point holds: no `trade_node` token appears anywhere in the file, so trade companies never name a node. But they are not *bare* province lists — the keys in use are `provinces`, `color`, `name`, `names`, `primary_culture`, `tag` and `trigger` (4 trigger blocks, all tag/culture tests). The province list is the only geographic content; it is not the only content. |
| Y412 | REFUTED | Comment-stripped sweep of `common/`, `missions/`, `decisions/`, `events/` for every `[a-z_]*trade_node[a-z_]*` token, then checked each against `common/scripted_triggers/` and `common/scripted_effects/` to separate engine constructs from user-defined names. | The four families the document lists are all real (`home_trade_node` 36, `any_active_trade_node` 90, `random_active_trade_node` 66, `every_active_trade_node` 9, `any/random/every/all_trade_node_member_province` 80/75/16/15, `highest_value_trade_node` 38). But the list is **not** the set: nine further **engine** constructs are in use and none is covered — `every_trade_node_member_country` (44), `any_trade_node_member_country` (16), `add_trade_node_income` (28, e.g. `missions/99_Hansa_Missions.txt:2034`), `trade_node_value` (20), `any_trade_node` (6), `same_trade_node_as` (3), `all_trade_node` (3), `random_trade_node` (3), `has_privateer_share_in_trade_node` (1). Each was checked and none is defined in `scripted_triggers/` or `scripted_effects/`. Two of the omissions matter for this mod specifically: `trade_node_value` and `add_trade_node_income` read and write node value, which §2.1 rewrites. (`is_trade_node_province` and `is_inland_trade_node_province` *are* scripted triggers, and are correctly outside the engine list.) **A follow-up sweep found eight more**, all node-scoped engine constructs whose names do not contain `trade_node` and which a token search on that substring therefore misses: `trade_share` (671 uses), `is_strongest_trade_power` (373), `add_trade_modifier` (293), `trade_income_percentage` (146), `privateer_power` (111), `has_trader` (62), `is_node_in_trade_company_region` (36), `has_most_province_trade_power` (8) — none of them scripted-defined. The list is short by **17** engine constructs, and the exposed surface is roughly **2,100** uses rather than the ~380 the four named families cover. |
| Y413 | CONFIRMED | Follows from Y410 plus the mod's own scope. | No scripted content names a node, and the mod changes only connections — the four probe mods rewrite `common/tradenodes` link blocks, leaving node identities and `members` lists untouched. With no node name to collide with, the name-collision class is empty. |
| Y414 | PARTIAL | From Y412's inventory of what scripted content actually uses. | The exposure is real and larger than the claim states: `highest_value_trade_node` (38 uses) and node-scoped triggers do change sense under reorientation — but so do `trade_node_value` (20), `add_trade_node_income` (28) and `same_trade_node_as` (3), which the document's list never mentions. The mechanism is right; its inventory of the exposed surface is short by the same **17** constructs as Y412 — including `trade_share` (671 uses), the construct every §1.10 threshold in the table is actually written in, and `is_strongest_trade_power` (373), a within-node power-share comparison. A concrete instance of the sense-change the claim predicts: `missions/AFR_Mutapa_Missions.txt:704 zim_dominate_upstream_trade` is named for vanilla's flow direction but contains **no direction test at all** — its trigger is ownership, ports, centre-of-trade level, `is_strongest_trade_power` and `trade_share`. It cannot break; it can only stop meaning what its name says. |
| Y415 | UNTESTABLE | — | A statement of project policy. |

## §1.11 — Treasure fleets

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y416 | UNTESTABLE | — | The mod's rule; no build. It is a *change* from vanilla (where privateers can intercept), so nothing in the install can confirm it. |
| Y417 | UNTESTABLE | — | The mod's routing rule; no build. |
| Y418 | CONFIRMED | Grepped the install for the diversion mechanic. | It exists and is exactly a colonial gold-fleet diversion: `common/subject_type_upgrades/00_subject_type_upgrades.txt:30` defines `enlarge_the_gold_fleet`, gated on `is_subject_of_type = crown_colony`, granting `modifier_overlord = { treasure_fleet_income = 0.2 }` against `modifier_subject = { liberty_desire = 10 }`; `common/government_reforms/06_government_reforms_common.txt:296` grants a further `treasure_fleet_income = 0.25`; and `localisation/EU4_l_english.yml:1041 INCOME_TREASURE_FLEET:0 "Treasure Fleet"` makes it its own income line. Income moves from the colonial nation to the overlord where the mechanic is active. Supporting defines: `TREASURE_FLEET_INFLATION = 0.5`, `TREASURE_FLEET_OPINION_HIT = -25`. |
| Y419 | CONFIRMED | Checked both halves: the engine's category, and what the model reads. | The engine keeps gold as its own category — `localisation/text_l_english.yml:981 GOLD_INCOME:0 "Gold Income"`, plus `GOLD_MINE_SIZE = 40` as the base income and `GOLD_INFLATION` for its own inflation path — separate from tax and production. And `solver.py` excludes it explicitly: `EXCLUDED = {"gold", "unknown"}`, `GOODS = sorted(g for g in PRICES if g not in EXCLUDED)`, so gold enters no supply share, no `V_g` and no `wealth` term, diverted or not. |

## §1.12 — What the game displays

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y420 | UNTESTABLE | — | Mod design; no build. |
| Y421 | UNTESTABLE | — | Mod map-mode design; no build. |
| Y422 | UNTESTABLE | — | Mod interaction design; no build. |
| Y423 | CONFIRMED | Enumerated the node window's value fields in `interface/tradeinterface.gui`; counted the goods in `common/prices/00_prices.txt` via `solver.py`. | The window carries exactly four node-level value fields, and they are the four named: `incoming_value` (L199/L668), `local_value` (L211/L680), `total_value` (L223/L692), `outgoing_value` (L235/L704) — plus `piracy_value`, `light_ships_in_node_value` and `goods_produced_value`. None takes a commodity argument; no per-good field exists. And thirty is the right number: `GOODS in price file (excl gold/unknown): 30` (29 live at 1444, `coal` latent). |
| Y424 | PARTIAL | Read the save's link representation. | The one-scalar-per-link half is CONFIRMED from the primary source: each link appears once, as an `incoming = { add= value= from= }` block in the receiving node — 159 blocks for 159 links, with no reverse-direction field anywhere. Whether the *UI* renders it "as net" is a rendering claim about a window I did not open; the shipped `.gui` has one label per link entry, which is consistent with it. |
| Y425 | UNTESTABLE | — | Describes what the mod will show for a quantity the mod defines; no build. |
| Y426 | UNTESTABLE | — | A statement about the mod's future asset footprint; no build. Its one factual precondition — that the incoming-link entries already exist as clickable widgets — is CONFIRMED at Y355 and Y357. |

---

## Summary

**Counts by verdict** (162 claims):

| Verdict | Count |
|---|---|
| CONFIRMED | 108 |
| PARTIAL | 19 |
| REFUTED | 3 |
| UNTESTABLE | 32 |

By section: §1.6 — 60 / 10 / 2 / 6 (78 claims). §1.7 — 6 / 2 / 0 / 8 (16). §1.8 — 6 / 2 / 0 / 5 (13).
§1.9 — 5 / 2 / 0 / 2 (9). §1.10 — 28 / 2 / 1 / 4 (35). §1.11 — 2 / 0 / 0 / 2 (4).
§1.12 — 1 / 1 / 0 / 5 (7).

### REFUTED (3)

- **Y333** — "The orientation degrades before the sink set does." Under the shipped solver the first
  scale at which the orientation degrades (×10⁻⁷) is the same scale at which the sink set degrades
  (`{english_channel, hangzhou}`, 22 flips), and the document's own ×10⁻⁴ figures show the same
  coincidence. The trailing conclusion survives on other evidence (at ×10⁻⁸, 24 edges are wrong and
  the sink set is right); the reason given for it does not.
- **Y332** — "the zero-flow tolerance is absolute (`1e-11`), so scaling `b` down pushes genuine flow arcs into
  the free set." The premise is true; the causal claim is not. Setting `ZERO_TOL` to **exactly 0** leaves the flip
  count, the free-set size and the sink set unchanged at every scale. The free set grows because HiGHS returns the
  all-zero flow once `|b|max` falls below the *primal* feasibility tolerance — not because a tolerance
  reclassifies anything.
- **Y412** — "Scripted content reaches nodes only structurally, through [four families]." Nine further
  engine constructs are in live use and none is covered: `every_trade_node_member_country` (44 uses),
  `any_trade_node_member_country` (16), `add_trade_node_income` (28), `trade_node_value` (20),
  `any_trade_node` (6), `same_trade_node_as` (3), `all_trade_node` (3), `random_trade_node` (3),
  `has_privateer_share_in_trade_node` (1). Two of them read and write node value, which §2.1
  rewrites.

### PARTIAL (19)

`Y329`, `Y081`, `Y084`, `Y087`, `Y992`, `Y109`, `Y111`, `Y342`, `Y114`, `Y119` (§1.6);
`Y350`, `Y355` (§1.7); `Y370`, `Y373` (§1.8); `Y383`, `Y384` (§1.9); `Y411`, `Y414` (§1.10); `Y424` (§1.12).

The five that matter most:

1. **Y109 / Y111 — the European-development table is under-resolved and two of its rows are wrong.**
   At α_Φ = 2.0 on a 0.002 grid the field has at least **15** intervals over ×1.00–×2.50, not 10.
   Row 6 (`×1.36 – ×1.38 | genua, gulf_of_siam`) is really two intervals — `hangzhou` still holds an
   end over ×1.362–×1.370. Row 7 (`×1.38 – ×1.95 | english_channel, genua, rheinland — Asia holds
   none`) is false over ×1.702–×1.710, where **`doab`** holds an end. A third interval,
   ×1.288–×1.290, carrying the five-node set, is missed entirely. All three are narrower than the
   0.01 grid — exactly the failure mode of bisecting only the boundaries a coarse grid detects — so
   the claim that "boundaries are bisected, so each row is the interval over which the set is
   constant" is not true of rows 6 and 7. §1.6's prose also says "`hangzhou` leaves at ×1.19", which
   contradicts its own row 4, and "two intervals narrower than ×0.03" where its own table has three
   and the field has five. The claim in this pair that is fully confirmed is the important one: **the
   orientation is order-invariant at every row** (0 of 8 relabellings moved an edge at a
   representative point in all 15 intervals).

2. **Y081 / Y332 — §1.6's "Scale" paragraph is a pre-tolerance-pinning measurement.** The flip counts
   (22, 96) and sink sets (`{english_channel, hangzhou}`, `{hangzhou}`) are exactly right, but under
   the shipped solver they occur at ×10⁻⁷ and ×10⁻⁹, not ×10⁻⁴ and ×10⁻⁶ — three orders of
   magnitude, exactly the three orders by which §1.6 itself (L533) tightened the LP tolerance from
   scipy's 1e-7 default to 1e-10. The paragraph also attributes the degradation to the absolute
   `ZERO_TOL = 1e-11`, but at the first degrading scale the free set is unchanged at 80/159 and only
   grows from ×10⁻⁸ down. The mechanism named is real; it is not the one producing the quoted
   numbers.

3. **Two cited scripts do not compute what they are cited for.** `scripts/epsilon6.py` (L570, the
   `TIE_EPS` bands) **crashes** on a signature mismatch with the current `drain.phase2`, and its
   `eps = 0` validation compares the shipped map to itself. `scripts/europe.py` (L586, the European
   table) runs α_Φ = 1.5 over ×1.00–×1.60 on a fixed 0.01 grid with no bisection — a different
   experiment at a different constant over a different range.

4. **Y992 — the `TIE_EPS` band is on the orientation, not the sink set.** Under the shipped
   configuration the sink set is `{genua, hangzhou}` at every `TIE_EPS` from 1e-13 to 1e5 and at 0;
   there is no band at all. What shows a plateau at [1e-4, 1] is the edge-flip count. The document's
   "1e-6" lower edge is a real measurement, but from the superseded configuration
   (`TIE_EPS2 = 0`, default LP tolerance); pinning the tolerance moves it down by three orders. Both
   mechanisms the document offers for the edges are correct.

5. **Y119 — "the eastern four keeping ends of their own" is false.** `constantinople`, `crimea`,
   `kiev` and `kazan` hold no end at any multiplier from ×1.00 to ×9.00 under the 22-node scaling.
   What prevents a sole sink is `english_channel` and then `rheinland`. The sole-sink onset under the
   18-node scaling also bisects to ×1.5185, not "about ×1.55".

### Two things settled in the document's favour that it did not claim to have settled

- **Y383's pending half, partly.** §1.9 flags "the threshold in raw power is `TRADE_PROPAGATE_THRESHOLD ×
  TRADE_PROPAGATE_DIVIDER`" as pending §2.7 probe 8. The save narrows it but does not close it: over 414
  propagated entries in `VANILLA_start.eu4`, **every threshold in `(5.014, 10.038]` fits identically** (max
  error 0.0014, 414 of 414 exact), while ≤ 5.014 is off by up to 1.0032 and > 10.038 by ≥ 2.016. So the
  no-threshold reading is decisively excluded and `10` is consistent — but 6, 7, 8 and 9 fit just as
  well, because the observed downstream powers have a gap between 5.014 and 10.038. Stating "= 10,
  measured" would be an over-claim; "in (5.01, 10.04], consistent with 2 × 5" is what the data supports.
- **Y099's comparison, on today's field.** The document asserts that the superseded marking-order
  aggregate scored higher on self-coherence while deliberately maintaining no figure for it. I built
  `Φ_ord = Σ_g V_g·order_g` from the current per-good runs: **59.8% edge-goods / 59.6%
  value-weighted**, against `Φ_w`'s 55.1% / 54.8%. The assertion holds on the current field, not just
  on v5's.

### On the 32 UNTESTABLE

All but three are the same thing: **the mod has no build.** `mod/` contains four probe mods
(`pgt_cycle`, `pgt_flip`, `pgt_flip_ordered`, `pgt_permute`), each of which rewrites only
`common/tradenodes`. There is no per-good-trade DLL, descriptor or emitter. So §1.7's merchant
assignment semantics (Y358–Y362), §1.8's per-good collection and eligibility rules (Y366–Y369,
Y374), §1.10's gate resolution and fallback ladder (Y388–Y390), §1.11's treasure-fleet routing
(Y416–Y417) and §1.12's display behaviour (Y420–Y422, Y425–Y426) all describe behaviour that does
not exist yet. Each would be settled by the same thing: a built mod. Y328 and Y349 are the same case
for `Φ_w`'s installation and its reference-vs-DLL correctness check.

The remaining ones need a source that does not exist rather than a build: Y084 and Y087 need the
**v6.0 spec snapshot** (the tree holds v1–v5 and the current v6.1, nothing between), and Y384's
compounded-rate half needs a save in which some country holds both ship trade power and a
`ship_power_propagation` modifier — none of the four readable saves does, and none can, since every
source of that modifier postdates 1444.

---

**Document integrity.** `per-good-trade-spec.md` was MD5 `59c84a97799db9db97fe889b6e3c6776` before
this audit and `59c84a97799db9db97fe889b6e3c6776` after it. The document did not change under me.


---

# Addendum — follow-up measurements requested by the coordinator

Six questions came back on the report above. Four needed new measurement; those runs are recorded
here, and two verdicts changed as a result (**Y332** PARTIAL → REFUTED, **Y383** CONFIRMED → PARTIAL).
The spec MD5 was re-checked before and after this addendum: `59c84a97799db9db97fe889b6e3c6776`,
unchanged.

## A1 — `epsilon6.py`: the gate cannot fail by construction

Agreed, and the coordinator's diagnosis is more precise than mine. `_UNIT` is captured as
`flowop.mincost_flow`, whose signature is now `mincost_flow(s, c, cost=None)` and which applies unit
costs **only when `cost is None`** — but `drain.phase2` passes `cost=TIE_COST` explicitly. So
`solve(0.0)` does not run a unit-cost Phase 2 at all: it runs the shipped tie-break Phase 2, and the
`eps = 0` gate compares the shipped map to itself. The variable name is also wrong. A gate written to
catch exactly this class of error is structurally incapable of firing.

## A2 — the Scale paragraph: what actually drives the flips

**Do the counts hold at the corrected scales?** Yes, exactly. `/tmp/q2_mech.py` part E:

| scale | flips | free set | sinks |
|---|---|---|---|
| ×10⁻⁶ | 0 | 80 | `genua, hangzhou` |
| ×10⁻⁷ | **22** | 80 | **`english_channel, hangzhou`** |
| ×10⁻⁸ | 24 | 90 | `genua, hangzhou` |
| ×10⁻⁹ | **96** | 159 | **`hangzhou`** |

Both counts and both sink sets are the document's, three orders of magnitude lower. Only the
exponents moved.

**What drives them.** Not `ZERO_TOL`, and not the dual tolerance either. Three separations:

1. **`ZERO_TOL` is entirely innocent.** Set to 1e-14, 1e-17, 1e-20 and **exactly 0**, the answer is
   identical at both scales — ×10⁻⁷ stays 22 flips / free 80, ×10⁻⁹ stays 96 flips / free 159.
   A tolerance of zero cannot be reclassifying anything, so the free set reaching 159 means HiGHS
   returned a flow that is **exactly zero on every edge**.
2. **The primal tolerance is the driver, and it is absolute.** At ×10⁻⁹, `|b_w|max = 3.5e-11`,
   which is *below* the pinned primal feasibility tolerance of 1e-10. The all-zero flow is therefore
   already primal-feasible, and being the cheapest such vector it is what HiGHS returns. Phase 2
   contributes nothing, every edge is free, and the orientation falls entirely to the Phase 3 sweep.
3. **Confirmed by separating the two tolerances** (`/tmp/q2c.py`). At ×10⁻⁷: loosening the
   **primal** tolerance from 1e-10 to 1e-7 collapses the run to 96 flips / free 159; loosening the
   **dual** tolerance over the same range changes nothing (22 flips, free 80). At `b × 1`, loosening
   the primal tolerance all the way to 1e-4 produces **0 flips**, because `|b_w|max = 0.0347` is still
   347× larger.

So there are **two independent failure modes**, and the paragraph conflates them into one wrong one:

- **Dual feasibility tolerance vs the tie-break margin** — `b`-independent. At `b × 1`, loosening
  the dual tolerance to 1e-4 gives 8 flips with the sink set intact. This is the mode `flowop.py`
  already documents correctly (the tie-break margin is as small as 3.8e-8) and the one §2.3's pinning
  to 1e-10 fixed; Y1008's per-good order-invariance depends on it.
- **Primal feasibility tolerance vs `|b|max`** — this is the scale sensitivity §1.6's paragraph is
  actually about. Clean while `|b|max` is a few hundred times the tolerance; partial degradation
  within one to two orders of it; total collapse to the zero flow once `|b|max` drops below it.

A suggested rewrite, if useful: *the premise the implementation adds is that the solver's* primal
*feasibility tolerance is absolute (1e-10, §2.3), so scaling `b` down eventually makes the zero flow
feasible and the LP returns it. Measured: identical orientation from ×1 down to ×10⁻⁶; 22 edge
flips at ×10⁻⁷ where the sink set becomes `{english_channel, hangzhou}`; and at ×10⁻⁹, where
`|b_w|max = 3.5e-11` falls below the tolerance, the LP returns the all-zero flow, all 159 edges go
free and the orientation is decided by the sweep alone (96 flips, sink set `{hangzhou}`). The
zero-flow tolerance `ZERO_TOL = 1e-11` plays no part in this: setting it to zero changes nothing at
any scale. Normalising into (−1, 1) scales 1444's `b_w` up by ~28.8× and is safe; scaling down is
not.*

I'd also drop "the orientation degrades before the sink set does" from that paragraph rather than
restate it — see A3.

## A3 — Y333: delete, don't restate

I agree with the coordinator, and for a second reason beyond the one given. The sentence is false as
stated (both degrade first at ×10⁻⁷), *and* the observation that would replace it points the other
way: at ×10⁻⁸ the sink set is back at `{genua, hangzhou}` while 24 edges are wrong. So the honest
version of the point is not "the orientation degrades first" but "the sink set is a lossy summary of
the orientation — it can be right while the map is wrong." If that is worth keeping, keep *that*,
attached to the ×10⁻⁸ row, and drop the ordering claim entirely. Stating coincident scales and
letting the reader infer is the worst of the three options: it preserves the shape of the false
argument.

## A4 — the European table: option (b), and the headline survives

My view is (b), and I now have the measurement that decides it.

I re-scanned the three disputed regions at **0.0002** (`/tmp/q3_fine.py`), ten times finer than the
0.002 grid that found the errors:

| region | result |
|---|---|
| ×1.355–×1.395 | 4 runs; the row-6 split confirmed at ×1.3620 and ×1.3690 |
| ×1.690–×1.730 | 3 runs; `doab` holds an end over ×1.7018–×1.7092, width 0.0074 |
| ×1.280–×1.300 | 3 runs; the missed interval is ×1.2868–×1.2882, width **0.0014** |
| ×2.000–×2.060 | 1 run — no hidden structure |
| ×1.450–×1.510 | 1 run — no hidden structure |

Two things follow. First, the long runs are genuinely uniform, so the *direction* is robust: the
widest interval on the 0.002 grid is **×1.974–×2.458** (width 0.484), and it is
`english_channel, genua, rheinland` — **three European ends, none in Asia**. The headline survives
intact; only the interval carrying it moves (it was attributed to ×1.38–×1.95, which is now known to
contain `doab`). Second, the narrowest interval keeps shrinking as the grid does — 0.01 → 0.002 found
three new intervals, 0.002 → 0.0002 found one 0.0014 wide. I have no evidence there is a floor, so
any published resolution is refutable by the next auditor with a finer grid. That is the argument
against (a).

So: **(b)**, keeping the two endpoints (`{genua, hangzhou}` at ×1.00; `{genua, rheinland}` by ×2.50)
and the direction, plus the one interval that is load-bearing for §3.1's goal — the widest run, now
correctly ×1.974–×2.458. Nothing else in my slice depends on the row boundaries; Y111's
sub-claims are *about* the boundaries, so they go with the table. If any of the table is kept, the
constancy claim must go regardless, which makes (c) strictly worse than (b) at the same word count.

## A5 — Y119: the surrounding claim survives, both halves understated

- **18-node scaling.** `genua` becomes the sole sink at **×1.51845** (bisected to five decimals) and
  stays the sole sink continuously to ×3.20 — the only non-sole row in a 0.02 sweep from ×1.50 is
  ×1.50 itself, below the onset. So the claim holds; "about ×1.55" should read ×1.52.
- **22-node scaling.** No sole sink below ×4 — and none below **×20** (still `{genua, rheinland}`
  there). True, and understated by more than a factor of five.
- **The eastern four.** No end at any multiplier from ×1.00 to ×20. The clause is my finding to
  delete, agreed. The replacement, if one is wanted, is factual and available: what prevents a sole
  sink is `english_channel` up to about ×3 and `rheinland` from there out past ×20.

## A6 — Y412: option (ii) plus (iii), not (i) — and the list is short by 17, not 9

**No, none of the nine is a direction dependency.** Classified: value (`trade_node_value`,
`add_trade_node_income`), power share (`has_privateer_share_in_trade_node`), membership
(`every/any_trade_node_member_country`, `same_trade_node_as`), scope
(`any/all/random_trade_node`). Zero direction tests. I also swept scripted content for any
upstream/downstream engine token and found none: the only hits are
`zim_dominate_upstream_trade` and its localisation keys in `missions/AFR_Mutapa_Missions.txt` and
`events/flavorZIM.txt` — a mission *name*, whose trigger is ownership, ports, centre-of-trade level,
`is_strongest_trade_power` and `trade_share`. It is the perfect illustration of Y414: named for
vanilla's flow, unable to break, able only to stop meaning what its name says.

**Against (i): the list is longer than either of us thought.** A second sweep for node-scoped engine
constructs whose names do *not* contain `trade_node` — which is why both my first pass and the
document's list missed them — found eight more, none scripted-defined:

| construct | uses | reads |
|---|---|---|
| `trade_share` | 671 | within-node power share |
| `is_strongest_trade_power` | 373 | within-node power comparison |
| `add_trade_modifier` | 293 | writes node trade power |
| `trade_income_percentage` | 146 | value |
| `privateer_power` | 111 | power share |
| `has_trader` | 62 | merchant presence |
| `is_node_in_trade_company_region` | 36 | membership |
| `has_most_province_trade_power` | 8 | power comparison |

That makes the document's four families short by **17** engine constructs, and the exposed surface
roughly **2,100** uses against the ~380 the four families cover. `trade_share` alone is the construct
every threshold in §1.10's own table is written in.

So (i) is the wrong fix: a 21-family enumeration is a maintenance liability that will go stale on the
next patch, and its value is low because the interesting fact is not the roster but the *classes*.
I'd do **(ii) + (iii)**: narrow the claim to what is true — *no scripted content names a trade node,
and nothing in it tests flow direction* — and then add the compatibility note by class, with counts:
value-reading and value-writing constructs (`trade_node_value`, `add_trade_node_income`,
`trade_income_percentage`, ~194 uses) are evaluated against a node economy §2.1 overwrites;
power-share constructs (`trade_share`, `is_strongest_trade_power`, `privateer_power`,
`has_most_province_trade_power`, ~1,163 uses) are evaluated against shares that §1.9's
direction-dependent propagation moves; and `add_trade_modifier` (293) writes into that same
distribution. Direction dependency is genuinely absent, which is the good news and is worth stating
as the measured result it now is.

## A7 — Y383 and Y099: one is weaker than I reported, one holds

**Y383 — I over-reached, and I have downgraded it to PARTIAL above.** Bisecting the threshold over
twenty candidates against the 414 propagated entries:

| threshold | max error | 414-of-414 exact? |
|---|---|---|
| 0 – 5 | 1.0032 | no |
| **6, 7, 8, 9, 9.5, 9.9, 10** | **0.0014** | **yes** |
| 10.1 | 2.016 | no |
| 10.5 – 20 | 2.088 – 3.997 | no |

Every value in `(5.014, 10.038]` fits identically, because the observed downstream `province_power`
values have a gap there (largest below 5.014; smallest above 10.038). So the save **decisively
excludes the no-threshold reading** — that is the real result, and it is worth stating — but it
cannot distinguish 10 from 6, 7, 8 or 9. Recording this as "the threshold is 10, measured" would be
the same species of error as the figures this audit found: a fit reported as a measurement. My
recommendation: state it as *one observation with the method named* — "measured against 414
propagated entries in the 1444 save, the threshold lies in (5.01, 10.04], consistent with
`TRADE_PROPAGATE_THRESHOLD × TRADE_PROPAGATE_DIVIDER = 10`; the no-threshold reading is excluded" —
and keep §3.13's question open, narrowed. Closing it needs a save with a downstream holder inside
the gap.

**Y099 — strong enough to state as measured.** `Φ_ord = Σ_g V_g·order_g`, built from the current
per-good marking orders, orients all 159 edges and scores **59.8% of edge-goods / 59.6%
value-weighted** against `Φ_w`'s 55.1% / 54.8%. The reconstruction matches the document's own
definition at L1636, the comparison is on today's field rather than v5's, and the gap (4.7 points) is
two orders above any rounding. One caveat to carry with it: `Φ_ord` has 14 sinks on this field, so
the operator being compared is not a near-substitute — which is itself the argument §3.9 is making,
and stating the number does not weaken it.

## A8 — the UNTESTABLE verdicts

Agreed, and I'd hold that line firmly. Nine of the twelve §1.7/§1.8 stipulations describe per-good
collection, eligibility and merchant semantics that no shipped artefact implements; "confirmed by
reading the design" would mean confirming the document against itself, which is the exact failure
this audit exists to catch. The one thing I would add: they are not equally far from testable. Y367
(`collected_share`) and Y368 (per-good transfer eligibility) are *formulas* and could be validated
against the reference solver the moment one computes them, without a DLL — which would move them
from UNTESTABLE to a script citation, the same standing as §1.6's figures. Y358–Y361 and
Y420–Y422 cannot move without a build. That distinction may be worth recording in §2.9's build
order.


---

# Addendum 2 — sign-off on the coordinator's proposed edits

Eight items proposed. **Six APPROVED, two APPROVED WITH CORRECTION.** Three needed fresh
measurement; those runs are below. Spec MD5 re-checked: `59c84a97799db9db97fe889b6e3c6776`, unchanged.

| # | Item | Verdict |
|---|---|---|
| 1 | Y333 delete + replacement point | **APPROVE** |
| 2 | Scale paragraph rewrite | **APPROVE WITH CORRECTION** — ×10⁻² is stale, should be ×10⁻⁶ |
| 3 | European table, option (b) | **APPROVE** — quote the interval, with its verification resolution |
| 4 | Y412 (ii)+(iii) by class | **APPROVE WITH CORRECTION** — counts are 2,249 / 425, and the `trade_share` gloss over-reaches |
| 5 | Y119 corrections | **APPROVE** |
| 6 | Y383 one observation, narrowed | **APPROVE** |
| 7 | Y099 state as measured | **APPROVE** |
| 8 | Y367/Y368 in §2.9 | **APPROVE** |

## Item 2 — the correction

`347×` is right: `|b_w|max = 0.034664`, and `0.034664 / 1e-4 = 346.6`. The separation is stated
correctly. But the proposed text opens "identical orientation from ×1 down to **×10⁻²**", which is
the v5-era figure. Re-measured under the shipped solver (`/tmp/chk1.py`):

| scale | ×10⁻¹ | ×10⁻² | ×10⁻³ | ×10⁻⁴ | ×10⁻⁵ | ×10⁻⁶ | ×10⁻⁷ |
|---|---|---|---|---|---|---|---|
| flips | 0 | 0 | 0 | 0 | 0 | 0 | **22** |

The orientation is identical from ×1 down to **×10⁻⁶**. Carrying ×10⁻² into a paragraph whose other
two exponents are being corrected would leave one stale figure of the same species behind, in the
same sentence.

## Item 3 — the two questions

**Should ×1.974–×2.458 be quoted?** Yes, now — I verified it. A full 0.001 scan of the interval
(485 points, `/tmp/chk2.py`) returns **one run**: `english_channel, genua, rheinland` uniform across
×1.9740–×2.4570, with **no non-European end anywhere in it**. That is a materially better-evidenced
claim than the row it replaces: ×1.38–×1.95 was never scanned below 0.01, and the `doab` interval
hiding in it is 0.0074 wide — a 0.001 scan would have caught it. Quote it **with its resolution**
("uniform on a 0.001 grid across its full width"), which is the discipline whose absence broke the
old table. Without that qualifier it is the same kind of claim, just luckier.

**Should the 0.0014 interval be recorded?** Yes, in the document, in one clause. It is the reason no
resolution is publishable as exhaustive, and it is the thing that stops a future editor from
re-deriving a constancy claim from whatever grid they happen to run. Leaving it only in my report
means the next person to touch the section has to rediscover it.

## Item 4 — the counts, and a gloss that over-reaches

Exact counts:

| group | uses |
|---|---|
| four structural families (the document's list) | **425** |
| nine further `trade_node` engine constructs | 124 |
| eight node-scoped constructs without `trade_node` in the name | 1,700 |
| **total** | **2,249** |

So "~2,100" → **2,249**, and "~380" → **425**. By class: value-reading/writing **194**
(`trade_income_percentage` 146, `add_trade_node_income` 28, `trade_node_value` 20); power-share
**1,164** (`trade_share` 671, `is_strongest_trade_power` 373, `privateer_power` 111,
`has_most_province_trade_power` 8, `has_privateer_share_in_trade_node` 1); writes node power
**293** (`add_trade_modifier`); membership/presence 161; scope 12.

**The `trade_share` gloss needs narrowing.** "The construct §1.10's own thresholds are written in" is
true of two of the seven table rows and false of five. Improve Inland Routes and Propagate Religion
are written in `trade_share` (25 occurrences in `common/trading_policies/00_trading_policies.txt`).
The other five — `JUSTIFY_TRADE_CONFLICT_LIMIT`, `JUSTIFY_TRADE_CONFLICT_ACTOR_LIMIT`,
`MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`, `TRADE_COMPANY_STRONG_LIMIT`,
`TRADE_COMPANY_CONTROL_LIMIT` — appear in **0** script files: they are engine-internal and are not
expressed in any scripted construct. The accurate form: *`trade_share` is the construct the two
trading-policy rows of §1.10's table are written in, and it is the single most-used node-scoped
construct in the game's scripted content at 671 uses.*

## The outside question — Φ_ord vs Φ_w under sweep-key variation

It does **not** change anything I concluded about `Φ_w`'s stability. My conclusions are each about
invariance to a *named* perturbation, measured directly: relabelling (0 of 159 edges over 220
permutations), ±1% wealth noise (0 edges over six seeds), and scaling (now correctly characterised).
None of them depends on the same instrument also discriminating between operators. My instrument's
sensitivity was already established by its own positive controls — the unit-cost configuration moves
26 of 159 edges on the identity, 40 of 40 permutations return different supports, and per-good
config B moves 81–95 of 290 runs.

But I re-ran it rather than take it on trust, because Y084 ("both are properties of the world") sits
in my slice. Holding labels fixed and varying only the sweep key (`/tmp/chk1.py`):

| sweep key | ends | sink set | edges moved vs shipped |
|---|---|---|---|
| `defasc_beta` (shipped) | 2 | `genua, hangzhou` | 0 |
| `def_beta` | 2 | `genua, hangzhou` | **35** |
| `def_absb` | 2 | `genua, hangzhou` | **39** |
| v2-style scan-order sweep | 2 | `genua, hangzhou` | **25** |
| 20 random `pid` tie-breaks | 2 | `genua, hangzhou` × 20 | — |

**One qualification the §3.9 write-up should carry.** `Φ_w`'s *sink set* is robust to sweep-key
variation — two ends, the same two nodes, in all 24 configurations tried, against `Φ_ord`'s
14 / 8 / 8. That contrast is real and is worth stating. But `Φ_w`'s *orientation* is **not** robust to
it: 25 to 39 of 159 edges move. Nothing in §1.6 claims otherwise — the section claims order-invariance,
which holds — so no verdict in my slice changes. The risk is only in how the contrast gets written:
"Φ_w stays at 2 throughout" is true, and "Φ_w is stable under sweep-key variation" would be the same
species of over-claim as the two I retracted. The sweep key is a design choice in `drain.py`
(`deterministic=True`), not a world property, and up to a quarter of the installed map depends on it.

## Item 8 — record the distinction

Yes, record it. Y367 (`collected_share`) and Y368 (per-good transfer eligibility) are formulas over
quantities the reference solver already has; a script that computes them would move both from
UNTESTABLE to a script citation with no DLL involved, the same standing as §1.6's figures. Y358–Y361,
Y420–Y422 and Y425–Y426 cannot move without a build. Recording that in §2.9 turns a flat block of 32
unverifiable claims into two, and the smaller one is cheap to clear.

---

# Addendum 3 — response to the final proposal

**Not unconditional.** Seven of the nine items are correct as written. Two are not, and one of the
two is a defect created by items 1 and 2 interacting. Spec MD5 re-checked:
`59c84a97799db9db97fe889b6e3c6776`, unchanged.

## Item 2 — the `ZERO_TOL` sentence is false at ×10⁻⁸

The proposed closing sentence reads: *"`ZERO_TOL` is not involved: setting it to exactly 0 leaves the
flip count, the free-set size and the sink set unchanged at **every scale**."*

I had only ever tested that at ×1, ×10⁻⁶, ×10⁻⁷ and ×10⁻⁹ — the scales the paragraph quotes. I had
not tested ×10⁻⁸, which is the one scale where the free set is neither 80 nor 159 and therefore the
only one where `ZERO_TOL` has room to act. Measured now (`/tmp/chk3.py`):

| scale | `ZERO_TOL` = 1e-11 | `ZERO_TOL` = 0 |
|---|---|---|
| ×1 | 0 flips, free 80 | 0 flips, free 80 |
| ×10⁻⁶ | 0 flips, free 80 | 0 flips, free 80 |
| ×10⁻⁷ | 22 flips, free 80 | 22 flips, free 80 |
| **×10⁻⁸** | **24 flips, free 90** | **26 flips, free 85** |
| ×10⁻⁹ | 96 flips, free 159 | 96 flips, free 159 |

At ×10⁻⁸ the flip count and the free-set size both move. The sink set does not. So the universal is
false, and it is false **precisely at the scale item 1 introduces into the document** — item 1's
replacement sentence quotes the ×10⁻⁸ row, so as proposed the two edits would put a universal claim
and its counterexample in the same section.

Correct forms, either is fine:

- *`ZERO_TOL` is not what drives this: setting it to exactly 0 leaves the flip count, the free-set
  size and the sink set unchanged at every scale quoted here.* (True: ×1, ×10⁻⁶, ×10⁻⁷, ×10⁻⁹.)
- Or keep the universal and state the exception: *…unchanged at ×1, ×10⁻⁶, ×10⁻⁷ and ×10⁻⁹; at ×10⁻⁸
  it moves the flip count from 24 to 26 and the free set from 90 to 85, leaving the sink set alone.*

The paragraph's substantive claim — that the primal tolerance and not `ZERO_TOL` is the mechanism
behind the 22 and the 96 — is unaffected and stands.

## Item 3 — one scoping word

"×1.974–×2.457 is the widest interval" does not say widest *over what range*. With the table dropped
the reader no longer has ×1.00–×2.50 in front of them, and an unscoped superlative is not checkable.
Suggest "the widest interval over ×1.00–×2.50". The claim itself is sound: it is 0.001-verified
across its full width, and because refinement can only split runs and make them smaller, no finer
grid can promote a different run past it.

## The §1.6 question — yes, and it is more load-bearing there than in §3.9

I measured it rather than judging it. Holding labels and every input fixed and changing only the
sweep key, **seven of the seventeen facts §1.6 quotes about the installed graph change**
(`/tmp/chk4.py`):

| quoted fact | shipped `defasc_beta` | `def_beta` | `def_absb` | scan-order |
|---|---|---|---|---|
| sources | **5** | 10 | 10 | 7 |
| source `c_w` ranks | **55–79** | 40–76 | 37–76 | 37–76 |
| source mean degree | **2.4** | 2.6 | 2.6 | 2.6 |
| Cape ordered pairs | **81** | 42 | 42 | 63 |
| Europe→sink pairs | **27** | 26 | 26 | 26 |
| northern route | **11 hops via the steppe** | 6 hops via Manchuria | 6 hops | 6 hops |
| Iberian route | **11 hops via the Red Sea** | **no route** | **no route** | **no route** |

Unchanged in all four: the sink set (`genua, hangzhou`), `genua`'s out-degree 0 / in-degree 5 and its
five in-neighbours, `english_channel → champagne → genua`, the Cape's in- and out-sets, 0 Europe→sink
routes via the Cape, acyclicity, and 159/159 oriented.

Two of the casualties are the section's signature exhibits. The northern route becomes
`white_sea → novgorod → kazan → siberia → girin → beijing → hangzhou` — Manchuria, not the Volga and
the Silk Road. **The Iberian route ceases to exist entirely.** These sit directly under §1.6's
heading *"And the 1444 map draws the pre-Columbian trade geography unprompted"* — which is true of
the shipped operator and not true of the operator with a different sweep key.

Nothing in §1.6 is thereby wrong. Its L524 claim is about the **node order**, and node order changes
none of this (0 of 159 edges over 220 relabellings). But the section frames the question as a binary
— world-property versus ordering-artifact — and the sweep key is a third category that the binary
hides: a design choice in `drain.py`, neither the world nor the numbering. A reader of §1.6 alone
would reasonably conclude the Volga route is something the 1444 field produces. It is something the
field *and* `deterministic=True` produce together.

So: yes, it belongs in §1.6, and it should say more there than in §3.9. §3.9 needs it as a contrast
between two operators. §1.6 needs it as a scope statement on its own figures — something like *the
five sources, the two route chains and the Cape's 81 pairs are properties of the field under the
sweep key §2.3 fixes; a different key leaves the sink set, `genua`'s degrees and the Cape's in- and
out-sets alone but moves 25–39 of 159 edges and both route chains.* Put next to L524's node-order
paragraph, that closes the gap the binary opens.

None of my verdicts change. Every figure I confirmed reproduces exactly under the shipped
configuration, which is what the document describes, and the document nowhere claims key-invariance.
This is a scope qualification, not a refutation — but it is the same class of gap as the two
over-claims retracted earlier today, and it is cheaper to close now than after a reader has built on
it.

---

# Addendum 4 — response to the resent proposal

**REJECTED**, on item 2 only. Items 3 and 16 are correct as resent. The rejection is the same defect
one level down: the replacement sentence swapped a false universal for a false uniqueness claim.

## Item 2 — ×10⁻⁸ is not "the one scale"; it is a band

The resent text says *"at ×10⁻⁸, **the one scale** where the free set is neither 80 nor 159 and the
tolerance therefore has room to act…"*. I had only ever sampled a decade grid, so I could not have
supported that and should have said so last round. Sampled between the decades (`/tmp/chk5.py`,
shipped tolerances, flips against the ×1 baseline):

| scale | free @ 1e-11 | free @ 0 | flips @ 1e-11 | flips @ 0 |
|---|---|---|---|---|
| ×10⁻⁶ | 80 | 80 | 0 | 0 |
| ×3·10⁻⁷ | 80 | 80 | 17 | 17 |
| ×10⁻⁷ | 80 | 80 | 22 | 22 |
| ×7·10⁻⁸ | **81** | 80 | 24 | 22 |
| ×5·10⁻⁸ | **84** | 81 | 9 | 10 |
| ×3·10⁻⁸ | **83** | 81 | 14 | 16 |
| ×2·10⁻⁸ | **85** | 82 | 13 | 15 |
| ×10⁻⁸ | **90** | 85 | 24 | 26 |
| ×7·10⁻⁹ | **89** | 81 | 30 | 35 |
| ×5·10⁻⁹ | **91** | 81 | 44 | 50 |
| ×3·10⁻⁹ | **140** | 138 | 82 | 81 |
| ×2·10⁻⁹ | 159 | 159 | 96 | 96 |
| ×10⁻⁹ | 159 | 159 | 96 | 96 |

The free set is intermediate at **eight** of the thirteen scales tested — a band running roughly
×7·10⁻⁸ down to ×3·10⁻⁹, about one and a half decades — and `ZERO_TOL` changes the answer at every
point inside it, not only at ×10⁻⁸. The flip count inside the band is also non-monotone (24, 9, 14,
13, 24, 30, 44, 82), so it is not a clean progression from "clean" to "collapsed".

The paragraph's explanatory point is sound in kind and wrong in extent: `ZERO_TOL` acts exactly where
the free set is intermediate, and that is a band rather than a point. A correct form:

> *`ZERO_TOL` is not what drives these: at ×10⁻⁷ and ×10⁻⁹ setting it to exactly 0 leaves the flip
> count, the free-set size and the sink set unchanged. It is not inert everywhere — across roughly
> ×7·10⁻⁸ to ×3·10⁻⁹, where the free set is intermediate rather than 80 or 159, zeroing it moves the
> flip count at every scale sampled (at ×10⁻⁸, 24 flips and 90 free edges become 26 and 85) — but
> that band lies between the two scales this paragraph quotes, and it moves neither of them.*

Note the band sits **between** ×10⁻⁷ and ×10⁻⁹, not below both.

## Item 16(a) — no ratio; the resent text is already right

Do not add "of seventeen". Seventeen is a denominator I chose for a checkable-facts list that the
document does not define, and the next auditor would pick a different one and get a different ratio.
The resent paragraph says "seven of the figures this section quotes" and then itemises all seven in
the same sentence, so the count is self-verifying from the list and needs no denominator. One
constraint that follows: if the list is trimmed in editing, the numeral must be trimmed with it, or
it becomes an unsupported count over an unstated set — the same defect, smaller.

## Item 16(b) — yes, and the two routes are not equally affected

The section presents them as a matched pair. They are not. Measured across the three non-shipped
keys:

- **The northern route survives in existence but not in path.** It is still `white_sea → … →
  hangzhou` under every key, but under all three others it runs `white_sea → novgorod → kazan →
  siberia → girin → beijing → hangzhou` — six hops through Manchuria, not eleven through Samarkand,
  Lahore and the Ganges. The Volga-and-steppe reading is a property of the shipped key.
- **The Iberian route does not survive at all.** Under all three other keys `sevilla` reaches
  `hangzhou` by no directed path whatever. It is not a different road to the same place; the
  connection is absent.

So §1.6 should do three things. Attribute both routes to the shipped key, not to the field alone.
Mark the Iberian one as the stronger case, because "no counterpart under the other keys" is a
different order of dependence from "a different path". And qualify the heading: *"the 1444 map draws
the pre-Columbian trade geography unprompted"* claims emergence from the field, and what is measured
is emergence from the field **and** `deterministic=True` together — it holds at one of the four keys
tried. "Unprompted" is the word doing the work, and it is the word the measurement does not support.

---

# Addendum 5 — answer to "is there another unmeasured scope in item 2?"

**Yes, two — and REJECTED again.** The phrase you asked about survives. Two others in the same
sentence do not, and the second exposes something the paragraph's whole narrative shape gets wrong.

## The phrase you asked about is fine

"Identical orientation from ×1 down to ×10⁻⁶" was a decade-grid claim, so I sampled five points per
decade (×1, ×7·10⁻¹, ×5·10⁻¹, ×3·10⁻¹, ×2·10⁻¹, and the same pattern through every decade) —
**31 scales, 0 flips and `{genua, hangzhou}` at every one**. The claim is true and is now verified
between the decades as well as on them. Good instinct; it just happens to hold.

## What does not: the two "where … becomes" clauses

Both assert a *transition* at a decade row. Neither transition is there.

| scale | flips | sinks |
|---|---|---|
| ×10⁻⁶ | 0 | `genua, hangzhou` |
| ×7·10⁻⁷ | **2** | `genua, hangzhou` |
| ×5·10⁻⁷ | 2 | `genua, hangzhou` |
| ×4·10⁻⁷ | 2 | `genua, hangzhou` |
| ×3·10⁻⁷ | 17 | `english_channel, hangzhou` |
| ×10⁻⁷ | 22 | `english_channel, hangzhou` |
| ×5·10⁻⁹ | 44 | `hangzhou` |
| ×4·10⁻⁹ | 72 | **`genua`** |
| ×3·10⁻⁹ | 82 | **`gulf_of_siam, nippon`** |
| ×2.5·10⁻⁹ | 96 | `hangzhou` |
| ×10⁻⁹ | 96 | `hangzhou` |

**First clause.** The orientation first moves at **×7.1·10⁻⁷** (bisected; 2 flips, sink set still
baseline), and the sink set changes at **≈×3.9·10⁻⁷** (bisected: `{genua, hangzhou}` holds to
×3.873·10⁻⁷). Neither is ×10⁻⁷. At ×10⁻⁷ both facts are *true* — 22 flips, that sink set — but
"where it becomes" says the change happens there, and it happened two and a half times higher.

**Second clause, and this is the serious one.** The sink set below ×10⁻⁶ is **not monotone**. Going
down it runs `{genua, hangzhou}` → `{english_channel, hangzhou}` → `{hangzhou}` at ×5·10⁻⁹ →
**`{genua}`** at ×4·10⁻⁹ → **`{gulf_of_siam, nippon}`** at ×3·10⁻⁹ → `{hangzhou}` from ×2.5·10⁻⁹
down. Two of those sets share no member with either endpoint, and `nippon` and `gulf_of_siam` are
ends that appear nowhere else in this section. "96 at ×10⁻⁹ where it becomes `{hangzhou}`" describes
a single settling; what happens is an excursion through two unrelated sink sets and back.

## What this means for the paragraph's shape, not just its wording

The narrative is clean → 22 flips → 96 flips, two steps. The measurement is a progressive,
non-monotone collapse across roughly two decades, of which the two quoted rows are **samples, not
boundaries**. That is the same defect as "every scale" and "the one scale", one level up: the decade
grid is being read as structure.

Minimal fix — drop the transition verbs and add one clause:

> …identical orientation from ×1 down to ×10⁻⁶ (verified five points per decade); at ×10⁻⁷ the map
> is **22** edge flips from the baseline with sink set `{english_channel, hangzhou}`, and at ×10⁻⁹ it
> is **96** with sink set `{hangzhou}`. *These are samples of a progressive collapse, not its
> boundaries: the orientation first moves at ×7.1·10⁻⁷, the sink set first changes at ×3.9·10⁻⁷, and
> between ×5·10⁻⁹ and ×2.5·10⁻⁹ it passes through `{genua}` and `{gulf_of_siam, nippon}` before
> settling.*

Everything else in the resent item 2 is measured and correct: the primal-versus-`|b|max` mechanism,
`|b|max = 3.5e-11` below 1e-10 at ×10⁻⁹, all 159 free, the primal/dual separation at ×10⁻⁷, the
347× at ×1, and the `ZERO_TOL` band `×7·10⁻⁸`–`×3·10⁻⁹` lying between the two quoted scales and
moving neither. The `at every scale sampled` hedge in the `ZERO_TOL` clause is correctly scoped and
should stay exactly as worded.

---

# Addendum 6 — (a) the band is fine; (b) keep the names; and one word of mine is wrong

**REJECTED**, on a word I supplied myself last round.

## (a) The band does not need a further hedge — it needed a bisection, which it now has

Two things to separate. **Contiguity:** verified. Sampled at 20 scales from ×1.2·10⁻⁷ to
×1.5·10⁻⁹, the free set is 80 at ×1.2·10⁻⁷, ×10⁻⁷, ×9·10⁻⁸ and ×8·10⁻⁸; intermediate continuously
from ×7·10⁻⁸ to ×3·10⁻⁹; and 159 at ×2.5·10⁻⁹ and below. It never returns to 80 inside. "Band" is
the right word.

**Extent:** my first attempt at the edges used inverted brackets — it assumed ×9·10⁻⁸ was
intermediate when the free set there is 80 — so both figures it produced were artifacts of a bad
bracket and I discarded them. Re-bisected from verified brackets (×8·10⁻⁸ not intermediate,
×7·10⁻⁸ intermediate; ×3·10⁻⁹ intermediate, ×2.5·10⁻⁹ not):

- **upper edge ×7.099·10⁻⁸** — free is 80 above it, intermediate below
- **lower edge ×2.885·10⁻⁹** — intermediate above it, 159 below

So "roughly ×7·10⁻⁸ to ×3·10⁻⁹" is correct as written: the upper edge is ×7.1·10⁻⁸, and ×3·10⁻⁹ is
a conservative statement of a lower edge at ×2.885·10⁻⁹. **No hedge change needed**, and the
"at every scale sampled" clause inside it should stay exactly as worded.

## The rejection: "progressive" is wrong, and it is my word

The denser sample shows the flip count below ×10⁻⁶ is not a progression at all:

| scale | ×10⁻⁷ | ×8·10⁻⁸ | ×7·10⁻⁸ | ×6·10⁻⁸ | ×5·10⁻⁸ | **×4·10⁻⁸** | ×3·10⁻⁸ | ×2·10⁻⁸ | ×10⁻⁸ | ×7·10⁻⁹ | ×5·10⁻⁹ | ×4·10⁻⁹ | ×3·10⁻⁹ | ×2.5·10⁻⁹ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| flips | 22 | 22 | 24 | 9 | 9 | **6** | 14 | 13 | 24 | 30 | 44 | 72 | 82 | 96 |

At **×4·10⁻⁸ the map is 6 flips from baseline** — nearly four times *closer* to the true orientation
than at ×10⁻⁷, which is a hundredfold larger `b`. The sequence is not monotone anywhere in the
middle, and ×10⁻⁷'s 22 is not even a local landmark: ×8·10⁻⁸ gives 22 as well.

I wrote "samples of a progressive collapse" last round and it is the same defect as the three
before it — a shape asserted over a range I had sampled at one point per decade. Corrected:

> *These are samples of a non-monotone region, not boundaries of a progression: the orientation first
> moves at ×7.1·10⁻⁷ and the sink set first changes at ×3.9·10⁻⁷, but between ×10⁻⁷ and ×2.5·10⁻⁹
> the flip count wanders rather than climbing — it falls to 6 at ×4·10⁻⁸, closer to the baseline
> than ×10⁻⁷'s 22, before rising to 96 — and the sink set passes through `{genua}` and
> `{gulf_of_siam, nippon}` on the way.*

## (b) Keep the names, and inoculate in the same clause

Keep them. "Two other sink sets" is the unverifiable summary this audit exists to catch; naming them
is what makes the claim checkable, and they are the evidence for the non-monotonicity.

The reconciliation risk is real but it is answered by a fact I can supply: **at ×3·10⁻⁹ the free set
is 140 of 159 — 88% of the map is oriented by the sweep alone, with almost no flow information
left.** Put that in the same clause and `nippon` cannot be mistaken for a candidate end; it is
visibly the output of a Phase 2 that has stopped solving. Something like *…passes through `{genua}`
and `{gulf_of_siam, nippon}` — sink sets of a solve with 88% of its edges unoriented by flow, not
ends the field produced.*

That also does work the paragraph needs anyway: it tells the reader what "the sweep decides alone"
costs, which is otherwise only asserted at ×10⁻⁹ where the figure is 100%.

---

# Addendum 7 — "wanders" survives; the sink-set enumeration beside it does not

**REJECTED.** Not on the word you asked about — that one is now verified. On the clause immediately
after it, which is the fifth shape asserted from a sample.

## "Wanders" is supported, and here is why the question had a real answer

I resampled the region at 29 points over ×10⁻⁷ to ×2.5·10⁻⁹ (`/tmp/chk10.py`), roughly one point per
7% step. My own suspicion going in was that the region was two regimes — one downward excursion, then
a monotone climb — which would have made "wanders" wrong for the lower half. **It is not.**

- **11 of 28 steps are decreases**, and they are distributed across the whole region, not
  concentrated in one dip: ×7.36·10⁻⁸→×6.31·10⁻⁸ (22→9), ×5.41·10⁻⁸→×4.64·10⁻⁸ (9→6),
  ×2.15·10⁻⁸→×1.85·10⁻⁸ (30→9), ×1.36·10⁻⁸→×10⁻⁸ (31→28→24), ×8.99·10⁻⁹→×6.53·10⁻⁹ (32→28→26→23),
  ×5.87·10⁻⁹→×4.74·10⁻⁹ (45→44→43), ×4.26·10⁻⁹→×3.83·10⁻⁹ (74→72).
- **The lower stretch is not monotone either.** From ×10⁻⁸ down: 24, 32, 28, 26, 23, 45, 44, 43, 74,
  72, 72, 75, 96, 96. The two-regime hypothesis is refuted.

"Wanders" is also the right strength of claim: non-monotonicity is existential, so a counterexample
settles it, and I have eleven. Unlike "progressive", more sampling can only add decreases. Keep it.

## What must go: "the sink set passes through `{genua}` and `{gulf_of_siam, nippon}`"

At 29 points the sink set takes **six** distinct values, not two:

| sink set | points |
|---|---|
| `{genua, hangzhou}` — **the baseline** | **12** |
| `{hangzhou}` | 7 |
| `{english_channel, hangzhou}` | 5 |
| `{genua}` | 3 |
| `{genua, gulf_of_siam, wien}` | 1 |
| `{gulf_of_siam}` | 1 |

Three problems with the clause as written. It names two sets where there are at least six. Two of
the six — `{genua, gulf_of_siam, wien}` at ×4.74·10⁻⁹ and `{gulf_of_siam}` alone at ×3.09·10⁻⁹ — are
not mentioned, and `wien` is a node that appears nowhere in this discussion. And
`{gulf_of_siam, nippon}` does not appear at **either** neighbouring sample point in this denser
sweep (×3.44·10⁻⁹ gives `{genua}`, ×3.09·10⁻⁹ gives `{gulf_of_siam}`) — it is a feature narrower than
a 7% step, so quoting it as one of two waypoints presents the narrowest thing in the region as
typical of it.

## The form that ends this

The distinction that has been missing for five rounds is between **exact characterisations**, which
denser sampling refutes, and **lower bounds**, which denser sampling can only strengthen. Every
failure in this paragraph has been the first kind. Recast the clause as the second:

> *…the flip count wanders rather than climbing — 11 of 28 sampled steps are decreases, and it falls
> to 6 at ×4·10⁻⁸, closer to baseline than ×10⁻⁷'s 22, before rising to 96 — and the sink set takes
> **at least six** distinct values across 29 sampled scales, including the baseline
> `{genua, hangzhou}` at 12 of them and, at ×3·10⁻⁹, sets from a solve with 88% of its edges
> unoriented by flow.*

"At least six across 29 sampled scales" cannot be refuted by a finer grid, only raised. It drops the
named waypoints, which is what your own fallback proposed, while keeping the evidence for
non-monotonicity that made naming them attractive.

## One thing worth promoting rather than cutting

**The baseline sink set `{genua, hangzhou}` recurs at 12 of the 29 points inside the degenerate
region** — at ×6.31·10⁻⁸, ×1.85·10⁻⁸, ×10⁻⁸ and nine others, while 6 to 31 edges are wrong. That is
a stronger statement of item 1's replacement point than the ×10⁻⁸ row alone: the sink set is not
merely occasionally right while the map is wrong, it is right at **41% of sampled scales** inside a
region where the solver has stopped solving. If any single figure from this whole exchange belongs in
§1.6, it is that one.

---

# Addendum 8 — two defects in the final item 2, one of them mine

**REJECTED.** The mechanism sentence is correct and I confirmed it last round. Two other clauses are
not, and the first is wording I supplied without checking.

## 1. "The sign pattern is read once, in Phase 4" — my error

I proposed that phrasing to replace "Phase 0 reads signs". I checked that Phase 0 does not read the
sign; I did not check that Phase 4 was the only place that does. It is not. `drain.py` reads it in
**five places across three phases**:

| line | phase | read |
|---|---|---|
| 53 | **Phase 1** | `Dset = [v for v in core if beta[v] < 0]` — selects the demander set |
| 196, 198 | **Phase 3** | `DEF[v] = max(0.0, -beta[v]) + …` — clamps negatives in the sweep key |
| 271, 283 | **Phase 4** | `directed.append((v, u) if bv >= 0 else (u, v))` — orients peeled edges |

"Once" is a scope assertion made without sampling the scope, which is the same error class as the
four before it, and this time I introduced it rather than caught it. The conclusion is untouched —
every one of the five reads is invariant under positive scaling, so the scale argument holds — but
the sentence states a fact about the implementation that the implementation contradicts.

Correct form:

> *…the sign pattern is read in Phase 1's demander set, Phase 3's `DEF` key and Phase 4's peeled-edge
> orientation, and all three are invariant under positive scaling; Phase 1's HHI is built from mass
> shares; the LP optimum scales linearly with identical net-flow signs; and the priority key is
> order-isomorphic under positive scaling.*

## 2. "Either scale `b` up, or scale the tolerance with it" — the second option does not exist

The shipped tolerance is **already at HiGHS's floor**. Tested directly:

| tolerance | accepted? |
|---|---|
| 1e-9 | yes |
| **1e-10** | **yes — the floor, and the shipped value** |
| 1e-11, 1e-12, 1e-14, 1e-16 | **rejected: `Invalid option value`** |

`flowop.py` says so in its own comment — *"At 1e-10 (HiGHS's floor for these options)"* — so the
document is offering an option its own solver notes rule out.

It is worse than merely unavailable. A rejected tolerance **does not raise**: HiGHS emits an
`OptimizeWarning`, `res.success` stays `True`, and the solve silently falls back to the **1e-7
default** — three orders *looser* than the pinned setting. An implementer following this advice makes
the problem worse than doing nothing, and gets a successful-looking result. I hit this myself earlier
in this audit: a test that tried to scale the tolerance with `b` returned 96 flips at ×10⁻⁶, which I
initially read as a finding before noticing the warning.

Correct form:

> **Do not scale `b` down. Scale it up.** *The tolerance cannot be scaled down to compensate: 1e-10 is
> HiGHS's floor for these options, and any smaller value is rejected with `Invalid option value`,
> leaves `success` true, and silently reverts to the 1e-7 default — three orders looser than the
> pinned setting, so the attempted fix makes the failure worse and hides it.*

## Everything else in the final text is verified

The mechanism sentence — absolute **primal** tolerance, the all-zero flow becoming feasible and being
optimal because every arc cost is strictly positive and `f ≥ 0`, Phase 2 contributing nothing, the
sweep deciding alone — is correct, needs no figure, and the singular "primal" is the right precision.
`|b_w|max = 0.034664` → 0.0347, and it is what makes "normalising scales it *up*" checkable (factor
28.8). Phase 1's HHI from mass shares, the LP scaling linearly, and the order-isomorphic priority key
are all as verified under Y331.

---

# Addendum 9 — the deletion is right; the dependency list is short by one

**REJECTED as scoped**, not on the deletion. Delete the paragraph. But §3.13 also depends on it, and
in a way a cross-reference sweep would not surface, because the dependency is a *fact* rather than a
pointer.

## (a) A third dependency: §3.13 line 1764

> - **The zero-flow tolerance is scale-coupled.** §2.3 now records it as absolute rather than purely
>   numerical — v2.1 filed it as numerical-only — and being absolute is what makes it interact with
>   the magnitude of `b` (§1.6). Either normalise `b` to a fixed scale before the solve or make the
>   tolerance relative. Undecided.

Three problems, and deleting §1.6's paragraph makes all three worse rather than better:

1. **The stated mechanism is refuted.** The zero-flow tolerance is *not* what couples to the scale of
   `b`. Setting `ZERO_TOL` to exactly 0 leaves the flip count, the free-set size and the sink set
   unchanged at ×10⁻⁷ and ×10⁻⁹. The coupling is to the **primal feasibility** tolerance.
2. **The dangling reference is to the only place this was stated.** With §1.6's paragraph gone, the
   "(§1.6)" points nowhere and the claim has no support anywhere in the document.
3. **One of its two proposed remedies does not exist.** "Make the tolerance relative" — if that means
   the LP tolerance, 1e-10 is HiGHS's floor and a smaller value is rejected with `Invalid option
   value`, leaves `success` true, and silently reverts to 1e-7. This is the same bad advice I
   rejected in item 2, surviving in a second location.

Left as-is, §3.13 would be the only remaining statement of a mechanism this audit refuted, with a
broken pointer and an unavailable remedy — a worse residue than the paragraph being deleted.

**Recommendation: close it rather than delete it.** This round answered it. The coupling is real, it
is the primal tolerance not the zero-flow tolerance, the margin is 8.6 orders (below), and one of the
two remedies is unavailable. §3.13 is the register of open questions; converting an "Undecided" to a
settled entry is worth more than dropping it, and dropping it silently loses the record that it was
answered rather than abandoned. If the design owner wants zero residue on the topic, deleting is
defensible — but not leaving it standing.

**§1.1's Phase 0 is not a dependency.** It states the sign read itself — *"orienting each pendant edge
by the sign of its absorbed subtree balance"* — so it is self-contained and loses nothing. (Separately
and outside my slice: §1.1 describes Phase 0 as doing that orienting, while `drain.py` defers it to
`compile_dirs` in Phase 4. Specification-versus-implementation split, not an error, but it is the
same discrepancy I recorded under Y331 and whoever owns §1.1 may want it.)

## (b) The hazard is not reachable — agree, delete the warning

Measured across the aggregate and all 29 per-good balance vectors:

| vector | `\|b\|max` | multiple of the 1e-10 tolerance |
|---|---|---|
| aggregate `b_w` | 0.0347 | **3.47·10⁸** |
| `grain` (smallest per-good) | 0.0368 | 3.68·10⁸ |
| `cloves` (largest) | 0.980 | 9.8·10⁹ |

The aggregate `b_w` is the closest thing in the entire shipped model to the hazard, and it sits
**8.6 orders of magnitude** above it. Nothing per-good comes nearer.

And it is structural, not incidental. `b_w = 1/N − c_w`, so the uniform supply term alone puts the
scale at `1/N = 0.0125` for N = 80; reaching 1e-10 would need every node's `c_w` to equal `1/N` to
within 1e-10, or a map of order 10¹⁰ nodes. An implementer does not arrive here by accident — they
arrive by deliberately rescaling `b`, which is the one thing the document would have been warning
them about.

So: no reachable hazard, no warning needed, and the figures were never load-bearing. Delete.

## Verdict

Delete lines 487–497 and the §2.3:1026 cross-reference as proposed, **and resolve §3.13:1764** — close
it with what was measured, or delete it, but do not leave it. With that, my slice is closed.

---

# Addendum 10 — (a) confirmed; (b) reintroduces the obligation, and one figure is already wrong

## (a) The deletion — CONFIRMED

Lines 487–497 and the §2.3:1026 reference. Nothing further depends on them; the hazard measurement
stands.

## (i) Yes, the closure as drafted reintroduces the obligation — and worse

**None of the three figures is guarded.** `verify6.py` anchors 37 checks, and `0.0347` is among them
at :97 and :143 — via computed needles (`shows(doc, "largest b_w", "**{:.4f}**", O["largest |b_w|"])`),
which is why it survives at §1.6:546. But **8.6 orders**, **1/N = 0.0125** and the **1e-10 floor** are
guarded by nothing. Adding three unguarded figures to close a question is the same trade the deletion
was meant to end.

**And "8.6" is already imprecise.** For the aggregate `b_w` at α_Φ = 2.0 the margin is
log₁₀(0.0346639 / 1e-10) = **8.5**, not 8.6. The 8.6 is my figure for `grain` (0.0367623), which I
quoted in Addendum 9 for the smallest per-good vector and which has been carried across to the
aggregate. It also moves with α_Φ:

| α_Φ | 1.0 | 1.5 | 2.0 | 3.0 | 4.0 | 8.0 |
|---|---|---|---|---|---|---|
| `\|b_w\|max` | 0.0173 | 0.0225 | 0.0347 | 0.0917 | 0.194 | 0.725 |
| orders above 1e-10 | 8.2 | 8.4 | **8.5** | 9.0 | 9.3 | 9.9 |

So a figure stated as "8.6" is wrong at every α_Φ in the document's own sensitivity range, including
the shipped one.

**There is a form that carries the same force with nothing to re-derive.** The margin has a structural
floor that does not depend on α_Φ, on the field, or on any measurement: at least one node carries
`c_w < 1e-6`, so for that node `|b_w| = 1/N − c_w ≈ 1/N`, and therefore

> `|b|max ≥ 1/N` whenever any node holds negligible wealth — which is **more than eight orders above
> the tolerance** for N = 80, and stays above eight orders for any map below ~10⁸ nodes.

That is a bound rather than a measurement. It cannot go stale on a re-run, a different α_Φ, a later
save or a modded map, because it depends only on N and on the existence of one poor node. It needs no
guard in `verify6.py` — which is the property the three drafted figures lack.

**Recommendation:** take the qualitative form you offered — coupling is to the primal tolerance,
hazard unreachable, one remedy unavailable — with that single structural bound in place of the three
figures. Keep the `Invalid option value` mechanism verbatim: it is a solver behaviour, not a field
measurement, and it is the part an implementer can act on.

## (ii) Do not reopen part 1's slice — this is a note, not a correction

I checked what §1.1 actually says before answering. **§1.1 already attributes the un-peel to Phase 4**:
*"**Phase 4 — un-peel** the Phase-0 pendants in reverse"*, and its own T1 worked example says
*"Phase 4 restores the edge B→C"*. So the document is internally coherent and matches `drain.py`,
where `compile_dirs` does the sign read.

That leaves Phase 0's *"orienting each pendant edge by the sign of its absorbed subtree balance"* as a
statement of **the rule** — by what the orientation is determined — rather than of **the timing**.
Read that way it is not an error at all, and §1.1 is a specification of a five-phase operator, which
is entitled to decompose the bookkeeping differently from the implementation so long as the output
matches; §2.8's correctness check is exact orientation equality, which is output-level.

The only place the attribution was load-bearing was the Scale paragraph's "Phase 0 reads signs"
enumeration, which is being deleted. With that gone it drops from a defect to a phrasing preference.

So: **preconfirmation note, not a batch fix.** Reopening a confirmed slice to change defensible
phrasing costs a round and invites exactly the churn this paragraph has just cost. If preconfirmation
reads it as ambiguous, part 1 can decide then — it is their section and they may have chosen the
phrasing deliberately.

---

# Addendum 11 — (a) confirmed; (b) rejected, twice, both from compression

**(a) CONFIRMED.** Lines 487–497 and the §2.3:1026 reference. **(ii) agreed** — preconfirmation note.

**(b) REJECTED.** Two defects, and neither was in the longer draft. Both were created by shortening it.

## 1. "Setting `ZERO_TOL` to exactly 0 changes nothing" — the scope qualifier was dropped

This is the Addendum 3 universal returning in compressed form. Measured:

| scale | `ZERO_TOL` = 1e-11 | `ZERO_TOL` = 0 | |
|---|---|---|---|
| ×10⁻⁷ | 22 flips, free 80 | 22, 80 | unchanged |
| **×10⁻⁸** | **24 flips, free 90** | **26, 85** | **changed** |
| ×10⁻⁹ | 96 flips, free 159 | 96, 159 | unchanged |

And across the whole band ×7·10⁻⁸ to ×3·10⁻⁹, `ZERO_TOL = 0` moved the flip count at **all eight
sampled scales**. The earlier draft carried "at ×10⁻⁷ and ×10⁻⁹" precisely because of this; the
compression removed the two scales and left the verb.

**Fix — use the mechanism, which needs no scope.** At the collapse the LP returns a flow that is
exactly zero on every edge, so every edge is free at *any* tolerance, zero included. That is
unconditionally true and it is stronger evidence for the attribution than a "changes nothing" claim:

> *The coupling is to the **primal feasibility** tolerance, not the zero-flow tolerance: at the
> collapse the LP returns a flow that is exactly zero on every edge, so every edge is free at any
> tolerance including zero, and what makes that zero flow primal-feasible — and therefore optimal,
> since every arc cost is strictly positive and `f ≥ 0` — is scaling `b` far enough down.*

## 2. "Stays above it for any map below roughly 10⁸ nodes" — two different claims conflated

"It" reads as *eight orders*, and the figure is wrong for either reading:

| N | 80 | 100 | 10³ | 10⁶ | **10⁸** | 10¹⁰ |
|---|---|---|---|---|---|---|
| `1/N` | 0.0125 | 0.01 | 0.001 | 1e-6 | **1e-8** | 1e-10 |
| orders above 1e-10 | 8.1 | 8.0 | 7.0 | 4.0 | **2.0** | **0.0** |

- **Above eight orders** holds only to **N ≤ 100** — one order past the shipped map, not six.
- **Above the tolerance at all** holds to **N < 10¹⁰**, which is the number I gave in Addendum 9 and
  the one that belongs here.

At 10⁸ nodes the margin is 2.0 orders — still safe, but the sentence claims eight.

**Fix:** *"…which is more than eight orders above the tolerance for N = 80, and remains **above the
tolerance** for any map below roughly **10¹⁰** nodes."*

## On the closing note — agreed, with one addition

The count is **seven**, not six, and the last two failures have a different mechanism from the first
five. The first five were claims over ranges nobody had sampled. **These last two were correctly
scoped in the longer draft and lost their scope when it was shortened** — the qualifier "at ×10⁻⁷ and
×10⁻⁹" was cut as redundant, and "10¹⁰" became "10⁸" while the surrounding clause kept a bound
belonging to the other reading.

That is worth separating in the §3.16 record, because the remedy differs. Against the first kind:
sample the range at the resolution the claim implies. Against the second: **a scoped claim cannot be
shortened by removing its scope** — when a qualifier looks redundant it is usually the only thing
making the sentence true, and every compression of a verified sentence needs re-verifying as if it
were new text. Six of these seven rounds ended in a shorter sentence than they began, which is
where the risk concentrated.

And the honest summary of the scale material stands as you put it: it was **deleted, not fixed**,
after seven measured attempts failed the same way.
