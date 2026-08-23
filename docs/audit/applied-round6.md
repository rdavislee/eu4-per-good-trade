# Round-6 application record

What actually went into the spec from `fixes-round6.md`, what changed on the way in, and what was
refused. The batch was negotiated to unconditional confirmation and then pre-confirmed by a separate
agent; **every figure was still re-measured before it was written**, and that pass moved or rejected
figures in **eight of the 47 rows**. The negotiation and the pre-confirmation were both worth having —
they caught four wrong figures between them — and neither was a substitute for measuring again at the
moment of writing.

Spec before: `59c84a97799db9db97fe889b6e3c6776`, 1,979 lines. All figures below are from scripts in
`scripts/`, re-run against the current operator (α_Φ = 2.0, `TIE_COST`, `LP_OPTS` pinned at 1e-10).

---

## Rows whose agreed figure did not survive re-measurement

| # | agreed | measured | instrument |
|---|---|---|---|
| B4 | 30 flips on razed China | **32** | `m2` — zeroing `hangzhou` → `{genua, gulf_of_siam}` |
| B5 | 19.8% / 6.9%, 46 and 16 of 232 | **19.4% / 7.3%, 45 and 17 of 232** | `m1` |
| B6 | structured term 11 of 29 "against 0" | 11 of 29 **against 1** (`paper`) | `m3` |
| B15 | "seven" figures, later "10 of 22"; **both** long routes | **6 of 19** on an explicit enumeration; **only the Iberian** route ceases — the northern one survives both keys | `m8` |
| B16 | ~2,249 uses, later 425 | **410**, and **no `trade_node` token outside the four families** | `m9` |
| B17 | sole sink to ×3.20; none below ×20 | sole sink ×1.52 **continuous to ×3.60**; none below **×25** | `m7` |

The spec carries the measured column. Where a swept range is quoted it names the top of the range
actually swept rather than implying the property ends there.

**B9 is the counter-example, and it is the instructive one.** I re-measured its residual as 1.2e-16
against the agreed 5.2e-17 and wrote mine into the document. Building `round6.py` showed the agreed
figure was right: my throwaway probe had fed the identity an unnormalised `c_w` — algebraically the
same vector, numerically a different rounding. Re-measuring is not a trump card over a negotiated
figure; it only settles anything when the instrument is the one that ships.

## Rows refused

**B18, both halves.**

- *Y099 — quoting `Φ_ord`'s 59.8 / 59.6 self-coherence against `Φ_w`'s 55.1 / 54.8.* R3 forbids
  maintaining figures for a rejected operator and names `Φ_ord` explicitly. §3.9 keeps the comparison
  as a direction, which is what R3 prescribes for a load-bearing comparison. `final.py` **does**
  measure both numbers and they are in `final.out`; they are simply not written into the document.
- *Y383 — the propagation threshold in (5.01, 10.04].* Nothing in this tree computes it. Settling it
  needs §2.7 probe 8, which has not been run: the game probes that were run are 13, 14, 15 and the
  declaration-order companion. Writing the interval would have installed an unsourced number, which
  is the failure §3.16 nominates as the risk — and the exact trap C5 was created to close. §1.9 and
  §3.13 keep "pending probe 8".

**B19** was already correct in the frozen spec (90.6%, 5,723 of 6,320; 55.1 / 54.8) and needed no
edit.

## Found while applying, not in the batch

- **D11 — `coverage6.py` did not subtract its baseline.** It asked "did the harness go red?" instead
  of "did it go red *because of this mutation*", so any standing failure converted genuinely
  unprotected figures from MISSED into the unscored NO SITE bucket. Live effect: coverage read
  **4 of 4 (100%)** while two unrelated checks were red, where the honest number is **4 of 7 (57%)**.
  A coverage score that rises because something else is broken is the same defect class as D6.
- **D11b — `coverage6.py` ignored its command-line argument** and always read the hardcoded spec
  path. This masked D11: a probe of the fix never opened the probe document, so the fix appeared to
  make no difference. That is D2's defect (a harness choosing its own subject) surviving in a third
  script.
- **`verify6.py`'s docstring still advertised default targets** that D1 had removed.
- **`fixes-agreed.md` is frozen but was still judged against live measurements**, producing eight
  permanent reds. A permanently-red path teaches people to ignore red, so a frozen target's
  differences now report as **DRIFT**: still computed, still printed with the exact figures, but not
  able to fail a run. Two negative fixtures pin the mechanism (below).
- **`redtest6.py` gained two fixtures**, 5 and 6: a `FROZEN` marker planted in the *live* spec must
  not silence it, and a standing red must not move coverage's denominator. Fixture 6's first form
  passed vacuously — a harness that ignores its argument also leaves the denominator unmoved — so it
  now also requires the run to **name** the red it excluded.
- **C3's two cache checks were re-scoped.** They were pointed at `Φ_ord`'s self-coherence, which
  would have forced the R3 breach above. They now guard Phase 1's k census (`k = 1` for 27 of 29
  goods — §1.1 quotes it and only `final.py` computes it) and connectivity **as a second producer**,
  so `measure6.py` and `final.py` disagreeing shows up as a failure rather than as a figure that
  happens to be right for one of them.

## C2's acceptance test

`final.py:245` was the last Phase-2 call in the tree still passing **unit** costs — the degeneracy
§2.3 exists to remove, inside the calibration §3.13 describes. Verified before and after:

- acceptance: `V107` moved `['genua']` → `{doab, genua}`, as pre-confirmation predicted.
- `V035` reads 0 on both sides, which is why pre-confirmation dropped it as an acceptance test.
- `c2valid.py` (new): at **baseline** knobs the calibration body now reproduces `drain.run_drain`
  on **all 30 b-vectors**. With unit costs it disagreed on **30 of 30**, by 20 to 64 edges each — so
  it had been reading a different vertex from the shipped operator for every good, not drifting at
  the margins. §2.8's spice/cloves row moved as a result and now records why.

## The reread

Reading the whole document after the edits caught **ten** further problems, six of them created by
this batch:

1. C5's new instrument citation pointed at figures "below" that are in the bullet **above**.
2. C1's frozen-table clause left the sentence it interrupted dangling after a long parenthetical.
3. A5 and A2 opened two paragraphs twenty-five lines apart with the **same sentence**.
4. A2's rewrite ended on a clause with no antecedent.
5. B14 deleted the Europe table; **three** later sentences still pointed at it and at "the row
   boundaries".
6. B15's scope paragraph called the two long routes "below" when it sits after them.
7. A pointer to "the Europe table below" in §1.6's opening, carrying a **wrong** count with it —
   the sweep takes the count through two, three, four *and* five.
8. §2.3 said the calibration option "moves both knobs", which it does not — it replaces Phase 1,
   moves the tolerance, and unclamps α.
9. C4's §2.8 half had not been applied at all — only the §2.1 half had.
10. D10's negative-fixture requirement was agreed for §2.9's build order and was missing from it.

Items 9 and 10 are the ones worth noting: both were agreed, pre-confirmed items that a
figure-by-figure check would never have surfaced, because nothing was *wrong* — something was
absent. Only reading the section they belonged in found them.

## What the claims delta caught

The delta is an inventory pass, not a review, and it still found two things worth fixing.

**Six measured propositions were quoted with no instrument.** §1.6's sweep-key scope (6 of 19),
§1.10's exposure counts (410 across four families), §2.3's structured-term comparison (11 of 29
against 1), §3.2's Cape-by-flow (28 of 29), §3.6's margin pair (7.53e-06 against 1.267e-07) and
§3.9's flow identity — all measured for this round with throwaway scripts that were never in the
tree. That is Y250's defect, and C5 exists in this very batch to close it. `scripts/round6.py` now
computes all of them plus §2.8's barbell and razed-China figures, and each site cites it.

Building that instrument **corrected one of my own figures**: the flow-identity residual is
**5.2e-17**, not the 1.2e-16 I had written. My throwaway script fed the identity an unnormalised
`c_w` intermediate — algebraically the same vector, numerically a different rounding. The figure the
batch originally agreed was right, and the version I "measured" over it was wrong. The document now
carries what its named script prints, which is the only version of the figure that can be checked.

**The ID range in my brief was wrong.** I told the agent the previous census ran `Y001`–`Y1050` and
that new IDs should start at `Y1051`. The file actually runs to **`Y1057`**, so that would have
reused seven live IDs — the precise failure the ID-stability rule exists to prevent, introduced by
the person enforcing it. The agent checked the file instead of trusting the brief and started at
`Y1058`. The rerun brief now tells the agent to establish the range itself and to follow the files
over the brief wherever the two disagree.

## Phi_ord removed entirely, and what that uncovered

The superseded marking-order aggregate is **gone from the document** — 0 mentions, from 12 before
this round. R3 as written kept it as a rejection record with its design arguments and no figures;
the owner's decision was that it should not be there at all.

Two things had to be undone first, both introduced by this batch. B8 rebuilt section 3.9's bullet on
a *new* empirical comparison across sweep keys, and `round6.py` grew a block to measure it — new
maintenance for an operator the model does not install, added by the batch enforcing the rule
against exactly that. `final.py` was also still computing its self-coherence and caching three
figures no consumer read. Both are removed. What survives is the rejection reasoning with the
operator described rather than named, and it is **stronger without the measurement**: the aggregate
is a function of Phase 3's marking order, so its ends depend on the queue discipline **by
definition**. No instrument, no figures, nothing to re-run when the field moves.

**Testing the R3 guard found it had never guarded the document.** Planting the operator back into
the spec left `verify6.py` green. The guard sat in `run()` — the *checklist* path — so it had only
ever applied to `fixes-agreed.md`; the spec path carried a needle for one stale percentage
(`Φ_ord`'s **60.3%**) that any other reappearance would slip past. The guard is now the bare token
in `run_spec()`, and retested: green on the clean spec, **1 failed** on a reintroduction.

A second defect surfaced in the same test. The first version of the widened guard asserted the
operator's absence from `fixes-agreed.md`, which is frozen history and names it legitimately. It did
not fail — it *drifted*, because frozen targets report DRIFT rather than failure. So the DRIFT
mechanism added earlier in this batch concealed a wrong assertion on its first outing. The guard is
gone from that path, with a comment recording why.

## What the full reread found

Reading all 2,063 lines end to end after the edits caught two more, both from this batch:

- **Section 3.10 said "no residual is quoted for that" and then quoted one two lines later.** B12
  removed the figure from one sentence and left it restated in the next paragraph.
- **Section 2.1 opened and closed the same paragraph with "ship single-player only"**, the second
  time broken across three ragged lines.

Neither is a wrong figure, which is why no figure check could find them. Only reading the sections
did.

## State

| | |
|---|---|
| `verify6.py` on the spec | **33 checks, 0 failed** |
| `verify6.py` on the frozen checklist | 21 checks, 0 failed, 8 DRIFT |
| `mutate6.py` on the spec | 12 of 12 planted errors caught |
| `coverage6.py` | 4 of 7 uniquely-locatable figures (57%), baseline empty |
| `redtest6.py` | 6 fixtures, all produce the required red |
| `c2valid.py` | 30 checks, 0 failed |
| `props6.py` | 0 orientation changes over 145 scheduler permutations |
| `round6.py` (new) | reproduces all nine round-6 figures the document quotes |
| `fingerprint6.py` | `8b13dddb…faa1012c`, identical across five `PYTHONHASHSEED` values |

Spec after: `a95c71c0c9db8bc65cbbc24b2ba6ca58`, 2,063 lines, self-identifying as **v6.2**.

Next: a fresh claims extraction against the edited spec, then a new no-context validation agent.
