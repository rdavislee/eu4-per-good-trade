# Validation — Per-Good Trade Network Spec v6.5, round 10 (delta-scoped)

**Document under test:** `per-good-trade-spec.md`, 2,270 lines, MD5 `f9a70dfd859e1c97b266c35de4a1b228`, version stamp 6.5.

**Census validated:** `claims-delta-round10.md` — 1,172 rows (`Y001`–`Y1354`, with gaps).

---

## Carry statement

This round is **delta-scoped**. The prior full-census validation, `validation-round9.md`, graded
`claims-delta-round9.md`'s 1,077 rows against spec v6.4 (MD5 `0989f4dc54d31514123eed24f0aae5c5`)
and returned 1,055 CONFIRMED / 14 PARTIAL / 0 REFUTED / 8 UNTESTABLE.

**Every row of the current census not listed in the scope below carries its round-9 verdict
unchanged, recorded once here and not re-asserted per row.** That carry is licensed by the
reconstruction check in *Footing* below: `round10.diff` applied to the frozen v6.4 baseline
reproduces the current spec byte-for-byte, so every line outside the diff's 31 hunks is identical
to the text round 9 graded.

**Carried: 1,045 rows** — the 1,046 UNCHANGED rows less `Y375`, which is pulled into scope because
its round-9 verdict was PARTIAL. Their carried verdicts are **1,036 CONFIRMED, 1 PARTIAL (`Y483`,
§2.3 — the only round-9 PARTIAL not touched by this round's diff), 8 UNTESTABLE**. The 8 UNTESTABLE
rows are not re-investigated; each is examined below only for whether anything this round changed
its testability.

**Freshly graded here: 127 rows** — 28 CHANGED, 3 REWORDED, 95 NEW, and `Y375`.

---

## Footing — the census's own accounting

| check | result |
|---|---|
| Spec MD5 | `f9a70dfd859e1c97b266c35de4a1b228`, 2,270 lines — matches the brief. |
| Frozen baseline MD5 | `per-good-trade-spec-v6.4-round10-frozen.md` = `0989f4dc54d31514123eed24f0aae5c5`, 2,190 lines — matches the brief, and matches the document round 9 states it graded. |
| **Diff reconstructs the spec** | **YES.** `patch -p0` of `round10.diff` (31 hunks) onto a fresh copy of the frozen baseline yields MD5 `f9a70dfd859e1c97b266c35de4a1b228` — bit-identical to `per-good-trade-spec.md`. All 31 hunks applied clean: no fuzz, no offsets, no rejects. Text outside the hunks is therefore byte-identical, which is what licenses the carry. |
| Census row count | 1,172 rows matching `^\| Y\d+ \|`; highest ID `Y1354` — matches the summary line. |
| Status partition | U 1,046 + RW 3 + C 28 + N 95 = 1,172 ✓. (UNCHANGED rows use a 5-column layout with no status cell; C/RW/N rows use the 8-column layout carrying status and an old→new column.) |
| **CHANGED set = brief's list** | **YES** — exactly 28 IDs, set-equal to the brief: Y098 Y137 Y323 Y384 Y421 Y422 Y423 Y424 Y426 Y438 Y447 Y486 Y572 Y580 Y581 Y591 Y637 Y652 Y683 Y693 Y790 Y1099 Y1115 Y1144 Y1195 Y1203 Y1218 Y1245. |
| **REWORDED set = brief's list** | **YES** — exactly 3: Y425 Y1035 Y1246. |
| **NEW set = brief's list** | **YES** — exactly 95, contiguous `Y1260`–`Y1354`, no gaps in the span and no NEW row outside it. |

**Footing verdict: CONFIRMED.** The diff reconstructs the spec from the frozen baseline, and the
work list matches the census's C/RW/N sets exactly.

---

## Method

Each in-scope claim was graded against primary sources: the EU4 1.37.5 install at
`C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV` — its `interface/`,
`common/`, `localisation/` and `patchnotes/` trees — the readable saves (`VANILLA_start.eu4`,
`Castile1444_12_22.eu4`), the crash dumps in the OneDrive `crashes/` directory, the reference
implementation and instruments in `scripts\`, and the prior version directories `..\v1-laplacian\`
… `..\v5-owner-agnostic\`. Measured figures were reproduced by running the instrument; file claims
were settled by opening the file and quoting the line; derivations were graded step by step.

Fresh instrument runs and lead probes for this round are in `scripts\r11\`: `measure6.out`,
`p3_y1035.out`, `telescope.out`, `L_localvalue.py`/`.out` (node `local_value` reconstruction),
`L_effaut.py` (autonomy / production-efficiency save test), `L_rank2.py`, `BRIEF.md`, and the slice
probes `A_*`, `B_*`, `C_*`, `D_*`.

Four slices were graded by subagents (model sonnet) against `scripts\r11\BRIEF.md`. **Every PARTIAL
a subagent returned was independently re-run or re-read by the lead validator before entering this
file** — two were overturned to CONFIRMED on that recheck (`Y1290`, `Y790`), two were sustained
(`Y1291`, `Y1352`), and two were sustained on narrower and better-evidenced grounds than the
subagent gave (`Y1275`, `Y1341`). Two further PARTIALs (`Y1331`, `Y375`) are the lead's own, found
on lead measurement. No subagent returned a REFUTED.

**Verdicts.** CONFIRMED = reproduced or verified as scoped. PARTIAL = part holds, part fails, or
the claim outruns its evidence. REFUTED = the sources contradict it as scoped. UNTESTABLE =
unsettleable with these materials; the row says what would settle it.

Rows scoped to a named observation, a stated design intent, or marked
specification-not-measurement are graded at that scope: the question is whether the spec's
statement is accurate, not whether the unbuilt thing works. The UI/DLL specification rows (§1.12,
§1.8's inject block, §3.14's candidate enumeration) had their factual components — gui-file facts,
save-structure facts, define values, figures — graded empirically, and their specification
components graded at stated scope.

---

## §0 — lineage and the v6.5 preamble

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1144 | **CONFIRMED** | lead: enumerated all 31 `.py` files in `..\v4-owner-agnostic\`; grepped each for `event_modifiers` and `static_modifiers` | Exactly three v4.0 scripts reference both directories, and all three loop over both: `audit_modifiers.py:21` `for root, sub in (("common", "event_modifiers"), ("common", "static_modifiers")):`; `audit_alpha.py:16` `for sub in ("event_modifiers", "static_modifiers"):`; `audit_bands.py:15` `for sub in ("event_modifiers","static_modifiers"):`. Round 9's fourth candidate `audit_seventh.py` has **0** occurrences of `event_modifiers` and reads only `00_static_modifiers.txt` (L125), so the new "both modifier directories" qualifier excludes it correctly. Count of three is exact; the v4.0 attribution holds. *(Closes round 9's PARTIAL.)* |
| Y1260 | **CONFIRMED** | lead: read spec L85-93; hunk-by-hunk read of all 31 diff hunks | §0: "**v6.5** changes the money and the display, not the map." Borne out by the hunk inventory — money: §1.6 `V_g` (-539), §1.8 inject block (-789), §2.2 (-1000, -1021, -1040), §2.6 (-1343, -1359), §2.8 (-1465), §3.4 (-1646); display: §1.12 (-911), §2.9 (-1465), §3.9 (-1835), §3.14 (-1993). No hunk touches §1.1's phases, §1.2, §1.3's wealth formula, `α`, or `Φ_w`'s definition. |
| Y1261 | **CONFIRMED** | lead + slice C: read spec L84-87 against §1.8 L810-823 | §0's restatement matches §1.8's definition in substance: `inject_g(n)` = the engine's `trade_goods_size` quantity for `g` at `n` × the current price, read live from engine memory each tick, routed per §1.8 over the per-good graphs. |
| Y1262 | **CONFIRMED** | lead: hunk-by-hunk read of `round10.diff` against §1.2, §1.3, §1.4 and §1.6's line ranges | No hunk falls in §1.2. The §1.3 hunk (-316,+326) is a **pure insertion** of a five-line note; the `goods_produced` / `trade_value` / `tax_value` / `wealth` / `c(n,g)` block above it is unmodified context. No hunk touches §1.4's `α(g)`. The §1.6 hunk (-539) changes only the `V_g` line — the `s_w`, `c_w`, `b_w`, `α_Φ = 2.0` block and `Φ_w = DRAIN(b_w)` are unmodified context. All four named orientation inputs are byte-identical. |
| Y1263 | **CONFIRMED** | lead: read spec L87-88 against §1.6 L557 | §1.6 L557 now reads ``V_g     = Σ_n inject_g(n)`` annotated "§1.8's engine-injected value" — `V_g` does follow the routed economy. |
| Y1264 | **CONFIRMED** | lead + slice D: read the §3.4 hunk (-1646,+1717) | The rewrite adds "**The scope of this argument is the orientation shares**" and "The routed economy is the other half of the two-quantity design", and re-subjects the trade-value paragraph from "the aggregate" to "`V_g` and the routed value" — a re-scoping to the two-quantity design, as claimed. |
| Y1265 | **CONFIRMED** | slice A + lead: read spec L89-92 against §1.12 L945-984 | All three sub-claims are present in §1.12: "Every incident link is shown, with the value flowing in each direction along it" (L951); "the **same widgets repopulate with that good's numbers**" (L959); "**Merchant assignment happens in these tabs**: panels in both groups carry the assign button" (L969). |
| Y1266 | **CONFIRMED** | slice A + lead: read spec L92-93 against §1.12 L980-981 | §1.12: "Showing both directions as positive flows also settles the negative-link display question by design: no negative net is ever displayed (§2.9, §3.9)." |

## §1.1 — the per-good graphs

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1195 | **CONFIRMED** | lead: `diff scripts/val5_pergood.py scripts/props6.py`; `wc -l` on both | `val5_pergood.py` is still on disk. `diff` emits exactly one opcode, `129a130,158` — a pure insertion: **0** deleted lines, 129 → 158. The inserted block is the permutation loop (its first lines are the C5 comment and the loop). The spec now says "an added block" and names no count, so round 9's refuted "27 added lines" is withdrawn rather than repaired. The still-on-disk, verbatim and zero-deletions halves all hold. *(Closes round 9's PARTIAL.)* |

## §1.3 — wealth

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1267 | **CONFIRMED** | lead + slice C: read spec L320-330 | §1.3's block gives `trade_value(p) = goods_produced(p) · price(good(p))` and `wealth(p) = tax_value(p) + trade_value(p)`; `wealth` feeds only `c(n,g)` / `s` / `Φ_w`, i.e. orientation. The added note states exactly that. |
| Y1268 | **CONFIRMED** | lead + slice C: read spec L330 against §1.8 L810-823 | Consistent with §1.8's definition of `inject` as the routed quantity. |
| Y1269 | **CONFIRMED** | lead + slice C: read spec L330-332; read `scripts/solver.py:161-164` | The distinction is carried in the code as well as the prose. `solver.py` L161-163: "`prod_income` is MISNAMED: goods_produced * price is the trade_value component of wealth (sec 1.3), NOT production income -- no efficiency, no autonomy enters"; L164 sets `prod_income=gp * price` where `gp` derives from `base_production` and devastation only. |

## §1.6 — the aggregate graph

| ID | verdict | method | evidence |
|---|---|---|---|
| Y098 | **CONFIRMED** | lead: fresh run of `scripts/measure6.py` (`scripts/r11/measure6.out`) | `Phi_w self-coherence edge-goods 55.1`; `Phi_w self-coherence value-weighted 54.9`. The weighting basis really is inject: `measure6._inject_weights()` (L79-114) opens `VANILLA_start.eu4`'s `gamestate`, sums each node block's `trade_goods_size` slots by good, and multiplies by that good's `current_price` from the save's `change_price` block — i.e. `Σ_n inject_g(n)`, not the old `price(g)·Σ_m gp`. Both figures reproduce to the quoted decimal. |
| Y323 | **CONFIRMED** | lead: read spec L557; read `solver.build_sc` L196; cross-read §2.3 L1271-1272 and §3.2 L1583-1584 | §1.6 L557 reads ``V_g     = Σ_n inject_g(n)   # per-good value weights (display, link values, AI) — §1.8's engine-injected value``; the consumer list is unchanged. Adversarial check for an internal contradiction: §3.2 and §2.3 still weight two figures by `price(g)·Σ_m goods_produced(m,g)` (`solver.py:196` `V = np.array([PRICES[g] * world[gi] …])`), but both sites now **name that base explicitly and say why** — "pinned so §1.6's `inject` redefinition cannot silently re-base it". That is an explicit historical pin, not a contradiction. |
| Y1270 | **CONFIRMED** | lead: read `measure6._inject_weights()` L79-114; read §1.3's Garnatah note L353-359 | The weight is built from the save's per-node `trade_goods_size` arrays × the save's `current_price`, so it inherits the save's roll. §1.3's Garnatah note is the correct referent: it records that a window figure carries the owner's `global_trade_goods_size_modifier` (Granada's 1444 `Industrious` ruler, +10%) and that "Ruler personalities are rolled at game start wherever country history scripts none, so any window figure is one sample of a random variable". |
| Y1099 | **CONFIRMED** | lead: fresh run of `scripts/europe.py`; read `per-good-trade-spec-v6.1-frozen.md` L597-606 | The direction survives both methods (Europe 1 end → 3, Asia 1 → 0). The widest interval does not. v6.1's withdrawn table names **×1.38–×1.95** as "the widest single interval in the table" (L598, L604-605). `europe.py`'s uniform 0.001 grid prints `widest run with three European ends and none in Asia : x1.973-x2.456`. Since `1.95 < 1.973` the two spans are disjoint, and only the grid figures are quoted in the current text. *(Closes round 9's PARTIAL.)* |
| Y1271 | **CONFIRMED** | lead: same two sources | Both endpoints reproduce exactly and the intervals do not overlap. |
| Y1272 | **CONFIRMED** | lead: `europe.py` maximal-run table | The grid shows the bisection's single ×1.38–×1.95 span is in fact three runs — `x1.382-x1.701`, the one-off `doab` set at `x1.702-x1.709`, and `x1.710-x1.947` — then broken again at `x1.948-x1.972` where `hangzhou` returns. One interval where the grid finds four is exactly a sampling artifact. `europe.py` also reproduces the section's other maintained figures: "runs narrower than x0.01: 3 (x1.287-x1.288; x1.362-x1.368; x1.702-x1.709 ONE-OFF)". |

## §1.8 — routing, `inject`, and the gates

| ID | verdict | method | evidence |
|---|---|---|---|
| Y375 | **PARTIAL** | lead recheck against the current text: read spec L842-846 and §2.7 item 19 L1493-1496; re-grepped `common/defines.lua`, `common/defines/` and all `localisation/*_l_english.yml` | The trade-range half is file-sourced and reproduces exactly: `localisation/hints_l_english.yml:230 HINT_TRADERANGE_TEXT:0 "Trade Range determines how far away you may send a Merchant…"`; `EU4_l_english.yml:1353 TRADE_RANGE_IRO`; `EU4_l_english.yml:2847 TRADE_NODES_OUT_OF_RANGE`. **The both-ends half is still not settleable from these materials**: no define and no English string states it. The nearest hit, `core_l_english.yml:281 TRANSFER_TRADE_POWER_TO_DESC` — "in trade nodes where they both have power" — is the *diplomatic* country-to-country Transfer Trade Power relation, a different mechanic, and does not name the node-transfer rule §1.8 asserts. **What the round-10 fix changed is the disclosure, not the evidence**: §1.8 now adds "and carried as §2.7 item 19", and §2.7 item 19 exists and is the both-ends rule with a stated method. The unsupported half is now a scheduled measurement rather than a bare gap, but remains unmeasured. **What would settle it:** running §2.7 probe 19 — one session, node window, observing whether transfer enters a node where the receiving side holds power at only one end. |
| Y1273 | **CONFIRMED** | slice C: read spec L810; independent save parse | The quantity is real and computable exactly as described: `trade_goods_size` for `g` at `n` × the good's `current_price`, both read from the save. |
| Y1274 | **CONFIRMED** | slice C: grep `common/buildings/`, `common/tradecompany_investments/`, `common/ideas/` | All three named modifier families exist and feed goods produced: `00_buildings.txt` `manufactory = { trade_goods_size = 1.0 }`; `tradecompany_investments/00_Investments.txt` `area_modifier = { trade_goods_size = 0.15 }` (and 0.3 in another investment); `trade_goods_size` appears in `00_basic_ideas.txt`, `00_country_ideas.txt` and `zz_group_ideas.txt`. Graded at the row's stipulated scope. |
| Y1275 | **PARTIAL** | lead recheck: read `common/static_modifiers/00_static_modifiers.txt` (`local_autonomy_multiplicative`, `production_efficiency` blocks); grepped `localisation/*_l_english.yml`; ran lead probe `scripts/r11/L_effaut.py` on `VANILLA_start.eu4` | **The autonomy half is a direct file fact and is corroborated on the save.** `local_autonomy_multiplicative = { local_manpower_modifier = -1.0, local_sailors_modifier = -1.0, local_tax_modifier = -1.0, local_production_efficiency = -1.0, province_trade_power_modifier = -0.5, … }` — it scales `local_production_efficiency` and `local_tax_modifier` and **does not mention `trade_goods_size` or `trade_goods_size_modifier` at all**. On the save, across 245 singleton (node, good) cells, r(local_autonomy, engine/model ratio) = **−0.097**, and the sample's highest-autonomy province, Valencia (pid 213, glass, **91.0%** autonomy), reproduces the autonomy-free prediction **exactly** (1.000 = 1.000). **The production-efficiency half is not file-stated.** No shipped file carries vanilla's trade-value construction — the static `production_efficiency` block grants only `colonist_placement_chance = 0.2`, and nothing anywhere links `production_efficiency` to `trade_goods_size`. The evidence is absence-of-linkage plus distinct modifier keys plus localisation keeping `TRADE_GOODS_SIZE` ("Local Goods Produced") separate from `TRADE_VALUE` and production income. **The exact disagreement:** the row's provenance, "read from a file (the vanilla trade-value construction)", names a source that does not exist as a file for the efficiency half. **What would settle it:** a province-window read comparing Trade Value across two owners differing only in production efficiency. |
| Y1276 | **CONFIRMED** | slice C + lead: read §1.3 L342-352, §1.8 L814 | §1.3 establishes the annual basis from the engine's own tooltips ("The engine's own province tooltips give both as *annual* quantities divided by twelve for display… Both monthly figures being the annual value over twelve is what lets the annual forms add directly"). §1.8 cites exactly that. |
| Y1277 | **CONFIRMED** | lead probe `scripts/r11/L_localvalue.py` (independent of `measure6`), cross-checked against slice C's independent parse | On the reconciling nodes the ratio `Σ_g trade_goods_size × current_price` : `local_value` is **12.00** to two decimals on **57** nodes; the whole ratio histogram is `[(12.00, 57), (12.01, 2), (11.98, 2), (12.05, 1), …]` — the only departures from 12.00 are the last-decimal cases and the New World shortfall nodes (7.59, 6.97, 5.98, 7.40). The engine's node fields are monthly twelfths, measured at exactly 12.00× where they reconcile. |
| Y1278 | **CONFIRMED** | slice C: read spec L816 | "The DLL reads it live from engine memory each tick." Graded at stated (DESIGN / stipulated) scope; no DLL exists to test against. |
| Y1279 | **CONFIRMED** | lead + slice C: read `measure6._inject_weights()` L79-114; independent reproduction | The reference-side counterpart is exactly the save's per-node `trade_goods_size` array × the save's `current_price`, which is what the shipped code computes and what two independent probes reproduce. |
| Y1280 | **CONFIRMED** | lead probe `L_localvalue.py`; slice C's independent parse; read `common/tradegoods/00_tradegoods.txt` | All 80 `node={…}` blocks under `trade={` carry a `trade_goods_size` array, and the slot-count distribution is uniform: `{33: 80}` — exactly 33 slots in every one of the 80 blocks. `00_tradegoods.txt` carries 32 top-level entries, so slots 1–32 map to file indices 0–31 and slot 0 is unmapped (and all-zero, per Y1282). The slot map is confirmed at Jaccard 1.000 in Y1281. |
| Y1281 | **CONFIRMED** | slice C: independent parse cross-referencing `common/tradenodes/00_tradenodes.txt` members against save province `trade_goods` | Restricting node membership to **owned** provinces — which is what "goods produced" means, and is `solver.province_table`'s own filter — gives **Jaccard = 1.000000, 0 mismatches**, both pooled and as a mean of per-node values, and the transposed per-slot formulation gives 1.0000 on all 30 real-good slots. (The naive variant counting native/undiscovered members too gives 0.973, which is the expected artifact of provinces that nominally carry a good but produce nothing.) |
| Y1282 | **CONFIRMED** | lead probe `L_localvalue.py` (exhaustive over all 80 nodes) | `slots never nonzero on any node: [0, 30, 32]` — slots 0, 30 and 32 are all-zero and every other slot is nonzero somewhere. Slot 30 → `coal`, consistent with §1.6's independent "coal produces nowhere at the 1444 start"; slot 32 → `unknown`; slot 0 is the unmapped leading slot. |
| Y1283 | **CONFIRMED** | slice C: full province-record field census over all 4,941 province records | Every province record carries exactly one `trade_goods` field — a scalar label, not an array — and the node `trade_goods_size` arrays are pre-summed across members (verified in the Y1277 and Y1281 computations). One good per province, summed by the engine to node × good, is exactly the granularity routing needs. |
| Y1284 | **CONFIRMED** | lead + slice C: read spec L821 against §1.3 L320-325 | §1.3's `trade_value(p) = goods_produced(p) · price(good(p))` with `goods_produced(p) = GP_COEFF · base_production(p) · (1 + Σ province-state goods modifiers)` reads development, the trade good (via price) and province condition, and nothing else — no building, trade-company or owner term. |
| Y1285 | **CONFIRMED** | slice C: read spec L823; `common/buildings/00_buildings.txt`; §1.3's formula | `manufactory = { trade_goods_size = 1.0 }` feeds the engine's `trade_goods_size` and therefore `inject`; §1.3's `goods_produced(p)` has no building term at all, so a manufactory moves the money and not the arrows. |
| Y1286 | **CONFIRMED** | lead + slice C: read §2.7 L1493-1496 | §2.7 item 19 exists and is the both-ends rule: "**The both-ends rule.** §1.8 carries 'no transfer into a node where nobody holds power at both ends' from the trade interface's behaviour, named by no define, string or searched file." |
| Y1310 | **CONFIRMED** | slice C: full province-record field census (4,941 records, 2,472 owned) | No province record anywhere carries `goods_produced`, `trade_goods_size`, `production`, `produced` or `trade_value`. Province level carries only `base_production` (an input) and `trade_goods` (a label). The produced quantity exists only at node level. (Corroborating: the 2,472 owned count matches the spec's independently stated "2,472 counted provinces", and `latent_trade_goods` appears 58 times, matching the "58 latent-coal provinces" figure.) |
| Y1311 | **CONFIRMED** | slice C: read spec L1101 and L816 | §2.2: "The shipped DLL carries a second implementation of items 4–7 … including the live `inject_g(n)` read (§1.8)." §1.8 supports it. Graded at stated (DESIGN) scope. |

## §1.9 — trade power propagation

| ID | verdict | method | evidence |
|---|---|---|---|
| Y384 | **CONFIRMED** | lead: read spec L859; grepped the install for `ship_power_propagation`, `PROPAGAT` in `common/defines.lua` and `common/defines/`, and `localisation/*_l_english.yml` | The re-scoping is accurately carried and is what round 9 asked for. L859 now marks **both** halves as derived: "the *only-under* conditional is the model's reading of the modifier's own semantics, unprobed" and "the composition too is stated by no file, string or observation, so both halves are the model's derived reading rather than engine fact". The underlying absence holds on re-search: the only propagation defines are `TRADE_PROPAGATE_DIVIDER = 5` and `TRADE_PROPAGATE_THRESHOLD = 2` (`defines.lua` L1205-1206), and the only `ship_power_propagation` localisation is the bare label `MODIFIER_SHIP_POWER_PROPAGATION:0 "Ship Tradepower Propagation"` — nothing states that propagation happens *only* under the modifier, nor how the two compose. The flat assertion round 9 could not settle is withdrawn. *(Closes round 9's PARTIAL.)* |
| Y1245 | **CONFIRMED** | lead: `grep -rl "ship_power_propagation"` over the install, then read each hit | All four named grant sites exist: **static modifiers** — `00_static_modifiers.txt:1511`, `private_enterprise_subject = { … ship_power_propagation = 0.1 }`; **ideas** — `00_basic_ideas.txt:1163` `grand_navy = { … ship_power_propagation = 0.25 }` and `00_country_ideas.txt:17160` `msa_in_every_port = { … ship_power_propagation = 0.2 }`; **reforms** — `02_government_reforms_republics.txt:3122` `ship_power_propagation = 0.25`; **an age ability** — `common/ages/00_default.txt:434-439` `ab_ship_power_propagation = { … modifier = { ship_power_propagation = 0.2 } }`. *(Scope note, not a deduction: two further grant families exist that the sentence does not name — `custom_ideas/05_leviathan_custom_ideas.txt` and two mission modifiers in `event_modifiers/01_mission_modifiers.txt`. The claim is existence-scoped, not exhaustive, so this does not cost it.)* |
| Y1246 | **CONFIRMED** | lead: diffed the bullet against `per-good-trade-spec-v6.4-round10-frozen.md`; re-searched defines and localisation | The reword is what the census says: "**their** composition is stated by no file, string or observation" → "**the composition too** is stated by no file, string or observation"; the proposition is otherwise word-for-word. The proposition itself holds: both ingredients are file-stated (`TRADE_PROPAGATE_DIVIDER = 5`; `ship_power_propagation` in five shipped files) but no define, string or observation states how they compose. |
| Y1287 | **CONFIRMED** | lead: same file reads as Y1245 | Each of the four named grant sites is quoted above with its file and line. |
| Y1288 | **CONFIRMED** | lead: read spec L859; read §2.7's 19 items | The spec says exactly this, and "unprobed" holds: none of §2.7's nineteen probes covers the only-under conditional (item 19 is the both-ends rule, item 8 the propagation threshold). Graded at stated (PROCESS / unsourced) scope. |

## §1.12 — the trade UI

| ID | verdict | method | evidence |
|---|---|---|---|
| Y421 | **CONFIRMED** | slice A: read spec L948-955 against frozen L913-914 | "**Aggregate trade view.** Provinces coloured by node, arrows between nodes, drawing `Φ_w`" — the rename holds and the arrow-weight sentence is withdrawn with nothing replacing it; what the section now says of `Φ_w` is that it "remains the drawn installed direction". |
| Y422 | **CONFIRMED** | slice A: read spec L957-962 | Matches word for word, including the "for the good" scoping of the sink test and "clears back to the aggregate view" as the clear target. |
| Y423 | **CONFIRMED** | slice A + lead: read spec L978-980; read `interface/tradeinterface.gui` | The not-representable verdict is reversed by swap-on-view exactly as claimed, and the six enumerated node-window fields all exist (see Y1290). The "thirty" is carried unchanged text, a round approximation of the 32-entry goods list. |
| Y424 | **CONFIRMED** | slice A + lead: read spec L951-955 and §2.6 L1426 | "**Every incident link is shown, with the value flowing in each direction along it**: two directed figures per physical link, never one net scalar." The engine's single stored per-link field survives at §2.6 ("Per-link values are written net to the engine's one per-link field"), so the reversal is a display change and the storage claim is not contradicted. |
| Y425 | **CONFIRMED** | slice A: read frozen L920-924 against spec L977-978 | Frozen: "Per-country effective trade power where eligibility differs by good. Shown as a value-weighted aggregate." Current: "**Still overlay-only**: per-country effective trade power where eligibility differs by good, shown as a value-weighted aggregate." The item and its value-weighted-aggregate treatment are word-for-word; only the heading carrying them changed, exactly as the census states. |
| Y426 | **CONFIRMED** | slice A: read spec L982-984 and §1.7 L778-793 | "No new art, sprites, shaders, or map-mode chrome. The UI changes are three, all on existing widgets: incoming-entry assignability (§1.7), the directional value panels, and per-good repopulation of the node and link fields." §1.7 confirms incoming-entry assignability is real content there ("what an incoming entry does — it must accept a merchant assignment rather than merely navigate"). |
| Y1289 | **CONFIRMED** | lead recheck: read `interface/mapicons.gui` | `total_value` exists inside both windows: `trade_small_mapicon` (windowType at L15) carries `name = "total_value"` at L49; `trade_big_mapicon` (windowType at L74) carries it at L120. |
| Y1290 | **CONFIRMED** (overturns slice A's PARTIAL) | lead recheck: read `interface/tradeinterface.gui` `TradeNodeInterface` windowType L53-481 in full; grepped every `name = "…value…"` in the file | All six named fields exist inside the node window at the quoted names: `incoming_value` L199, `local_value` L211, `total_value` L223, `outgoing_value` L235, `our_from_this` L248, `piracy_value` L267. Slice A returned PARTIAL on a seventh `_value`-suffixed widget, `light_ships_in_node_value` (L287). **I overturn that**: L281-286 shows it is paired with `guiButtonType { name = "light_ships_in_node", spriteType = "GFX_trade_ship" }` — it is a **light-ship count, not a value field** — and the spec's own predicate on the six ("every one now Σ_g of the per-good economy") excludes a ship count by construction. Slice A's finding rests on a name-suffix grep rather than on what the widget holds. (`goods_produced_value` at L590 is in `TradeCompanyNodeInterface`, a different window, and is out of scope.) The enumeration of six is correct. |
| Y1291 | **PARTIAL** (sustains slice A) | lead recheck: read `tradeinterface.gui` L245-254 and L714-723 (both node-window copies); grepped all of `localisation/` and `interface/` for `our_from_this` / `OUR_FROM_THIS` | The widget exists at both copies, but **no localisation key, tooltip, or `_label` sibling is attached to it** — the only occurrences of the token anywhere are the two gui declarations themselves. Its declaration carries only `position = {x = 388 y = 220}`, `font = "vic_22"`, `maxWidth = 240`, `text = "0"`, `format = centre`. By contrast the four node-total fields each pair with a `TN_*_VALUE` label textbox. **The exact disagreement:** the row is typed ENGINE with provenance "read from a file (`tradeinterface.gui`)", but the file gives the widget's *name and position* and does not state its semantics; "the country's own take" is an inference from the name ("our … from this") and the widget's prominent central placement. Plausible, but not what the cited file says. **What would settle it:** one node-window session comparing the displayed figure against the country's own trade income from that node. |
| Y1292 | **CONFIRMED** | slice A: read spec L952-953 | "every one now Σ_g of the per-good economy", referring to the six fields verified in Y1290. |
| Y1293 | **CONFIRMED** | slice A: read spec L951-952 | Exact quote match. |
| Y1294 | **CONFIRMED** | slice A: read spec L952-954 against §1.1 L139-141 | §1.1: "Every trade good has its own directed network over the same adjacency. Direction is computed, never authored" — each good's orientation derives from its own balance, so two goods sharing a link can legitimately run opposite ways. The cross-reference holds. |
| Y1295 | **CONFIRMED** | slice A: read spec L954-955 | "`Φ_w` remains the drawn installed direction; the directional panels are realized sums." |
| Y1296 | **CONFIRMED** | slice A: read spec L959-962 | Matches the claim's paraphrase faithfully. |
| Y1297 | **CONFIRMED** | slice A: read spec L960-961 | Parenthetical: "(`piracy_value` as the good's share of the node's skim)". |
| Y1298 | **CONFIRMED** | slice A: read spec L961-962 against §1.1's Phase 2 | §1.1 Phase 2 orients every support edge by its net flow — one direction per edge per good — so a per-good view carries one direction per edge by construction. |
| Y1299 | **CONFIRMED** | lead recheck: read `interface/tradeinterface.gui` L88-114 | `incoming_nodes_listbox` L90 with `position = { x = 10 y = -15 }`; `outgoing_nodes_listbox` L110 with `position = { x = 210 y = -15 }`. Same `y`, both above the panel's top edge (tabs across the top); `x = 10 < x = 210` gives incoming-left / outgoing-right, exactly as claimed. |
| Y1300 | **CONFIRMED** | slice A: read spec L966-968 | Exact quote match. Graded at stated (DESIGN) scope. |
| Y1301 | **CONFIRMED** | slice A: read spec L969-971 | Exact quote match. A forward design claim for the mod's own UI, not an assertion that vanilla's tabs carry an assign button today; its factual premise (link-end steering) is confirmed at Y1302. |
| Y1302 | **CONFIRMED** | slice A: read §1.7 L790-793 | §1.7: "A merchant assigned to link `{n,m}`: steers every good oriented `n → m`, is inert for every good oriented `m → n`" — assignment is to a link end and steers exactly the goods oriented away from that node, as the claim states. |
| Y1303 | **CONFIRMED** | slice A: read spec L970-971 against §1.7 L785-788 | §1.7: "what changes is **what an incoming entry does** — it must accept a merchant assignment rather than merely navigate." The cross-reference is accurate. |
| Y1304 | **CONFIRMED** | lead recheck: read `interface/tradeinterface.gui` L17-50, the whole `TradeNodeLink` windowType | Its only children are `guiButtonType { name = "NextNodeButton" … }` and `instantTextBoxType { name = "NextNodeButton_label" … }` — exactly one button and one label, nothing else. |
| Y1305 | **CONFIRMED** | slice A + lead: read spec L972-973; the file reads at Y1290 and Y1304 | The widget classes the claim calls "existing" are all confirmed present in `tradeinterface.gui`. |
| Y1306 | **CONFIRMED** | slice A: read spec L973-975; §2.7 item 7 L1450; §2.5 L1397-1400 | §2.7 probe 7 reads "**Render data.** Is arrow render state separate from the economic link?" — matching "arrow render state versus the economic link" exactly, and §2.7 records items 1–10 as unrun, consistent with calling it a feasibility dependency. §2.5 is the pattern-scanning / hooking section, so "added hooking surface under §2.5" is accurate. |
| Y1307 | **CONFIRMED** | slice A: read spec L978-979 | Exact quote match. |
| Y1308 | **CONFIRMED** | slice A: read spec L979-980 | The derivation holds: swap-on-view needs one reused slot rather than one field per good. |
| Y1309 | **CONFIRMED** | slice A: read spec L980-981, §2.9 L1556, §3.9 L1913 | All three sites agree: §1.12 "no negative net is ever displayed (§2.9, §3.9)"; §2.9 "decided by design (§1.12: both directions shown as positive flows, no net scalar displayed)"; §3.9 "§1.12 shows each link's two directions as positive flows, so no negative net is displayed". |

## §2.2 — solver

| ID | verdict | method | evidence |
|---|---|---|---|
| Y438 | **CONFIRMED** | slice C + lead: read spec L1061; Y1310's province-record census | Item 2's field list matches the claim exactly, and its parenthetical ("the engine's produced quantity lives at node level; no province record carries one") is independently confirmed at Y1310. |
| Y447 | **CONFIRMED** | lead: read `scripts/drain.py` L143, L203-259, L276-291; re-derived the arc count from `solver.EDGES_UND` | The flow sizing is exact: 80 nodes and 2 × 159 = **318** arcs. The sweep complexity is now right for the code that actually runs: `run_drain`'s default is `deterministic=True` (L276), which calls `sweep_priority` (L290) — a Kahn sweep with a `heapq` priority ready-queue (L209 `import heapq`; pushes at L232, L248, L255, L258; pop at L236). Each edge relaxation and free-adjacency check pushes at most once, so the queue takes O(V+E) operations at O(log V) each: **O((V+E) log V)**, exactly as written, and "priority sweep" names `sweep_priority` correctly. Round 9's refuted `O(V+E)` is repaired. *(Non-blocking note, recorded rather than deducted: the stall branch at L237-250 scans all of `core` once per stall, adding O(V) per promotion or fallback. On this field `measure6.py` reports `promotions / fallbacks (1, 0)`, so that path contributes 80 operations once — within a constant of the stated bound. Closes round 9's PARTIAL.)* |
| Y1203 | **CONFIRMED** | slice C: read `scripts/solver.py` (`province_table`), `scripts/provinces.py`, `measure6._inject_weights` | `provinces.py` builds the province dataset from `history/provinces` (docstring: "Build the 1444.11.11 province dataset from history/provinces"), which `solver.province_table()` consumes. Exactly **twenty** owned provinces have no `trade_goods` in the history reconstruction and are resolved from the save — "the twenty rolled trade goods" is exact, not approximate. The node `trade_goods_size` array read is `measure6._inject_weights()`, which §2.2 itself calls part of the reference implementation, so the added second save read is real. |

## §2.3 — constants and inputs

| ID | verdict | method | evidence |
|---|---|---|---|
| Y137 | **CONFIRMED** | lead: read `..\v4-owner-agnostic\scripts\audit_modifiers.py` in full; grepped it for `provincial_production_size`; enumerated `.py` files in `..\v3-owner-agnostic\` and `..\v5-owner-agnostic\` | All three halves hold. The three-sweep count is exact (see Y1144). The walked-past half is exact: `provincial_production_size` occurs **0** times in `audit_modifiers.py`, whose `WEALTH_KEYS` are `("trade_goods_size", "trade_goods_size_modifier", "local_tax_modifier", "trade_value_modifier")` and whose hit detection fires only on modifiers applied through `history/provinces` — so it loads the block holding `GP_COEFF` and never surfaces it. The v3.0/v5.0 half is exact: `..\v3-owner-agnostic\` ships **0** `.py` files anywhere in its tree, and of `..\v5-owner-agnostic\`'s 50 `.py` files **none** references both modifier directories. *(Closes round 9's PARTIAL.)* |
| Y1312 | **CONFIRMED** | lead + slice B: same file reads as Y1144 | The three are `audit_modifiers.py` (L21), `audit_alpha.py` (L16) and `audit_bands.py` (L15), each with an explicit loop over both directory names. |
| Y1313 | **CONFIRMED** | lead + slice B: grepped all 31 v4 scripts for single-file reads of the modifier files | Two qualify: `audit_seventh.py:125` `sm = pdx.load(os.path.join(EU4, "common", "static_modifiers", "00_static_modifiers.txt"))` and `validate_v4.py:147` `sm = io.open(os.path.join(EU4, "common", "static_modifiers", "00_static_modifiers.txt"), …).read()`. Neither references `event_modifiers` at all, so both read the same files without sweeping them. |
| Y1115 | **CONFIRMED** | lead: read spec L1236-1244; wrote and ran `scripts/r11/telescope.out`; ran `scripts/round6.py` | The qualification repairs round 9's refuted step. On a monotone stretch `Σ\|w[i+1] − w[i]\| = \|w[end] − w[start]\|` holds exactly (probe: `[0,3,7,12]` → sum 12, endpoint difference 12), and off it the identity fails (round 9's `[0,10,0]` → sum 20, endpoint difference 0; **1,951 of 2,000** random 5-node paths fail it). The scoped statement is therefore true where it is now scoped. The conclusion it supports reproduces: `round6.py` gives "shipped: 159 distinct edge costs of 159; goods with an alternative optimum 1 of 29 (paper)" against "structured: 159 distinct edge costs of 159; goods with an alternative optimum 11 of 29". *(Non-blocking note: "routings traversing similar wealth profiles" is looser than the exact condition, which is that the two routings' \|Δw\| steps sum equally; it is not false, and the measured 11-vs-1 result is what carries the argument. Closes round 9's PARTIAL.)* |
| Y1035 | **CONFIRMED** | lead: ran `scripts/p3_y1035.py` fresh (`scripts/r11/p3_y1035.out`); read its weighting base at L23-25 and L29 | Every figure reproduces: `self-coherence delta (full - first): edge-goods -0.04  value-weighted -0.10`. The "nothing else moves" tail also reproduces on both configurations — `Phi_w sinks genua,hangzhou`, `sinks/good 2-8 mean 3.69`, `acyclic 29/29`, `+/-1% noise edges moved (6 seeds) [0, 0, 0, 0, 0, 0]`. The rewording is faithful: the probe's weight is `VAL[g] = Σ val[g]` accumulated from `r["prod_income"]` = `gp × price`, i.e. `price(g)·Σ_m goods_produced(m,g)` — the orientation model's per-good trade value, which is what the new wording names explicitly. |
| Y1314 | **CONFIRMED** | lead: read spec L1271-1272; read `p3_y1035.py` L23-29 and `solver.build_sc` L196 | The pin is accurate and load-bearing. The probe's base is the orientation model's per-good trade value, not inject — and the two now differ measurably: with the old base the weighted self-coherence is **54.8%** (`p3_y1035.py`, shipped config) while with inject it is **54.9%** (`measure6.py`). Naming the base is exactly what stops §1.6's redefinition silently re-basing the 0.10. |
| Y1315 | **CONFIRMED** | slice B: read `common/disasters/decline_of_mali.txt` | L4 `has_dlc = "Origins"` and L37 `caravan_power = -0.33`, both inside the same `decline_of_mali = { … }` block — the potential requires the DLC, the effect carries the modifier. The value is exactly −0.33. |
| Y1316 | **CONFIRMED** (absence, graded on the search actually run) | slice B: grepped `common/`, `events/`, `decisions/`, `missions/` for `has_dlc` within 5 lines of `treasure_fleet` and `caravan_power`; checked all 16 files containing `caravan_power` and all 21 lines containing `treasure_fleet`; grepped for `has_dlc_feature` / `is_dlc_enabled` / `dlc_enabled` (0 hits install-wide); checked `defines.lua`'s `CARAVAN_*` entries | No `has_dlc` or equivalent gate sits near any `treasure_fleet*` or `caravan_power` token other than the already-known Mali disaster, and no alternate DLC-trigger syntax exists anywhere in the install. `CARAVAN_FACTOR`, `CARAVAN_POWER_MAX` and `CARAVAN_POWER_MIN` sit in `defines.lua` unguarded. The absence holds under this search. |
| Y1317 | **CONFIRMED** | slice B: inference graded against Y1316's result | `has_dlc` triggers are resolved by the script interpreter against engine/Steam ownership state, not by any data file; with no shipped gate on the grant mechanic or diversion, engine-side conditionality is what remains. Graded at stated (MODEL / unsourced) scope. |
| Y1318 | **CONFIRMED** | slice B: checked prior rounds and the spec for an executed toggle run | The spec names `dlc_load.json` toggling as the probe-class confirmation and does not claim the run has happened. Methodologically accurate as a specified probe. Graded at stated (PROCESS / unsourced) scope. |

## §2.4 — the tradenodes file

| ID | verdict | method | evidence |
|---|---|---|---|
| Y486 | **CONFIRMED** | lead: read `..\v2-drain\game-session.md` L152 and L184, and `..\v3-owner-agnostic\validation-v3.md` L464-478 | Every count now matches its source. `retention`: the session's own table records `0/80 differ` in both the noise control and the test — unchanged on 80 of 80. `total`: the table records `1/79 differ, max 0.012%` in both columns, so 78 of 79 — the denominator 79 is the source's, not a slip. The exception is named correctly: v3's audit identifies `zambezi` at 147.384 vs 147.366. The 159-errors half holds: "`logs/error.log` contains **exactly 159 lines**, one per backwards link, no more and no less". *(Closes round 9's PARTIAL, which was that a flat "unchanged" mis-stated `total`.)* |
| Y1319 | **CONFIRMED** | lead: same two sources | The one `total` exception is `zambezi`, drifting 0.012%, and it is within run-to-run variance rather than an effect of the permutation: the identical-vanilla control shows the *same* one node at the *same* 0.012%, and the permuted run reads 147.366, i.e. inside the null. |

## §2.6 — the tick

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1320 | **CONFIRMED** | slice D: read §2.6 L1407-1410 against §1.8 L810-824 | §2.6: "The origination is §1.8's `inject_g(n)`, read live at the tick and routed per §1.8 over the per-good graphs." §1.8 defines exactly that quantity and that live read. |
| Y1321 | **CONFIRMED** | slice D + lead: read §2.6 L1407-1410, §1.8 L814-815, §1.3 L342-351 | §2.6 states the annual basis with the ÷12 at the engine-write boundary; §1.8 and §1.3 both corroborate that the engine's node fields hold monthly twelfths, and Y1277's measurement finds them at exactly 12.00× on the reconciling nodes. |
| Y1322 | **CONFIRMED** | lead recheck: read §1.3 L342-352 | §1.3 does establish the relation from the engine's own tooltips, not from a save measurement: "The engine's own province tooltips give both as *annual* quantities divided by twelve for display. The tax tooltip reads … observed `Base: 0.49 (Yearly 6.00)` at `base_tax` 6 and `Base: 0.16 (Yearly 2.00)` at `base_tax` 2 … Both monthly figures being the annual value over twelve is what lets the annual forms add directly." §2.6's citation is accurate. |
| Y1323 | **CONFIRMED** | slice D: read §2.6 L1426; independent save read of `trade/node/incoming={…}` blocks | Beyond what the stipulated scope requires, the save corroborates it: each incoming record carries exactly one `value=` scalar per link, with no per-good breakdown and no second net-vs-gross field, and `tradeinterface.gui` carries one `TradeNodeLink` widget class per link. |
| Y1324 | **CONFIRMED** | slice D: read §2.6 L1426 against §1.12 L952-956 and L980-981 | Both sites agree that the display shows two positive directional figures and never the stored net. |
| Y1325 | **CONFIRMED** | slice D: read §2.7 item 4 L1460 | Item 4 verbatim: "**Negative link values.** Write one; observe arrow rendering and protect-trade allocation." Arrow rendering and protect-trade allocation are engine-side consumers of the stored per-link value, so §2.6's citation is accurate. |

## §2.7 — probes

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1326 | **CONFIRMED** (absence holds) | slice D, re-run independently by the lead: grepped `common/defines.lua`, `common/defines/`, and all `localisation/*_l_english.yml` for a both-ends rule | No define and no English string states it. The `defines.lua` hits for "both" are unrelated (HRE and peace-term comments); the only power-transfer strings are `TRADE_POWER_UPSTREAM` ("where it already has power" — §1.9's propagation qualifier, a different mechanic) and the steering strings. The one near-miss, `core_l_english.yml:281 TRANSFER_TRADE_POWER_TO_DESC` "in trade nodes where they both have power", is the diplomatic country-to-country relation, not the node-transfer rule. The claimed absence survives an adversarial re-search. |
| Y1327 | **CONFIRMED** | slice D: read §2.7 item 19 L1493-1496 | Verbatim: "Observe whether transfer enters a node where the receiving side holds power at only one end — one session, node window." Graded at stated (DESIGN) scope. |

## §2.8 — validation

| ID | verdict | method | evidence |
|---|---|---|---|
| Y572 | **CONFIRMED** | lead: fresh `measure6.py` run | §2.8's restatement now matches §1.6's: **54.9%** of edge-goods weighted by §1.8's `inject` and **55.1%** unweighted, both reproduced. The weighted-not-counted rule and the clustering prediction are carried unchanged. |
| Y1328 | **CONFIRMED** | slice D: read §2.8 L1542 against §1.8 L810-824 | §1.8 makes `inject` literally the engine's own produced trade value rather than an independent re-derivation, so "identical to vanilla's by construction" is accurate for the origination term specifically. |
| Y1329 | **CONFIRMED** | slice D: read §2.8 L1542 | Verbatim match; graded as a design expectation at stated scope. |
| Y1330 | **CONFIRMED** | slice D: read §2.8's economy-tab row L1521 and the income-balance row L1542 | The economy-tab row exists and carries exactly the tolerance/null-run statement cited: "stock trade values are not reproducible run to run … Any comparison against unmodded numbers needs a tolerance and a null run." |
| Y1331 | **PARTIAL** | lead probe `scripts/r11/L_localvalue.py`, run against `VANILLA_start.eu4`; tolerance sweep and truncation test; cross-checked against `scripts/r10/A_lv3.py` and slice C's independent parse | The measurement reproduces; the word **"exactly"** does not. Only **79** of the 80 nodes carry a `local_value` field (`cape_of_good_hope` has none, and an all-zero `trade_goods_size` array). Of those 79, **57** agree with `Σ trade_goods_size × price ÷ 12` to better than 0.001, and — decisively — **57** reproduce the printed value digit-for-digit under the engine's own truncation convention, the one §1.3 independently establishes for these displays (`trunc(recon/12, 3) == local_value`). 58 is reachable two ways, and **neither is 58 nodes reproducing `local_value` exactly**: either by admitting `philippines`, where the reconstruction is `3.010000` against the save's printed `3.009` — a genuine last-place disagreement that truncation would print as `3.010`, admitted only by a ≤0.001 *inclusive* band it sits exactly on — or by counting `cape_of_good_hope`, which has no `local_value` field at all, as a 0 = 0 match. Under literal equality only **13** of 80 match, and under 3-dp *rounding* only 33. **The exact disagreement: the exact-reproduction count is 57, not 58.** The rest of the row is unaffected — see Y1332. |
| Y1332 | **CONFIRMED** | lead probe `scripts/r11/L_localvalue.py`; New-World split computed over all 80 nodes | Both halves reproduce. Aggregate: `recon/12 = 326.43` against `engine local_value = 337.80`, a shortfall of **−3.37%**, which is the quoted 3.4% low. "Short almost entirely in New World nodes" holds quantitatively: of the 11.372 total shortfall, **10.558 (92.8%)** sits in New World nodes, the seven largest all being `chesapeake_bay` (2.96), `st_lawrence` (2.24), `ohio` (2.23), `mississippi_river` (1.27), `rio_grande` (0.68), `james_bay` (0.59), `california` (0.48). The entire non-New-World remainder is 0.814. |
| Y1333 | **CONFIRMED** | slice D: read §2.8 L1542 | Verbatim: "a known reference-side gap, recorded so nobody chases it as a model defect." Accurate to what it frames. |

## §2.9 — build order

| ID | verdict | method | evidence |
|---|---|---|---|
| Y580 | **CONFIRMED** | slice D: read §2.7 in full (L1428-1498) and enumerated its items | §2.7 now runs to nineteen items. Items 1-11 are the v1 probe set, which §2.7 records as unrun ("none of the ten has been run (§2.9 counts them open)"); item 12 is "dropped rather than run"; items 13-15 "were run … results folded into §1.9, §2.4 and §3.6"; items 16-19 are open. That is **fifteen open — 1-11 and 16-19** — matching §2.9's own count verbatim. Probe 19 is the new one, so the count moving from fourteen to fifteen is correct. |
| Y581 | **CONFIRMED** | slice D: read §2.9 L1556 against the frozen baseline's three-item list | The "Then" list now carries exactly two items ("write §1.10's classified call-site list into the spec; gate income balance on both metrics"); the former third item is removed and replaced by a separate declarative sentence recording the policy as already settled. |
| Y1218 | **CONFIRMED** | slice C: read §2.9 L1548 | Exact match, resting on the same facts as Y1203 — the twenty rolled goods and the node `trade_goods_size` arrays. |
| Y1334 | **CONFIRMED** | slice D: read §2.9 L1554 against §2.5 L1397-1401 | §2.5's scope is "Pattern scanning and function hooking, following the EU4dll precedent, which provides the attach scaffolding on this binary but nothing about trade structures" — locating new live fields is exactly what falls under it, so the citation is accurate. |
| Y1335 | **CONFIRMED** | slice D: read §2.9 L1556 | Verbatim match. |

## §3.2 — why monotonicity fails

| ID | verdict | method | evidence |
|---|---|---|---|
| Y591 | **CONFIRMED** | lead: fresh run of `scripts/r9/lead/L_rank2.py` | Both figures now reproduce to the quoted decimal: `unweighted mean : 16.6664%` → **16.7%**, and `value-weighted : 7.5944%` → **7.6%**. Round 9's refuted 17.1% / 7.7% are repaired. The qualitative half is unchanged and holds. *(Closes round 9's PARTIAL.)* |
| Y1336 | **CONFIRMED** | lead: read `scripts/solver.py:196`; read spec L1583-1584 | `build_sc` returns `V = np.array([PRICES[g] * world[gi] for gi, g in enumerate(GOODS)])` with `world = gp.sum(axis=1)` — i.e. exactly `price(g)·Σ_m goods_produced(m,g)`. The spec names this base and pins it against §1.6's redefinition, correctly. |
| Y1337 | **CONFIRMED** | lead: fresh run of `scripts/r9/lead/L_rank2.py` | Both figures are that script's outputs, reproduced above. |

## §3.4 — why supply is pre-modifier

| ID | verdict | method | evidence |
|---|---|---|---|
| Y637 | **CONFIRMED** | slice D + lead: read §3.4 L1724 against §1.3's formula | The re-subjecting is accurate and the logic holds: §1.3's `trade_value(p) = goods_produced(p) · price` excludes production efficiency and autonomy by construction, while vanilla's production income is defined by them, so substituting it would make `V_g` and the routed economy depend on owners' idea groups and autonomy. |
| Y1338 | **CONFIRMED** | slice D: read §3.4 L1720 | Verbatim match. |
| Y1339 | **CONFIRMED** | slice D: read §3.4 L1720 against §1.8 | Verbatim match, and §1.8 does state that `inject` carries vanilla's goods-produced modifiers (confirmed at Y1274). |
| Y1340 | **CONFIRMED** | slice D: read §3.1 Goal 7 and §3.4 L1720 | Goal 7 verbatim: "**The game's own numbers are the model's numbers.** Anything reading trade income reads the real one." §3.4's "Goal 7 makes the game's money the model's money" is a fair gloss of that, and the manufactory clause is §3.4's own illustration rather than an attribution to Goal 7's text. Goal 7 is not about something else. |
| Y1341 | **PARTIAL** (sustains slice D, on narrower grounds) | lead recheck: wrote and ran `scripts/r11/L_effaut.py` against `VANILLA_start.eu4`; read `common/static_modifiers/00_static_modifiers.txt`; counted `production_efficiency` occurrences in the save's `gamestate` | The **substance holds** — `inject` does inherit the exclusion. The **autonomy** half is verified two ways on the save, cleanly: across 245 singleton (node, good) cells r(local_autonomy, engine/model ratio) = **−0.097**, and the sample's 91.0%-autonomy extreme, Valencia (pid 213, glass), reproduces the autonomy-free prediction **exactly** (1.000 = 1.000), as do `ganges_delta` ivory at 61.0% and `chengdu` silk at 54.5%. **The production-efficiency half cannot be verified on the save**: `production_efficiency` occurs **0 times** in the save's `gamestate`, so it can only be proxied through owner `adm_tech`. That proxy points the right way — r(adm_tech, ratio) = **−0.207**, with the mean ratio *higher* at `adm_tech` 1 (1.52) than at `adm_tech` 3 (1.09), the opposite of efficiency entering — but it is confounded by the building and terrain modifiers that dominate the residual, and the 1444 tech spread is only 1–3. The strongest evidence for that half is structural, not save-based: `local_autonomy_multiplicative` scales `local_production_efficiency` and `local_tax_modifier` but never `trade_goods_size`, and the static `production_efficiency` block grants only `colonist_placement_chance`. **The exact disagreement:** "verified two ways **on the save**" overstates the efficiency half's provenance — one of the two ways is a file fact, and the save cannot carry the other. |
| Y1342 | **PARTIAL** (sustains slice D) | lead recheck: read §1.3's formula block L320-325, §1.6's `c_w` L557-563, and §3.4's parenthetical L1726-1727 | The **production-income** half is exactly true — nothing anywhere in the model computes production income. The **trade-value** half is not. §1.3 L323 defines `wealth(p) = tax_value(p) + trade_value(p)`, and §1.6 defines `c_w(n) = Σ_{p ∈ n} wealth(p)^α_Φ / Σ_{q ∈ world} wealth(q)^α_Φ`, so `Φ_w` sums and exponentiates a quantity of which `trade_value(p)` is a **literal additive summand** — a fact the spec's own §1.3 note, added by this same round's diff, states in as many words: "**The `trade_value(p)` defined here is a component of `wealth(p)`**". **The exact disagreement:** what the sentence can defensibly claim is that the aggregate is not *weighted by* either quantity — it is not the `V_g`-weighted aggregate v2.0 had, which is precisely what the rest of the parenthetical goes on to say. "Reads neither quantity" overstates that into an absence which §1.3 contradicts one hunk earlier. Rewording to "the aggregate graph is weighted by neither quantity" would close it. |
| Y1343 | **CONFIRMED** | slice D: read `..\v2-drain\per-good-trade-spec.md` L3-12 and L847-854 | v2.1's header: "**v2.1** replaces the installed aggregate: `Φ_ord` (the value-weighted marking order) gives way to **`Φ_w`**, DRAIN run once more with wealth itself as the good." And the superseded-entry list: "**`Φ_ord = Σ_g V_g·order_g` as the installed graph.** *(v2.0 entry, superseded in v2.1.)*" A `V_g`-weighted aggregate that was v2.0's and went at v2.1's `Φ_w` adoption — exactly as claimed. |

## §3.6 — why acyclicity is enforced

| ID | verdict | method | evidence |
|---|---|---|---|
| Y652 | **CONFIRMED** | lead: read all three `exception.txt` files in the OneDrive `crashes/` directory (`eu4_20260820_134250`, `_134617`, `_165621`) | Every element of the re-scoped claim reproduces in all three dumps. Stack overflow: L5 `Unhandled Exception C00000FD (EXCEPTION_STACK_OVERFLOW) at address 0x00007FF6DDE6A8B4`. Frame count: exactly **1002** `eu4.exe` frames, numbered 1…1002, in each dump. Identical: stripping the leading frame index leaves **1 distinct line** across all 1002 — `eu4.exe                  (function-name not available) (+ 0)`. No per-frame addresses: every frame reads `(+ 0)` with no address, so the trace cannot distinguish recursion from any other deep call chain — which is exactly what the new wording concedes. The claim now says what the dumps show and hedges what they do not. *(Closes round 9's PARTIAL, which was that "unbounded same-module recursion" outran the evidence.)* |

## §3.9 — why `Φ_w` is the installed graph

| ID | verdict | method | evidence |
|---|---|---|---|
| Y683 | **CONFIRMED** | lead: parsed `common/tradenodes/00_tradenodes.txt` for node blocks carrying no `outgoing` key; recomputed node wealth from `solver.ROWS` | Both halves now hold. Exactly **three** of the 80 node blocks carry no `outgoing` key, and they are `genua`, `venice`, `english_channel` — the three named. The withdrawn "biggest cities and richest areas" characterisation, which round 9 refuted on `venice`, is replaced by measured ranks that reproduce exactly (see Y1344-Y1346). *(Closes round 9's PARTIAL.)* |
| Y693 | **CONFIRMED** | slice D: read §3.9 L1908-1915 against §1.12 | The deferral is genuinely withdrawn and the two questions are separated; §1.12 does settle the display policy as claimed, and the disagreement rate remains a measured quantity (§2.8, Y572). |
| Y1344 | **CONFIRMED** | lead: recomputed node wealth as `Σ_{p ∈ n} (tax + trade_value)` from `solver.ROWS` | `english_channel` is rank **1** of 80 at 316.6 and `genua` rank **4** at 296.0 — two of the three authored ends in the top node-wealth ranks. |
| Y1345 | **CONFIRMED** | lead: same computation | `venice` is rank **21** of 80 at **180.6**, behind `mexico` (300.4), `gulf_of_siam` (297.9), `malacca` (295.2) and seventeen others. Both the rank and the figure reproduce exactly. |
| Y1346 | **CONFIRMED** | lead: same computation, graded at the row's MODEL scope | The measured half is exact: at rank 21 of 80, `venice` is demonstrably not the wealth pick, while the other two authored ends are ranks 1 and 4. *(Scope note: the "historical pick" half is the reading the measurement licenses, not itself a measurement — §3.9 presents it as a gloss on authored intent, which is the row's stated MODEL scope.)* |

## §3.14 — the AI

| ID | verdict | method | evidence |
|---|---|---|---|
| Y1347 | **CONFIRMED** | slice D: read §3.14 L2072 against §1.12 L966-975 | §3.14: "Candidates are (node, incident-link-end) pairs — both of the node window's tab groups, not `Φ_w`-outgoing links." §1.12's tab description ("panels in both groups carry the assign button", over `incoming_nodes_listbox` and `outgoing_nodes_listbox`) is what the cross-reference claims it is. |
| Y1348 | **CONFIRMED** | slice D: read §3.14 L2072 against §1.1's phases | §1.1's Phase 2 orients support edges by net flow and Phase 3 completes the free edges by the sweep — so each good's per-edge direction is the solver's own output, as claimed. |
| Y1349 | **CONFIRMED** | slice D: read §3.14 L2072 | Verbatim match; graded at stated (stipulated) scope. |
| Y1350 | **CONFIRMED** | slice D: read §3.14 L2069-2072 | Follows from the scoring construction: scoring sums the survival table over a candidate's active good set, so an empty set sums to zero. Graded at stated scope. |

## §3.16 — how the standard was refuted

| ID | verdict | method | evidence |
|---|---|---|---|
| Y790 | **CONFIRMED** (overturns slice B's PARTIAL) | lead recheck: read `patchnotes/1.8 Patchnotes.txt`; grepped 1.37.5's `common/` for any 75% overseas floor; read `common/defines.lua:1147` and `common/static_modifiers/00_static_modifiers.txt`; grepped `..\v1-laplacian\` | All three propositions the census row carries hold. **Real**: `1.8 Patchnotes.txt` L40 states the floor verbatim. **Historical**: no 75% overseas autonomy floor exists anywhere in 1.37.5 — the only `min_local_autonomy` values in `00_static_modifiers.txt` are **20** (L315, `pasha_state`), **50** (L349, `colonial_core`), **90** (L358, `territory_core`) and **90** (L364, `territory_non_core`), and a grep for `min_local_autonomy = 75` / `MIN_AUTONOMY = 75` / an `OVERSEAS.*AUTONOMY` define over all of `common/` returns nothing. **v1 carried it as current**: see Y1354. **1.37 floors file-exposed**: `defines.lua:1147 COLONY_MIN_AUTONOMY = 50,` plus the four static-modifier values above. Slice B returned PARTIAL on the "settling both ends" phrase, but that phrase belongs to `Y1352`'s proposition, not this row's — the census's claim column for `Y790` carries no dating citation, and the "historical" half is settled here directly by the floor's total absence from 1.37.5 independently of when it went. *(Closes round 9's PARTIAL, which was that no autonomy floor keyed on `overseas` exists in 1.37.5 to date — the rewrite now dates it from the archive instead.)* |
| Y1351 | **CONFIRMED** | lead recheck: read `patchnotes/1.8 Patchnotes.txt` (the archive is in the **EU4 install**, not the mod tree) | L40 reads verbatim: "- Overseas provinces now have a minimum autonomy of 75% instead of the 'distant overseas' penalty". Quote, file and line number all exact. |
| Y1352 | **PARTIAL** (sustains slice B) | lead recheck: read `patchnotes/1.16 Patchnotes.txt` L42; grepped the whole file for `overseas`, `autonomy`, `75` | The citation is exact: L42 reads "- Implemented a new system called \"States & Territories\", where states gives most benefits of being non-overseas, while territories have autonomy and is considered to be overseas for many rules." **But it does not establish supersession.** The 1.16 notes contain **zero** occurrences of "75", never mention the overseas floor, and nowhere say S&T replaces or removes it; the nearest supporting line is L244 "- Added min_local_autonomy modifier", which the claim does not cite. **The exact disagreement:** the cited line supports "States & Territories was introduced at 1.16" and nothing more, so §3.16's "the tree's own version archive settling both ends" overstates the 1.16 end — it is settled by inference (S&T's own description plus the floor's verified absence from 1.37.5's files), not by the archive. **What would settle it:** a patchnote line stating the removal, or the 1.16-era `common/` tree itself. |
| Y1353 | **CONFIRMED** | slice B: grepped `patchnotes/1.12 Patchnotes.txt` for `overseas`, `autonomy`, `minimum` | The three `overseas` hits are cultural acceptance (L64), the `is_overseas_subject` trigger (L376) and a port modifier (L433); the three `autonomy` hits are gold production (L74), sound effects (L265) and the `set_local_autonomy` effect (L304); `minimum` returns 0 hits. None is an overseas-floor change. |
| Y1354 | **CONFIRMED** | slice B: grepped `..\v1-laplacian\` | `v1-laplacian/per-good-trade-spec.md:60`: "Overseas provinces are floored at 75% autonomy, so they contribute roughly a quarter of their development's income." Stated as a current game fact with no historical caveat — exactly what the row asserts. |

---

## UNTESTABLE carry — the 8 prior rows

Per the brief these were not re-investigated. Each was examined only for whether anything in this
round's 31 hunks changed its testability.

| ID | § | testability changed this round? | basis |
|---|---|---|---|
| Y350 | §1.7 | **No — carried UNTESTABLE.** | §1.7 lives at L778-793 (old-file ~L742-757) and **no hunk falls in that range** — the diff jumps from `-670` to `-789`. §1.7 is byte-identical to the text round 9 graded. Still: only a debugger session or engine-code read would settle a one-merchant-per-country-per-node cap. |
| Y370 | §1.8 | **No — carried UNTESTABLE.** | The two outgoing-division rules are byte-identical between the frozen baseline (L803, L805) and the current spec (L837, L839) — verified by direct comparison, not by hunk arithmetic alone. §1.8's two hunks add the `inject` block and the §2.7-item-19 pointer; neither supplies a source for the split rule, and no new probe covers it (item 19 is the both-ends rule). |
| Y371 | §1.8 | **No — carried UNTESTABLE.** | Same two byte-identical lines; same gap. |
| Y372 | §1.8 | **No — carried UNTESTABLE.** | Same. |
| Y373 | §1.8 | **No — carried UNTESTABLE.** | Same. |
| Y505 | §2.6 | **No — carried UNTESTABLE.** | The three-pass sentence at L1405 is unmodified context in hunk `-1343,+1404`; the hunk only inserts the origination/annual-basis sentence after it. §2.7 still records "none of the ten has been run", so probes 1 and 2 — which name this exact pass structure as unresolved — remain unrun. |
| Y512 | §2.6 | **No — carried UNTESTABLE.** | The "Two deadlines, not one window" bullets at L1420-1421 are unchanged; §2.7 probe 3 remains unrun. |
| Y513 | §2.6 | **No — carried UNTESTABLE.** | Same bullets, same unrun probe 3. |

---

## Summary

### Freshly graded this round — 127 rows

| verdict | rows |
|---|---|
| CONFIRMED | 120 |
| PARTIAL | 7 |
| REFUTED | 0 |
| UNTESTABLE | 0 |
| **total** | **127** |

Breakdown by scope class:

| scope class | rows | CONFIRMED | PARTIAL |
|---|---|---|---|
| CHANGED | 28 | 28 | 0 |
| REWORDED | 3 | 3 | 0 |
| NEW | 95 | 89 | 6 |
| `Y375` (carried UNCHANGED, re-graded) | 1 | 0 | 1 |
| **total** | **127** | **120** | **7** |

**Every one of the 28 CHANGED and 3 REWORDED rows is CONFIRMED.** All 7 PARTIALs are on new or
re-graded material: 6 NEW rows and `Y375`.

Round 9 returned 14 PARTIALs. Thirteen of them were in this round's scope, and **twelve are now
closed** — `Y137`, `Y384`, `Y447`, `Y486`, `Y591`, `Y652`, `Y683`, `Y790`, `Y1099`, `Y1115`,
`Y1144`, `Y1195`, all now CONFIRMED against re-run instruments and re-read files. `Y375` is the one
that is not: its fix added disclosure (§1.8's pointer) and a scheduled probe (§2.7 item 19) rather
than evidence. The fourteenth, `Y483`, was untouched by the diff and carries.

### Carried from round 9 — 1,045 rows

| verdict | rows |
|---|---|
| CONFIRMED | 1,036 |
| PARTIAL | 1 (`Y483`, §2.3 — DLC-conditionality of caravan power / treasure-fleet diversion, not settleable from files) |
| REFUTED | 0 |
| UNTESTABLE | 8 (all re-examined above; none had its testability changed by this round) |
| **total** | **1,045** |

### Census total

| verdict | rows |
|---|---|
| CONFIRMED | 1,156 |
| PARTIAL | 8 |
| REFUTED | 0 |
| UNTESTABLE | 8 |
| **total** | **1,172** |

### The 7 fresh non-CONFIRMED verdicts

- **`Y375`** (§1.8) — PARTIAL. Trade-range half file-sourced; both-ends half still stated by no define, string or shipped file. The fix added §2.7 item 19, which schedules the measurement but does not supply it.
- **`Y1275`** (§1.8) — PARTIAL. The autonomy exclusion is a direct file fact and save-measured; the production-efficiency exclusion is not file-stated — no shipped file carries vanilla's trade-value construction, so the row's cited provenance does not exist for that half.
- **`Y1291`** (§1.12) — PARTIAL. `our_from_this` exists in `tradeinterface.gui` but carries no localisation key, tooltip or label sibling; "the country's own take" is an inference from the widget's name, not something the cited file states.
- **`Y1331`** (§2.8) — PARTIAL. The exact-reproduction count is **57 of 80**, not 58: only 79 nodes carry a `local_value` field, 57 reproduce it digit-for-digit under the engine's own truncation convention, and both routes to 58 require admitting a node that does not reproduce (`philippines`, 3.010000 vs printed 3.009) or one with no field at all (`cape_of_good_hope`).
- **`Y1341`** (§3.4) — PARTIAL. The substance holds and the autonomy half is verified two ways on the save; but `production_efficiency` appears **0 times** in the save, so "verified two ways on the save" overstates the efficiency half, whose real support is structural.
- **`Y1342`** (§3.4) — PARTIAL. "The aggregate graph reads neither quantity" is exactly true of production income and false of trade value: §1.3 L323 makes `trade_value(p)` a literal summand of the `wealth(p)` that §1.6's `c_w` sums — as §1.3's own note, added this same round, states.
- **`Y1352`** (§3.16) — PARTIAL. `1.16 Patchnotes.txt` L42 introduces States & Territories exactly as quoted, but the file contains no occurrence of "75" and never says S&T supersedes the overseas floor; the supersession is inference, not archive.
