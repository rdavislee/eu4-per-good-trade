# -*- coding: utf-8 -*-
"""v6 batch 27 — the pre-confirmation's two mismatches and three caveats.

The first is a revert: "19 land provinces" was correct and I changed it to 20 on a members count
that includes province 1460, which is in `map/default.map`'s `sea_starts`. A claim about *land*
provinces is not answered by a count of *members*.

The third is R2 applied to figures I introduced last round: across three independent 800-trial sets
the minor end-holders range (sevilla 79-117, rheinland 112-136), so those counts are not stable at
that sample size and are no longer quoted as if they were."""
import patch_lib
E = []

E.append(dict(id="Q09", clears="Q09: revert to 19 land provinces, and say why it is not 20",
section="3.13",
old="""**Per province, because node boundaries are an authoring artifact.** Node sizes run from 20 land
provinces (`cape_of_good_hope`) to 77 (`girin`) — a 4× spread""",
new="""**Per province, because node boundaries are an authoring artifact.** Node sizes run from 19 land
provinces (`cape_of_good_hope` — its `members` list has 20 entries, but 1460 is a sea zone, listed in
`map/default.map`'s `sea_starts`) to 77 (`girin`) — a 4× spread"""))

E.append(dict(id="Q10", clears="Q10: the genua takeover point, on a fine grid", section="1.6",
old="""basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates to `genua`
past roughly ×1.70 — and""",
new="""basin grows from 18 nodes to 28 by about ×1.44, then gives way as the end itself migrates: `genua`
first holds an end at ×1.63 and is the sole end from ×1.64 through ×2.00 — and"""))

E.append(dict(id="Q07", clears="Q07: 1.6's copy of the objective deviation", section="1.6",
old="""and the LP objective is identical to
2.22e-16, so these are different *optimal* orientations rather than different answers.""",
new="""and the LP objective is identical to within
4.44e-16, so these are different *optimal* orientations rather than different answers."""))

E.append(dict(id="Q03-06", clears="Q03-Q06: the minor holders are not stable at n=800", section="1.6",
old="""runs. `hangzhou` was an end in **786 of 800** and `english_channel` in **322**. The Asian end is the
robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a
fact about that node. The European end is one of several the same world admits: `gulf_of_siam` held an
end in 459 runs, `wien` in 259, `rheinland` in 122, `sevilla` in 112. The count itself ranged 1 to 5,
most often 2 or 3.

*Proportions are pooled over all 800 draws rather than given as a per-seed range, because the range
is itself a function of which seeds are drawn: two honest eight-hundred-trial runs reported 97–100
and 96–100 per hundred for the same quantity.*""",
new="""runs. **`hangzhou` was an end in about 98% of them and `english_channel` in about 40%.** The Asian
end is the robust one — not invariant, since orderings exist where it loses its end, but near enough
that it is a fact about that node. The European end is one of several the same world admits, and after
`english_channel` the most frequent are `gulf_of_siam` (a little over half the runs), `wien` (about a
third), then `rheinland` and `sevilla`. The count itself ranged 1 to 5, most often 2 or 3.

*The two leading proportions are quoted to two figures and the trailing ones qualitatively, because
that is as far as this sample supports: across three independent 800-trial sets `hangzhou` came in at
784–789 and `english_channel` at 322–336, while `sevilla` ranged 79–117 and `rheinland` 112–136. A
per-seed range is worse still, being a function of which seeds are drawn.*"""))

E.append(dict(id="Q03b", clears="2.4's copy, to the same precision", section="2.4",
old="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in 786
   of 800 relabellings, `english_channel` in 322, and the count ranges 1 to 5 (§1.6).""",
new="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in about
   98% of relabellings, `english_channel` in about 40%, and the count ranges 1 to 5 (§1.6)."""))

E.append(dict(id="Q03c", clears="2.8's copy, to the same precision", section="2.8",
old="""which it does in 786 of 800 relabellings (§1.6)""",
new="""which it does in about 98% of relabellings (§1.6)"""))

patch_lib.apply(E)
