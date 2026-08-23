# Claims Delta — Per-Good Trade Network Spec, round 10 (v6.4 round-10 frozen → v6.5 current)

**Current document:** `per-good-trade-spec.md`, 2,270 lines, MD5 `f9a70dfd859e1c97b266c35de4a1b228`.

**Prior inventory:** `claims-delta-round9.md` — the claim census taken of this document at 2,190
lines, MD5 `0989f4dc54d31514123eed24f0aae5c5`. Its rows are the UNCHANGED (1035), REWORDED (1),
CHANGED (18) and NEW (23) tables — **1,077 live rows**, every one of them carried here. A row
entering the compressed UNCHANGED table below from one of round 9’s wider tables keeps that
table’s full wording rather than being re-truncated.

**Prior state compared against:** `per-good-trade-spec-v6.4-round10-frozen.md` (2,190 lines, MD5
`0989f4dc54d31514123eed24f0aae5c5`), byte-exact and unedited.

**Change record:** `round10.diff`, 438 lines, **31 hunks**. Verified before use: `patch` applied to
the frozen file reproduces `per-good-trade-spec.md` at MD5 `f9a70dfd859e1c97b266c35de4a1b228`,
byte-for-byte. An old→new line map built from the hunks was then checked line-by-line against both
files: **0 mismatches** across all 2,129 mapped old lines. 61 old lines are deleted or modified;
141 new lines are added. Every classification below is against the actual old text and the actual
new text, not against the prior census’s paraphrases.

**ID range found:** `Y001`–`Y1259`, **1,077 distinct IDs**, each used exactly once. 182 numbers in
that span are unused — the already-retired IDs of earlier rounds plus the numbers those rounds
skipped — and they stay unused. Highest number actually used: **1259**.

**First new ID assigned:** `Y1260` (new propositions run `Y1260`–`Y1354`, in document order).

**Counts:**

| status | rows |
|---|---|
| UNCHANGED | 1046 |
| REWORDED | 3 |
| CHANGED | 28 |
| REMOVED | 0 |
| NEW | 95 |
| **total rows** | **1172** |

**Notes.** (1) 1,077 live rows in, 1,077 carried out (1046 + 3 + 28 + 0). No live row was dropped
and no number was reused. (2) Nothing was removed outright this round: every deletion in the diff
is a replacement inside a carried row, so the REMOVED table is empty. The two deletions with no
direct replacement — §1.12’s "Arrow weight from realized value crossing the link" and §1.1’s "27
added lines" — are clauses inside `Y421` and `Y1195`, whose remaining words still stand, so both
are carried as CHANGED with the withdrawal recorded rather than retired. (3) The unit of
classification is the claim’s own supporting words, not the physical line: a row whose own words
survive byte-identical is UNCHANGED even when the sentence around them was edited or the paragraph
was re-wrapped, and the edit is then carried as its own CHANGED or NEW row (`Y1159`/`Y1286`,
`Y483`/`Y1315`–`Y1318`, `Y514`/`Y1323`–`Y1325`, `Y576`/`Y1328`–`Y1333`, `Y634`/`Y1338`–`Y1340`,
`Y750`/`Y1347`–`Y1350`, `Y449`/`Y1311` all split this way). (4) `Line` is the line in the current
document where the claim or its anchor sentence now sits; for a CHANGED row it is the line the
changed text now occupies. (5) Types are this delta’s five-way vocabulary (ENGINE / MODEL /
MEASURED / DESIGN / PROCESS), carried from the prior census for carried rows. (6) Three changes of
this round live outside the document and so outside this census: `scripts/measure6.py`’s agreement
weight is now built from inject-based weights read from the save (`_inject_weights`, the node
`trade_goods_size` arrays) rather than from `price × goods_produced`, its orientation-side shares
unchanged; `scripts/solver.py`’s `prod_income` line gained a comment naming the field a misnomer
("`goods_produced * price` is the trade_value"); and `scripts/verify6.py`’s self-coherence phrase
template was updated to the spec’s new wording. No census row was ever taken of any of the three.
(7) The version stamp on L3 moved 6.4 → 6.5; the census has never carried a row for it.

## CHANGED — still asserted, but what it asserts moved

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y1144 | §0 | v4.0’s tree ships three sweep scripts, `audit_modifiers.py` among them, and all three sweep both modifier directories. | CHANGED | old: "**the one shipped sweep script is v4.0's `audit_modifiers.py`**" → new: "**the shipped sweep scripts are v4.0's — three sweep both modifier directories, `audit_modifiers.py` among them**"; one script becomes three, and the sweep is characterised as covering both modifier directories. The v4.0 attribution is unchanged | PROCESS | `audit_modifiers.py`; §2.3 | 21 |
| Y1195 | §1.1 | `val5_pergood.py` is still on disk, and `diff` shows `props6.py` is that file verbatim — zero deletions — plus an added block carrying the permutation loop. | CHANGED | old: "plus **27 added lines** carrying the permutation loop" → new: "plus **an added block** carrying the permutation loop"; the line count is withdrawn and the addition left unquantified. The still-on-disk, verbatim and zero-deletions halves are unchanged | PROCESS | `diff` of `props6.py` against `val5_pergood.py` | 248 |
| Y323 | §1.6 | `V_g = Σ_n inject_g(n)` — the per-good value weights used for display, link values and AI are the world sum of §1.8’s engine-injected value. | CHANGED | old: "`V_g     = price(g) · Σ_m goods_produced(m,g)`" → new: "`V_g     = Σ_n inject_g(n)`", annotated "§1.8's engine-injected value"; the weight is redefined from price times world goods-produced to the node sum of the engine's own injected value. The display / link-values / AI consumer list is unchanged | MODEL | stipulated | 557 |
| Y098 | §1.6 | Agreement with the per-good graphs is 55.1% of edge-goods and 54.9% weighted by §1.8’s `inject`. | CHANGED | old: "**54.8%** value-weighted" → new: "**54.9%** weighted by **§1.8's `inject`**"; the figure moves by a tenth of a point and the weighting basis moves from the old `V_g` to the engine-injected value. The 55.1% unweighted figure is unchanged | MEASURED | numerical test (`measure6.py`) | 638 |
| Y1099 | §1.6 | The direction survives the bisection-versus-grid difference; the widest interval does not — the bisection’s ×1.38–×1.95 and the grid’s ×1.973–×2.456 do not overlap — so only the grid’s figures are maintained. | CHANGED | old: "**the direction and the widest interval survive** that difference; the row boundaries did not, and quoting them invited exactly the trajectory reading the paragraph above warns against" → new: "the direction survives that difference; **the widest interval did not**", with the two non-overlapping intervals quoted and the conclusion that "bisection rows were sampling artifacts, and only the grid's figures are maintained"; the widest interval moves from surviving the difference to not surviving it, and the quoting-invited-a-trajectory-reading clause is dropped | PROCESS | `p3_bisect.py`; `round6.py` | 690 |
| Y384 | §1.9 | Ship trade power propagates only under a ship-propagation modifier — the only-under conditional being the model’s unprobed reading of the modifier’s own semantics — at a compounded rate the model reads as the propagation share multiplied by that modifier. | CHANGED | old: propagates "**only where the country has a ship-propagation modifier**", asserted flat, with only the composition marked as the model's reading → new: the only-under conditional is itself "**the model's reading of the modifier's own semantics, unprobed**", and "**both halves** are the model's derived reading rather than engine fact"; one derived reading becomes two, and the flat half of the claim is withdrawn | ENGINE | stipulated | 861 |
| Y1245 | §1.9 | The ship-propagation modifier and its grants are file-stated: `ship_power_propagation` in the static modifiers, ideas, reforms and an age ability. | CHANGED | old: "the modifier and **the share** are each file-stated" → new: "the modifier and **its grants** are file-stated (`ship_power_propagation` in the static modifiers, ideas, reforms and an age ability)"; the propagation share leaves the clause, the modifier's grant sites enter it, and the modifier key is named | ENGINE | read from a file (the shipped files) | 861 |
| Y421 | §1.12 | The aggregate trade view colours provinces by node and draws arrows between nodes rendering `Φ_w`. | CHANGED | old: "**Trade map mode.** Provinces coloured by node, arrows between nodes, drawing `Φ_w`. **Arrow weight from realized value crossing the link.**" → new: "**Aggregate trade view.** Provinces coloured by node, arrows between nodes, drawing `Φ_w`"; the view is renamed and the arrow-weight sentence is withdrawn with nothing replacing it — what the section now says of `Φ_w` is that it "remains the drawn installed direction". The colouring and the `Φ_w` arrow layer are unchanged | MODEL | stipulated | 948 |
| Y422 | §1.12 | Clicking a province switches province colouring to the vanilla trade-goods rendering for that good and redirects the arrow layer to that good’s graph; a sink is visible as a node with no outgoing arrows for the good; clicking the node icon clears back to the aggregate view. | CHANGED | old: "a sink is visible as a node with **no outgoing arrows**" and "clicking the node icon **clears back to `Φ_w`**" → new: "no outgoing arrows **for the good**" and "clears back to **the aggregate view**"; the sink test is scoped to the selected good and the clear target is named as the view rather than the operator. The province-colouring and arrow-layer halves are unchanged | MODEL | stipulated | 958 |
| Y424 | §1.12 | A link’s two-way traffic is shown as two directed figures per physical link, never one net scalar. | CHANGED | old: "A link's two-way traffic. **One scalar per link, shown as net**", listed under "**Not representable in the vanilla UI**" → new: "**Every incident link is shown, with the value flowing in each direction along it**: two directed figures per physical link, **never one net scalar**"; the not-representable verdict is reversed. The engine's single stored per-link field survives, at §2.6 (`Y514`, `Y1323`) | ENGINE | stipulated | 952 |
| Y423 | §1.12 | Value broken down by commodity is delivered in the main UI by swap-on-view — only the selected good’s numbers displayed at a time — so no thirty-field storage in engine structures is needed. | CHANGED | old: "Value broken down by commodity" is "**not representable in the vanilla UI**" and shown in the companion overlay instead: "the node window carries several node-level value fields (incoming / local / total / outgoing), but none takes a commodity argument — **zero per-good fields, where thirty would be needed**" → new: per-good value display "**move[s] into the main UI by swap-on-view**", the node window's fields are enumerated as **six** named `tradeinterface.gui` fields, and "**no thirty-field storage in engine structures is needed**"; the not-representable verdict is reversed, the overlay is no longer where this is shown, and the field count moves from four to six | ENGINE | read from a file (the node window's fields) | 978 |
| Y426 | §1.12 | There is no new art, sprites, shaders or map-mode chrome; the UI changes are three, all on existing widgets — incoming-entry assignability (§1.7), the directional value panels, and per-good repopulation of the node and link fields. | CHANGED | old: "Making the node window's existing incoming-link entries assignable (§1.7) is **the only UI change**" → new: "**The UI changes are three**, all on existing widgets: incoming-entry assignability (§1.7), the directional value panels, and per-good repopulation of the node and link fields"; one UI change becomes three. The no-new-art half is unchanged | DESIGN | stipulated | 983 |
| Y438 | §2.2 | Solver item 2 is a parser for non-ironman saves reading province owner, `base_tax`, `base_production`, trade good, development, and the per-node `trade_goods_size` arrays. | CHANGED | old: "trade good, **goods produced**, development" → new: "trade good, development, **and the per-node `trade_goods_size` arrays**"; the per-province goods-produced read is replaced by a node-level array read | DESIGN | stipulated | 1061 |
| Y447 | §2.2 | Cost per good is one uncapacitated min-cost flow on 80 nodes and 318 arcs plus an O((V+E) log V) priority sweep. | CHANGED | old: "plus an **O(V+E)** sweep" → new: "plus an **O((V+E) log V) priority** sweep"; the sweep's complexity gains a log factor and is named a priority sweep. The min-cost-flow half and the 80-nodes / 318-arcs figures are unchanged | MODEL | algebraic derivation | 1082 |
| Y1203 | §2.2 | The reference implementation builds its province table from `history/provinces`, reading the save for the twenty rolled trade goods and the node `trade_goods_size` arrays. | CHANGED | old: "reading the save **only** for the twenty rolled trade goods" → new: "reading the save for the twenty rolled trade goods **and the node `trade_goods_size` arrays**"; the exclusivity is dropped and a second save read is added | PROCESS | the reference implementation | 1101 |
| Y137 | §2.3 | v3.0 through v5.0 said neither wealth coefficient was in a file; v4.0’s tree ships three scripts that sweep both modifier directories, and `audit_modifiers.py` walked past the block holding one of them, while v3.0 and v5.0 repeated the claim without shipping a sweep. | CHANGED | old: "v4.0's tree ships **the one sweep script, `audit_modifiers.py`**, which walked past the block holding one of them" → new: "v4.0's tree ships **three scripts that sweep both modifier directories — `audit_modifiers.py`, `audit_alpha.py`, `audit_bands.py`; others read the same files without sweeping them** — and `audit_modifiers.py` walked past the block holding one of them"; one sweep script becomes three. The walked-past-the-block and the v3.0/v5.0 halves are unchanged | PROCESS | the prior spec versions; `audit_modifiers.py` | 1173 |
| Y1115 | §2.3 | `\|w[u] − w[v]\|` telescopes on monotone stretches, collapsing there to the endpoint difference, so routings traversing similar wealth profiles can still total the same and the term cancels where ties need breaking; `frac(lo·hi·7919)` has no such structure, and that is the whole of its job. | CHANGED | old: "**telescopes**: summed along a path it collapses to **a function of the endpoints**, so **two routings between the same endpoints** can still total the same and the term cancels **exactly** where a tie needs breaking" → new: "**telescopes on monotone stretches** — there it collapses to the endpoint difference — so **routings traversing similar wealth profiles** can still total the same and the term cancels where ties need breaking"; the telescoping is scoped to monotone stretches, the equal-total case widens from same-endpoint routings to similar wealth profiles, and "exactly" is dropped. The `frac(lo·hi·7919)` half is unchanged | MODEL | derivation | 1238 |
| Y486 | §2.4 | Measured: a file with all 159 links declared backwards logged exactly 159 such errors and then loaded and played normally — `retention` unchanged on 80 of 80 nodes and `total` on 78 of 79 — with the power-dependent fields differing only within the engine’s own run-to-run variance. | CHANGED | old: "with node **`total` and `retention` unchanged** and the power-dependent fields differing only within the engine's own run-to-run variance" → new: "**`retention` unchanged on 80 of 80 nodes and `total` on 78 of 79**, the exception (`zambezi`) drifting 0.012%, within the engine's own run-to-run variance (§2.8) — with the power-dependent fields differing only within that variance"; a flat unchanged becomes two counts with one named exception. The 159-errors-and-played-normally half is unchanged | ENGINE | engine test | 1319 |
| Y572 | §2.8 | `Φ_w`-vs-realized sign disagreement is measured rather than asserted, weighted by trade value rather than link count, against a known static baseline — `Φ_w` agrees with the per-good graphs on 54.9% of edge-goods weighted by §1.8’s `inject` and 55.1% unweighted — and is predicted to cluster at nodes with 3+ outgoing links and partial merchant coverage, thinning as coverage densifies. | CHANGED | old: "**54.8%** of edge-goods *weighted by trade value*" → new: "**54.9%** of edge-goods **weighted by §1.8's `inject`**"; §2.8's restatement of the baseline follows §1.6's (`Y098`). The 55.1% unweighted figure, the clustering prediction and the weighted-not-counted rule are unchanged | MEASURED | numerical test (§1.6) | 1536 |
| Y1218 | §2.9 | The full save parser (§2.2 item 2) comes next in the solver track, the reference reading the save for the twenty rolled trade goods and the node `trade_goods_size` arrays. | CHANGED | old: "the reference reads the save **only** for the twenty rolled trade goods" → new: "the reference reads the save for the twenty rolled trade goods **and the node `trade_goods_size` arrays**"; the same edit as `Y1203`, at §2.9's restatement | DESIGN | §2.2 item 2 | 1548 |
| Y580 | §2.9 | The memory track is the §2.7 probe session, the fifteen items still open there (1–11 and 16–19) on one trace. | CHANGED | old: "the **fourteen** items still open there (**1–11 and 16–18**)" → new: "the **fifteen** items still open there (**1–11 and 16–19**)" — probe 19 added. The one-trace half is unchanged | DESIGN | §2.7 | 1554 |
| Y581 | §2.9 | Then: write §1.10’s classified call-site list into the spec and gate income balance on both metrics. | CHANGED | old: the list's third item was "**decide the negative-link display policy against a measured number**" → new: the item leaves the list — "**The negative-link display policy is decided by design (§1.12: both directions shown as positive flows, no net scalar displayed); §2.8's disagreement measurement is still collected**"; a deferred decision becomes a settled one and the list drops from three items to two | DESIGN | stipulated | 1556 |
| Y591 | §3.2 | Monotonicity killed v1’s rank-orientation strawman and the tested `s − c` operator: demand had to increase at every hop, so 16.7% of world demand (unweighted per-good mean; 7.6% weighted by the orientation model’s per-good trade value) became unreachable and Genoa was crowned a cloves sink cloves could not reach. | CHANGED | old: "**17.1%** of world demand (unweighted per-good mean; **7.7%** value-weighted)" → new: "**16.7%** of world demand (unweighted per-good mean; **7.6%** weighted by the orientation model's per-good trade value, `price(g)·Σ_m goods_produced(m,g)` — `solver.build_sc`'s base)"; both figures move and the weighting base is named and pinned. The monotonicity argument and the Genoa case are unchanged | MEASURED | numerical test (`scripts/r9/lead/L_rank2.py`) | 1582 |
| Y637 | §3.4 | `V_g` and the routed value are trade value rather than production income, because a province’s trade value is unaffected by production efficiency or local autonomy while production income is defined by them; substituting production income would make `V_g` and the routed economy depend on owners’ idea groups and autonomy. | CHANGED | old: "This is also why **the aggregate uses trade value** rather than production income … Substituting production income would make `V_g` — **and with it the aggregate's weighting** — depend on owners' idea groups and autonomy" → new: "This is also why **`V_g` and the routed value are trade value** rather than production income … would make **`V_g` and the routed economy** depend"; the subject moves from the aggregate to `V_g` and the routed economy, and the added parenthetical says the aggregate graph "reads neither quantity". The trade-value-versus-production-income contrast is unchanged | MODEL | algebraic derivation | 1724 |
| Y652 | §3.6 | The dumps show a stack overflow under 1002 recorded identical `eu4.exe` frames, consistent with same-module recursion though carrying no per-frame addresses to prove it. | CHANGED | old: "The dumps show **an unbounded same-module recursion** on the tested cycle" → new: "The dumps show **a stack overflow under 1002 recorded identical `eu4.exe` frames — consistent with same-module recursion, though they carry no per-frame addresses to prove it**"; the recursion moves from what the dumps show to what they are consistent with, and the frame count and identity enter the claim | ENGINE | the crash dumps | 1794 |
| Y683 | §3.9 | What vanilla’s authored arrows encode is authored intent about where trade centres, with three authored ends (`genua`, `venice`, `english_channel`). | CHANGED | old: "What vanilla's authored arrows encode is **empires pointing at the biggest cities and richest areas**, with three authored ends" → new: "**authored intent about where trade centres**: three authored ends …, **two of them in the top node-wealth ranks and `venice` at rank 21 of 80 (180.6) — the historical pick rather than the wealth pick**"; the biggest-cities-and-richest-areas reading is withdrawn and replaced by measured ranks. The three named authored ends are unchanged | ENGINE | read from a file; numerical test | 1865 |
| Y693 | §3.9 | That is why the disagreement rate is measured rather than assumed; display policy for negative link values is settled by design, and the disagreement rate stays a measured quantity. | CHANGED | old: "and why display policy for negative link values is **a decision deferred to data**" → new: "Display policy for negative link values is **settled by design** — §1.12 shows each link's two directions as positive flows, so no negative net is displayed — **and the disagreement rate stays a measured quantity**"; the deferral is withdrawn and the two questions are separated. The measured-rather-than-assumed half is unchanged | DESIGN | stipulated | 1912 |
| Y790 | §3.16 | Mechanism 1, file values remembered from an older patch: the 75% overseas autonomy floor is real but historical and v1 carried it as current, and 1.37’s regime floors are file-exposed — `COLONY_MIN_AUTONOMY = 50` in `defines.lua`, the rest in `common/static_modifiers/00_static_modifiers.txt`. | CHANGED | old: "the 75% overseas autonomy floor is **pre-Common-Sense**" → new: it "is **real but historical** — introduced at 1.8 and superseded by States & Territories at 1.16, the tree's own version archive settling both ends — **and v1 carried it as current**"; the patch attribution moves off Common Sense onto 1.8/1.16 and the failure is restated as carrying a superseded value rather than a removed one. The 1.37 file-exposed half is unchanged | ENGINE | read from a file (`defines.lua`; `common/static_modifiers/00_static_modifiers.txt`; the tree's patchnote archive) | 2203 |

## REWORDED — same proposition, different words

| ID | § | claim | status | rewording | type | provenance | line |
|---|---|---|---|---|---|---|---|
| Y1246 | §1.9 | The composition of the ship-propagation modifier and the propagation share is stated by no file, string or observation. | REWORDED | "**their** composition is stated by no file, string or observation" becomes "**the composition too** is stated by no file, string or observation" — the possessive becomes a definite article and "too" marks this as the second of the bullet's two derived readings. The proposition is otherwise word-for-word; what the rewritten bullet adds around it is carried on `Y1287` and `Y1288` | PROCESS | unsourced | 861 |
| Y425 | §1.12 | Per-country effective trade power where eligibility differs by good is shown in the companion overlay as a value-weighted aggregate. | REWORDED | the bullet under "**Not representable in the vanilla UI**, and shown in the companion overlay instead" — "Per-country effective trade power where eligibility differs by good. Shown as a value-weighted aggregate." — becomes the sentence "**Still overlay-only**: per-country effective trade power where eligibility differs by good, shown as a value-weighted aggregate"; the item and its value-weighted-aggregate treatment are word-for-word, and only the heading carrying them is rewritten. The two items that left that list are carried on `Y423` and `Y424` | ENGINE | stipulated | 977 |
| Y1035 | §2.3 | What the second-order term costs: self-coherence with the per-good graphs falls by at most a tenth of a point (0.04 edge-goods, 0.10 weighted), and nothing else measured moves — sinks per good stay 2–8 mean 3.69, all 29 stay acyclic, `Φ_w`’s sinks are unchanged, and the ±1% wealth-noise result stays 0 edges moved on six seeds. | REWORDED | "0.10 **value-weighted**" becomes "0.10 **weighted by the orientation model's per-good trade value**" — the same weighting base, named explicitly instead of by the label, because §1.6 has redefined what "value" weights. Both figures and every other clause are word-for-word. The pinning clause the rewrite adds is carried on `Y1314` | MEASURED | numerical test | 1271 |

## REMOVED — the document no longer makes this claim

*None this round. No row of the prior census lost its claim: every hunk that deletes text either
replaces it or deletes a clause inside a row whose remaining words still stand, and each such row
is carried on the same ID as CHANGED or REWORDED. The two clause-level withdrawals — §1.12's
arrow-weight sentence and §1.1's "27 added lines" — sit inside `Y421` and `Y1195`.*


## UNCHANGED — still asserted, in substance and in figure (compressed)

| ID | § | claim | type | line |
|---|---|---|---|---|
| Y207 | §0 | The target build is EU4 1.37.5 Inca. | DESIGN | 5 |
| Y208 | §0 | The design is extended-timeline compatible. | DESIGN | 5 |
| Y209 | §0 | The design targets connected maps only. | DESIGN | 5 |
| Y210 | §0 | This document supersedes v1.3, which lives in `../v1-laplacian/`. | PROCESS | 6 |
| Y211 | §0 | v1 oriented each good by a Laplacian potential. | MODEL | 6 |
| Y212 | §0 | v1's sink placement was shown to be topological rather than economic. | MODEL | 7 |
| Y213 | §0 | A four-operator bake-off replaced the orientation core with the DRAIN algorithm. | MODEL | 8 |
| Y214 | §0 | The claim-audit corrections from `../v1-laplacian/validation.md` settleable from files were folded in at v2 and carried since. | PROCESS | 9 |
| Y1143 | §0 | No exhaustive re-check of those corrections has been made. | PROCESS | 11 |
| Y1142 | §0 | The folded claim-audit corrections were spot-verified in the round-7 audit, whose record samples 6 of 60, with none missing. | MEASURED | 11 |
| Y1185 | §0 | The round-7 spot-verification’s sample is C407, C101, C037/C038 and C128/C130/C131/C132. | PROCESS | 11 |
| Y1237 | §0 | The round-7 audit’s record of that spot-verification is `scripts/r7/out/S01.md`, row Y214. | PROCESS | 11 |
| Y215 | §0 | "replaces the installed aggregate with `Φ_w`"; the old operator is no longer named | MODEL | 12 |
| Y001 | §0 | v6.0 makes owner-agnosticism true by construction rather than by a rule that has to be policed. | DESIGN | 14 |
| Y216 | §0 | This version keeps v3.0's owner-agnostic wealth. | DESIGN | 14 |
| Y002 | §0 | The substantive change of v6.0 is to §1.3: wealth is a function of the province's development, its trade good … | DESIGN | 15 |
| Y003 | §0 | The two-test modifier classifier and everything it governed — trade-good modifiers, great projects, permanent … | DESIGN | 16 |
| Y004 | §0 | The two-test classifier is v4.0’s; v3.0 used a structural rule about which block of a trade-good definition a modifier sits in; the whole-install sweep as documented apparatus is v5.0’s alone. | MODEL | 19 |
| Y005 | §0 | On the 1444 start the deleted apparatus was worth 105.30 ducats — 0.98% of the 10,712.70 the field totalled … | MEASURED | 22 |
| Y006 | §0 | That classification was wrong in both independent audits that examined it … | PROCESS | 23 |
| Y007 | §0 | Three start-state reads are corrected in the same pass: `on_startup` devastation, dated `add_base_*` … | DESIGN | 26 |
| Y008 | §0 | Phase 2's min-cost flow is degenerate under unit arc costs, so presentation order selected which optimum was … | MEASURED | 29 |
| Y965 | §0 | v6.1 changes the operator, not the field. | DESIGN | 29 |
| Y966 | §0 | §2.3 now breaks that tie inside the objective, in two terms — one carrying the design intent, one generic. | MODEL | 30 |
| Y1000 | §0 | §2.3 also pins the solver's optimality tolerance, which turned out to be a correctness requirement rather … | MODEL | 31 |
| Y1001 | §0 | The margin by which the tie-break makes the optimum unique is as small as 3.8e-8 while HiGHS's default … | MEASURED | 33 |
| Y967 | §0 | With all three changes in place the orientation is unchanged across every relabelling tried — 0 of 180 on the … | MEASURED | 34 |
| Y968 | §0 | A canonical node order remains an emitter requirement because the order-invariance is a measurement rather … | MODEL | 37 |
| Y1002 | §0 | The orientation is also unchanged under permutation of the LP's column order. | MODEL | 37 |
| Y969 | §0 | `α_Φ` moves from 1.5 to 2.0. | MODEL | 40 |
| Y970 | §0 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste, and §2.3 states them … | DESIGN | 40 |
| Y971 | §0 | Every derivation previously offered for `α_Φ` is withdrawn without replacement. | MODEL | 42 |
| Y972 | §0 | The 1444 sink set moved from `{english_channel, hangzhou}` to `{genua, hangzhou}`. | MEASURED | 42 |
| Y1186 | §0 | `{english_channel, hangzhou}` is v6.0’s sink set, computed under the unit-cost solver. | MEASURED | 42 |
| Y1187 | §0 | The tie-break and `α_Φ` moved together. | PROCESS | 44 |
| Y1188 | §0 | The tie-break alone re-decides the α = 1.5 answer: the shipped operator at 1.5 gives a single sink, consistent with §1.6’s own count row. | MEASURED | 44 |
| Y1058 | §0 | What moves with the sink set is every figure derived from the aggregate graph — the sink set and its ranks, the source set, the sensitivity bands, and the European scaling. | MODEL | 46 |
| Y1059 | §0 | What holds is everything computed before the aggregate solve: the wealth field, the per-province and per-node totals, … | MODEL | 48 |
| Y1060 | §0 | The per-good graphs' `α(g)` does not read `α_Φ`. | MODEL | 49 |
| Y1061 | §0 | A count was quoted here and is not maintained: `measure6.py`'s figure list grows whenever a figure gains a guard, so t … | PROCESS | 50 |
| Y1003 | §0 | §2.1 records what multiplayer would additionally need, which is now build discipline rather than a design … | MODEL | 51 |
| Y1062 | §0 | v6.2 narrows the wealth rule and changes no number on the 1444 field. | MODEL | 54 |
| Y1063 | §0 | `unrest` is dropped from §1.3's table rather than carried as an excluded row. | PROCESS | 55 |
| Y1064 | §0 | Both changes follow the same reading: a trade node is owner-agnostic, so wealth measures what a province can buy, and … | DESIGN | 56 |
| Y1065 | §0 | An occupying army is a fact about a war. | DESIGN | 59 |
| Y1066 | §0 | What a revolt and an occupation cost the owner is real and is the owner's problem, which is exactly what §1.3 declines … | DESIGN | 59 |
| Y1067 | §0 | The 1444 figures are unchanged because neither input was ever live on that field: `unrest` was already not read, and n … | MODEL | 64 |
| Y1068 | §0 | What moves is what happens during a campaign, which is where the rule now differs from v6.1. | MODEL | 65 |
| Y1069 | §0 | Every figure the retired `unrest` accounting carried is withdrawn rather than repaired, and with it the `revolt_risk` … | PROCESS | 66 |
| Y1189 | §0 | v6.3 changes no computation and no number on the 1444 field. | MODEL | 70 |
| Y1190 | §0 | v6.3 corrects two conclusions the round-8 audit outran: §3.3’s aggregate-versus-per-good distortion comparison and §3.9’s definition of an end. | PROCESS | 70 |
| Y1191 | §0 | v6.3 re-scopes replicate- and build-dependent figures to what their instruments support — §2.2’s timing, §2.3’s seed-dependence and §2.5’s frozen binary. | PROCESS | 72 |
| Y1192 | §0 | v6.3 states the reference implementation’s coverage of §2.2’s list and hands its gaps to §2.9. | PROCESS | 73 |
| Y1193 | §0 | v6.3 adds §2.7 item 18, the devastation scaling probe. | PROCESS | 74 |
| Y1238 | §0 | v6.4 changes no computation. | MODEL | 77 |
| Y1239 | §0 | v6.4 corrects one false file claim: §3.16’s autonomy floors sit in the static-modifier file after all. | PROCESS | 77 |
| Y1240 | §0 | v6.4 re-scopes six figures to their instruments and sources — the quantisation census, the hashseed sweep, the timing inside-count, `genua`’s in-arcs, the build stamp and the permutation-measurement history. | PROCESS | 78 |
| Y1241 | §0 | v6.4 marks three readings at their evidence class: peace valuation’s define, ship propagation’s composition and the localisation-string rule. | PROCESS | 80 |
| Y1242 | §0 | v6.4 retires a dangling residual citation (§3.14), a non-existent trade good (`tools`) and §2.7’s result-tense preamble. | PROCESS | 81 |
| Y009 | §0 | Prose convention: no empirical absolutes — no superlative, no universal quantifier and no threshold asserted … | DESIGN | 95 |
| Y010 | §0 | list is the gravity kernels, the v1 Laplacian, RANK and the seeded basins; `Φ_ord` no longer named | DESIGN | 98 |
| Y011 | §0 | Those rejected-operator numbers were re-measured and re-refuted across the v3 and v5 audits, and not one of the rejection arguments depends on them. | PROCESS | 100 |
| Y1194 | §0 | v4.0’s audit touched one gravity figure and passed it. | PROCESS | 101 |
| Y220 | §0 | Where a comparison is genuinely load-bearing it is stated as a direction rather than as a figure that has to … | DESIGN | 102 |
| Y012 | §0 | Every graded claim from `../v5-owner-agnostic/validation-v5.md` — 22 refuted, 39 partial, 1 unverifiable — is folded t … | PROCESS | 107 |
| Y1070 | §0 | `fixes-agreed.md` carries a row for all 62 graded claims. | PROCESS | 109 |
| Y1071 | §0 | `fixes-agreed.md` is frozen at v6.0: it records what v6.0 changed relative to v5.0 and is not maintained against later … | PROCESS | 109 |
| Y1072 | §0 | Where a figure in `fixes-agreed.md` has since moved, this document is the live one. | PROCESS | 110 |
| Y1073 | §0 | Neither harness targets `fixes-agreed.md` by default. | PROCESS | 111 |
| Y217 | §0 | Measured figures carry the script that produced them where one is named, and the coverage paragraph below records the exceptions. | DESIGN | 112 |
| Y218 | §0 | Deleted text is quoted in `changes-v6.md`. | PROCESS | 112 |
| Y1145 | §0 | The coverage paragraph below records the figures that carry no script. | PROCESS | 112 |
| Y013 | §0 | `scripts/verify6.py` reads figures out of the document text and fails when they disagree with a value … | PROCESS | 114 |
| Y974 | §0 | `verify6.py`'s coverage of the figures this document prints is partial. | PROCESS | 116 |
| Y1051 | §0 | Neither a count nor a proportion of that coverage is given here, for two different reasons, and "partial" is … | DESIGN | 117 |
| Y975 | §0 | No count is given here because some of the harness's checks are generated per matching phrase, so the total … | PROCESS | 118 |
| Y015 | §0 | No coverage proportion is offered because the denominator is not well defined: how a numeric token is delimited moves the count of "the figures the spec prints" by hundreds of tokens. | PROCESS | 120 |
| Y1052 | §0 | An earlier draft of this paragraph asserted "well under half" two sentences before refusing to give a ratio, … | PROCESS | 122 |
| Y016 | §0 | `scripts/coverage6.py` is the honest measure — it corrupts each spec-printed figure whether the harness looks … | PROCESS | 123 |
| Y017 | §0 | Some figures carry a script attribution instead of a guard, and a few carry neither. | PROCESS | 125 |
| Y1074 | §0 | A figure with no script named at its line, and none named for its block, has not been reproduced by anything in `scrip … | PROCESS | 126 |
| Y018 | §0 | `scripts/mutate6.py` reports a higher score that should not be read as coverage: it plants errors only in … | PROCESS | 129 |
| Y219 | §0 | The document has three sections: §1 Mechanics states what the system does, §2 Implementation states how it is … | DESIGN | 133 |
| Y221 | §1.1 | Every trade good has its own directed network over the same adjacency. | MODEL | 141 |
| Y222 | §1.1 | Direction is computed, never authored. | DESIGN | 141 |
| Y223 | §1.1 | For each good `g` the balance is `b_g(n) = s_g(n) − c_g(n)`, oriented by DRAIN in four named phases: peel, … | MODEL | 143 |
| Y224 | §1.1 | Phase 0 repeatedly removes degree-1 nodes, orienting each pendant edge by the sign of its absorbed subtree balance (ne … | MODEL | 144 |
| Y225 | §1.1 | Phase 0 is exact rather than heuristic: every removed edge is a bridge and flow on a tree is determined by … | MODEL | 148 |
| Y226 | §1.1 | On the vanilla map Phase 0 is a no-op — minimum degree 2, zero bridges. | MEASURED | 149 |
| Y227 | §1.1 | Phase 0 exists for modded maps. | DESIGN | 150 |
| Y228 | §1.1 | Phase 1 takes the connected clusters of net demanders in the core, computes the Herfindahl index of their … | MODEL | 152 |
| Y229 | §1.1 | one knob, `r` (default 0); `ρ` withdrawn as a parameter the shipped operator never had | MODEL | 154 |
| Y1075 | §1.1 | The cluster dilation radius `r` links demanders within `r` hops before clustering. | MODEL | 154 |
| Y230 | §1.1 | On vanilla 1444 demand is so ubiquitous that k = 1 for 27 of 29 goods at the default knobs. | MEASURED | 155 |
| Y231 | §1.1 | Phase 1's selection is deliberately weak because Phase 3 self-corrects upward. | DESIGN | 156 |
| Y1076 | §1.1 | A demand-mass quantile `ρ` was documented here as a second Phase-1 knob; the shipped operator has no such parameter — … | PROCESS | 157 |
| Y1077 | §1.1 | The §3.13 calibration option carries its own Phase 1 and does implement a quantile; that is where `ρ` is described. | MODEL | 159 |
| Y232 | §1.1 | Phase 2 solves the uncapacitated min-cost flow serving `b_g` and orients every support edge by its net flow. | MODEL | 162 |
| Y976 | §1.1 | Phase 2's arc costs are near-unit, symmetric in the arc, and read from node wealth: a first-order term … | MODEL | 162 |
| Y977 | §1.1 | The costs are not unit because with unit costs the optimum is not unique and which one the solver returns … | MODEL | 165 |
| Y233 | §1.1 | The support is a spanning-tree basis of at most N−1 edges when the solver returns a basic (vertex) optimum, … | MODEL | 167 |
| Y234 | §1.1 | An interior-point solve without crossover can split flow across equal-length parallel paths and return a … | MODEL | 168 |
| Y235 | §1.1 | §2.2 therefore requires network simplex or a simplex LP. | DESIGN | 170 |
| Y1004 | §1.1 | §2.3 additionally requires the solver's optimality tolerance to be tighter than the margin the tie-break … | MODEL | 170 |
| Y236 | §1.1 | For any optimum the support contains no directed cycle, because with all costs strictly positive a directed … | MODEL | 172 |
| Y237 | §1.1 | Edges with zero net flow are free and are deferred to Phase 3. | MODEL | 175 |
| Y238 | §1.1 | Phase 3 marks nodes Kahn-style: a node is ready when every flow out-neighbour is already marked and it is a … | MODEL | 177 |
| Y239 | §1.1 | Among ready nodes the sweep pops by the priority key (DEF ascending, b ascending, index), where `DEF(v)` is … | MODEL | 179 |
| Y240 | §1.1 | The flow-arc subgraph is acyclic and fixed before any free edge, so `DEF` involves no circularity. | MODEL | 180 |
| Y241 | §1.1 | On a stall the sweep promotes the heaviest flow-terminal demander among the candidates into the sink set, and … | MODEL | 181 |
| Y242 | §1.1 | If the candidates hold no flow-terminal demander at all, the fallback branch promotes the highest-wealth … | MODEL | 183 |
| Y243 | §1.1 | Node wealth is a good-independent input, so the fallback branch needs no bootstrap. | MODEL | 184 |
| Y244 | §1.1 | Candidates at a stall are the unmarked nodes whose flow out-neighbours are all marked; because the flow … | MODEL | 185 |
| Y245 | §1.1 | A candidate carrying any flow out-arc is already ready, and a candidate with inflow is a flow-terminal … | MODEL | 187 |
| Y019 | §1.1 | The fallback branch fires only when every candidate is support-isolated with zero post-peel balance. | MODEL | 189 |
| Y020 | §1.1 | The balance the priority key reads is the one Phase 0 hands on, with each pendant's balance folded into its … | MODEL | 190 |
| Y021 | §1.1 | On a connected core the fallback needs the folded balance to vanish across the core: for a per-good graph … | MODEL | 192 |
| Y022 | §1.1 | Nodes hold between 0 and 72 counted provinces, so equal per-province wealth makes unequal node sums. | MEASURED | 195 |
| Y023 | §1.1 | Where the wealth key ties, the node index decides. | MODEL | 196 |
| Y024 | §1.1 | §2.8's containment set includes the fallbacks because of T3 — a fallback promotion that is a sink in neither … | DESIGN | 197 |
| Y246 | §1.1 | Free edges orient from later-marked to earlier-marked. | MODEL | 200 |
| Y247 | §1.1 | Phase 4 un-peels the Phase-0 pendants in reverse order. | MODEL | 203 |
| Y1078 | §1.1 | Phase 4 emits the orientations Phase 0 determined for the pendants: Phase 0 decides those directions, Phase 4 is where … | MODEL | 203 |
| Y1079 | §1.1 | A pendant sink is visible only after Phase 4 (T1, §3.2). | MODEL | 204 |
| Y248 | §1.1 | Each §1.1 property is labelled proved, measured, or true-by-construction, and the three are never allowed to … | DESIGN | 207 |
| Y250 | §1.1 | The §1.1 property measurements were regenerated by `measure6.py` and `props6.py`. | MEASURED | 208 |
| Y249 | §1.1 | That labelling discipline caught four over-claims between v2.0 and v3.0. | MODEL | 211 |
| Y251 | §1.1 | Global DAG: every arc points from later-marked to earlier-marked, so reversed marking order is a topological … | MODEL | 214 |
| Y252 | §1.1 | Measured acyclic on 29 of 29 goods. | MEASURED | 215 |
| Y253 | §1.1 | Every sink is one of four kinds: a selected demand centre that turned out flow-terminal, a stall-promoted … | MODEL | 217 |
| Y025 | §1.1 | On 1444 the fallback and pendant cases are empty and the sink set is exactly `{selected ∩ flow-terminal} ∪ … | MEASURED | 219 |
| Y026 | §1.1 | That equality is a measurement on this input rather than a theorem, and v2 asserted it as one. | MODEL | 221 |
| Y027 | §1.1 | It does not become a theorem by attaching conditions: "Phase 0 a no-op and no fallback firing" looks … | MODEL | 223 |
| Y254 | §1.1 | Three constructed cases break the sink-set equality: a pendant net-importing leaf is a sink outside the set … | MEASURED | 224 |
| Y255 | §1.1 | A node with no outgoing links for `g` is a sink for `g`; sinks differ per good; there is no global end node. | MODEL | 227 |
| Y256 | §1.1 | The orientation contains a flow serving 100% of every good's demand, because the LP imposes node balance and … | MODEL | 229 |
| Y257 | §1.1 | The premise that makes the LP feasible is connectedness: on a disconnected map the balance must hold per … | MODEL | 231 |
| Y258 | §1.1 | §2.2a states the connectedness requirement and what the solver does when it is violated. *(Row text corrected this round: the prior census cited §2.2; the spec’s sentence — untouched by the diff — reads §2.2a. The correction is to the row, not to the document.)* | MODEL | 234 |
| Y259 | §1.1 | Measured on 1444, which is one component: 100.0% of demand reachable from supply, 29/29 goods, zero orphan … | MEASURED | 235 |
| Y260 | §1.1 | Ready-marking is a monotone closure, so the stall sequence and both promotion branches are provably … | MODEL | 237 |
| Y261 | §1.1 | Free-edge direction is deterministic, by the same closure argument plus the priority key's index tiebreak. | MODEL | 237 |
| Y262 | §1.1 | "zero orientation changes over 145 scheduler permutations (29 goods × 5)", cited to `props6.py` | MEASURED | 241 |
| Y1005 | §1.1 | Measured: zero exact `(DEF, b)` key collisions across all 2,320 core nodes of the 29 per-good solves — not … | MEASURED | 242 |
| Y1006 | §1.1 | Phase 1's within-cluster argmin and its top-k cluster cut are untied on the same field, so no index tiebreak … | MEASURED | 244 |
| Y1080 | §1.1 | The determinism bullet’s figures are all `props6.py`’s — the core-node count included. | PROCESS | 246 |
| Y1081 | §1.1 | `props6.py` was copied and extended from `val5_pergood.py`, and the permutation loop was written for this citation — the figure had been quoted since v2, computed in-tree only at width 2 until this loop widened it to the cited 145. | PROCESS | 250 |
| Y1243 | §1.1 | Before this loop the permutation figure was computed in-tree only by `final.py`’s V035 — sweep-only re-keying, two permutations per good. | PROCESS | 251 |
| Y263 | §1.1 | The certificate flow is a near-fewest-hop routing in aggregate: with unit costs the objective would be … | MODEL | 253 |
| Y978 | §1.1 | the bound is the interval `[1, 1 + TIE_EPS + TIE_EPS2]` itself; no percentage is derived, because the spread relative … | MODEL | 255 |
| Y264 | §1.1 | No per-unit shortest-path claim is made and none holds, because a unit may detour when sink assignment … | MODEL | 259 |
| Y265 | §1.1 | The efficiency property carries no measurement and wants none: it follows from the construction of the LP, … | DESIGN | 262 |
| Y266 | §1.1 | The §3.13 calibration deliberately degrades efficiency, which is a change to the program being solved rather … | DESIGN | 263 |
| Y267 | §1.1 | The orientation is recomputed on a fixed monthly tick, aligned to the vanilla trade tick. | MODEL | 267 |
| Y268 | §1.1 | Orientation is read from the current solve every time, with no memory of the previous one. | MODEL | 267 |
| Y269 | §1.1 | The LP is deterministic on one machine and one build — six identical solves gave one orientation on the reference impl … | MEASURED | 267 |
| Y1082 | §1.1 | The six identical solves are six solves inside a single process, blind to anything that varies between processes; `fin … | MODEL | 269 |
| Y270 | §1.1 | What remains open across machines is §3.13’s build-discipline question (§2.1), not LP determinism, which §2.1 retires. | DESIGN | 272 |
| Y271 | §1.2 | `s(n,g) = goods_produced(n,g)` over the world sum of `goods_produced(m,g)`. | MODEL | 277 |
| Y272 | §1.2 | `goods_produced` is a physical quantity — pre-production-efficiency and pre-autonomy. | MODEL | 280 |
| Y273 | §1.2 | `goods_produced` moves with devastation, occupation and prosperity, because `00_static_modifiers.txt`'s … | ENGINE | 280 |
| Y274 | §1.2 | There is no regularizer: v1 mixed in `s ← (1 − ε)·s + ε/N` to keep dead branches from being oriented by … | MODEL | 282 |
| Y275 | §1.2 | DRAIN's free edges are oriented combinatorially by the drainage sweep rather than by comparing near-equal … | MODEL | 283 |
| Y276 | §1.2 | One node has `b = 0` exactly at 1444 — `cape_of_good_hope` — and it is handled as an ordinary conduit. | MEASURED | 284 |
| Y277 | §1.3 | Demand is assembled per province, then summed to the node. | MODEL | 289 |
| Y028 | §1.3 | Wealth is owner-agnostic and reads three things about the province: its development, its trade good, and its … | MODEL | 291 |
| Y278 | §1.3 | Wealth is a property of the place — what the land is worth per year, before anyone's government touches it. | DESIGN | 292 |
| Y279 | §1.3 | Wealth reads no autonomy, no production efficiency, no national ideas, no estate or government modifiers, and no techn … | MODEL | 292 |
| Y029 | §1.3 | Two provinces with the same development, trade good and condition have the same wealth whoever owns them. | MODEL | 294 |
| Y280 | §1.3 | A province's wealth does not change when it is conquered. | MODEL | 296 |
| Y030 | §1.3 | Owner-agnosticism is true by construction rather than by a policed rule; v3.0 through v5.0 stated the property and then defended it by classifying the install — v4.0 and v5.0 with the two-test classifier, v3.0 with a structural rule (§0) — a large surface that was wrong in both independent audits. | DESIGN | 298 |
| Y031 | §1.3 | `base_tax`, `base_production` and the trade good are bare attributes of the place, so nothing about them … | MODEL | 303 |
| Y032 | §1.3 | What the change gives up: `gems`' `local_tax_modifier` and `incense`' `trade_value_modifier` are genuinely … | DESIGN | 304 |
| Y033 | §1.3 | The dropped apparatus was live on 89 of the 2,472 counted provinces — 43 `gems` plus 31 `incense` plus 16 … | ENGINE | 309 |
| Y034 | §1.3 | That count depends on the field: it is 87 under the withdrawn `is_city` filter, and 89 rather than 88 because … | ENGINE | 310 |
| Y1083 | §1.3 | The deleted-apparatus figures are reproduced by `apparatus6.py`, which holds the deleted classifier's constants frozen … | PROCESS | 313 |
| Y1084 | §1.3 | The frozen constants record what v5.0's input surface was worth, not a live table, and sit in their own file precisely … | DESIGN | 314 |
| Y1085 | §1.3 | `measure6.py` imports the apparatus figures rather than restating them. | PROCESS | 316 |
| Y281 | §1.3 | The model trades that fidelity for an input surface with no classification question in it. | DESIGN | 318 |
| Y035 | §1.3 | `goods_produced(p) = GP_COEFF · base_production(p) · (1 + sum of province-state goods modifiers)`, with no … | MODEL | 321 |
| Y036 | §1.3 | `trade_value(p) = goods_produced(p) · price(good(p))` in ducats per year, with no trade-value modifier term. | MODEL | 322 |
| Y037 | §1.3 | `tax_value(p) = TAX_COEFF · base_tax(p)` — no modifier at all (restated L54, L378, L1007) *(Row text corrected this round: the prior census’s L49-50, L349 and L955 were stale. The three restatement sites in the current document are §0’s v6.2 note at L54, §1.3’s “No modifier reaches the tax term at all.” paragraph at L378, and §2.2 item 4’s “The tax term takes no modifier at all” at L1007. The correction is to the row, not to the document.)* | MODEL | 323 |
| Y282 | §1.3 | `wealth(p) = tax_value(p) + trade_value(p)`, in ducats per year. | MODEL | 324 |
| Y283 | §1.3 | `c(n,g)` is the node's share of world wealth raised to `α(g)`: the sum over provinces in the node of … | MODEL | 326 |
| Y038 | §1.3 | `GP_COEFF` is a shipped file value: `common/static_modifiers/00_static_modifiers.txt` carries … | ENGINE | 334 |
| Y284 | §1.3 | `GP_COEFF` and `TAX_COEFF` have different provenance from one another. | DESIGN | 334 |
| Y039 | §1.3 | `GP_COEFF` is therefore moddable and is read at runtime rather than hardcoded. | DESIGN | 338 |
| Y040 | §1.3 | `TAX_COEFF` is in no file that has been found — not `defines.lua`, not `common/defines/`, not that … | ENGINE | 338 |
| Y285 | §1.3 | The tax and trade terms share a time basis and are safe to add, because the engine's own province tooltips … | ENGINE | 342 |
| Y041 | §1.3 | The tax tooltip's schema is `Base: trunc(base_tax × 0.0833333) (Yearly base_tax)`, observed as `Base: 0.49 … | ENGINE | 343 |
| Y042 | §1.3 | The parenthetical is `base_tax` itself and the `Base` line is its truncated twelfth; it is not twelve times … | ENGINE | 346 |
| Y043 | §1.3 | v4.0 and v5.0 wrote the schema as `Base: X (Yearly 12·X)`, false on both of its own data points, and v3.0 … | PROCESS | 347 |
| Y044 | §1.3 | The monthly production tooltip's `Trade Value` line is consistent with the same relation on one observation, … | ENGINE | 348 |
| Y045 | §1.3 | Both monthly figures being the annual value over twelve is what lets the annual forms add directly, and the … | MODEL | 350 |
| Y286 | §1.3 | The coefficients were measured on two provinces: Garnatah (223) with `base_tax` 6, `base_production` 4, silk … | ENGINE | 353 |
| Y287 | §1.3 | Only the tooltips' `Base` lines are used. | DESIGN | 354 |
| Y288 | §1.3 | A province window's `Trade Value` also carries the owner's `global_trade_goods_size_modifier`. | ENGINE | 355 |
| Y289 | §1.3 | Garnatah's window read 3.52 rather than 0.80 × 4.00 = 3.20 because Granada's 1444 monarch held the … | ENGINE | 356 |
| Y290 | §1.3 | Ruler personalities are rolled at game start wherever country history scripts none, so any window figure is … | ENGINE | 357 |
| Y1146 | §1.3 | The `Base`-line schema, the truncation ordering below and the window's modifier composition are recorded observations from those tooltip sessions. | ENGINE | 361 |
| Y1147 | §1.3 | What the materials re-verify — and what the round-7 audit re-verified again — is the save-side inputs and every step of the arithmetic. | PROCESS | 362 |
| Y1148 | §1.3 | The on-screen strings are the observation itself, and a named observation is a source §3.16 admits. | DESIGN | 363 |
| Y291 | §1.3 | Modifiers apply after the coefficient, not before: the engine computes the base from development first and … | ENGINE | 366 |
| Y046 | §1.3 | Observed on Garnatah, `base_tax` 6 with `Tax Income Efficiency 125.0%` displays `Base 0.49` and then `0.62`; … | ENGINE | 367 |
| Y047 | §1.3 | The example establishes only the ordering — base from development first, percentage second — and nothing … | ENGINE | 370 |
| Y048 | §1.3 | v4.0 and v5.0 read this as "0.49 × 1.25 = 0.6125 shown as 0.62", which requires rounding while §2.3 requires … | PROCESS | 372 |
| Y049 | §1.3 | Flat goods bonuses would add into `goods_produced` before the price multiply — the goods-produced tooltip … | ENGINE | 373 |
| Y050 | §1.3 | Province condition is the one thing besides development and the good that wealth reads: five static modifiers describe … | ENGINE | 379 |
| Y979 | §1.3 | `unrest` is deliberately not read; its 1444 liveness (the 21-province reading) is no longer asserted — the revolt-risk … | MODEL | 382 |
| Y051 | §1.3 | four-row table; `occupied` enters `goods_produced` only, its tax half "granted by the file and not read"; no `unrest` … | ENGINE | 386 |
| Y054 | §1.3 | `devastation`'s scaling law is the one row in the table not settled by a shipped file: … | ENGINE | 388 |
| Y1196 | §1.3 | Until §2.7 item 18 runs, `devastation`’s scaling law is an unverified scaling assumption, testable in one live session. | PROCESS | 388 |
| Y1197 | §1.3 | The stock 1444 start already carries two devastation levels — Bohemia 50, Erzgebirge and Moravia 20 — so one session gives two province windows. | ENGINE | 388 |
| Y053 | §1.3 | no modifier reaches the tax term at all; all four rows enter `goods_produced` | MODEL | 393 |
| Y1086 | §1.3 | `occupied`'s `local_tax_modifier` is granted by the file and not read: an occupier's presence is a fact about who is s … | DESIGN | 394 |
| Y981 | §1.3 | `STATE_TAX_MOD` is empty, kept as an empty declaration | MODEL | 397 |
| Y1087 | §1.3 | `STATE_TAX_MOD` is kept as an empty declaration rather than deleted, so the shape of the exclusion stays legible in th … | DESIGN | 397 |
| Y1088 | §1.3 | On the 1444 start `prosperity`, `under_siege` and `occupied` are live on no counted province — all three describe cond … | MEASURED | 401 |
| Y1089 | §1.3 | The wealth rule carries four modifiers, of which one is exercised by the reference field. | MODEL | 403 |
| Y980 | §1.3 | Revolt risk is not a property of the place: in play it carries separatism from recent conquest, unaccepted culture, wr … | MODEL | 406 |
| Y1090 | §1.3 | A province in revolt still has the buying power its development gives it; whether its owner manages to collect against … | DESIGN | 411 |
| Y984 | §1.3 | The effect `unrest` would buy is already bought: conquest costing a province its wealth is delivered by `devastation`, … | MODEL | 414 |
| Y1091 | §1.3 | No figure is quoted for what the `unrest` exclusion costs, and none should be reconstructed. | DESIGN | 418 |
| Y1092 | §1.3 | Earlier drafts carried such a figure, and keeping it accurate meant parsing `revolt_risk` out of the save — an input s … | PROCESS | 419 |
| Y1093 | §1.3 | The exclusion is a decision about what wealth means, and a measured cost would not bear on it. | DESIGN | 422 |
| Y058 | §1.3 | The condition modifiers are what make the map answer to war: §1.2's volatility and §3.3's "a besieged province genuine … | DESIGN | 424 |
| Y059 | §1.3 | Eleven counted provinces begin devastated — Bohemia at 50, Erzgebirge and Moravia at 20 — and no … | ENGINE | 429 |
| Y060 | §1.3 | That devastation is applied by `on_startup`, which fires `flavor_boh.15` ("The Aftermath of the Hussite … | ENGINE | 430 |
| Y061 | §1.3 | The start devastation costs 13.40 ducats across the eleven affected counted provinces. | MEASURED | 431 |
| Y062 | §1.3 | The start state is what the engine produces rather than what the history files say, and that costs three … | DESIGN | 436 |
| Y063 | §1.3 | `on_startup` also fires `flavor_mng.42`, `flavor_mos.1`, `flavor_geo.1` and others directly from its own … | ENGINE | 439 |
| Y064 | §1.3 | Development does not move before the first tick: on this start the history parse matches the save on 2,472 of … | ENGINE | 442 |
| Y065 | §1.3 | v6.0's first draft said `flavor_geo.1` carries `add_base_tax` and could move development pre-tick; it does … | ENGINE | 444 |
| Y066 | §1.3 | `add_base_*` in a dated block before the start date accumulates, and v5.0 and earlier overwrote instead of … | ENGINE | 448 |
| Y067 | §1.3 | `is_city = yes` is not a filter the engine applies: 20 owned provinces omit or comment out that line — … | ENGINE | 451 |
| Y068 | §1.3 | The model counts a province when it has an owner and lies in a trade node: 2,472 provinces, not 2,452. | DESIGN | 453 |
| Y069 | §1.3 | Twenty counted provinces have no trade good in their history file (`trade_goods = unknown`), and the engine … | ENGINE | 456 |
| Y070 | §1.3 | The model reads the good the engine actually rolled rather than predicting the draw, and pricing those … | DESIGN | 458 |
| Y071 | §1.3 | On this save the twenty came up seven `fur`, five `grain`, three `wool`, two `livestock`, and one each of … | ENGINE | 460 |
| Y293 | §1.3 | Everything the engine itemised on a real province that is not local is excluded: `Reform Iqta` (+5%, government), `Clergy` (+5% observed, estate — the file value is loyalty-scaled, so the 5 is the scaled instance rather than a file constant), national ideas (+15%), production efficiency from technology (+2%), and the owner’s goods-produced modifiers. | ENGINE | 466 |
| Y1149 | §1.3 | `01_church.txt` grants `global_tax_modifier = 0.2` under "scale with loyalty & power", so the Clergy 5 is a scaled instance rather than a file constant. | ENGINE | 466 |
| Y294 | §1.3 | `Core` (+75%) and `City` (+25%) are not excluded, because they are already inside `TAX_COEFF`. | MODEL | 469 |
| Y295 | §1.3 | The engine's tax multiplier is the sum of the itemised percentages: Garnatah's `Tax Income Efficiency: … | ENGINE | 470 |
| Y1150 | §1.3 | Of Garnatah's `Tax Income Efficiency: 125.0%`, the 75, 25, Iqta 5 and ideas 15 are file-confirmed — 120 of the 125 — and the Clergy 5 is the loyalty-scaled remainder observed on the tooltip. | ENGINE | 471 |
| Y296 | §1.3 | A cored city province carrying nothing else sums to exactly 0.75 + 0.25 = 1.00 and yields `base_tax` ducats a … | ENGINE | 474 |
| Y072 | §1.3 | The model applies `TAX_COEFF = 1.0` to every province it counts: ownership is not modelled, so every province … | DESIGN | 476 |
| Y297 | §1.3 | Carrying either the `Core` or the `City` term again would double-count it. | MODEL | 477 |
| Y073 | §1.3 | That is a modelling choice with a known cost: two readings, both on cored city provinces at `base_tax` 2 and … | DESIGN | 478 |
| Y074 | §1.3 | `base_tax` at 1444 runs up to 15 (province 1821), with total development reaching 33 there. | ENGINE | 479 |
| Y298 | §1.3 | Unowned provinces are outside the model: `s` and `c` are computed over provinces that have an owner and lie … | DESIGN | 482 |
| Y299 | §1.3 | What owner-agnostic demand buys: demand stops responding to who rules and responds only to what is there, so … | DESIGN | 485 |
| Y075 | §1.3 | Owner-agnostic wealth also removes a large source of hidden owner-dependence from the aggregate graph of … | MODEL | 487 |
| Y300 | §1.4 | `α(g) = clamp((price(g)/P₀)^k, α_min, α_max)` with `P₀ = 2.0` ducats. | MODEL | 493 |
| Y301 | §1.4 | α > 1 makes demand superlinear in provincial wealth, so luxuries concentrate on individually rich provinces. | MODEL | 496 |
| Y302 | §1.4 | α = 1 makes demand proportional to economic size. | MODEL | 497 |
| Y303 | §1.4 | α < 1 makes demand sublinear, so bulk goods spread toward populous regions. | MODEL | 498 |
| Y304 | §1.4 | α moves with vanilla price events in both directions, with no smoothing. | MODEL | 500 |
| Y305 | §1.5 | Gold is excluded by configuration. | MODEL | 504 |
| Y306 | §1.5 | Gold-mine income is its own income category in the engine (`INCOMEGOLD`, `gold_income` as a distinct … | ENGINE | 504 |
| Y307 | §1.5 | Under owner-agnostic wealth the exclusion is stronger still: `wealth(p)` is built from `base_tax`, … | MODEL | 507 |
| Y308 | §1.5 | Gold is inert in vanilla trade value (`base_price = 0`, `goldtype = yes`), so the exclusion costs nothing. | ENGINE | 510 |
| Y309 | §1.5 | Whether the per-province production-income field nevertheless carries the gold figure before the country-level split i … | MODEL | 513 |
| Y310 | §1.5 | Any good with zero world production this month has no graph, because `s(n,g)` is undefined when nothing … | MODEL | 516 |
| Y311 | §1.5 | A latent good acquires graph, value weight and survival-table entry on the first month any province produces … | MODEL | 518 |
| Y312 | §1.5 | Activation is not a local addition: a province produces exactly one trade good at a time, so a latent good … | ENGINE | 520 |
| Y313 | §1.5 | In the month of conversion the new good gains a producer and the old good loses one, so both goods' supply … | MODEL | 524 |
| Y314 | §1.5 | The converting province is repriced, so `wealth(p)` changes and with it `c(n,g)` for every good in the game, … | MODEL | 526 |
| Y315 | §1.5 | `V_g` moves for both goods, reweighting every display, link value and AI score. | MODEL | 529 |
| Y316 | §1.5 | `Φ_w` moves on activation, because §1.6 runs DRAIN on that same wealth field. | MODEL | 530 |
| Y317 | §1.5 | An activation is a world-state change on the scale of a development change or a conquest, and every graph in … | DESIGN | 532 |
| Y076 | §1.5 | Repricing to coal the 45 latent-coal provinces that are owned at 1444 flips 16 of 159 `Φ_w` edges and adds … | MEASURED | 533 |
| Y077 | §1.5 | The counterfactual holds every non-repriced input fixed: province 4237 is both latent-coal and one of the … | MEASURED | 535 |
| Y318 | §1.5 | Coal's base price of 10.0 is the highest in the shipped price table. | ENGINE | 539 |
| Y319 | §1.5 | v2.1 held that a latent good leaves `Φ_w` unaffected because "`Φ_w` reads wealth, not goods"; that was true under v2.0 … | MODEL | 542 |
| Y320 | §1.5 | Coal produces nowhere at the 1444 start. | ENGINE | 547 |
| Y321 | §1.5 | Coal's default trigger fires on Enlightenment (the Manufactories branches require special flags), per … | ENGINE | 547 |
| Y322 | §1.5 | The 58 latent-coal provinces convert province-by-province over years rather than in a single tick, so the … | ENGINE | 550 |
| Y324 | §1.6 | For the wealth good, supply is uniform: `s_w(n) = 1/N`. | MODEL | 559 |
| Y325 | §1.6 | For the wealth good, `c_w(n)` is the node's share of world wealth raised to `α_Φ`. | MODEL | 560 |
| Y326 | §1.6 | `b_w = s_w − c_w`, with `α_Φ = 2.0`, a hyperparameter. | MODEL | 561 |
| Y327 | §1.6 | `Φ_w = DRAIN(b_w)` — the §1.1 operator with wealth as the good. | MODEL | 563 |
| Y328 | §1.6 | `Φ_w` is the graph installed in the game. | DESIGN | 566 |
| Y329 | §1.6 | Under `Φ_w` every node supplies uniformly and rich nodes are net demanders, so all wealth in the world pulls … | MODEL | 566 |
| Y078 | §1.6 | Both the sinks' count and their locations move with the wealth field, and `α_Φ` sets how sharply … | MODEL | 569 |
| Y079 | §1.6 | scaling European development alone moves the count both up and down before it settles back at two (the sweep below) | MEASURED | 570 |
| Y080 | §1.6 | v2.0 through v4.0 said the count "emerges from concentration" and v5.0 said "the count is set by `α_Φ`"; both … | MODEL | 572 |
| Y330 | §1.6 | What the world state moves is where the sinks are and how the map drains toward them, which is the property … | DESIGN | 577 |
| Y083 | §1.6 | Measured on 1444 data at `α_Φ = 2.0`: two sinks, `genua` and `hangzhou`, at `c_w` ranks 2 and 1 and … | MEASURED | 580 |
| Y084 | §1.6 | Both sinks are properties of the world, because the orientation does not depend on how the nodes are numbered … | MODEL | 581 |
| Y335 | §1.6 | With unit arc costs Phase 2's b-flow is degenerate: many routings reach the same minimum cost, and the … | MODEL | 585 |
| Y085 | §1.6 | Measured on that LP directly, 40 of 40 permutations return a different optimal support at an objective … | MEASURED | 587 |
| Y087 | §1.6 | So the old sink set was partly an artifact of the node order, and v6.0 said so. | MODEL | 588 |
| Y986 | §1.6 | Phase 2 now breaks those ties inside the objective, with a cost symmetric in the arc and read from node … | MODEL | 591 |
| Y086 | §1.6 | Over 180 relabellings — three seeds of 60, every input held fixed — the orientation did not change once: 0 of … | MEASURED | 592 |
| Y987 | §1.6 | On the same LP under the tie-break cost, 0 of 40 permutations return a different support. | MEASURED | 592 |
| Y988 | §1.6 | The instrument is a reimplementation, and a reimplementation whose Phase 2 minimises the old objective … | MEASURED | 598 |
| Y989 | §1.6 | A symmetric cost is required rather than a stylistic choice: a directional preference of the form `1 − … | MODEL | 601 |
| Y091 | §1.6 | Nothing this section quotes about the installed graph is conditional on the node order. | MODEL | 605 |
| Y093 | §1.6 | Over the 180 relabellings the sink set, every edge direction, and the promotion and fallback counts were … | MEASURED | 605 |
| Y990 | §1.6 | The per-good graphs are a different matter: the tie-break cost is read from good-independent node wealth, but … | MODEL | 610 |
| Y991 | §1.6 | Under the first-order tie-break term alone with the solver tolerance pinned, 76 of 290 per-good relabelling runs moved an edge. | MEASURED | 613 |
| Y1007 | §1.6 | §2.3’s second-order term takes per-good relabelling sensitivity from 76 to 0 of 290 with the tolerance pinned in both configurations, and the goods admitting an alternative optimum from 18 of 29 to 1. | MEASURED | 615 |
| Y1008 | §1.6 | Pinning the solver’s optimality tolerance takes per-good relabelling sensitivity from 12 to 0 of 290 with the full cost in both configurations. | MEASURED | 616 |
| Y1009 | §1.6 | On this field the per-good graphs are order-invariant over the orderings tried, as `Φ_w` is. | MODEL | 617 |
| Y336 | §1.6 | The emitter should still fix one canonical order, because both order-invariance guarantees are measured … | DESIGN | 620 |
| Y993 | §1.6 | The value weights are the exception: `V_g` is `price(g)` times a sum over producers, with no direction in it, … | MODEL | 622 |
| Y094 | §1.6 | Phase 1 selects `hangzhou`; `genua` arrives by stall promotion, so there is 1 promotion and 0 fallbacks. | MEASURED | 626 |
| Y095 | §1.6 | Five sources, all in the bottom half of the wealth field, at `c_w` ranks 55–79 and mean degree 2.4 against … | MEASURED | 627 |
| Y337 | §1.6 | v2 called the sources "cul-de-sacs"; the degrees are not far off that reading here, but it is a description … | MODEL | 628 |
| Y096 | §1.6 | Every node drains to a sink, the map is acyclic and 159/159 oriented, the sink set is unchanged under ±1% … | MEASURED | 629 |
| Y082 | §1.6 | 1444's `b_w` has largest magnitude 0.0347. | MEASURED | 630 |
| Y338 | §1.6 | `Φ_w`'s marking order is a per-node scalar whose descending comparison reproduces the DAG (0 violations), so … | MEASURED | 632 |
| Y097 | §1.6 | Per good on the same field: 2–8 sinks, mean 3.69, 29/29 acyclic, 0 fallbacks fired, and 90.6% of ordered node … | MEASURED | 635 |
| Y1094 | §1.6 | The agreement figure is a description of how often one power map coincides with twenty-nine commodity maps, not a qual … | DESIGN | 640 |
| Y100 | §1.6 | `α_Φ = 2.0`, `TIE_EPS = 1e-3` and `TIE_EPS2 = 1e-6` are hyperparameters; the choice is developer taste and … | DESIGN | 645 |
| Y102 | §1.6 | No derivation is claimed, none is implied, and none should be reconstructed from the figures below: they … | DESIGN | 647 |
| Y103 | §1.6 | Across `α_Φ` = 1.00…8.00 at 0.01 the sink set is a step function, and `α_Φ = 2.0` sits in the band [1.63, … | MEASURED | 651 |
| Y104 | §1.6 | Sampled at six values the sink count is non-monotone: 3 → 1 → 2 → 2 → 1 → 1 across `α_Φ` in {1, 1.5, 2, 3, 4, … | MEASURED | 653 |
| Y992 | §1.6 | The sink set is unchanged at every `TIE_EPS` value tried from 1e-13 to 1e+12 — 24 grid points. | MEASURED | 654 |
| Y1151 | §1.6 | `epsilon6.py` validates by reproducing the shipped map 159/159 at eps = `TIE_EPS`. | MEASURED | 655 |
| Y1152 | §1.6 | For the sinks, `TIE_EPS` is a switch with nothing to tune anywhere in reach. | MODEL | 656 |
| Y1153 | §1.6 | What moves at the `TIE_EPS` extremes is edge orientation: up to 16 edges below 1e-4 and up to 25 above 3. | MEASURED | 657 |
| Y1154 | §1.6 | An earlier printing bounded the `TIE_EPS` band at about 1e-6 and about 1 and supplied each edge with a mechanism; both edges are withdrawn, because no sink transition exists at either. | PROCESS | 658 |
| Y1010 | §1.6 | `TIE_EPS2` behaves the same way as `TIE_EPS` and was measured at 1e-7, 1e-6 and 1e-5, all three leaving the … | MEASURED | 661 |
| Y105 | §1.6 | A written warning against reintroducing the withdrawn justifications for `α_Φ` — resemblance to vanilla's … | DESIGN | 665 |
| Y106 | §1.6 | "Europe becomes the centre of trade as it develops" is the design claim, and it is what §3.1's first goal … | DESIGN | 670 |
| Y107 | §1.6 | At 1444 the map ends in Genoa and in Hangzhou, and as European development compounds Europe gains ends and … | MEASURED | 671 |
| Y108 | §1.6 | The mechanism carrying that is that wealth is linear in development, so developing a region moves its `c_w` … | MODEL | 672 |
| Y109 | §1.6 | the table is withdrawn ("A table of interval boundaries was published here and is withdrawn"); the sweep is re-reporte … | MEASURED | 676 |
| Y1095 | §1.6 | The European sweep samples uniformly on a 0.001 grid from ×1.000 to ×2.600. | MEASURED | 677 |
| Y110 | §1.6 | The table is to be read as a direction rather than a trajectory: it scales all 824 counted European provinces by one f … | DESIGN | 679 |
| Y1096 | §1.6 | The widest interval carrying three European ends and none in Asia runs ×1.973 to ×2.456, with `english_channel`, `genu … | MEASURED | 680 |
| Y111 | §1.6 | The European-scaling path is not monotone: `hangzhou` leaves, returns and leaves again, `gulf_of_siam` holds an end over one stretch and nowhere else, and of the three intervals narrower than ×0.01, one — ×1.702–×1.709 — carries a set that appears nowhere else in the sweep. | MEASURED | 683 |
| Y1097 | §1.6 | A table of interval boundaries was published here and is withdrawn: its rows came from bisection and disagree with a u … | PROCESS | 687 |
| Y1098 | §1.6 | The effect of a boundary that sits between samples is a row that looks like a fact and is an artifact of the sampling. | MODEL | 688 |
| Y340 | §1.6 | These are properties of this snapshot rather than constants of the model — what one field yielded under one scaling, w … | DESIGN | 699 |
| Y112 | §1.6 | Because §1.3's wealth is linear in development, scaling development and scaling wealth are the same operation here — m … | MEASURED | 700 |
| Y341 | §1.6 | All three institutions the period is named for begin in Europe between 1450 and 1550: Renaissance `1450.1.1` … | ENGINE | 704 |
| Y342 | §1.6 | The Renaissance's embracement bonus is `development_cost = -0.05`, a standing discount on every subsequent … | ENGINE | 707 |
| Y343 | §1.6 | Those institution bonuses are country-scoped, so §1.3 excludes them from wealth directly; they reach the map … | MODEL | 708 |
| Y344 | §1.6 | "draws A RECOGNISABLE pre-Columbian trade geography" — the definite claim and "unprompted" both softened | MEASURED | 712 |
| Y345 | §1.6 | From the north the route to the Asian end is the Volga and the steppe: `white_sea → novgorod → kazan → … | MEASURED | 713 |
| Y113 | §1.6 | From Iberia the route is the African coast and the Red Sea: `sevilla → safi → timbuktu → katsina → ethiopia → … | MODEL | 715 |
| Y114 | §1.6 | No route leaves `genua` at all — it is a sink, out-degree 0 against in-degree 5, and the western Mediterranean, the Adriatic, the Rhône corridor and Alexandria carry power into it. | MEASURED | 717 |
| Y994 | §1.6 | `english_channel` is not an end at this α: it drains to `genua` in two hops through `champagne`, and reaches … | MODEL | 718 |
| Y1244 | §1.6 | `genua`’s five in-arcs are `valencia`, `tunis`, `ragusa`, `champagne` and `alexandria`. | MEASURED | 718 |
| Y115 | §1.6 | No Europe→sink route passes the Cape of Good Hope, checked exhaustively rather than sampled: of the 23 … | MEASURED | 723 |
| Y346 | §1.6 | "asserted as a universal because the whole set was enumerated rather than sampled — which is the only ground on which … | DESIGN | 724 |
| Y116 | §1.6 | The Cape is a live conduit rather than an idle one: in-degree 2, out-degree 2, with 81 ordered node pairs for … | MEASURED | 729 |
| Y117 | §1.6 | The Cape’s 81 is a count of pairs `(a, b)` where `a` reaches the Cape, the Cape reaches `b`, and `a` reaches `b` — not pairs where some shortest path transits it, which gives 71. | MEASURED | 733 |
| Y1155 | §1.6 | Requiring *every* shortest path to transit the Cape gives 60 pairs on the same field. | MEASURED | 734 |
| Y1156 | §1.6 | Requiring a *unique* shortest path through the Cape gives 43 pairs on the same field. | MEASURED | 735 |
| Y118 | §1.6 | In the per-good graphs the Cape also carries Asian spices to Europe; `Φ_w` models power, not cargo. | MODEL | 736 |
| Y119 | §1.6 | sole sink from ×1.52, continuous to the top of the swept range; all-22 gives no sole sink below ×25, the set settling … | MEASURED | 740 |
| Y1100 | §1.6 | Swept from ×2.50 to ×25.00 on the all-22 scaling, none of the eastern four holds an end at any multiple, and both surv … | MEASURED | 742 |
| Y1101 | §1.6 | The earlier draft's clause attributing the no-sole-sink behaviour to "the eastern four pulling ends of their own" was … | PROCESS | 744 |
| Y120 | §1.6 | The Cape reverses under the same growth — 1444's `ivory_coast`/`zanzibar`→Cape→`comorin_cape`/`malacca` … | MEASURED | 745 |
| Y347 | §1.6 | The 22 European nodes are the 18 western and central ones (`english_channel`, `north_sea`, `baltic_sea`, … | MODEL | 750 |
| Y121 | §1.6 | Dev-stacking a single node's top province concentrates the map on that node, and extra sinks at intermediate … | MODEL | 754 |
| Y1102 | §1.6 | This section's figures are measured under the shipped sweep key (DEF ascending, β ascending, index), which is a design … | MODEL | 757 |
| Y1103 | §1.6 | Measured against DEF-descending on the same field: of the 19 aggregate-graph facts `round6.py` checks, 6 move and 13 d … | MEASURED | 759 |
| Y1104 | §1.6 | The thirteen that hold: the sink set and its count, the promotion count, the fallback count, acyclicity, the number of … | MEASURED | 760 |
| Y1105 | §1.6 | The six that move: the source count (5 against 10), the sources' `c_w` rank range, their mean degree, the Cape's order … | MEASURED | 763 |
| Y1106 | §1.6 | Under the descending key `sevilla` reaches neither `ganges_delta` nor the Asian end, so the Iberian route ceases to ex … | MEASURED | 765 |
| Y1107 | §1.6 | The northern route's endpoints stay connected under both keys — the check is that `white_sea` still reaches `hangzhou` … | MEASURED | 766 |
| Y1108 | §1.6 | The two long routes are properties of this field and this key; the sink set is a property of the field alone. | MODEL | 769 |
| Y348 | §1.6 | The v1 diagnostic identity (`Φ ≡ φ₀` at α = 1) does not survive the operator change, because DRAIN performs … | MODEL | 773 |
| Y349 | §1.6 | Its replacement as the end-to-end correctness check is exact orientation equality between the reference and … | DESIGN | 774 |
| Y350 | §1.7 | Merchant placement, range and the collect/steer choice are vanilla, with one merchant per country per node. | ENGINE | 780 |
| Y351 | §1.7 | A merchant present gives +2 trade power (`MERCHANT_MAX_POWER_BONUS`) and a +10% bonus on trade income … | ENGINE | 780 |
| Y352 | §1.7 | v1 and v2 both called the second bonus "+10% trade efficiency"; trade efficiency and a flat income bonus are … | ENGINE | 780 |
| Y353 | §1.7 | Collect is vanilla, including the −50% penalty outside the home node. | ENGINE | 782 |
| Y1157 | §1.7 | The −50% off-home collect penalty is `TRADE_NON_CAPITAL_OFFICE = -0.50` at `common/defines.lua:1200`, the define §2.3's table names. | ENGINE | 782 |
| Y354 | §1.7 | Under Steer the node window lists every link incident to the node. | MODEL | 784 |
| Y355 | §1.7 | The vanilla window already renders both an incoming and an outgoing link list as clickable entries … | ENGINE | 784 |
| Y356 | §1.7 | What changes is what an incoming entry does — it must accept a merchant assignment rather than merely … | DESIGN | 787 |
| Y357 | §1.7 | §2.7 item 14 settled that the incoming entry only navigates: clicking `Safi` in Sevilla's window switched the … | ENGINE | 788 |
| Y358 | §1.7 | A merchant assigned to link {n,m} steers every good oriented n → m. | MODEL | 793 |
| Y359 | §1.7 | A merchant assigned to link {n,m} is inert for every good oriented m → n. | MODEL | 794 |
| Y360 | §1.7 | A merchant keeps its assignment when a link flips; only its active good set changes. | MODEL | 795 |
| Y361 | §1.7 | The same physical link can host a merchant at each end, active on disjoint good sets. | MODEL | 797 |
| Y362 | §1.7 | Caravan power requires the merchant to be steering at least one good on that link; assignment alone does not … | MODEL | 799 |
| Y363 | §1.7 | That constrains only the two steering conditions — collecting at an inland node as main trading port is … | MODEL | 800 |
| Y364 | §1.7 | The engine's own caravan grant conditions are `merchant_present_inland` and `merchant_steering_to_inland`, … | ENGINE | 801 |
| Y365 | §1.7 | §2.7 item 11 settles the caravan recipient, and §3.11 carries both readings of the exposure surface. | DESIGN | 803 |
| Y366 | §1.8 | Trade power and collect/transfer intent are node-wide; what varies per good is what they produce. | MODEL | 808 |
| Y367 | §1.8 | `collected_share(n,g) = 1` if n is a sink for g, else `P_collect / (P_collect + P_transfer(g))`. | MODEL | 829 |
| Y368 | §1.8 | Transfer eligibility is per good: a country's power counts toward `P_transfer(g)` only if it has a merchant … | MODEL | 833 |
| Y369 | §1.8 | The remainder moves per good by the vanilla two-case rule. | MODEL | 835 |
| Y370 | §1.8 | If any country steers `g` at `n`, the outgoing value of `g` is divided across outgoing links in proportion to … | ENGINE | 837 |
| Y371 | §1.8 | An outgoing link with no steerer receives nothing, even when other links are steered. | ENGINE | 837 |
| Y372 | §1.8 | A single steerer takes all of `g`'s outgoing value down its link, however little power it holds. | ENGINE | 837 |
| Y373 | §1.8 | If no country steers `g` at `n`, the outgoing value splits evenly across `g`'s outgoing links. | ENGINE | 839 |
| Y374 | §1.8 | At `g`'s sink there is no remainder: 100% is collected and divided among collectors by trade power. | MODEL | 841 |
| Y375 | §1.8 | Vanilla gates still apply: trade range, and the rule that there is no transfer into a node where nobody holds … | ENGINE | 843 |
| Y1158 | §1.8 | The both-ends rule is stated from the trade interface's behaviour; no define, string or searched file names it. | ENGINE | 844 |
| Y1159 | §1.8 | The both-ends rule is a probe-class fact under §3.16's own rule, and is recorded as such. | PROCESS | 845 |
| Y376 | §1.8 | What trade range gates is reach, not flow: every string, define and modifier that mentions it is about where … | ENGINE | 846 |
| Y377 | §1.8 | No string, define or modifier ties range to link flow — which is a statement about the files rather than a … | ENGINE | 851 |
| Y378 | §1.8 | There is no trade "supply range" in the engine; the only supply-range constructs are naval. | ENGINE | 854 |
| Y379 | §1.9 | A country whose provincial trade power in a node meets the threshold receives a share of it in immediately upstream nodes, with no power-or-merchant condition on the receiving country there, and with distance the one gate the save shows remaining. | ENGINE | 860 |
| Y380 | §1.9 | The engine's own tooltip says power transfers "to trade nodes where it already has power", and that qualifier … | ENGINE | 860 |
| Y381 | §1.9 | Measured: France holds zero provinces and zero merchants in Sevilla and still appears there with 3.3 power, … | ENGINE | 860 |
| Y382 | §1.9 | This line was §3.16's cautionary case; it is now closed, and it closed in favour of the spec. | DESIGN | 860 |
| Y383 | §1.9 | The propagation share is `1 / TRADE_PROPAGATE_DIVIDER`, and the threshold in raw power is … | ENGINE | 860 |
| Y1160 | §1.9 | What the save shows gating propagated receipt is distance: 72 of 272 threshold-qualifying (country, upstream-node) pairs receive nothing, concentrated in distant colonial pairs. | MEASURED | 860 |
| Y1161 | §1.9 | England qualifies in `english_channel` yet propagates nothing into `chesapeake_bay`. | MEASURED | 860 |
| Y1162 | §1.9 | That pattern is consistent with trade range gating propagated receipt — an unstated gate, added to §2.7's probes as item 17. | MODEL | 860 |
| Y385 | §1.9 | Propagation is strictly one hop and never chains. | ENGINE | 862 |
| Y386 | §1.9 | A node receives the summed contributions of all its downstream neighbours. | ENGINE | 863 |
| Y387 | §1.9 | Direction for propagation is read from `Φ_w`. | MODEL | 865 |
| Y388 | §1.10 | Any mechanism gated on one nation being upstream or downstream of another evaluates TRUE. | DESIGN | 869 |
| Y389 | §1.10 | Any node-pair direction dependency reads `Φ_w`. | DESIGN | 871 |
| Y390 | §1.10 | Where a gate scopes a set or a path, that scope reads `Φ_w` with a three-rung fallback ladder: the `Φ_w` … | DESIGN | 873 |
| Y391 | §1.10 | The mechanics below the gates are unpatched and unchanged; reorientation reaches them through the trade power … | ENGINE | 879 |
| Y392 | §1.10 | Nothing in that group is patched and all of it moves monthly. | MODEL | 879 |
| Y393 | §1.10 | Trade-conflict casus belli thresholds are `JUSTIFY_TRADE_CONFLICT_LIMIT` (target) and … | ENGINE | 885 |
| Y394 | §1.10 | Privateer blocking is thresholded by `MINIMUM_TRADE_POWER_TO_PREVENT_PRIVATEER`. | ENGINE | 887 |
| Y395 | §1.10 | Trade-company extra merchant and control are thresholded by `TRADE_COMPANY_STRONG_LIMIT` and … | ENGINE | 888 |
| Y396 | §1.10 | Improve Inland Routes needs 50% to establish and 40% to maintain plus a merchant present in the node, and is … | ENGINE | 890 |
| Y397 | §1.10 | Propagate Religion needs 50% to establish and 50% to maintain in the default branch and 35/35 in the terminal … | ENGINE | 891 |
| Y398 | §1.10 | The nine `N_trade_power_for_propogate_religion` country-flag rungs are banded: maintain trails select by 5–10 … | ENGINE | 891 |
| Y399 | §1.10 | The banding is the reverse of what v1 recorded: Improve Inland Routes is the one unconditionally banded … | ENGINE | 893 |
| Y400 | §1.10 | Banding therefore absorbs very little chatter: a power share oscillating across any single-valued limit … | ENGINE | 895 |
| Y401 | §1.10 | Banding is not the only damper: three shipped defines rate-limit the mechanics that carry these thresholds. | ENGINE | 897 |
| Y122 | §1.10 | `TRADING_POLICY_COOLDOWN_MONTHS = 12` applies to seven of the nine entries in … | ENGINE | 898 |
| Y123 | §1.10 | `maximize_profit` and `maximize_profit_upgraded` carry `cooldown = no` in … | ENGINE | 903 |
| Y124 | §1.10 | `TRADE_COMPANY_DAYS_TO_SWAP_LEADER = 30` with `TRADE_COMPANY_COOLDOWN = 60` means a flickering share does not … | ENGINE | 904 |
| Y125 | §1.10 | What is left exposed are the undamped rows of §1.10’s table — both trade-conflict casus belli rows and privateer blocking, three of its seven. | ENGINE | 906 |
| Y1198 | §1.10 | Four of the table’s seven rows are damped — two by the policy cooldown and two by the trade-company defines. | ENGINE | 907 |
| Y402 | §1.10 | The flicker-risk set is "every country at a single-valued limit, plus flagless countries at Propagate … | ENGINE | 908 |
| Y403 | §1.10 | Casus belli availability is the most visible symptom, since it can appear and vanish month to month. | ENGINE | 910 |
| Y126 | §1.10 | Measured on the 1444 start, the caravan cap of 50 is 9.4% to 47.0% of an inland node's total trade power, … | MEASURED | 913 |
| Y127 | §1.10 | As a share of the node's total after the grant lands — 50/(total+50) — the same figures read 8.6% to 32.0%, … | MEASURED | 913 |
| Y128 | §1.10 | On §2.2's derived 25-node inland basis (dropping `siberia`) the median is 21.3%, or 17.5% after the grant. | MEASURED | 913 |
| Y404 | §1.10 | Caravan power is in this group but is not a threshold mechanic and is not a function of raw trade power at … | ENGINE | 913 |
| Y405 | §1.10 | When caravan power applies it is worth up to the cap for any major power — enough to move a node's power … | MODEL | 913 |
| Y406 | §1.10 | The largest single incumbent holder runs 23.6 to 143.2, so a country at the caravan cap outweighs the largest … | MEASURED | 913 |
| Y407 | §1.10 | v4.0 read the save's per-node `highest_power` field as the largest incumbent's power; it is not — parsing … | ENGINE | 913 |
| Y408 | §1.10 | What `highest_power` does hold was not determined, and the model does not read it. | MODEL | 913 |
| Y409 | §1.10 | v1 and v2 both described caravan power as "a step function on raw power", which contradicted their own §3.11. | PROCESS | 913 |
| Y410 | §1.10 | No mission, decision, event, or trade company in 1.37.5 names a trade node — zero non-comment references … | ENGINE | 915 |
| Y411 | §1.10 | Trade companies are bare province lists. | ENGINE | 916 |
| Y412 | §1.10 | "through four families" with the member-province family spelled out (`any/random/every/all_…`) and an explicit caveat … | ENGINE | 917 |
| Y1109 | §1.10 | Measured across `common/`, `missions/`, `decisions/` and `events/` with comments stripped, the four structural constru … | MEASURED | 919 |
| Y1110 | §1.10 | None of the 80 node names appears anywhere in the four trees. | MEASURED | 921 |
| Y1111 | §1.10 | The token scan matches `trade_node` as a bare word and by construction cannot see every compound key containing it; su … | ENGINE | 922 |
| Y1112 | §1.10 | "Bounded by class" is the honest claim only for the families named; the full key inventory is an emitter-time enumerat … | DESIGN | 924 |
| Y413 | §1.10 | Nodes themselves never change under the mod — only connections do — so the name-collision class of conflict … | MODEL | 925 |
| Y414 | §1.10 | What remains exposed is semantics: `highest_value_trade_node` and node-scoped triggers are evaluated against … | ENGINE | 927 |
| Y415 | §1.10 | That semantic exposure is accepted and listed for the compatibility pass rather than engineered around. | DESIGN | 930 |
| Y416 | §1.11 | The overlord always receives the treasure fleet. | DESIGN | 935 |
| Y417 | §1.11 | The fleet routes by the §1.10 ladder, passing each node en route where privateers skim a share proportional … | MODEL | 935 |
| Y418 | §1.11 | Where the diversion mechanic is active, colonial gold income is diverted from the colonial nation. | ENGINE | 937 |
| Y419 | §1.11 | Diverted gold does not enter `wealth` at either end, for the deeper reason of §1.5: gold income is its own … | MODEL | 938 |
| Y1163 | §1.12 | §1.12 specifies display behaviour the DLL must deliver; its present tense is specification, not observation of a build that does not yet exist. | PROCESS | 943 |
| Y420 | §1.12 | The in-game economy is the per-good economy: node values, the node window, pie charts, the ledger, the … | DESIGN | 946 |
| Y427 | §2.1 | The implementation is one program: a runtime-attached DLL that each month reads live game state, solves per … | DESIGN | 993 |
| Y428 | §2.1 | It ships with a generated `00_tradenodes.txt` for load time and a companion overlay for what the engine … | DESIGN | 993 |
| Y429 | §2.1 | The target platform is Windows/Steam. | DESIGN | 995 |
| Y430 | §2.1 | Achievements are off with any mod (`ACHIEVEMENTS_DISABLED_MODIFIED_GAME`). | ENGINE | 995 |
| Y431 | §2.1 | The engine will load an ironman save in a modded game — `Loading ironman in modded game` is a shipped code … | ENGINE | 996 |
| Y432 | §2.1 | EU4 multiplayer is lockstep with checksums, so every client must reach the same answer; the classical worry … | ENGINE | 1000 |
| Y434 | §2.1 | DRAIN's exposure is different in kind from v1's dense linear algebra, which was badly exposed to it: v1 … | MODEL | 1002 |
| Y435 | §2.1 | DRAIN's comparisons are of input-derived quantities (`DEF`, `b`, arc costs) rather than of solver residuals, … | MODEL | 1007 |
| Y1011 | §2.1 | The multiplayer question is no longer whether the arithmetic agrees to the last bit but whether the build is … | DESIGN | 1009 |
| Y995 | §2.1 | §2.3's two changes move the desync question from a design problem to a verification one: the largest exposure … | MODEL | 1013 |
| Y1113 | §2.1 | The determinism fingerprint is one SHA-256 over `Φ_w` and all 29 per-good graphs, including sinks, sources, promotions … | MODEL | 1020 |
| Y1012 | §2.1 | There is no randomness in the solve: an identical output fingerprint over repeated runs, separate processes and six `PYTHONHASHSEED` values (0, 1, 2, 42, 12345, `random`), so there is no seed to pin and no set-iteration order to depend on. | MEASURED | 1020 |
| Y1013 | §2.1 | The margin by which the optimum is unique is 3.8e-8 worst per good and 7.5e-6 on the aggregate — 8 to 10 … | MEASURED | 1021 |
| Y1014 | §2.1 | Orientation under LP column permutation: 0 flips on the aggregate and on all 29 goods, with an objective … | MEASURED | 1022 |
| Y1015 | §2.1 | The per-good `abs(net)` distribution is bimodal — 2,321 edge-goods at exactly 0 and 2,290 above 1e-6, with … | MEASURED | 1024 |
| Y1114 | §2.1 | The smallest non-zero per-good `\|net\|` magnitude is 6.94e-06. | MEASURED | 1024 |
| Y1016 | §2.1 | A few units in the last place cannot change any decision this solver makes, so what remains is not … | MODEL | 1026 |
| Y1017 | §2.1 | Check 1 — one binary per platform and no cross-platform sessions, because a single compiled instruction stream gives identical IEEE-754 results on any x86-64 host it runs on. | DESIGN | 1030 |
| Y1199 | §2.1 | Running on *any* host requires building to the architecturally-mandatory baseline (SSE2). | DESIGN | 1030 |
| Y1200 | §2.1 | Targeting an optional extension turns "any host" into "any host with that extension" — check 2’s live risk restated at build scope. | DESIGN | 1031 |
| Y1018 | §2.1 | The `../v2-drain/` DLL precedent is already Windows- and Steam-only, so the one-binary rule matches practice … | MODEL | 1033 |
| Y1019 | §2.1 | Check 2 — no runtime CPU dispatch in the LP solver and single-threaded: this is the live risk, because … | DESIGN | 1035 |
| Y1020 | §2.1 | Check 3 — §2.8's cross-implementation orientation check compares the DLL against the reference implementation … | DESIGN | 1039 |
| Y1021 | §2.1 | Every trade number EU4 writes to a save is quantised to 1/1000: a full sweep of the six fields `total`, `val`, `p_pow`, `retention`, `collector_power` and `max_pow` finds 3,354 values in `VANILLA_start.eu4` and 3,810 in `Castile1444_12_22.eu4`, 0 off-grid in both. | ENGINE | 1044 |
| Y1022 | §2.1 | Quantisation of that kind erases any divergence below half a grid step, which is the standard cheap defence. | ENGINE | 1047 |
| Y1247 | §2.1 | The quantisation census was run by `val62p4_quant.py`, its output recorded at `scripts/r8/quant.out`. | PROCESS | 1047 |
| Y1023 | §2.1 | The files cannot settle whether the rounding happens in the simulation or only in the serialiser; that needs … | ENGINE | 1048 |
| Y1024 | §2.1 | Quantisation would not rescue this solver either way: the orientation margins of 3.8e-8 to 7.5e-6 are three … | MODEL | 1050 |
| Y436 | §2.1 | Until checks 1–3 are done, ship single-player only. | DESIGN | 1054 |
| Y1025 | §2.1 | The reason for shipping single-player has changed: it is no longer "vertex selection is machine-dependent" … | MODEL | 1054 |
| Y437 | §2.2 | Solver item 1 is a parser for `common/tradenodes/00_tradenodes.txt` reading adjacency, `members`, … | DESIGN | 1060 |
| Y439 | §2.2 | Solver item 3 is a parser for `common/defines.lua` merged with `common/defines/` overrides in load order. | DESIGN | 1062 |
| Y129 | §2.2 | `TAX_COEFF · base_tax + …` — "The tax term takes no modifier at all" | MODEL | 1063 |
| Y130 | §2.2 | four modifiers in scope, all four reaching `goods_produced`; at 1444 only `devastation` is live, on eleven; `unrest` d … | MEASURED | 1065 |
| Y440 | §2.2 | `GP_COEFF` is read from `common/static_modifiers/00_static_modifiers.txt` rather than hardcoded. | ENGINE | 1068 |
| Y131 | §2.2 | World wealth is 10,607.40 annual ducats over 2,472 counted provinces. | MEASURED | 1072 |
| Y441 | §2.2 | Solver item 5 is DRAIN per good: a min-cost b-flow using network simplex or a simplex LP rather than … | DESIGN | 1073 |
| Y442 | §2.2 | The Phase-4 evaluator's `unserved` and `stranded` must be equal by conservation, since the sum of `b_g` over … | MODEL | 1075 |
| Y443 | §2.2 | `Φ_w` is one more DRAIN run with wealth as the good — the 30th solve, same code path. | MODEL | 1077 |
| Y444 | §2.2 | Solver item 6 is a survival table `S_g[n][H]` for AI scoring, one table serving every country. | DESIGN | 1078 |
| Y445 | §2.2 | Solver item 7 is a mutual reachability census: 30 goods × 80 BFS producing an 80×80 matrix whose entry counts … | DESIGN | 1079 |
| Y1164 | §2.2 | The 30 goods × 80 BFS mutual-reachability census, as an 80×80 counting matrix, is the DLL deliverable. | DESIGN | 1079 |
| Y1165 | §2.2 | The reference implementation ships the boolean projection of that census over the 29 live goods, and that projection is what feeds §3.8's 5,723. | MODEL | 1079 |
| Y446 | §2.2 | Solver item 8 is a synthetic-shock harness that edits parsed province data and re-solves. | PROCESS | 1080 |
| Y132 | §2.2 | Measured on the reference implementation (scipy/HiGHS plus the deterministic sweep, one machine): of order 0.1 s for all 29 goods. | MEASURED | 1083 |
| Y133 | §2.2 | Repeated 12-run experiments on one machine do not reproduce each other closely enough for anything finer; across every replicate batch to date every all-29 median is of order 0.1 s while per-good-average maxima land on both sides of 10 ms. | MEASURED | 1085 |
| Y134 | §2.2 | v5.0’s "0.17–0.21 s for all 29 goods" is not reproducible: the number of twelve runs landing inside that interval has run from 0 to 12 across recorded replicates. | MEASURED | 1091 |
| Y1248 | §2.2 | A count of 0 runs inside v5.0’s interval is recorded in `scripts/r8/p3_time.out` among others, and a count of 12 in `scripts/val62check/p3_time_p4.out`. | MEASURED | 1092 |
| Y1249 | §2.2 | 0 and 12 are the floor and the ceiling of a count out of twelve, so no endpoint is left to outrun. | PROCESS | 1093 |
| Y1250 | §2.2 | No interior set is enumerated: successive audit passes keep recording interior values a prior pass had not collected, so an enumerated set would be the same outrunnable figure this parenthetical exists to retire. | PROCESS | 1094 |
| Y448 | §2.2 | That order of magnitude is reached with a generic LP; the all-29 figure is what a native network simplex would have to improve on, and no measurement in this project supports a specific projection, and none is offered. | DESIGN | 1097 |
| Y450 | §2.2 | The two implementations must agree on orientation exactly — a combinatorial comparison with no tolerance band … | DESIGN | 1101 |
| Y449 | §2.2 | Two implementations of one specification: the list above specifies the solver deliverable, the reference implementation (standalone, run against parsed saves, the thing every validation in §2.8 is measured on) ships a stated subset of it, and the shipped DLL carries a second implementation of items 4–7 in the host language reading live memory instead of save files. | DESIGN | 1101 |
| Y1201 | §2.2 | The reference implementation ships items 1 (less `path`/`control`), 4, 5, 7 (as the boolean projection) and 8 of §2.2’s list. | PROCESS | 1101 |
| Y1202 | §2.2 | The shipped node file carries `path` and `control` and `nodes.py` discards both, while §2.4 item 3 nevertheless obliges the emitter to reverse both. | PROCESS | 1101 |
| Y1204 | §2.2 | The reference implementation reads three defines by regex rather than by the merged parse of item 3. | PROCESS | 1101 |
| Y1205 | §2.2 | The reference implementation does not build the survival table. | PROCESS | 1101 |
| Y1206 | §2.2 | §2.9’s build order is where those reference-implementation gaps are owned. | PROCESS | 1101 |
| Y451 | §2.2 | The parsers and the harness stay reference-only, and the DLL never reads a save. | PROCESS | 1103 |
| Y452 | §2.2 | Inland is derived rather than trusted from the flag: a node with no coastal province among its `members`. | DESIGN | 1105 |
| Y453 | §2.2 | The derivation and the flag disagree at exactly one node — `siberia` carries `inland=yes` but has two … | ENGINE | 1106 |
| Y454 | §2.2a | v2 called the target "map-agnostic" while proving its central properties only for the map it was measured on; … | MODEL | 1111 |
| Y455 | §2.2a | Premise 1 is that the node graph is connected: reachability is LP feasibility, and the LP is feasible because … | MODEL | 1115 |
| Y456 | §2.2a | On a graph with more than one component the global balance is not enough — each component must balance … | MODEL | 1116 |
| Y457 | §2.2a | Vanilla 1444 is one component. | MEASURED | 1119 |
| Y458 | §2.2a | The solver must compute components once at load; on a single component it proceeds, and on more than one it … | DESIGN | 1121 |
| Y459 | §2.2a | The solver must not silently hand an infeasible program to the LP. | DESIGN | 1124 |
| Y460 | §2.2a | v1 carried per-component renormalisation and v2 dropped it without replacement; v3 restores the requirement. | PROCESS | 1125 |
| Y461 | §2.2a | Premise 2 is that Phase 0 is a no-op, or the map-dependent properties are read as measurements: several §1.1 … | MODEL | 1128 |
| Y462 | §2.2a | Where Phase 0 acts, three properties weaken and the spec says so rather than asserting through it. | DESIGN | 1130 |
| Y463 | §2.2a | Global DAG is proved on a 2-core map and still proved where Phase 0 acts, because pendant edges are bridges … | MODEL | 1135 |
| Y464 | §2.2a | Sink-set equality is measured exact 29/29 on a 2-core map and fails where Phase 0 acts, because a pendant … | MEASURED | 1136 |
| Y465 | §2.2a | Marking order reproduces the DAG on a 2-core map and fails where Phase 0 acts, because pendants have no marking order … | MODEL | 1137 |
| Y135 | §2.2a | Where Phase 0 acts, free-edge determinism is unaffected but index-independence is not: the key reads the … | MODEL | 1138 |
| Y466 | §2.2a | Two further cases are independent of Phase 0 and both break sink-set equality inside the 2-core: a selected … | MEASURED | 1140 |
| Y467 | §2.2a | The stated target is connected maps: on a connected map with minimum degree at least 2 every §1.1 property is … | DESIGN | 1145 |
| Y468 | §2.2a | On a connected map with pendants the algorithm still runs and still produces an acyclic, fully-oriented, … | MODEL | 1146 |
| Y469 | §2.2a | On a disconnected map the solver must renormalise per component or refuse. | DESIGN | 1148 |
| Y470 | §2.3 | Constants are read at runtime and never hardcoded. | DESIGN | 1153 |
| Y471 | §2.3 | The nine runtime-read uses map to named defines: `TRADE_PROPAGATE_DIVIDER`, `TRADE_PROPAGATE_THRESHOLD`, … | ENGINE | 1155 |
| Y472 | §2.3 | `TRADE_MERCHANT_PRESENT` is a bonus on income, not trade efficiency. | ENGINE | 1162 |
| Y136 | §2.3 | The two wealth coefficients are not the same kind of constant: the emitter reads `GP_COEFF` rather than … | DESIGN | 1167 |
| Y473 | §2.3 | `GP_COEFF` is 0.2 goods produced per point of `base_production`, measured on four provinces at four … | ENGINE | 1181 |
| Y474 | §2.3 | `TAX_COEFF` is 1.0 ducat per year per point of `base_tax`, measured on two provinces at two development … | ENGINE | 1182 |
| Y475 | §2.3 | Both coefficients are read off the tooltips' base lines, which carry no owner term — Garnatah also has … | ENGINE | 1184 |
| Y476 | §2.3 | Neither coefficient is read off a province window, because a window figure carries the owner's modifiers and … | ENGINE | 1185 |
| Y477 | §2.3 | Prices come from `common/prices/00_prices.txt` at runtime and are never hardcoded. | ENGINE | 1186 |
| Y478 | §2.3 | The design constants are the excluded-goods list (defaulting to gold), the α price anchor `P₀ = 2.0`, the … | DESIGN | 1189 |
| Y480 | §2.3 | two knobs — `r = 0` and the 1e-11 tolerance; `ρ` withdrawn as never shipped | MODEL | 1192 |
| Y481 | §2.3 | "an absolute threshold rather than a relative one; §3.13 records why that is settled rather than open" | MODEL | 1193 |
| Y482 | §2.3 | the option "replaces Phase 1, moves the zero-flow tolerance and removes α's clamp"; still recorded in §3.13, still not … | DESIGN | 1196 |
| Y479 | §2.3 | `α_Φ`, `TIE_EPS` and `TIE_EPS2` are hyperparameters whose values are developer taste, the document offers no … | MODEL | 1199 |
| Y339 | §2.3 | Changing any of the three hyperparameters is a design decision, and §1.6 records how the field responds … | DESIGN | 1202 |
| Y996 | §2.3 | `TIE_EPS` and `TIE_EPS2` together set the Phase-2 objective, `cost(u,v) = 1 + TIE_EPS·(w[u]+w[v])/2 + … | MODEL | 1207 |
| Y1026 | §2.3 | The two cost terms do different jobs and only the first means anything: the first-order term is the design … | DESIGN | 1218 |
| Y1027 | §2.3 | The second-order term is tie-breaking and nothing else; its form is arbitrary and no reading should be … | DESIGN | 1220 |
| Y998 | §2.3 | A single cost vector does not make every solve unique, because uniqueness of an LP optimum depends on `b` as … | MODEL | 1223 |
| Y1028 | §2.3 | Measured on zero-reduced-cost arcs outside the support: the aggregate `b_w` goes from 40 under unit costs to … | MEASURED | 1226 |
| Y1029 | §2.3 | Adding the second-order term takes the zero-reduced-cost arcs to 1 arc on 1 good. | MEASURED | 1228 |
| Y1166 | §2.3 | The earlier 84 → 13 printings mixed seeds: 84 at seeds 1 and 2024, 13 at seed 606, with no single seed yielding both. | MEASURED | 1232 |
| Y1167 | §2.3 | Those earlier figures were measured at the HiGHS default tolerance, which the shipped solver does not use. | PROCESS | 1233 |
| Y1168 | §2.3 | They are replaced rather than repaired. | PROCESS | 1234 |
| Y999 | §2.3 | BOTH costs make all 159 edge costs distinct (the 3-pairs-equal claim gone); the structured term leaves 11 of 29 goods … | MEASURED | 1236 |
| Y1030 | §2.3 | The solver's optimality tolerance is a correctness requirement rather than a performance knob, and HiGHS … | MODEL | 1245 |
| Y1207 | §2.3 | The tolerance option and its default are what scipy documents; the termination behaviour is established behaviourally by the bisection below rather than from HiGHS’s internals. | PROCESS | 1246 |
| Y1208 | §2.3 | HiGHS’s internals are outside the materials. | PROCESS | 1248 |
| Y1053 | §2.3 | `scipy.optimize.linprog`'s `method="highs"` options document that default as `1e-07`, for both the dual and … | MODEL | 1249 |
| Y1031 | §2.3 | The margin by which the tie-break makes the optimum unique runs as low as 3.8e-8 on some per-good solves, so … | MEASURED | 1250 |
| Y1032 | §2.3 | Over six permutations of the LP’s column order, `copper` and `paper` returned 4 and 8 orientation flips summed over the six — copper’s on four distinct edge-slots, paper’s on two, flipped in four of the six — with objectives differing by 7.7e-10 relative: unequal-quality answers rather than tied optima. | MEASURED | 1253 |
| Y1054 | §2.3 | The tolerance mechanism is confirmed rather than inferred, by bisecting the tolerance against `copper`. | MODEL | 1258 |
| Y1055 | §2.3 | Leaving the solver tolerance unset and setting it to 1e-7 give identical results at every seed tried, and that identity — not any flip count — is what pins the effective default independently of the documentation. | MEASURED | 1259 |
| Y1169 | §2.3 | The `copper` flip count over four column permutations is a function of the seed that draws the permutations; `p3_bisect.py`’s three seeds (20260821, 7, 4242) give 2, 8 and 6. | MEASURED | 1260 |
| Y1209 | §2.3 | Seeds 0–30 span 4–14 flips, with 8 the most common. | MEASURED | 1260 |
| Y1210 | §2.3 | The counting rule is the same throughout — distinct per-permutation flips — and the two instruments agree wherever seeds coincide. | MEASURED | 1261 |
| Y1056 | §2.3 | 1e-8 gives 0 flips at every seed, and 1e-8 is the first value below `copper`’s 3.765e-8 margin. | MEASURED | 1264 |
| Y1057 | §2.3 | The flips therefore appear exactly when the tolerance exceeds the margin, which is the claim. | MODEL | 1265 |
| Y1033 | §2.3 | `flowop.LP_OPTS` ships 1e-10 — HiGHS's floor for these options, taken for headroom rather than necessity — … | MEASURED | 1266 |
| Y1034 | §2.3 | No figure in this document moved when the pinned tolerance went in: the shipped column order was already … | PROCESS | 1267 |
| Y1036 | §2.3 | What the second-order term buys is replacing a tiebreak that was arbitrary and order-dependent — the node … | DESIGN | 1274 |
| Y1037 | §2.3 | The normalisation of `w` is load-bearing per good and that is a cost of the second-order term; for the first-order term alone it was not, by algebra rather than by sweep — `w` enters only through `TIE_EPS · (w[u] + w[v]) / 2` — so the normalisation is a strength choice. | MODEL | 1284 |
| Y1170 | §2.3 | §1.6's `TIE_EPS` sweep is run on the shipped two-term cost and is the sensitivity record for the tie-break's strength. | PROCESS | 1287 |
| Y1038 | §2.3 | dividing by the world total moves the aggregate by 7 of 159 edges, and 13 of 29 per-good graphs move under at least on … | MEASURED | 1288 |
| Y1116 | §2.3 | `w/mean` and `N·w/sum` are algebraically the same vector, and on this field min-max and `w/max` are too, so a sweep ov … | MODEL | 1293 |
| Y1117 | §2.3 | `cape_of_good_hope` holds no counted province at all: its 20 members are one sea zone and nineteen land provinces, non … | ENGINE | 1295 |
| Y1118 | §2.3 | A re-measuring probe must inherit `flowop.LP_OPTS`: without the pinned tolerance the same sweep undercounts — under `w … | MEASURED | 1297 |
| Y1039 | §2.3 | The choice of normalisation is a third arbitrary decision with an observable consequence where before it was free; min … | DESIGN | 1302 |
| Y997 | §2.3 | Every DRAIN solve uses this cost, per good as well as aggregate, and since `w` is node wealth the same cost … | MODEL | 1305 |
| Y483 | §2.3 | DLC state is a third input axis: treasure-fleet diversion and caravan power are both DLC-conditional, and … | ENGINE | 1310 |
| Y484 | §2.4 | The tradenodes file is generated once from the campaign start date's `Φ_w` and then owned by the DLL in … | DESIGN | 1314 |
| Y485 | §2.4 | The engine performs no topological sort; it validates that the file is one, logging … | ENGINE | 1316 |
| Y487 | §2.4 | What the engine does not tolerate is a cycle: a hand-authored two-node cycle produced … | ENGINE | 1324 |
| Y488 | §2.4 | The crash dump records no per-frame addresses. | ENGINE | 1326 |
| Y489 | §2.4 | Acyclicity is therefore a hard correctness requirement of the emitter, established by observation rather than … | DESIGN | 1327 |
| Y1171 | §2.4 | The session record `../v2-drain/game-session.md` covers only the first two of the crash launches. | PROCESS | 1329 |
| Y1172 | §2.4 | The three dumps — `eu4_20260820_134250`, `_134617`, `_165621` in the EU4 `crashes/` directory — are identical in exception address and frame depth, and are the citation for the count of three. | ENGINE | 1330 |
| Y490 | §2.4 | A reversed link is honoured completely: moving one `outgoing` block from `sevilla` to `valencia` with the … | ENGINE | 1333 |
| Y491 | §2.4 | In that test Valencia moved from Sevilla's outgoing side to its incoming side, Sevilla became an end node … | ENGINE | 1335 |
| Y492 | §2.4 | Every provincial power figure was unchanged in that test. | ENGINE | 1338 |
| Y493 | §2.4 | That test is the mod's core premise verified end to end. | DESIGN | 1339 |
| Y494 | §2.4 | Item 1: emit in decreasing `Φ_w` marking order, which is the convention the engine states and the shipped … | ENGINE | 1341 |
| Y138 | §2.4 | A canonical node order is still a correctness requirement but is no longer what decides the installed map: … | DESIGN | 1343 |
| Y495 | §2.4 | Phase 2's min-cost b-flow is degenerate under unit arc costs: many distinct supports carry the same optimal … | MODEL | 1347 |
| Y139 | §2.4 | Measured on that objective, 40 of 40 permutations return a different optimal support. | MEASURED | 1349 |
| Y140 | §2.4 | Those permutations reach an objective identical to within a few units in the last place. | MODEL | 1349 |
| Y147 | §2.4 | §2.3 now breaks those ties inside the objective. | MODEL | 1350 |
| Y141 | §2.4 | On the same LP under the tie-break cost 0 of 40 permutations return a different support, and running the … | MEASURED | 1351 |
| Y143 | §2.4 | A wealth-weighted cost need not break ties in a per-good LP whose `b` is a different vector; the second-order term takes per-good relabelling sensitivity from 76 of 290 to 0 with the tolerance pinned in both configurations, and pinning the tolerance takes it from 12 of 290 to 0 with the full cost in both. | MEASURED | 1360 |
| Y146 | §2.4 | The counts are HiGHS-specific in their detail but not in kind: any simplex returns a vertex of a degenerate … | MODEL | 1371 |
| Y144 | §2.4 | v6.0’s 580-of-580 per-good sweep measures the unit-cost objective, so it describes the former solver and is superseded — by the relabelling triple above — rather than contradicted. | PROCESS | 1375 |
| Y148 | §2.4 | §1.1's priority key ties in more places than §1.1 documents — besides the free-edge sweep it decides Phase … | MEASURED | 1378 |
| Y496 | §2.4 | One visible consequence of node order: the node window renders its incoming/outgoing link lists in file … | ENGINE | 1383 |
| Y149 | §2.4 | The end-flag list is a function of the world rather than of the node order: across the 180 relabellings of … | DESIGN | 1386 |
| Y497 | §2.4 | Item 2: `end=yes` on every `Φ_w` sink, stripped from any former end node that gains outgoing links. | DESIGN | 1386 |
| Y150 | §2.4 | 1444 has two end nodes, `genua` and `hangzhou`, against vanilla's three. | MEASURED | 1389 |
| Y498 | §2.4 | The end count is not fixed — it follows the wealth field and `α_Φ` — so the emitter reads it from the solve … | DESIGN | 1392 |
| Y1211 | §2.4 | That the emitter reads the end count from the solve is emitter behaviour and so specification; the premise, a varying count, is measured. | PROCESS | 1392 |
| Y499 | §2.4 | Item 3: link reversal means moving the `outgoing` block, reversing the `path` province list and reversing the … | DESIGN | 1394 |
| Y500 | §2.4 | Item 4: `location`, `members`, `inland=yes`, `ai_will_propagate_through_trade` and unrecognized keys … | DESIGN | 1395 |
| Y501 | §2.5 | Attachment uses pattern scanning and function hooking, following the EU4dll precedent, which provides the … | DESIGN | 1399 |
| Y502 | §2.5 | The mod ships a runtime-patching DLL rather than a modified executable. | DESIGN | 1399 |
| Y1213 | §2.5 | A patch is a new binary — §2.3’s re-measure-on-patch rule applied to offsets. | DESIGN | 1399 |
| Y1212 | §2.5 | The binary is at build `835bfdf8`, the hash constant across `eu4_rev.txt` and all three crash dumps, whose metadata stamps it `2024-10-03 10:50:26 +0200`. | ENGINE | 1399 |
| Y503 | §2.5 | The binary is frozen at build `835bfdf8`, so offsets found stay found for that binary, and a patch is a new binary. | ENGINE | 1399 |
| Y1251 | §2.5 | `eu4_rev.txt` carries the hash alone. | ENGINE | 1399 |
| Y504 | §2.5 | The nation-pair direction gates of §1.10 are hooked and returned true at the call site rather than by forcing … | DESIGN | 1401 |
| Y505 | §2.6 | The monthly trade tick runs in three passes: static power and modifiers; a pass from the end nodes … | ENGINE | 1405 |
| Y506 | §2.6 | Written each tick: node trade value as the sum over goods of `value_g(n)`. | MODEL | 1414 |
| Y507 | §2.6 | Written each tick: node collectible pool as the sum over goods of `value_g(n) · collected_share(n,g)`. | MODEL | 1415 |
| Y508 | §2.6 | Written each tick: per-link value as net realized flow summed over goods, in the installed `Φ_w` direction. | MODEL | 1416 |
| Y509 | §2.6 | Country trade income is derived by the engine from the written fields, unless stored. | ENGINE | 1417 |
| Y510 | §2.6 | Feeding the engine the collectible pool is sufficient for a narrower reason than it looks: `collect_pool` is … | MODEL | 1419 |
| Y511 | §2.6 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a … | MODEL | 1419 |
| Y512 | §2.6 | There are two deadlines, not one window: display immediately after the value pass, because AI consumers read … | ENGINE | 1423 |
| Y513 | §2.6 | Payment is bounded by the month boundary, since the treasury reconciles at the start of each month against … | ENGINE | 1424 |
| Y514 | §2.6 | Per-link values are written net, which can be negative where realized flow opposes the drawn arrow. | MODEL | 1426 |
| Y515 | §2.7 | Items 1–10 are the v1 probe set, to be settled with a debugger on a vanilla install in one session, though the claim audit found several are observable without one. | DESIGN | 1430 |
| Y1252 | §2.7 | None of probe items 1–10 has been run, and §2.9 counts them open. | PROCESS | 1431 |
| Y516 | §2.7 | Items 13–15 were run against 1.37.5, with results folded into §1.9, §2.4 and §3.6. | PROCESS | 1434 |
| Y517 | §2.7 | Item 12 was dropped rather than run, because under owner-agnostic wealth the per-province production-income … | DESIGN | 1435 |
| Y518 | §2.7 | Probe 13 settled and reversed the hedge: the engine does not tolerate a cycle — `EXCEPTION_STACK_OVERFLOW`, 1002 frames at one address, on three launches. | ENGINE | 1440 |
| Y1173 | §2.7 | §2.4's citation note reconciles the session record's two launches with the three dumps. | PROCESS | 1440 |
| Y519 | §2.7 | Probe 14 settled and confirmed the spec: the incoming-link entry only navigates, and clicking `Safi` in … | ENGINE | 1442 |
| Y520 | §2.7 | Probe 15 settled and reversed the spec's caution: the tooltip's "where it already has power" is not a … | ENGINE | 1444 |
| Y151 | §2.7 | §1.9’s upstream-propagation claim is consistent with probe 15’s reading — one observation on one node, enough to retire the cautionary case and not enough to promote the rule to a measurement. | ENGINE | 1447 |
| Y1174 | §2.7 | §1.9 has since gained the 272-pair save census that bounds the propagation rule from the other side (probe 17). | PROCESS | 1449 |
| Y521 | §2.7 | The §2.4 item 3 link-reversal check is done and passed: a hand-flipped link loaded with zero errors and … | ENGINE | 1451 |
| Y522 | §2.7 | The declaration-order companion question is settled: the engine validates order and logs one error per … | ENGINE | 1454 |
| Y523 | §2.7 | Probe 1 is pass caching: for each of the three passes independently, does flipping a link crash, produce … | DESIGN | 1457 |
| Y524 | §2.7 | Probe 2 is pass 2's content: what imposes its ordering, given that propagation is one hop and cannot chain. | DESIGN | 1458 |
| Y525 | §2.7 | Probe 3 is write windows: where income accumulation sits relative to the value pass, and whether writing … | DESIGN | 1459 |
| Y526 | §2.7 | Probe 4 is negative link values: write one and observe arrow rendering and protect-trade allocation. | DESIGN | 1460 |
| Y527 | §2.7 | Probe 5 is merchant storage: flip a link hosting a steering merchant and see whether the assignment dangles, … | DESIGN | 1461 |
| Y528 | §2.7 | Probe 6 is caravan, twice: does the engine grant it for a merchant assigned to a link that is incoming in … | DESIGN | 1462 |
| Y529 | §2.7 | Probe 7 is render data: is arrow render state separate from the economic link. | DESIGN | 1463 |
| Y530 | §2.7 | Probe 8 is `TRADE_PROPAGATE_THRESHOLD` semantics: set it to 4 and check whether the raw requirement doubles. | DESIGN | 1464 |
| Y531 | §2.7 | Probe 9 is diverted gold: does diverted colonial gold still appear in the per-province production income … | DESIGN | 1465 |
| Y532 | §2.7 | Probe 10 is caller enumeration: disassemble and list every call site of "is X downstream of Y", classified as … | DESIGN | 1466 |
| Y533 | §2.7 | Static string-table analysis already yields three named direction call sites — `DIPLO_SELLPROV_NOT_UPSTREAM`, `TREASURE_FLEET_TOOLTIP_CANT_REACH` and `TRADE_POWER_UPSTREAM` — and no colonisation refusal string exists. | ENGINE | 1466 |
| Y1214 | §2.7 | `$WHO$` in the sell-province strings is the buyer, established by its sibling keys `DIPLO_SELLPROV_ABOVE_TREASURY` ("Price is above $WHO$ treasury") and `_NOPORT_NOCORE` ("cannot be made into a core of $WHO$"). | ENGINE | 1466 |
| Y1215 | §2.7 | Those sell-province keys are all AI-acceptance reasons evaluated on the counterparty. | ENGINE | 1466 |
| Y534 | §2.7 | Probe 11 is the caravan recipient: place a merchant in a coastal node steering toward an inland one, read … | DESIGN | 1467 |
| Y535 | §2.7 | The engine tooltip and the identifier `merchant_steering_to_inland` both read as the inland node, and if that … | ENGINE | 1467 |
| Y1040 | §2.7 | Probe 16 asks whether EU4's 1/1000 quantisation happens in the simulation or in the serialiser, to be settled … | DESIGN | 1469 |
| Y1041 | §2.7 | If the rounding happens in the simulation the engine erases sub-milli-ducat divergence every tick, which is a … | ENGINE | 1472 |
| Y1042 | §2.7 | Probe 16 settles what §2.1 may claim about the engine's own defence and whether the mod should round at its … | DESIGN | 1475 |
| Y1175 | §2.7 | Probe 17 asks whether trade range gates propagated receipt. | DESIGN | 1482 |
| Y1176 | §2.7 | Probe 17's method: observe one near pair and one far pair for the same country, and check whether receipt appears exactly where the upstream node is in trade range. | DESIGN | 1485 |
| Y1216 | §2.7 | Probe 18 is the devastation scaling law: §1.3’s `devastation` row applies `-2 × level/100` on the wiki’s word, the one scaling in that table resting on community documentation. | DESIGN | 1488 |
| Y1217 | §2.7 | Probe 18’s method: read `goods_produced` in the two 1444 devastation windows — Bohemia 50, Erzgebirge and Moravia 20 — and check the penalty scales linearly through them. | DESIGN | 1490 |
| Y536 | §2.7 | All writes land atomically at the tick hook with the sim paused. | DESIGN | 1498 |
| Y537 | §2.8 | Graph-sources on the 1444 field: `cloves` from `the_moluccas` alone (Indonesian); `spices` from `the_moluccas` and `kongo` (Central Africa). | MEASURED | 1504 |
| Y538 | §2.8 | under the calibration `spices` sinks at `doab` and `genua`, and `cloves` moves to `beijing`; the expectation "is met b … | MEASURED | 1504 |
| Y1043 | §2.8 | v6.0 listed Australia, Venice and Deccan among the spice and cloves termini; none of the three holds either … | MEASURED | 1504 |
| Y1119 | §2.8 | The calibration figures moved when §2.3's tie-break cost reached the calibration's own Phase 2 — it was the last solve … | PROCESS | 1504 |
| Y152 | §2.8 | 19.4% (45 of 232) against 7.3% (17 of 232), cited to `round6.py` | MEASURED | 1505 |
| Y540 | §2.8 | Malacca to Cape post-1500: spice routes Malacca to Cape to Europe. | MODEL | 1506 |
| Y541 | §2.8 | Malacca to Cape pre-1500: the corridor is withheld by range and the power-at-both-ends gate, not by direction. | MODEL | 1507 |
| Y542 | §2.8 | A 1000 AD start puts sinks in the Muslim world and Song China, with no era data. | MODEL | 1508 |
| Y153 | §2.8 | On the razed field the result is order-invariant like the baseline: 40 of 40 relabellings return `{genua, … | MEASURED | 1509 |
| Y154 | §2.8 | 32 of 159 (`round6.py`) | MEASURED | 1509 |
| Y155 | §2.8 | `hangzhou`, not `beijing`, is China's wealth pole under §1.3: node wealth 226.7 against 143.0 — ranks 12 and … | MEASURED | 1509 |
| Y156 | §2.8 | Zeroing `beijing` also moves the map — 8 flips — because deleting a percent of world wealth renormalises … | MEASURED | 1509 |
| Y543 | §2.8 | "v4.0 said zeroing `beijing` 'moves nothing'" — the attribution narrowed to one version (and the correction now restat … | PROCESS | 1509 |
| Y544 | §2.8 | Ming losing the Mandate moves nothing on the day it happens, because the Mandate is an owner property and … | MODEL | 1510 |
| Y545 | §2.8 | That row is the owner-agnosticism check, not a responsiveness check. | DESIGN | 1510 |
| Y546 | §2.8 | A major war in China shifts corridors for the duration, reverting as devastation heals. | MODEL | 1511 |
| Y547 | §2.8 | Many poor provinces versus few rich: luxury demand goes to the rich-province node and bulk to the … | MODEL | 1512 |
| Y548 | §2.8 | On a price crash α falls below 1 and regional sinks reappear. | MODEL | 1513 |
| Y549 | §2.8 | Caribbean 1650: sugar production income makes it a sink for cloth, iron and wine. | MODEL | 1514 |
| Y550 | §2.8 | Kilwa 1000: ivory income makes it a sink for Indian textiles. | MODEL | 1515 |
| Y551 | §2.8 | A consuming leaf terminates the DAG of every good it consumes but does not produce. | MODEL | 1516 |
| Y552 | §2.8 | An inert merchant's goods take the even split as if the node were empty, while node-wide bonuses still apply. | MODEL | 1517 |
| Y553 | §2.8 | A node sinking spice but not cloth collects spice fully and cloth at the ratio, with cloth's remainder pushed. | MODEL | 1518 |
| Y554 | §2.8 | A near-balanced link may flip monthly, carries near-zero either way, and assignments survive. | MODEL | 1519 |
| Y555 | §2.8 | A two-way Atlantic corridor has merchants at both ends on disjoint good sets, neither blocking the other. | MODEL | 1520 |
| Y556 | §2.8 | Economy tab versus overlay: every displayed trade figure matches the per-good economy to the ducat, and this … | DESIGN | 1521 |
| Y557 | §2.8 | Stock trade values are not reproducible run to run: two identical vanilla 1444 Castile starts differ on 49 of … | ENGINE | 1521 |
| Y558 | §2.8 | AI merchant placement is randomised at start, and it is the three power-dependent fields that inherit it: … | ENGINE | 1521 |
| Y559 | §2.8 | Any comparison against unmodded numbers needs a tolerance and a null run. | DESIGN | 1521 |
| Y560 | §2.8 | Reachability is asserted every tick: 100% of every good's demand reachable from its supply, zero orphan sinks … | MODEL | 1522 |
| Y561 | §2.8 | Conservation is asserted every good every tick: Phase-4 sum of `unserved` equals sum of `stranded` to machine … | MODEL | 1523 |
| Y562 | §2.8 | Determinism is asserted: re-running a tick reproduces the orientation bit-for-bit, and promotions and … | MODEL | 1524 |
| Y1044 | §2.8 | A new validation row asserts the LP is configured tighter than the tie-break margin: `flowop.LP_OPTS` sets … | MODEL | 1525 |
| Y1045 | §2.8 | assert the option is set, then classify each off-support arc's reduced cost in three branches (halt / report / halt), … | MODEL | 1525 |
| Y1120 | §2.8 | `paper` is today in the genuine-tie state: a zero reduced cost on an arc that carries no flow in any optimum — the rep … | MEASURED | 1525 |
| Y563 | §2.8 | Acyclicity is asserted on every per-good graph, on `Φ_w`, and on the emitted file's declaration order. | DESIGN | 1526 |
| Y564 | §2.8 | Sink-set containment is a hard assertion every tick, unconditionally: every sink inside the 2-core lies in … | MODEL | 1527 |
| Y565 | §2.8 | Asserting containment in `{selected} ∪ {promoted}` alone would halt on T3, which is correct behaviour, so the … | MODEL | 1527 |
| Y566 | §2.8 | Sink-set equality is monitored rather than asserted: it is measured exact on 1444 (29/29 goods, zero … | MEASURED | 1527 |
| Y567 | §2.8 | Where Phase 0 acts the equality does not apply and is not asserted; the check on a peeled edge is the Phase-4 … | MODEL | 1528 |
| Y568 | §2.8 | Colonization check: an observer run to 1600 sees New World colonization proceed at roughly vanilla pace. | MODEL | 1529 |
| Y569 | §2.8 | AI convergence check: greedy assignment settles with damping rather than oscillating. | MODEL | 1530 |
| Y570 | §2.8 | Latent-good check: while latent there is no graph, no value weight and no survival-table entry, and all three … | MEASURED | 1531 |
| Y571 | §2.8 | Cross-implementation check: the DLL and the reference implementation agree on orientation exactly for every … | DESIGN | 1532 |
| Y573 | §2.8 | Flip behaviour is measured per decade in peace versus war, along with whether flips revert as occupation … | MODEL | 1540 |
| Y574 | §2.8 | Propagated-share change per node is measured on each flip alongside the trade-power/in-degree covariance, and … | MODEL | 1541 |
| Y575 | §2.8 | Total propagated power is not the quantity to watch: reorientation cannot change edge count, so the sum of … | MODEL | 1541 |
| Y576 | §2.8 | Income balance is measured on two metrics — total world collected income and its distribution across … | DESIGN | 1542 |
| Y577 | §2.9 | The build is not phases but two tracks run in parallel. | DESIGN | 1546 |
| Y578 | §2.9 | "every define the model reads" is a runtime read, with `TAX_COEFF` the named exception — the one constant in no shippe … | DESIGN | 1548 |
| Y1219 | §2.9 | The `path`/`control` read closes item 1’s remaining gap. | DESIGN | 1548 |
| Y1121 | §2.9 | Each per-tick assertion is paired with a negative fixture that makes it fail, because an assertion nobody has watched … | DESIGN | 1549 |
| Y1122 | §2.9 | Four of the defects the round-5 audit found were checks that could not fail. | PROCESS | 1551 |
| Y1123 | §2.9 | `scripts/redtest6.py` is the reference-side version of the negative-fixture requirement. | PROCESS | 1551 |
| Y579 | §2.9 | Then the b-flow and sweep with their per-tick assertions (reachability, conservation, acyclicity, determinism, 2-core sink containment), the per-tick sink-set equality monitor, per-good eligibility, realized flows, the `Φ_w`-vs-realized disagreement measurement, the reachability census, the flip-rate measurement, and the survival table. | DESIGN | 1552 |
| Y1220 | §2.9 | No implementation yet builds the survival table (§2.2 item 6). | PROCESS | 1552 |
| Y582 | §3.1 | Goal 1, world responsiveness: trade direction follows the world's current state, never authored arrows, so a … | DESIGN | 1564 |
| Y583 | §3.1 | Goal 2, realism: commodities flow differently, and China is a silk source and a spice sink at once — … | DESIGN | 1565 |
| Y584 | §3.1 | Goal 3, preserve the feedback loop: sinks accumulate, fund development and reinforce, which is how mercantile … | DESIGN | 1566 |
| Y585 | §3.1 | Goal 4, represent return flows: export regions historically imported manufactures, and vanilla cannot express … | DESIGN | 1567 |
| Y586 | §3.1 | Goal 5, route-aware direction: direction must reflect where a good can ultimately reach, not which neighbour … | DESIGN | 1568 |
| Y587 | §3.1 | Goal 6: zero authored data. | DESIGN | 1569 |
| Y588 | §3.1 | Goal 7: the game's own numbers are the model's numbers, so anything reading trade income reads the real one. | DESIGN | 1570 |
| Y589 | §3.2 | Two families of orientation fail before this one: the first fails by theorem, the second by an exact rule … | MODEL | 1574 |
| Y590 | §3.2 | Local comparison is monotone: orienting each edge by comparing its endpoints — wealth, `s − c`, or any node … | MODEL | 1578 |
| Y592 | §3.2 | Merchants cannot repair a wrong orientation — a merchant selects among existing outgoing arrows and cannot … | ENGINE | 1585 |
| Y593 | §3.2 | v1's Laplacian sink rule is exactly `(c − s)/deg > mean(neighbour φ) − min(neighbour φ)`, verified on every … | MEASURED | 1589 |
| Y594 | §3.2 | Because supply is sparse where demand is dense, that right-hand side is set by supply geography: spices are … | MEASURED | 1591 |
| Y595 | §3.2 | Under v1's Laplacian, sinks landed where the field was locally flat rather than where demand was: the … | MEASURED | 1595 |
| Y596 | §3.2 | v1 and v2 quantified the asymmetry as "supply contrast 10⁷ against demand contrast 10²–10³", but that ratio … | MODEL | 1598 |
| Y157 | §3.2 | What the ratio metric cannot see is the thing the diagnosis rests on: sparsity — most nodes produce nothing … | MODEL | 1600 |
| Y158 | §3.2 | On the contrast metric itself the demand side is the wider one, not the supply side. | MODEL | 1604 |
| Y597 | §3.2 | No parameter fixes the Laplacian's placement: an α strong enough to matter destroys §1.4's regime split. | MODEL | 1605 |
| Y159 | §3.2 | Better wealth inputs move Genoa to a co-sink at roughly ×1.7 without making demand the determinant of … | MEASURED | 1606 |
| Y160 | §3.2 | Moving the spice sink to a Chinese node takes a multiple of that node's wealth in the region of 3.6–4.8×, … | MEASURED | 1607 |
| Y161 | §3.2 | These are wealth multiples rather than demand multiples: because demand is `wealth^α` normalised over the … | MODEL | 1609 |
| Y162 | §3.2 | The four named Chinese nodes are not the cheapest — `girin` needs 3.89× and `yumen` 4.49×, both inside the … | MEASURED | 1610 |
| Y598 | §3.2 | v2 wrote "1.7× where 4–5× is needed", which compressed two different quantities into one comparison and … | MODEL | 1612 |
| Y599 | §3.2 | The conservation lesson: operators that impose node balance somewhere (the v1 solve, a min-cost flow) serve … | MODEL | 1615 |
| Y600 | §3.2 | DRAIN takes conservation from the b-flow — reachability is LP feasibility on a connected map rather than an … | MODEL | 1615 |
| Y601 | §3.2 | Of the four claims, v1 did state aggregate acyclicity as C061 ("`Φ` is a potential, so orienting edges by it … | PROCESS | 1621 |
| Y163 | §3.2 | Sink placement is a measurement on one input: on 1444, final sinks = `{selected ∩ flow-terminal} ∪ … | MEASURED | 1626 |
| Y164 | §3.2 | v5.0 tried to rescue that equality by attaching two conditions — Phase 0 a no-op and no fallback firing — and … | MODEL | 1628 |
| Y602 | §3.2 | T1, pendant importer: triangle A(+5), B(−3), D(0) with a leaf C(−2) on B; Phase 0 peels C, Phase 4 restores … | MEASURED | 1633 |
| Y603 | §3.2 | T2, free-edge race inside the 2-core: a five-cycle S1(+3)–u1(−3)–w(0)–u2(−2)–S2(+2)–S1 with a chord w–S1, … | MEASURED | 1636 |
| Y604 | §3.2 | T3, the fallback branch inside the 2-core: triangle A, B, C with `b = 0` at all three and node wealth 3, 2, … | MEASURED | 1641 |
| Y605 | §3.2 | What survives unconditionally is the subset direction within the 2-core over the set the sweep maintains: … | MODEL | 1647 |
| Y606 | §3.2 | Pendant net-importers are the only sinks outside that set. | MODEL | 1650 |
| Y607 | §3.2 | §2.8 therefore carries two runtime checks rather than one weakened one: containment inside the 2-core … | DESIGN | 1650 |
| Y608 | §3.2 | On pendant edges the Phase-4 orientation rule is the check and T1 is expected output. | DESIGN | 1653 |
| Y609 | §3.2 | Written as a single assertion with an escape clause, all three counterexamples would disappear into the … | MODEL | 1654 |
| Y610 | §3.2 | Free-edge direction is marking order under the (DEF asc, b asc, index) priority, deterministic by … | MEASURED | 1657 |
| Y611 | §3.2 | Reachability: the orientation contains the LP certificate, so every unit of demand is servable — measured … | MODEL | 1669 |
| Y612 | §3.2 | Aggregate acyclicity: `Φ_w` is itself a DRAIN orientation, so it is acyclic by the same marking-order … | MODEL | 1671 |
| Y613 | §3.2 | `Φ_w`'s marking order is a per-node scalar reproducing the DAG, for any consumer that needs a potential. | MODEL | 1673 |
| Y614 | §3.2 | Conduits still work: a node with `s = c = 0` (the 1444 Cape exactly) carries flow through, with in- and out-degree bot … | MEASURED | 1675 |
| Y1124 | §3.2 | Degree is the weaker evidence for conduit function and was the only kind offered before: an oriented edge is not a rou … | MODEL | 1676 |
| Y1125 | §3.2 | On the certificate flow itself the Cape has both incoming and outgoing flow on 28 of 29 goods; the exception is `paper … | MEASURED | 1678 |
| Y615 | §3.2 | The corridor runs through the Cape, which is the short route to Atlantic Europe: Malacca reaches the Channel … | MEASURED | 1680 |
| Y616 | §3.2 | Peripheral termini still exist — the LP's branch ends are consumed at the end of the line — and value only … | MODEL | 1684 |
| Y617 | §3.3 | Demand is purchasing power, and under §1.3 purchasing power is what the place is worth per year. | DESIGN | 1689 |
| Y619 | §3.3 | The return-flow effect is real but modest at vanilla prices: sugar (3.0), cocoa (4.0) and coffee (3.0) are … | ENGINE | 1689 |
| Y620 | §3.3 | v1 and v2 said "negligible development but large production income", which overstated the gap. | MODEL | 1689 |
| Y621 | §3.3 | There is no colonial-nation dependency, no timeline restriction and no owner dependency. | MODEL | 1689 |
| Y618 | §3.3 | Wealth captures return flows for free: a sugar island’s production term is carried by its trade good rather than by its development, so it becomes a genuine consumer of cloth and iron. | MODEL | 1689 |
| Y622 | §3.3 | Wealth is chosen for what the place is rather than who runs it: autonomy drift, national ideas, government … | MODEL | 1691 |
| Y623 | §3.3 | What remains still moves deliberately: development changes, trade goods change, prices move with events, and … | MODEL | 1691 |
| Y624 | §3.3 | A besieged province genuinely produces less, so that volatility is economics rather than noise, and a trade … | DESIGN | 1691 |
| Y625 | §3.3 | What the model removes is the volatility that was really about ownership: a province no longer changes what … | MODEL | 1691 |
| Y626 | §3.3 | The instruction is to plan around the world rather than around the graph: the map is legible, not unchanging. | DESIGN | 1691 |
| Y627 | §3.3 | Trade income is excluded for circularity rather than speed: including it would close a … | MODEL | 1693 |
| Y628 | §3.3 | The loop still closes the long way: trade income funds development, and development raises tax and production … | MODEL | 1693 |
| Y165 | §3.3 | `cape_of_good_hope`'s `members` list has 20 entries but province 1460 is a sea zone, listed in … | ENGINE | 1695 |
| Y629 | §3.3 | Node sizes run from 19 land provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread with no structural … | ENGINE | 1695 |
| Y630 | §3.3 | Raising a node's aggregate wealth to a power rewards node size, so luxuries would drain toward whichever node … | MODEL | 1699 |
| Y1221 | §3.3 | The shipped `α(g)` puts `cloves` — base price 8.0, live at 1444 — at the ceiling `α_max = 3.0`, exponent 2.0. | MEASURED | 1707 |
| Y1222 | §3.3 | At that ceiling exponent the same two comparisons read `(77/19)² ≈ 16.4×` and `(68/33)² ≈ 4.25×`. | MEASURED | 1708 |
| Y631 | §3.3 | The distortion is measured against the per-province form the model defines rather than against equal totals: node-level α overweights a k-province node by `k^(α−1)` at fixed per-province wealth, giving ≈2× and ≈1.44× at `α(g) = 1.5` and 4.1× and 2.1× at the installed `α_Φ = 2.0`, so the slicing distortion the per-province form avoids is largest on the price-clamped goods, with the aggregate sitting between the worked per-good example and the clamp ceiling. | MODEL | 1709 |
| Y632 | §3.3 | v2 said a 77-province node "beats a 19-province node of equal total wealth by 2×"; at equal totals the … | MODEL | 1711 |
| Y633 | §3.3 | With the exponent inside the sum, superlinear demand concentrates where individual provinces are rich, and at … | MODEL | 1714 |
| Y634 | §3.4 | Production efficiency does not conjure more cloves; it means the owner extracts more ducats from the same … | MODEL | 1720 |
| Y635 | §3.4 | Owner effects do not belong in demand either: v1 and v2 excluded them from supply and then let them back in … | MODEL | 1722 |
| Y636 | §3.4 | Supply and demand are both properties of the place, so the supply-side argument applies unchanged and with … | DESIGN | 1722 |
| Y166 | §3.4 | In v1 substituting production income also measurably broke the α = 1 identity, with orientation agreement … | MEASURED | 1728 |
| Y638 | §3.5 | Anchoring at 2 ducats rather than the price median means a good's market concentration moves only when its … | MODEL | 1734 |
| Y639 | §3.5 | Under a median anchor a good could concentrate because some unrelated commodity got expensive — noise dressed … | MODEL | 1734 |
| Y640 | §3.5 | At vanilla base prices nothing sits below the 2.0 anchor: the minimum tradeable base price is exactly 2.0, … | ENGINE | 1736 |
| Y641 | §3.5 | Grain is 2.5, not the 1.25 v1 recorded; both of v1's figures were price/P₀ misread as prices. | ENGINE | 1738 |
| Y642 | §3.5 | The sublinear regime is entered only when a price event pushes a good beneath the anchor, and the shipped … | ENGINE | 1739 |
| Y167 | §3.5 | `change_price` values are fractions of the good's base price rather than ducats, and the shipped save … | ENGINE | 1745 |
| Y168 | §3.5 | The install carries 161 textual `change_price` blocks — 93 in `events/`, 14 in `missions/`, 1 in `common/`, … | ENGINE | 1751 |
| Y169 | §3.5 | Ten of the 161 never execute — four inside `effect_tooltip = "…"` strings, three inside the `effect = "…"` … | ENGINE | 1753 |
| Y170 | §3.5 | Six of the seven quoted blocks duplicate a block already counted in `events/` and the seventh names a price … | ENGINE | 1756 |
| Y171 | §3.5 | v4.0 said 154 by silently dropping the quoted seven and v5.0 said 161 by counting them; both were wrong about … | PROCESS | 1759 |
| Y172 | §3.5 | v5.0 claimed the scan was "guarded by a per-file count assertion", and there was no assertion anywhere in its … | MODEL | 1760 |
| Y173 | §3.5 | `verify6.py` checks the census total and its `events/` component against computed values, carrying the rest of the by-tree breakdown only as a literal-string presence check, and `measure6.py`’s walker still swallows parse failures with `except Exception: pass`. | PROCESS | 1762 |
| Y174 | §3.5 | The reason a plain parse misses the quoted blocks is mechanical: `pdx.py` tokenises a quoted string as one … | MODEL | 1764 |
| Y643 | §3.5 | The history route matters: `wool`'s largest single negative is `NEW_DRAPERIES` at −0.25 in the history file, … | ENGINE | 1768 |
| Y175 | §3.5 | 1.875 is the single-key floor rather than the campaign figure: the same `1540.1.1` block also applies … | ENGINE | 1770 |
| Y176 | §3.5 | The partition needs the history value: `events/PriceChanges.txt`'s −0.20 for the same key would alone floor … | ENGINE | 1773 |
| Y644 | §3.5 | v2's 13 was right, and v3.0 reached 12 by parsing four of the five trees. | PROCESS | 1776 |
| Y645 | §3.5 | The point of having the sublinear regime is that without it a crash could only fail to concentrate a market, … | DESIGN | 1777 |
| Y646 | §3.5 | α is deliberately mild: production geography is what differentiates goods and α expresses only how … | DESIGN | 1781 |
| Y647 | §3.6 | A margin on orientation is a correctness bug rather than a tuning knob: holding an edge against the current … | MODEL | 1785 |
| Y648 | §3.6 | Tested in v1: with tol = 1e-3 and values {0, 0.0006, 0.0012}, tolerance-based tie-breaking turned an acyclic … | MEASURED | 1787 |
| Y649 | §3.6 | The node-file format represents cycles perfectly well — it is a list of named directed links with no … | ENGINE | 1789 |
| Y650 | §3.6 | What the design depends on is the engine's behaviour on a cyclic file, and that is now measured rather than … | ENGINE | 1790 |
| Y651 | §3.6 | A hand-authored two-node cycle produced `EXCEPTION_STACK_OVERFLOW` at a single exception address under 1002 … | ENGINE | 1792 |
| Y653 | §3.6 | Acyclicity is enforced because of what the engine does on a cycle: it demonstrably did not survive the cycle class tested — established by observation over one construction (§2.4), not by proof over all cyclic inputs. | DESIGN | 1795 |
| Y654 | §3.6 | Nothing needs to stop churn: a link whose flow-support membership alternates month to month carries … | MODEL | 1799 |
| Y655 | §3.6 | The "carries near-nothing" half is measured rather than derived, because v1's continuity argument (a … | MODEL | 1801 |
| Y656 | §3.6 | Measured on 1444: across 29 goods × 6 random 1e-9 demand nudges, zero support-membership changes moved more … | MEASURED | 1803 |
| Y657 | §3.6 | At exactly degenerate inputs — two equal-hop corridors — the map from `b` to the chosen support is … | MODEL | 1805 |
| Y1046 | §3.6 | With both cost terms and the solver's optimality tolerance pinned, the optimum is unique on the aggregate and … | MEASURED | 1807 |
| Y1126 | §3.6 | The uniqueness margin is not a constant of the design, and how much of it is a gift of the chosen `α_Φ` is worth knowi … | DESIGN | 1810 |
| Y1127 | §3.6 | On the aggregate the margin is 7.53e-06 at `α_Φ` = 2.0 and 1.267e-07 at 1.5 — a factor of sixty for a change §1.6 trea … | MEASURED | 1811 |
| Y1128 | §3.6 | Per good, two of the 29 solves sit inside HiGHS's 1e-7 default — `copper` at 3.765e-08 and `paper` at 8.92e-08 — and 2 … | MEASURED | 1813 |
| Y1129 | §3.6 | `round6.py` reports the margin as the smallest positive reduced cost on an arc outside the support. | MODEL | 1814 |
| Y1130 | §3.6 | Pinning the tolerance is load-bearing at these values rather than precautionary; a future change to `α_Φ` or to the we … | DESIGN | 1815 |
| Y1047 | §3.6 | The discontinuity remains a property of the program: an input that made two routings exactly equal in cost … | MODEL | 1817 |
| Y658 | §3.6 | v1's ε is deleted because the problem it patched no longer exists: the Laplacian oriented dead branches by … | MODEL | 1820 |
| Y659 | §3.6 | DRAIN's free edges are oriented combinatorially: the priority sweep's key (DEF, b, index) is computed from … | MODEL | 1823 |
| Y660 | §3.6 | The measured count of exact key ties on 1444 data is zero, and the LP itself is deterministic (six identical … | MEASURED | 1826 |
| Y661 | §3.6 | Determinism is asserted per tick rather than approximated by a nudge. | DESIGN | 1828 |
| Y662 | §3.6 | What replaces the ε-magnitude question in §3.13 is the cross-machine question, which §2.1 narrows. | DESIGN | 1828 |
| Y1048 | §3.6 | The LP does not need to pivot identically, only to reach the same optimum, which the tie-break's margin makes … | MODEL | 1829 |
| Y663 | §3.7 | Vanilla's rule is that effective trade power counts only countries which collect or transfer downstream, and … | ENGINE | 1835 |
| Y664 | §3.7 | Under a per-good model "downstream" is per good, so at a node where your home is downstream for cloth and … | MODEL | 1837 |
| Y666 | §3.7 | Forcing eligibility true for all goods at once would be "direction doesn't exist" rather than "everyone is … | MODEL | 1837 |
| Y665 | §3.7 | Per-good eligibility returns true for some goods at every node, so no node is globally inert, while still preventing a nation’s power from shoving a good away from where it collects that good. | MODEL | 1837 |
| Y1223 | §3.7 | Measured on the 1444 field, every node holds an out-arc for at least 18 of the 29 goods. | MEASURED | 1837 |
| Y667 | §3.7 | The misstatement that any non-collecting country with trade power is transferring is wrong. | ENGINE | 1839 |
| Y1177 | §3.7 | The save's own ledger shows the engine distinguishing collecting from non-collecting trade power. | ENGINE | 1839 |
| Y1178 | §3.7 | At `sevilla`, `pull_power` 17.642 is exactly FRA 3.319 + ARA 14.323. | MEASURED | 1839 |
| Y1179 | §3.7 | At `venice`, 15.199 of non-collector power carries no `pull_power` at all. | MEASURED | 1839 |
| Y668 | §3.8 | The vanilla gates encode an assumption that a nation pair has one global relationship to trade, upstream or … | MODEL | 1843 |
| Y669 | §3.8 | Every province is upstream for some good, because a region that receives your cloth ships you its furs. | MODEL | 1843 |
| Y670 | §3.8 | There is no fact of the matter for the gate to test, so the honest fix is to stop consulting it rather than … | DESIGN | 1843 |
| Y671 | §3.8 | Node-pair dependencies are different and keep reading `Φ_w`, because propagation is a relation between two … | MODEL | 1845 |
| Y672 | §3.8 | That distinction is easy to miss and expensive to get wrong. | DESIGN | 1845 |
| Y673 | §3.8 | Propagate Religion is node-local — it establishes a centre of conversion in the node's own province — but … | ENGINE | 1847 |
| Y674 | §3.8 | The shipped policy file gates Propagate Religion on the trade share and the node being in a trade company … | ENGINE | 1850 |
| Y675 | §3.8 | No trading policy anywhere in `00_trading_policies.txt` tests upstream/downstream. | ENGINE | 1852 |
| Y676 | §3.8 | Three of the five trading policies have no trade-share threshold at all — merchant-present only. | ENGINE | 1854 |
| Y677 | §3.8 | This is written down because the deferred artifact does not exist yet, and a community restatement of the … | DESIGN | 1855 |
| Y678 | §3.8 | Scopes read `Φ_w` rather than any-good reachability, because a gate is a boolean while a scope is a set or a … | DESIGN | 1859 |
| Y679 | §3.8 | `Φ_w` is the graph the engine already walks, so those call sites are left alone, which collapses the … | ENGINE | 1859 |
| Y680 | §3.8 | Reading `Φ_w` for scopes is legible — one map predicts where fleets sail — and balanced, because area-effect … | DESIGN | 1859 |
| Y681 | §3.8 | Any-good connectivity on 1444 data under DRAIN is 90.6% (5,723 of 6,320) of ordered node pairs, and v2's … | MEASURED | 1859 |
| Y682 | §3.9 | The installed graph exists for the engine's direction-dependent systems — propagation, fleet routes, … | DESIGN | 1863 |
| Y177 | §3.9 | On this field `english_channel` is the richest node at 316.6 and is not a sink — it drains to `genua`, 4th at … | MEASURED | 1869 |
| Y1224 | §3.9 | `mexico`, `gulf_of_siam` and `sevilla` are not ends for two different reasons, which the flow separates. | MODEL | 1871 |
| Y1131 | §3.9 | A node can draw more edges in than it sends out and still be a thoroughfare; the quantity that separates a net demander from an end is not a degree comparison. | MODEL | 1872 |
| Y1225 | §3.9 | What separates a node from an end is not flow carriage either. | MODEL | 1873 |
| Y1132 | §3.9 | The flow identity the LP enforces is `flow_in(n) − flow_out(n) = −b_w(n)`. | MODEL | 1874 |
| Y1133 | §3.9 | The identity holds on all 36 net demanders and on all 80 nodes, to a maximum residual of 5.2e-17. | MEASURED | 1875 |
| Y1134 | §3.9 | Every net demander absorbs exactly its own deficit and passes the rest on; an end is a node the whole orientation gives no out-arc — no flow arc and no free edge. | MODEL | 1876 |
| Y1226 | §3.9 | `sevilla` passes 0.0201 of the 0.0324 it receives. | MEASURED | 1876 |
| Y1227 | §3.9 | For `mexico` and `gulf_of_siam` the rest is exactly zero — flow_out 0 — making them two of the 18 of 80 nodes with out-degree above zero and no outgoing flow at all. | MEASURED | 1877 |
| Y1135 | §3.9 | 18 of 80 nodes have out-degree above zero while carrying no outgoing flow at all. | MEASURED | 1878 |
| Y1228 | §3.9 | `mexico` and `gulf_of_siam` are still not ends, because each keeps a single free out-edge. | MEASURED | 1879 |
| Y1229 | §3.9 | Carrying flow out is not necessary for non-endhood. | MODEL | 1880 |
| Y1230 | §3.9 | The flow arcs terminate where the identity sends them, and the free edges are Phase 3’s completion. | MODEL | 1882 |
| Y685 | §3.9 | Wealth pulls but the wealthiest node is not automatically an end: what makes an end is that no arc of either kind leaves, a property of the whole field and the graph rather than of a single node’s rank, and the ends emerge and move when the wealth moves. | MODEL | 1883 |
| Y686 | §3.9 | `Φ_w` reuses the §1.1 operator unchanged: one implementation, one set of guarantees (LP feasibility, … | DESIGN | 1886 |
| Y687 | §3.9 | "Two aggregates were tested and rejected before the third was adopted" | MODEL | 1891 |
| Y688 | §3.9 | The value-weighted net flow (the sum over goods of `V_g · net_g`) is a flow, flows circulate, and it … | MODEL | 1893 |
| Y178 | §3.9 | the ends are "a function of the order Phase 3 pops its ready queue, which is a design choice inside the operator" — no … | MODEL | 1895 |
| Y689 | §3.9 | acyclic for free only; the self-coherence comparison is no longer made anywhere in the document | MODEL | 1895 |
| Y180 | §3.9 | "That follows from the definition and needs no measurement" (§3.15: "The rejection is structural, so no figure is kept … | DESIGN | 1897 |
| Y690 | §3.9 | `Φ_w` is adopted for one operator, one set of guarantees, and ends that move with the world: reusing §1.1 … | DESIGN | 1898 |
| Y181 | §3.9 | v2.1 through v4.0's "two vanilla-like ends at 1444" justification is withdrawn and must not be revived even … | MODEL | 1901 |
| Y182 | §3.9 | only the buys half — "What it buys is one operator, one set of guarantees, and ends that sit where the wealth is" | DESIGN | 1905 |
| Y691 | §3.9 | A difference in `Φ_w` across a link is not the net value crossing it. | MODEL | 1908 |
| Y692 | §3.9 | Realized movement follows vanilla propagation — a good can be diluted by an even split across three links … | MODEL | 1909 |
| Y694 | §3.9 | Link values are realized flows, which makes conservation hold by construction. | MODEL | 1914 |
| Y695 | §3.10 | Paying countries correctly while leaving the display wrong is a strictly weaker position: node values, pie charts and the ledger would describe an economy nobody is playing, and those figures have readers. | ENGINE | 1919 |
| Y1231 | §3.10 | Income-threshold content reads trade income in shipped files — `trade_income_percentage` in the church-aspect, decree and estate files. | ENGINE | 1919 |
| Y1233 | §3.10 | The defines expose light-ship constants — cost, maintenance, time, sailors, combat width — but no rule tying the build decision to node value. | ENGINE | 1919 |
| Y1232 | §3.10 | AI light-ship building and trade-league behaviour are engine-internal readers. | ENGINE | 1919 |
| Y1234 | §3.10 | No §2.7 probe enumerates node-value readers — item 10 enumerates direction-gate call sites, a different question — so the enumeration that would settle those two readers is named here as missing. | PROCESS | 1919 |
| Y1253 | §3.10 | Peace valuation reads node value through shipped defines. | ENGINE | 1919 |
| Y1254 | §3.10 | `PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.1`, its comment stating the rule — "AI desire for transfering trade power is multiplied by this for each 0.1 trade value in shared nodes". | ENGINE | 1919 |
| Y1255 | §3.10 | `PEACE_TERMS_TRADE_POWER_VALUE_MAX = 2.0` and `PEACE_TERMS_TRADE_POWER_NO_TRADE_INTEREST_MULT = 0` sit alongside it. | ENGINE | 1919 |
| Y696 | §3.10 | The engine's data model is sufficient at node level for a narrower reason than it first appears: … | MODEL | 1921 |
| Y697 | §3.10 | What factors out is `powershare_C`, a country's share among collectors, and whether a country collects is a … | MODEL | 1921 |
| Y698 | §3.10 | `income_C(n)` = the sum over goods of `value_g(n) · collected_share(n,g) · powershare_C(n)` = … | MODEL | 1924 |
| Y699 | §3.10 | That is an identity rather than a measurement: `powershare_C(n)` carries no `g`, so it factors out of the … | MODEL | 1927 |
| Y700 | §3.10 | Every term that feeds a collector's power at a node is node-wide — the merchant bonus, the off-home penalty, … | MODEL | 1927 |
| Y701 | §3.10 | One scalar per node reproduces every country's income exactly, and the engine's own math does the rest. | MODEL | 1927 |
| Y702 | §3.10 | v1 through v3.0 quoted floating-point residuals of the income identity — 5.7e-14 here and 1.4e-14 below — produced by constructions none of those documents states, while v4.0 quoted its own 1.3e-16 on a construction it does state. | PROCESS | 1928 |
| Y1136 | §3.10 | No residual is quoted for the doubles check: a floating-point residual of an exact identity measures the arithmetic, n … | DESIGN | 1928 |
| Y1180 | §3.10 | v4.0 quoted its own 1.3e-16 on a construction it does state: `gulf_of_siam`, thirteen goods carrying local value, per-good eligibility, and the off-home penalty on two of the three collectors. | PROCESS | 1928 |
| Y184 | §3.10 | Propagation is kept on a single graph, and the reason is not the one v1 through v6.0's own first draft gave. | DESIGN | 1930 |
| Y185 | §3.10 | "the identity holds by construction." — the doubles residual clause deleted with the withdrawn measurement | MODEL | 1930 |
| Y186 | §3.10 | `gulf_of_siam`'s 29 goods leave it by seven distinct downstream sets. | MEASURED | 1930 |
| Y187 | §3.10 | Per-good propagation does not break the income identity: defining `ps̄_C` as the per-good shares weighted by … | MODEL | 1930 |
| Y188 | §3.10 | Both inputs to `ps̄_C` already exist per good at write time, and §2.6 sums exactly them into `collect_pool`. | MODEL | 1930 |
| Y189 | §3.10 | The real cost is that `ps̄_C` is not derivable from trade power alone: it is value-weighted, so installing it … | MODEL | 1932 |
| Y190 | §3.10 | That is a claim about what the engine exposes rather than about a magnitude, and it is why the single graph … | DESIGN | 1932 |
| Y191 | §3.10 | Every magnitude previous versions quoted here — v1 through v3.0's "off by 5.96 ducats on a node paying ~250" … | PROCESS | 1932 |
| Y192 | §3.10 | No figure of the author's own is quoted here, because the identity holds and the objection is structural, and … | DESIGN | 1932 |
| Y703 | §3.10 | Only the decomposition by good exceeds what the engine can hold. | ENGINE | 1934 |
| Y704 | §3.11 | In vanilla, steering is outgoing-only: trade cannot be steered upstream at any amount of power, per the … | ENGINE | 1938 |
| Y705 | §3.11 | The display is not outgoing-only: the node window already lists incoming links as clickable entries. | ENGINE | 1940 |
| Y706 | §3.11 | Because only outgoing links can be steered, "assigned" and "steering" are the same condition in vanilla and … | ENGINE | 1941 |
| Y707 | §3.11 | §1.7 makes incoming entries assignable and pulls "assigned" and "steering" apart. | DESIGN | 1944 |
| Y708 | §3.11 | The engine’s caravan grant fires on `merchant_present_inland` or `merchant_steering_to_inland`, with nothing checking whether value moves — an absence-of-strings finding rather than a proof of the engine’s internal logic, with §2.7 item 6 named as what would settle it. | ENGINE | 1945 |
| Y1181 | §3.11 | Both caravan trigger strings are verbatim in the binary's string table, and no third exists near them. | ENGINE | 1946 |
| Y1182 | §3.11 | §2.7 item 6 is the probe that settles whether the engine checks that value moves. | DESIGN | 1947 |
| Y709 | §3.11 | The caravan tooltip reads as granting the bonus in the inland node ("steers towards an inland trade node will … | ENGINE | 1948 |
| Y710 | §3.11 | §2.7 item 11 settles the recipient with one merchant and two node windows, and the exposure surface is either … | DESIGN | 1950 |
| Y711 | §3.11 | §1.7's added condition is the right guard under both readings. | DESIGN | 1953 |
| Y712 | §3.11 | Caravan power is total country development divided by 3 plus policy and idea modifiers, clamped to [2, 50]. | ENGINE | 1953 |
| Y713 | §3.11 | Nineteen countries are at the caravan cap from raw 1444 development alone, and Burgundy, Korea, the Timurids … | MEASURED | 1954 |
| Y714 | §3.11 | Caravan power does not scale with node presence at all. | ENGINE | 1956 |
| Y715 | §3.11 | Requiring the merchant to steer something restores the vanilla state of affairs, and granting on bare … | DESIGN | 1958 |
| Y716 | §3.12 | The argument is consistency with §3.8: the gate compares two trade capitals on a graph where the nation-pair … | DESIGN | 1963 |
| Y717 | §3.12 | v1 claimed a stronger argument — that the gate is bistable, denial raising the colonial node's wealth and … | MODEL | 1964 |
| Y718 | §3.12 | That bistability argument is deleted: gold income never enters `wealth` at all, so neither granting nor … | MODEL | 1966 |
| Y719 | §3.12 | The engine's own denial branch confirms what denial does: "They will keep their gold income instead." | ENGINE | 1968 |
| Y720 | §3.12 | A slow second-order version survives — kept gold spent on development raises `base_tax` and `base_production` … | DESIGN | 1969 |
| Y721 | §3.12 | Gold receipts inflate, and the files state an income-relative normalisation only for peace gold, so the small-economy exposure of universal granting is the observed direction rather than a file-stated law. | ENGINE | 1974 |
| Y722 | §3.12 | The route rule is a balance dial, since privateers skim per node passed, which is why hop counts are compared … | DESIGN | 1974 |
| Y1183 | §3.12 | `GOLD_INFLATION` and `TREASURE_FLEET_INFLATION` are both flat 0.5. | ENGINE | 1974 |
| Y1184 | §3.12 | The files state an income-relative normalisation only for peace gold — `INFLATION_FROM_PEACE_GOLD`, per month of income. | ENGINE | 1974 |
| Y723 | §3.13 | Prose-sourced questions are to be distrusted and nothing built on them. | DESIGN | 1978 |
| Y724 | §3.13 | Colonization's gate shape rests on one mod author's report, contradicted in-thread, and the observed … | MODEL | 1980 |
| Y725 | §3.13 | Static string-table analysis leans the same way: the only direction-refusal strings in the binary belong to … | ENGINE | 1980 |
| Y726 | §3.13 | The caller enumeration must be able to return "no colonization gate exists" as a successful result. | DESIGN | 1980 |
| Y727 | §3.13 | Derived questions are probably right and cheaply falsifiable. | DESIGN | 1982 |
| Y728 | §3.13 | The `TRADE_PROPAGATE_THRESHOLD` file value and the documented raw requirement differ by exactly the … | ENGINE | 1984 |
| Y729 | §3.13 | Propagation is one hop and cannot chain, so something else in pass 2 imposes its ordering; eligibility … | ENGINE | 1985 |
| Y730 | §3.13 | The debugger-only list is shorter than v1 believed: of §2.7, only pass caching, pass-2 content, write windows … | DESIGN | 1987 |
| Y731 | §3.13 | Items 11–15 need a save, a tooltip, or one file edit, and the propagation-threshold and one-hop questions are … | DESIGN | 1988 |
| Y732 | §3.13 | Of the three cheapest probes, the cyclic file changed what this spec says, the incoming-link button confirmed it, and the caravan recipient is pending, with §3.11 turning on it. | DESIGN | 1990 |
| Y733 | §3.13 | One question is open in the v6.0 wealth model, and it is a question rather than a number, because §1.3 … | DESIGN | 1994 |
| Y193 | §3.13 | The one open wealth question is now a design question rather than a classification one: should any source … | DESIGN | 1996 |
| Y195 | §3.13 | The keys `trade_goods_size` and `trade_goods_size_modifier` are granted in many places: buildings, event … | ENGINE | 1999 |
| Y194 | §3.13 | v3.0 through v5.0 tried to admit the province-scoped subset by rule, and that rule was wrong in both … | MODEL | 2002 |
| Y196 | §3.13 | Re-admitting any of those sources re-admits the maintenance burden with it, and the question to settle first … | DESIGN | 2004 |
| Y734 | §3.13 | Settled and moved: `local_production_efficiency` from a trade good is outside wealth, because Barcelona’s production tooltip read `Production Efficiency: +12.0% / From Technology: +2.0% / Producing Glass: +10.0%`, so the engine books glass’s +10% on production income, which wealth does not compute. | ENGINE | 2009 |
| Y1235 | §3.13 | Both halves of the settled-and-moved note rest on recorded tooltip observations, with the standing §1.3’s observation note gives such readings. | PROCESS | 2009 |
| Y735 | §3.13 | Settled and moved: `TAX_COEFF` is 1.0 across the development range — `Base: 0.49 (Yearly 6.00)` at `base_tax` … | ENGINE | 2013 |
| Y736 | §3.13 | `k`, `α_min` and `α_max` remain unresolved; the test is whether they produce the intended three-regime split, … | DESIGN | 2019 |
| Y737 | §3.13 | CLOSED — the hazard is not reachable from inside the model (no scale knob exists; see Y1137-Y1138), and the entry is k … | MODEL | 2020 |
| Y1137 | §3.13 | `b_w` is built with `s_w(n) = 1/N` uniform against a `c_w` that sums to 1, so its largest magnitude cannot fall below … | MODEL | 2023 |
| Y1138 | §3.13 | The 1e-11 threshold is `flowop.ZERO_TOL`, a post-solve classification constant the implementation may set to anything; … | MODEL | 2026 |
| Y1139 | §3.13 | The solver's feasibility tolerances (`flowop.LP_OPTS`) bottom out at HiGHS's 1e-10: below that the option is rejected … | MODEL | 2029 |
| Y1140 | §3.13 | The silent revert to the 1e-7 default is measured rather than inferred, on `copper`: an unset tolerance and 1e-7 produce identical flips — the count seed-dependent, `round6.py`’s fixed permutation set showing 8 — and a rejected 1e-11 reproduces the default’s flips exactly. | MEASURED | 2034 |
| Y738 | §3.13 | Whether `α_min` ever bites is now bounded from files: the sublinear regime is reachable through vanilla price events for 13 of 30 goods, exactly on the boundary for 2, and unreachable for 15; whether those events fire often enough in a real campaign remains the open half. | ENGINE | 2040 |
| Y1236 | §3.13 | Of the goods for which the sublinear regime is unreachable, 11 have no negative price event at all and 4 have a largest negative that stops above the anchor. | MEASURED | 2041 |
| Y739 | §3.13 | it tracks price "more closely than the baseline does"; only the configuration is recorded (α unclamped at exponent 2, … | MEASURED | 2044 |
| Y1141 | §3.13 | No span, correlation or reach figure is quoted for the calibration option: it is not adopted, its numbers move with ev … | DESIGN | 2047 |
| Y740 | §3.13 | Unclamped α-squared is a demand-model decision, because luxuries become court goods. | DESIGN | 2051 |
| Y197 | §3.13 | the sink lands on a high-demand node rather than a geographic accident; the demand-order triple is withdrawn | MEASURED | 2052 |
| Y741 | §3.13 | it "re-routes arcs carrying a small fraction of a good's mass, and it costs one good full reach"; all three figures wi … | MEASURED | 2053 |
| Y198 | §3.13 | v2 said Beijing "holds the richest single province", which it does not — that is `hangzhou` — and no … | PROCESS | 2055 |
| Y742 | §3.13 | The baseline does not adopt the calibration, and adopting it is a §1.4 decision rather than a solver knob. | DESIGN | 2055 |
| Y743 | §3.13 | The open multiplayer item is build discipline rather than LP pivot determinism, which §2.1 retires. | DESIGN | 2058 |
| Y1049 | §3.13 | What is open is whether the shipped solver build does runtime CPU dispatch or threads its reductions — either … | MODEL | 2060 |
| Y1050 | §3.13 | Also open is whether the DLL reproduces the reference implementation's orientation exactly, which cannot be … | DESIGN | 2062 |
| Y744 | §3.13 | AI merchant reassignment cadence is open. | DESIGN | 2064 |
| Y745 | §3.14 | The two ends of a link never compete: a merchant at `n` on {n,m} moves goods oriented n to m, one at `m` … | MODEL | 2068 |
| Y746 | §3.14 | One precompute serves every country: for each good, a backward pass over its DAG gives `S_g[n][H]`, the … | MODEL | 2070 |
| Y747 | §3.14 | `collected_share(n,g)` reaches 1 at `g`'s sink, which terminates the recursion. | MODEL | 2070 |
| Y748 | §3.14 | All three survival-table inputs are country-independent aggregates, so this is one table rather than one per … | MODEL | 2070 |
| Y749 | §3.14 | v1 and v2 both said 0.75 MB, which is the single-precision figure; the rest of the solver is double precision — 29 goods × 80 × 80 entries at 8 bytes is 1,484,800 bytes — so the natural implementation is twice what v1 and v2 recorded. | MODEL | 2070 |
| Y750 | §3.14 | Scoring reads the survival table for both steering and collecting, so the opportunity cost of collecting … | MODEL | 2072 |
| Y751 | §3.14 | The off-home penalty is a power modifier rather than a haircut on value: it reduces the country's trade power … | ENGINE | 2074 |
| Y752 | §3.14 | Scoring a collect candidate as value × share × 0.5 is wrong; the halving must be applied to power and the … | MODEL | 2074 |
| Y753 | §3.14 | That is also why the off-home penalty falls out of the survival table at all: the table is built from … | MODEL | 2074 |
| Y754 | §3.14 | The home-node bonus is voided entirely by placing any collector outside the home node, so a collect … | ENGINE | 2076 |
| Y755 | §3.14 | Greedy scoring against a moving field can oscillate between AIs; damping the shares between passes should … | MODEL | 2076 |
| Y756 | §3.14 | Reassignment cadence is undecided and is the one item left for the human, because merchants take travel time … | DESIGN | 2078 |
| Y757 | §3.14 | Mirroring vanilla's cadence is the stated preference, but the relevant define was not located in the visible … | DESIGN | 2080 |
| Y758 | §3.14 | The computed alternative moves a merchant when `(V_new − V_incumbent) × expected_tenure > V_incumbent × … | MODEL | 2081 |
| Y759 | §3.14 | The argument for computing the cadence is that vanilla's cadence was tuned against a graph that never moves, … | DESIGN | 2083 |
| Y760 | §3.15 | The v1 Laplacian potential as the orientation core is rejected: its sink placement is topological, sinks … | MODEL | 2087 |
| Y200 | §3.15 | v3.0 and v4.0 repeated the 10⁷ versus 10²–10³ ratio in this entry while v4.0's own §3.2 was withdrawing it. | PROCESS | 2091 |
| Y199 | §3.15 | The Laplacian entry maintains no copy of the contrast measurement — §3.2 carries it — and with v1's ε floor … | MODEL | 2093 |
| Y201 | §3.15 | `cloves` has a single producer and so no contrast to measure at all, which is the sparsity point in miniature. | MODEL | 2094 |
| Y761 | §3.15 | The Laplacian was diagnosed, measured and replaced, and what it did guarantee — 100% reachability via … | MODEL | 2096 |
| Y762 | §3.15 | Pure min-cost-flow orientation with no sweep is rejected: it orients only the roughly 79-edge support (a … | MEASURED | 2100 |
| Y202 | §3.15 | Ranked orientation wins the sink-demand alignment statistics — a far higher share of top-demand nodes in its … | MODEL | 2104 |
| Y203 | §3.15 | Seeded basin growth converges flow to the chosen seeds and starves everything off a supply-to-seed path, … | MODEL | 2113 |
| Y763 | §3.15 | Seeded basin growth's useful ideas — HHI-adaptive sink count and stall self-correction — survive inside … | MODEL | 2115 |
| Y764 | §3.15 | DEF-descending free-edge priority is rejected as measurably worse: on the certificate, unmet demand is … | MODEL | 2119 |
| Y765 | §3.15 | Authored demand weights are rejected: authored data in a model that needs none. | DESIGN | 2124 |
| Y766 | §3.15 | Trade income inside `wealth` is rejected: it reintroduces flow-demand-orientation-flow circularity, and the … | MODEL | 2126 |
| Y767 | §3.15 | Node-level α is rejected: it makes demand concentration a function of how finely the map was sliced. | MODEL | 2128 |
| Y768 | §3.15 | A median-relative α anchor is rejected: a good's concentration would shift because other goods changed price. | MODEL | 2130 |
| Y769 | §3.15 | α floored at 1 is rejected: it discards the cheap-bulk regime. | DESIGN | 2132 |
| Y770 | §3.15 | Production income as the aggregate supply term is rejected because it makes world supply depend on owners' … | MODEL | 2134 |
| Y771 | §3.15 | A τ margin on orientation is rejected: it manufactures cycles. | MODEL | 2136 |
| Y772 | §3.15 | Uniform supply in the aggregate solve is a v1 entry, moot in v2 and retained for history: it answered a … | MODEL | 2138 |
| Y773 | §3.15 | "the installed graph is `Φ_w`" — the v2.0-history parenthetical dropped | PROCESS | 2142 |
| Y774 | §3.15 | "a value-weighted aggregate of the per-good marking orders … acyclic for free, but its ends are a function of Phase 3' … | MODEL | 2144 |
| Y204 | §3.15 | "The rejection is structural, so no figure is kept for it" — the ceiling history deleted | DESIGN | 2147 |
| Y205 | §3.15 | The 3-mass gravity field over the top-3 pairwise-unconnected demanders reproduces whatever end count it is … | MODEL | 2149 |
| Y775 | §3.15 | The emergent-count wealth good replaced the pinned-count fields. | MODEL | 2158 |
| Y776 | §3.15 | A vestigial in-game economy with net treasury settlement is rejected: correct treasuries, wrong displays, … | DESIGN | 2160 |
| Y777 | §3.15 | it does NOT break the factoring (§3.10's `ps̄_C` identity survives); it is rejected because installing the share means … | MODEL | 2162 |
| Y778 | §3.15 | Node-level collect/transfer rules are rejected: the collect/transfer split is per good because whether a good … | MODEL | 2168 |
| Y779 | §3.15 | Treating unsteered goods as fully collected is rejected: transfer power does not come from merchants, and … | MODEL | 2170 |
| Y780 | §3.15 | Undirected shortest path as the primary fleet route is rejected: a geodesic over a directional structure can … | MODEL | 2172 |
| Y781 | §3.15 | Automatic per-good merchant targeting is rejected: one vanilla arrow click already achieves per-good … | DESIGN | 2174 |
| Y782 | §3.15 | Companion-overlay merchant assignment is rejected: assignment must stay a game action or vanilla knowledge … | DESIGN | 2176 |
| Y783 | §3.15 | Emission-time pruning of near-flat links is rejected: peripheral termini are intended consumption, and the … | DESIGN | 2178 |
| Y784 | §3.15 | Edge conductance / weighted Laplacian stays rejected: v1 rejected it as "too much mechanical surface", the … | MODEL | 2183 |
| Y785 | §3.15 | Staged delivery is rejected: the intermediate states are different designs sharing a solver rather than … | DESIGN | 2188 |
| Y786 | §3.15 | "The aggregate map is not a DAG" is still an error, with v1's reason corrected: v1 defended it by claiming … | MEASURED | 2190 |
| Y787 | §3.15 | The aggregate is a DAG because `Φ_w` is a DRAIN orientation, acyclic by the marking-order argument, whose own … | MODEL | 2192 |
| Y788 | §3.16 | v1 carried an evidence standard — "every retraction traced to a premise that entered through prose; nothing … | MODEL | 2198 |
| Y789 | §3.16 | At least fifteen non-prose claims failed, by three distinct mechanisms. | MODEL | 2200 |
| Y1256 | §3.16 | 1.37’s regime floors in `common/static_modifiers/00_static_modifiers.txt` are `min_local_autonomy = 20` (pasha_state), `50` (colonial_core) and `90` (territory_core, territory_non_core). | ENGINE | 2209 |
| Y1257 | §3.16 | That is the same file the model reads for `GP_COEFF` and the four province-state modifiers. | PROCESS | 2211 |
| Y1258 | §3.16 | 0 is the no-floor case, a value in no file. | ENGINE | 2211 |
| Y1259 | §3.16 | The item said until v6.3 that the 90/20/0 floors were "not in `defines.lua` or any file that has been searched" — the failure mode the item describes, committed by the item, the values having sat in a file already read for other constants. | PROCESS | 2212 |
| Y791 | §3.16 | Mechanism 2, file values transformed and then reported as raw: v1's grain (1.25) and livestock (1.00) base … | ENGINE | 2215 |
| Y792 | §3.16 | Mechanism 3, the spec's own algebra instantiated without checking the instantiation: ε provably preserved the … | MODEL | 2218 |
| Y206 | §3.16 | Implemented as written, v1's ε left the α = 1 identity's residual at 1e-5 against v1's ε of 1e-6, and would … | MEASURED | 2220 |
| Y793 | §3.16 | One of only three claims carrying `verified (method unstated)` provenance — Propagate Religion's gating — … | MODEL | 2223 |
| Y794 | §3.16 | The real signal in the audit was provenance: nine of the sixteen refuted ENGINE claims were UNSOURCED, and … | MODEL | 2224 |
| Y795 | §3.16 | The rule is not "trust derivations" and not "distrust prose" but that anything which entered without a … | DESIGN | 2228 |
| Y796 | §3.16 | Every engine fact in this spec must carry its source — a file path, a binary string, or a named observation — … | DESIGN | 2229 |
| Y797 | §3.16 | The gap that mattered more than any refutation: v1 never stated what determines sink placement, so the claim … | PROCESS | 2232 |
| Y798 | §3.16 | The audit found that flaw only by running the solver and asking why the output looked wrong. | MODEL | 2235 |
| Y799 | §3.16 | The standing repair is in this document's structure: what determines sink placement, what determines … | PROCESS | 2235 |
| Y800 | §3.16 | Each of those properties is provable or measured-and-labelled and each is checked at runtime — as an … | DESIGN | 2239 |
| Y801 | §3.16 | The next audit's first question should be which property of the output this spec still does not state. | DESIGN | 2243 |
| Y802 | §3.16 | The cautionary case is now closed and it closed the other way: the propagation source condition was corrected … | MODEL | 2246 |
| Y803 | §3.16 | Probe 15 settled it: the qualifier is descriptively false, since a country with no provinces and no merchant … | ENGINE | 2249 |
| Y804 | §3.16 | The lesson is not the one the case was filed under: it was filed as "agreement between reviewers is not … | MODEL | 2254 |
| Y805 | §3.16 | That a localisation string describes intent rather than behaviour is demonstrated here by one string and adopted as the rule of evidence, not asserted as a property of every string. | ENGINE | 2256 |
| Y806 | §3.16 | Sources are necessary but not sufficient, and an engine fact sourced to a string is settled only when … | DESIGN | 2258 |
| Y807 | §3.16 | During the declaration-order test a permuted node file differed from vanilla on 61 of 80 nodes — a real … | ENGINE | 2263 |
| Y808 | §3.16 | That measurement was meaningless, because two runs of the same vanilla build differ on 49 of 80 nodes by up … | ENGINE | 2265 |
| Y809 | §3.16 | A measurement without a null comparison is not evidence. | DESIGN | 2268 |
| Y810 | §3.16 | Every measured claim in this document that could vary run to run should carry the control that bounds its … | PROCESS | 2269 |

## NEW — propositions the prior census does not cover (`Y1260`–`Y1354`, document order)

| ID | § | claim | status | type | provenance | line |
|---|---|---|---|---|---|---|
| Y1260 | §0 | v6.5 changes the money and the display, not the map. | NEW | DESIGN | unsourced | 85 |
| Y1261 | §0 | The value the network routes is the engine's own — `inject_g(n)`, the engine's node × good produced quantity times the current price, read live from engine memory each tick and routed through the per-good graphs. | NEW | MODEL | §1.8 | 85 |
| Y1262 | §0 | Every orientation input — §1.3's wealth, §1.2's shares, `α` and `Φ_w` — is unchanged at v6.5. | NEW | DESIGN | §1.2; §1.3; §1.6 | 87 |
| Y1263 | §0 | `V_g` follows the routed economy. | NEW | MODEL | §1.6 | 88 |
| Y1264 | §0 | §3.4 is re-scoped to the two-quantity design. | NEW | PROCESS | §3.4 | 89 |
| Y1265 | §0 | §1.12 specifies the trade UI around the routed economy: the aggregate view shows each link's value in both directions, a selected good's view repopulates the same widgets with that good's numbers, and merchants are assignable on any link end from the node window's tabs. | NEW | DESIGN | §1.12 | 89 |
| Y1266 | §0 | That UI design closes the negative-link display question, both directions shown as positive flows. | NEW | DESIGN | §1.12 | 92 |
| Y1267 | §1.3 | The `trade_value(p)` defined in §1.3 is a component of `wealth(p)` and feeds orientation only. | NEW | MODEL | §1.3 | 329 |
| Y1268 | §1.3 | The money the network routes is §1.8's `inject`, the engine's own quantity. | NEW | MODEL | §1.8 | 330 |
| Y1269 | §1.3 | `trade_value(p)` and `inject` are different numbers with different jobs — one decides where the arrows point, the other is what moves along them — and conflating them is the error the split exists to prevent. | NEW | MODEL | §1.3; §1.8 | 330 |
| Y1270 | §1.6 | The 54.9% weighted agreement figure is computed from the save's `trade_goods_size` arrays, so it is scoped to this save's roll (§1.3's Garnatah note). | NEW | PROCESS | `measure6.py`; the 1444 save | 638 |
| Y1271 | §1.6 | The bisection's widest interval is ×1.38–×1.95 and the grid's is ×1.973–×2.456, and the two do not overlap. | NEW | MEASURED | `p3_bisect.py`; `round6.py` | 690 |
| Y1272 | §1.6 | The bisection rows were sampling artifacts, and only the grid's figures are maintained. | NEW | PROCESS | `p3_bisect.py`; `round6.py` | 691 |
| Y1273 | §1.8 | `inject_g(n)` is the engine's own produced trade value at node × good: the engine's `trade_goods_size` quantity for `g` at `n` times the current price. | NEW | MODEL | §1.8 | 810 |
| Y1274 | §1.8 | `inject` carries every modifier vanilla applies — buildings, trade-company investments and owner goods-produced modifiers. | NEW | ENGINE | stipulated | 811 |
| Y1275 | §1.8 | Production efficiency and autonomy are outside vanilla's trade value by vanilla's own construction. | NEW | ENGINE | read from a file (the vanilla trade-value construction) | 812 |
| Y1276 | §1.8 | `inject` is an annual quantity, like every value in this document. | NEW | MODEL | §1.3's time-basis note | 814 |
| Y1277 | §1.8 | The engine's own node fields are monthly twelfths of `inject`, measured at exactly 12.00× on reconciling nodes. | NEW | MEASURED | the 1444 save | 815 |
| Y1278 | §1.8 | The DLL reads `inject` live from engine memory each tick. | NEW | DESIGN | stipulated | 816 |
| Y1279 | §1.8 | The reference implementation's counterpart to `inject` is the save's per-node `trade_goods_size` array times the save's current price. | NEW | PROCESS | the reference implementation | 816 |
| Y1280 | §1.8 | The save carries 33 `trade_goods_size` slots in each of the 80 node blocks, slot *k* corresponding to `00_tradegoods.txt` index *k−1*. | NEW | ENGINE | read from a file (the 1444 save; `00_tradegoods.txt`) | 817 |
| Y1281 | §1.8 | That slot map was verified at Jaccard 1.000 against node good-membership. | NEW | MEASURED | the 1444 save | 818 |
| Y1282 | §1.8 | Slots 0, 30 and 32 are all-zero. | NEW | MEASURED | the 1444 save | 819 |
| Y1283 | §1.8 | The node × good granularity is already exactly what routing needs, with no per-province step, because a province produces one good and the engine has summed them. | NEW | MODEL | algebraic derivation | 820 |
| Y1284 | §1.8 | `inject` is a different quantity from §1.3's `trade_value(p)`, which is an orientation input and reads only development, the trade good and province condition. | NEW | MODEL | §1.3 | 821 |
| Y1285 | §1.8 | A manufactory moves `inject` and with it the money, and does not move the arrows. | NEW | MODEL | §1.3; §1.8 | 823 |
| Y1286 | §1.8 | The both-ends rule is carried as §2.7 item 19. | NEW | PROCESS | §2.7 item 19 | 845 |
| Y1287 | §1.9 | `ship_power_propagation` is granted in the static modifiers, ideas, reforms and an age ability. | NEW | ENGINE | read from a file (the shipped files) | 861 |
| Y1288 | §1.9 | The only-under-a-modifier conditional is the model's reading of the modifier's own semantics, and is unprobed. | NEW | PROCESS | unsourced | 861 |
| Y1289 | §1.12 | The map-mode box shows the node's total trade value — `total_value` in `interface/mapicons.gui`'s `trade_small_mapicon` / `trade_big_mapicon`. | NEW | ENGINE | read from a file (`interface/mapicons.gui`) | 948 |
| Y1290 | §1.12 | The node window's six value fields are `incoming_value`, `local_value`, `total_value`, `outgoing_value`, `our_from_this` and `piracy_value`, all in `tradeinterface.gui`. | NEW | ENGINE | read from a file (`tradeinterface.gui`) | 950 |
| Y1291 | §1.12 | `our_from_this` is the country's own take. | NEW | ENGINE | read from a file (`tradeinterface.gui`) | 951 |
| Y1292 | §1.12 | Every one of those six fields is now Σ_g of the per-good economy. | NEW | DESIGN | stipulated | 952 |
| Y1293 | §1.12 | Every incident link is shown, with the value flowing in each direction along it. | NEW | DESIGN | stipulated | 952 |
| Y1294 | §1.12 | Under the per-good model the same link can carry cloth one way and fur the other. | NEW | MODEL | §1.1 | 954 |
| Y1295 | §1.12 | `Φ_w` remains the drawn installed direction, and the directional panels are realized sums. | NEW | DESIGN | stipulated | 955 |
| Y1296 | §1.12 | Selecting a good repopulates the same widgets with that good's numbers: the node box the good's value at the node, the window all six fields for the good alone, each edge the good's realized flow. | NEW | DESIGN | stipulated | 959 |
| Y1297 | §1.12 | In a per-good view `piracy_value` is the good's share of the node's skim. | NEW | DESIGN | stipulated | 961 |
| Y1298 | §1.12 | In a per-good view each edge carries one direction only, since a single good's graph orients every edge one way. | NEW | MODEL | §1.1 | 962 |
| Y1299 | §1.12 | Vanilla's node-window layout — connected-node tabs across the top, incoming on the left (`incoming_nodes_listbox`), outgoing on the right (`outgoing_nodes_listbox`) — is kept. | NEW | ENGINE | read from a file (`tradeinterface.gui`) | 966 |
| Y1300 | §1.12 | The tabs are grouped by the active view's graph: `Φ_w` in the aggregate view, the selected good's orientation in a per-good view. | NEW | DESIGN | stipulated | 968 |
| Y1301 | §1.12 | Merchant assignment happens in the node window's tabs, panels in both groups carrying the assign button. | NEW | DESIGN | stipulated | 969 |
| Y1302 | §1.12 | Assignment is to a link *end* at this node and steers exactly the goods oriented away from this node on that link. | NEW | MODEL | §1.7 | 970 |
| Y1303 | §1.12 | The node window's tabs are where §1.7's incoming-entry assignability is delivered. | NEW | PROCESS | §1.7 | 971 |
| Y1304 | §1.12 | Today's `TradeNodeLink` widget carries one button and one label per link. | NEW | ENGINE | read from a file (`tradeinterface.gui`) | 972 |
| Y1305 | §1.12 | The directional value panels and per-good repopulation are new data on existing widget classes. | NEW | DESIGN | stipulated | 973 |
| Y1306 | §1.12 | The feasibility dependencies are §2.7 probe 7 (arrow render state versus the economic link) and a node-window data-source hook, added hooking surface under §2.5. | NEW | PROCESS | §2.5; §2.7 probe 7 | 974 |
| Y1307 | §1.12 | Per-good value display and two-way traffic move into the main UI by swap-on-view, only the selected good's numbers displayed at a time. | NEW | DESIGN | stipulated | 978 |
| Y1308 | §1.12 | Swap-on-view means no thirty-field storage in engine structures is needed. | NEW | DESIGN | algebraic derivation | 979 |
| Y1309 | §1.12 | Showing both directions as positive flows settles the negative-link display question by design, and no negative net is ever displayed. | NEW | DESIGN | §2.9; §3.9 | 980 |
| Y1310 | §2.2 | The engine's produced quantity lives at node level; no province record carries one. | NEW | ENGINE | read from a file (the 1444 save) | 1061 |
| Y1311 | §2.2 | The shipped DLL's second implementation includes the live `inject_g(n)` read. | NEW | DESIGN | §1.8 | 1101 |
| Y1312 | §2.3 | v4.0's tree ships three scripts that sweep both modifier directories: `audit_modifiers.py`, `audit_alpha.py` and `audit_bands.py`. | NEW | PROCESS | read from a file (v4.0's tree) | 1174 |
| Y1313 | §2.3 | Other scripts in that tree read the same files without sweeping them. | NEW | PROCESS | read from a file (v4.0's tree) | 1175 |
| Y1314 | §2.3 | The base of the 0.10 weighted self-coherence figure is pinned to the orientation model's per-good trade value, so §1.6's `inject` redefinition cannot silently re-base it. | NEW | PROCESS | §1.6 | 1272 |
| Y1315 | §2.3 | Shipped content carries a DLC-gated *modifier* of caravan power: `common/disasters/decline_of_mali.txt` gates a `caravan_power = -0.33` disaster on `has_dlc = "Origins"`. | NEW | ENGINE | read from a file (`common/disasters/decline_of_mali.txt`) | 1310 |
| Y1316 | §2.3 | No shipped file gates the caravan *grant mechanic* or treasure-fleet *diversion* themselves on a DLC flag. | NEW | ENGINE | the absence of a shipped rule | 1310 |
| Y1317 | §2.3 | That conditionality is engine-side, and the flag must be read via the engine. | NEW | MODEL | unsourced | 1310 |
| Y1318 | §2.3 | A `dlc_load.json` toggle run is the probe-class confirmation of it. | NEW | PROCESS | unsourced | 1310 |
| Y1319 | §2.4 | In the backwards-links run the one `total` exception is `zambezi`, drifting 0.012%, within the engine's own run-to-run variance. | NEW | MEASURED | engine test; §2.8 | 1321 |
| Y1320 | §2.6 | The origination written each tick is §1.8's `inject_g(n)`, read live at the tick and routed per §1.8 over the per-good graphs. | NEW | DESIGN | §1.8 | 1407 |
| Y1321 | §2.6 | The tick's figures are in the document's annual basis, with the ÷12 conversion at the engine-write boundary, since the engine's node fields hold monthly twelfths. | NEW | DESIGN | §1.3 | 1408 |
| Y1322 | §2.6 | That annual-over-twelve relation is the one §1.3 established from the engine's own tooltips. | NEW | PROCESS | §1.3 | 1409 |
| Y1323 | §2.6 | The engine has one per-link value field, and the net per-link value is written to it. | NEW | ENGINE | stipulated | 1426 |
| Y1324 | §2.6 | The display never shows that net, since §1.12 shows both directions as positive flows. | NEW | DESIGN | §1.12 | 1426 |
| Y1325 | §2.6 | §2.7 item 4 covers the engine's own consumers of a negative stored value. | NEW | PROCESS | §2.7 item 4 | 1426 |
| Y1326 | §2.7 | Probe 19 is the both-ends rule: §1.8 carries "no transfer into a node where nobody holds power at both ends" from the trade interface's behaviour, named by no define, string or searched file. | NEW | DESIGN | §1.8 | 1493 |
| Y1327 | §2.7 | Probe 19's method: observe whether transfer enters a node where the receiving side holds power at only one end — one session, node window. | NEW | DESIGN | unsourced | 1495 |
| Y1328 | §2.8 | Under §1.8 the origination is identical to vanilla's by construction. | NEW | MODEL | §1.8 | 1542 |
| Y1329 | §2.8 | The world total collected income is therefore expected to track vanilla's up to steering boosts, routing differences and merchant placement. | NEW | DESIGN | §1.8 | 1542 |
| Y1330 | §2.8 | It is compared against the DLL's live read, with a tolerance and a null run (the economy-tab row). | NEW | DESIGN | §2.8's economy-tab row | 1542 |
| Y1331 | §2.8 | The save-based reference reconstruction, Σ `trade_goods_size` × price ÷ 12, reproduces the engine's `local_value` exactly on 58 of 80 nodes. | NEW | MEASURED | the 1444 save | 1542 |
| Y1332 | §2.8 | That reconstruction runs 3.4% low in aggregate, short almost entirely in New World nodes. | NEW | MEASURED | the 1444 save | 1542 |
| Y1333 | §2.8 | The shortfall is a known reference-side gap, recorded so nobody chases it as a model defect. | NEW | PROCESS | unsourced | 1542 |
| Y1334 | §2.9 | The memory track also needs locating the engine's live produced-quantity fields, the node trade-goods arrays and/or the per-province quantities behind them (§2.5's pattern-scanning scope), which §1.8's live read needs. | NEW | DESIGN | §1.8; §2.5 | 1554 |
| Y1335 | §2.9 | §2.8's disagreement measurement is still collected even though the negative-link display policy is settled. | NEW | DESIGN | §2.8 | 1556 |
| Y1336 | §3.2 | The 7.6% weighting base is `price(g)·Σ_m goods_produced(m,g)` — `solver.build_sc`'s base, pinned so §1.6's `inject` redefinition cannot silently re-base it. | NEW | PROCESS | `solver.py`; §1.6 | 1583 |
| Y1337 | §3.2 | The 16.7% and 7.6% figures are `scripts/r9/lead/L_rank2.py`'s. | NEW | PROCESS | `scripts/r9/lead/L_rank2.py` | 1584 |
| Y1338 | §3.4 | The scope of §3.4's pre-modifier argument is the orientation shares: where a good comes from is a property of the place, so owner choices must not move the arrows. | NEW | DESIGN | §1.2 | 1720 |
| Y1339 | §3.4 | The routed economy is the other half of the two-quantity design and deliberately carries the engine's own goods-produced modifiers. | NEW | DESIGN | §1.8 | 1720 |
| Y1340 | §3.4 | Goal 7 makes the game's money the model's money — a manufactory moves the ducats without moving the map. | NEW | DESIGN | §3.1 Goal 7 | 1720 |
| Y1341 | §3.4 | `inject` inherits the production-efficiency and autonomy exclusion §3.4 demands, by vanilla's own construction, verified two ways on the save. | NEW | MEASURED | the 1444 save | 1724 |
| Y1342 | §3.4 | The aggregate graph reads neither trade value nor production income: `Φ_w` is built from §1.3's wealth field. | NEW | MODEL | §1.3; §1.6 | 1726 |
| Y1343 | §3.4 | The `V_g`-weighted aggregate this paragraph once described was v2.0's, gone at v2.1's `Φ_w` adoption. | NEW | PROCESS | the v2.0 and v2.1 texts | 1727 |
| Y1344 | §3.9 | Two of vanilla's three authored ends are in the top node-wealth ranks. | NEW | MEASURED | numerical test | 1866 |
| Y1345 | §3.9 | `venice` sits at node-wealth rank 21 of 80, at 180.6. | NEW | MEASURED | numerical test | 1867 |
| Y1346 | §3.9 | `venice` is the historical pick rather than the wealth pick. | NEW | MODEL | numerical test | 1867 |
| Y1347 | §3.14 | AI merchant candidates are (node, incident-link-end) pairs — both of the node window's tab groups, not `Φ_w`-outgoing links. | NEW | DESIGN | §1.12 | 2072 |
| Y1348 | §3.14 | A candidate's active good set is the goods oriented away from that node on that link, which is the solver's own output. | NEW | MODEL | §1.1 | 2072 |
| Y1349 | §3.14 | The AI reads the per-good orientations directly and never infers from the drawn map. | NEW | DESIGN | stipulated | 2072 |
| Y1350 | §3.14 | A candidate steering nothing scores zero and is never chosen. | NEW | DESIGN | algebraic derivation | 2072 |
| Y1351 | §3.16 | The 75% overseas autonomy floor was introduced at 1.8: `patchnotes/1.8 Patchnotes.txt` L40 reads "Overseas provinces now have a minimum autonomy of 75% instead of the 'distant overseas' penalty". | NEW | ENGINE | read from a file (`patchnotes/1.8 Patchnotes.txt`) | 2205 |
| Y1352 | §3.16 | It was superseded by States & Territories at 1.16: `1.16 Patchnotes.txt` L42 introduces States & Territories. | NEW | ENGINE | read from a file (`patchnotes/1.16 Patchnotes.txt`) | 2207 |
| Y1353 | §3.16 | 1.12's patch notes carry no overseas-floor change. | NEW | ENGINE | read from a file (the tree's patchnote archive) | 2207 |
| Y1354 | §3.16 | v1 carried the 75% floor as current. | NEW | PROCESS | `../v1-laplacian/` | 2208 |

---

**Summary.** U 1046 / RW 3 / C 28 / R 0 / N 95 — 1172 rows in all; highest ID used `Y1354`.

**Work list for the delta-scoped validation.** The prior rows whose verdict-relevant text changed
this round, and which the next round grades alongside the 95 NEW rows, are the 28 CHANGED —
`Y098`, `Y137`, `Y323`, `Y384`, `Y421`, `Y422`, `Y423`, `Y424`, `Y426`, `Y438`, `Y447`, `Y486`,
`Y572`, `Y580`, `Y581`, `Y591`, `Y637`, `Y652`, `Y683`, `Y693`, `Y790`, `Y1099`, `Y1115`, `Y1144`,
`Y1195`, `Y1203`, `Y1218`, `Y1245` — and the 3 REWORDED — `Y425`, `Y1035`, `Y1246`. 31 carried
rows in all; every other carried row is UNCHANGED and out of scope.
