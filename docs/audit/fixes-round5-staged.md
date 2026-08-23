# Round-5 fixes — staged, not applied

**The spec is frozen at `f597de9d10ade20b0e69c5089932e8b4` while validation round 4 grades it.**
Nothing here is in the document. Editing between an extraction and the validation that grades it is
what invalidated the round-five inventory, so findings wait here and go in as one batch afterwards.

---

## Already known before the gate

**S1 — §0's coverage sentence has no verifiable content, and its ratio is wrong.** The round-7
extraction classified it `verified (method unstated)` — the only such row in 188 — because it names
neither a script nor a count:

> "a script is named about a dozen times against roughly three times that many unguarded figures, and
> some of the most recent additions carry neither a guard nor an attribution."

Measured now:

| quantity | value |
|---|---|
| distinct scripts named in the spec | **7** |
| total script citations | **15** |
| figures confirmed guarded (uniquely locatable) | **8 of 9** |
| figures not confirmed guarded | **≈26** — 1 locatable miss plus 25 whose value occurs more than once, so a single-site mutation cannot be aimed at them |

So "about a dozen" is defensible for 15, but "roughly three times that many" implies ~45 unguarded
against a real figure nearer 26 — **under twice, not three times.**

**Proposed replacement.** Drop the ratio and point at the tool, since any count here moves with every
edit to the document (it already moved 5/11 → 4/10 → 8/10 → 8/9 within this version):

> Under half of the figures it prints are guarded. `scripts/coverage6.py` reports the current split,
> and it should be re-run rather than quoted, because the number moves with every edit. Some figures
> carry a script attribution instead of a guard, and a few of the most recent additions carry
> neither.

That keeps what is true and load-bearing — coverage is partial, and the tool that measures it is in
the tree — without asserting a proportion that will be stale by the next round.

---

## To be added when validation returns

Its REFUTED and PARTIAL rows, negotiated with the agent, then measured by a separate
pre-confirmation agent before any of it is written.

---

## From validation round 4 (168 CONFIRMED / 19 PARTIAL / 1 REFUTED on 188 claims)

Verified independently before staging. Nothing here is applied; the spec is frozen at
`f597de9d10ade20b0e69c5089932e8b4`.

### The refutation

**S2 — Y134, an attribution error, and the fix restores a figure rather than removing one.** §2.4 says
the 580-of-580 relabelling sweep and the arc-permutation result came from scripts "never shipped", and
withdraws them. **`v5-owner-agnostic/scripts/_audit_b_1444perm.py` exists** (4,883 bytes) and contains
the sweep. A real result was deleted for a false reason. Restore it with the correct citation, and
keep the arc-permutation half, which was correct as written.

### The one model omission

**S3 — Y047, a fifth province-state modifier.** `unrest` grants `local_tax_modifier = -0.02` in
`common/static_modifiers/00_static_modifiers.txt` and is province state, so §1.3's table is short by
one row. Measured from the save's `gamestate`:

| | |
|---|---|
| counted provinces with unrest > 0 at 1444 | **21** |
| unrest values present | 4.834, 7.834, 9.834, 14.834 |
| tax forgone at −0.02 per point | **12.23 ducats** |
| share of world wealth | **0.115%** |

This is the first genuine *omission* from the wealth model since option (c) was adopted; every other
correction this version has made was to a figure or a quantifier. Adding it also adds a **second**
unverified scaling law — the model already assumes `devastation` applies as `−2 × level/100` and flags
that as an assumption; `unrest`'s per-point scaling needs the same flag unless a file settles it.

### The attribution I created while fixing attributions

**S4 — Y086/Y132.** `relabel6.py` was written because figures were attributed to scripts that did not
contain them; the spec then credited it with an LP-objective figure it did not compute. It now solves
Phase 2's LP directly under each permutation:

| | |
|---|---|
| identity objective | 0.712275977829 |
| max relative deviation | **6.235e-16** over 40 permutations |
| permutations with a different optimal support | **40 of 40** |

The auditor measured 6.66e-16 independently. Both exceed the **4.44e-16** the spec states, which goes.
Where the reimplementation cannot produce a figure, the script now says so rather than allowing the
citation to stand.

### Say less rather than restate

Seven of the nineteen partials repair by **deletion**, not re-measurement — Y080, Y084, Y086, Y092,
Y106, Y129, Y132 — which is the shape of what is left in this document: numbers quoted more precisely
than their sample supports. Y047 is the only partial whose repair *adds* something.

### Outside the inventory, in scope anyway

**S5 — §3.5's campaign sentence.** The same `1540.1.1` block in `history/countries/HAB - Austria.txt`
also applies `COTTON_IMPORTS = -0.10` to `wool`, so a campaign reaching 1540 holds two live negative
keys and wool sits near 1.625–1.6875, not 1.875. **1.875 is the single-event floor** — correct for the
13/2/4/11 partition, wrong for the campaign claim. Carried UNCHANGED from an earlier version, so no
claim row covers it.

**S6 — `fixes-agreed.md` is stale** (10,594.70, 90.2%, 5,703), so `verify6.py` reports 5 failures
against it and 0 against the spec, while holding a typed literal for each. Either retire the file from
the harness's default target or update it; a checked document that nobody maintains produces exactly
the false signal `every_site()` exists to catch.
