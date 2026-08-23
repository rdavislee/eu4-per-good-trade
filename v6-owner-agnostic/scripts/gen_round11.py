# -*- coding: utf-8 -*-
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.normpath(os.path.join(BASE, '..', 'docs', 'audit'))  # audit records moved here
unch = json.load(io.open(os.path.join(BASE, 'unch.json'), encoding='utf-8'))

HEADER = u"""# Claims Delta — Per-Good Trade Network Spec, round 11 (v6.5 round-11 frozen → v6.6 current)

**Current document:** `per-good-trade-spec.md`, 2,283 lines, MD5 `48414cb316bd6b3c3355b1b87afdc3e2`.

**Prior inventory:** `claims-delta-round10.md` — the claim census taken of this document at 2,270
lines, MD5 `f9a70dfd859e1c97b266c35de4a1b228`. Its rows are the UNCHANGED (1046), REWORDED (3),
CHANGED (28) and NEW (95) tables — **1,172 live rows**, every one of them carried here. A row
entering the compressed UNCHANGED table below from one of round 10’s wider tables keeps that
table’s full wording rather than being re-truncated.

**Prior state compared against:** `per-good-trade-spec-v6.5-round11-frozen.md` (2,270 lines, MD5
`f9a70dfd859e1c97b266c35de4a1b228`), byte-exact and unedited.

**Change record:** `round11.diff`, 144 lines, **13 hunks**. Verified before use: `patch` applied to
the frozen file reproduces `per-good-trade-spec.md` at MD5 `48414cb316bd6b3c3355b1b87afdc3e2`,
byte-for-byte. An old→new line map built from the hunks was then checked line-by-line against both
files: **0 mismatches** across all 2,251 mapped old lines. 19 old lines are deleted or modified;
32 new lines are added. Every classification below is against the actual old text and the actual
new text, not against the prior census’s paraphrases.

**ID range found:** `Y001`–`Y1354`, **1,172 distinct IDs**, each used exactly once. 182 numbers in
that span are unused — the already-retired IDs of earlier rounds plus the numbers those rounds
skipped — and they stay unused. Highest number actually used: **1354**.

**First new ID assigned:** `Y1355` (new propositions run `Y1355`–`Y1372`, in document order).

**Counts:**

| status | rows |
|---|---|
| UNCHANGED | 1158 |
| REWORDED | 4 |
| CHANGED | 9 |
| REMOVED | 1 |
| NEW | 18 |
| **total rows** | **1190** |

**Notes.** (1) 1,172 live rows in, 1,171 live rows out (1158 + 4 + 9). One row retires: `Y1353`,
§3.16’s "1.12’s patch notes carry no overseas-floor change", whose clause hunk 13 deletes with
nothing asserting it in its place. No number was reused, and the retired number stays unused.
(2) The unit of classification is the claim’s own supporting words, not the physical line: a row
whose own words survive byte-identical is UNCHANGED even when the sentence around them was edited,
and the edit is then carried as its own CHANGED, REWORDED or NEW row. Every hunk this round
rewrites part of a sentence that other rows also sit on, so this rule does most of the work:
`Y375` and `Y376` keep §1.8’s gate sentence while its parenthetical is carried on `Y1158`,
`Y1159`, `Y1286` and `Y1360`; `Y1273`, `Y1274` and `Y1276`–`Y1285` keep §1.8’s `inject`
paragraph while its efficiency clause is carried on `Y1275` and `Y1359`; `Y1290` keeps §1.12’s
six-field list while the `our_from_this` gloss is carried on `Y1291` and `Y1361`; `Y1315`–`Y1318`
keep §2.3’s DLC evidence sentence while the axis sentence is carried on `Y483` and `Y1362`;
`Y1327` keeps probe 19’s method while its preamble is carried on `Y1326`; `Y576`, `Y1328`–`Y1330`,
`Y1332` and `Y1333` keep §2.8’s income bullet while its count is carried on `Y1331` and `Y1363`;
`Y637` and `Y1343` keep §3.4’s sentences while their evidence and parenthetical are carried on
`Y1341`, `Y1342` and `Y1364`–`Y1370`; `Y790` and `Y1351` keep §3.16 item 1 while its supersession
clause is carried on `Y1352`, `Y1371` and `Y1372`. This is the treatment round 7 gave `Y375` when
that same §1.8 parenthetical was first added. (3) The both-ends rule’s three consequence sites —
`Y541`, `Y616`, `Y783` — are REWORDED rather than UNCHANGED: each proposition is word-for-word,
and each sentence gains the pointer "(both-ends: the model’s reading, §1.8; probe §2.7 item 19)".
The pointer is recorded in the rewording column rather than as three NEW rows, because what it
asserts is already censused at `Y1158` and `Y1286`. (4) `Line` is the line in the current document
where the claim or its anchor sentence now sits; for a CHANGED row it is the line the changed text
now occupies. (5) Types are this delta’s five-way vocabulary (ENGINE / MODEL / MEASURED / DESIGN /
PROCESS), carried from the prior census for carried rows. (6) No instrument was edited this round:
`round11.diff` is the complete change record, and nothing sits outside this census on a model
script’s account. The three files this census added under `scripts/` — `prep_round11.py`
(line map and carry), `gen_round11.py` (emission) and `check_round11.py` (ID, wording, type and
line-range checks) — are census tooling, read nothing of the model and state no claim. (7) The
version stamp on L3 moved 6.5 → 6.6; the census has never carried a row for it.
(8) Two added phrases are deliberately given no NEW row because they restate, at the same site,
propositions the census already carries: §2.3’s "engine-side … named by no shipped file"
(`Y1316`, `Y1317`) and §3.16’s "quoted verbatim in the tree’s own version archive" (`Y1351`).
Both are recorded inside the CHANGED rows that carry their sentences.

## CHANGED — still asserted, but what it asserts moved

| ID | § | claim | status | old → new | type | provenance | line |
|---|---|---|---|---|---|---|---|
"""

CHANGED = [
    (u"Y1275", u"§1.8",
     u"Production efficiency and autonomy are outside vanilla’s trade value by the identity’s form, which admits no efficiency input.",
     u"old: \"production efficiency and autonomy are outside vanilla's trade value **by vanilla's own construction**\" → new: \"… outside vanilla's trade value **by the identity's form, which admits no efficiency input**; §3.4 carries the evidence note\"; the warrant moves from vanilla's construction to the form of the `local_value` identity, and the evidence itself is delegated to §3.4 (`Y1359`). The exclusion of efficiency and autonomy is unchanged",
     u"ENGINE", u"the `local_value` identity (§3.4)", 820),
    (u"Y1158", u"§1.8",
     u"The both-ends rule is the model’s reading; no define, string or searched file names it, and no session has observed it.",
     u"old: \"the both-ends rule is **stated from the trade interface's behaviour**; no define, string or searched file names it\" → new: \"the both-ends rule is **the model's reading** … no define, string or searched file names it **and no session has observed it**\"; the source moves from observed interface behaviour to the model's own reading, and the recorded absence of evidence widens from files to sessions. The no-define/string/file half is word-for-word. The v1 lineage the rewrite adds is carried on `Y1360`",
     u"ENGINE", u"unsourced", 852),
    (u"Y1291", u"§1.12",
     u"`our_from_this` is read as the country’s own take — an inference from the widget’s name.",
     u"old: \"`our_from_this` **(the country's own take)**\" → new: \"`our_from_this` **(read as the country's own take — an inference from the widget's name; no localisation key, tooltip or label sibling names it)**\"; the gloss moves from a flat field reading to an inference from the widget's name. The field's place in the six-field list is unchanged (`Y1290`); the absence of a naming key is carried on `Y1361`",
     u"ENGINE", u"read from a file (`tradeinterface.gui`); inference from the widget’s name", 960),
    (u"Y483", u"§2.3",
     u"DLC state is a third input axis: treasure-fleet diversion and caravan power are both DLC-conditional — an engine-side conditionality, named by no shipped file and unprobed pending the `dlc_load.json` toggle run — and caravan modifier values are readable even when inert, so the model keys on the DLC flag and never on the presence of a value.",
     u"old: \"Treasure-fleet diversion and caravan power are both **DLC-conditional, and** caravan modifier values are readable even when inert — so key on the DLC flag, never on the presence of a value\" → new: \"… both DLC-conditional **— an engine-side conditionality, named by no shipped file and unprobed pending the toggle run the evidence sentence below names —** and caravan modifier values are readable even when inert, so key on the DLC flag, never on the presence of a value\"; the conditionality is re-scoped at the sentence that asserts it — engine-side, named by no shipped file, unprobed. The readable-when-inert half and the key-on-the-flag instruction are word-for-word; the unprobed state is carried on `Y1362`",
     u"ENGINE", u"stipulated", 1319),
    (u"Y1326", u"§2.7",
     u"Probe 19 is the both-ends rule: §1.8 carries \"no transfer into a node where nobody holds power at both ends\" as the model’s reading; no define, string, searched file or recorded session supports it.",
     u"old: \"§1.8 carries … **from the trade interface's behaviour, named by no define, string or searched file**\" → new: \"§1.8 carries … **as the model's reading; no define, string, searched file or recorded session supports it**\"; the probe item follows §1.8's re-scoping (`Y1158`) so the two sites cannot disagree, and the evidence absence widens to recorded sessions. The probe's method is unchanged (`Y1327`)",
     u"DESIGN", u"§1.8", 1503),
    (u"Y1331", u"§2.8",
     u"The save-based reference reconstruction, Σ `trade_goods_size` × price ÷ 12, reproduces the engine’s `local_value` digit-for-digit on 57 of the 79 nodes that carry the field, under §1.3’s truncation convention.",
     u"old: \"reproduces the engine's `local_value` **exactly on 58 of 80 nodes**\" → new: \"reproduces the engine's `local_value` **digit-for-digit on 57 of the 79 nodes that carry the field** (under §1.3's truncation convention; `cape_of_good_hope` carries no field)\"; the count moves from 58-of-80 to 57-of-79, the match is named digit-for-digit and scoped to a stated truncation convention, and the denominator drops the node that carries no field (`Y1363`). The 3.4%-low half (`Y1332`) and the known-gap note (`Y1333`) are unchanged",
     u"MEASURED", u"the 1444 save", 1551),
    (u"Y1341", u"§3.4",
     u"`inject` inherits the production-efficiency and autonomy exclusion §3.4 demands; the evidence, at its class, is the save’s `local_value` identity, which has no efficiency and no autonomy term in it, with the autonomy half checked directly as well.",
     u"old: \"`inject` inherits exactly the exclusion this section demands, **by vanilla's own construction (verified two ways on the save)**\" → new: \"`inject` inherits exactly the exclusion this section demands. **The evidence, at its class: the save's `local_value` identity … has no efficiency and no autonomy term in it; and the autonomy half is checked directly as well**\"; the by-construction warrant and the unquantified \"verified two ways\" are replaced by the two named checks, whose statement and figures are carried on `Y1364`–`Y1369`",
     u"MEASURED", u"the 1444 save", 1734),
    (u"Y1342", u"§3.4",
     u"The aggregate graph reads neither `V_g` nor production income: `Φ_w` is built from §1.3’s wealth field.",
     u"old: \"(The aggregate graph reads **neither quantity**: `Φ_w` is built from §1.3's wealth field\" → new: \"(The aggregate graph reads **neither `V_g` nor production income**: `Φ_w` is built from §1.3's wealth field **— which carries §1.3's `trade_value(p)` as a summand, the orientation-side quantity, not §1.8's `inject` —**\"; the two excluded quantities are named instead of referred to, and the wealth field is qualified by what it does carry (`Y1370`). The `Φ_w`-from-§1.3's-wealth-field half is word-for-word",
     u"MODEL", u"§1.3; §1.6", 1736),
    (u"Y1352", u"§3.16",
     u"The 75% floor was superseded at 1.16 — an inference from the tree’s version archive rather than a quoted sentence — where `1.16 Patchnotes.txt` L42 introduces States & Territories.",
     u"old: \"**superseded by States & Territories at 1.16, the tree's own version archive settling both ends** (… `1.16 Patchnotes.txt` L42 introduces States & Territories …)\" → new: \"superseded at 1.16 — **where the supersession is an inference from that archive rather than a quoted sentence**: `1.16 Patchnotes.txt` L42 introduces States & Territories, **whose territories carry autonomy in place of the overseas rule, and the floor appears in no later note**\"; the supersession moves from a fact the archive settles to an inference drawn from it, and the inference's two premises are carried on `Y1371` and `Y1372`. The L42 read is word-for-word",
     u"ENGINE", u"read from a file (`patchnotes/1.16 Patchnotes.txt`); inference from the tree’s patchnote archive", 2218),
]

REWORDED_HDR = u"""
## REWORDED — same proposition, different words

| ID | § | claim | status | rewording | type | provenance | line |
|---|---|---|---|---|---|---|---|
"""

REWORDED = [
    (u"Y1159", u"§1.8",
     u"The both-ends rule is a probe-class fact under §3.16’s own rule, and is recorded as such.",
     u"\"a probe-class fact under §3.16's own rule, **recorded as such and carried as §2.7 item 19**\" becomes \"a probe-class fact under §3.16's own rule, **carried as §2.7 item 19**\"; the probe-class classification is word-for-word, and the dropped \"recorded as such\" names the very recording that survives beside it — the §2.7 carry, itself censused at `Y1286`",
     u"PROCESS", u"§3.16", 854),
    (u"Y541", u"§2.8",
     u"Malacca to Cape pre-1500: the corridor is withheld by range and the power-at-both-ends gate, not by direction.",
     u"\"Corridor withheld by range and the power-at-both-ends gate, not by direction\" becomes \"Corridor withheld by range and the power-at-both-ends gate **(both-ends: the model's reading, §1.8; probe §2.7 item 19)**, not by direction\"; the proposition is word-for-word, and the inserted pointer names the gate's scope source and its probe (one of the three consequence sites of note 3)",
     u"MODEL", u"stipulated", 1516),
    (u"Y616", u"§3.2",
     u"Peripheral termini still exist — the LP’s branch ends are consumed at the end of the line — and value only arrives where someone holds power at both ends of the link.",
     u"\"value only arrives where someone holds power at both ends of the link\" becomes \"… at both ends of the link **(both-ends: the model's reading, §1.8; probe §2.7 item 19)**\"; the sentence is otherwise word-for-word, and the inserted pointer names the gate's scope source and its probe (one of the three consequence sites of note 3)",
     u"MODEL", u"algebraic derivation", 1693),
    (u"Y783", u"§3.15",
     u"Emission-time pruning of near-flat links is rejected: peripheral termini are intended consumption, and the power-at-both-ends gate already withholds unworked corridors, with the §3.13 calibration option’s twig tolerance a bounded measured exception.",
     u"\"the power-at-both-ends gate already withholds unworked corridors\" becomes \"the power-at-both-ends gate **(both-ends: the model's reading, §1.8; probe §2.7 item 19)** already withholds unworked corridors\"; the rejection, its two reasons and the twig-tolerance exception are word-for-word, and the inserted pointer names the gate's scope source and its probe (one of the three consequence sites of note 3)",
     u"DESIGN", u"stipulated", 2190),
]

REMOVED_BLOCK = u"""
## REMOVED — the document no longer makes this claim

| ID | § | claim (census wording) | what removed it | type | provenance (was) | line |
|---|---|---|---|---|---|---|
| Y1353 | §3.16 | 1.12's patch notes carry no overseas-floor change. | hunk 13 (old L2204–L2208 → new L2216–L2221) rewrites item 1's patch-archive parenthetical and drops the clause "1.12's notes carry no overseas-floor change" outright. What stands in its place — "the floor appears in no later note", censused as `Y1372` — is scoped to notes after 1.16 and asserts nothing about 1.12. No other sentence in the document mentions 1.12 | ENGINE | was: read from a file (the tree's patchnote archive) | — |

"""

UNCH_HDR = u"""
## UNCHANGED — still asserted, in substance and in figure (compressed)

| ID | § | claim | type | line |
|---|---|---|---|---|
"""

NEW_HDR = u"""
## NEW — propositions the prior census does not cover (`Y1355`–`Y1372`, document order)

| ID | § | claim | status | type | provenance | line |
|---|---|---|---|---|---|---|
"""

NEW = [
    (u"Y1355", u"§0", u"v6.6 is a phrasing round: no computation, definition or design moves.", u"PROCESS", u"stipulated", 95),
    (u"Y1356", u"§0", u"v6.6 corrects one figure to its instrument — the reference reconstruction’s 57-of-79 count.", u"PROCESS", u"§2.8", 95),
    (u"Y1357", u"§0", u"v6.6 re-scopes seven statements at their evidence class: §3.4’s aggregate parenthetical and save-evidence note, §1.8’s `inject` evidence and both-ends rule, §3.16’s supersession inference, §1.12’s `our_from_this` gloss and §2.3’s DLC conditionality.", u"PROCESS", u"§1.8; §1.12; §2.3; §3.4; §3.16", 96),
    (u"Y1358", u"§0", u"v6.6 points the both-ends rule’s three consequence sites at their one scope source.", u"PROCESS", u"§1.8; §2.7 item 19", 99),
    (u"Y1359", u"§1.8", u"§3.4 carries the evidence note for the efficiency-and-autonomy exclusion.", u"PROCESS", u"§3.4", 821),
    (u"Y1360", u"§1.8", u"The both-ends rule is carried from v1, where its ancestor C102 is recorded UNSOURCED and NEEDS_GAME.", u"PROCESS", u"`../v1-laplacian/` (C102)", 852),
    (u"Y1361", u"§1.12", u"No localisation key, tooltip or label sibling names `our_from_this`.", u"ENGINE", u"a file/string search that found nothing", 960),
    (u"Y1362", u"§2.3", u"The engine-side DLC conditionality is unprobed, pending the `dlc_load.json` toggle run.", u"PROCESS", u"unsourced", 1319),
    (u"Y1363", u"§2.8", u"`cape_of_good_hope` carries no `local_value` field, which is why 79 of the 80 nodes carry it.", u"ENGINE", u"read from a file (the 1444 save)", 1551),
    (u"Y1364", u"§3.4", u"The save’s `local_value` identity is Σ_g `trade_goods_size`(n,g) × price(g) ÷ 12, and it reproduces the engine’s own field digit-for-digit on 57 of the 79 nodes that carry it.", u"MEASURED", u"the 1444 save", 1734),
    (u"Y1365", u"§3.4", u"That identity has no efficiency and no autonomy term in it.", u"MODEL", u"the `local_value` identity", 1734),
    (u"Y1366", u"§3.4", u"The autonomy half is checked directly as well: autonomy-heavy provinces reproduce the autonomy-free prediction exactly.", u"MEASURED", u"the 1444 save", 1734),
    (u"Y1367", u"§3.4", u"Barcelona, pid 213, is the `valencia`-node glass cell, at 91% `local_autonomy`.", u"MEASURED", u"the 1444 save", 1734),
    (u"Y1368", u"§3.4", u"Barcelona is the province §2.3’s `GP_COEFF` table and §3.13’s tooltip note already cite.", u"PROCESS", u"§2.3; §3.13", 1734),
    (u"Y1369", u"§3.4", u"r(`local_autonomy`, engine/model ratio) ≈ −0.1 over the 245 singleton (node, good) cells.", u"MEASURED", u"the 1444 save", 1734),
    (u"Y1370", u"§3.4", u"§1.3’s wealth field carries §1.3’s `trade_value(p)` as a summand — the orientation-side quantity, not §1.8’s `inject`.", u"MODEL", u"§1.3; §1.8", 1737),
    (u"Y1371", u"§3.16", u"States & Territories’ territories carry autonomy in place of the overseas rule.", u"ENGINE", u"read from a file (the tree’s patchnote archive)", 2220),
    (u"Y1372", u"§3.16", u"The 75% overseas floor appears in no patch note later than 1.16.", u"ENGINE", u"read from a file (the tree’s patchnote archive)", 2221),
]

FOOTER = u"""
---

**Summary.** U 1158 / RW 4 / C 9 / R 1 / N 18 — 1190 rows in all; highest ID used `Y1372`.

**Work list for the delta-scoped validation.** The prior rows whose verdict-relevant text changed
this round, and which the next round grades alongside the 18 NEW rows (`Y1355`–`Y1372`), are the
9 CHANGED — `Y483`, `Y1158`, `Y1275`, `Y1291`, `Y1326`, `Y1331`, `Y1341`, `Y1342`, `Y1352` — and
the 4 REWORDED — `Y541`, `Y616`, `Y783`, `Y1159`. 13 carried rows in all; every other carried row
is UNCHANGED and out of scope. `Y1353` is retired and is graded by nobody.
"""

out = [HEADER]
for i, s, c, d, t, p, l in CHANGED:
    out.append(u"| %s | %s | %s | CHANGED | %s | %s | %s | %d |\n" % (i, s, c, d, t, p, l))
out.append(REWORDED_HDR)
for i, s, c, d, t, p, l in REWORDED:
    out.append(u"| %s | %s | %s | REWORDED | %s | %s | %s | %d |\n" % (i, s, c, d, t, p, l))
out.append(REMOVED_BLOCK)
out.append(UNCH_HDR)
for r in unch:
    out.append(u"| %s | %s | %s | %s | %d |\n" % (r['id'], r['sec'], r['claim'], r['typ'], r['new']))
out.append(NEW_HDR)
for i, s, c, t, p, l in NEW:
    out.append(u"| %s | %s | %s | NEW | %s | %s | %d |\n" % (i, s, c, t, p, l))
out.append(FOOTER)

io.open(os.path.join(AUDIT, 'claims-delta-round11.md'), 'w', encoding='utf-8').write(u"".join(out))
print("written", len(unch), "unchanged rows")
