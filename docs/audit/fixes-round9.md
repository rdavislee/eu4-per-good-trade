# Round-9 fixes — draft for negotiation, nothing applied

Answering `validation-round8.md`: **1,028 CONFIRMED · 18 PARTIAL · 1 REFUTED · 7 UNTESTABLE** over
1,054 claims. The spec is frozen at `88da3fe76244ab4f43ef41edf3e50768` (2,165 lines) until this
list is negotiated to unconditional confirmation and separately preconfirmed. The 7 UNTESTABLE rows
are all probe-class engine facts whose rows name what would settle them — Y483 a `dlc_load.json`
toggle run, Y505/Y509/Y512/Y513 the §2.6 tick-structure probes (§2.7 items 1–3), Y728 probe 8,
Y754 a live before/after power read — the loop's floor, not its backlog; none is addressed here.
R1 is untouched by every row.

## A. The refutation

| # | ID | fix |
|---|---|---|
| A1 | Y790 | §3.16 item 1: "the 90/20/0 floors are not in `defines.lua` or any file that has been searched" is false and is corrected: the floors **are** file-exposed, as static modifiers — `common/static_modifiers/00_static_modifiers.txt` carries `min_local_autonomy = 20` (pasha_state, L315), `= 50` (colonial_core, L349) and `= 90` (territory_core L358 and territory_non_core L364) — the same file the model reads for `GP_COEFF` and the four province-state modifiers. The corrected item keeps the v1 lesson (the 75% overseas floor is pre-Common-Sense; `COLONY_MIN_AUTONOMY = 50` is the defines-side value) and adds the sharper one: the "not in any file that has been searched" defence was itself the failure mode the item describes — the values sat in a file already read for other constants. **The applied text names 20/50/90 as the file-exposed floors and 0 as the no-floor case**: no `min_local_autonomy = 0` exists anywhere, so "the 90/20/0 floors are file-exposed" would be a new over-claim and is not written. |

## B. Figures corrected to their instruments

| # | ID | fix |
|---|---|---|
| B1 | Y134 | §2.2's v5.0 parenthetical: "varies from 0 to 11 across replicates" is outrun — `scripts/val62check/p3_time_p4.out` records a **12 of 12** batch — and becomes: the inside-count has run **from 0 to 12 of twelve** across recorded replicates (0 in `scripts/r8/p3_time.out` among others, 12 in `scripts/val62check/p3_time_p4.out`). Because 0 and 12 are the floor and the ceiling of a count out of twelve, no endpoint is left to outrun. **No interior set is enumerated**: successive audit passes keep recording interior values a prior pass had not collected — the preconfirmation sweep alone added 2, 5 and 6 to what negotiation had — so an enumerated set is the same outrunnable figure the parenthetical exists to retire. The refutation-by-variance framing is unchanged. |
| B2 | Y1012 | Both fingerprint sites — §2.1's randomness row and §2.8's determinism row — correct "five `PYTHONHASHSEED` values including `random`" to **six** (0, 1, 2, 42, 12345, `random`), which is `fingerprint6.py`'s own documented sweep. |
| B3 | Y1021 | Both quantisation sites — §2.1's paragraph and §2.7 item 16 — replace the 495-value sample with the full-sweep census: `scripts/val62p4_quant.py` (fresh output `scripts/r8/quant.out`) sweeps all six named fields of the save's `trade={}` block and finds **3,354** values in `VANILLA_start.eu4` and **3,810** in `Castile1444_12_22.eu4`, **0 off-grid in both** — one current, reproducible figure rather than a stale sample (R3). |
| B4 | Y114 | §1.6's `genua` sentence enumerates all five in-arcs — `valencia`, `tunis`, `ragusa`, `champagne`, `alexandria` — so the regional gloss covers what the measurement shows: the western Mediterranean, the Adriatic, the Rhône corridor **and Alexandria** carry power into it. |
| B5 | Y1212 | §2.5: the build attribution is split to what each source holds — build `835bfdf8`, the hash constant across `eu4_rev.txt` (which carries the hash alone, no timestamp) and all three crash dumps, whose metadata stamps it `2024-10-03 10:50:26 +0200`. |

## C. Scope and characterisation

| # | ID | fix |
|---|---|---|
| C1 | Y695, Y1232 | §3.10: peace valuation moves to the file-evidenced half — `defines.lua` carries `PEACE_TERMS_TRADE_POWER_VALUE_MULT = 0.1` with its comment stating the node-value rule ("AI desire … is multiplied by this for each 0.1 trade value in shared nodes"), with `_MAX = 2.0` and `_NO_TRADE_INTEREST_MULT = 0` alongside. AI light-ship building and trade-league behaviour remain the engine-internal readers, and the missing-enumeration clause now covers those **two**, not three. |
| C2 | Y515 | §2.7's preamble: "Items 1–10 are the v1 probe set, settled with a debugger on a vanilla install in one session" reads as a result and is a plan — corrected to "**to be settled** with a debugger on a vanilla install in one session"; none of the ten has been run, which §2.9's open count already states. |
| C3 | Y549 | `tools` is not an EU4 trade good (absent from `00_tradegoods.txt` and `00_prices.txt`) — and it occurs at **two sites**, both fixed: §2.8's Caribbean row's imports become goods the install ships, **cloth, iron, wine**; and §3.3's "a genuine consumer of cloth and tools" becomes "a genuine consumer of **cloth and iron**". Y549 graded only the §2.8 row; the second site is the same defect and leaving it would keep a non-existent good in the document. |
| C4 | Y384 | §1.9's ship-propagation bullet marks its composition as the model's reading: the ship-propagation modifier is file-confirmed and the propagation share is a define, but **no file, string or observation states how they compose** — "share multiplied by that modifier" is carried as the derived reading it is, not as an engine fact. |
| C5 | Y173 | §3.5's harness note, two accuracy fixes: `verify6.py` checks the census total **and its `events/` component** against computed values, carrying the rest of the by-tree breakdown (missions 14, common 1, history 53) only as a literal-string presence check — stated exactly so, in the note whose job is recording what the harness does not cover; and `measure6.py`'s walker swallows parse failures with `except Exception: pass`, not "a bare `except`". |
| C6 | Y749 | §3.14: the residual clause "and its residuals sit at 1e-16, one ULP of a double (§3.10)" is dropped — §3.10 quotes no residual figure of its own (it prints v1–v4's only as retirement history) and states why quoting one is wrong, so the citation dangles and the figure is exactly what R3 retires. The MB arithmetic and the v1/v2 attribution stand (confirmed). |
| C7 | Y805 | §3.16: "A localisation string describes intent, not behaviour" is recast as the rule of evidence it is — demonstrated by the one cautionary case (`TRADE_POWER_UPSTREAM_DESC`) and **adopted as policy** for how string-sourced facts are graded, not asserted as an empirical property of every string; §0's no-empirical-absolutes convention applies to this sentence like any other. |
| C8 | Y1142, Y1185 | §0's lineage parenthetical: the seven IDs it names do not match the audit record and are replaced by what `scripts/r7/out/S01.md` (row Y214) actually samples — **C407, C101, C037/C038, C128/C130/C131/C132, recorded there as 6 of 60** — none missing; "no exhaustive re-check has been made" stays. The parenthetical cites the record file so the sample is checkable. |
| C9 | Y1081 **[instrument+spec]** | §1.1's parenthetical: "the figure had been quoted since v2 with nothing in the tree that computed it" is corrected — `final.py`'s **V035** runs the same sweep-only scheduler permutation in-tree at width 2 (its `sweep_priority(pid=)` re-keys only the sweep, the same construction), so the honest history is: quoted since v2, computed in-tree at width 2 by V035, widened to the cited 145 by the `props6.py` loop. **`props6.py`'s comment is corrected in the same pass** — its "lives nowhere else in the tree" overstates identically. |
| C10 | Y258, Y037 | **Census hygiene — no spec edit.** Y258's census row mis-cites §2.2 where the spec text (L216) correctly says §2.2a; Y037's census row carries pre-round-8 line references (L49-50/L349/L955; the live sites are L55/L370/L994-996). Both rows are corrected at the next claims-delta pass; the spec is untouched, and both claims grade against the spec's actual text. |

## What negotiation must settle

- Every row: CONFIRMED or REJECTED, no conditions; anything conditional comes back.
- B1 and C5 carry the negotiated replacements: B1 claims the 0-to-12 range with the endpoint
  sources only (`scripts/r8/p3_time.out` for 0, `scripts/val62check/p3_time_p4.out` for 12) and
  enumerates no interior set — the preconfirmation pass refuted an enumerated set inside a single
  sweep, which is the demonstration; C5 scopes the harness to "total and `events/` component
  against computed values, the rest a literal-string presence check".
- B3 now embeds the instrument and censuses you named (`scripts/val62p4_quant.py`,
  `scripts/r8/quant.out`, 3,354 / 3,810, 0 off-grid).
- C8 mirrors the record's own accounting (6 of 60, with the IDs it lists), the reading you stated.
- C9 pairs a spec correction with an instrument-comment correction, as round 8's C10 did; confirm both halves or neither.
- C10 asks you to confirm that the spec text is correct at both sites and the census rows are the error — i.e. that no spec edit is the right treatment.
