> **QUARANTINED — produced under a steered prompt. Do not use as the inventory.**
>
> The brief that produced this asked the extraction agent for two things extraction must never be
> asked for: a list of measured claims lacking an instrument, and a hunt for internal
> inconsistencies. Both are evaluation, and mixing evaluation into extraction destroys the
> extract-then-validate separation this project is built on. The census tables below may be sound;
> they were produced alongside instructions that were not, so they are not trusted as the canonical
> inventory. Superseded by a clean pass.

# Claims Delta — v6.1 census → v6.2 document

## Header

**Current document.** `per-good-trade-spec.md`, **2,063 lines**, MD5 **`a95c71c0c9db8bc65cbbc24b2ba6ca58`**,
self-identifying at line 3 as **Version 6.2**. Both figures match the brief.

**Census compared to.** `claims-v6.md` (1,566 lines, MD5 `b95f98345e1679f49a03581fac8778f7`), the
twelfth inventory, taken against the spec at **1,979 lines**, MD5 `59c84a97799db9db97fe889b6e3c6776`,
self-identifying as v6.1. Both match the brief.

**ID range found in the census.** Read off the file, not taken on trust: **`Y001`–`Y1057`**,
**1,049 rows**, every ID unique. Exactly eight numbers in that span are absent — `Y014`, `Y088`,
`Y089`, `Y090`, `Y092`, `Y101`, `Y142`, `Y145` — which are the eight the brief lists as retired. They
stay retired here and none is reused. The highest ID the census actually uses is **`Y1057`**.

**First new ID assigned: `Y1058`.** New propositions run **`Y1058`–`Y1137`**, in document order.

**What the 1,049 census rows are.** **894** are propositions live in the v6.1 document. **155** were
already `REMOVED` when the census was written — v5.0 propositions superseded before it, carried under
`(v5)` section markers with v5.0 line numbers. Those 155 have no counterpart in v6.2 either, so their
status is unchanged; they are kept in a separate block of the REMOVED table so the **15** propositions
*this* edit removed are not buried among them.

**Counts.**

| Status | Count |
|---|---|
| UNCHANGED | 825 |
| REWORDED | 3 |
| CHANGED | 51 |
| REMOVED — by this edit | 15 |
| REMOVED — already absent before this edit | 155 |
| NEW (`Y1058`–`Y1137`) | 80 |
| **Total rows** | **1,129** |

894 live v6.1 rows = 825 UNCHANGED + 3 REWORDED + 51 CHANGED + 15 REMOVED. 1,049 carried + 80 new = 1,129.

**Corrections to the brief.** None on the two files. The brief is right about the document (2,063
lines, MD5 `a95c71c0c9db8bc65cbbc24b2ba6ca58`, v6.2), about the census (1,979 lines, MD5
`59c84a97799db9db97fe889b6e3c6776`, v6.1) and about the eight retired IDs. One correction to the
**pre-existing `claims-delta-v62.md`**, which the brief told me to treat as untrusted and overwrite:
it was written against a *different* state of the document — it records 2,078 lines and MD5
`706a092fbb1961c501799c618b235e89` — so none of its line numbers and none of its figures were carried
over. It is overwritten in full.

## Method notes

- **IDs are matched by text and meaning, never by locator.** The document shifted +84 lines overall and
  non-uniformly. Measured section-by-section: §0 **+22**, §1.1 **+13**, §1.3 **+7**, §1.6 **−4**,
  §1.10 **+5**, §2.1 **−2**, §2.3 **+14**, §2.9 **+3**, §3.2 **+3**, §3.6 **+7**, §3.9 **−1**,
  §3.13 **+18**, §3.15 **−1**, and every other section 0.
- **Four sections changed content at zero net line delta** and were diffed by text rather than by count:
  **§2.8** (the calibration spice/cloves row, the barbell percentages, the razed-China flip count, the
  tolerance row, one deleted v2 attribution), **§3.10** (the five-node residual measurement withdrawn),
  **§2.4** and **§2.7** (checked line by line; no change found). §2.1's two-line loss is a reflow of one
  paragraph, with content changes in the fingerprint and free-vs-flow table rows.
- **`Φ_ord` is gone from the document.** The symbol appears nowhere in v6.2; the census uses it in
  nine claim cells. Where the surrounding proposition is otherwise identical the row is filed
  REWORDED; where a figure or a sub-claim went with it, CHANGED or REMOVED.
- **REWORDED is only partly recoverable from these two files.** The census records paraphrases, not the
  document's wording, so a pure wording change with no change of assertion usually leaves nothing to
  compare against. Three rows are filed REWORDED — the ones where the census cell preserves a
  distinctive token the current document no longer uses. The true count is higher and is not
  recoverable from the two files named in the brief.
- **A script attribution added or removed is filed CHANGED** where the census's provenance cell is
  explicit that no instrument was named. Five scripts appear in the current document that appear
  **nowhere** in the census — `round6.py`, `props6.py`, `apparatus6.py`, `fingerprint6.py` and
  `scripts/redtest6.py` — while the census does name every script the v6.1 document named
  (`measure6.py`, `relabel6.py`, `europe.py`, `epsilon6.py`, `toys.py`, `flowop.py`, `drain.py`,
  `pdx.py`, `verify.py`, `solver.py`, `coverage6.py`, `mutate6.py`, `verify6.py`). All five exist in
  `scripts/`.
- **Types are re-assigned to the brief's vocabulary by rule**, since the census uses a different one
  (MODEL / DESIGN / INSTALL / ENGINE / MATH): a claim about the audit, the harness, this document or a
  prior version of it → `PROCESS`; otherwise a claim whose census provenance is `numerical test` or
  `computed by a named script` → `MEASURED`; otherwise census `INSTALL`/`ENGINE` → `ENGINE`; otherwise
  census `MODEL`/`MATH` → `MODEL`; otherwise `DESIGN`. Resulting live distribution: MODEL 308,
  DESIGN 192, ENGINE 184, MEASURED 143, PROCESS 67.
- **The `line` column for UNCHANGED rows is computed.** Every row in the twelve sections whose length
  changed carries an explicitly re-read line; rows in the zero-delta sections carry the census locator
  plus that section's constant offset, which is exact. Treat UNCHANGED lines as accurate to ±2; CHANGED,
  REWORDED and NEW lines were read off the current file directly.
- **The UNCHANGED table is compressed** to ID / § / short label / type / line, as the brief permits. It
  is the last table, because it is 825 rows long.
- **Two header lines are not enumerated**, following the census, which carries no row for `**Version:**`
  or `**Status:**`. The version bump 6.1 → 6.2 is recorded in this delta's header instead.

---

## CHANGED (51)

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y010 | §0 | The rejected-operator convention names which operators lose their measurements. | CHANGED | **old:** covers `Φ_ord`, the gravity kernels, the v1 Laplacian, RANK and the seeded basins. **new:** covers the gravity kernels, the v1 Laplacian, RANK, the seeded basins "and anything else the section rejects" — `Φ_ord` is no longer named. | DESIGN | stipulated | 67 |
| Y012 | §0 | Every graded claim from `validation-v5.md` is folded through and `fixes-agreed.md` maps each one. | CHANGED | **old:** 22 refuted, 39 partial, 1 unverifiable; `fixes-agreed.md` maps each one to the change that answers it. **new:** adds "62 in all" and "carries a row for all 62". | PROCESS | `../v5-owner-agnostic/validation-v5.md`, `fixes-agreed.md` | 76 |
| Y973 | §0 | How many of `measure6.py`'s printed figures move with the `α_Φ` change. | CHANGED | **old:** 29 of the 59 figures `measure6.py` prints move with the sink set. **new:** "A count was quoted here. It is not maintained: `measure6.py`'s figure list grows whenever a figure gains a guard, so the count moved for reasons that had nothing to do with `α_Φ`." | PROCESS | `measure6.py` named, but for why the count is not maintained rather than for a count | 45 |
| Y229 | §1.1 | Phase 1's knobs and their defaults. | CHANGED | **old:** two knobs — a demand-mass quantile `ρ` defaulting to 1.0 and a cluster dilation radius `r` defaulting to 0. **new:** one knob — `r` (default 0), which links demanders within `r` hops before clustering; `ρ` is withdrawn as not a parameter of the shipped operator. | MODEL | stipulated; `drain.py` named for the withdrawal | 121 |
| Y978 | §1.1 | The bound on the fewest-hop approximation. | CHANGED | **old:** at those values the cost spread is under a tenth of a percent of the base cost, so the routing is within that factor of fewest-hop. **new:** "The bound is that interval itself, which is what an implementer needs; no percentage is derived from it, because the spread relative to the base cost is a restatement of `TIE_EPS` and not a second fact." | MODEL | derivation over the LP objective | 221 |
| Y033 | §1.3 | The dropped apparatus was live on 89 of the 2,472 counted provinces (43 `gems` + 31 `incense` + 16 great-project/permanent-modifier, less province 542). | CHANGED | **old:** figures stated with no script named at this line. **new:** same figures, now attributed — "These figures are reproduced by `apparatus6.py`, which holds the deleted classifier's constants **frozen**". | MEASURED | `apparatus6.py` (L276), imported by `measure6.py` (L279) | 270 |
| Y037 | §1.3 | The tax term of the wealth formula. | CHANGED | **old:** `tax_value(p) = TAX_COEFF · base_tax(p) · (1 + Σ province-state tax modifiers)`. **new:** `tax_value(p) = TAX_COEFF · base_tax(p)`. | MODEL | stipulated | 286 (restated 49–50, 945) |
| Y050 | §1.3 | How many province-condition static modifiers the table carries and what they reach. | CHANGED | **old:** five static modifiers describe a province's own state, all five defined in `00_static_modifiers.txt`, four applied, `unrest` excluded. **new:** "Four static modifiers are applied, all four defined in `common/static_modifiers/00_static_modifiers.txt`, and **all four reach `goods_produced`**. A fifth, `unrest`, is defined in the same file and is deliberately not read." | ENGINE | `common/static_modifiers/00_static_modifiers.txt` | 332 |
| Y051 | §1.3 | The condition-modifier table's rows and their targets. | CHANGED | **old:** `occupied` −0.5 plus `local_tax_modifier = -0.5`, entering **both** `goods_produced` and the tax term. **new:** `occupied` enters `goods_produced` only — "the tax half is granted by the file and **not read**". The `unrest` row is deleted from the table (see `Y052`). | ENGINE | `common/static_modifiers/00_static_modifiers.txt` | 338 |
| Y292 | §1.3 | `unrest`'s per-point scaling convention in the shipped file. | CHANGED | **old:** the `unrest` block's own comment reads `#10% longer time to build troops for each rr`, so its values apply per point, and the neighbouring `nationalism` block uses the same convention. **new:** reduced to a clause inside the `devastation` note — "`unrest` and `nationalism` both carry per-unit comments in it". | ENGINE | `00_static_modifiers.txt` | 341 |
| Y053 | §1.3 | Which modifiers touch the tax term. | CHANGED | **old:** `occupied` and `unrest` touch the tax term; the other three reach `goods_produced` alone. **new:** "**No modifier reaches the tax term at all.** `tax_value` is a direct function of `base_tax`, and all four rows above enter `goods_produced`." | MODEL | derivation | 346 |
| Y981 | §1.3 | What `solver.py`'s `STATE_TAX_MOD` contains. | CHANGED | **old:** carries `occupied` alone, so four of the five rows in the table are applied. **new:** is **empty**, and is kept as an empty declaration rather than deleted so the shape of the exclusion stays legible in the code. | MODEL | `solver.py` | 350 |
| Y055 | §1.3 | What excluding `unrest` costs. | CHANGED | **old:** 12.23 ducats, 0.115% of the 10,607.40 world wealth reading it from the save, or 9.40 ducats, 0.089% reading only the authored 16. **new:** "*No figure is quoted for what the exclusion costs, and none should be reconstructed.*" | PROCESS | stipulated | 372 |
| Y079 | §1.6 | What the sink count does as Europe is scaled. | CHANGED | **old:** at `α_Φ = 2.0` the 1444 field gives two sinks and a modestly grown Europe gives two, three or five. **new:** "scaling European development alone takes the count through **two, three, four and five** before settling back at two". | MEASURED | unsourced at this line | 521 |
| Y099 | §1.6 | What §3.9 records about the agreement figure. | CHANGED | **old:** the superseded marking-order aggregate scored higher on that measure, and §3.9 records why the trade was taken while maintaining no figure for it. **new:** "§3.9 records what that agreement is and is not evidence for." | DESIGN | stipulated | 586 |
| Y109 | §1.6 | The European-scaling experiment and its published interval table. | CHANGED | **old:** bisected boundaries, sink set constant over ten named intervals from ×1.00 to ×2.50, with the ten sets listed. **new:** "sampled uniformly on a 0.001 grid from ×1.000 to ×2.600"; the interval table is withdrawn (see `Y1091`). | MEASURED | `europe.py` | 617 |
| Y110 | §1.6 | What the European-scaling experiment is not evidence for. | CHANGED | **old:** "the row boundaries are a property of one synthetic experiment". **new:** "The intent is the claim; the interval quoted above is a property of one synthetic sweep", with "real growth is province by province, with price changes and colonisation on top" added. | DESIGN | derivation | 634 |
| Y111 | §1.6 | The non-monotonicity of the European-scaling path. | CHANGED | **old:** `hangzhou` leaves at ×1.19, returns at ×1.95 and leaves again; `gulf_of_siam` holds an end across ×1.19–×1.38; two intervals narrower than ×0.03. **new:** the multiples are dropped — "leaves, returns and leaves again", "over one stretch", "several intervals narrower than ×0.01". | MEASURED | unsourced at this line (`europe.py` named at L617) | 623 |
| Y119 | §1.6 | The node-scaling results for the 18 and the 22 European nodes. | CHANGED | **old:** sole `genua` from about ×1.55; scaling all 22 gives no sole sink below ×4, the eastern four keeping ends of their own. **new:** sole `genua` from **×1.52**, staying sole continuously to ×3.60 (the top of the range swept); all 22 gives no sole sink below **×25**, and from about ×2.50 the set is `{genua, rheinland}`. The eastern-four clause is deleted (see `Y1094`). | MEASURED | unsourced at this line | 675 |
| Y1012 | §2.1 | There is no randomness in the solve. | CHANGED | **old:** identical output fingerprint over repeated runs, separate processes and five `PYTHONHASHSEED` values, no instrument named. **new:** same, now attributed — "(`fingerprint6.py`, one SHA-256 over `Φ_w` and all 29 per-good graphs including sinks, sources, promotions, fallbacks and the Phase-2 objective)". | MEASURED | `fingerprint6.py` | 905 |
| Y1015 | §2.1 | The free-versus-flow classification margin. | CHANGED | **old:** 2,321 edge-goods at exactly 0 and 2,290 above 1e-6, with nothing between; no instrument named. **new:** same, plus "the smallest non-zero magnitude being 6.94e-06", attributed to `round6.py`. | MEASURED | `round6.py` | 909 |
| Y129 | §2.2 | Solver item 4's per-province wealth formula. | CHANGED | **old:** `TAX_COEFF · base_tax · (1 + province-state tax modifiers) + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`. **new:** `TAX_COEFF · base_tax + GP_COEFF · base_production · (1 + province-state goods modifiers) · price`, with "The tax term takes no modifier at all." added. | DESIGN | stipulated | 943 |
| Y130 | §2.2 | How many condition modifiers are in scope and which are live at 1444. | CHANGED | **old:** five in scope, four applied; `devastation` live on eleven provinces and `unrest` on twenty-one, `unrest` not read. **new:** four in scope, all four reaching `goods_produced`; only `devastation` live, on eleven provinces; `unrest` defined in the same file and not read. | MEASURED | unsourced at this line | 946 |
| Y480 | §2.3 | DRAIN's knobs at their defaults. | CHANGED | **old:** three knobs — `ρ = 1.0`, `r = 0`, zero-flow tolerance `1e-11`. **new:** two knobs — `r = 0` and the zero-flow tolerance `1e-11`; `ρ` withdrawn as not a parameter of the shipped Phase 1. | MODEL | stipulated | 1064 |
| Y481 | §2.3 | The status of the zero-flow tolerance. | CHANGED | **old:** it is an absolute threshold, so it couples to the scale of `b`. **new:** "That tolerance is an **absolute** threshold rather than a relative one; §3.13 records why that is settled rather than open." | MODEL | derivation, cross-referred to §3.13 | 1065 |
| Y482 | §2.3 | What the §3.13 calibration option changes. | CHANGED | **old:** moves all three knobs plus α's clamp. **new:** "replaces Phase 1, moves the zero-flow tolerance and removes α's clamp". | DESIGN | stipulated | 1068 |
| Y999 | §2.3 | Why a structured second-order term was rejected. | CHANGED | **old:** because it makes all 159 arc costs distinct where the shipped cost leaves 3 pairs equal, and still leaves 72 of 232 per-good supports moving. **new:** "Both costs make **all 159 edge costs distinct**, so distinctness cannot be what separates them"; the difference is that the absolute-difference term **telescopes**; measured, the structured term leaves **11 of 29** goods admitting an alternative optimum against the shipped term's **1** (`paper`). | MEASURED | `round6.py` | 1104 |
| Y1038 | §2.3 | What the choice of normalisation moves. | CHANGED | **old:** across the three normalisations (maximum, mean, world total) the aggregate `Φ_w` is unchanged, 0 of 159 edges differing, but 5 of the 29 per-good graphs differ. **new:** dividing by the **world total** moves the aggregate `Φ_w` by **7 of 159 edges**, and across all candidates **13 of the 29** per-good graphs move under at least one. | MEASURED | unsourced at this line | 1148 |
| Y1056 | §2.3 | 1e-8 already gives 0 flips and is the first value below `copper`'s 3.765e-8 margin. | CHANGED | **old:** stated with no instrument named. **new:** same figures, now attributed to `round6.py`. | MEASURED | `round6.py` | 1125 |
| Y538 | §2.8 | Where the calibration puts the spice and cloves sinks. | CHANGED | **old:** under the α-calibration `spices` sinks at Genoa alone and `cloves` moves to Deccan, so the v1 expectation is not recovered by the calibration either. **new:** `spices` sinks at `doab` and `genua`, and `cloves` moves to a Chinese node, `beijing`; the expectation is met by **no single good** — the calibration puts a Chinese end on cloves and a European one on spices, in two different graphs. | MEASURED | unsourced at this line | 1333 |
| Y152 | §2.8 | The high-demand-node barbell. | CHANGED | **old:** 19.8% among each good's top eight demanders (46 of 232) against 6.9% among its bottom eight (16 of 232). **new:** **19.4%** (45 of 232) against **7.3%** (17 of 232), attributed to `round6.py`, with "the two constructions differ and only this one gives these figures" added. | MEASURED | `round6.py` | 1334 |
| Y154 | §2.8 | The razed-China flip count. | CHANGED | **old:** 30 of 159 edges flipping. **new:** **32 of 159**, attributed to `round6.py`. | MEASURED | `round6.py` | 1338 |
| Y543 | §2.8 | Which versions said zeroing `beijing` "moves nothing". | CHANGED | **old:** v2 through v4.0 said it. **new:** v4.0 said it. | PROCESS | prior spec versions | 1338 |
| Y1045 | §2.8 | What the solver-tolerance check asserts. | CHANGED | **old:** assert the option is set and that the returned objective's reduced costs clear the tolerance. **new:** assert the option is set, then classify each off-support arc's reduced cost in **three branches** (halt / report / halt), "because a single 'clears the tolerance' test halts on correct behaviour"; the per-good floor on this field is 3.765e-08 on `copper`. | MEASURED | `round6.py` | 1354 |
| Y579 | §2.9 | The solver track's per-tick assertions. | CHANGED | **old:** the list of assertions and the equality monitor. **new:** the containment set is spelled out as `{selected} ∪ {promoted} ∪ {fallbacks}`, and each assertion is "paired with a negative fixture that makes it fail". | DESIGN | stipulated; `scripts/redtest6.py` named | 1377 |
| Y614 | §3.2 | The Cape as a conduit. | CHANGED | **old:** a node with `s = c = 0` carries flow through, with in- and out-degree both nonzero for all 29 goods. **new:** the degree evidence is demoted — "Degree is the weaker evidence and was the only kind offered before … but an oriented edge is not a routed unit" — and replaced by the certificate flow, on which the Cape has both incoming and outgoing flow on **28 of 29** goods. | MEASURED | `round6.py` | 1503 |
| Y684 | §3.9 | What separates a rich net demander from an end. | CHANGED | **old:** a rich non-sink node draws more edges in than it sends out as a net demander, even though flow passes through. **new:** "The quantity that separates them from an end is not a degree comparison … but the flow identity the LP enforces: `flow_in(n) − flow_out(n) = −b_w(n)`". | MODEL | derivation, measured at `round6.py` (L1695) | 1691 |
| Y687 | §3.9 | How many aggregates were tested. | CHANGED | **old:** "Three aggregates were tested; one is impossible and one was superseded." **new:** "Two aggregates were tested and rejected before it." | MODEL | stipulated | 1707 |
| Y689 | §3.9 | The marking-order aggregate's properties. | CHANGED | **old:** `Φ_ord` is acyclic for free **and scores higher than `Φ_w` on self-coherence with the per-good graphs**, which is the cost of the trade and is not disputed. **new:** "An aggregate built from the per-good **marking orders** is acyclic for free, but its ends are a function of the order Phase 3 pops its ready queue" — the self-coherence comparison is gone. | MODEL | derivation | 1711 |
| Y178 | §3.9 | Why the marking-order aggregate's ends are artifacts. | CHANGED | **old:** the sharpest evidence is what relabelling does to them — its end count and end set both move with the node order, where `Φ_w`'s do not. **new:** "That follows from the definition and needs no measurement." | MODEL | derivation | 1711 |
| Y182 | §3.9 | What adopting `Φ_w` costs and buys. | CHANGED | **old:** what it costs is self-coherence with the per-good graphs, which the superseded marking-order aggregate scores higher on; what it buys is one operator, one set of guarantees and ends that sit where the wealth is. **new:** the cost half is deleted; only "What it buys is one operator, one set of guarantees, and ends that sit where the wealth is." survives. | DESIGN | stipulated | 1721 |
| Y183 | §3.10 | The residual on the income identity. | CHANGED | **old:** across Sevilla, Genoa, Champagne, Malacca and the Gulf of Siam, using each node's real 1444 country table, the two forms agree to a worst relative disagreement of 0 to 3.7e-16. **new:** "A run can show only that the implementation does the algebra in doubles, and no residual is quoted for that." | MODEL | derivation | 1742 |
| Y185 | §3.10 | Why reading one installed graph keeps the identity. | CHANGED | **old:** the identity holds by construction **and in doubles to within one to three units in the last place**. **new:** "so the identity holds by construction" — the ULP clause is dropped. | MODEL | derivation | 1744 |
| Y737 | §3.13 | The status of the zero-flow tolerance as an open question. | CHANGED | **old:** scale-coupled — either normalise `b` before the solve or make the tolerance relative — **undecided**. **new:** "It is now closed, and the entry is kept because the reasoning is what stops it being reopened", with the hazard shown unreachable from inside the model and the tolerance-scaling repair shown unavailable. | MODEL | derivation; `round6.py` for the revert measurement | 1830 |
| Y739 | §3.13 | The sink-count-span calibration. | CHANGED | **old:** makes sink counts track price — **span exactly 1..5, spearman(price, sinks) = −0.20** — with α unclamped at exponent 2, ρ = 0.5, twig tolerance 3e-4. **new:** "makes sink counts track price more closely than the baseline does"; the span and correlation figures are withdrawn, the configuration is kept. | MEASURED | `drain-orientation.md` §5–6, `changes-v5.md` §39–41 — no script in `scripts/` | 1848 |
| Y197 | §3.13 | What the calibration does to the cloves sink. | CHANGED | **old:** under α = 16 the cloves demand order is `hangzhou`, `beijing`, `doab`, and the sink lands on a high-demand node. **new:** the demand order is withdrawn; only "under α = 16 the cloves sink lands on a high-demand node rather than a geographic accident" survives. | MEASURED | unsourced at this line | 1857 |
| Y741 | §3.13 | What the twig tolerance costs. | CHANGED | **old:** re-routes arcs individually carrying under 0.03% of world supply — up to about 0.18% of a good's mass in total — and drops `cloves` to 99.97% reach. **new:** "re-routes arcs carrying a small fraction of a good's mass, and it costs one good full reach". | MEASURED | unsourced at this line | 1858 |
| Y773 | §3.15 | `φ₀` as the installed graph, rejected. | CHANGED | **old:** the installed graph is `Φ_w` **(v2.0 briefly used `Φ_ord`)**. **new:** the parenthetical is deleted; "the installed graph is `Φ_w` and its correctness check is cross-implementation orientation equality". | MODEL | stipulated | 1947 |
| Y774 | §3.15 | The marking-order aggregate as the installed graph, rejected. | CHANGED | **old:** the most self-coherent aggregate measured — better than `Φ_w` on that one axis, acyclic for free — but its ends are scheduling artifacts and its end count does not concentrate as demand concentrates. **new:** "Acyclic for free, but its ends are a function of Phase 3's queue discipline rather than of the world (§3.9)" — both the self-coherence ranking and the end-count clause are gone. | MODEL | derivation | 1950 |
| Y204 | §3.15 | The withdrawal of the coherence-ceiling role. | CHANGED | **old:** the entry maintains no figures and its "measured coherence ceiling any future aggregate should be compared against" role is withdrawn; the ceiling v2.0 and v2.1 quoted predates §3.6's deterministic sweep and was never regenerated. **new:** "The rejection is structural, so no figure is kept for it." | PROCESS | stipulated | 1952 |
| Y777 | §3.15 | Why per-good propagation is rejected. | CHANGED | **old:** because it breaks the income factoring and with it Goal 7. **new:** "*Not* because it breaks the income factoring — it does not; §3.10 shows the identity survives with a value-weighted share `ps̄_C`. It is rejected because installing that share means writing each country a **fictitious per-node trade power**". | MODEL | derivation, cross-referred to §3.10 | 1967 |

---

## REWORDED (3)

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y215 | §0 | v2.1 replaced the installed aggregate with `Φ_w`, DRAIN run once more with wealth itself as the good. | REWORDED | — (the census cell names the superseded aggregate `Φ_ord`; the current line names no symbol for it; assertion unchanged) | MODEL | stipulated | 10 |
| Y319 | §1.5 | v2.1 held that a latent good leaves `Φ_w` unaffected because "`Φ_w` reads wealth, not goods"; that held under v2.0's aggregate, which gave a latent good no weight, and became false with the operator change. | REWORDED | — ("that was true under v2.0's `Φ_ord`, where `V_g = 0` gave a latent good zero weight" → "The proposition held under v2.0's aggregate, which weighted each good by `V_g` and so gave a latent good none") | MODEL | derivation | 492 |
| Y344 | §1.6 | The 1444 map draws a pre-Columbian trade geography. | REWORDED | — ("draws the pre-Columbian trade geography **unprompted**" → "draws a **recognisable** pre-Columbian trade geography") | MEASURED | unsourced at this line | 652 |

---

## REMOVED (170 — 15 by this edit, 155 already absent before it)

### Removed by the v6.1 → v6.2 edit (15)

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y052 | §1.3 | `unrest` grants `local_tax_modifier = -0.02` per point of revolt risk and enters `tax_value`. | REMOVED | — | ENGINE | `00_static_modifiers.txt` | — |
| Y979 | §1.3 | `unrest` is live at the 1444 start and is deliberately not read. | REMOVED | — | MODEL | stipulated | — |
| Y982 | §1.3 | 21 counted provinces carry revolt risk in the 1444 start save. | REMOVED | — | ENGINE | the save | — |
| Y057 | §1.3 | Sixteen of the 21 are authored in `history/provinces` at integer risk 5/8/10/15 (Sofala's comment quoted); the other five, all Shirvan-owned, receive theirs at runtime, so reading them needs the save. | REMOVED | — | ENGINE | `history/provinces`, the save | — |
| Y983 | §1.3 | Even at the start date a quarter of the revolt risk is owner-derived, and during a campaign that share only grows. | REMOVED | — | MODEL | derivation over the 16/5 split | — |
| Y056 | §1.3 | Admitting `unrest` moves 4 of 159 edges of the installed graph and leaves the sink set `{genua, hangzhou}` unchanged. | REMOVED | — | MEASURED | unsourced | — |
| Y985 | §1.3 | An earlier draft said admitting `unrest` moves no edge; that was measured at `α_Φ = 1.5` and does not hold at 2.0. | REMOVED | — | PROCESS | unsourced | — |
| Y331 | §1.6 | In exact arithmetic only the sign pattern and proportions of `b_w` matter: Phase 0 reads signs, Phase 1's HHI is built from mass shares, the LP optimum scales linearly with identical net-flow signs, and the priority key is order-isomorphic under positive scaling. | REMOVED | — | MODEL | derivation | — |
| Y332 | §1.6 | The implementation adds one premise: the zero-flow tolerance is absolute (`1e-11`), so scaling `b` down pushes genuine flow arcs into the free set. | REMOVED | — | MODEL | derivation | — |
| Y081 | §1.6 | Measured: identical orientation from ×1 down to ×10⁻², 22 edge flips at ×10⁻⁴ where the sink set becomes `{english_channel, hangzhou}`, and 96 at ×10⁻⁶ where it becomes `{hangzhou}`. | REMOVED | — | MEASURED | unsourced | — |
| Y333 | §1.6 | The orientation degrades before the sink set does, so the sink set is not the quantity to watch here. | REMOVED | — | MODEL | derivation | — |
| Y334 | §1.6 | Normalising into (−1, 1) scales 1444's `b_w` up and is safe; scaling down is not, so either scale `b` up or scale the tolerance with it. | REMOVED | — | MODEL | derivation | — |
| Y539 | §2.8 | v2 said "China holds a spice sink only under the calibration", which its own parenthetical contradicted. | REMOVED | — | PROCESS | prior spec version | — |
| Y179 | §3.9 | Most of `Φ_ord`'s ends terminate no good, none of the demand capitals is among them, and its end count does not concentrate as demand concentrates. | REMOVED | — | MODEL | derivation | — |
| Y180 | §3.9 | No figure is quoted for any of that: the operator is not installed, its numbers moved with every change to the wealth field, three successive audits spent their effort recounting them, and the design argument depends on none of them. | REMOVED | — | PROCESS | stipulated | — |

### Already REMOVED when the census was written — v5.0 propositions superseded before this edit (155)

These are carried forward verbatim from the census, which filed them under `(v5)` section markers with
v5.0 line numbers. None has a counterpart in v6.2 either, so none changes status here.

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y433 | §2.1 (v5) | Supporting multiplayer requires the computation to be bit-reproducible across machines. | REMOVED (already absent before this edit) | — | DESIGN | algebraic derivation | — |
| Y811 | §0 (v5) | v5.0's substantive change was applying the local-modifier classification to the whole install rather than to the… | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y812 | §0 (v5) | The whole-install classification adds sixteen provinces and moves the aggregate graph from two 1444 sinks to one. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y813 | §0 (v5) | No figure in v5.0 is unverified, and the one place the document declines to project a number says so in place. | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y814 | §1.1 (v5) | On a connected core the fallback branch fires only when `b` is identically 0 across it. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y815 | §1.1 (v5) | `b` identically 0 happens for the aggregate graph on a uniform-wealth map. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y816 | §1.1 (v5) | At a fallback stall the candidates are usually all zero-wealth, so the wealth key ties and the index decides. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y817 | §1.1 (v5) | That index tiebreak is why §2.4 item 1 makes a canonical emitter node order a correctness requirement rather than a… | REMOVED (already absent before this edit) | — | DESIGN | algebraic derivation | — |
| Y818 | §1.1 (v5) | On 1444 the per-good sink counts are 1-7 per good with mean 3.6. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y819 | §1.1 (v5) | The §1.1 property measurements were regenerated for v5.0 by `v5measure.py`. | REMOVED (already absent before this edit) | — | MEASURED | computed by a named script | — |
| Y820 | §1.1 (v5) | On a map where Phase 0 is a no-op and no fallback fires, the last two sink cases are empty and the sink set is exactly… | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y821 | §1.3 (v5) | Two provinces with the same terrain, development and trade good have the same wealth whoever owns them. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y822 | §1.3 (v5) | `trade_value(p)` carries a `(1 + sum of local trade-value modifiers)` factor. | REMOVED (already absent before this edit) | — | MODEL | stipulated | — |
| Y823 | §1.3 (v5) | `goods_produced(p)` carries a local flat goods bonuses term added to `GP_COEFF · base_production`. | REMOVED (already absent before this edit) | — | MODEL | stipulated | — |
| Y824 | §1.3 (v5) | Both wealth coefficients were measured from the running game and neither is a define, `defines.lua` having been… | REMOVED (already absent before this edit) | — | ENGINE | read from a file (a negative search) | — |
| Y825 | §1.3 (v5) | The tax tooltip schema is `Base: X (Yearly 12·X)`. | REMOVED (already absent before this edit) | — | ENGINE | measured in-game | — |
| Y826 | §1.3 (v5) | The monthly production tooltip's `Trade Value` line is the province window's annual `Trade Value` over twelve, observed… | REMOVED (already absent before this edit) | — | ENGINE | measured in-game | — |
| Y827 | §1.3 (v5) | Both monthly figures are the annual value over twelve, so the annual forms add directly with no conversion. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y828 | §1.3 (v5) | `Base 0.49` then `Tax Income Efficiency 125.0%` gives 0.6125, which the province window shows as 0.62. | REMOVED (already absent before this edit) | — | ENGINE | measured in-game | — |
| Y829 | §1.3 (v5) | Flat goods bonuses are the exception to modifier ordering: they add into `goods_produced` before the price multiply. | REMOVED (already absent before this edit) | — | ENGINE | measured in-game | — |
| Y830 | §1.3 (v5) | Fifteen 1444 provinces carry a flat bonus in the additive `Base Goods Produced` block, so the ordering matters in… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y831 | §1.3 (v5) | A modifier is local if and only if its value depends only on the province's own attributes — terrain, climate, trade… | REMOVED (already absent before this edit) | — | MODEL | stipulated | — |
| Y832 | §1.3 (v5) | A modifier enters wealth if and only if it modifies `goods_produced`, `price` or `tax_value`. | REMOVED (already absent before this edit) | — | MODEL | stipulated | — |
| Y833 | §1.3 (v5) | The engine's trade-good data model is one instance of the locality test: a good's `province = { }` block is… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y834 | §1.3 (v5) | The two tests are applied to the whole install rather than one file; v4.0 stated the rule and then swept only… | REMOVED (already absent before this edit) | — | PROCESS | read from a file (v4.0's sweep) | — |
| Y835 | §1.3 (v5) | `gems` `local_tax_modifier = 0.15` on 43 provinces is local and enters `tax_value`. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y836 | §1.3 (v5) | `incense` `trade_value_modifier = 0.1` on 29 provinces is local and enters `trade_value`. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y837 | §1.3 (v5) | Great-project `province_modifiers` where `can_use_modifiers_trigger` is empty (6 provinces) are local and enter… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y838 | §1.3 (v5) | `add_permanent_province_modifier` in the undated province-history block (10 provinces) is local and enters… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y839 | §1.3 (v5) | The five static condition modifiers are all zero at the 1444 start, and §1.2 and §3.3 both depend on them biting later. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y840 | §1.3 (v5) | `glass` `local_production_efficiency = 0.1` is local but does not enter wealth, because it modifies production income… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y841 | §1.3 (v5) | `chinaware` `local_autonomy = -0.1` is local but does not enter wealth, because it modifies local autonomy which wealth… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y842 | §1.3 (v5) | 361 provinces carry a centre of trade at 1444, and no CoT level in `common/centers_of_trade/` grants any of the four… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y843 | §1.3 (v5) | `production_leader` `trade_goods_size_modifier = 0.10` is not local, because which country leads a good's production is… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y844 | §1.3 (v5) | Goods-produced efficiency from nearby merchant republics, trading cities and trade companies… | REMOVED (already absent before this edit) | — | ENGINE | read from a file (a binary offset) | — |
| Y845 | §1.3 (v5) | Buildings are local by the test and empty at 1444, because no province's start state carries a temple, workshop or… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y846 | §1.3 (v5) | `terrain.txt` and the climate static modifiers are local but grant only keys wealth does not compute —… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y847 | §1.3 (v5) | A great project contributes the `province_modifiers` accumulated up to its `starting_tier` when its… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y848 | §1.3 (v5) | 85 of the 130 great projects live at 1444 are gated on a country's culture, religion, government or flags. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y849 | §1.3 (v5) | Six great projects carry a key wealth reads: `falun_copper_mine` (province 8, `trade_goods_size` 3.0),… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y850 | §1.3 (v5) | Province 1821 is the richest single province in the game. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y851 | §1.3 (v5) | The starting tier is the right line and "owner action" is not, because development is an owner action so a rule… | REMOVED (already absent before this edit) | — | DESIGN | algebraic derivation | — |
| Y852 | §1.3 (v5) | The ten permanent modifiers are `granary_of_the_mediterranean` (362, 363, 2316, 4316), `skanemarket` (6),… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y853 | §1.3 (v5) | `province_triggered_modifiers`' `stora_kopparberget_modifier` is gated `NOT = { has_dlc = "Leviathan" }` and grants… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y854 | §1.3 (v5) | Every wealth figure in v5.0 was measured with Leviathan installed. | REMOVED (already absent before this edit) | — | MODEL | stipulated | — |
| Y855 | §1.3 (v5) | Glass and chinaware — local but not entering — are the whole of the rule-versus-vocabulary tension, since §1.3 excludes… | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y856 | §1.3 (v5) | Every province the model counts is a city (`is_city = yes`). | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y857 | §1.3 (v5) | `s` and `c` are computed over provinces with an owner and `is_city = yes`. | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y858 | §1.3 (v5) | Owner-agnostic wealth removes the single largest source of hidden owner-dependence from the aggregate graph. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y859 | §1.5 (v5) | Repricing the 45 owned latent-coal provinces flips 29 of 159 `Φ_w` edges. | REMOVED (already absent before this edit) | — | MEASURED | computed by a named script (`v5measure.py`) | — |
| Y860 | §1.5 (v5) | Coal's base price of 10.0 is the highest in vanilla. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y861 | §1.6 (v5) | `Φ_w`'s sink count is set by `α_Φ` and only the sink locations are emergent. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y862 | §1.6 (v5) | Downscaling `b_w` gives 16 edge flips at ×10⁻² and 83 at ×10⁻⁶. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y863 | §1.6 (v5) | 1444's `b_w` has largest magnitude 0.0227. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y864 | §1.6 (v5) | Measured at `α_Φ = 1.5` there is one sink, `hangzhou`, rank 1 in the `α_Φ`-weighted wealth field `c_w` and rank 10 in… | REMOVED (already absent before this edit) | — | MEASURED | computed by a named script (`v5measure.py`) | — |
| Y865 | §1.6 (v5) | v2 through v4's two-sink result was measured on a wealth field missing the sixteen provinces v5's §1.3 carries, and… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y866 | §1.6 (v5) | v2 also wrote "wealth ranks" without saying which, and the plain reading was wrong then too. | REMOVED (already absent before this edit) | — | PROCESS | read from a file (the prior spec version) | — |
| Y867 | §1.6 (v5) | Phase 1 selects `hangzhou` directly, so there are 0 promotions and 0 fallbacks and the self-correction never fires on… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y868 | §1.6 (v5) | Seven sources — `kongo`, `patagonia`, `james_bay`, `mississippi_river`, `chengdu`, `australia`, `tunis` — at `c_w`… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y869 | §1.6 (v5) | 0 edge flips and 0 sink-set changes under ±1% wealth noise across 5 seeds. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y870 | §1.6 (v5) | Agreement with the per-good graphs is 52.5% of edge-goods (51.5% value-weighted) against the superseded `Φ_ord`'s 60.3%… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y871 | §1.6 (v5) | v2's 62.7% was measured under the old scan-order sweep and was never regenerated after §3.6 adopted the deterministic… | REMOVED (already absent before this edit) | — | PROCESS | read from a file (the prior spec version) | — |
| Y872 | §1.6 (v5) | The `α_Φ` sink-count band table: 1 sink `hangzhou` at [1.43, 1.93] width 0.50 (the widest band on this field); 3 sinks… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y873 | §1.6 (v5) | v4.0's two-sink result is not a band: refined to 0.001 it spans [1.406, 1.424], 0.018 wide against the one-sink band's… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y874 | §1.6 (v5) | Under ±1% wealth noise across 8 seeds the narrow window's edges move by up to 0.02 while its width ranges 0.00 to 0.03,… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y875 | §1.6 (v5) | The three wide bands over those same seeds keep widths of 0.28-0.51 with edges moving no more than 0.03. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y876 | §1.6 (v5) | A constant cannot honestly be placed inside a window narrower than the uncertainty in its own edges. | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y877 | §1.6 (v5) | An earlier draft said the narrow window "moves or disappears entirely" under noise; at 8 seeds it disappears on none of… | REMOVED (already absent before this edit) | — | PROCESS | numerical test | — |
| Y878 | §1.6 (v5) | `α_Φ` is retained at 1.5 because it sits inside the widest sink-count band and nothing now selects a different value. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y879 | §1.6 (v5) | Sampled at the six values v2 used the sink count is 5, 1, 2, 4, 3, 1. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y880 | §1.6 (v5) | A 1-2% European development edge produces a European sink: at ×1.02 across Europe's 823 counted provinces the sinks are… | REMOVED (already absent before this edit) | — | MEASURED | computed by a named script (`europe.py`) | — |
| Y881 | §1.6 (v5) | `english_channel` is a sink at every larger European growth factor tested. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y882 | §1.6 (v5) | What the model claims is the threshold rather than the size of the historical edge: 2% is enough, and the project… | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y883 | §1.6 (v5) | All three institutions the period is named for begin in Europe inside the 1450-1550 window. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y884 | §1.6 (v5) | The Renaissance's embracement bonus is a standing 5% discount on every subsequent development point. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y885 | §1.6 (v5) | The Lowlands alone suffice: developing only the nine Lowland provinces in `english_channel` (Holland, Zeeland,… | REMOVED (already absent before this edit) | — | MEASURED | computed by a named script (`europe.py`) | — |
| Y886 | §1.6 (v5) | ±2% random wealth noise leaves the 1444 sink set unchanged on three seeds, while +2% applied systematically to Europe… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y887 | §1.6 (v5) | The 1444 Silk Road route runs through `doab`: genua, alexandria, aleppo, persia, lahore, doab, ganges_delta, burma,… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y888 | §1.6 (v5) | From the Channel the route is the Hansa and the Danube: english_channel, lubeck, saxony, wien, venice, ragusa,… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y889 | §1.6 (v5) | Nothing routes through the Cape, which is what a 1444 map should say. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y890 | §1.6 (v5) | The Cape's per-good spice route is malacca, cape_of_good_hope, zanzibar, gulf_of_aden, alexandria, genua. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y891 | §1.6 (v5) | Scaling the 22 European nodes' wealth ×2 makes `genua` the sole sink, and under the 18-node set alone sole-`genua`… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y892 | §1.6 (v5) | Between ×3 and ×3.75 the Cape of Good Hope reverses and outside that window it does not, so the reversal is a band and… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y893 | §1.6 (v5) | Dev-stacking `hangzhou`'s top province keeps it the sole sink at ×20, ×30 and ×50, with a transient split into three at… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y894 | §1.10 (v5) | Almost nothing absorbs threshold chatter. | REMOVED (already absent before this edit) | — | ENGINE | algebraic derivation | — |
| Y895 | §1.10 (v5) | The caravan cap of 50 is 8.6% to 32.0% of an inland node's total trade power, median 17.9% over the flag's 26 inland… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y896 | §2.2 (v5) | Solver item 4's wealth formula includes local flat goods bonuses inside the goods term and a `(1 + local trade-value… | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y897 | §2.2 (v5) | The solver reads local modifiers from §1.3's whole-install classification: `gems` (+15% tax, 43 provinces), `incense`… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y898 | §2.2 (v5) | World wealth is 10,677.50 annual ducats over 2,452 counted provinces. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y899 | §2.2 (v5) | Solve cost is 0.17-0.21 s for all 29 goods, a mean of 5.7-7.3 ms per good across runs, with individual goods ranging… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y900 | §2.2a (v5) | Where Phase 0 acts, free-edge determinism is the same in both halves, because peeling does not touch the priority key. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y901 | §2.3 (v5) | The two wealth coefficients of §1.3 are hardcoded in the binary, `defines.lua` and `common/defines/` having been… | REMOVED (already absent before this edit) | — | ENGINE | read from a file (a negative search) | — |
| Y902 | §2.3 (v5) | `α_Φ`'s stated calibration is withdrawn because on the corrected wealth field 1.5 does not yield the two-sink map, and… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y903 | §2.3 (v5) | 1.5 is retained because it sits inside the widest sink-count band and nothing now selects a different value. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y904 | §2.4 (v5) | The node order is a correctness requirement because §1.1's priority key breaks exact ties by node index and on the… | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y905 | §2.4 (v5) | Without one canonical node order kept stable across rebuilds, the same world can produce two different maps. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y906 | §2.4 (v5) | 1444 has one end node, `hangzhou`, against vanilla's three. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y907 | §2.7 (v5) | §1.9's "every immediately upstream node" is correct as written and gains no qualifier. | REMOVED (already absent before this edit) | — | ENGINE | engine test | — |
| Y908 | §2.8 (v5) | Sinks are 1 to 7 per good, and high-demand nodes are sinks at 14.5% in the top demand decile against 6.9% in the bottom. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y909 | §2.8 (v5) | Zeroing `hangzhou`-node development moves the `Φ_w` sinks from {hangzhou} to {doab, english_channel, gulf_of_siam,… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y910 | §2.8 (v5) | `hangzhou`'s `c_w` rank is 1 against `beijing`'s 31, node wealth 245.0 against 143.8, and it holds the richest single… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y911 | §2.8 (v5) | Zeroing `beijing` gives 17 flips with sinks {doab, english_channel, hangzhou, sevilla}, because it deletes 1.3% of… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y912 | §2.8 (v5) | The rank gap is what carries the razed-China row, not a null result. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y913 | §2.8 (v5) | `Φ_w` agrees with the per-good graphs on 51.5% of edge-goods weighted by trade value and 52.5% unweighted. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y914 | §3.2 (v5) | With no regularizer the spices supply ratio over producing nodes is 36 against a demand ratio of 482.2, which points… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y915 | §3.2 (v5) | Better wealth inputs plausibly deliver about 1.7×, measured as `genua` becoming a co-sink at ×1.720. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y916 | §3.2 (v5) | A spice sink at any of the four Chinese trade nodes needs 3.6-4.9×, i.e. 9.3-21.4% of all world spice demand at one… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y917 | §3.2 (v5) | The four China-region nodes outside that set — `girin`, `yumen`, `chengdu`, `lhasa` — need 4.0× to 10.8×. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y918 | §3.2 (v5) | v2's "1.7× where 4-5× is needed" compressed two different thresholds into one comparison. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y919 | §3.2 (v5) | The one place the node indexing is load-bearing is the fallback branch, where the candidates are typically all… | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y920 | §3.3 (v5) | `cape_of_good_hope` has 19 land provinces, stated without the `sea_starts` explanation. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y921 | §3.4 (v5) | In v1 substituting production income collapsed orientation agreement from 159/159 to 68/159. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y922 | §3.5 (v5) | All 161 `change_price` blocks were parsed. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y923 | §3.5 (v5) | v4.0 said 154 and 7 because its parser silently recovered nothing from five mission files, which a bare `except` hid,… | REMOVED (already absent before this edit) | — | PROCESS | read from a file (v4.0's toolchain) | — |
| Y924 | §3.5 (v5) | 1.875 is the figure a campaign reaching 1540 holds. | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y925 | §3.8 (v5) | 92.2% (5825 of 6320) of ordered node pairs are connected by at least one good on 1444 data under DRAIN. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y926 | §3.9 (v5) | `genua`, `gulf_of_siam` and `sevilla` rank 3rd, 2nd and 7th by node wealth on the corrected field at 296.0, 299.2 and… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y927 | §3.9 (v5) | `Φ_ord` remains the most self-coherent aggregate measured, at 60.3% edge-good agreement with the per-good graphs… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y928 | §3.9 (v5) | Of `Φ_ord`'s 13 end nodes at 1444, 8 terminate no good at all and none of the demand capitals is among them. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y929 | §3.9 (v5) | `Φ_ord`'s end count never concentrates: 11-17 ends measured across cloves-α 2 to 64, never approaching vanilla's three. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y930 | §3.9 (v5) | v2 called that "α-invariant … 9-17 ends", which is neither the right word for a quantity ranging 11-17 nor a band… | REMOVED (already absent before this edit) | — | PROCESS | read from a file (the prior spec version) | — |
| Y931 | §3.9 (v5) | Self-coherence was traded for legible, wealth-anchored, world-responsive ends. | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y932 | §3.9 (v5) | On the corrected wealth field there is one end, in China, matching none of vanilla's three, so the… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y933 | §3.9 (v5) | The trade is 7.8 points of self-coherence given up for one operator and world-responsive ends, and the 1444 count is… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y934 | §3.10 (v5) | The two income forms agree to at most one unit in the last place. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y935 | §3.10 (v5) | Propagation cannot be made per good. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y936 | §3.10 (v5) | Per-good propagation destroys the income identity, because §1.9 reads a node's downstream neighbours and those differ… | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y937 | §3.10 (v5) | The driver is not how many distinct downstream sets a node has but whether its collectors hold differing power across… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y938 | §3.10 (v5) | `gulf_of_siam` has eight distinct downstream sets and still shows a 0.003% effect, because its collectors hold almost… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y939 | §3.10 (v5) | Per-good propagation's error is redistributive and single-digit percent with the sign varying by collector: Sevilla… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y940 | §3.10 (v5) | That error is thirteen orders of magnitude above the float residual and it moves income between countries. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y941 | §3.10 (v5) | Keeping propagation on a single graph is load-bearing for Goal 7 rather than merely convenient. | REMOVED (already absent before this edit) | — | DESIGN | algebraic derivation | — |
| Y942 | §3.10 (v5) | The largest local trade value of any node in the model is 112.6. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y943 | §3.10 (v5) | v4.0's 0.41% replacement figure was an artifact of freezing one term at the alphabetically first commodity. | REMOVED (already absent before this edit) | — | PROCESS | read from a file (v4.0's construction) | — |
| Y944 | §3.13 (v5) | The open wealth question is what else multiplies `goods_produced` and which side of the owner line each source falls on. | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y945 | §3.13 (v5) | §1.3's classification handles the sources observed so far: the owner's `global_trade_goods_size_modifier` (out,… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y946 | §3.13 (v5) | Fifteen 1444 provinces carry a flat `trade_goods_size`, five from great projects and ten from permanent province… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y947 | §3.13 (v5) | `trade_goods_size` and `trade_goods_size_modifier` appear in buildings, estate privileges, government reforms, church… | REMOVED (already absent before this edit) | — | ENGINE | read from a file | — |
| Y948 | §3.13 (v5) | The settling work is to enumerate every source of both keys and classify each, and the model needs the answer only for… | REMOVED (already absent before this edit) | — | DESIGN | stipulated | — |
| Y949 | §3.13 (v5) | Deccan, demand rank 2 under α = 16 with the rank-1 demander `hangzhou` acting as a transit node, becomes the cloves… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y950 | §3.13 (v5) | `hangzhou`'s richest province is 30.4 against Beijing's 19.5, and under the calibration Beijing is only demand rank 3. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y951 | §3.15 (v5) | With v1's ε floor removed the contrasts run 4-97 on supply against 211-20,400 on demand across the 29 goods. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y952 | §3.15 (v5) | Ranked orientation's alignment statistics: rho_val +0.281 against DRAIN's +0.054, and 43.8% of top-decile nodes are… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y953 | §3.15 (v5) | Ranked orientation reaches 83.0% of demand with 31 orphan sinks. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y954 | §3.15 (v5) | Ranked orientation posts 8 net-producer sinks where DRAIN, LAP and FLOW all post zero. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y955 | §3.15 (v5) | Ranked orientation keeps 10-16 sinks per good against DRAIN's 1-7. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y956 | §3.15 (v5) | Seeded basin growth reaches 88.4% at its best tuning. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y957 | §3.15 (v5) | `Φ_ord` is retained as the measured coherence ceiling any future aggregate should be compared against, and that ceiling… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y958 | §3.15 (v5) | No parameter steers `Φ_ord`'s end count. | REMOVED (already absent before this edit) | — | MODEL | algebraic derivation | — |
| Y959 | §3.15 (v5) | The 3-mass gravity field hits any chosen end count exactly for γ no greater than 0.7 and any count up to six, and at γ… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y960 | §3.15 (v5) | The gravity field's best vanilla-arrow agreement is 61% (97 of 159 arrows) at γ = 0.90-0.95, with γ = 0.97 giving 93… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y961 | §3.15 (v5) | v2.1 through v4.0 put the gravity field's best agreement at γ = 0.97 and said the five- and six-mass fields give four… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y962 | §3.15 (v5) | v2.0 and v2.1 both quoted 69% = 110 of 159 for the gravity field, which is not reached at any γ, and the… | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y963 | §3.15 (v5) | A local wealth maximum survives every positive α, measured as at least 10 ends at α up to 16. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |
| Y964 | §3.16 (v5) | Implemented as written, v1's ε left the α = 1 identity failing at 1e-5. | REMOVED (already absent before this edit) | — | MEASURED | numerical test | — |

---

## NEW (80 — `Y1058`–`Y1137`, in document order)

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y1058 | §0 | What moves with the `α_Φ` change is every figure derived from the aggregate graph — the sink set and its ranks, the source set, the sensitivity bands, and the European scaling. | NEW | — | MODEL | derivation | 41 |
| Y1059 | §0 | What holds is everything computed before the aggregate solve: the wealth field, the per-province and per-node totals, the price census, and the per-good graphs, whose `α(g)` does not read `α_Φ`. | NEW | — | MODEL | derivation | 43 |
| Y1060 | §0 | v6.2 narrows the wealth rule and changes no number on the 1444 field. | NEW | — | DESIGN | stipulated | 49 |
| Y1061 | §0 | `unrest` is dropped from §1.3's table rather than carried as an excluded row. | NEW | — | DESIGN | stipulated | 50 |
| Y1062 | §0 | Both changes follow the same reading: a trade node is owner-agnostic, so wealth measures what a province *can buy*, and neither a revolt nor an occupier changes that. | NEW | — | DESIGN | derivation | 51 |
| Y1063 | §0 | An occupying army is a fact about a war. | NEW | — | DESIGN | stipulated | 54 |
| Y1064 | §0 | What a revolt and an occupier cost the owner is real and is the owner's problem, which is exactly what §1.3 declines to model. | NEW | — | DESIGN | derivation | 54 |
| Y1065 | §0 | The 1444 figures are unchanged because `unrest` was already not read. | NEW | — | MODEL | derivation | 59 |
| Y1066 | §0 | No province is occupied at a start date with no wars. | NEW | — | ENGINE | unsourced | 60 |
| Y1067 | §0 | What moves is what happens **during a campaign**, which is where the rule now differs from v6.1. | NEW | — | DESIGN | derivation | 61 |
| Y1068 | §0 | Every figure the retired `unrest` accounting carried is withdrawn rather than repaired, and with it the `revolt_risk` parse — an input surface maintained for a quantity nothing reads. | NEW | — | PROCESS | stipulated | 62 |
| Y1069 | §0 | `fixes-agreed.md` is **frozen at v6.0**: it records what v6.0 changed relative to v5.0, is not maintained against later versions, and where a figure in it has since moved this document is the live one. | NEW | — | PROCESS | `fixes-agreed.md` | 78 |
| Y1070 | §0 | Neither harness targets `fixes-agreed.md` by default. | NEW | — | PROCESS | stipulated | 80 |
| Y1071 | §1.1 | The shipped operator has no demand-mass quantile parameter — `drain.py`'s Phase 1 clusters every demander. | NEW | — | MODEL | `drain.py` | 123 |
| Y1072 | §1.1 | The §3.13 calibration option carries its own Phase 1 and does implement a quantile; that is where `ρ` is described. | NEW | — | MODEL | stipulated, cross-referred to §3.13 | 125 |
| Y1073 | §1.1 | Phase 0 decides the pendant directions and Phase 4 is where they enter the graph, which is why a pendant sink is visible only after Phase 4 (**T1**, §3.2). | NEW | — | MODEL | derivation | 170 |
| Y1074 | §1.1 | `measure6.py` produced the core-node count; `props6.py` produced the scheduler permutations, the argmin and cut ties, and the reachability and orphan-sink figures. | NEW | — | PROCESS | `measure6.py`, `props6.py` | 212 |
| Y1075 | §1.1 | `props6.py` was renamed from a round-5 working file and its permutation loop was written for this citation — the figure had been quoted since v2 with nothing in the tree that computed it. | NEW | — | PROCESS | `props6.py` | 214 |
| Y1076 | §1.1 | The six identical solves are six solves **inside a single process**, and so blind to anything that varies between processes. | NEW | — | MODEL | derivation | 233 |
| Y1077 | §1.1 | `fingerprint6.py` covers the between-process question separately (§2.1). | NEW | — | PROCESS | `fingerprint6.py` | 235 |
| Y1078 | §1.3 | The deleted-apparatus figures are reproduced by `apparatus6.py`, which holds the deleted classifier's constants **frozen**. | NEW | — | PROCESS | `apparatus6.py` | 276 |
| Y1079 | §1.3 | Those constants record what v5.0's input surface was worth, not a live table, and sit in their own file precisely so that nothing can wire them back into the wealth path. | NEW | — | DESIGN | stipulated | 277 |
| Y1080 | §1.3 | `measure6.py` imports the apparatus figures rather than restating them. | NEW | — | PROCESS | `measure6.py` | 279 |
| Y1081 | §1.3 | The model does not read `occupied`'s `local_tax_modifier`: an occupier's presence is a fact about who is standing on the province, which is the class of input §1.3 exists to exclude. | NEW | — | DESIGN | derivation | 348 |
| Y1082 | §1.3 | The production half already carries the effect that matters, since occupied land ships less. | NEW | — | MODEL | derivation | 349 |
| Y1083 | §1.3 | On the 1444 start only `devastation` is live. | NEW | — | MEASURED | unsourced at this line | 354 |
| Y1084 | §1.3 | `prosperity`, `under_siege` and `occupied` have no input until the emitter reads live province state, because all three describe conditions a campaign produces and a start date does not. | NEW | — | MODEL | derivation | 354 |
| Y1085 | §1.3 | The wealth rule carries four modifiers, of which one is exercised by the reference field. | NEW | — | MODEL | derivation | 356 |
| Y1086 | §1.3 | A province in revolt still has the buying power its development gives it; whether its owner manages to collect against that buying power is a fact about the owner, and a trade node is not a fact about the owner. | NEW | — | DESIGN | derivation | 364 |
| Y1087 | §1.3 | Earlier drafts carried a figure for the `unrest` exclusion, and keeping it accurate meant parsing `revolt_risk` out of the save — an input surface maintained for a quantity the model does not read, which is the maintenance §1.3 deleted the modifier classifier to be rid of. | NEW | — | PROCESS | stipulated | 372 |
| Y1088 | §1.3 | The exclusion is a decision about what wealth *means*, and a measured cost would not bear on it. | NEW | — | DESIGN | stipulated | 375 |
| Y1089 | §1.6 | The direction is unambiguous: Europe goes from one end to three and Asia goes from one to none. | NEW | — | MEASURED | `europe.py` (named in the lead-in at L617) | 620 |
| Y1090 | §1.6 | The widest interval carrying three European ends and none in Asia runs **×1.973 to ×2.456**, with `english_channel`, `genua` and `rheinland` holding them. | NEW | — | MEASURED | `europe.py` (named in the lead-in at L617) | 621 |
| Y1091 | §1.6 | A table of interval boundaries was published here and is withdrawn: its rows came from bisection and disagree with a uniform grid about where several boundaries lie, so a boundary sitting between samples produced a row that looks like a fact and is an artifact of the sampling. | NEW | — | PROCESS | stipulated | 628 |
| Y1092 | §1.6 | The direction and the widest interval survive that difference; the row boundaries did not, and quoting them invited exactly the trajectory reading the paragraph above warns against. | NEW | — | PROCESS | stipulated | 630 |
| Y1093 | §1.6 | At every multiple above ×2.50 on the 22-node scaling both surviving ends are western. | NEW | — | MEASURED | unsourced at this line | 680 |
| Y1094 | §1.6 | The "eastern four pulling ends of their own" clause of an earlier draft was invented and is deleted rather than repaired. | NEW | — | PROCESS | stipulated | 681 |
| Y1095 | §1.6 | §1.6's figures are measured under the shipped sweep key `(DEF ascending, β ascending, index)`, which is a design choice inside Phase 3 rather than a property of the world, so a different key moves some of them. | NEW | — | MODEL | derivation | 693 |
| Y1096 | §1.6 | Measured against DEF-*descending* on the same field: of the **19** aggregate-graph facts this section states, **6 move**. | NEW | — | MEASURED | `round6.py`, which lists all 19 and marks the ones that move | 695 |
| Y1097 | §1.6 | What does not move under the descending key: the sink set, the promotion and fallback counts, acyclicity, `genua`'s degrees, the Cape's degrees, and the two-hop `english_channel → champagne → genua` route. | NEW | — | MEASURED | `round6.py` | 697 |
| Y1098 | §1.6 | What moves under the descending key: the source set (5 sources against 10), its `c_w` rank range and mean degree, and the Cape's ordered-pair count (81 against 42). | NEW | — | MEASURED | `round6.py` | 699 |
| Y1099 | §1.6 | Under the descending key the Iberian long route ceases to exist: `sevilla` reaches no Asian end at all, and no path runs from it to `ganges_delta`. | NEW | — | MEASURED | `round6.py` | 701 |
| Y1100 | §1.6 | The northern long route survives both keys. | NEW | — | MEASURED | `round6.py` | 702 |
| Y1101 | §1.6 | The two long routes are therefore properties of this field *and* this key, while the sink set is a property of the field alone. | NEW | — | MODEL | derivation | 702 |
| Y1102 | §1.10 | The four-construct list is exhaustive on this install rather than illustrative: across `common/`, `missions/`, `decisions/` and `events/` those four account for **410 uses** — 36, 165, 171 and 38 respectively — and **no `trade_node` token outside them**. | NEW | — | MEASURED | `round6.py`, comments stripped | 833 |
| Y1103 | §1.10 | Checked the same way, none of the 80 node names appears anywhere in those four trees. | NEW | — | MEASURED | `round6.py` | 836 |
| Y1104 | §1.10 | The exposure is bounded by class and not merely unenumerated: what scripted content can do to a node is exactly what those four constructs express. | NEW | — | MODEL | derivation | 836 |
| Y1105 | §2.3 | `\|w[u] − w[v]\|` **telescopes**: summed along a path it collapses to a function of the endpoints, so two routings between the same endpoints can still total the same and the term cancels exactly where a tie needs breaking. | NEW | — | MODEL | derivation | 1106 |
| Y1106 | §2.3 | `frac(lo·hi·7919)` has no such structure, and that is the whole of its job. | NEW | — | MODEL | derivation | 1108 |
| Y1107 | §2.3 | Measured on the same field: the structured term leaves **11 of 29** goods admitting an alternative optimum against the shipped term's **1** (`paper`). | NEW | — | MEASURED | `round6.py` | 1109 |
| Y1108 | §2.3 | `w/mean` and `N·w/sum` are **algebraically the same vector**, and on this field min-max and `w/max` are too, because the minimum node wealth is exactly zero — `cape_of_good_hope` holds no counted province wealth. | NEW | — | MODEL | derivation | 1153 |
| Y1109 | §2.3 | A sweep over five "normalisations" is therefore a sweep over three. | NEW | — | MODEL | derivation | 1156 |
| Y1110 | §2.3 | The normalisation probe must inherit `flowop.LP_OPTS`: without the pinned tolerance the same sweep **undercounts**, returning a strict subset of the goods that actually move. | NEW | — | MEASURED | names `flowop.LP_OPTS`, not the script that ran the sweep | 1157 |
| Y1111 | §2.8 | The calibration figures moved when §2.3's tie-break cost reached the calibration's own Phase 2 — it was the last solve in the tree still passing unit costs, and it had been reading a different vertex from the shipped operator on every good. | NEW | — | PROCESS | stipulated | 1333 |
| Y1112 | §2.8 | The tolerance check must classify each off-support arc's reduced cost in three branches, because a single "clears the tolerance" test halts on correct behaviour. | NEW | — | DESIGN | derivation | 1354 |
| Y1113 | §2.8 | **Halt** if the smallest *positive* reduced cost is at or below the tolerance, since the optimum is then not separated from its neighbours. | NEW | — | DESIGN | derivation | 1354 |
| Y1114 | §2.8 | **Report** if a reduced cost is zero and the arc carries no flow in any optimum — a genuine tie the tie-break did not reach, and the state `paper` is in today. | NEW | — | DESIGN | derivation | 1354 |
| Y1115 | §2.8 | **Halt** if a reduced cost is zero and the arc can carry flow, which means an alternative optimum is reachable and the orientation is not determined. | NEW | — | DESIGN | derivation | 1354 |
| Y1116 | §2.8 | The per-good margin floor on this field is **3.765e-08**, on `copper` — the same measurement §3.6 quotes. | NEW | — | MEASURED | `round6.py` | 1354 |
| Y1117 | §2.9 | Each per-tick assertion is paired with a negative fixture that makes it fail, because an assertion nobody has watched go red is an assertion nobody has tested. | NEW | — | DESIGN | stipulated | 1378 |
| Y1118 | §2.9 | Four of the defects the round-5 audit found were checks that could not fail. | NEW | — | PROCESS | stipulated | 1379 |
| Y1119 | §2.9 | `scripts/redtest6.py` is the reference-side version of the negative-fixture discipline. | NEW | — | PROCESS | `scripts/redtest6.py` | 1380 |
| Y1120 | §3.2 | Degree is the weaker evidence for conduit behaviour and was the only kind offered before: an oriented edge is not a routed unit. | NEW | — | MODEL | derivation | 1504 |
| Y1121 | §3.2 | On the certificate flow itself the Cape has both incoming and outgoing flow on **28 of 29** goods; the exception is `paper`, which routes none through it in either direction. | NEW | — | MEASURED | `round6.py` | 1505 |
| Y1122 | §3.6 | The tie-break margin is not a constant of the design, and it is worth knowing how much of it is a gift of the chosen `α_Φ`. | NEW | — | MODEL | derivation | 1631 |
| Y1123 | §3.6 | On the aggregate the margin is **7.53e-06** at `α_Φ = 2.0` and **1.267e-07** at 1.5 — a factor of sixty for a change §1.6 treats as taste. | NEW | — | MEASURED | `round6.py` (named at L1635) | 1632 |
| Y1124 | §3.6 | **Two of the 29** per-good solves sit inside HiGHS's 1e-7 default (`copper` at 3.765e-08, `paper` at 8.92e-08) and 27 sit above it. | NEW | — | MEASURED | `round6.py` (named at L1635) | 1633 |
| Y1125 | §3.6 | `round6.py` reports the margin as the smallest positive reduced cost on an arc outside the support. | NEW | — | PROCESS | `round6.py` | 1635 |
| Y1126 | §3.6 | Pinning the tolerance is load-bearing at these values rather than precautionary, and a future change to `α_Φ` or to the wealth field should re-measure it rather than assume the headroom survives. | NEW | — | DESIGN | derivation | 1636 |
| Y1127 | §3.9 | What separates a net demander from an end is the flow identity the LP enforces, `flow_in(n) − flow_out(n) = −b_w(n)`, which holds on all **36** net demanders and on all 80 nodes to a maximum residual of **5.2e-17**. | NEW | — | MEASURED | `round6.py` | 1693 |
| Y1128 | §3.9 | Every net demander absorbs exactly its own deficit and passes the rest on; an end is a node that passes none on. | NEW | — | MODEL | derivation | 1695 |
| Y1129 | §3.9 | **18 of 80** nodes have out-degree above zero while carrying no outgoing flow at all. | NEW | — | MEASURED | `round6.py` | 1696 |
| Y1130 | §3.13 | The zero-flow-tolerance entry is kept after being closed because the reasoning is what stops it being reopened. | NEW | — | PROCESS | stipulated | 1830 |
| Y1131 | §3.13 | The scale hazard is not reachable from inside the model: `b_w` is built with `s_w(n) = 1/N` uniform against a `c_w` that sums to 1, so its largest magnitude cannot fall below `1/N` without changing what the model computes; there is no scale knob to turn. | NEW | — | MODEL | derivation | 1834 |
| Y1132 | §3.13 | HiGHS's own floor for these options is 1e-10, and below it the option is rejected with `Invalid option value` while `success` stays true and the solver **silently reverts to the 1e-7 default**. | NEW | — | MEASURED | `round6.py` (named at L1840) | 1837 |
| Y1133 | §3.13 | A silent revert is worse than not setting the option, because it looks like it worked. | NEW | — | DESIGN | derivation | 1839 |
| Y1134 | §3.13 | Measured on `copper`: an unset tolerance and 1e-7 each move 8 edge-slots over four column permutations, 1e-8 and 1e-10 each move none, and **a rejected 1e-11 moves 8** — it behaves like the default, not like the last valid setting. | NEW | — | MEASURED | `round6.py` | 1840 |
| Y1135 | §3.13 | The free-versus-flow margin measured in §2.1 is six orders wide with nothing inside it, so nothing is close to the boundary. | NEW | — | MODEL | derivation, cross-referred to §2.1 | 1843 |
| Y1136 | §3.13 | No span, correlation or reach figure is quoted for the calibration option, on the same ground §3.9 gives for the superseded aggregate: it is not adopted, its numbers move with every change to the wealth field and to §2.3's cost, and the decision does not turn on them. | NEW | — | PROCESS | stipulated | 1852 |
| Y1137 | §3.13 | The last such change moved the calibration's sink sets while the argument for and against it stayed exactly the same. | NEW | — | PROCESS | stipulated | 1855 |

---

## UNCHANGED (825)

Compressed to ID / § / short label / type / line, as the brief permits. Lines in the twelve sections
whose length changed were re-read against the current file; lines in the zero-delta sections are the
census locator plus that section's constant offset. Treat these as accurate to ±2.

| ID | § | claim (short label) | type | line |
|---|---|---|---|---|
| Y207 | §0 | The target build is EU4 1.37.5 Inca. | DESIGN | 5 |
| Y208 | §0 | The design is extended-timeline compatible. | DESIGN | 5 |
| Y209 | §0 | The design targets connected maps only. | DESIGN | 5 |
| Y210 | §0 | This document supersedes v1.3, which lives in `../v1-laplacian/`. | PROCESS | 6 |
| Y211 | §0 | v1 oriented each good by a Laplacian potential. | MODEL | 6 |
| Y212 | §0 | v1's sink placement was shown to be topological rather than economic. | MODEL | 7 |
| Y213 | §0 | A four-operator bake-off replaced the orientation core with the DRAIN algorithm. | MODEL | 8 |
| Y214 | §0 | Every claim-audit correction from `../v1-laplacian/validation.md` that is settleable… | PROCESS | 9 |
| Y001 | §0 | v6.0 makes owner-agnosticism true by construction rather than by a rule that has to be… | DESIGN | 13 |
| Y216 | §0 | This version keeps v3.0's owner-agnostic wealth. | DESIGN | 13 |
| Y002 | §0 | The substantive change of v6.0 is to §1.3: wealth is a function of the province's… | DESIGN | 14 |
| Y003 | §0 | The two-test modifier classifier and everything it governed — trade-good modifiers,… | DESIGN | 16 |
| Y004 | §0 | The two-test classifier is v4.0's; v3.0 used a structural rule about which block of a… | MODEL | 18 |
| Y005 | §0 | On the 1444 start the deleted apparatus was worth 105.30 ducats — 0.98% of the… | MEASURED | 20 |
| Y006 | §0 | That classification was wrong in both independent audits that examined it… | PROCESS | 21 |
| Y007 | §0 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated… | DESIGN | 24 |
| Y008 | §0 | Phase 2's min-cost flow is degenerate under unit arc costs, so presentation order… | MEASURED | 27 |
| Y965 | §0 | v6.1 changes the operator, not the field. | DESIGN | 27 |
| Y966 | §0 | §2.3 now breaks that tie inside the objective, in two terms — one carrying the design… | MODEL | 28 |
| Y1000 | §0 | §2.3 also pins the solver's optimality tolerance, which turned out to be a correctness… | MODEL | 29 |
| Y1001 | §0 | The margin by which the tie-break makes the optimum unique is as small as 3.8e-8 while… | MEASURED | 31 |
| Y967 | §0 | With all three changes in place the orientation is unchanged across every relabelling… | MEASURED | 32 |
| Y968 | §0 | A canonical node order remains an emitter requirement because the order-invariance is a… | MODEL | 35 |
| Y1002 | §0 | The orientation is also unchanged under permutation of the LP's column order. | MEASURED | 35 |
| Y969 | §0 | `α_Φ` moves from 1.5 to 2.0. | MODEL | 38 |
| Y970 | §0 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste,… | DESIGN | 38 |
| Y971 | §0 | Every derivation previously offered for `α_Φ` is withdrawn without replacement. | MODEL | 40 |
| Y972 | §0 | The 1444 sink set moves from `{english_channel, hangzhou}` to `{genua, hangzhou}`. | MEASURED | 40 |
| Y1003 | §0 | §2.1 records what multiplayer would additionally need, which is now build discipline… | MODEL | 46 |
| Y009 | §0 | Prose convention: no empirical absolutes — no superlative, no universal quantifier and… | DESIGN | 65 |
| Y011 | §0 | Those rejected-operator numbers were re-measured and re-refuted in three successive… | PROCESS | 70 |
| Y220 | §0 | Where a comparison is genuinely load-bearing it is stated as a direction rather than as… | DESIGN | 71 |
| Y013 | §0 | `scripts/verify6.py` reads figures out of the document text and fails when they… | PROCESS | 81 |
| Y217 | §0 | Measured figures carry the script that produced them. | DESIGN | 81 |
| Y218 | §0 | Deleted text is quoted in `changes-v6.md`. | PROCESS | 81 |
| Y974 | §0 | `verify6.py`'s coverage of the figures this document prints is partial. | PROCESS | 84 |
| Y1051 | §0 | Neither a count nor a proportion of that coverage is given here, for two different… | DESIGN | 85 |
| Y975 | §0 | No count is given here because some of the harness's checks are generated per matching… | PROCESS | 86 |
| Y015 | §0 | No coverage proportion is offered because the denominator is not well defined: counting… | PROCESS | 87 |
| Y1052 | §0 | An earlier draft of this paragraph asserted "well under half" two sentences before… | PROCESS | 90 |
| Y016 | §0 | `scripts/coverage6.py` is the honest measure — it corrupts each spec-printed figure… | PROCESS | 91 |
| Y017 | §0 | Some figures carry a script attribution instead of a guard, and a few carry neither. | PROCESS | 93 |
| Y018 | §0 | `scripts/mutate6.py` reports a higher score that should not be read as coverage: it… | PROCESS | 95 |
| Y219 | §0 | The document has three sections: §1 Mechanics states what the system does, §2… | DESIGN | 99 |
| Y221 | §1.1 | Every trade good has its own directed network over the same adjacency. | MODEL | 107 |
| Y222 | §1.1 | Direction is computed, never authored. | DESIGN | 107 |
| Y223 | §1.1 | For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`, oriented by DRAIN in four… | MODEL | 109 |
| Y224 | §1.1 | Phase 0 repeatedly removes degree-1 nodes, orienting each pendant edge by the sign of… | MODEL | 112 |
| Y225 | §1.1 | Phase 0 is exact rather than heuristic: every removed edge is a bridge and flow on a… | MODEL | 114 |
| Y226 | §1.1 | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | MEASURED | 115 |
| Y227 | §1.1 | Phase 0 exists for modded maps. | DESIGN | 116 |
| Y228 | §1.1 | Phase 1 takes the connected clusters of net demanders in the core, computes the… | MODEL | 118 |
| Y230 | §1.1 | On vanilla 1444 demand is so ubiquitous that k = 1 for 27 of 29 goods at the default… | MEASURED | 122 |
| Y231 | §1.1 | Phase 1's selection is deliberately weak because Phase 3 self-corrects upward. | DESIGN | 123 |
| Y232 | §1.1 | Phase 2 solves the uncapacitated min-cost flow serving `b_g` and orients every support… | MODEL | 128 |
| Y976 | §1.1 | Phase 2's arc costs are near-unit, symmetric in the arc, and read from node wealth: a… | MODEL | 129 |
| Y977 | §1.1 | The costs are not unit because with unit costs the optimum is not unique and which one… | MODEL | 131 |
| Y233 | §1.1 | The support is a spanning-tree basis of at most N−1 edges when the solver returns a… | MODEL | 133 |
| Y234 | §1.1 | An interior-point solve without crossover can split flow across equal-length parallel… | MODEL | 135 |
| Y235 | §1.1 | §2.2 therefore requires network simplex or a simplex LP. | DESIGN | 136 |
| Y1004 | §1.1 | §2.3 additionally requires the solver's optimality tolerance to be tighter than the… | MODEL | 137 |
| Y236 | §1.1 | For any optimum the support contains no directed cycle, because with all costs strictly… | MODEL | 138 |
| Y237 | §1.1 | Edges with zero net flow are free and are deferred to Phase 3. | MODEL | 141 |
| Y238 | §1.1 | Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is… | MODEL | 143 |
| Y239 | §1.1 | Among ready nodes the sweep pops by the priority key (DEF ascending, b ascending,… | MODEL | 145 |
| Y240 | §1.1 | The flow-arc subgraph is acyclic and fixed before any free edge, so `DEF` involves no… | MODEL | 147 |
| Y241 | §1.1 | On a stall the sweep promotes the heaviest flow-terminal demander among the candidates… | MODEL | 148 |
| Y242 | §1.1 | If the candidates hold no flow-terminal demander at all, the fallback branch promotes… | MODEL | 149 |
| Y243 | §1.1 | Node wealth is a good-independent input, so the fallback branch needs no bootstrap. | MODEL | 150 |
| Y244 | §1.1 | Candidates at a stall are the unmarked nodes whose flow out-neighbours are all marked;… | MODEL | 151 |
| Y245 | §1.1 | A candidate carrying any flow out-arc is already ready, and a candidate with inflow is… | MODEL | 153 |
| Y019 | §1.1 | The fallback branch fires only when every candidate is support-isolated with zero… | MODEL | 155 |
| Y020 | §1.1 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's… | MODEL | 156 |
| Y021 | §1.1 | On a connected core the fallback needs the folded balance to vanish across the core:… | MODEL | 158 |
| Y022 | §1.1 | Nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes… | MEASURED | 160 |
| Y023 | §1.1 | Where the wealth key ties, the node index decides. | MODEL | 161 |
| Y024 | §1.1 | §2.8's containment set includes the fallbacks because of T3 — a fallback promotion that… | DESIGN | 162 |
| Y246 | §1.1 | Free edges orient from later-marked to earlier-marked. | MODEL | 166 |
| Y247 | §1.1 | Phase 4 un-peels the Phase-0 pendants in reverse order. | MODEL | 169 |
| Y248 | §1.1 | Each §1.1 property is labelled proved, measured, or true-by-construction, and the three… | DESIGN | 173 |
| Y250 | §1.1 | The §1.1 property measurements were regenerated for v6.0 by `measure6.py`. | MEASURED | 174 |
| Y249 | §1.1 | That labelling discipline caught four over-claims between v2.0 and v3.0. | PROCESS | 177 |
| Y251 | §1.1 | Global DAG: every arc points from later-marked to earlier-marked, so reversed marking… | MODEL | 180 |
| Y252 | §1.1 | Measured acyclic on 29 of 29 goods. | MEASURED | 181 |
| Y253 | §1.1 | Every sink is one of four kinds: a selected demand centre that turned out… | MODEL | 183 |
| Y025 | §1.1 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected… | MEASURED | 185 |
| Y026 | §1.1 | That equality is a measurement on this input rather than a theorem, and v2 asserted it… | MODEL | 187 |
| Y027 | §1.1 | It does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback… | MODEL | 188 |
| Y254 | §1.1 | Three constructed cases break the sink-set equality: a pendant net-importing leaf is a… | MEASURED | 190 |
| Y255 | §1.1 | A node with no outgoing links for `g` is a sink for `g`; sinks differ per good; there… | MODEL | 193 |
| Y256 | §1.1 | The orientation contains a flow serving 100% of every good's demand, because the LP… | MODEL | 195 |
| Y257 | §1.1 | The premise that makes the LP feasible is connectedness: on a disconnected map the… | MODEL | 197 |
| Y258 | §1.1 | §2.2 states the connectedness requirement and what the solver does when it is violated. | MODEL | 200 |
| Y259 | §1.1 | Measured on 1444, which is one component: 100.0% of demand reachable from supply, 29/29… | MEASURED | 201 |
| Y260 | §1.1 | Ready-marking is a monotone closure, so the stall sequence and both promotion branches… | MODEL | 203 |
| Y261 | §1.1 | Free-edge direction is deterministic, by the same closure argument plus the priority… | MODEL | 205 |
| Y262 | §1.1 | That free-edge direction is a function of the graph and the balances alone — that the… | MEASURED | 206 |
| Y1005 | §1.1 | Measured: zero exact `(DEF, b)` key collisions across all 2,320 core nodes of the 29… | MEASURED | 209 |
| Y1006 | §1.1 | Phase 1's within-cluster argmin and its top-k cluster cut are untied on the same field,… | MEASURED | 210 |
| Y263 | §1.1 | The certificate flow is a near-fewest-hop routing in aggregate: with unit costs the… | MODEL | 217 |
| Y264 | §1.1 | No per-unit shortest-path claim is made and none holds, because a unit may detour when… | MODEL | 224 |
| Y265 | §1.1 | The efficiency property carries no measurement and wants none: it follows from the… | DESIGN | 226 |
| Y266 | §1.1 | The §3.13 calibration deliberately degrades efficiency, which is a change to the… | DESIGN | 227 |
| Y267 | §1.1 | The orientation is recomputed on a fixed monthly tick, aligned to the vanilla trade… | MODEL | 231 |
| Y268 | §1.1 | Orientation is read from the current solve every time, with no memory of the previous… | MODEL | 231 |
| Y269 | §1.1 | The LP is deterministic on one machine and one build — six identical solves gave one… | MEASURED | 232 |
| Y270 | §1.1 | Across machines LP determinism is the open question of §3.13. | DESIGN | 236 |
| Y271 | §1.2 | `s(n,g) = goods_produced(n,g)` over the world sum of `goods_produced(m,g)`. | MODEL | 241 |
| Y272 | §1.2 | `goods_produced` is a physical quantity — pre-production-efficiency and pre-autonomy. | MODEL | 244 |
| Y273 | §1.2 | `goods_produced` moves with devastation, occupation and prosperity, because… | ENGINE | 244 |
| Y274 | §1.2 | There is no regularizer: v1 mixed in `s ← (1 − ε)·s + ε/N` to keep dead branches from… | MODEL | 246 |
| Y275 | §1.2 | DRAIN's free edges are oriented combinatorially by the drainage sweep rather than by… | MODEL | 247 |
| Y276 | §1.2 | One node has `b = 0` exactly at 1444 — `cape_of_good_hope` — and it is handled as an… | MEASURED | 248 |
| Y277 | §1.3 | Demand is assembled per province, then summed to the node. | MODEL | 253 |
| Y028 | §1.3 | Wealth is owner-agnostic and reads three things about the province: its development,… | MODEL | 255 |
| Y278 | §1.3 | Wealth is a property of the place — what the land is worth per year, before anyone's… | DESIGN | 256 |
| Y279 | §1.3 | Wealth reads no autonomy, no production efficiency, no national ideas, no estate or… | MODEL | 257 |
| Y029 | §1.3 | Two provinces with the same development, trade good and condition have the same wealth… | MODEL | 258 |
| Y280 | §1.3 | A province's wealth does not change when it is conquered. | MODEL | 260 |
| Y030 | §1.3 | Owner-agnosticism is true by construction rather than by a policed rule; v3.0 through… | PROCESS | 262 |
| Y031 | §1.3 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so… | MODEL | 266 |
| Y032 | §1.3 | What the change gives up: `gems`' `local_tax_modifier` and `incense`'… | DESIGN | 267 |
| Y034 | §1.3 | That count depends on the field: it is 87 under the withdrawn `is_city` filter, and 89… | ENGINE | 274 |
| Y281 | §1.3 | The model trades that fidelity for an input surface with no classification question in… | DESIGN | 281 |
| Y035 | §1.3 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + sum of province-state goods… | MODEL | 284 |
| Y036 | §1.3 | `trade_value(p) = goods_produced(p) · price(good(p))` in ducats per year, with no… | MODEL | 285 |
| Y282 | §1.3 | `wealth(p) = tax_value(p) + trade_value(p)`, in ducats per year. | MODEL | 287 |
| Y283 | §1.3 | `c(n,g)` is the node's share of world wealth raised to `α(g)`: the sum over provinces… | MODEL | 289 |
| Y038 | §1.3 | `GP_COEFF` is a shipped file value: `common/static_modifiers/00_static_modifiers.txt`… | ENGINE | 292 |
| Y284 | §1.3 | `GP_COEFF` and `TAX_COEFF` have different provenance from one another. | PROCESS | 292 |
| Y039 | §1.3 | `GP_COEFF` is therefore moddable and is read at runtime rather than hardcoded. | DESIGN | 295 |
| Y040 | §1.3 | `TAX_COEFF` is in no file that has been found — not `defines.lua`, not… | ENGINE | 296 |
| Y285 | §1.3 | The tax and trade terms share a time basis and are safe to add, because the engine's… | ENGINE | 300 |
| Y041 | §1.3 | The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`,… | ENGINE | 301 |
| Y042 | §1.3 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it… | ENGINE | 303 |
| Y043 | §1.3 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own… | PROCESS | 305 |
| Y044 | §1.3 | The monthly production tooltip's `Trade Value` line is consistent with the same… | ENGINE | 306 |
| Y045 | §1.3 | Both monthly figures being the annual value over twelve is what lets the annual forms… | MODEL | 308 |
| Y286 | §1.3 | The coefficients were measured on two provinces: Garnatah (223) with `base_tax` 6,… | ENGINE | 311 |
| Y287 | §1.3 | Only the tooltips' `Base` lines are used. | DESIGN | 312 |
| Y288 | §1.3 | A province window's `Trade Value` also carries the owner's… | ENGINE | 313 |
| Y289 | §1.3 | Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444… | ENGINE | 314 |
| Y290 | §1.3 | Ruler personalities are rolled at game start wherever country history scripts none, so… | ENGINE | 315 |
| Y291 | §1.3 | Modifiers apply after the coefficient, not before: the engine computes the base from… | ENGINE | 319 |
| Y046 | §1.3 | Observed on Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base… | ENGINE | 320 |
| Y047 | §1.3 | The example establishes only the ordering — base from development first, percentage… | ENGINE | 323 |
| Y048 | §1.3 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires… | PROCESS | 324 |
| Y049 | §1.3 | Flat goods bonuses would add into `goods_produced` before the price multiply — the… | ENGINE | 326 |
| Y054 | §1.3 | `devastation`'s scaling law is the one row in the table not settled by a shipped file:… | ENGINE | 341 |
| Y980 | §1.3 | Revolt risk is not a property of the place: in play it carries separatism from recent… | MODEL | 359 |
| Y984 | §1.3 | The effect `unrest` would buy is already bought: conquest costing a province its wealth… | MODEL | 368 |
| Y058 | §1.3 | The condition modifiers are what make the map answer to war: §1.2's volatility and… | DESIGN | 378 |
| Y059 | §1.3 | Eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20… | ENGINE | 382 |
| Y060 | §1.3 | That devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The… | ENGINE | 383 |
| Y061 | §1.3 | The start devastation costs 13.40 ducats across the eleven affected counted provinces. | MEASURED | 385 |
| Y062 | §1.3 | The start state is what the engine produces rather than what the history files say, and… | DESIGN | 389 |
| Y063 | §1.3 | `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others… | ENGINE | 392 |
| Y064 | §1.3 | Development does not move before the first tick: on this start the history parse… | ENGINE | 395 |
| Y065 | §1.3 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move… | ENGINE | 397 |
| Y066 | §1.3 | `add_base_*` in a dated block before the start date accumulates, and v5.0 and earlier… | ENGINE | 401 |
| Y067 | §1.3 | `is_city = yes` is not a filter the engine applies: 20 owned provinces omit or comment… | ENGINE | 404 |
| Y068 | §1.3 | The model counts a province when it has an owner and lies in a trade node: 2,472… | DESIGN | 406 |
| Y069 | §1.3 | Twenty counted provinces have no trade good in their history file (`trade_goods =… | ENGINE | 409 |
| Y070 | §1.3 | The model reads the good the engine actually rolled rather than predicting the draw,… | MEASURED | 411 |
| Y071 | §1.3 | On this save the twenty came up seven `fur`, five `grain`, three `wool`, two… | ENGINE | 413 |
| Y293 | §1.3 | Everything the engine itemised on a real province that is not local is excluded:… | ENGINE | 418 |
| Y294 | §1.3 | `Core` (+75%) and `City` (+25%) are not excluded, because they are already inside… | MODEL | 422 |
| Y295 | §1.3 | The engine's tax multiplier is the sum of the itemised percentages: Garnatah's `Tax… | ENGINE | 422 |
| Y296 | §1.3 | A cored city province carrying nothing else sums to exactly 0.75 + 0.25 = 1.00 and… | ENGINE | 425 |
| Y072 | §1.3 | The model applies `TAX_COEFF = 1.0` to every province it counts: ownership is not… | DESIGN | 426 |
| Y297 | §1.3 | Carrying either the `Core` or the `City` term again would double-count it. | MODEL | 428 |
| Y073 | §1.3 | That is a modelling choice with a known cost: two readings, both on cored city… | DESIGN | 429 |
| Y074 | §1.3 | `base_tax` at 1444 runs up to 15 (province 1821), with total development reaching 33… | ENGINE | 430 |
| Y298 | §1.3 | Unowned provinces are outside the model: `s` and `c` are computed over provinces that… | DESIGN | 433 |
| Y299 | §1.3 | What owner-agnostic demand buys: demand stops responding to who rules and responds only… | DESIGN | 436 |
| Y075 | §1.3 | Owner-agnostic wealth also removes a large source of hidden owner-dependence from the… | MODEL | 438 |
| Y300 | §1.4 | `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)` with `P₀ = 2.0` ducats. | MODEL | 444 |
| Y301 | §1.4 | α > 1 makes demand superlinear in provincial wealth, so luxuries concentrate on… | MODEL | 447 |
| Y302 | §1.4 | α = 1 makes demand proportional to economic size. | MODEL | 448 |
| Y303 | §1.4 | α < 1 makes demand sublinear, so bulk goods spread toward populous regions. | MODEL | 449 |
| Y304 | §1.4 | α moves with vanilla price events in both directions, with no smoothing. | MODEL | 451 |
| Y305 | §1.5 | Gold is excluded by configuration. | MODEL | 455 |
| Y306 | §1.5 | Gold-mine income is its own income category in the engine (`INCOMEGOLD`, `gold_income`… | ENGINE | 455 |
| Y307 | §1.5 | Under owner-agnostic wealth the exclusion is stronger still: `wealth(p)` is built from… | MODEL | 458 |
| Y308 | §1.5 | Gold is inert in vanilla trade value (`base_price = 0`, `goldtype = yes`), so the… | ENGINE | 461 |
| Y309 | §1.5 | Whether the per-province production-income field nevertheless carries the gold figure… | MODEL | 462 |
| Y310 | §1.5 | Any good with zero world production this month has no graph, because `s(n,g)` is… | MODEL | 467 |
| Y311 | §1.5 | A latent good acquires graph, value weight and survival-table entry on the first month… | MODEL | 469 |
| Y312 | §1.5 | Activation is not a local addition: a province produces exactly one trade good at a… | ENGINE | 471 |
| Y313 | §1.5 | In the month of conversion the new good gains a producer and the old good loses one, so… | MODEL | 475 |
| Y314 | §1.5 | The converting province is repriced, so `wealth(p)` changes and with it `c(n,g)` for… | MODEL | 477 |
| Y315 | §1.5 | `V_g` moves for both goods, reweighting every display, link value and AI score. | MODEL | 480 |
| Y316 | §1.5 | `Φ_w` moves on activation, because §1.6 runs DRAIN on that same wealth field. | MODEL | 481 |
| Y317 | §1.5 | An activation is a world-state change on the scale of a development change or a… | DESIGN | 483 |
| Y076 | §1.5 | Repricing to coal the 45 latent-coal provinces that are owned at 1444 flips 16 of 159… | MEASURED | 484 |
| Y077 | §1.5 | The counterfactual holds every non-repriced input fixed: province 4237 is both… | MEASURED | 486 |
| Y318 | §1.5 | Coal's base price of 10.0 is the highest in the shipped price table. | ENGINE | 490 |
| Y320 | §1.5 | Coal produces nowhere at the 1444 start. | ENGINE | 498 |
| Y321 | §1.5 | Coal's default trigger fires on Enlightenment (the Manufactories branches require… | ENGINE | 498 |
| Y322 | §1.5 | The 58 latent-coal provinces convert province-by-province over years rather than in a… | ENGINE | 501 |
| Y323 | §1.6 | `V_g = price(g) ·` the world sum of `goods_produced(m,g)` are the per-good value… | MODEL | 508 |
| Y324 | §1.6 | For the wealth good, supply is uniform: `s_w(n) = 1/N`. | MODEL | 510 |
| Y325 | §1.6 | For the wealth good, `c_w(n)` is the node's share of world wealth raised to `α_Φ`. | MODEL | 511 |
| Y326 | §1.6 | `b_w = s_w − c_w`, with `α_Φ = 2.0`, a hyperparameter. | MODEL | 512 |
| Y327 | §1.6 | `Φ_w = DRAIN(b_w)` — the §1.1 operator with wealth as the good. | MODEL | 514 |
| Y328 | §1.6 | `Φ_w` is the graph installed in the game. | DESIGN | 517 |
| Y329 | §1.6 | Under `Φ_w` every node supplies uniformly and rich nodes are net demanders, so all… | MODEL | 517 |
| Y078 | §1.6 | Both the sinks' count and their locations move with the wealth field, and `α_Φ` sets… | MODEL | 520 |
| Y080 | §1.6 | v2.0 through v4.0 said the count "emerges from concentration" and v5.0 said "the count… | MODEL | 524 |
| Y330 | §1.6 | What the world state moves is where the sinks are and how the map drains toward them,… | DESIGN | 528 |
| Y083 | §1.6 | Measured on 1444 data at `α_Φ = 2.0`: two sinks, `genua` and `hangzhou`, at `c_w` ranks… | MEASURED | 531 |
| Y084 | §1.6 | Both sinks are properties of the world, because the orientation does not depend on how… | MODEL | 532 |
| Y335 | §1.6 | With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same… | MODEL | 536 |
| Y085 | §1.6 | Measured on that LP directly, 40 of 40 permutations return a different optimal support… | MEASURED | 538 |
| Y087 | §1.6 | So the old sink set was partly an artifact of the node order, and v6.0 said so. | MODEL | 539 |
| Y986 | §1.6 | Phase 2 now breaks those ties inside the objective, with a cost symmetric in the arc… | MODEL | 542 |
| Y086 | §1.6 | Over 180 relabellings — three seeds of 60, every input held fixed — the orientation did… | MEASURED | 543 |
| Y987 | §1.6 | On the same LP under the tie-break cost, 0 of 40 permutations return a different… | MEASURED | 543 |
| Y988 | §1.6 | The instrument is a reimplementation, and a reimplementation whose Phase 2 minimises… | MEASURED | 549 |
| Y989 | §1.6 | A symmetric cost is required rather than a stylistic choice: a directional preference… | MODEL | 551 |
| Y091 | §1.6 | Nothing this section quotes about the installed graph is conditional on the node order. | MODEL | 556 |
| Y093 | §1.6 | Over the 180 relabellings the sink set, every edge direction, and the promotion and… | MEASURED | 556 |
| Y990 | §1.6 | The per-good graphs are a different matter: the tie-break cost is read from… | MODEL | 561 |
| Y991 | §1.6 | Under the first-order tie-break term alone, 84 of 290 per-good relabelling runs moved… | PROCESS | 563 |
| Y1007 | §1.6 | §2.3's second-order term took per-good relabelling sensitivity from 84 of 290 runs to… | MEASURED | 563 |
| Y1008 | §1.6 | Pinning the solver's optimality tolerance took the remaining per-good relabelling… | MEASURED | 565 |
| Y1009 | §1.6 | On this field the per-good graphs are order-invariant over the orderings tried, as… | MEASURED | 566 |
| Y336 | §1.6 | The emitter should still fix one canonical order, because both order-invariance… | DESIGN | 568 |
| Y993 | §1.6 | The value weights are the exception: `V_g` is `price(g)` times a sum over producers,… | MODEL | 570 |
| Y094 | §1.6 | Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is 1 promotion… | MEASURED | 573 |
| Y095 | §1.6 | Five sources, all in the bottom half of the wealth field, at `c_w` ranks 55–79 and mean… | MEASURED | 574 |
| Y337 | §1.6 | v2 called the sources "cul-de-sacs"; the degrees are not far off that reading here, but… | MODEL | 575 |
| Y096 | §1.6 | Every node drains to a sink, the map is acyclic and 159/159 oriented, the sink set is… | MEASURED | 577 |
| Y082 | §1.6 | 1444's `b_w` has largest magnitude 0.0347. | MEASURED | 578 |
| Y338 | §1.6 | `Φ_w`'s marking order is a per-node scalar whose descending comparison reproduces the… | MEASURED | 579 |
| Y097 | §1.6 | Per good on the same field: 2–8 sinks, mean 3.69, 29/29 acyclic, 0 fallbacks fired, and… | MEASURED | 583 |
| Y098 | §1.6 | Agreement with the per-good graphs is 55.1% of edge-goods and 54.8% value-weighted. | MEASURED | 586 |
| Y100 | §1.6 | `α_Φ = 2.0`, `TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6` are hyperparameters; the choice is… | DESIGN | 589 |
| Y102 | §1.6 | No derivation is claimed, none is implied, and none should be reconstructed from the… | DESIGN | 590 |
| Y103 | §1.6 | Across `α_Φ` = 1.00…8.00 at 0.01 the sink set is a step function, and `α_Φ = 2.0` sits… | MEASURED | 595 |
| Y104 | §1.6 | Sampled at six values the sink count is non-monotone: 3 → 1 → 2 → 2 → 1 → 1 across… | MEASURED | 597 |
| Y992 | §1.6 | For `TIE_EPS` the sink set is unchanged from about 1e-6 to about 1 — six orders of… | MEASURED | 598 |
| Y1010 | §1.6 | `TIE_EPS2` behaves the same way as `TIE_EPS` and was measured at 1e-7, 1e-6 and 1e-5,… | MEASURED | 602 |
| Y105 | §1.6 | A written warning against reintroducing the withdrawn justifications for `α_Φ` —… | DESIGN | 606 |
| Y106 | §1.6 | "Europe becomes the centre of trade as it develops" is the design claim, and it is what… | DESIGN | 611 |
| Y107 | §1.6 | At 1444 the map ends in Genoa and in Hangzhou, and as European development compounds… | MEASURED | 612 |
| Y108 | §1.6 | The mechanism carrying that is that wealth is linear in development, so developing a… | MODEL | 613 |
| Y340 | §1.6 | These are properties of this snapshot rather than constants of the model — what one… | DESIGN | 639 |
| Y112 | §1.6 | Because §1.3's wealth is linear in development, scaling development and scaling wealth… | MEASURED | 640 |
| Y341 | §1.6 | All three institutions the period is named for begin in Europe between 1450 and 1550:… | ENGINE | 644 |
| Y342 | §1.6 | The Renaissance's embracement bonus is `development_cost = -0.05`, a standing discount… | ENGINE | 647 |
| Y343 | §1.6 | Those institution bonuses are country-scoped, so §1.3 excludes them from wealth… | MODEL | 649 |
| Y345 | §1.6 | From the north the route to the Asian end is the Volga and the steppe: `white_sea →… | MEASURED | 653 |
| Y113 | §1.6 | From Iberia the route is the African coast and the Red Sea: `sevilla → safi → timbuktu… | MEASURED | 655 |
| Y114 | §1.6 | No route leaves `genua` at all — it is a sink, out-degree 0 against in-degree 5, so the… | MEASURED | 657 |
| Y994 | §1.6 | `english_channel` is not an end at this α: it drains to `genua` in two hops through… | MEASURED | 658 |
| Y115 | §1.6 | No Europe→sink route passes the Cape of Good Hope, checked exhaustively rather than… | MEASURED | 662 |
| Y346 | §1.6 | That no Europe→sink route passes the Cape is what a 1444 map should say, and it is the… | DESIGN | 664 |
| Y116 | §1.6 | The Cape is a live conduit rather than an idle one: in-degree 2, out-degree 2, with 81… | MEASURED | 667 |
| Y117 | §1.6 | The 81 is a count of pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`,… | MEASURED | 670 |
| Y118 | §1.6 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models… | MEASURED | 673 |
| Y120 | §1.6 | The Cape reverses under the same growth — 1444's… | MEASURED | 681 |
| Y347 | §1.6 | The 22 European nodes are the 18 western and central ones (`english_channel`,… | MODEL | 686 |
| Y121 | §1.6 | Dev-stacking a single node's top province concentrates the map on that node, and extra… | MEASURED | 690 |
| Y348 | §1.6 | The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change,… | MODEL | 706 |
| Y349 | §1.6 | Its replacement as the end-to-end correctness check is exact orientation equality… | DESIGN | 708 |
| Y350 | §1.7 | Merchant placement, range and the collect/steer choice are vanilla, with one merchant… | ENGINE | 713 |
| Y351 | §1.7 | A merchant present gives +2 trade power (`MERCHANT_MAX_POWER_BONUS`) and a +10% bonus… | ENGINE | 713 |
| Y352 | §1.7 | v1 and v2 both called the second bonus "+10% trade efficiency"; trade efficiency and a… | ENGINE | 713 |
| Y353 | §1.7 | Collect is vanilla, including the −50% penalty outside the home node. | ENGINE | 715 |
| Y354 | §1.7 | Under Steer the node window lists every link incident to the node. | MODEL | 717 |
| Y355 | §1.7 | The vanilla window already renders both an incoming and an outgoing link list as… | ENGINE | 717 |
| Y356 | §1.7 | What changes is what an incoming entry does — it must accept a merchant assignment… | DESIGN | 720 |
| Y357 | §1.7 | §2.7 item 14 settled that the incoming entry only navigates: clicking `Safi` in… | ENGINE | 721 |
| Y358 | §1.7 | A merchant assigned to link {n,m} steers every good oriented n → m. | MODEL | 726 |
| Y359 | §1.7 | A merchant assigned to link {n,m} is inert for every good oriented m → n. | MODEL | 727 |
| Y360 | §1.7 | A merchant keeps its assignment when a link flips; only its active good set changes. | MODEL | 728 |
| Y361 | §1.7 | The same physical link can host a merchant at each end, active on disjoint good sets. | MODEL | 730 |
| Y362 | §1.7 | Caravan power requires the merchant to be steering at least one good on that link;… | MODEL | 732 |
| Y363 | §1.7 | That constrains only the two steering conditions — collecting at an inland node as main… | MODEL | 733 |
| Y364 | §1.7 | The engine's own caravan grant conditions are `merchant_present_inland` and… | ENGINE | 734 |
| Y365 | §1.7 | §2.7 item 11 settles the caravan recipient, and §3.11 carries both readings of the… | DESIGN | 736 |
| Y366 | §1.8 | Trade power and collect/transfer intent are node-wide; what varies per good is what… | MODEL | 741 |
| Y367 | §1.8 | `collected_share(n,g) = 1` if n is a sink for g, else `P_collect / (P_collect +… | MODEL | 746 |
| Y368 | §1.8 | Transfer eligibility is per good: a country's power counts toward `P_transfer(g)` only… | MODEL | 750 |
| Y369 | §1.8 | The remainder moves per good by the vanilla two-case rule. | MODEL | 752 |
| Y370 | §1.8 | If any country steers `g` at `n`, the outgoing value of `g` is divided across outgoing… | ENGINE | 754 |
| Y371 | §1.8 | An outgoing link with no steerer receives nothing, even when other links are steered. | ENGINE | 754 |
| Y372 | §1.8 | A single steerer takes all of `g`'s outgoing value down its link, however little power… | ENGINE | 754 |
| Y373 | §1.8 | If no country steers `g` at `n`, the outgoing value splits evenly across `g`'s outgoing… | ENGINE | 756 |
| Y374 | §1.8 | At `g`'s sink there is no remainder: 100% is collected and divided among collectors by… | MODEL | 758 |
| Y375 | §1.8 | Vanilla gates still apply: trade range, and the rule that there is no transfer into a… | ENGINE | 760 |
| Y376 | §1.8 | What trade range gates is reach, not flow: every string, define and modifier that… | ENGINE | 761 |
| Y377 | §1.8 | No string, define or modifier ties range to link flow — which is a statement about the… | ENGINE | 766 |
| Y378 | §1.8 | There is no trade "supply range" in the engine; the only supply-range constructs are… | ENGINE | 769 |
| Y379 | §1.9 | A country whose provincial trade power in a node meets the threshold receives a share… | ENGINE | 775 |
| Y380 | §1.9 | The engine's own tooltip says power transfers "to trade nodes where it already has… | ENGINE | 775 |
| Y381 | §1.9 | Measured: France holds zero provinces and zero merchants in Sevilla and still appears… | ENGINE | 775 |
| Y382 | §1.9 | This line was §3.16's cautionary case; it is now closed, and it closed in favour of the… | PROCESS | 775 |
| Y383 | §1.9 | The propagation share is `1 / TRADE_PROPAGATE_DIVIDER`, and the threshold in raw power… | ENGINE | 775 |
| Y384 | §1.9 | Ship trade power propagates only where the country has a ship-propagation modifier, at… | ENGINE | 776 |
| Y385 | §1.9 | Propagation is strictly one hop and never chains. | ENGINE | 777 |
| Y386 | §1.9 | A node receives the summed contributions of all its downstream neighbours. | ENGINE | 778 |
| Y387 | §1.9 | Direction for propagation is read from `Φ_w`. | MODEL | 780 |
| Y388 | §1.10 | Any mechanism gated on one nation being upstream or downstream of another evaluates… | DESIGN | 784 |
| Y389 | §1.10 | Any node-pair direction dependency reads `Φ_w`. | DESIGN | 786 |
| Y390 | §1.10 | Where a gate scopes a set or a path, that scope reads `Φ_w` with a three-rung fallback… | DESIGN | 788 |
| Y391 | §1.10 | The mechanics below the gates are unpatched and unchanged; reorientation reaches them… | ENGINE | 794 |
| Y392 | §1.10 | Nothing in that group is patched and all of it moves monthly. | MODEL | 794 |
| Y393 | §1.10 | Trade-conflict casus belli thresholds are `JUSTIFY_TRADE_CONFLICT_LIMIT` (target) and… | ENGINE | 800 |
| Y394 | §1.10 | Privateer blocking is thresholded by `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`. | ENGINE | 802 |
| Y395 | §1.10 | Trade-company extra merchant and control are thresholded by… | ENGINE | 803 |
| Y396 | §1.10 | Improve Inland Routes needs 50% to establish and 40% to maintain plus a merchant… | ENGINE | 805 |
| Y397 | §1.10 | Propagate Religion needs 50% to establish and 50% to maintain in the default branch and… | ENGINE | 806 |
| Y398 | §1.10 | The nine `N_trade_power_for_propogate_religion` country-flag rungs are banded: maintain… | ENGINE | 806 |
| Y399 | §1.10 | The banding is the reverse of what v1 recorded: Improve Inland Routes is the one… | ENGINE | 808 |
| Y400 | §1.10 | Banding therefore absorbs very little chatter: a power share oscillating across any… | ENGINE | 810 |
| Y401 | §1.10 | Banding is not the only damper: three shipped defines rate-limit the mechanics that… | ENGINE | 812 |
| Y122 | §1.10 | `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to seven of the nine entries in… | ENGINE | 814 |
| Y123 | §1.10 | `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no` in… | ENGINE | 818 |
| Y124 | §1.10 | `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` means a… | ENGINE | 820 |
| Y125 | §1.10 | What is left exposed is everything without a cooldown, which is most of the ladder. | ENGINE | 821 |
| Y402 | §1.10 | The flicker-risk set is "every country at a single-valued limit, plus flagless… | ENGINE | 822 |
| Y403 | §1.10 | Casus belli availability is the most visible symptom, since it can appear and vanish… | ENGINE | 824 |
| Y126 | §1.10 | Measured on the 1444 start, the caravan cap of 50 is 9.4% to 47.0% of an inland node's… | MEASURED | 827 |
| Y127 | §1.10 | As a share of the node's total after the grant lands — 50/(total+50) — the same figures… | MEASURED | 827 |
| Y128 | §1.10 | On §2.2's derived 25-node inland basis (dropping `siberia`) the median is 21.3%, or… | MEASURED | 827 |
| Y404 | §1.10 | Caravan power is in this group but is not a threshold mechanic and is not a function of… | ENGINE | 827 |
| Y405 | §1.10 | When caravan power applies it is worth up to the cap for any major power — enough to… | MODEL | 827 |
| Y406 | §1.10 | The largest single incumbent holder runs 23.6 to 143.2, so a country at the caravan cap… | MEASURED | 827 |
| Y407 | §1.10 | v4.0 read the save's per-node `highest_power` field as the largest incumbent's power;… | ENGINE | 827 |
| Y408 | §1.10 | What `highest_power` does hold was not determined, and the model does not read it. | MODEL | 827 |
| Y409 | §1.10 | v1 and v2 both described caravan power as "a step function on raw power", which… | PROCESS | 827 |
| Y410 | §1.10 | No mission, decision, event, or trade company in 1.37.5 names a trade node — zero… | ENGINE | 829 |
| Y411 | §1.10 | Trade companies are bare province lists. | ENGINE | 830 |
| Y412 | §1.10 | Scripted content reaches nodes only structurally, through `home_trade_node`,… | ENGINE | 831 |
| Y413 | §1.10 | Nodes themselves never change under the mod — only connections do — so the… | MODEL | 838 |
| Y414 | §1.10 | What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers… | ENGINE | 840 |
| Y415 | §1.10 | That semantic exposure is accepted and listed for the compatibility pass rather than… | DESIGN | 842 |
| Y416 | §1.11 | The overlord always receives the treasure fleet. | DESIGN | 847 |
| Y417 | §1.11 | The fleet routes by the §1.10 ladder, passing each node en route where privateers skim… | MODEL | 847 |
| Y418 | §1.11 | Where the diversion mechanic is active, colonial gold income is diverted from the… | ENGINE | 849 |
| Y419 | §1.11 | Diverted gold does not enter `wealth` at either end, for the deeper reason of §1.5:… | MODEL | 850 |
| Y420 | §1.12 | The in-game economy is the per-good economy: node values, the node window, pie charts,… | DESIGN | 855 |
| Y421 | §1.12 | Trade map mode colours provinces by node and draws arrows between nodes rendering… | MODEL | 857 |
| Y422 | §1.12 | Clicking a province switches province colouring to the vanilla trade-goods rendering… | MODEL | 859 |
| Y423 | §1.12 | Value broken down by commodity is not representable in the vanilla UI: the node window… | ENGINE | 863 |
| Y424 | §1.12 | A link's two-way traffic is not representable: one scalar per link, shown as net. | ENGINE | 866 |
| Y425 | §1.12 | Per-country effective trade power where eligibility differs by good is not… | ENGINE | 867 |
| Y426 | §1.12 | There is no new art, sprites, shaders or map-mode chrome; making the node window's… | DESIGN | 869 |
| Y427 | §2.1 | The implementation is one program: a runtime-attached DLL that each month reads live… | DESIGN | 878 |
| Y428 | §2.1 | It ships with a generated `00_tradenodes.txt` for load time and a companion overlay for… | DESIGN | 878 |
| Y429 | §2.1 | The target platform is Windows/Steam. | DESIGN | 880 |
| Y430 | §2.1 | Achievements are off with any mod (`ACHIEVEMENTS_DISABLED_MODIFIED_GAME`). | ENGINE | 880 |
| Y431 | §2.1 | The engine will load an ironman save in a modded game — `Loading ironman in modded… | ENGINE | 881 |
| Y432 | §2.1 | EU4 multiplayer is lockstep with checksums, so every client must reach the same answer;… | ENGINE | 885 |
| Y434 | §2.1 | DRAIN's exposure is different in kind from v1's dense linear algebra, which was badly… | MODEL | 887 |
| Y435 | §2.1 | DRAIN's comparisons are of input-derived quantities (`DEF`, `b`, arc costs) rather than… | MODEL | 892 |
| Y1011 | §2.1 | The multiplayer question is no longer whether the arithmetic agrees to the last bit but… | DESIGN | 894 |
| Y995 | §2.1 | §2.3's two changes move the desync question from a design problem to a verification… | MODEL | 898 |
| Y1013 | §2.1 | The margin by which the optimum is unique is 3.8e-8 worst per good and 7.5e-6 on the… | MEASURED | 906 |
| Y1014 | §2.1 | Orientation under LP column permutation: 0 flips on the aggregate and on all 29 goods,… | MEASURED | 907 |
| Y1016 | §2.1 | A few units in the last place cannot change any decision this solver makes, so what… | MODEL | 911 |
| Y1017 | §2.1 | Check 1 — one binary per platform and no cross-platform sessions, because a single… | DESIGN | 914 |
| Y1018 | §2.1 | The `../v2-drain/` DLL precedent is already Windows- and Steam-only, so the one-binary… | MODEL | 915 |
| Y1019 | §2.1 | Check 2 — no runtime CPU dispatch in the LP solver and single-threaded: this is the… | DESIGN | 917 |
| Y1020 | §2.1 | Check 3 — §2.8's cross-implementation orientation check compares the DLL against the… | DESIGN | 921 |
| Y1021 | §2.1 | Every trade number EU4 writes to a save is quantised to 1/1000: 495 of 495 sampled… | ENGINE | 925 |
| Y1022 | §2.1 | Quantisation of that kind erases any divergence below half a grid step, which is the… | ENGINE | 927 |
| Y1023 | §2.1 | The files cannot settle whether the rounding happens in the simulation or only in the… | ENGINE | 928 |
| Y1024 | §2.1 | Quantisation would not rescue this solver either way: the orientation margins of 3.8e-8… | MODEL | 930 |
| Y436 | §2.1 | Until checks 1–3 are done, ship single-player only. | DESIGN | 934 |
| Y1025 | §2.1 | The reason for shipping single-player has changed: it is no longer "vertex selection is… | MODEL | 934 |
| Y437 | §2.2 | Solver item 1 is a parser for `common/tradenodes/00_tradenodes.txt` reading adjacency,… | DESIGN | 940 |
| Y438 | §2.2 | Solver item 2 is a parser for non-ironman saves reading province owner, `base_tax`,… | DESIGN | 941 |
| Y439 | §2.2 | Solver item 3 is a parser for `common/defines.lua` merged with `common/defines/`… | DESIGN | 942 |
| Y440 | §2.2 | `GP_COEFF` is read from `common/static_modifiers/00_static_modifiers.txt` rather than… | ENGINE | 948 |
| Y131 | §2.2 | World wealth is 10,607.40 annual ducats over 2,472 counted provinces. | MEASURED | 952 |
| Y441 | §2.2 | Solver item 5 is DRAIN per good: a min-cost b-flow using network simplex or a simplex… | DESIGN | 953 |
| Y442 | §2.2 | The Phase-4 evaluator's `unserved` and `stranded` must be equal by conservation, since… | MODEL | 955 |
| Y443 | §2.2 | `Φ_w` is one more DRAIN run with wealth as the good — the 30th solve, same code path. | MODEL | 957 |
| Y444 | §2.2 | Solver item 6 is a survival table `S_g[n][H]` for AI scoring, one table serving every… | DESIGN | 958 |
| Y445 | §2.2 | Solver item 7 is a mutual reachability census: 30 goods × 80 BFS producing an 80×80… | PROCESS | 959 |
| Y446 | §2.2 | Solver item 8 is a synthetic-shock harness that edits parsed province data and… | PROCESS | 960 |
| Y447 | §2.2 | Cost per good is one uncapacitated min-cost flow on 80 nodes and 318 arcs plus an… | MODEL | 962 |
| Y132 | §2.2 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one… | MEASURED | 963 |
| Y133 | §2.2 | Repeated 12-run experiments on one machine do not reproduce each other closely enough… | MEASURED | 965 |
| Y134 | §2.2 | v5.0's "0.17–0.21 s for all 29 goods" is not reproducible: across three replicates of… | MEASURED | 968 |
| Y448 | §2.2 | "Milliseconds each" holds already with a generic LP; the all-29 figure is what a native… | DESIGN | 970 |
| Y449 | §2.2 | There are two implementations of one specification: the reference solver (standalone,… | DESIGN | 975 |
| Y450 | §2.2 | The two implementations must agree on orientation exactly — a combinatorial comparison… | DESIGN | 975 |
| Y451 | §2.2 | The parsers and the harness stay reference-only, and the DLL never reads a save. | PROCESS | 977 |
| Y452 | §2.2 | Inland is derived rather than trusted from the flag: a node with no coastal province… | DESIGN | 979 |
| Y453 | §2.2 | The derivation and the flag disagree at exactly one node — `siberia` carries… | ENGINE | 980 |
| Y454 | §2.2a | v2 called the target "map-agnostic" while proving its central properties only for the… | MODEL | 985 |
| Y455 | §2.2a | Premise 1 is that the node graph is connected: reachability is LP feasibility, and the… | MODEL | 989 |
| Y456 | §2.2a | On a graph with more than one component the global balance is not enough — each… | MODEL | 990 |
| Y457 | §2.2a | Vanilla 1444 is one component. | MEASURED | 993 |
| Y458 | §2.2a | The solver must compute components once at load; on a single component it proceeds, and… | DESIGN | 995 |
| Y459 | §2.2a | The solver must not silently hand an infeasible program to the LP. | DESIGN | 998 |
| Y460 | §2.2a | v1 carried per-component renormalisation and v2 dropped it without replacement; v3… | PROCESS | 999 |
| Y461 | §2.2a | Premise 2 is that Phase 0 is a no-op, or the map-dependent properties are read as… | MODEL | 1002 |
| Y462 | §2.2a | Where Phase 0 acts, three properties weaken and the spec says so rather than asserting… | PROCESS | 1004 |
| Y463 | §2.2a | Global DAG is proved on a 2-core map and still proved where Phase 0 acts, because… | MODEL | 1009 |
| Y464 | §2.2a | Sink-set equality is measured exact 29/29 on a 2-core map and fails where Phase 0 acts,… | MEASURED | 1010 |
| Y465 | §2.2a | Marking order reproduces the DAG on a 2-core map and fails where Phase 0 acts, because… | MODEL | 1011 |
| Y135 | §2.2a | Where Phase 0 acts, free-edge determinism is unaffected but index-independence is not:… | MODEL | 1012 |
| Y466 | §2.2a | Two further cases are independent of Phase 0 and both break sink-set equality inside… | MEASURED | 1014 |
| Y467 | §2.2a | The stated target is connected maps: on a connected map with minimum degree at least 2… | DESIGN | 1019 |
| Y468 | §2.2a | On a connected map with pendants the algorithm still runs and still produces an… | MODEL | 1020 |
| Y469 | §2.2a | On a disconnected map the solver must renormalise per component or refuse. | DESIGN | 1022 |
| Y470 | §2.3 | Constants are read at runtime and never hardcoded. | DESIGN | 1027 |
| Y471 | §2.3 | The nine runtime-read uses map to named defines: `TRADE_PROPAGATE_DIVIDER`,… | ENGINE | 1029 |
| Y472 | §2.3 | `TRADE_MERCHANT_PRESENT` is a bonus on income, not trade efficiency. | ENGINE | 1036 |
| Y136 | §2.3 | The two wealth coefficients are not the same kind of constant: the emitter reads… | DESIGN | 1041 |
| Y137 | §2.3 | v3.0 through v5.0 said neither coefficient was in a file, and shipped a whole-install… | PROCESS | 1047 |
| Y473 | §2.3 | `GP_COEFF` is 0.2 goods produced per point of `base_production`, measured on four… | ENGINE | 1053 |
| Y474 | §2.3 | `TAX_COEFF` is 1.0 ducat per year per point of `base_tax`, measured on two provinces at… | ENGINE | 1054 |
| Y475 | §2.3 | Both coefficients are read off the tooltips' base lines, which carry no owner term —… | ENGINE | 1056 |
| Y476 | §2.3 | Neither coefficient is read off a province window, because a window figure carries the… | ENGINE | 1057 |
| Y477 | §2.3 | Prices come from `common/prices/00_prices.txt` at runtime and are never hardcoded. | ENGINE | 1058 |
| Y478 | §2.3 | The design constants are the excluded-goods list (defaulting to gold), the α price… | DESIGN | 1061 |
| Y479 | §2.3 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste,… | MODEL | 1071 |
| Y339 | §2.3 | Changing any of the three hyperparameters is a design decision, and §1.6 records how… | DESIGN | 1074 |
| Y996 | §2.3 | `TIE_EPS` and `TIE_EPS2` together set the Phase-2 objective, `cost(u,v) = 1 +… | MODEL | 1079 |
| Y1026 | §2.3 | The two cost terms do different jobs and only the first means anything: the first-order… | DESIGN | 1090 |
| Y1027 | §2.3 | The second-order term is tie-breaking and nothing else; its form is arbitrary and no… | DESIGN | 1092 |
| Y998 | §2.3 | A single cost vector does not make every solve unique, because uniqueness of an LP… | MODEL | 1095 |
| Y1028 | §2.3 | Measured on zero-reduced-cost arcs outside the support: the aggregate `b_w` goes from… | MEASURED | 1098 |
| Y1029 | §2.3 | Adding the second-order term takes the zero-reduced-cost arcs to 1 arc on 1 good. | MEASURED | 1100 |
| Y1030 | §2.3 | The solver's optimality tolerance is a correctness requirement rather than a… | MODEL | 1113 |
| Y1053 | §2.3 | `scipy.optimize.linprog`'s `method="highs"` options document that default as `1e-07`,… | MODEL | 1114 |
| Y1031 | §2.3 | The margin by which the tie-break makes the optimum unique runs as low as 3.8e-8 on… | MEASURED | 1116 |
| Y1032 | §2.3 | Measured: over six permutations of the LP's column order, `copper` and `paper` returned… | MEASURED | 1118 |
| Y1054 | §2.3 | The tolerance mechanism is confirmed rather than inferred, by bisecting the tolerance… | MEASURED | 1123 |
| Y1055 | §2.3 | Leaving the tolerance unset and setting it to 1e-7 give the same 8 flips over four… | MEASURED | 1123 |
| Y1057 | §2.3 | The flips therefore appear exactly when the tolerance exceeds the margin, which is the… | MODEL | 1126 |
| Y1033 | §2.3 | `flowop.LP_OPTS` ships 1e-10 — HiGHS's floor for these options, taken for headroom… | MEASURED | 1127 |
| Y1034 | §2.3 | No figure in this document moved when the pinned tolerance went in: the shipped column… | PROCESS | 1129 |
| Y1035 | §2.3 | What the second-order term costs: self-coherence with the per-good graphs falls 0.1–0.2… | MEASURED | 1132 |
| Y1036 | §2.3 | What the second-order term buys is replacing a tiebreak that was arbitrary and… | DESIGN | 1134 |
| Y1037 | §2.3 | The normalisation of `w` is load-bearing per good and that is a cost of the… | MODEL | 1144 |
| Y1039 | §2.3 | The choice of normalisation is a third arbitrary decision with an observable… | DESIGN | 1160 |
| Y997 | §2.3 | Every DRAIN solve uses this cost, per good as well as aggregate, and since `w` is node… | MODEL | 1163 |
| Y483 | §2.3 | DLC state is a third input axis: treasure-fleet diversion and caravan power are both… | ENGINE | 1168 |
| Y484 | §2.4 | The tradenodes file is generated once from the campaign start date's `Φ_w` and then… | DESIGN | 1172 |
| Y485 | §2.4 | The engine performs no topological sort; it validates that the file is one, logging… | ENGINE | 1174 |
| Y486 | §2.4 | Measured: a file with all 159 links declared backwards logged exactly 159 such errors… | ENGINE | 1177 |
| Y487 | §2.4 | What the engine does not tolerate is a cycle: a hand-authored two-node cycle produced… | ENGINE | 1181 |
| Y488 | §2.4 | The crash dump records no per-frame addresses. | ENGINE | 1183 |
| Y489 | §2.4 | Acyclicity is therefore a hard correctness requirement of the emitter, established by… | DESIGN | 1184 |
| Y490 | §2.4 | A reversed link is honoured completely: moving one `outgoing` block from `sevilla` to… | ENGINE | 1188 |
| Y491 | §2.4 | In that test Valencia moved from Sevilla's outgoing side to its incoming side, Sevilla… | ENGINE | 1190 |
| Y492 | §2.4 | Every provincial power figure was unchanged in that test. | ENGINE | 1193 |
| Y493 | §2.4 | That test is the mod's core premise verified end to end. | DESIGN | 1194 |
| Y494 | §2.4 | Item 1: emit in decreasing `Φ_w` marking order, which is the convention the engine… | ENGINE | 1196 |
| Y138 | §2.4 | A canonical node order is still a correctness requirement but is no longer what decides… | DESIGN | 1198 |
| Y495 | §2.4 | Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports… | MODEL | 1202 |
| Y139 | §2.4 | Measured on that objective, 40 of 40 permutations return a different optimal support. | MEASURED | 1204 |
| Y140 | §2.4 | Those permutations reach an objective identical to within a few units in the last place. | MEASURED | 1204 |
| Y147 | §2.4 | §2.3 now breaks those ties inside the objective. | MODEL | 1205 |
| Y141 | §2.4 | On the same LP under the tie-break cost 0 of 40 permutations return a different… | MEASURED | 1206 |
| Y143 | §2.4 | The tie-break cost is built from good-independent node wealth so it applies to every… | MEASURED | 1212 |
| Y146 | §2.4 | The counts are HiGHS-specific in their detail but not in kind: any simplex returns a… | MODEL | 1224 |
| Y144 | §2.4 | v6.0 quoted a 580-of-580 per-good sweep from… | PROCESS | 1226 |
| Y148 | §2.4 | §1.1's priority key ties in more places than §1.1 documents — besides the free-edge… | MEASURED | 1231 |
| Y496 | §2.4 | One visible consequence of node order: the node window renders its incoming/outgoing… | ENGINE | 1236 |
| Y149 | §2.4 | The end-flag list is a function of the world rather than of the node order: across the… | MEASURED | 1239 |
| Y497 | §2.4 | Item 2: `end=yes` on every `Φ_w` sink, stripped from any former end node that gains… | DESIGN | 1239 |
| Y150 | §2.4 | 1444 has two end nodes, `genua` and `hangzhou`, against vanilla's three. | MEASURED | 1242 |
| Y498 | §2.4 | The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter… | DESIGN | 1243 |
| Y499 | §2.4 | Item 3: link reversal means moving the `outgoing` block, reversing the `path` province… | DESIGN | 1246 |
| Y500 | §2.4 | Item 4: `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade` and… | DESIGN | 1247 |
| Y501 | §2.5 | Attachment uses pattern scanning and function hooking, following the EU4dll precedent,… | DESIGN | 1251 |
| Y502 | §2.5 | The mod ships a runtime-patching DLL rather than a modified executable. | DESIGN | 1251 |
| Y503 | §2.5 | The binary is frozen, so offsets found stay found. | ENGINE | 1251 |
| Y504 | §2.5 | The nation-pair direction gates of §1.10 are hooked and returned true at the call site… | DESIGN | 1253 |
| Y505 | §2.6 | The monthly trade tick runs in three passes: static power and modifiers; a pass from… | ENGINE | 1257 |
| Y506 | §2.6 | Written each tick: node trade value as the sum over goods of `value_g(n)`. | MODEL | 1263 |
| Y507 | §2.6 | Written each tick: node collectible pool as the sum over goods of `value_g(n) ·… | MODEL | 1264 |
| Y508 | §2.6 | Written each tick: per-link value as net realized flow summed over goods, in the… | MODEL | 1265 |
| Y509 | §2.6 | Country trade income is derived by the engine from the written fields, unless stored. | ENGINE | 1266 |
| Y510 | §2.6 | Feeding the engine the collectible pool is sufficient for a narrower reason than it… | MODEL | 1268 |
| Y511 | §2.6 | What factors out is `powershare_C`, a country's share among collectors, and whether a… | MODEL | 1268 |
| Y512 | §2.6 | There are two deadlines, not one window: display immediately after the value pass,… | ENGINE | 1272 |
| Y513 | §2.6 | Payment is bounded by the month boundary, since the treasury reconciles at the start of… | ENGINE | 1273 |
| Y514 | §2.6 | Per-link values are written net, which can be negative where realized flow opposes the… | MODEL | 1275 |
| Y515 | §2.7 | Items 1–10 are the v1 probe set, settled with a debugger on a vanilla install in one… | PROCESS | 1279 |
| Y516 | §2.7 | Items 12–15 are done: they were run against 1.37.5 in `../v2-drain/game-session.md` and… | ENGINE | 1282 |
| Y517 | §2.7 | Item 12 was dropped rather than run, because under owner-agnostic wealth the… | DESIGN | 1283 |
| Y518 | §2.7 | Probe 13 settled and reversed the hedge: the engine does not tolerate a cycle —… | ENGINE | 1287 |
| Y519 | §2.7 | Probe 14 settled and confirmed the spec: the incoming-link entry only navigates, and… | PROCESS | 1289 |
| Y520 | §2.7 | Probe 15 settled and reversed the spec's caution: the tooltip's "where it already has… | PROCESS | 1291 |
| Y151 | §2.7 | §1.9's "every immediately upstream node" is consistent with probe 15's reading — one… | ENGINE | 1294 |
| Y521 | §2.7 | The §2.4 item 3 link-reversal check is done and passed: a hand-flipped link loaded with… | ENGINE | 1297 |
| Y522 | §2.7 | The declaration-order companion question is settled: the engine validates order and… | ENGINE | 1300 |
| Y523 | §2.7 | Probe 1 is pass caching: for each of the three passes independently, does flipping a… | DESIGN | 1303 |
| Y524 | §2.7 | Probe 2 is pass 2's content: what imposes its ordering, given that propagation is one… | DESIGN | 1304 |
| Y525 | §2.7 | Probe 3 is write windows: where income accumulation sits relative to the value pass,… | DESIGN | 1305 |
| Y526 | §2.7 | Probe 4 is negative link values: write one and observe arrow rendering and… | DESIGN | 1306 |
| Y527 | §2.7 | Probe 5 is merchant storage: flip a link hosting a steering merchant and see whether… | DESIGN | 1307 |
| Y528 | §2.7 | Probe 6 is caravan, twice: does the engine grant it for a merchant assigned to a link… | DESIGN | 1308 |
| Y529 | §2.7 | Probe 7 is render data: is arrow render state separate from the economic link. | DESIGN | 1309 |
| Y530 | §2.7 | Probe 8 is `TRADE_PROPAGATE_THRESHOLD` semantics: set it to 4 and check whether the raw… | DESIGN | 1310 |
| Y531 | §2.7 | Probe 9 is diverted gold: does diverted colonial gold still appear in the per-province… | DESIGN | 1311 |
| Y532 | §2.7 | Probe 10 is caller enumeration: disassemble and list every call site of "is X… | DESIGN | 1312 |
| Y533 | §2.7 | Static string-table analysis already yields three named direction call sites —… | ENGINE | 1312 |
| Y534 | §2.7 | Probe 11 is the caravan recipient: place a merchant in a coastal node steering toward… | DESIGN | 1313 |
| Y535 | §2.7 | The engine tooltip and the identifier `merchant_steering_to_inland` both read as the… | ENGINE | 1313 |
| Y1040 | §2.7 | Probe 16 asks whether EU4's 1/1000 quantisation happens in the simulation or in the… | DESIGN | 1315 |
| Y1041 | §2.7 | If the rounding happens in the simulation the engine erases sub-milli-ducat divergence… | ENGINE | 1317 |
| Y1042 | §2.7 | Probe 16 settles what §2.1 may claim about the engine's own defence and whether the mod… | DESIGN | 1320 |
| Y536 | §2.7 | All writes land atomically at the tick hook with the sim paused. | DESIGN | 1327 |
| Y537 | §2.8 | Spice and cloves at 1444: source in Indonesia and both source there alone — `spices`… | MEASURED | 1333 |
| Y1043 | §2.8 | v6.0 listed Australia, Venice and Deccan among the spice and cloves termini; none of… | MEASURED | 1333 |
| Y540 | §2.8 | Malacca to Cape post-1500: spice routes Malacca to Cape to Europe. | MODEL | 1335 |
| Y541 | §2.8 | Malacca to Cape pre-1500: the corridor is withheld by range and the power-at-both-ends… | MODEL | 1336 |
| Y542 | §2.8 | A 1000 AD start puts sinks in the Muslim world and Song China, with no era data. | MODEL | 1337 |
| Y153 | §2.8 | On the razed field the result is order-invariant like the baseline: 40 of 40… | MEASURED | 1338 |
| Y155 | §2.8 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against… | MEASURED | 1338 |
| Y156 | §2.8 | Zeroing `beijing` also moves the map — 8 flips — because deleting a percent of world… | MEASURED | 1338 |
| Y544 | §2.8 | Ming losing the Mandate moves nothing on the day it happens, because the Mandate is an… | MODEL | 1339 |
| Y545 | §2.8 | That row is the owner-agnosticism check, not a responsiveness check. | DESIGN | 1339 |
| Y546 | §2.8 | A major war in China shifts corridors for the duration, reverting as devastation heals. | MODEL | 1340 |
| Y547 | §2.8 | Many poor provinces versus few rich: luxury demand goes to the rich-province node and… | MODEL | 1341 |
| Y548 | §2.8 | On a price crash α falls below 1 and regional sinks reappear. | MODEL | 1342 |
| Y549 | §2.8 | Caribbean 1650: sugar production income makes it a sink for cloth, tools and wine. | MODEL | 1343 |
| Y550 | §2.8 | Kilwa 1000: ivory income makes it a sink for Indian textiles. | MODEL | 1344 |
| Y551 | §2.8 | A consuming leaf terminates the DAG of every good it consumes but does not produce. | MODEL | 1345 |
| Y552 | §2.8 | An inert merchant's goods take the even split as if the node were empty, while… | MODEL | 1346 |
| Y553 | §2.8 | A node sinking spice but not cloth collects spice fully and cloth at the ratio, with… | MODEL | 1347 |
| Y554 | §2.8 | A near-balanced link may flip monthly, carries near-zero either way, and assignments… | MODEL | 1348 |
| Y555 | §2.8 | A two-way Atlantic corridor has merchants at both ends on disjoint good sets, neither… | MODEL | 1349 |
| Y556 | §2.8 | Economy tab versus overlay: every displayed trade figure matches the per-good economy… | DESIGN | 1350 |
| Y557 | §2.8 | Stock trade values are not reproducible run to run: two identical vanilla 1444 Castile… | ENGINE | 1350 |
| Y558 | §2.8 | AI merchant placement is randomised at start, and it is the three power-dependent… | ENGINE | 1350 |
| Y559 | §2.8 | Any comparison against unmodded numbers needs a tolerance and a null run. | DESIGN | 1350 |
| Y560 | §2.8 | Reachability is asserted every tick: 100% of every good's demand reachable from its… | MODEL | 1351 |
| Y561 | §2.8 | Conservation is asserted every good every tick: Phase-4 sum of `unserved` equals sum of… | MODEL | 1352 |
| Y562 | §2.8 | Determinism is asserted: re-running a tick reproduces the orientation bit-for-bit, and… | MODEL | 1353 |
| Y1044 | §2.8 | A new validation row asserts the LP is configured tighter than the tie-break margin:… | MODEL | 1354 |
| Y563 | §2.8 | Acyclicity is asserted on every per-good graph, on `Φ_w`, and on the emitted file's… | DESIGN | 1355 |
| Y564 | §2.8 | Sink-set containment is a hard assertion every tick, unconditionally: every sink inside… | MODEL | 1356 |
| Y565 | §2.8 | Asserting containment in `{selected} ∪ {promoted}` alone would halt on T3, which is… | MODEL | 1356 |
| Y566 | §2.8 | Sink-set equality is monitored rather than asserted: it is measured exact on 1444… | MEASURED | 1356 |
| Y567 | §2.8 | Where Phase 0 acts the equality does not apply and is not asserted; the check on a… | MODEL | 1357 |
| Y568 | §2.8 | Colonization check: an observer run to 1600 sees New World colonization proceed at… | MODEL | 1358 |
| Y569 | §2.8 | AI convergence check: greedy assignment settles with damping rather than oscillating. | MODEL | 1359 |
| Y570 | §2.8 | Latent-good check: while latent there is no graph, no value weight and no… | MEASURED | 1360 |
| Y571 | §2.8 | Cross-implementation check: the DLL and the reference implementation agree on… | DESIGN | 1361 |
| Y572 | §2.8 | `Φ_w`-vs-realized sign disagreement is measured rather than asserted, weighted by trade… | MEASURED | 1365 |
| Y573 | §2.8 | Flip behaviour is measured per decade in peace versus war, along with whether flips… | MODEL | 1369 |
| Y574 | §2.8 | Propagated-share change per node is measured on each flip alongside the… | MODEL | 1370 |
| Y575 | §2.8 | Total propagated power is not the quantity to watch: reorientation cannot change edge… | MODEL | 1370 |
| Y576 | §2.8 | Income balance is measured on two metrics — total world collected income and its… | DESIGN | 1371 |
| Y577 | §2.9 | The build is not phases but two tracks run in parallel. | DESIGN | 1375 |
| Y578 | §2.9 | The solver track starts with the defines parser, because §2.3 makes every constant a… | DESIGN | 1377 |
| Y580 | §2.9 | The memory track is the §2.7 probe session, all ten items on one trace. | DESIGN | 1383 |
| Y581 | §2.9 | Then: write §1.10's classified call-site list into the spec, gate income balance on… | PROCESS | 1385 |
| Y582 | §3.1 | Goal 1, world responsiveness: trade direction follows the world's current state, never… | DESIGN | 1393 |
| Y583 | §3.1 | Goal 2, realism: commodities flow differently, and China is a silk source and a spice… | DESIGN | 1394 |
| Y584 | §3.1 | Goal 3, preserve the feedback loop: sinks accumulate, fund development and reinforce,… | DESIGN | 1395 |
| Y585 | §3.1 | Goal 4, represent return flows: export regions historically imported manufactures, and… | DESIGN | 1396 |
| Y586 | §3.1 | Goal 5, route-aware direction: direction must reflect where a good can ultimately… | DESIGN | 1397 |
| Y587 | §3.1 | Goal 6: zero authored data. | DESIGN | 1398 |
| Y588 | §3.1 | Goal 7: the game's own numbers are the model's numbers, so anything reading trade… | DESIGN | 1399 |
| Y589 | §3.2 | Two families of orientation fail before this one: the first fails by theorem, the… | MODEL | 1403 |
| Y590 | §3.2 | Local comparison is monotone: orienting each edge by comparing its endpoints — wealth,… | MODEL | 1407 |
| Y591 | §3.2 | Monotonicity killed v1's rank-orientation strawman and the tested `s − c` operator the… | MEASURED | 1410 |
| Y592 | §3.2 | Merchants cannot repair a wrong orientation — a merchant selects among existing… | ENGINE | 1412 |
| Y593 | §3.2 | v1's Laplacian sink rule is exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour… | MEASURED | 1416 |
| Y594 | §3.2 | Because supply is sparse where demand is dense, that right-hand side is set by supply… | MEASURED | 1418 |
| Y595 | §3.2 | Under v1's Laplacian, sinks landed where the field was locally flat rather than where… | MEASURED | 1422 |
| Y596 | §3.2 | v1 and v2 quantified the asymmetry as "supply contrast 10⁷ against demand contrast… | MODEL | 1425 |
| Y157 | §3.2 | What the ratio metric cannot see is the thing the diagnosis rests on: sparsity — most… | MODEL | 1427 |
| Y158 | §3.2 | On the contrast metric itself the demand side is the wider one, not the supply side. | MEASURED | 1431 |
| Y597 | §3.2 | No parameter fixes the Laplacian's placement: an α strong enough to matter destroys… | MODEL | 1432 |
| Y159 | §3.2 | Better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the… | MEASURED | 1433 |
| Y160 | §3.2 | Moving the spice sink to a Chinese node takes a multiple of that node's wealth in the… | MEASURED | 1434 |
| Y161 | §3.2 | These are wealth multiples rather than demand multiples: because demand is `wealth^α`… | MODEL | 1436 |
| Y162 | §3.2 | The four named Chinese nodes are not the cheapest — `girin` needs 3.89× and `yumen`… | MEASURED | 1437 |
| Y598 | §3.2 | v2 wrote "1.7× where 4–5× is needed", which compressed two different quantities into… | MODEL | 1439 |
| Y599 | §3.2 | The conservation lesson: operators that impose node balance somewhere (the v1 solve, a… | MODEL | 1442 |
| Y600 | §3.2 | DRAIN takes conservation from the b-flow — reachability is LP feasibility on a… | MODEL | 1444 |
| Y601 | §3.2 | Of the four claims, v1 did state aggregate acyclicity as C061 ("`Φ` is a potential, so… | PROCESS | 1448 |
| Y163 | §3.2 | Sink placement is a measurement on one input: on 1444, final sinks = `{selected ∩… | MEASURED | 1453 |
| Y164 | §3.2 | v5.0 tried to rescue that equality by attaching two conditions — Phase 0 a no-op and no… | MODEL | 1455 |
| Y602 | §3.2 | T1, pendant importer: triangle A(+5), B(−3), D(0) with a leaf C(−2) on B; Phase 0 peels… | MEASURED | 1460 |
| Y603 | §3.2 | T2, free-edge race inside the 2-core: a five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1… | MEASURED | 1463 |
| Y604 | §3.2 | T3, the fallback branch inside the 2-core: triangle A, B, C with `b = 0` at all three… | MEASURED | 1468 |
| Y605 | §3.2 | What survives unconditionally is the subset direction within the 2-core over the set… | MODEL | 1474 |
| Y606 | §3.2 | Pendant net-importers are the only sinks outside that set. | MODEL | 1477 |
| Y607 | §3.2 | §2.8 therefore carries two runtime checks rather than one weakened one: containment… | DESIGN | 1477 |
| Y608 | §3.2 | On pendant edges the Phase-4 orientation rule is the check and T1 is expected output. | DESIGN | 1480 |
| Y609 | §3.2 | Written as a single assertion with an escape clause, all three counterexamples would… | MODEL | 1481 |
| Y610 | §3.2 | Free-edge direction is marking order under the (DEF asc, b asc, index) priority,… | MEASURED | 1484 |
| Y611 | §3.2 | Reachability: the orientation contains the LP certificate, so every unit of demand is… | MEASURED | 1496 |
| Y612 | §3.2 | Aggregate acyclicity: `Φ_w` is itself a DRAIN orientation, so it is acyclic by the same… | MODEL | 1498 |
| Y613 | §3.2 | `Φ_w`'s marking order is a per-node scalar reproducing the DAG, for any consumer that… | MODEL | 1500 |
| Y615 | §3.2 | The corridor runs through the Cape, which is the short route to Atlantic Europe:… | MEASURED | 1507 |
| Y616 | §3.2 | Peripheral termini still exist — the LP's branch ends are consumed at the end of the… | MODEL | 1511 |
| Y617 | §3.3 | Demand is purchasing power, and under §1.3 purchasing power is what the place is worth… | DESIGN | 1516 |
| Y618 | §3.3 | Wealth captures return flows for free: a sugar island's production term is carried by… | MODEL | 1516 |
| Y619 | §3.3 | The return-flow effect is real but modest at vanilla prices: sugar (3.0), cocoa (4.0)… | ENGINE | 1516 |
| Y620 | §3.3 | v1 and v2 said "negligible development but large production income", which overstated… | MODEL | 1516 |
| Y621 | §3.3 | There is no colonial-nation dependency, no timeline restriction and no owner dependency. | MODEL | 1516 |
| Y622 | §3.3 | Wealth is chosen for what the place is rather than who runs it: autonomy drift,… | MODEL | 1518 |
| Y623 | §3.3 | What remains still moves deliberately: development changes, trade goods change, prices… | MODEL | 1518 |
| Y624 | §3.3 | A besieged province genuinely produces less, so that volatility is economics rather… | DESIGN | 1518 |
| Y625 | §3.3 | What the model removes is the volatility that was really about ownership: a province no… | MODEL | 1518 |
| Y626 | §3.3 | The instruction is to plan around the world rather than around the graph: the map is… | DESIGN | 1518 |
| Y627 | §3.3 | Trade income is excluded for circularity rather than speed: including it would close a… | MODEL | 1520 |
| Y628 | §3.3 | The loop still closes the long way: trade income funds development, and development… | MODEL | 1520 |
| Y165 | §3.3 | `cape_of_good_hope`'s `members` list has 20 entries but province 1460 is a sea zone,… | ENGINE | 1522 |
| Y629 | §3.3 | Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4×… | ENGINE | 1522 |
| Y630 | §3.3 | Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain… | MODEL | 1526 |
| Y631 | §3.3 | The distortion is measured against the per-province form the model defines rather than… | MODEL | 1527 |
| Y632 | §3.3 | v2 said a 77-province node "beats a 19-province node of equal total wealth by 2×"; at… | MODEL | 1535 |
| Y633 | §3.3 | With the exponent inside the sum, superlinear demand concentrates where individual… | MODEL | 1538 |
| Y634 | §3.4 | Production efficiency does not conjure more cloves; it means the owner extracts more… | MODEL | 1544 |
| Y635 | §3.4 | Owner effects do not belong in demand either: v1 and v2 excluded them from supply and… | MODEL | 1546 |
| Y636 | §3.4 | Supply and demand are both properties of the place, so the supply-side argument applies… | DESIGN | 1546 |
| Y637 | §3.4 | The aggregate uses trade value rather than production income because a province's trade… | MODEL | 1548 |
| Y166 | §3.4 | In v1 substituting production income also measurably broke the α = 1 identity, with… | MEASURED | 1550 |
| Y638 | §3.5 | Anchoring at 2 ducats rather than the price median means a good's market concentration… | MODEL | 1556 |
| Y639 | §3.5 | Under a median anchor a good could concentrate because some unrelated commodity got… | MODEL | 1556 |
| Y640 | §3.5 | At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base… | ENGINE | 1558 |
| Y641 | §3.5 | Grain is 2.5, not the 1.25 v1 recorded; both of v1's figures were price/P₀ misread as… | ENGINE | 1560 |
| Y642 | §3.5 | The sublinear regime is entered only when a price event pushes a good beneath the… | ENGINE | 1561 |
| Y167 | §3.5 | `change_price` values are fractions of the good's base price rather than ducats, and… | ENGINE | 1567 |
| Y168 | §3.5 | The install carries 161 textual `change_price` blocks — 93 in `events/`, 14 in… | ENGINE | 1573 |
| Y169 | §3.5 | Ten of the 161 never execute — four inside `effect_tooltip = "…"` strings, three inside… | ENGINE | 1575 |
| Y170 | §3.5 | Six of the seven quoted blocks duplicate a block already counted in `events/` and the… | PROCESS | 1578 |
| Y171 | §3.5 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them;… | PROCESS | 1581 |
| Y172 | §3.5 | v5.0 claimed the scan was "guarded by a per-file count assertion", and there was no… | PROCESS | 1582 |
| Y173 | §3.5 | `verify6.py` checks the census only by requiring the printed total to match a computed… | PROCESS | 1584 |
| Y174 | §3.5 | The reason a plain parse misses the quoted blocks is mechanical: `pdx.py` tokenises a… | MODEL | 1586 |
| Y643 | §3.5 | The history route matters: `wool`'s largest single negative is `NEW_DRAPERIES` at −0.25… | ENGINE | 1590 |
| Y175 | §3.5 | 1.875 is the single-key floor rather than the campaign figure: the same `1540.1.1`… | ENGINE | 1592 |
| Y176 | §3.5 | The partition needs the history value: `events/PriceChanges.txt`'s −0.20 for the same… | ENGINE | 1595 |
| Y644 | §3.5 | v2's 13 was right, and v3.0 reached 12 by parsing four of the five trees. | PROCESS | 1598 |
| Y645 | §3.5 | The point of having the sublinear regime is that without it a crash could only fail to… | DESIGN | 1599 |
| Y646 | §3.5 | α is deliberately mild: production geography is what differentiates goods and α… | DESIGN | 1603 |
| Y647 | §3.6 | A margin on orientation is a correctness bug rather than a tuning knob: holding an edge… | MODEL | 1607 |
| Y648 | §3.6 | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based… | MEASURED | 1609 |
| Y649 | §3.6 | The node-file format represents cycles perfectly well — it is a list of named directed… | ENGINE | 1610 |
| Y650 | §3.6 | What the design depends on is the engine's behaviour on a cyclic file, and that is now… | ENGINE | 1612 |
| Y651 | §3.6 | A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single… | ENGINE | 1613 |
| Y652 | §3.6 | The engine walks the node graph recursively and a cycle never terminates. | ENGINE | 1616 |
| Y653 | §3.6 | Acyclicity is enforced because the engine provably cannot survive its absence, not — as… | DESIGN | 1617 |
| Y654 | §3.6 | Nothing needs to stop churn: a link whose flow-support membership alternates month to… | MEASURED | 1620 |
| Y655 | §3.6 | The "carries near-nothing" half is measured rather than derived, because v1's… | MODEL | 1622 |
| Y656 | §3.6 | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, zero… | MEASURED | 1624 |
| Y657 | §3.6 | At exactly degenerate inputs — two equal-hop corridors — the map from `b` to the chosen… | MODEL | 1626 |
| Y1046 | §3.6 | With both cost terms and the solver's optimality tolerance pinned, the optimum is… | MEASURED | 1628 |
| Y1047 | §3.6 | The discontinuity remains a property of the program: an input that made two routings… | MODEL | 1638 |
| Y658 | §3.6 | v1's ε is deleted because the problem it patched no longer exists: the Laplacian… | MODEL | 1641 |
| Y659 | §3.6 | DRAIN's free edges are oriented combinatorially: the priority sweep's key (DEF, b,… | MODEL | 1644 |
| Y660 | §3.6 | The measured count of exact key ties on 1444 data is zero, and the LP itself is… | MEASURED | 1647 |
| Y661 | §3.6 | Determinism is asserted per tick rather than approximated by a nudge. | DESIGN | 1649 |
| Y662 | §3.6 | What replaces the ε-magnitude question in §3.13 is the cross-machine question, which… | DESIGN | 1650 |
| Y1048 | §3.6 | The LP does not need to pivot identically, only to reach the same optimum, which the… | MODEL | 1651 |
| Y663 | §3.7 | Vanilla's rule is that effective trade power counts only countries which collect or… | ENGINE | 1656 |
| Y664 | §3.7 | Under a per-good model "downstream" is per good, so at a node where your home is… | MODEL | 1658 |
| Y665 | §3.7 | Per-good eligibility returns true for some goods at every node, so no nation is ever… | MODEL | 1658 |
| Y666 | §3.7 | Forcing eligibility true for all goods at once would be "direction doesn't exist"… | MODEL | 1658 |
| Y667 | §3.7 | The common misstatement — that any non-collecting country with trade power is… | ENGINE | 1660 |
| Y668 | §3.8 | The vanilla gates encode an assumption that a nation pair has one global relationship… | MODEL | 1664 |
| Y669 | §3.8 | Every province is upstream for some good, because a region that receives your cloth… | MODEL | 1664 |
| Y670 | §3.8 | There is no fact of the matter for the gate to test, so the honest fix is to stop… | DESIGN | 1664 |
| Y671 | §3.8 | Node-pair dependencies are different and keep reading `Φ_w`, because propagation is a… | MODEL | 1666 |
| Y672 | §3.8 | That distinction is easy to miss and expensive to get wrong. | DESIGN | 1666 |
| Y673 | §3.8 | Propagate Religion is node-local — it establishes a centre of conversion in the node's… | PROCESS | 1668 |
| Y674 | §3.8 | The shipped policy file gates Propagate Religion on the trade share and the node being… | ENGINE | 1671 |
| Y675 | §3.8 | No trading policy anywhere in `00_trading_policies.txt` tests upstream/downstream. | ENGINE | 1673 |
| Y676 | §3.8 | Three of the five trading policies have no trade-share threshold at all —… | ENGINE | 1675 |
| Y677 | §3.8 | This is written down because the deferred artifact does not exist yet, and a community… | DESIGN | 1676 |
| Y678 | §3.8 | Scopes read `Φ_w` rather than any-good reachability, because a gate is a boolean while… | DESIGN | 1680 |
| Y679 | §3.8 | `Φ_w` is the graph the engine already walks, so those call sites are left alone, which… | ENGINE | 1680 |
| Y680 | §3.8 | Reading `Φ_w` for scopes is legible — one map predicts where fleets sail — and… | DESIGN | 1680 |
| Y681 | §3.8 | Any-good connectivity on 1444 data under DRAIN is 90.6% (5,723 of 6,320) of ordered… | MEASURED | 1680 |
| Y682 | §3.9 | The installed graph exists for the engine's direction-dependent systems — propagation,… | DESIGN | 1684 |
| Y683 | §3.9 | What vanilla's authored arrows encode is empires pointing at the biggest cities and… | ENGINE | 1686 |
| Y685 | §3.9 | Wealth pulls but the wealthiest node is not automatically an end: what makes an end is… | MODEL | 1688 |
| Y177 | §3.9 | On this field `english_channel` is the richest node at 316.6 and is not a sink — it… | MEASURED | 1689 |
| Y686 | §3.9 | `Φ_w` reuses the §1.1 operator unchanged: one implementation, one set of guarantees (LP… | DESIGN | 1702 |
| Y688 | §3.9 | The value-weighted net flow (the sum over goods of `V_g · net_g`) is a flow, flows… | MEASURED | 1709 |
| Y690 | §3.9 | `Φ_w` is adopted for one operator, one set of guarantees, and ends that move with the… | DESIGN | 1714 |
| Y181 | §3.9 | v2.1 through v4.0's "two vanilla-like ends at 1444" justification is withdrawn and must… | MODEL | 1717 |
| Y691 | §3.9 | A difference in `Φ_w` across a link is not the net value crossing it. | MODEL | 1724 |
| Y692 | §3.9 | Realized movement follows vanilla propagation — a good can be diluted by an even split… | MODEL | 1725 |
| Y693 | §3.9 | That is why the disagreement rate is measured rather than assumed, and why display… | DESIGN | 1727 |
| Y694 | §3.9 | Link values are realized flows, which makes conservation hold by construction. | MODEL | 1729 |
| Y695 | §3.10 | Paying countries correctly while leaving the display wrong is a strictly weaker… | ENGINE | 1733 |
| Y696 | §3.10 | The engine's data model is sufficient at node level for a narrower reason than it first… | MODEL | 1735 |
| Y697 | §3.10 | What factors out is `powershare_C`, a country's share among collectors, and whether a… | MODEL | 1735 |
| Y698 | §3.10 | `income_C(n)` = the sum over goods of `value_g(n) · collected_share(n,g) ·… | MODEL | 1738 |
| Y699 | §3.10 | That is an identity rather than a measurement: `powershare_C(n)` carries no `g`, so it… | MODEL | 1742 |
| Y700 | §3.10 | Every term that feeds a collector's power at a node is node-wide — the merchant bonus,… | MODEL | 1742 |
| Y701 | §3.10 | One scalar per node reproduces every country's income exactly, and the engine's own… | MODEL | 1742 |
| Y702 | §3.10 | v1 through v4.0 quoted "agreement to 5.7e-14" here and 1.4e-14 below; both are… | PROCESS | 1742 |
| Y184 | §3.10 | Propagation is kept on a single graph, and the reason is not the one v1 through v6.0's… | DESIGN | 1744 |
| Y186 | §3.10 | `gulf_of_siam`'s 29 goods leave it by seven distinct downstream sets. | MEASURED | 1744 |
| Y187 | §3.10 | Per-good propagation does not break the income identity: defining `ps̄_C` as the… | MODEL | 1744 |
| Y188 | §3.10 | Both inputs to `ps̄_C` already exist per good at write time, and §2.6 sums exactly them… | MODEL | 1744 |
| Y189 | §3.10 | The real cost is that `ps̄_C` is not derivable from trade power alone: it is… | MODEL | 1746 |
| Y190 | §3.10 | That is a claim about what the engine exposes rather than about a magnitude, and it is… | DESIGN | 1746 |
| Y191 | §3.10 | Every magnitude previous versions quoted here — v1 through v3.0's "off by 5.96 ducats… | PROCESS | 1746 |
| Y192 | §3.10 | No figure of the author's own is quoted here, because the identity holds and the… | DESIGN | 1746 |
| Y703 | §3.10 | Only the decomposition by good exceeds what the engine can hold. | ENGINE | 1748 |
| Y704 | §3.11 | In vanilla, steering is outgoing-only: trade cannot be steered upstream at any amount… | ENGINE | 1752 |
| Y705 | §3.11 | The display is not outgoing-only: the node window already lists incoming links as… | ENGINE | 1754 |
| Y706 | §3.11 | Because only outgoing links can be steered, "assigned" and "steering" are the same… | ENGINE | 1755 |
| Y707 | §3.11 | §1.7 makes incoming entries assignable and pulls "assigned" and "steering" apart. | DESIGN | 1758 |
| Y708 | §3.11 | The engine's caravan grant fires on `merchant_present_inland` or… | ENGINE | 1758 |
| Y709 | §3.11 | The caravan tooltip reads as granting the bonus in the inland node ("steers towards an… | ENGINE | 1760 |
| Y710 | §3.11 | §2.7 item 11 settles the recipient with one merchant and two node windows, and the… | DESIGN | 1762 |
| Y711 | §3.11 | §1.7's added condition is the right guard under both readings. | DESIGN | 1765 |
| Y712 | §3.11 | Caravan power is total country development divided by 3 plus policy and idea modifiers,… | ENGINE | 1765 |
| Y713 | §3.11 | Nineteen countries are at the caravan cap from raw 1444 development alone, and… | MEASURED | 1766 |
| Y714 | §3.11 | Caravan power does not scale with node presence at all. | ENGINE | 1768 |
| Y715 | §3.11 | Requiring the merchant to steer something restores the vanilla state of affairs, and… | DESIGN | 1770 |
| Y716 | §3.12 | The argument is consistency with §3.8: the gate compares two trade capitals on a graph… | DESIGN | 1775 |
| Y717 | §3.12 | v1 claimed a stronger argument — that the gate is bistable, denial raising the colonial… | PROCESS | 1776 |
| Y718 | §3.12 | That bistability argument is deleted: gold income never enters `wealth` at all, so… | MODEL | 1778 |
| Y719 | §3.12 | The engine's own denial branch confirms what denial does: "They will keep their gold… | ENGINE | 1780 |
| Y720 | §3.12 | A slow second-order version survives — kept gold spent on development raises `base_tax`… | DESIGN | 1781 |
| Y721 | §3.12 | Inflation scales with money received relative to economy size, so universal granting… | ENGINE | 1786 |
| Y722 | §3.12 | The route rule is a balance dial, since privateers skim per node passed, which is why… | DESIGN | 1786 |
| Y723 | §3.13 | Prose-sourced questions are to be distrusted and nothing built on them. | DESIGN | 1790 |
| Y724 | §3.13 | Colonization's gate shape rests on one mod author's report, contradicted in-thread, and… | PROCESS | 1792 |
| Y725 | §3.13 | Static string-table analysis leans the same way: the only direction-refusal strings in… | ENGINE | 1792 |
| Y726 | §3.13 | The caller enumeration must be able to return "no colonization gate exists" as a… | DESIGN | 1792 |
| Y727 | §3.13 | Derived questions are probably right and cheaply falsifiable. | DESIGN | 1794 |
| Y728 | §3.13 | The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by… | ENGINE | 1796 |
| Y729 | §3.13 | Propagation is one hop and cannot chain, so something else in pass 2 imposes its… | ENGINE | 1797 |
| Y730 | §3.13 | The debugger-only list is shorter than v1 believed: of §2.7, only pass caching, pass-2… | DESIGN | 1799 |
| Y731 | §3.13 | Items 11–15 need a save, a tooltip, or one file edit, and the propagation-threshold and… | DESIGN | 1800 |
| Y732 | §3.13 | Three of the cheap probes — caravan recipient, cyclic file, incoming-link button —… | PROCESS | 1802 |
| Y733 | §3.13 | One question is open in the v6.0 wealth model, and it is a question rather than a… | DESIGN | 1805 |
| Y193 | §3.13 | The one open wealth question is now a design question rather than a classification one:… | DESIGN | 1808 |
| Y195 | §3.13 | The keys `trade_goods_size` and `trade_goods_size_modifier` are granted in many places:… | ENGINE | 1810 |
| Y194 | §3.13 | v3.0 through v5.0 tried to admit the province-scoped subset by rule, and that rule was… | PROCESS | 1813 |
| Y196 | §3.13 | Re-admitting any of those sources re-admits the maintenance burden with it, and the… | DESIGN | 1815 |
| Y734 | §3.13 | Settled and moved: `local_production_efficiency` from a trade good is outside wealth,… | ENGINE | 1820 |
| Y735 | §3.13 | Settled and moved: `TAX_COEFF` is 1.0 across the development range — `Base: 0.49… | ENGINE | 1823 |
| Y736 | §3.13 | `k`, `α_min` and `α_max` remain unresolved; the test is whether they produce the… | DESIGN | 1829 |
| Y738 | §3.13 | Whether `α_min` ever bites is now bounded from files: the sublinear regime is reachable… | ENGINE | 1845 |
| Y740 | §3.13 | Unclamped α-squared is a demand-model decision, because luxuries become court goods. | DESIGN | 1856 |
| Y742 | §3.13 | The baseline does not adopt the calibration, and adopting it is a §1.4 decision rather… | DESIGN | 1859 |
| Y198 | §3.13 | v2 said Beijing "holds the richest single province", which it does not — that is… | MEASURED | 1861 |
| Y743 | §3.13 | The open multiplayer item is build discipline rather than LP pivot determinism, which… | DESIGN | 1863 |
| Y1049 | §3.13 | What is open is whether the shipped solver build does runtime CPU dispatch or threads… | MODEL | 1863 |
| Y1050 | §3.13 | Also open is whether the DLL reproduces the reference implementation's orientation… | DESIGN | 1866 |
| Y744 | §3.13 | AI merchant reassignment cadence is open. | DESIGN | 1869 |
| Y745 | §3.14 | The two ends of a link never compete: a merchant at `n` on {n,m} moves goods oriented n… | MODEL | 1873 |
| Y746 | §3.14 | One precompute serves every country: for each good, a backward pass over its DAG gives… | MODEL | 1875 |
| Y747 | §3.14 | `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. | MODEL | 1875 |
| Y748 | §3.14 | All three survival-table inputs are country-independent aggregates, so this is one… | MODEL | 1875 |
| Y749 | §3.14 | v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the… | MODEL | 1875 |
| Y750 | §3.14 | Scoring reads the survival table for both steering and collecting, so the opportunity… | MODEL | 1877 |
| Y751 | §3.14 | The off-home penalty is a power modifier rather than a haircut on value: it reduces the… | ENGINE | 1879 |
| Y752 | §3.14 | Scoring a collect candidate as value × share × 0.5 is wrong; the halving must be… | MODEL | 1879 |
| Y753 | §3.14 | That is also why the off-home penalty falls out of the survival table at all: the table… | MODEL | 1879 |
| Y754 | §3.14 | The home-node bonus is voided entirely by placing any collector outside the home node,… | ENGINE | 1881 |
| Y755 | §3.14 | Greedy scoring against a moving field can oscillate between AIs; damping the shares… | MODEL | 1881 |
| Y756 | §3.14 | Reassignment cadence is undecided and is the one item left for the human, because… | DESIGN | 1883 |
| Y757 | §3.14 | Mirroring vanilla's cadence is the stated preference, but the relevant define was not… | DESIGN | 1885 |
| Y758 | §3.14 | The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure… | MODEL | 1886 |
| Y759 | §3.14 | The argument for computing the cadence is that vanilla's cadence was tuned against a… | DESIGN | 1888 |
| Y760 | §3.15 | The v1 Laplacian potential as the orientation core is rejected: its sink placement is… | MODEL | 1892 |
| Y200 | §3.15 | v3.0 and v4.0 repeated the 10⁷ versus 10²–10³ ratio in this entry while v4.0's own §3.2… | PROCESS | 1896 |
| Y199 | §3.15 | The Laplacian entry maintains no copy of the contrast measurement — §3.2 carries it —… | MODEL | 1897 |
| Y201 | §3.15 | `cloves` has a single producer and so no contrast to measure at all, which is the… | MODEL | 1899 |
| Y761 | §3.15 | The Laplacian was diagnosed, measured and replaced, and what it did guarantee — 100%… | MODEL | 1901 |
| Y762 | §3.15 | Pure min-cost-flow orientation with no sweep is rejected: it orients only the roughly… | MEASURED | 1905 |
| Y202 | §3.15 | Ranked orientation wins the sink-demand alignment statistics — a far higher share of… | MODEL | 1909 |
| Y203 | §3.15 | Seeded basin growth converges flow to the chosen seeds and starves everything off a… | MODEL | 1918 |
| Y763 | §3.15 | Seeded basin growth's useful ideas — HHI-adaptive sink count and stall self-correction… | MODEL | 1920 |
| Y764 | §3.15 | DEF-descending free-edge priority is rejected as measurably worse: on the certificate,… | MEASURED | 1924 |
| Y765 | §3.15 | Authored demand weights are rejected: authored data in a model that needs none. | DESIGN | 1929 |
| Y766 | §3.15 | Trade income inside `wealth` is rejected: it reintroduces flow-demand-orientation-flow… | MODEL | 1931 |
| Y767 | §3.15 | Node-level α is rejected: it makes demand concentration a function of how finely the… | MODEL | 1933 |
| Y768 | §3.15 | A median-relative α anchor is rejected: a good's concentration would shift because… | MODEL | 1935 |
| Y769 | §3.15 | α floored at 1 is rejected: it discards the cheap-bulk regime. | DESIGN | 1937 |
| Y770 | §3.15 | Production income as the aggregate supply term is rejected because it makes world… | MODEL | 1939 |
| Y771 | §3.15 | A τ margin on orientation is rejected: it manufactures cycles. | MODEL | 1941 |
| Y772 | §3.15 | Uniform supply in the aggregate solve is a v1 entry, moot in v2 and retained for… | MODEL | 1943 |
| Y205 | §3.15 | The 3-mass gravity field over the top-3 pairwise-unconnected demanders reproduces… | MODEL | 1954 |
| Y775 | §3.15 | The emergent-count wealth good replaced the pinned-count fields. | MODEL | 1963 |
| Y776 | §3.15 | A vestigial in-game economy with net treasury settlement is rejected: correct… | DESIGN | 1965 |
| Y778 | §3.15 | Node-level collect/transfer rules are rejected: the collect/transfer split is per good… | MODEL | 1973 |
| Y779 | §3.15 | Treating unsteered goods as fully collected is rejected: transfer power does not come… | MODEL | 1975 |
| Y780 | §3.15 | Undirected shortest path as the primary fleet route is rejected: a geodesic over a… | MODEL | 1977 |
| Y781 | §3.15 | Automatic per-good merchant targeting is rejected: one vanilla arrow click already… | DESIGN | 1979 |
| Y782 | §3.15 | Companion-overlay merchant assignment is rejected: assignment must stay a game action… | DESIGN | 1981 |
| Y783 | §3.15 | Emission-time pruning of near-flat links is rejected: peripheral termini are intended… | DESIGN | 1983 |
| Y784 | §3.15 | Edge conductance / weighted Laplacian stays rejected: v1 rejected it as "too much… | PROCESS | 1988 |
| Y785 | §3.15 | Staged delivery is rejected: the intermediate states are different designs sharing a… | DESIGN | 1993 |
| Y786 | §3.15 | "The aggregate map is not a DAG" is still an error, with v1's reason corrected: v1… | MEASURED | 1995 |
| Y787 | §3.15 | The aggregate is a DAG because `Φ_w` is a DRAIN orientation, acyclic by the… | MODEL | 1997 |
| Y788 | §3.16 | v1 carried an evidence standard — "every retraction traced to a premise that entered… | PROCESS | 2003 |
| Y789 | §3.16 | At least fifteen non-prose claims failed, by three distinct mechanisms. | PROCESS | 2005 |
| Y790 | §3.16 | Mechanism 1, file values remembered from an older patch: the 75% overseas autonomy… | ENGINE | 2008 |
| Y791 | §3.16 | Mechanism 2, file values transformed and then reported as raw: v1's grain (1.25) and… | ENGINE | 2010 |
| Y792 | §3.16 | Mechanism 3, the spec's own algebra instantiated without checking the instantiation: ε… | PROCESS | 2013 |
| Y206 | §3.16 | Implemented as written, v1's ε left the α = 1 identity's residual at 1e-5 against v1's… | MEASURED | 2015 |
| Y793 | §3.16 | One of only three claims carrying `verified (method unstated)` provenance — Propagate… | PROCESS | 2018 |
| Y794 | §3.16 | The real signal in the audit was provenance: nine of the sixteen refuted ENGINE claims… | PROCESS | 2019 |
| Y795 | §3.16 | The rule is not "trust derivations" and not "distrust prose" but that anything which… | DESIGN | 2023 |
| Y796 | §3.16 | Every engine fact in this spec must carry its source — a file path, a binary string, or… | PROCESS | 2024 |
| Y797 | §3.16 | The gap that mattered more than any refutation: v1 never stated what determines sink… | PROCESS | 2027 |
| Y798 | §3.16 | The audit found that flaw only by running the solver and asking why the output looked… | PROCESS | 2030 |
| Y799 | §3.16 | The standing repair is in this document's structure: what determines sink placement,… | PROCESS | 2030 |
| Y800 | §3.16 | Each of those properties is provable or measured-and-labelled and each is checked at… | DESIGN | 2034 |
| Y801 | §3.16 | The next audit's first question should be which property of the output this spec still… | PROCESS | 2038 |
| Y802 | §3.16 | The cautionary case is now closed and it closed the other way: the propagation source… | MODEL | 2041 |
| Y803 | §3.16 | Probe 15 settled it: the qualifier is descriptively false, since a country with no… | ENGINE | 2044 |
| Y804 | §3.16 | The lesson is not the one the case was filed under: it was filed as "agreement between… | MODEL | 2049 |
| Y805 | §3.16 | A localisation string describes intent, not behaviour. | ENGINE | 2052 |
| Y806 | §3.16 | Sources are necessary but not sufficient, and an engine fact sourced to a string is… | DESIGN | 2052 |
| Y807 | §3.16 | During the declaration-order test a permuted node file differed from vanilla on 61 of… | ENGINE | 2056 |
| Y808 | §3.16 | That measurement was meaningless, because two runs of the same vanilla build differ on… | ENGINE | 2058 |
| Y809 | §3.16 | A measurement without a null comparison is not evidence. | DESIGN | 2061 |
| Y810 | §3.16 | Every measured claim in this document that could vary run to run should carry the… | PROCESS | 2062 |

---

## Measured claims with no named instrument

**The list is not empty.** I typed **162** rows `MEASURED` — 141 carried census rows (after re-typing
into the brief's vocabulary, and excluding the 15 this edit removed) and 21 of the 80 NEW rows. Of
those 162, **88 name no script in `scripts/`**, either at their own line or by an explicit
cross-reference to a line that does. They are listed below.

Six rows that would otherwise appear here are **excluded** because a lead-in sentence attributes the
block they sit in: `Y252`, `Y025`, `Y254`, `Y259` (§1.1's property bullets, covered by L174
"regenerated for v6.0 by `measure6.py`" and by the L212–216 note naming `props6.py`); `Y603`, `Y604`
(§3.2's T2 and T3, covered by L1459 "all run through a faithful implementation of §1.1 (`toys.py`)").
One row is excluded by explicit cross-reference: `Y570` (§2.8's latent-good row cites §1.5, whose
L486 names `measure6.py` for the same figure).

Two rows in the list name a *file* but not a script: `Y739` cites `drain-orientation.md` §5–6 and
`changes-v5.md` §39–41; `Y1110` names `flowop.LP_OPTS` (the option object in `flowop.py`) but not the
script that ran the sweep it reports.

| ID | § | claim | line |
|---|---|---|---|
| Y005 | §0 | On the 1444 start the deleted apparatus was worth 105.30 ducats — 0.98% of the 10,712.70 the field totalled with it, 0.99% of the 10,607.40… | 20 |
| Y008 | §0 | Phase 2's min-cost flow is degenerate under unit arc costs, so presentation order selected which optimum was returned. | 27 |
| Y1001 | §0 | The margin by which the tie-break makes the optimum unique is as small as 3.8e-8 while HiGHS's default tolerance is 1e-7, so the solver… | 31 |
| Y967 | §0 | With all three changes in place the orientation is unchanged across every relabelling tried — 0 of 180 on the aggregate and 0 of 290 per… | 32 |
| Y1002 | §0 | The orientation is also unchanged under permutation of the LP's column order. | 35 |
| Y226 | §1.1 | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | 115 |
| Y022 | §1.1 | Nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes unequal node sums. | 160 |
| Y276 | §1.2 | One node has `b = 0` exactly at 1444 — `cape_of_good_hope` — and it is handled as an ordinary conduit. | 248 |
| Y1083 | §1.3 | On the 1444 start only `devastation` is live. | 354 |
| Y070 | §1.3 | The model reads the good the engine actually rolled rather than predicting the draw, and pricing those provinces at zero instead… | 411 |
| Y079 | §1.6 | At α_Φ = 2.0 the 1444 field gives two sinks, and scaling European development alone takes the count through two, three, four and five… | 521 |
| Y085 | §1.6 | Measured on that LP directly, 40 of 40 permutations return a different optimal support at an objective identical to within a few units in… | 538 |
| Y093 | §1.6 | Over the 180 relabellings the sink set, every edge direction, and the promotion and fallback counts were identical, so for `Φ_w` the… | 556 |
| Y1007 | §1.6 | §2.3's second-order term took per-good relabelling sensitivity from 84 of 290 runs to 13, and the goods admitting an alternative optimum… | 563 |
| Y1008 | §1.6 | Pinning the solver's optimality tolerance took the remaining per-good relabelling sensitivity to 0 of 290. | 565 |
| Y1009 | §1.6 | On this field the per-good graphs are order-invariant over the orderings tried, as `Φ_w` is. | 566 |
| Y097 | §1.6 | Per good on the same field: 2–8 sinks, mean 3.69, 29/29 acyclic, 0 fallbacks fired, and 90.6% of ordered node pairs (5,723 of 6,320)… | 583 |
| Y098 | §1.6 | Agreement with the per-good graphs is 55.1% of edge-goods and 54.8% value-weighted. | 586 |
| Y107 | §1.6 | At 1444 the map ends in Genoa and in Hangzhou, and as European development compounds Europe gains ends and Asia loses its one. | 612 |
| Y111 | §1.6 | The path is not monotone — `hangzhou` leaves, returns and leaves again; `gulf_of_siam` holds an end over one stretch and nowhere else;… | 623 |
| Y112 | §1.6 | Because §1.3's wealth is linear in development, scaling development and scaling wealth are the same operation here — maximum difference 0.0… | 640 |
| Y344 | §1.6 | The 1444 map draws a recognisable pre-Columbian trade geography. | 652 |
| Y345 | §1.6 | From the north the route to the Asian end is the Volga and the steppe: `white_sea → novgorod → kazan → siberia → samarkand → lahore → lhasa… | 653 |
| Y113 | §1.6 | From Iberia the route is the African coast and the Red Sea: `sevilla → safi → timbuktu → katsina → ethiopia → gulf_of_aden → comorin_cape →… | 655 |
| Y114 | §1.6 | No route leaves `genua` at all — it is a sink, out-degree 0 against in-degree 5, so the western Mediterranean, the Adriatic and the Rhône… | 657 |
| Y994 | §1.6 | `english_channel` is not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches the Asian end not at all. | 658 |
| Y115 | §1.6 | No Europe→sink route passes the Cape of Good Hope, checked exhaustively rather than sampled: of the 23 European nodes there are 27… | 662 |
| Y119 | §1.6 | Scaling the 18 western and central European nodes makes `genua` the sole sink from ×1.52, staying sole to ×3.60; scaling all 22 gives no… | 675 |
| Y1093 | §1.6 | At every multiple above ×2.50 on the 22-node scaling both surviving ends are western. | 680 |
| Y120 | §1.6 | The Cape reverses under the same growth — 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` drainage becomes… | 681 |
| Y121 | §1.6 | Dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate boosts are expected behaviour… | 690 |
| Y126 | §1.10 | Measured on the 1444 start, the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, median 21.6%, over the flag's 26… | 827 |
| Y127 | §1.10 | As a share of the node's total after the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, median 17.7%; v5.0 quoted those… | 827 |
| Y128 | §1.10 | On §2.2's derived 25-node inland basis (dropping `siberia`) the median is 21.3%, or 17.5% after the grant. | 827 |
| Y406 | §1.10 | The largest single incumbent holder runs 23.6 to 143.2, so a country at the caravan cap outweighs the largest incumbent in 7 of the 26… | 827 |
| Y1013 | §2.1 | The margin by which the optimum is unique is 3.8e-8 worst per good and 7.5e-6 on the aggregate — 8 to 10 orders above double-precision unit… | 906 |
| Y1014 | §2.1 | Orientation under LP column permutation: 0 flips on the aggregate and on all 29 goods, with an objective spread of 1.1e-15. | 907 |
| Y130 | §2.2 | The only modifiers in scope are the four describing the province’s own condition, all four reaching `goods_produced`; at 1444 only… | 946 |
| Y131 | §2.2 | World wealth is 10,607.40 annual ducats over 2,472 counted provinces. | 952 |
| Y132 | §2.2 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): of order 0.1 s for all 29 goods, and… | 963 |
| Y133 | §2.2 | Repeated 12-run experiments on one machine do not reproduce each other closely enough to support anything finer — three replicates gave… | 965 |
| Y134 | §2.2 | v5.0's "0.17–0.21 s for all 29 goods" is not reproducible: across three replicates of twelve runs the number of runs landing inside that… | 968 |
| Y457 | §2.2a | Vanilla 1444 is one component. | 993 |
| Y464 | §2.2a | Sink-set equality is measured exact 29/29 on a 2-core map and fails where Phase 0 acts, because a pendant net-importer is a sink outside… | 1010 |
| Y466 | §2.2a | Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: a selected flow-terminal demander can lose… | 1014 |
| Y1028 | §2.3 | Measured on zero-reduced-cost arcs outside the support: the aggregate `b_w` goes from 40 under unit costs to 0 under the first-order term… | 1098 |
| Y1029 | §2.3 | Adding the second-order term takes the zero-reduced-cost arcs to 1 arc on 1 good. | 1100 |
| Y1031 | §2.3 | The margin by which the tie-break makes the optimum unique runs as low as 3.8e-8 on some per-good solves, so it sits inside the default… | 1116 |
| Y1032 | §2.3 | Measured: over six permutations of the LP's column order, `copper` and `paper` returned orientations differing on 12 and 8 edge-slots with… | 1118 |
| Y1035 | §2.3 | What the second-order term costs: self-coherence with the per-good graphs falls 0.1–0.2 points and nothing else measured moves — sinks per… | 1132 |
| Y1038 | §2.3 | Dividing by the world total moves the aggregate `Φ_w` by 7 of 159 edges, and across all candidate normalisations 13 of the 29 per-good… | 1148 |
| Y1110 | §2.3 | Without the pinned tolerance the normalisation sweep undercounts, returning a strict subset of the goods that actually move. | 1157 |
| Y143 | §2.4 | The tie-break cost is built from good-independent node wealth so it applies to every per-good solve, but it need not break ties in a… | 1212 |
| Y148 | §2.4 | §1.1's priority key ties in more places than §1.1 documents — besides the free-edge sweep it decides Phase 1's within-cluster argmin, the… | 1231 |
| Y149 | §2.4 | The end-flag list is a function of the world rather than of the node order: across the 180 relabellings of item 1 the end set came back as… | 1239 |
| Y150 | §2.4 | 1444 has two end nodes, `genua` and `hangzhou`, against vanilla's three. | 1242 |
| Y1043 | §2.8 | v6.0 listed Australia, Venice and Deccan among the spice and cloves termini; none of the three holds either sink on this field. | 1333 |
| Y537 | §2.8 | Spice and cloves at 1444: source in Indonesia and both source there alone — `spices` from `the_moluccas` and `kongo`, `cloves` from… | 1333 |
| Y538 | §2.8 | No Chinese node holds a `spices` sink in either configuration: under the §3.13 α-calibration `spices` sinks at `doab` and `genua`, and… | 1333 |
| Y566 | §2.8 | Sink-set equality is monitored rather than asserted: it is measured exact on 1444 (29/29 goods, zero fallbacks) but is not a theorem, and… | 1356 |
| Y572 | §2.8 | `Φ_w`-vs-realized sign disagreement is measured rather than asserted, weighted by trade value rather than link count, against a known… | 1365 |
| Y591 | §3.2 | Monotonicity killed v1's rank-orientation strawman and the tested `s − c` operator the same way: demand had to increase at every hop, so… | 1410 |
| Y593 | §3.2 | v1's Laplacian sink rule is exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour φ)`, verified on every (good, node) pair. | 1416 |
| Y594 | §3.2 | Because supply is sparse where demand is dense, that right-hand side is set by supply geography: spices are produced in 18 of 80 nodes and… | 1418 |
| Y595 | §3.2 | Under v1's Laplacian, sinks landed where the field was locally flat rather than where demand was: the highest-demand node in the game was… | 1422 |
| Y158 | §3.2 | On the contrast metric itself the demand side is the wider one, not the supply side. | 1431 |
| Y159 | §3.2 | Better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of placement. | 1433 |
| Y160 | §3.2 | Moving the spice sink to a Chinese node takes a multiple of that node's wealth in the region of 3.6–4.8×, observed on the 1444 field:… | 1434 |
| Y162 | §3.2 | The four named Chinese nodes are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the range — so the claim is about… | 1437 |
| Y610 | §3.2 | Free-edge direction is marking order under the (DEF asc, b asc, index) priority, deterministic by construction, while independence from the… | 1484 |
| Y611 | §3.2 | Reachability: the orientation contains the LP certificate, so every unit of demand is servable — measured 100.0%, 29/29 goods, zero orphan… | 1496 |
| Y166 | §3.4 | In v1 substituting production income also measurably broke the α = 1 identity, with orientation agreement collapsing to well under half the… | 1550 |
| Y648 | §3.6 | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based tie-breaking turned an acyclic prior into A → B → C → A. | 1609 |
| Y654 | §3.6 | Nothing needs to stop churn: a link whose flow-support membership alternates month to month carries near-nothing either way on the evidence… | 1620 |
| Y656 | §3.6 | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, zero support-membership changes moved more than 1e-6 of flow, and under… | 1624 |
| Y660 | §3.6 | The measured count of exact key ties on 1444 data is zero, and the LP itself is deterministic (six identical solves, one orientation). | 1647 |
| Y681 | §3.8 | Any-good connectivity on 1444 data under DRAIN is 90.6% (5,723 of 6,320) of ordered node pairs, and v2's 98.8% is v1's Laplacian figure,… | 1680 |
| Y688 | §3.9 | The value-weighted net flow (the sum over goods of `V_g · net_g`) is a flow, flows circulate, and it measurably contains directed cycles,… | 1709 |
| Y186 | §3.10 | `gulf_of_siam`'s 29 goods leave it by seven distinct downstream sets. | 1744 |
| Y713 | §3.11 | Nineteen countries are at the caravan cap from raw 1444 development alone, and Burgundy, Korea, the Timurids and Portugal start 2–10% short… | 1766 |
| Y739 | §3.13 | A measured calibration exists that makes sink counts track price more closely than the baseline does (α unclamped at exponent 2, ρ = 0.5,… | 1848 |
| Y197 | §3.13 | Under the calibration’s α = 16 the cloves sink lands on a high-demand node rather than a geographic accident. | 1857 |
| Y741 | §3.13 | The twig tolerance re-routes arcs carrying a small fraction of a good’s mass, and it costs one good full reach. | 1858 |
| Y198 | §3.13 | v2 said Beijing "holds the richest single province", which it does not — that is `hangzhou` — and no province-wealth figures are quoted. | 1861 |
| Y762 | §3.15 | Pure min-cost-flow orientation with no sweep is rejected: it orients only the roughly 79-edge support (a spanning-tree basis), leaving half… | 1905 |
| Y764 | §3.15 | DEF-descending free-edge priority is rejected as measurably worse: on the certificate, unmet demand is identically zero so DEF is total… | 1924 |
| Y786 | §3.15 | "The aggregate map is not a DAG" is still an error, with v1's reason corrected: v1 defended it by claiming net flow is the gradient of `Φ`,… | 1995 |
| Y206 | §3.16 | Implemented as written, v1's ε left the α = 1 identity's residual at 1e-5 against v1's ε of 1e-6, and would have been diagnosed as a solver… | 2015 |

---

## Internal inconsistencies

**Eight found.** Each entry gives the two passages and their line numbers, and stops.

**1 — a count that disagrees with the list it describes (§1.6).**
- L696–697: "of the 19 aggregate-graph facts this section states, **6 move**."
- L699–702, the enumeration of what moves: "the source set (5 sources against 10), its `c_w` rank
  range and mean degree, the Cape's ordered-pair count (81 against 42) — and **the Iberian long route
  ceases to exist**: under the descending key `sevilla` reaches no Asian end at all, and no path runs
  from it to `ganges_delta`." That names five items: source set, `c_w` rank range, mean degree,
  ordered-pair count, Iberian route.
- The complementary list at L697–699 names six or seven items depending on whether "the promotion and
  fallback counts" is read as one or two; neither list, nor the two together, totals 19.

**2 — two passages asserting different things about the same quantity (§2.9 vs §2.3 and §1.3).**
- L1377: "the **defines parser first**: §2.3 makes every constant in the model a runtime read".
- L1045–1047: "**`TAX_COEFF` is not in any file that has been found** — `defines.lua`,
  `common/defines/` and the static-modifier tables were searched — so it remains a measured constant".
- L296–298 says the same: "`TAX_COEFF` is in no file that has been found … so it stays a measured
  constant carrying the observation that produced it."

**3 — a cross-reference pointing at a section that does not contain what is claimed (§2.3 → §1.2).**
- L1154–1156: "on this field min-max and `w/max` are too, because the minimum node wealth is exactly
  zero — `cape_of_good_hope` holds no counted province wealth (§1.2)."
- L248–249, the whole of what §1.2 says about that node: "a node with `b = 0` exactly (one exists at
  1444: `cape_of_good_hope`) is handled as an ordinary conduit." §1.2 states a balance, not a wealth.
  (§3.2 L1503 does state `s = c = 0` for the Cape; §1.2, the section cited, does not.)

**4 — a cross-reference pointing at a section that does not contain what is claimed (§3.13 → §3.9).**
- L1852–1853: "*No span, correlation or reach figure is quoted for it*, on the same ground §3.9 gives
  for the superseded aggregate: it is not adopted, its numbers move with every change to the wealth
  field …"
- L1711–1713, all §3.9 now says about that aggregate: "An aggregate built from the per-good **marking
  orders** is acyclic for free, but its ends are a function of the order Phase 3 pops its ready queue
  … That follows from the definition and needs no measurement." The "numbers move with every change to
  the wealth field" ground is stated in §3.15 (L1957–1959, for the gravity kernels), not in §3.9.

**5 — a self-description contradicted inside its own section (§1.6).**
- L664–665: "That is what a 1444 map should say, and it is the one place in this section where a
  universal is asserted, because here the whole set was enumerated."
- L556, in the same section: "Nothing this section quotes about the **installed** graph."
- L577, in the same section: "Every node drains to a sink; acyclic, 159/159 oriented".

**6 — mixed denominators for the same node set in one sentence (§2.8).**
- L1350: "two identical vanilla 1444 Castile starts differ on **49 of 80** nodes by up to 8.96% …
  `retention` is identical on **80 of 80** nodes and `total` on **78 of 79**".
- The same measurement's restatement at L2059–2060 uses 80 throughout: "two runs of *the same vanilla
  build* differ on 49 of 80 nodes by up to 8.96%".

**7 — a count that disagrees with the list it describes (§2.9 vs §2.7).**
- L1383: "**Memory track** — the §2.7 probe session, **all ten items** on one trace."
- §2.7 carries items **1–11** (L1303–1313) and item **16** (L1315–1325) as unsettled — twelve — with
  items 12–15 recorded as done (L1282–1298) and item 12 dropped.

**8 — a bound and the measurements offered for it (§2.2).**
- L963–965: "Measured on the reference implementation … **of order 0.1 s for all 29 goods, and
  single-digit milliseconds per good on average.** That is the whole of the claim."
- L965–968: "three replicates gave per-good averages spanning 3.5–10.5, 3.5–10.8 and 3.1–4.7 ms".
