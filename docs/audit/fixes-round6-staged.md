# Round-6 fixes — staged, not applied

**The spec is frozen at `30a81da3d02dc79f83613e76a9c0d023` while extraction round 9 reads it and
validation round 5 grades it.** Nothing here is in the document. Editing between an extraction and the
validation that grades it is what invalidated the round-five inventory.

---

## S1 — devastation's scaling law is documented, not assumed

§1.3's note currently reads:

> *What no shipped file states is the **scaling law** for `devastation`: the model assumes the modifier
> applies in proportion to the level, `-2 x level/100`, and that proportionality is an assumption
> rather than a file value. It is the **only** such assumption in this table — `unrest` and
> `nationalism` both carry per-unit comments in that same file, so the convention for stating a
> scaling exists and `devastation` simply does not use it.*

The EU4 wiki's Devastation page states the penalties are **"scaled linearly according to the
percentage value"**, and lists them as what a province incurs **"at 100% devastation"**. That is
`-2 x level/100` exactly. The model's proportionality is therefore documented engine behaviour, not an
assumption of this design.

The wiki independently reproduces the file asymmetry the note argues from: its Static modifiers page
writes devastation's effect as a bare `-200% Local goods produced`, while `unrest` is listed under
explicit **"Per point of unrest"** language. So the second half of the note survives; only the word
"assumption" and the claim that it is the table's *only* one do not.

**Proposed replacement.** Keep the file observation, correct the provenance, and say plainly that this
row's source is community documentation rather than the install — every other row in the table is read
from `00_static_modifiers.txt`, and that difference is worth stating rather than smoothing over:

> *The magnitudes and directions above are all read from `00_static_modifiers.txt`. That file does not
> state the **scaling law** for `devastation`, and it is the only row here whose scaling it leaves
> open — `unrest` and `nationalism` both carry per-unit comments in it. The wiki settles the law: the
> penalties are scaled linearly with the percentage value and are quoted at 100% devastation, which is
> the `-2 x level/100` the model applies. **This is the one row whose scaling rests on community
> documentation rather than on a shipped file.***

Provenance to record: `read from a file` for the magnitude, `documented externally` for the scaling.
If the census's vocabulary has no such category, the honest label is the sentence, not a category.

---

## S2 — where the node-order dependence actually comes from, and that it is fixable

§1.6 and §2.4 state that the sink set's membership and size are conditional on the node order. That is
correct, but the document does not say *which phase* introduces the conditionality, and the natural
reading — that a tiebreak in the sweep is unspecified — is wrong. Every tiebreak in `drain.py` is
wealth-based, and the node index is never a primary key:

| decision | key | index's role |
|---|---|---|
| Phase 1 sink pick | `(beta[v], v)` — heaviest demander | third; exact ties only |
| Phase 3 sweep | `(-DEF[v], beta[v], pid[v])` | third; exact ties only |
| stall promotion | `(beta[v], v)` | second; exact ties only |
| stall fallback | `(NODEW[v], -v)` — node wealth | second; fires **0** times at 1444 |

The conditionality is **degeneracy in Phase 2's min-cost b-flow**. With unit arc costs many flow
patterns hit the identical minimum, and the simplex returns whichever its pivot path reaches.

Two results worth recording, both measured on 20 relabellings under one seed — a probe, not a
measurement, and not to be printed as a figure until re-run at a real sample size:

**A directional wealth preference cannot break the tie, for a structural reason.** A cost
`c(u->v) = 1 - eps*(w[v] - w[u])` is a potential difference, and for a fixed `b` the total cost of a
potential difference is `sum_n w[n]*b[n]` — the same for every feasible flow. So "prefer flow toward
the wealthier node" adds a constant and is invisible to the LP. Tested at eps = 1e-6 through 1e-2:
still 20 distinct supports of 20, objective spread ~1e-16. The corollary is worth stating in its own
right: the wealth gradient is already fully expressed by `b`, and contributes no tie-breaking
information on top of it.

**A symmetric corridor cost does break it.** `c = 1 - eps*(w[u] + w[v])/2`, cheap along rich corridors,
collapses the 20 supports to 2, stable across eps from 1e-3 to 1e-1. The residual split is a single
arc — whether `hormuz` is fed from `gujarat` or from `gulf_of_aden` — with 78 of 79 arcs shared and the
same 27 zero-out-degree nodes either way. The variant `c = 1 + eps*|w[u] - w[v]|` does nothing
(20 of 20 distinct), so it is corridor wealth that selects, not corridor levelness.

**Not yet shown, and not to be claimed:** that the *sink set* becomes ordering-invariant. The support
is upstream of Phase 3, which has its own keys and a promotion branch. What is shown is that Phase 2
stops being the source of the ambiguity.

**This is a change to the shipped algorithm, not to the document.** Taking it means re-measuring every
figure computed through `drain.py`, and the instrument rule applies to the modified solver as much as
to any reimplementation: it must reproduce the current answer on the identity permutation — 159 of 159
edges, Phase-0 core 80, 2 promotions, 0 fallbacks — before any figure from it is usable. Held as a
design decision, not applied.

---

## S3 — two provenance gaps the round-9 census names

- **Y017**, §0: "some figures carry a script attribution instead of a guard, and a few carry neither"
  names no instrument, and `coverage6.py` measures exactly that. Either cite it or drop the clause.
  This is residue from the round-5 rewrite that replaced a stale ratio with a pointer to the tool; the
  pointer went in and the qualitative tail stayed.
- **Y723**, colonization's gate: rests on one mod author's forum report that was contradicted
  in-thread. The census records that the observed behaviour needs no gate at all. Whether the gate
  stays is a design call; what should not stay is a contested secondary source cited as if settled.

---

## To be added when validation round 5 returns

Its REFUTED and PARTIAL rows, negotiated with the agent that produced them, then measured by a
separate pre-confirmation agent before any of it is written.
