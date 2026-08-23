# -*- coding: utf-8 -*-
"""v6 batch 25 — three overstatements the pre-confirmation agent caught in the ordering result, all
mine, all from generalising one random seed; plus one overstated claim about the harness.

Verified across four seeds (100 relabellings each): hangzhou holds an end 100/99/97/98, so "100 of
100" is a seed artifact and "every ordering tried" is false. Fallbacks stay 0 and genua holds an end
at Europe x2.00 in 60 of 60, so the blanket conditional was too broad."""
import patch_lib
E = []

E.append(dict(id="R09", clears="the ordering result, stated across seeds not one", section="1.6",
old="""returns a different optimal orientation: across 100 relabellings with α_Φ and every input held
fixed, the orientation changed 100 times, a mean of 26 of 159 edges moved, and the sink set came back
exactly as `{english_channel, hangzhou}` **8 times**. But `hangzhou` was an end in **100 of 100**,
and `english_channel` in **40**. The Asian end is the robust one; the European end is one of several
the same world admits — `gulf_of_siam` held an end in 55 runs, `wien` in 37, `sevilla` in 19. The
count itself ranged 1 to 5, most often 2.

**So read the rest of this section as conditional on one canonical node order**, which §2.4 item 1
requires the emitter to fix. That is not a caveat about precision; it is a statement about what kind
of fact the European end is.""",
new="""returns a different optimal orientation. Across 400 relabellings — four seeds of 100, with `α_Φ` and
every input held fixed — **the orientation changed every time**, a mean of about 25 of 159 edges
moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **5 to 10 runs per
hundred**. `hangzhou` was an end in **97 to 100 per hundred** and `english_channel` in **37 to 44**.
The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but
near enough that it is a fact about that node. The European end is one of several the same world
admits: `gulf_of_siam` held an end in about half the runs, `wien` in a third, `sevilla` in a fifth.
The count itself ranged 1 to 5, most often 2 or 3.

**What is conditional on the node order, and what is not.** Conditional: the sink set's membership
and size, and everything derived from them — §2.4's end-flag list, and which European node holds an
end in the table below. Not conditional, over the same relabellings: the map is fully oriented
(159/159) and acyclic every time, no fallback ever fires, and the LP objective is identical to
2.22e-16, so these are different *optimal* orientations rather than different answers. §2.4 item 1
requires the emitter to fix one canonical order for exactly this reason."""))

E.append(dict(id="R09b", clears="2.4's derived universal", section="2.4",
old="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end under
   every ordering tried, `english_channel` under about 40% of them, and the count ranges 1 to 5
   (§1.6).""",
new="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in
   97–100 orderings per hundred, `english_channel` in 37–44, and the count ranges 1 to 5 (§1.6).""",
))

E.append(dict(id="R09c", clears="the Europe table's ordering note, which named an invariant row",
section="1.6",
old="""*Which* European node holds an end at a given factor is ordering-dependent in the same way the 1444
set is — `english_channel` at ×1.02, `rheinland` at ×1.56 and `genua` at ×2.00 are this ordering's
answers, not the world's — so the direction is the claim and the membership is not.""",
new="""*Which* European node holds an end at the smaller factors is ordering-dependent in the same way the
1444 set is, so the direction is the claim and the membership is not. The last row is the exception
and is worth separating: at ×2.00 `genua` held an end in **60 of 60** relabellings, so a single
Mediterranean end under that much European growth is a property of the field rather than of the
ordering."""))

E.append(dict(id="T05", clears="the harness claim overstated what attribution covers", section="0",
old="""**Under half** of the figures it prints are guarded, and the rest rest on their script attribution
alone.""",
new="""**Under half** of the figures it prints are guarded. The remainder are not all covered by anything
else either: a script is named about a dozen times against roughly three times that many unguarded
figures, and some of the most recent additions carry neither a guard nor an attribution."""))

patch_lib.apply(E)
