# Round-11 fixes — draft for negotiation, nothing applied

Answering `validation-round10.md`: **1,156 CONFIRMED · 8 PARTIAL · 0 REFUTED · 8 UNTESTABLE** over
1,172 claims (120/7/0/0 on the 127 freshly graded; the rest carried from round 9). The spec is
frozen at `f9a70dfd859e1c97b266c35de4a1b228` (2,270 lines) until this list is negotiated to
unconditional confirmation and separately preconfirmed. The 8 UNTESTABLE rows carry unchanged —
the loop's floor. **R1 is untouched by every row.** Every row here is a phrasing or figure repair;
none changes a computation, a definition, or a design decision.

| # | ID | fix |
|---|---|---|
| A1 | Y1331 | §2.8's income-balance bullet: the reconstruction count corrected to what the instrument shows — the save-based reconstruction reproduces the engine's `local_value` **digit-for-digit on 57 of the 79 nodes that carry the field** (under §1.3's truncation convention; `cape_of_good_hope` carries no field), and runs **3.4% low** in aggregate, the shortfall concentrated in New World nodes. "58 of 80" goes — both routes to it admit a node that fails the test it names. The same count in §2.8's A8 sentence and any echo corrected together. |
| A2 | Y1342 | §3.4's parenthetical: "The aggregate graph reads neither quantity" is corrected to what §1.3's own note (added the same round) says — the aggregate reads **neither `V_g` nor production income**: `Φ_w` is built from §1.3's wealth field, which carries §1.3's `trade_value(p)` as a summand — the orientation-side quantity, not §1.8's `inject`. |
| A3 | Y1341, Y1275 | Both "outside vanilla's trade value" evidence statements — §3.4's "verified two ways on the save" and §1.8's "by vanilla's own construction" — restated at their actual evidence, in your prescribed form at both sites: the save's `local_value` identity — Σ_g `trade_goods_size`(n,g) × price(g) ÷ 12, which reproduces the engine's own field digit-for-digit on **57 of the 79 nodes that carry it** — has **no efficiency and no autonomy term in it**; the autonomy half is checked directly as well, with autonomy-heavy provinces reproducing the autonomy-free prediction exactly (**Barcelona, pid 213**, the `valencia`-node glass cell, at 91% `local_autonomy` — the same province §2.3's `GP_COEFF` table and §3.13's tooltip note already cite) and r(`local_autonomy`, engine/model ratio) ≈ −0.1 over the **245 singleton (node, good) cells**. §1.8's "by vanilla's own construction" becomes "by the identity's form, which admits no efficiency input". |
| A4 | Y1352 | §3.16 item 1's supersession clause marked as the inference it is: 1.16's L42 introduces States & Territories; that the system **supersedes** the 75% floor is an inference from the archive — territories carry autonomy in place of the overseas rule, and the floor appears in no later note — not a quoted sentence. The introduction quote (1.8 L40) stays verbatim. |
| A5 | Y1291 | §1.12's `our_from_this` gloss marked at its source: "read as the country's own take — an inference from the widget's name; no localisation key, tooltip or label sibling names it". |
| A6 | Y375 | The both-ends rule restated at its true evidence class, at **both** of its sites: §1.8's clause becomes, in your prescribed form, **the model's reading** — carried from v1 where its ancestor (C102) is recorded UNSOURCED and NEEDS_GAME; no define, string or searched file names it and **no session has observed it** — a probe-class fact under §3.16's own rule, carried as §2.7 item 19; and §2.7 item 19's own preamble ("§1.8 carries … from the trade interface's behaviour") is corrected in the same edit to match — "§1.8 carries the rule as the model's reading; no define, string, searched file or recorded session supports it" — so the two sites cannot disagree. No observation is asserted anywhere, because none is recorded in the lineage. |
| A8 | Y616, Y541, Y783 | The both-ends rule's **three downstream consequence sites** — §2.8's "withheld by range and the power-at-both-ends gate" (Y541, v1 C299), §3.2's "value only arrives where someone holds power at both ends of the link" (Y616, v1 C385), and §3.15's "the power-at-both-ends gate already withholds unworked corridors" (Y783, v1 C664) — each gain the minimal pointer "(both-ends: the model's reading, §1.8; probe §2.7 item 19)", so with §1.8 itself every site of the rule or its consequences names the one scope source. **The criterion, stated**: v1's dependency records show exactly these three derivations resting on C102 (C299 claims.md:518, C385 :619, C664 :963), all surviving in the current text; the census already carries all three (typed MODEL/MODEL/DESIGN, Y616 round-9 CONFIRMED as an algebraic derivation), so the markers add ancestry and probe pointers — they re-scope nothing and retire nothing. |
| A7 | Y483 | **Spec edit, the §1.9 treatment.** §2.3's "Treasure-fleet diversion and caravan power are both DLC-conditional" is marked at its actual scope: the conditionality is **engine-side, named by no shipped file** (the adjacent sentence already documents the absence — no file gates the grant mechanic or the diversion), and **unprobed pending the `dlc_load.json` toggle run**. The readable-when-inert half and the key-on-the-flag design instruction are unchanged. |

## What negotiation must settle

- Every row: CONFIRMED or REJECTED, no conditions; anything conditional comes back.
- A1's count: confirm 57-of-79 is the right statement of your own measurement, including the
  convention name and the `cape_of_good_hope` exclusion.
- A3, A6 and A7 carry the prescribed forms, with the preconfirmation pass's two repairs folded
  in: A3 names the 91%-autonomy province correctly (Barcelona, pid 213 — not the Valencia node's
  namesake province, whose autonomy is 1.0), and A6 covers **both** sites of the
  interface-behaviour phrasing (§1.8 and §2.7 item 19) so the fix cannot create a
  self-contradiction between them.
- A8's history, attributed correctly: the round-10 validator's sweep flagged §3.2's clause; the
  preconfirmation pass corrected the premise (the clause is censused as Y616, MODEL, round-9
  CONFIRMED) and supplied the complete four-site classification (§1.8 + three C102-descendant
  consequences, C299/C385/C664), which the row now carries with its criterion.
