# Validation — spec v6.1, round 5, part 1 (§0, §1.1, §1.2, §1.3, §1.4, §1.5)

**Document under test.** `per-good-trade-spec.md`, MD5 `59c84a97799db9db97fe889b6e3c6776` computed at
the start of this pass and again at the end — **unchanged**, so nothing below was graded against a
moving text.

**Inventory under test.** `claims-v6.md` (twelfth census, MD5 `b95f98345e1679f49a03581fac8778f7`).
Every one of the **222** IDs in §0, §1.1, §1.2, §1.3, §1.4 and §1.5 gets a verdict. The `(v5)` /
`REMOVED` rows are out of scope and are not verdicted.

---

## Instruments

Everything below was re-derived from the install, the saves, the mod's own scripts, or a script
written for this pass.

| Instrument | What it is | Validation before use |
|---|---|---|
| `scripts/measure6.py` | shipped; re-run from scratch | output **byte-identical** to the committed `measure6.out` (60 labelled figures), so the figure set is reproducible |
| `scripts/relabel6.py` | shipped; run as `python relabel6.py 45` (4 seeds x 45 = 180) | its own identity-permutation gate passed: **159 of 159** edges agree with `drain.py`, sink set matches |
| `scripts/val5_save.py` (new) | independent reader for `VANILLA_start.eu4`'s `gamestate` province records | parses 4,941 provinces, 2,472 owned — matches `solver.py`'s own count and its `ROLLED` map |
| `scripts/val5_hist.py` (new) | `history/provinces` key-effective-at-1444.11.11 parser (undated block, then dated <= start in date order) | reproduces `prov1444.json` on `base_tax`/`base_production`/`owner` for all 2,472 counted provinces |
| `scripts/val5_agg.py` (new) | aggregate field + DRAIN, the construction `measure6.py` uses | reproduces the baseline exactly: sinks `{genua, hangzhou}`, 159/159 edges, acyclic, 1 promotion, 0 fallbacks, world wealth 10,607.40 |
| `scripts/val5_pergood.py` (new) | per-good `S`, `C`, `b` and the §1.1 property battery | reproduces `measure6.out`'s live goods (29), sinks per good (2/8/3.69), acyclic goods (29), fallbacks (0) |
| `scripts/val5_relabel_pg.py` (new) | the **per-good** relabelling experiment (29 goods x 10), which no shipped script performs | validated on the identity permutation **for every one of the 29 goods** against `drain.py` before any trial was counted; aborts otherwise |
| a throwaway `v60/` tree | the pre-v6.1 operator, rebuilt from the committed `flowop.py.bak` / `drain.py.bak` / `measure6.py.bak` | reproduces the v6.0 answer the document quotes: sinks `{english_channel, hangzhou}` |

Two engine-side sources were used that earlier rounds did not:

* **The save's own ledger.** `VANILLA_start.eu4` and `Castile1444_12_22.eu4` carry
  `lastmonthincometable` per country. Index 0 is taxation, index 1 is production. This is the
  engine's own arithmetic, written by the engine, and it settles `TAX_COEFF`, `GP_COEFF`, the
  annual-over-twelve basis and the `devastation` scaling law **without reading a tooltip**.
* **The localisation tables.** `BASE_TRADE_GOODS_SIZE` = "Base Goods Produced",
  `GOODS_PRODUCED_EFFICIENCY` = "Goods Produced Efficiency", `TAX_INCOME_EFFICIENCY` = "Tax Income
  Efficiency", `PROV_TRADEVALUE_DESCR` = "calculated by multiplying the amount of goods with their
  value", `HINT_INCOME_TEXT` = "Production comes from the Trade Value in a province and can be
  improved by Production Efficiency". These corroborate tooltip *shape* from files.

**What was not re-observed this session:** the four in-game tooltip *readings* themselves
(`Base: 0.49 (Yearly 6.00)`, `Base: 0.16 (Yearly 2.00)`, `Trade Value 3.52` -> `+0.29`, `Base 0.49`
-> `0.62` at 125%). EU4 was not launched. Where a claim rests on one of those strings, the row says
so and reports what the ledger, the files and the arithmetic do settle. In every such case the
independent evidence agrees with the reading, and in one case (Y289/Y290) the start save's own `GRA`
monarch personality set — `cruel`, `infertile`, `calm`, **not** `industrious` — independently
confirms the claim that a window figure is one sample of a random variable.

---

## §0 — Front matter (48 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y207 | CONFIRMED | read `launcher-settings.json` in the install root; read `meta` from `Castile1444_12_22.eu4` | `"version": "EU4 v1.37.5.0 Inca (491d)"`, `"rawVersion": "v1.37.5.0"`; the save's `savegame_version` reads `first=1 second=37 third=5 forth=0 name="Inca"` |
| Y208 | UNTESTABLE | looked for an artifact to run on a non-1444 start; the mod is a design document plus a reference solver — there is no DLL and no `.mod` | "extended-timeline compatible" is a forward claim about software that does not exist yet. Settling it needs the emitter built and run against an extended-timeline start date |
| Y209 | CONFIRMED | read §2.2a (L942-982) for the requirement; measured the component count of the shipped adjacency | §2.2a: "**Premise 1 — the node graph is connected**"; `val5_pergood.py` finds **1 component, 0 bridges, min degree 2** over the 80 nodes / 159 edges of `nodes.json`, so the shipped target is satisfied |
| Y210 | CONFIRMED | opened `../v1-laplacian/per-good-trade-spec.md` | header reads `**Version:** 1.3` |
| Y211 | CONFIRMED | read v1's operator in `solver.py`'s docstring and `../v1-laplacian/diagnosis.md` §1 | both state it as `L phi_g = s_g - c_g`, phi pinned to mean 0 per component — a Laplacian potential |
| Y212 | CONFIRMED | read `../v1-laplacian/diagnosis.md` §7 "Verdict" in full | "**C: confirmed, dominant.** Sinks are local minima and the test is `(c-s)/deg > mean(nbr phi) - min(nbr phi)`, exact on 2320/2320 pairs ... the field's shape is set by supply geometry; demand only chooses among nodes the geometry has already flattened." The paraphrase "topological rather than economic" is faithful |
| Y213 | CONFIRMED | opened `drain-orientation.md` | it reads "**Verdict: the strongest candidate of the four tested**" — a four-operator comparison, as claimed. Minor: the citation is written bare and the file is in `../v2-drain/`, so it resolves only from that directory |
| Y214 | UNTESTABLE | opened `../v1-laplacian/validation.md` (685 rows, 23 REFUTED / 37 PARTIAL / 49 NEEDS_GAME); looked for a fold-through map | no artifact maps v1's corrections onto v6.1 text (`fixes-agreed.md` maps v5's, not v1's). Settling it needs a v1-to-v6 claim-by-claim mapping |
| Y215 | CONFIRMED | read `../v2-drain/per-good-trade-spec.md` front matter | "**v2.1** replaces the installed aggregate: `Phi_ord` (the value-weighted marking order) gives way to **`Phi_w`**, DRAIN run once more with wealth itself as the good (§1.6, §3.9)" — verbatim the same sentence |
| Y216 | CONFIRMED | read `solver.py`'s `province_table()` and diffed against `../v5-owner-agnostic/scripts/solver.py` | v6 reads `base_tax`, `base_production`, `trade_goods` and `ON_STARTUP_DEVASTATION` only; no owner-conditioned term appears anywhere in the wealth expression |
| Y001 | CONFIRMED | diffed the two solvers' wealth code | v5 carries `LOCAL_TAX_MOD`, `LOCAL_TV_MOD`, `MON_FLAT`, `MON_GPMOD`, `MON_TVMOD`, `PERM_FLAT`; v6 carries none of them. The property now holds by the shape of the expression rather than by a rule |
| Y002 | CONFIRMED | as Y001 | v6's wealth is a function of `base_tax`, `base_production`, `trade_goods` (the rolled good where history says `unknown`) and devastation — development, good, condition, nothing else |
| Y003 | CONFIRMED | as Y001, plus a search for any surviving sweep | no classifier, no great-project table, no permanent-modifier table, no `has_dlc` term and no install sweep survives in `solver.py` |
| Y004 | CONFIRMED | read v3.0 L163-165, `../v4-owner-agnostic/validation-v4.md` W041, v5.0 L17; counted great-project mentions in each spec | v3.0: "its `province = { ... }` block is province-scoped ... income-relevant local ones are exactly three"; v4's audit records the repair as "a **two-test procedure** — local ... and enters wealth"; v5.0 L17 introduces "the local-modifier classification is applied to the whole install". v3 and v4 specs contain **0** mentions of great projects or permanent province modifiers |
| Y005 | CONFIRMED | recomputed the v5 apparatus (gems `local_tax_modifier` 0.15, incense `trade_value_modifier` 0.10, the six great-project and ten permanent-modifier provinces) on top of the v6 field from `prov1444.json` + `00_prices.txt` | v6 field **10,607.40**; field + apparatus **10,712.70**; difference **105.30**; 105.30/10,712.70 = **0.9829%** -> 0.98%; 105.30/10,607.40 = **0.9927%** -> 0.99%. All four figures reproduce |
| Y006 | CONFIRMED | read W041 in `validation-v3.md`, X035 in `validation-v5.md`, W041 in `validation-v4.md` | v3 W041 is in the REFUTED list of ten ("At least a fourth, and a whole further class"); v5 X035 is REFUTED ("The enumeration misses `provincial_production_size` and the two non-owner-gated `province_triggered_modifiers`"); v4's harness records "### W041 — CONFIRMED ... **Repair.** §1.3 replaces the structural shortcut with a two-test procedure". Both audits and the harness pass are exactly as described |
| Y007 | CONFIRMED | all three re-derived independently (see Y059, Y066, Y067) | `on_startup` devastation: 11 provinces in the save, **0** history files mention devastation. `add_base_*`: province 1 has `base_tax = 5` undated plus `add_base_tax = 1` at `1436.4.28`, save reads `6.000`. `is_city`: 20 owned provinces lack the line and all 20 are in the save's owned set |
| Y965 | CONFIRMED | diffed the field figures between the rebuilt v6.0 run and the v6.1 run | world wealth 10,607.40, counted provinces 2,472, devastation cost 13.40, richest province `1821 @ 27.00`, GP_COEFF 0.2, European provinces 824, latent-coal 58/45 — **identical in both**. Only operator-dependent figures moved |
| Y008 | CONFIRMED | `relabel6.py`'s Phase-2 probe: 40 random node permutations under unit arc cost | "unit cost (former) ... permutations returning a DIFFERENT optimal support: **40 of 40**", objective identical to `max rel deviation 5.626e-16`. Degenerate, and presentation order picked the optimum |
| Y966 | CONFIRMED | read §2.3's cost block against `flowop.py`'s `TIE_COST` | both are `1 + TIE_EPS*(w[u]+w[v])/2 + TIE_EPS2*frac(min*max*7919)` with `w` min-max normalised; the first term is named the design statement, the second "tie-breaking and nothing else" |
| Y1000 | CONFIRMED | read §2.3's tolerance paragraph and `flowop.LP_OPTS`, then measured whether it is load-bearing | `LP_OPTS = {"dual_feasibility_tolerance": 1e-10, "primal_feasibility_tolerance": 1e-10}`. At scipy's default, **7 of 174** per-good column permutations return a different orientation (copper 5, paper 2); at 1e-10, **0 of 174**. A correctness requirement, measured |
| Y1001 | CONFIRMED | computed reduced costs from the LP duals for all 29 per-good solves (`rc = cost - (y[v] - y[u])`), and read scipy's documented default | smallest **positive** off-support reduced cost **3.7648e-08** on `copper` (next: cotton 1.18e-7, grain 1.18e-7). `scipy/optimize/_linprog_highs.py`: "Dual feasibility tolerance. Default is 1e-07." So 3.8e-8 sits inside 1e-7, as claimed |
| Y967 | CONFIRMED | `relabel6.py 45` (4 seeds x 45 = 180) for the aggregate; `val5_relabel_pg.py 10` (29 x 10 = 290) for the per-good graphs, instrument validated per good on the identity permutation first | aggregate: "orientation changed : **0 of 180**", edges moving mean 0.00 range 0-0, baseline sink set 180/180. Per good: "runs moving an edge : **0 of 290**", sink set 0 of 290, max 0 edges. Both halves reproduce |
| Y1002 | CONFIRMED | re-solved Phase 2 under random permutations of the LP's arc columns, aggregate and all 29 goods | aggregate 0 of 6 supports differ, max relative objective deviation 5.62e-16; per good **0 of 174** differ |
| Y968 | CONFIRMED | checked that the invariance figures are samples (180 and 290 permutations) and that §2.4 still imposes the order | §2.4 item 1: "the emitter must fix one canonical node order and keep it stable across rebuilds, and that order must be the order **Phase 2's LP input** is built in". Kept as a requirement, and no longer what decides the map (0 of 180 / 0 of 290) |
| Y969 | CONFIRMED | read v5.0 L334 and v6.1 §2.3, and `measure6.py`'s constant | v5.0: "`alpha_Phi = 1.5`, a stipulated constant (§2.3)"; v6.1 §2.3: "the aggregate-graph exponent `alpha_Phi = 2.0`"; `measure6.py` L18: `A_PHI = 2.0` |
| Y970 | CONFIRMED | read §2.3 and cross-checked the three values against the code | §2.3: "**`alpha_Phi`, `TIE_EPS` and `TIE_EPS2` are hyperparameters. Their values are developer taste, and this document offers no justification for any of them.**" Values 2.0 / 1e-3 / 1e-6 match `measure6.A_PHI`, `flowop.TIE_EPS`, `flowop.TIE_EPS2` |
| Y971 | CONFIRMED | read §2.3's withdrawal sentence and checked the withdrawn arguments are absent from live text | "v2.1 through v4.0 said it was calibrated so that 1444 yields a two-sink map, and v5.0 said it sat in the widest sink-count band. Both are withdrawn." `verify6.py`'s R2 needle "the widest band on this field" passes as **gone** |
| Y972 | CONFIRMED | rebuilt the v6.0 operator from the committed `.bak` files and ran its `measure6.py`; compared with the v6.1 run | v6.0: `Phi_w sinks ['english_channel', 'hangzhou']`. v6.1: `Phi_w sinks ['genua', 'hangzhou']`. The move is exactly as stated |
| Y973 | PARTIAL | counted what `measure6.py` prints (61 lines, 60 distinct labels — `route genua -> hangzhou` is emitted twice and collides in `OUT`), then diffed the v6.0 run against the v6.1 run label by label | **the denominator is wrong: 60, not 59** — the script's own last line reads "wrote measure6.out with 60 labelled figures". 59 is what it prints when the sink set has one member, i.e. the alpha=1.5 case. The numerator is close but does not reproduce: v6.0 -> v6.1 moves **31 of 62** labels (26 same-label value changes plus 5 labels appearing or disappearing); moving alpha alone, tie-break held fixed, moves **23** |
| Y1003 | CONFIRMED | read §2.1 L842-895 | it lists three checks — "One binary per platform, and no cross-platform sessions", "No runtime CPU dispatch in the LP solver, and single-threaded", "§2.8's cross-implementation orientation check" — all build and verification discipline, no design change |
| Y009 | CONFIRMED | read the convention at L46-48, then grepped for superlatives, universal quantifiers and bare thresholds and inspected each hit | every world-facing superlative found is scoped to a named source or a measurement: "the highest in the shipped price table", "the only row here whose scaling it leaves open", "the largest incumbent in **7 of the 26** inland nodes". The unscoped `never`/`always` hits are statements about the model or proved properties ("the sweep always advances"), not empirical absolutes |
| Y010 | CONFIRMED | read §3.15 (L1805-1915) looking for a maintained figure under each named operator | the Laplacian entry says "this entry does not maintain a copy of it"; the `Phi_ord` and gravity entries each carry "*No figures are maintained for it*"; the RANK and seeded-basin entries carry no measurement at all. All five named operators are covered |
| Y011 | PARTIAL | traced the rejected-operator figures through all three audits | **re-measured: yes** — v3 W155 (`Phi_ord` end counts, re-run `w4.py`), v3 W190 (gravity kernel, `phiw3.py`), v4 W190, v5 X075/X076/X160/X190. **Re-refuted: no** — v5 graded X075 and X076 **CONFIRMED** ("2779/4611 = 60.3%"); only W190 (v3) and X160 (v5) came back PARTIAL. So they were re-measured three times and mostly held. The second half holds: every §3.15 entry argues structurally, so no rejection depends on a number |
| Y220 | CONFIRMED | grepped for the two quoted directional forms and re-read §3.15 for surviving comparison figures | the quoted forms appear only at L53 as illustrations, and §3.15 carries no comparative percentage for any rejected operator. Practice matches the stated rule |
| Y012 | CONFIRMED | read `validation-v5.md`'s summary table, scanned every graded row header, cross-referenced `fixes-agreed.md` | v5's summary: CONFIRMED 134, **REFUTED 22, PARTIAL 39, UNVERIFIABLE 1**, total 196 — exactly the three counts quoted. Of the 63 row headers carrying a non-CONFIRMED grade, **0** are missing from `fixes-agreed.md`, which mentions 64 `X` ids |
| Y218 | CONFIRMED | opened `changes-v6.md` (6,953 lines) and located the v6.1 material | a replay-verified diff ("274 asserted string replacements ... Replaying the 274 in order against v5.0 reproduces v6.0 byte for byte") with a `## v6.1` section carrying old/new pairs, e.g. the superseded front-matter paragraph at L6467 against its replacement at L6482 |
| Y217 | PARTIAL | listed the document's measured figures and checked each for a script attribution | followed for most figures (`measure6.py` is named at L147, L343, L444, L449) but broken for several: §0's **105.30 / 10,712.70** name no script; §1.3's **12.23 / 9.40**, **12.70**, and the **89 = 43 + 31 + 16 - 1** census name none. The document concedes this two sentences later (Y017), which is why this is PARTIAL and not REFUTED |
| Y013 | CONFIRMED | read `verify6.py`'s `shows()` / `every_site()` construction, then ran `python verify6.py ../per-good-trade-spec.md` | the needle is built from the computed value (`needle = template.format(*computed)`), so a document figure that disagrees fails. Run: "**RESULT: 30 checks, 0 failed**", exit 0. Thirty checks against a document printing hundreds of numeric tokens is not every figure, so the second half holds too |
| Y974 | CONFIRMED | ran `coverage6.py` (one mutation per computed figure, verifier re-run each time) | "60 computed figures; **9** of them appear verbatim in the spec"; "coverage: **6 of 9** uniquely-locatable spec figures are protected (67%)", 3 MISSED, 23 further figures unscored. Partial, measured |
| Y1051 | CONFIRMED | read L63-68 | the paragraph gives neither a count nor a proportion and states two distinct reasons (the count moves with the prose; the denominator is ill-defined). The claim is about the paragraph, and the paragraph does exactly that |
| Y975 | CONFIRMED | read `verify6.py`'s generated checks and its final print | `for _m2 in re.finditer(r"the (one|two|three|...) (?:that describe\|province-state modifiers)", doc, re.I): RES.append(...)` — one check per matching phrase, so the total is prose-dependent; and the harness prints "RESULT: %d checks, %d failed". The retired self-count check is commented in place |
| Y015 | PARTIAL | wrote eight tokenisers over the document text and counted occurrences and distinct values under each | the substantive point holds — occurrence counts run **1,167 to 2,401** and distinct-value counts **178 to 344** depending on delimitation, so the denominator is genuinely ill-defined. The stated endpoints do not reproduce: my nearest two definitions give **314** and **329** distinct values, and 329 is outside the quoted 279-326. No instrument is named at that line, so the exact pair cannot be checked |
| Y1052 | CONFIRMED | grepped `changes-v6.md` and the round-11 census for the withdrawn wording | `changes-v6.md` L5432 and L6509 carry the old text "**covers well under half of what the document prints.** No count is given here..."; L477 records the diagnosis. Round 11's census recorded it as Y974. The refusal survives in the current text; the ratio does not |
| Y016 | REFUTED | read `coverage6.py` line by line and ran it | it does **not** corrupt each spec-printed figure. Its universe is the 60 values `measure6.py` computes, and it mutates only those whose rendering occurs **exactly once** in the spec: "60 computed figures; **9** of them appear verbatim in the spec", with 23 more printed as "unscored rather than assumed protected" and the several hundred numeric tokens the script does not compute never touched at all. A broader denominator than `mutate6.py`'s, but not the document's figures. The "re-run rather than quote" half is right — the number moves with any edit |
| Y017 | CONFIRMED | took `coverage6.py`'s MISSED list as the unguarded set and inspected those sites in the document for a script name | unguarded but script-attributed: the coal figures sit beside "(`measure6.py`)". Unguarded and unattributed: `source mean degree vs map` (**2.4**), `demand contrast range`, plus §0's **105.30** and §1.3's **12.23 / 9.40 / 12.70**. Both categories exist, as claimed |
| Y018 | PARTIAL | read `mutate6.py`'s `_spec_mutations()` and ran `python mutate6.py ../per-good-trade-spec.md` | the circularity claim is exactly right: all twelve planted errors are built from `measure6.OUT` keys that `verify6.py` already checks (world wealth, counted provinces, self-coherence x2, sinks per good, connected pairs, largest b_w, alpha band, European provinces, coal flips, coal delta, price census). But "reports a higher score" is false as shipped: **on the spec** the run dies with `KeyError: 'band containing alpha=1.5'`, deterministically, on three consecutive runs. Line 31 asks for that key as a **literal** while `measure6.py` line 125 emits `"band containing alpha=%g" % A_PHI` = `band containing alpha=2`; `verify6.py` line 122 derives the same key correctly, so the fix was applied there and not here. It cannot be a stale-file artifact: `mutate6.py` never reads `measure6.out` (0 mentions), it takes `M.OUT` from an in-process import. Note the two invocation paths — with no argument the target is `../fixes-agreed.md`, which takes the 10-entry typed `CHECKLIST` and reports "caught 10 of 10"; only `per-good-trade-spec.md` reaches the 12-entry `_spec_mutations()` that crashes |
| Y219 | CONFIRMED | grepped the document's top-level headings | `# 1. Mechanics` (L81), `# 2. Implementation` (L831), `# 3. Reasoning` (L1331) — three sections, in that order, with those roles |

---

## §1.1 — Trade direction (65 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y221 | CONFIRMED | read `solver.py`'s edge construction and `drain.py`'s per-good entry point | `EDGES_UND` is built once from `nodes.json` and every good's `run_drain(b_g)` is handed the same edge list; only `b` differs. 29 live goods, each with its own orientation of the same 159 edges |
| Y222 | CONFIRMED | searched the model's inputs for an authored direction | `nodes.json`'s `outgoing` is used only to build the **undirected** edge set (`EDGES_UND = sorted(set(tuple(sorted(e))))`); direction comes out of Phase 2 and Phase 3. Nothing authored survives into the orientation |
| Y223 | CONFIRMED | read `drain.py`: `phase0`, `phase1`, `phase2`, `sweep_priority`, `compile_dirs` | `run_drain` calls exactly those five in order on `b = s - c`; the four named phases plus the un-peel are all present and match the prose |
| Y224 | CONFIRMED | read `phase0` and the pendant branch of `compile_dirs` | `phase0` repeatedly removes degree-1 nodes and does `beta[u] += beta[v]` (the residual fold). `compile_dirs` emits `(v, u)` when `bv >= 0` (net exporter and zero, toward core) and `(u, v)` otherwise (net importer, fed from core). The three cases match exactly |
| Y225 | CONFIRMED | algebra, plus a check that the removed edges are bridges | a degree-1 node's single edge is a cut edge by definition, and on a tree conservation determines the flow uniquely, so the sign of the absorbed subtree balance is the flow direction. `val5_pergood.py`'s Tarjan pass confirms the notion is the right one (bridges = cut edges) |
| Y226 | CONFIRMED | computed the degree sequence and ran Tarjan's bridge algorithm on the shipped adjacency; checked `len(core)` per good | **min degree 2, max 8, mean 3.98; 1 component; 0 bridges**. `phase0` leaves `len(core) == 80 == N` for all 29 goods, so it is a no-op on this map |
| Y227 | CONFIRMED | ran `toys.py` T1, a graph with a pendant | T1 (triangle A,B,D plus leaf C off B) drives Phase 0's peel and un-peel and produces the pendant-importer sink, so the code path is live for maps that have pendants |
| Y228 | CONFIRMED | read `phase1` | `M = [sum(-beta[v] for v in comp)]`, `q = m/D`, `HHI = sum(x*x)`, `k = int(min(max(round(1.0/HHI), 1), len(comps)))`, then `S.add(min(comps[j], key=lambda v: (beta[v], v)))` over the top-k by mass. Every element of the description is in the code |
| Y229 | PARTIAL | looked for both knobs in `drain.phase1`'s signature | the dilation radius is there (`phase1(core, beta, dilate_r=0)`) and implemented. **The demand-mass quantile `rho` is not implemented at all** — no parameter, no filtering of `Dset` by mass. Because its stated default is 1.0 (cluster every demander), shipped behaviour is unaffected, but the document credits Phase 1 with a knob the reference implementation does not have |
| Y230 | CONFIRMED | recomputed `phase1`'s `k` for every live good | `k` distribution over 29 goods: `{1: 27, 2: 2}` -> **k = 1 for 27 of 29** at the default knobs |
| Y231 | CONFIRMED | compared Phase 1's selection with the final sink set | on the aggregate Phase 1 selects one node (`hangzhou`) and Phase 3 promotes one more; per good the measured sink counts run 2-8 against `k in {1,2}`, so the upward self-correction is doing the work, as the design says |
| Y232 | CONFIRMED | read `phase2` | `mincost_flow(b, zeros, cost=TIE_COST)` then `net_per_edge`, orienting each edge by the sign of its net flow with a `ZERO_TOL = 1e-11` deadband |
| Y976 | CONFIRMED | read `flowop.TIE_COST` and checked symmetry numerically | cost vector is `1.0 + TIE_EPS*(_a1+_a2)/2 + TIE_EPS2*frac(min*max*7919)`; the two arcs of every edge carry **identical** cost (max difference 0 over all 159 edges), so it is symmetric in the arc; it reads node wealth only. Matches §2.3's block exactly |
| Y977 | CONFIRMED | measured degeneracy under unit cost, then uniqueness under the tie-break | unit cost: 40 of 40 permutations give a different optimal support. Tie-break: every per-good solve has strictly positive off-support reduced costs except `paper`, whose single zero-reduced-cost arc (`cape_of_good_hope -> malacca`) is **blocked** — maximising its flow subject to the optimal objective returns exactly 0.0, so no alternative optimum exists. One optimum to return, on all 29 goods |
| Y233 | CONFIRMED | counted the support of every per-good Phase-2 solve and tested each for an undirected cycle by union-find | support sizes **78 to 79** with N-1 = 79; **0 of 29** supports contain an undirected cycle. A basic (vertex) optimum, as the simplex family gives |
| Y234 | CONFIRMED (algebra) | attempted the empirical version: re-solved all 29 with `method="highs-ipm"` at `ipm_optimality_tolerance=1e-12` | the mathematics is sound — an interior-point iterate converges to the analytic centre of the optimal face, which splits flow across equal-cost parallel paths and can leave a support with a cycle. I could not exhibit it here: scipy's `highs-ipm` runs crossover, and under the tie-break the optimum is unique anyway, so all 29 supports came back acyclic and <= N-1. The claim is a conditional about crossover-free solves and is not contradicted |
| Y235 | CONFIRMED | read §2.2's numbered requirement list | item 5: "DRAIN per good: min-cost b-flow — **network simplex or a simplex LP, not interior-point without** ..." |
| Y1004 | CONFIRMED | read §2.3's tolerance paragraph and §1.1 L111-113; measured the necessity | §2.3 states the requirement in those terms; `flowop` pins 1e-10; and the measurement (7 of 174 permutation flips at the default, 0 at 1e-10) shows it is a correctness requirement rather than a setting |
| Y236 | CONFIRMED | algebra, plus a directed-cycle test on all 29 supports | with all costs > 0 (min cost 1.0000097), cancelling flow around a directed cycle strictly lowers the objective, so no optimum contains one — positivity is all the argument uses. Measured: `has_cycle` returns None on all 29 orientations, hence on all 29 supports |
| Y237 | CONFIRMED | read `phase2` and `sweep_priority` | edges with `abs(net) <= ZERO_TOL` go into `free` and are oriented only in `compile_dirs` after the sweep. Measured 80-81 free edges per good |
| Y238 | CONFIRMED | read `sweep_priority`'s `ready()` | `u not in marked and cnt[u] == 0 and ((u in Sset) or (len(outs[u]) > 0) or any(w in marked for w in freeadj[u]))`, where `cnt[u]` counts unmarked flow out-neighbours. The three disjuncts are exactly the three the prose lists |
| Y239 | CONFIRMED | read `run_drain`'s call and the key function | `run_drain` calls `sweep_priority(..., "defasc_beta")`, whose key is `lambda v: (DEF[v], beta[v], pid[v])` — DEF ascending, b ascending, index |
| Y240 | CONFIRMED | read `flow_def`; checked acyclicity of the flow subgraph | `flow_def` topologically sorts the flow-arc subgraph and accumulates `DEF[v] = max(0, -beta[v]) + sum(DEF[u] for u in outs[v])`; the subgraph is built in Phase 2, before any free edge is oriented, and is acyclic (Y236). No circularity |
| Y241 | CONFIRMED | read the stall branch | `terminals = [u for u in gated if len(outs[u]) == 0 and inflow[u] > ZERO_TOL]`; `s_star = min(terminals, key=lambda v: (beta[v], v))` — most negative balance, i.e. heaviest demander. Measured: 1 promotion on the aggregate, promotions supply the per-good sink counts above `k` |
| Y242 | CONFIRMED | read the fallback branch | `s_star = max(gated, key=lambda v: (NODEW[v], -v))` — highest wealth, and `-v` makes the lowest index win a tie |
| Y243 | CONFIRMED | read how `NODEW` is built | `NODEW` is accumulated once from `solver.ROWS` (`tax + prod_income`) with no good index anywhere in it, so it is available before any per-good solve. No bootstrap needed |
| Y244 | CONFIRMED | read the `gated` construction; algebra for existence | `gated = [u for u in core if u not in marked and cnt[u] == 0]`; since the flow subgraph is acyclic, its induced subgraph on unmarked nodes has at least one node with no unmarked flow out-neighbour, so `gated` is non-empty and the sweep advances. The code also raises explicitly if it ever is empty |
| Y245 | CONFIRMED | algebra over `ready()` and the terminal test | a gated node with `len(outs[u]) > 0` satisfies `ready()` and would have been popped, so any node reaching the stall test has no flow out-arc; among those, `inflow[u] > 0` is exactly "flow-terminal demander". The wording is loose (a candidate with inflow *and* out-arcs is ready, not terminal) but the code matches the intended reading |
| Y019 | CONFIRMED | algebra over the two branches | at a stall every gated node has no flow out-arc; the fallback runs only when none has inflow either, i.e. every candidate is support-isolated; and a support-isolated node must have post-peel balance 0, since a non-zero balance forces flow at that node in any feasible b-flow |
| Y020 | CONFIRMED | read what the key and the promotion branches read | `sweep_priority` and both promotion branches read `beta`, the array `phase0` returns after folding each pendant's balance into its parent — not the raw `b`. So the condition is on the folded field, and a map with non-zero raw balances can still reach the branch |
| Y021 | CONFIRMED | algebra over the aggregate construction in `val5_agg.cw` | `b_w = 1/N - c_w` with `c_w[n] = sum_{p in n} (w/w_max)^alpha_Phi / total`, so `b_w == 0` for every node iff every node's `sum wealth^alpha_Phi` is equal. Uniform per-province wealth gives node sums proportional to province counts, which are not equal (Y022). For a per-good graph, `b_g == 0` across a component means no producer and no consumer there |
| Y022 | CONFIRMED | counted counted-provinces per node from `solver.ROWS` and `nodes.json` | range **0 to 72**: `cape_of_good_hope` holds 0 counted provinces, `mexico` holds 72. (Total membership including unowned provinces runs 20 to 77.) So equal per-province wealth gives unequal node sums |
| Y023 | CONFIRMED | read the fallback key | `max(gated, key=lambda v: (NODEW[v], -v))` — on a wealth tie the node index decides |
| Y024 | CONFIRMED | read §2.8's sink-set row and §2.4 item 1 | §2.8: "every sink inside the 2-core lies in `{selected} u {promoted} u {fallbacks}` ... Asserting containment in `{selected} u {promoted}` alone would halt on **T3** (§3.2)" — T3 is the stated reason, and the wealth tie is not mentioned. §2.4 item 1: the canonical order "must be the order **Phase 2's LP input** is built in, not merely the order the sweep breaks ties in" — a stronger requirement, set by Phase 2 |
| Y246 | CONFIRMED | read `compile_dirs`'s free-edge branch | `directed.append((u, v) if order[u] > order[v] else (v, u))` — from later-marked to earlier-marked |
| Y247 | CONFIRMED | read `compile_dirs`'s pendant branch | `for (v, u, bv) in reversed(Plog)` — the peel log replayed in reverse |
| Y248 | CONFIRMED | read all five §1.1 property bullets and classified each label | Global DAG: proof plus "Measured: acyclic 29/29". Sink placement: "**That equality is a measurement on this input, not a theorem**". Reachability: "a feasibility theorem" plus a measurement. Scan-invariance: "provably independent of scheduling" for the closure part and "**measured, not proved**" for the indexing part. Efficiency: "**This one carries no measurement and wants none**". Each is labelled and none stands in for another |
| Y250 | PARTIAL | listed §1.1's measurements and checked which ones `measure6.py` actually computes | `measure6.py` regenerates three of them — `acyclic goods 29`, `sinks per good min/max/mean (2, 8, 3.69)`, `fallbacks fired across goods 0`. It does **not** compute the reachability figure (100.0% of demand, zero orphan sinks), the scan-invariance figures, the 2,320-node key-collision count, the sink-set **equality**, or Phase 0's no-op — those I had to write `val5_pergood.py` to reproduce. So the attribution is right for part of the section and wrong for the rest |
| Y249 | UNTESTABLE | looked for an enumeration of the four over-claims in v3's audit and changes documents | `validation-v3.md` grades the claim "### W010, W011 — CONFIRMED (the discipline itself)" and says "Its application is audited property by property below", but it never enumerates four caught over-claims, and I found no such list. Settling it needs a v2-to-v3 over-claim ledger |
| Y251 | CONFIRMED | algebra over `compile_dirs` plus the measured result | flow arcs point from higher to lower in the marking order (the sweep marks a node only when its flow out-neighbours are marked) and free edges are emitted later-to-earlier by construction, so reversed marking order is a topological order; a bridge cannot lie on a cycle. Measured acyclic 29/29 |
| Y252 | CONFIRMED | ran `has_cycle` on all 29 per-good orientations | **29 of 29 acyclic**, reproducing `measure6.out`'s `acyclic goods 29` |
| Y253 | CONFIRMED | checked the enumeration against the code's exit points, and exhibited the two rare kinds | a node has no out-arc only if it was never handed one: it is a selected sink that stayed flow-terminal, a stall promotion, a fallback promotion, or a pendant fed from the core. `toys.py` T1 exhibits the pendant kind and T3 the fallback kind, so the enumeration is complete and each kind is realisable |
| Y025 | CONFIRMED | computed the sink set and the formula set `{selected & flow-terminal} u {promoted}` for all 29 goods (the shipped harness does not test this) | **equality holds on 29 of 29 goods, no mismatches**; sink counts min 2, max 8, mean **3.69**; **0 fallbacks** fired across goods. All four figures reproduce |
| Y026 | CONFIRMED | read v2's §1.1 bullet and re-ran T1/T2 | v2's spec asserts it flatly: "**Sink placement is explicit:** the final sinks are exactly `{selected & flow-terminal} u {stall-promoted flow-terminal demanders}`". T1 and T2 both break it, so it is not a theorem, and v2 did assert it as one |
| Y027 | CONFIRMED | ran `toys.py` T2 and checked its two side conditions | T2 is a 5-cycle plus a chord — minimum degree 2, so Phase 0 is a no-op — and its run reports `promoted=[]` with no fallback. Actual sinks `['u2']` against formula set `['u1', 'u2']`: **EQUAL: False**. The two conditions hold and the equality still fails |
| Y254 | CONFIRMED | ran `toys.py` (which reimplements DRAIN for arbitrary graphs) and read each case | T1: actual sinks `['C']` (a pendant net-importing leaf) vs formula `['B']`. T2: actual `['u2']` vs formula `['u1','u2']`, with `u1` handed the out-arc `u1 -> w` over a free edge to the earlier-marked conduit. T3: actual `['A']` vs formula `[]`, and A is the fallback promotion. All three break the equality in the three stated ways |
| Y255 | CONFIRMED | definition check in `sinks_of`, plus per-good sink sets | `sinks_of` returns nodes with out-degree 0 in that good's orientation; the per-good sink sets differ (2 to 8 members, different nodes), and no node is a sink for all 29 goods, so there is no global end node |
| Y256 | CONFIRMED | algebra plus measurement | `s` and `c` are both normalised to 1 over the world, so `sum_n b_g(n) = 0` identically; the LP's equality constraints then impose node balance and any feasible flow serves all demand. Measured: **100.0000% of demand reachable from supply on all 29 goods, 0 orphan sinks** |
| Y257 | CONFIRMED | algebra plus `toys.py` T5, which builds a disconnected graph with cross-component imbalance | T5's LP returns "success: False | The problem is infeasible. (HiGHS Status 8: model_status is Infeasible)". Share normalisation balances the world, not each component, so a two-component graph with cross-component imbalance is infeasible outright |
| Y258 | CONFIRMED | read the cited section | the document says §2.2a (not §2.2 — the census row transcribes the pointer as §2.2), and §2.2a L948-981 does exactly this: "**Premise 1 — the node graph is connected**" plus what the solver does when it is violated ("**So the stated target is: connected maps**", with the pendant and disconnected cases spelled out) |
| Y259 | CONFIRMED | measured component count, per-good demand reachability and orphan sinks | 1 component; demand reachable from supply **min 100.0000%, max 100.0000%** across 29 goods; **0** orphan sinks |
| Y260 | CONFIRMED | algebra over `ready()`, plus a scheduler-permutation experiment | the ready set is a monotone closure of the marked set, so the stall points and both promotion branches read only the closure, not the order it was built in. Measured: permuting the sweep's index tiebreak over 5 random relabelings x 29 goods (145 trials) gives **0** orientation changes |
| Y261 | CONFIRMED | as Y260, plus the key-collision count | the closure fixes the candidate set and the priority key is total once `(DEF, b)` never ties — and it never does (Y1005) — so free-edge direction is determined |
| Y262 | CONFIRMED | ran the scheduler-permutation experiment described above | **0 of 145** scheduler permutations changed any orientation; and the exactness caveat is right — the guarantee holds because the key has no exact ties (Y1005) |
| Y1005 | CONFIRMED | counted exact `(DEF, b)` key collisions over every core node of every per-good solve | core nodes summed over goods = **2,320** (29 x 80, Phase 0 being a no-op); exact key collisions = **0**. Both the count and the scope reproduce |
| Y1006 | CONFIRMED | tested Phase 1's two decisions for exact ties on every good | within-cluster argmin ties: **0**; top-k cluster-cut ties (M[k-1] == M[k]): **0**. Together with Y1005 no index tiebreak in the algorithm fires |
| Y263 | CONFIRMED | read the objective and computed the realised cost vector's range | the objective is `sum(cost * f)` with `cost = 1 + TIE_EPS*(w[u]+w[v])/2 + TIE_EPS2*gen`; every arc cost lies in `[1, 1 + TIE_EPS + TIE_EPS2] = [1, 1.001001]` (checked for all 318 arcs), so the optimum minimises a hop count in which a hop between wealthy nodes counts marginally more |
| Y978 | PARTIAL | computed the cost vector's actual spread and the nominal width of the stated interval | realised spread `max - min = 9.276e-04` = **0.0928%** of the base cost, which is under a tenth of a percent. But the interval the same sentence quotes has width `TIE_EPS + TIE_EPS2 = 0.001001` = **0.1001%**, which is *not* under a tenth of a percent. The claim is true of the realised costs on this field and false of the bound it was just derived from |
| Y264 | CONFIRMED | algebra | min-cost flow minimises total cost over the whole b-vector; a unit's path is not separately optimised, so a unit can detour when the sink assignment requires it. Nothing in the objective constrains per-unit paths |
| Y265 | CONFIRMED | read the property and checked no figure is attached | the bullet carries no measurement, and any hop count would be recomputing the objective the LP already minimised. Consistent with Y248's discipline |
| Y266 | CONFIRMED | read §2.3's pointer and §3.13's calibration | §2.3: "A measured calibration option that moves all three plus alpha's clamp is recorded in §3.13; the baseline does not use it" — a change to the program being solved, so it cannot be evidence about the property of the baseline program |
| Y267 | CONFIRMED | read the statement and checked EU4's income cadence in the save | the save's country records carry `lastmonthincome` and `lastmonthincometable`, so the engine books trade and production income monthly; a monthly recompute aligned to that tick is coherent with the engine. (The DLL that would do the recomputing does not exist yet, so this is design intent verified against the engine's cadence) |
| Y268 | CONFIRMED | read `run_drain` for carried state | `run_drain(b)` builds everything from `b` and the graph; nothing is cached between calls and no previous orientation is read. Corroborated by the repeat-solve test (Y269), which is bit-identical |
| Y269 | CONFIRMED | ran six solves of the aggregate and six of one good in one process | **1 distinct orientation** out of six for the aggregate and **1** out of six for `spices` — six identical solves, one orientation |
| Y270 | CONFIRMED | read L199-201 and §3.13 | "The LP is deterministic on one machine and one build (six identical solves ...); across machines it is the open question of §3.13" — and §3.13's list does carry the cross-machine question; §2.1's multiplayer paragraph turns it into build discipline |

---

## §1.2 — Supply (6 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y271 | CONFIRMED | read `solver.build_sc` | `gp[gi, node] += r["gp"]`, `world = gp.sum(axis=1)`, `S[live] = gp[live] / world[live]` — the node's goods-produced over the world sum, exactly the stated formula. Checked one good: `S[grain]` sums to 1.000000 |
| Y272 | CONFIRMED | read `00_static_modifiers.txt`'s autonomy and production-efficiency blocks; read the engine's own hint text | `local_autonomy_multiplicative` scales `local_manpower_modifier`, `local_sailors_modifier`, `local_tax_modifier`, `local_production_efficiency`, `province_trade_power_modifier` and both force limits — and **not** `trade_goods_size`. The `production_efficiency` block carries only `colonist_placement_chance`. `HINT_INCOME_TEXT`: "Production comes from the Trade Value in a province and can be improved by Production Efficiency" — efficiency acts on income, not on goods produced |
| Y273 | CONFIRMED | read all four blocks in `common/static_modifiers/00_static_modifiers.txt` | `devastation` `trade_goods_size_modifier = -2`; `prosperity` `= 0.25`; `under_siege` `= -0.25`; `occupied` `= -0.5`. All four carry the key |
| Y274 | PARTIAL | read `solver.build_sc`'s signature and every call site | as run, there is no regularizer: `measure6.py`, `drain.py` and `val5_pergood.py` all take `eps=0.0` (or build `S` directly), so `s` is the raw share. But the shipped `build_sc(alpha_of_good, eps=1e-6)` **still contains** `S[live] = (1 - eps) * S[live] + eps / N` **with a non-zero default**, so a caller that omits `eps` gets v1's regularizer. True of the model, not yet true of the code |
| Y275 | CONFIRMED | read `compile_dirs` and the free-edge count | free edges (80-81 per good) are oriented by the marking order the sweep produces, never by comparing potentials; no near-equal float comparison enters. This is what removes the need for the epsilon floor |
| Y276 | CONFIRMED | tested `b[v] == 0.0` exactly for every node and every good | exactly one node has `b == 0.0` exactly, `cape_of_good_hope`, and it does so for **all 29 goods** (it holds 0 counted provinces, so `s = c = 0`). It is oriented like any other node: `measure6.out` gives it in-degree 2 and out-degree 2 on the installed graph |

---

## §1.3 — Demand (78 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y277 | CONFIRMED | read `solver.province_table` and `build_sc` | wealth is computed per province row, then `np.add.at(C[gi], pn, w/tot)` sums province contributions into the node. Per province, then to the node |
| Y028 | CONFIRMED | read the wealth expression | it reads `s["base_tax"]`, `s["base_production"]`, the trade good (via `PRICES`), and `ON_STARTUP_DEVASTATION[pid]`. Three things: development, good, condition |
| Y278 | CONFIRMED | as Y028 | no government, owner or country field enters; the units are ducats per year |
| Y279 | CONFIRMED | searched the whole wealth path for each named input | no autonomy, no production efficiency, no idea, no estate, no government reform and no technology term appears in `province_table` or `build_sc`. The v5 solver's `LOCAL_*`/`MON_*`/`PERM_*` tables are gone |
| Y029 | CONFIRMED | algebra over the expression | `wealth(p)` is a function of `(base_tax, base_production, good, devastation)` alone, so two provinces agreeing on those agree on wealth irrespective of owner |
| Y280 | CONFIRMED | algebra | the owner tag enters only the *counting* predicate (`if not s.get("owner"): continue`), never the value. A change of owner alone cannot move `wealth(p)`; what conquest does move is devastation/occupation/siege, which the section says explicitly and which are properties of the place |
| Y030 | CONFIRMED | as Y001 plus the two audit findings (Y006) | the classifier and its sweep are gone from the code; and both audits that examined the old classifier refuted it (v3 W041, v5 X035) |
| Y031 | CONFIRMED | inspected the province-history fields the parser reads | `base_tax`, `base_production` and `trade_goods` are plain scalar fields of the province's own history file; there is no modifier to classify |
| Y032 | CONFIRMED | read `common/tradegoods/00_tradegoods.txt` | `gems` carries `province = { local_tax_modifier = 0.15 }` and `incense` carries `province = { trade_value_modifier = 0.1 }` — both province-scoped and both absent from `solver.py` |
| Y033 | CONFIRMED | recomputed the census: counted-province goods from `prov1444.json` plus the rolled goods, and the great-project/permanent-modifier province ids from the v5 solver | gems **43**, incense **31**, great-project + permanent-modifier ids **16** (`6, 8, 262, 362, 363, 370, 371, 387, 542, 684, 1821, 1822, 2145, 2151, 2316, 4316`), overlap **{542}** — union **89** of 2,472, and 89 is also the number of provinces whose wealth actually moves when the apparatus is applied |
| Y034 | CONFIRMED | recomputed the census under the `is_city` filter; checked 4856's rolled good | of the 89, two are not `is_city = yes` (**1207** and **4856**), so the count under the withdrawn filter is **87**. Province 4856 has `trade_goods = unknown` in history and the save shows it rolled **incense**, so it is the 89th |
| Y281 | CONFIRMED | design statement, checked against the input surface | the surviving inputs are three scalar province fields plus a devastation level; there is no modifier-classification decision anywhere in them |
| Y035 | CONFIRMED | read the code; then tested the coefficient against the engine's own ledger | `gp = max(0.0, GOODS_PRODUCED_FACTOR * s["base_production"] * (1.0 + gmod))` — no additive term. Engine test: annualised production income divided by the model's `0.2 * base_production * price` over 663 countries has **median 1.042 and mode exactly 1.0** (278 countries), the spread above 1.0 being production-efficiency and goods-modifier effects the model deliberately drops |
| Y036 | CONFIRMED | read the code; read the engine's own description; ledger test as Y035 | `prod_income = gp * price`. `PROV_TRADEVALUE_DESCR`: "This is calculated by multiplying the amount of goods with their value." The ledger test puts the mode at 1.0 with the annual/12 basis |
| Y037 | CONFIRMED | read the code; engine ledger test | `tax = TAX_COEFF * s["base_tax"] * (1.0 + tmod)`. Engine test: annualised taxation income per point of country `base_tax` over 665 countries has **median 1.014 and mode 1.0** (518 countries), e.g. ATH `base_tax` 10 -> 0.833/month = 10.0/year, BOS 21 -> 1.75/month = 21.0/year |
| Y282 | CONFIRMED | read the code | `wealth = r["tax"] + r["prod_income"]` throughout (`val5_agg`, `measure6`, `drain.NODEW`), in ducats per year |
| Y283 | CONFIRMED | read `build_sc`; checked the normalised form used by `measure6` is identical | `w = wealth ** a; np.add.at(C[gi], pn, w / w.sum())`. `measure6` uses `(w/w.max())**a` normalised the same way; the two agree to **4.86e-17** on every good, since the `w_max` factors cancel |
| Y284 | CONFIRMED | read §2.3's provenance table and the two code paths | `GP_COEFF` is read from the install at import time by `solver._read_gp_coeff`; `TAX_COEFF = 1.0` is a literal with a measurement note. Different kinds of constant, as claimed |
| Y038 | CONFIRMED | read the file block and its localisation | `00_static_modifiers.txt`: `provincial_production_size = { trade_goods_size = 0.2 ship_recruit_speed = -0.01 }`; `EU4_l_english.yml:815: provincial_production_size:0 "Base Production"` |
| Y039 | CONFIRMED | read `solver._read_gp_coeff` | it parses the block out of the install at import and raises `RuntimeError("provincial_production_size not found - re-derive GP_COEFF")` rather than falling back to a literal. Read at runtime, and moddable |
| Y040 | CONFIRMED | negative search: every `TAX` define in `defines.lua`, the whole of `common/defines/`, a search for `0.0833` across `common/`, and the neighbouring static-modifier block | `defines.lua`'s TAX entries are `PS_RAISE_WAR_TAXES`, `PS_WAR_TAXES_LIMIT_MIN`, `ENFORCE_CULTURE_TAX_MULTIPLIER`, `SCUTAGE_TAX_FRACTION`, `WARTAXES_DURATION`, `CITY_SPRAWL_NUDGE_TAX_VALUE`, `BASE_TAX_COST_MODIFIER`, `FLAT_TAX_AMOUNT` — none is a ducats-per-base_tax coefficient. `common/defines/` holds only the dummy and the four difficulty files. **0** hits for `0.0833` anywhere in `common/`. And `provincial_tax_income` (the analogue of the block that holds `GP_COEFF`) carries only `regiment_recruit_speed`, `local_great_project_upgrade_time`, `local_build_time`, `local_institution_spread`. The negative result reproduces |
| Y285 | CONFIRMED | tested the basis against the engine's own ledger rather than a tooltip | for hundreds of countries the monthly taxation figure is exactly the annual over twelve: ATH `base_tax` 10 -> `0.833`, BOS 21 -> `1.750`, GOT 16 -> `1.366`. The production column behaves the same way (mode 1.0 against the model's annual figure /12). Both terms share the basis, so the annual forms add |
| Y041 | CONFIRMED | arithmetic on the stated schema, plus the ledger test for the parenthetical; the tooltip strings themselves were not re-read in-game | `trunc(6 x 0.0833333) = trunc(0.4999998) = 0.49` and `trunc(2 x 0.0833333) = trunc(0.1666666) = 0.16` — both observations are exactly what the schema predicts. The `(Yearly base_tax)` half is confirmed independently by the ledger: annualised tax per point of `base_tax` is 1.0 at the mode over 665 countries. Not re-observed this session: the two tooltip strings |
| Y042 | CONFIRMED | arithmetic over the two stated observations | 12 x 0.49 = **5.88** and 12 x 0.16 = **1.92**, neither of which is the parenthetical (6.00, 2.00); whereas `base_tax/12` truncated gives 0.49 and 0.16. The parenthetical is `base_tax` and the base line is its truncated twelfth |
| Y043 | CONFIRMED | grepped v3.0, v4.0 and v5.0 specs | v4.0 L163 and v5.0 L170 both read `Base: X (Yearly 12*X)` with the same two data points, which 12 x 0.49 = 5.88 falsifies; v3.0 contains **0** occurrences of that schema and **0** of `0.6125` |
| Y044 | CONFIRMED | arithmetic: solved the truncation interval implied by 3.52 -> 0.29 | truncation gives `0.29 <= 3.52/d < 0.30`, i.e. `d` in `(3.52/0.30, 3.52/0.29] = (11.733, 12.138]` — the stated `(11.73, 12.14]` to the quoted precision. One observation, one interval, correctly not claimed as exactly 12 |
| Y045 | CONFIRMED | algebra over the two established relations | if both monthly figures are the annual value over twelve then multiplying both by twelve preserves the sum, so the annual forms add directly; and the tax pair fixes the relation at `base_tax` 2 and 6 (two development levels), corroborated by the ledger across 665 countries |
| Y286 | CONFIRMED | read both province history files | `223 - Granada.txt`: `base_tax = 6`, `base_production = 4`, `trade_goods = silk`, no `local_autonomy` line (so 0). `1747 - Caceres.txt`: `base_tax = 2`, `base_production = 2`, `trade_goods = wool`. Every attribute matches (the file's name is "Granada"; "Garnatah" is the dynamic name under its Muslim owner) |
| Y287 | CONFIRMED | read §2.3's constants table | both coefficient rows cite the base lines (`Base Goods Produced` for GP_COEFF, the `(Yearly ...)` parenthetical for TAX_COEFF) and the text adds "Neither is read off a province window". Only the base lines are used |
| Y288 | CONFIRMED | file evidence for the mechanism; the window reading itself not re-observed | `industrious_personality` in `common/ruler_personalities/00_core.txt` grants `global_trade_goods_size_modifier = 0.1`, which is a country-scoped goods modifier, so a province window's Trade Value must carry it. The claim's mechanism is exactly right |
| Y289 | CONFIRMED | arithmetic closure on the reading, plus the file evidence | silk's `base_price` is **4.0**, so `0.2 x 4 x 1.10 x 4.0 = 3.52` exactly, against `0.2 x 4 x 4.0 = 3.20` without the +10%. The `Industrious` personality is `global_trade_goods_size_modifier = 0.1`, and `history/countries/GRA - Granada.txt` contains **0** `personality` entries, so the monarch's personality is not scripted. The reading is arithmetically closed by the file values |
| Y290 | CONFIRMED | read GRA's country history for a scripted personality, then read the monarch's personalities out of the start save | history scripts none (0 hits). The save's GRA record carries `cruel_personality=yes`, `infertile_personality=yes`, `calm_personality=yes` — **not** `industrious`. So the personality is rolled and differs between runs: a window figure is one sample of a random variable, while the base lines and the annual-over-twelve ratio (confirmed across 665 countries) are not |
| Y291 | CONFIRMED | ledger test of the ordering | the engine's per-country income equals a development-derived base times a multiplier: the tax mode is exactly 1.0 x `base_tax` and countries with extra `global_tax_modifier` land at 1.1-1.2 x, never at a shifted base. The base is computed from development first and the percentage applied to it |
| Y046 | CONFIRMED | arithmetic on the stated observation; the tooltip pair not re-observed | 0.49 x 1.25 = 0.6125, which truncates to **0.61**, not 0.62; while `6 x 0.0833... = 0.499999`, x 1.25 = `0.6249989`, which truncates to **0.62**. The displayed value is consistent only with multiplying the untruncated monthly value, exactly as claimed |
| Y047 | CONFIRMED | inspected what the single observation can distinguish | the example separates "base then percentage" from "percentage then base" but cannot fix the rounding rule, the number of internal digits, or the multiplier's own precision. Claiming only the ordering is correct |
| Y048 | CONFIRMED | grepped v4.0 and v5.0, and read §2.3's rule | v4.0 L178 and v5.0 L185 both read "giving 0.6125, which the province window shows as 0.62"; §2.3's table states "The displayed monthly is the truncation of `base_tax x 0.083333`". Truncation of 0.6125 is 0.61, so the two cannot both hold |
| Y049 | CONFIRMED | read the localisation keys for the two tooltip blocks; checked the model for any flat goods bonus | `BASE_TRADE_GOODS_SIZE:0 "Base Goods Produced"` (the additive block) and `GOODS_PRODUCED_EFFICIENCY:0 "Goods Produced Efficiency"` (the multiplicative one) both exist, so the tooltip has the stated shape. And under v6's §1.3 no source grants a flat `trade_goods_size`: the four condition modifiers are all `*_modifier` percentages, and the flat sources (great projects, permanent modifiers) are the deleted apparatus. Exercised by no province |
| Y050 | PARTIAL | read all 373 blocks of `00_static_modifiers.txt` and extracted every block carrying `trade_goods_size_modifier` or `local_tax_modifier`; then checked which the model applies | the five named blocks are all in that file with the stated keys, and `unrest` is excluded — both true. Two qualifications. (1) "**four of the five are applied**" is true of the model's tables but not of its code path: `province_table()` applies only `devastation` (`gmod = STATE_GOODS_MOD["devastation"] * dev; tmod = 0.0`); `prosperity`, `under_siege` and `occupied` have no input anywhere in the model, live or not. (2) "five static modifiers describe a province's own state" is not exhaustively derivable from the file: `expanded_infrastructure` is province-scoped and carries **both** wealth keys (`trade_goods_size_modifier = 0.05`, `local_tax_modifier = 0.1`), and `blockaded` is a province condition (with no wealth key). Nothing at 1444 carries either, so the field is unaffected |
| Y051 | CONFIRMED | read the four blocks | `devastation trade_goods_size_modifier = -2`; `prosperity = 0.25`; `under_siege = -0.25`; `occupied trade_goods_size_modifier = -0.5` **and** `local_tax_modifier = -0.5`. Every magnitude, sign and target matches the table |
| Y054 | CONFIRMED | read the `devastation` block for a scaling comment; checked the other four; then **tested the law against the engine** on the December save | the file gives the magnitude and no scaling law for `devastation` (no comment in the block), while `unrest` carries `#10% longer time to build troops for each rr` and `nationalism` `#for each year revolt risk!` — so it is the one row whose scaling the file leaves open. Better than the wiki: in `Castile1444_12_22.eu4`, BOH's engine production income is **9.324 ducats/year**, against a model of **8.668** at `-2 x level/100`, **15.134** at `-1 x level/100` and **21.600** unscaled (ratios 1.076 / 0.616 / 0.432, with CAS's control ratio 0.996). The `-2 x level/100` law is the only one that fits. (The wiki quotation itself was not fetched, so the attribution of those exact words is unchecked; the law they assert is now confirmed against the engine) |
| Y052 | CONFIRMED | read the `unrest` block | `unrest = { regiment_recruit_speed = 0.1 #10% longer time to build troops for each rr / ship_recruit_speed = 0.1 / local_tax_modifier = -0.02 }` — the key, the magnitude and the per-point reading are all there, and `local_tax_modifier` enters `tax_value` |
| Y053 | CONFIRMED | cross-read the five blocks' keys | `occupied` carries both keys and `unrest` carries `local_tax_modifier`; `devastation`, `prosperity` and `under_siege` carry only `trade_goods_size_modifier`. Exactly as stated |
| Y292 | CONFIRMED | read the two blocks' comments | the `unrest` block's comment is `#10% longer time to build troops for each rr`, verbatim, and `nationalism` uses the same per-unit convention (`#for each year revolt risk!`) — the unit differs (per year of nationalism rather than per point of risk) but the convention is the same |
| Y979 | CONFIRMED | counted provinces carrying `unrest` in the start save and searched the model for the modifier | **21** counted provinces carry a non-zero `unrest` field at 1444.11.11, and `solver.STATE_TAX_MOD = {"occupied": -0.5}` — no unrest term anywhere. Live, and deliberately not read |
| Y980 | CONFIRMED | file evidence for each named source of revolt risk | separatism, unaccepted culture, wrong religion and nationalism are all owner-relative: `nationalism` grants `local_unrest = 0.5` per year of nationalism, `non_accepted_culture` carries `local_tax_modifier = -0.33`, and both are relations between the province and its current owner. Reading unrest would therefore move a province's wealth on conquest |
| Y981 | PARTIAL | read `solver.py`'s two modifier dicts and every use of them | `STATE_TAX_MOD` does carry `occupied` alone — verbatim true. The inference "so four of the five rows are applied" holds only as a statement about the tables: `STATE_GOODS_MOD` lists four keys but `province_table()` reads only the devastation one, so three of the four have no input path. Same finding as Y050(1) |
| Y982 | CONFIRMED | parsed the province records of `VANILLA_start.eu4` independently of the model | exactly **21** provinces carry a non-zero `unrest` value, all 21 are in the model's counted set: 331, 418, 419, 1071, 1074, 1075, 1076, 1227, 1966, 2205, 2305, 2427, 2433, 2441, 2771, 2772, 4292, 4688, 4689, 4690, 4745 |
| Y057 | REFUTED | parsed `history/provinces` for both `unrest` and `revolt_risk` effective at 1444.11.11, and read the owner of each of the 21 | the 16/5 split is right in shape and wrong in substance. **16** provinces are authored with `unrest` at integer 5/8/10/15 — that part reproduces exactly. But the other **five (1071, 1074, 1076, 4689, 4690) are also authored in `history/provinces`**, as `revolt_risk = 15` in the *undated* block (e.g. `1071 - Tara.txt` line 17), with a `revolt_risk = 0` in a **1468** block that does not apply at the start date. So "receive theirs at runtime" is false and "reading them needs the save" is false — they are readable from history under a different key. They are also **Shaybanid**-owned (tag `SHY`, `countries/Shaybanid.txt`), not Shirvan. And Sofala's quoted comment is real but sits in a **1515.1.1** block (`unrest = 8`), so Sofala is not one of the start-date 21 at all |
| Y983 | REFUTED | as Y057 | the derivation rests on five of the 21 being owner-derived at runtime, and all 21 are authored in the province history. What the save adds is a uniform offset: every one of the 21 reads exactly the authored integer minus 0.166. So a quarter of the start-date revolt risk is not owner-derived; the owner-derived part is a 0.166 shim on all of it. (The forward-looking half — that the share grows in play — is untestable from a start-date save) |
| Y984 | CONFIRMED | checked that the three named modifiers are in the model and are place-scoped | `devastation`, `occupied` and `under_siege` are all in `STATE_GOODS_MOD` (with `occupied` also in `STATE_TAX_MOD`) and all three describe the province's own condition; they deliver conquest-costs-wealth without reading who the owner is. `unrest` would add owner dependence and no new mechanic |
| Y055 | CONFIRMED | recomputed the exclusion cost from the save's unrest values and from the authored integers, at `local_tax_modifier = -0.02` per point | from the save: **12.2307** ducats = **0.1153%** of 10,607.40. From the 16 `unrest`-keyed provinces at their authored integers: **9.4000** ducats = **0.0886%**. Both figures and both percentages reproduce. (Reading all 21 at their authored integers would give 12.40 — the 9.40 figure is exactly the 16-province subset) |
| Y056 | CONFIRMED | rebuilt the wealth field with `tax * (1 - 0.02 * unrest)` on the 21 provinces and re-ran the aggregate at `alpha_Phi = 2.0` | world wealth 10,595.17 (delta -12.2307); edge flips **4 of 159**; sink set `['genua', 'hangzhou']` -> `['genua', 'hangzhou']`, **unchanged**. Both halves reproduce |
| Y985 | CONFIRMED | repeated the same experiment at `alpha_Phi = 1.5` | at 1.5 the same wealth change moves **0** of 159 edges (sinks `['english_channel']` before and after). So the earlier draft's "moves no edge" was correct at 1.5 and is wrong at 2.0, exactly as the parenthetical says |
| Y058 | CONFIRMED | checked the three dependents named | §1.2 L209 rests on the four `trade_goods_size_modifier` blocks; §3.3 L1457 carries "A besieged province genuinely produces less"; §2.8's case table carries war rows ("Razed China", "Major war in China"). All three exist and depend on the condition modifiers |
| Y059 | CONFIRMED | counted devastated provinces in the start save; grepped all ~4,900 province history files for devastation; read `flavor_boh.15` | the save has exactly **11** devastated provinces: 266, 2968, 2970, 4724, 4725 at **50** and 265, 267, 1771, 2967, 4237, 4726 at **20** — matching `solver.ON_STARTUP_DEVASTATION` entry for entry. `grep -l devastation history/provinces/*.txt` returns **0 files**. `flavor_boh.15` applies `bohemia_area = { add_devastation = 50 }`, `erzgebirge_area` and `moravia_area` `= 20` |
| Y060 | CONFIRMED | traced the chain file by file | `common/on_actions/00_on_actions.txt` `on_startup = { ... on_startup_effect = yes }` -> `common/scripted_effects/01_scripted_effects_for_on_actions.txt` L4716 `on_startup_effect = {` ... L4795 `country_event = { id = flavor_boh.15 }` (gated on `tag = BOH` and a flag) -> `events/flavorBOH.txt` L939 `id = flavor_boh.15`, titled "The Aftermath of the Hussite Wars". Every link is as described |
| Y061 | CONFIRMED | re-ran `measure6.py` from scratch and compared the field with and without the devastation multiplier | `devastation cost in ducats  13.4`, reproduced bit-identically on a fresh run; the same figure is the one `verify6.py` checks against the document ("It costs **13.40 ducats**", PASS) |
| Y062 | CONFIRMED | the three reads were each verified independently (Y059, Y066, Y067) | all three are cases where `history/provinces` and the engine's start state disagree, and in all three the engine's state is what the model reads |
| Y063 | CONFIRMED | read the `on_startup` block in `common/on_actions/00_on_actions.txt` | its own `events = { }` list holds `muslim_school_events.20`, `flavor_got.1`, **`flavor_mng.42`**, **`flavor_mos.1`**, `flavor_fra.206`, **`flavor_geo.1`**, `flavor_mam.111`, and the block separately calls `on_startup_effect = yes` — two paths, as claimed |
| Y064 | CONFIRMED | compared my independent history parse against my independent save parse over all 2,472 counted provinces | mismatches: `base_tax` **0**, `base_production` **0**, `owner` **0**, `trade_goods` **20** — and the 20 are exactly the `unknown` provinces (774, 862, 895, 897, 907, 966, 1809, 2014, 2503, 2510, 2571, 2593, 2596, 2669, 2671, 2932, 4856, 4901, 4902, 4923) |
| Y065 | CONFIRMED | read `flavor_geo.1` and `flavor_geo.3` in `events/FlavorGEO.txt`; searched for what fires geo.3 | `flavor_geo.1`'s whole immediate effect is `add_legitimacy = -20`, `add_country_modifier = { name = "geo_powerful_nobles" ... }`, `set_country_flag = geo_received_starting_event` — legitimacy, a country modifier and a flag, no `add_base_*`. `flavor_geo.3` option b carries `capital_scope = { add_base_tax = 2 add_base_production = 2 ... }`, and the only thing that fires it is `missions/KoK_Georgian_Missions.txt:2043`. `on_startup` does not |
| Y066 | CONFIRMED | read `history/provinces/1-Uppland.txt` and the save's province 1 | undated `base_tax = 5`; `1436.4.28 = { ... add_base_tax = 1 }`; the save reads `base_tax=6.000`. (A second `add_base_tax = 2` sits at `1444.11.12`, one day after the start, and is correctly excluded.) Accumulation, not replacement |
| Y067 | CONFIRMED | listed counted provinces whose history lacks `is_city = yes` effective at the start date, then checked them in the save | exactly **20**: 265, 774, 857, 913, 958, 966, 1035, 1038, 1207, 2527, 2579, 2593, 2617, 2671, 2779, 2932, 4573, 4576, 4640, 4856. Province **265** is among them and is also one of the devastated eleven. `265 - Brno.txt` line 13 is `#is_city = yes` (commented out); 913, 1207 and 4856 have no such line at all; 774 and 857 have one only in a 1596/1583 block. All 20 are owned in the save |
| Y068 | CONFIRMED | counted owned-and-in-a-node provinces both ways | the model counts **2,472**; the save has **2,472** owned provinces; 2,472 - 20 = **2,452**, the figure the `is_city` filter would have given |
| Y069 | CONFIRMED | counted `trade_goods = unknown` in the history parse; checked every good has a `chance` block | **20** counted provinces read `unknown` in history, and each good in `00_tradegoods.txt` carries a `chance = { factor = ... }` block from which the engine draws |
| Y070 | CONFIRMED | summed the production income of the 20 rolled provinces | pricing them at zero loses exactly **12.70** ducats of world wealth, and `solver.province_table` does read `ROLLED[pid]` from the save rather than predicting the draw |
| Y071 | CONFIRMED | counted the rolled goods of those 20 provinces in the save | `{fur: 7, grain: 5, wool: 3, livestock: 2, cotton: 1, incense: 1, naval_supplies: 1}` — seven, five, three, two and one each of three, exactly as listed |
| Y293 | PARTIAL | corroborated each itemised percentage from files, and checked the exclusion in the code | the exclusion is CONFIRMED: none of these terms appears anywhere in `solver.py`. Of the itemisation, `Reform Iqta +5%` reproduces (`iqta` in `01_government_reforms_monarchies.txt` grants `global_tax_modifier = 0.05`, and GRA's history carries `add_government_reform = iqta`) and `national ideas +15%` reproduces (`GRA_ideas` grants `global_tax_modifier = 0.15`). `Clergy +5%` does not appear as a fixed +5% anywhere: the church estate grants `global_tax_modifier = 0.2` scaled by loyalty and influence, so +5% is a display value of a scaled term rather than a file constant. The `+2%` technology term was not located. The itemisation as a whole is an in-game tooltip reading and was not re-observed |
| Y294 | CONFIRMED | read the `core` and `city` static-modifier blocks | `core = { local_tax_modifier = 0.75 }` and `city = { local_tax_modifier = 0.25 }` — both province-scoped tax multipliers, and both inside the condition `TAX_COEFF = 1.0` was measured at, so excluding them would double-subtract |
| Y295 | CONFIRMED | arithmetic on both itemisations plus the file magnitudes | 75 + 25 + 5 + 5 + 15 = **125** and 75 + 25 + 5 = **105**, and the four magnitudes I could locate are file-exact (core 0.75, city 0.25, iqta 0.05, GRA ideas 0.15). The engine's multiplier being the sum of the itemised percentages is also what the ledger requires: the tax mode is exactly 1.0 x base_tax for a cored city with nothing else |
| Y296 | CONFIRMED | engine-ledger test, no tooltip | 0.75 + 0.25 = 1.00, and the engine's own ledger confirms the consequence directly: annualised taxation income per point of country `base_tax` has **mode exactly 1.0 over 665 countries** (518 of them), e.g. ATH 10 -> 0.833/month, BOS 21 -> 1.750/month. `TAX_COEFF = 1.0` is the right reference value |
| Y072 | CONFIRMED | read `province_table` | `tax=TAX_COEFF * s["base_tax"] * (1.0 + tmod)` is applied to every row it emits, with no core/city/ownership branch |
| Y297 | CONFIRMED | algebra | if the reference condition already includes core + city = 1.00 and the model then multiplied by 1.75 or 1.25, the same term would be counted twice |
| Y073 | CONFIRMED | read §2.3's TAX_COEFF row | "Two provinces, two development levels, from the `(Yearly ...)` parenthetical: Garnatah `base_tax` 6 ..., Caceres `base_tax` 2 ..." — two readings, both on cored city provinces, is exactly what it rests on. (This audit adds a much wider base: 665 countries' ledgers) |
| Y074 | CONFIRMED | scanned the counted provinces for the maximum `base_tax` and summed that province's development | province **1821** is the unique province at `base_tax = 15`, and its `base_tax + base_production + base_manpower = 33` |
| Y298 | CONFIRMED | read the counting predicate | `if not s.get("owner"): continue` then `node = PNODE.get(pid); if node is None: continue` — an owner and a trade node, nothing else |
| Y299 | CONFIRMED | algebra over the wealth expression | the only inputs that can move `c(n,g)` are development, the trade good, prices and the condition modifiers; the owner tag appears only in the counting predicate, so a conquest that does not devastate, besiege or occupy leaves the demand vector fixed |
| Y075 | CONFIRMED | checked that the aggregate reads the same field | `val5_agg`/`measure6` build `c_w` from the identical `W = tax + prod_income` array that the per-good `c(n,g)` uses, so every owner-dependence removed from wealth is removed from `Phi_w` as well |

---

## §1.4 — Market concentration (5 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y300 | CONFIRMED | read the alpha function in `flowop.py` / `measure6.py` and §2.3's constant | `ALPHA = lambda g: max(0.2, min(3.0, (PRICES[g] / 2.0) ** 1.0))` — `clamp((price/P0)^k, alpha_min, alpha_max)` with **P0 = 2.0**, k = 1, alpha_min = 0.2, alpha_max = 3.0, and §2.3 states "the alpha price anchor `P0 = 2.0`" |
| Y301 | CONFIRMED | algebra, plus the realised alpha values | for alpha > 1, `x^alpha` is convex, so a province of twice the wealth takes more than twice the demand share: luxuries concentrate on individually rich provinces. Realised: gems 2.0, cloves and coal 3.0 (clamped) |
| Y302 | CONFIRMED | algebra | at alpha = 1 the numerator is `sum_p wealth(p)`, so demand is proportional to the node's economic size |
| Y303 | CONFIRMED (unreachable on vanilla) | algebra, plus the realised alpha range over the shipped price table | for alpha < 1 the map is concave, so many modest provinces outweigh a few rich ones. Worth recording: over the 30 priced goods alpha runs **1.00 to 3.00** — the cheapest good sits exactly at `P0`, so the sublinear regime and `alpha_min = 0.2` are never reached on the vanilla table. The conditional is true; nothing exercises it |
| Y304 | CONFIRMED | counted signed `change_price` values over `events/`, `decisions/`, `missions/`, `common/`, `history/`; checked the model for a smoothing term | **121 positive and 40 negative** `change_price` blocks (values -0.75 to +1.5), so vanilla price events move prices in both directions; and alpha is recomputed from the current price with no filter, average or hysteresis anywhere in the expression |

---

## §1.5 — Goods without a graph (20 claims)

| ID | Verdict | Method | Evidence |
|---|---|---|---|
| Y305 | CONFIRMED | read `solver.py`'s exclusion set and §2.3's design-constants list | `EXCLUDED = {"gold", "unknown"}` and `GOODS = sorted(g for g in PRICES if g not in EXCLUDED)`; §2.3 lists "the excluded-goods list (defaults to gold)". Configuration, not a special case in the algorithm |
| Y306 | CONFIRMED | grepped the localisation for the income categories, `defines.lua` for the constant, and the script scopes for the field | `core_l_english.yml:106: INCOMEGOLD:0 "Gold"` sits in the income-category block beside `INCOMETAX` and `INCOMETRADE`, and `text_l_english.yml:2418: INCOMEPROD:0 "Production"` is a separate category — so gold is not booked as production income. `gold_income` is a scriptable field (used in `common/achievements.txt`), and `defines.lua:1137: GOLD_MINE_SIZE = 40, -- Base income from gold mines` (plus `GOLD_MINE_SIZE_PRIMITIVES = 4`) |
| Y307 | CONFIRMED | read the wealth expression for any income input | `wealth(p) = TAX_COEFF*base_tax + GP_COEFF*base_production*(1+gmod)*price` — no income field of any kind is read, so gold income cannot reach demand by any route |
| Y308 | CONFIRMED | read `common/prices/00_prices.txt` | `gold` carries `base_price = 0.0` and `goldtype = yes`; with a zero price its trade value is identically 0, so excluding it costs nothing |
| Y309 | PARTIAL | tried to resolve the cross-reference: listed §2.7's item numbers, then traced the probe back through v5 and v2 | the substance holds — nothing in the model reads a production-income field (Y307), so the question is moot for this model. But the pointer is stale and the conclusion is wrong in one respect. §2.7 now numbers **1-11 and 16** — there is no item 12. v2's §2.7 item 12 was the probe ("**Per-province gold.** Open one gold province's Production income tooltip: does the per-province field carry the gold figure ...") and it is indeed gone. However the same question survives as **§2.7 item 9, "Diverted gold. Does diverted colonial gold still appear in the per-province production income field?"**, still listed as a probe to run, so it is not true that the question was dropped rather than run |
| Y310 | CONFIRMED | read `build_sc`'s live mask and `V_g` | `live = world > 0` and `S[gi]` stays all-zero for a dead good; `V = PRICES[g] * world[gi]` is 0 when `world[gi]` is 0. Measured: 29 live goods of the 30 priced non-gold goods, coal being the dead one |
| Y311 | CONFIRMED | algebra over the same code | the mask is recomputed from the current `goods_produced` field every solve, so the first month a province produces the good it enters `live`, gets an `S` row, a non-zero `V_g` and a graph |
| Y312 | CONFIRMED | inspected the engine's province model | `trade_goods` is a single-valued province field in both `history/provinces` and the save's province records (one string, never a list), so activation replaces rather than adds |
| Y313 | CONFIRMED | algebra over `S` | `S[gi] = gp[gi] / world[gi]` is a share, so changing one province's good changes both goods' denominators and hence every producing node's share of both |
| Y314 | CONFIRMED | algebra plus the coal experiment | `wealth(p)` contains `price(good(p))`, and one wealth field feeds every good's `c(n,g)`. Measured: repricing the latent-coal provinces moves world wealth by +214.60 and moves the aggregate orientation, so the coupling is real |
| Y315 | CONFIRMED | read the `V_g` definition | `V = PRICES[g] * world[g]`, so both the losing and the gaining good's weights move; and §1.6/§1.7 use `V_g` for display, link value and AI score |
| Y316 | CONFIRMED | ran the coal counterfactual through the aggregate | `Phi_w` moves: **16 of 159** edges flip. §1.6 does build `Phi_w` by running DRAIN on the same wealth field, so activation reaches it |
| Y317 | CONFIRMED | compared the coal activation's effect with a development change | +214.60 ducats on a 10,607.40 field (2.0%) and 16 of 159 edges — the same order as the development and conquest scenarios §1.6 records, so "entitled to move" is consistent with how the model treats those |
| Y076 | CONFIRMED | re-derived the latent-coal set from `history/provinces`, re-priced the owned members and re-ran the aggregate | latent-coal provinces **58**, of which **45** are owned and counted; repricing them gives world-wealth delta **+214.60** and **16 of 159** edge flips. All three figures reproduce, and match `measure6.out` |
| Y077 | CONFIRMED | ran both counterfactuals — devastation retained and devastation dropped for province 4237 | 4237 is in both sets (latent-coal and the devastated eleven). Devastation retained: delta +214.60, 16 flips. Devastation dropped: delta +217.00, **16 flips**. The difference is exactly **2.40** ducats and **no additional edge moves** — both halves of the parenthetical reproduce, including the point that the edge count does not notice |
| Y318 | CONFIRMED | read the whole shipped price table | 32 price blocks; `coal` is `base_price = 10.0`, the maximum (next: cloves 8.0, then four goods at 4.0). Highest in the table |
| Y319 | CONFIRMED | read v2's §1.5 | v2's text reads "`Phi_w` reads wealth, not goods, and is unaffected" — verbatim the proposition described. It was consistent with `Phi_ord` (where a latent good's `V_g = 0` gives it no weight) and is false for `Phi_w`, which the 16-flip measurement demonstrates |
| Y320 | CONFIRMED | counted coal producers in the history parse and in the save | **0** provinces have `trade_goods = coal` at 1444 in either source, and `build_sc` marks coal not-live |
| Y321 | CONFIRMED | read coal's `trigger` block in `00_tradegoods.txt` | `is_latent = yes`; the trigger's first clause is `OR = { development_discounting_tribal = 20 / owner = { innovativeness = 20 } }`; then the default `if` branch (taken when neither the `GER_specific_coal` province flag nor the `earlier_coal_available` country flag is set) requires `provincial_institution_progress = { which = enlightenment value = 100 }` and `owner = { has_institution = enlightenment }`. The two Manufactories branches are the `else_if`/`else` reached only via those flags. Every element matches |
| Y322 | CONFIRMED | counted `latent_trade_goods` containing coal across `history/provinces` | **58** provinces, and conversion is per province through the trigger above (each needs its own institution progress at 100), so the set converts over years rather than in one tick |

---

# Summary

## Counts by verdict

| Verdict | Count | Share of 222 |
|---|---:|---:|
| CONFIRMED | **203** | 91.4% |
| PARTIAL | **13** | 5.9% |
| REFUTED | **3** | 1.4% |
| UNTESTABLE | **3** | 1.4% |

| Section | Claims | CONFIRMED | PARTIAL | REFUTED | UNTESTABLE |
|---|---:|---:|---:|---:|---:|
| §0 | 48 | 40 | 5 | 1 | 2 |
| §1.1 | 65 | 61 | 3 | 0 | 1 |
| §1.2 | 6 | 5 | 1 | 0 | 0 |
| §1.3 | 78 | 73 | 3 | 2 | 0 |
| §1.4 | 5 | 5 | 0 | 0 | 0 |
| §1.5 | 20 | 19 | 1 | 0 | 0 |
| **Total** | **222** | **203** | **13** | **3** | **3** |

**REFUTED (3):** `Y016`, `Y057`, `Y983`.

**PARTIAL (13):** `Y973`, `Y011`, `Y217`, `Y015`, `Y018` (§0); `Y229`, `Y250`, `Y978` (§1.1);
`Y274` (§1.2); `Y050`, `Y981`, `Y293` (§1.3); `Y309` (§1.5).

**UNTESTABLE (3):** `Y208`, `Y214` (§0); `Y249` (§1.1).

Two rows are CONFIRMED with a caveat worth carrying rather than a downgrade: `Y303` (the sublinear
alpha regime is real algebra but unreachable on the vanilla price table, where alpha runs 1.00-3.00)
and `Y234` (the interior-point cycle argument is sound, but scipy's `highs-ipm` runs crossover and
the tie-break makes the optimum unique, so I could not exhibit the failure empirically).

## The three refutations

**`Y016` — "`coverage6.py` is the honest measure — it corrupts each spec-printed figure whether the
harness looks at it or not."** It does not. Its universe is the 60 figures `measure6.py` computes,
and within that it mutates only the ones whose rendering appears **exactly once** in the document.
Its own output says so: "60 computed figures; **9** of them appear verbatim in the spec",
"coverage: 6 of 9 uniquely-locatable spec figures are protected (67%)", and then 23 further figures
listed as "unscored rather than assumed protected". The several hundred numeric tokens the document
prints that `measure6.py` does not compute are never touched. It is an honester denominator than
`mutate6.py`'s — that part of the sentence is fair — but it is not the document's figures.

**`Y057` — "16 are authored in `history/provinces` at integer 5/8/10/15 ... and the remaining five
are all Shirvan-owned and receive theirs at runtime, so reading them needs the save."** Three errors
in one sentence. The five (1071 Tara, 1074 Sibir, 1076 Kurgan, 4689 Om, 4690 Ishim) **are** authored
in `history/provinces`, as `revolt_risk = 15` in the **undated** block, with a `revolt_risk = 0` in a
1468 block the start date never reaches — so nothing about them needs the save. Their owner is
**Shaybanid** (`SHY`, `common/country_tags/00_countries.txt` -> `countries/Shaybanid.txt`), not
Shirvan. And Sofala, whose comment the sentence quotes as its example, is not one of the 21 at all:
its `unrest = 8` sits in a **1515.1.1** block. What does reproduce exactly is the 16/5 split by
*key* — 16 provinces carry `unrest` at integer 5/8/10/15, five carry `revolt_risk = 15` — which is
almost certainly where the error came from: a history parser that searched for `unrest` only would
see 16 authored and five unexplained.

**`Y983` — "even at the start date a quarter of the revolt risk is owner-derived, and during a
campaign that share only grows."** The premise is `Y057`'s and falls with it: all 21 are authored in
the province history. The save does show a uniform owner-side shim — every one of the 21 reads its
authored integer **minus 0.166** — but that is 1-2% of each value, not a quarter of the total. (The
forward-looking half, that the share grows in play, cannot be tested from a start-date save.)

## What the partials turn on

* `Y973` — `measure6.py` prints **60** labelled figures, not 59; 59 is what it prints when the sink
  set has one member, i.e. at alpha = 1.5. The numerator does not reproduce either: v6.0 -> v6.1
  moves 31 of 62 labels, or 26 counting only same-label value changes; alpha alone moves 23.
* `Y978` — the realised cost spread is **0.0928%** of the base cost, under a tenth of a percent as
  claimed; but the interval the same sentence quotes, `[1, 1 + TIE_EPS + TIE_EPS2]`, is **0.1001%**
  wide, which is not. True of the field, false of the bound it was derived from.
* `Y229` — Phase 1's demand-mass quantile `rho` is **not implemented** in `drain.py`: there is no
  parameter and no mass filter. Harmless at its stated default of 1.0, but the section credits the
  phase with a knob the reference solver does not have.
* `Y250` — `measure6.py` regenerates three of §1.1's measurements (acyclicity, sinks per good,
  fallbacks fired) and none of the others: the reachability figure, the scan-invariance figures, the
  2,320-node key-collision count, the sink-set **equality** and Phase 0's no-op are all absent from
  it. They are reproducible — `val5_pergood.py` does it — but not by the script the section names.
* `Y050` and `Y981` — "four of the five are applied" is true of `solver.py`'s tables and false of its
  code path. `province_table()` reads only `devastation`; `prosperity`, `under_siege` and `occupied`
  sit in `STATE_GOODS_MOD`/`STATE_TAX_MOD` with no input feeding them. `Y050` also over-claims
  exhaustiveness: `expanded_infrastructure` is province-scoped and carries **both** wealth keys.
* `Y274` — "there is no regularizer" is true of every shipped call site (all pass `eps=0.0`) and
  false of the shipped function, whose signature is still `build_sc(alpha_of_good, eps=1e-6)`.
* `Y018` — the circularity claim is exactly right, but `mutate6.py` cannot report a score at all:
  it dies with `KeyError: 'band containing alpha=1.5'`, a key that moved when alpha_Phi did.
* `Y011` — the rejected-operator figures were re-measured in three audits but not re-refuted; v5
  graded `Phi_ord`'s 60.3% **CONFIRMED**.
* `Y217` — several measured figures carry no script: §0's 105.30 / 10,712.70, §1.3's 12.23 / 9.40 /
  12.70 and the 89 = 43 + 31 + 16 - 1 census.
* `Y015` — the ill-defined denominator is real (my tokenisers give 1,167-2,401 occurrences and
  178-344 distinct values) but the stated 279-326 does not reproduce; my nearest definitions give
  314 and 329.
* `Y293` — `Reform Iqta +5%` and `national ideas +15%` reproduce from files; `Clergy +5%` is a
  scaled 0.2 estate modifier, not a file constant; the `+2%` technology term was not located.
* `Y309` — the substance holds (nothing in the model reads a production-income field) but the
  cross-reference is stale: §2.7 numbers **1-11 and 16**, and the question survives as **item 9**,
  "Diverted gold ... does diverted colonial gold still appear in the per-province production income
  field?", still listed as a probe to run.

## What I could not settle, and what would settle it

* `Y208` (extended-timeline compatibility) — needs the emitter built and run on a non-1444 start.
  There is no DLL and no `.mod` yet.
* `Y214` (every settleable v1 claim-audit correction folded through) — needs a v1-to-v6
  claim-by-claim mapping. `fixes-agreed.md` maps v5's 63 findings only; v1's audit has 685 rows.
* `Y249` (four over-claims caught between v2.0 and v3.0) — needs a v2-to-v3 over-claim ledger.
  `validation-v3.md` grades the *discipline* ("### W010, W011 — CONFIRMED (the discipline itself)")
  and never enumerates the four.
* The four in-game tooltip **strings** behind `Y041`, `Y044`, `Y046`, `Y049`, `Y288` and `Y293` were
  not re-read this session; EU4 was not launched. Everything they are used for was settled instead
  from the engine's own save ledger, the localisation tables and arithmetic, and all of it agrees
  with the quoted readings. The one place a file could not corroborate every term is `Y293`'s
  itemisation, so that is the only claim in this slice where a fresh tooltip would add anything.

## Notes for the next round

1. **The tooltip claims no longer need a tooltip.** `lastmonthincometable` in any non-ironman save
   gives per-country taxation (index 0) and production (index 1) income. Over 665 countries the
   annualised tax per point of `base_tax` has mode exactly **1.0** (518 of them; ATH 10 -> 0.833/mo,
   BOS 21 -> 1.750/mo), and the production analogue has mode exactly **1.0** against
   `0.2 * base_production * price` (278 of 663). That settles `TAX_COEFF`, `GP_COEFF`, the shared
   annual-over-twelve basis and the base-then-percentage ordering from a primary source, with no OCR.
2. **The `devastation` scaling law is no longer wiki-only.** §1.3 flags that row as the one resting
   on community documentation. In `Castile1444_12_22.eu4` BOH's production income fits
   `-2 x level/100` (ratio 1.076, against a CAS control of 0.996) and rejects `-1 x level/100`
   (0.616) and no scaling (0.432). The document can cite the save instead of the wiki.
3. **The start save's `lastmonthincome` predates `on_startup`.** At 1444.11.11 BOH's ledger still
   shows undevastated production, so any ledger check that depends on start-state events must use
   the later save.
4. **Two shipped-script defects that distort figure counts.** (a) `mutate6.py` aborts **on the
   spec** with `KeyError: 'band containing alpha=1.5'` — a literal key at line 31 against
   `measure6.py`'s computed `band containing alpha=2`; `verify6.py` line 122 already derives it from
   `measure6.A_PHI` and is the pattern to copy. Run with no argument and you get the other path
   entirely: the 10-entry typed `CHECKLIST` against `../fixes-agreed.md`, which passes 10 of 10 and
   says nothing about the spec. (b) `measure6.py` emits the label `route genua -> hangzhou` twice —
   line 182 inside the `for s_ in ("genua", "north_sea", "english_channel")` loop and line 184 as a
   literal — so the second `P()` overwrites the first in `OUT`, which is why `measure6.out` records
   that row as `None` while stdout shows 61 lines against 60 keys. Fix the emission, not the label.
5. **New instruments left in `scripts/`:** `val5_save.py`, `val5_hist.py`, `val5_agg.py`,
   `val5_pergood.py`, `val5_relabel_pg.py`. The last is the only implementation of the per-good
   relabelling experiment §0 and §2.4 item 1 quote; it validates itself against `drain.py` on the
   identity permutation for all 29 goods and aborts if that fails.

**Spec MD5 at the end of the pass: `59c84a97799db9db97fe889b6e3c6776` — unchanged from the start.**
