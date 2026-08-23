# -*- coding: utf-8 -*-
"""v6 batch 26 — the partials from validation round 3. The ordering figures move to a pooled
proportion over 800 relabellings, because a per-seed *range* is itself seed-dependent: two honest
runs over four seeds each gave 97-100 and 96-100 for the same quantity."""
import patch_lib
E = []

E.append(dict(id="Y078-081", clears="Y078/Y079/Y081/Y083/Y128: pooled proportions, not seed ranges",
section="1.6",
old="""returns a different optimal orientation. Across 400 relabellings — four seeds of 100, with `α_Φ` and
every input held fixed — **the orientation changed every time**, a mean of about 25 of 159 edges
moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **5 to 10 runs per
hundred**. `hangzhou` was an end in **97 to 100 per hundred** and `english_channel` in **37 to 44**.
The Asian end is the robust one — not invariant, since orderings exist where it loses its end, but
near enough that it is a fact about that node. The European end is one of several the same world
admits: `gulf_of_siam` held an end in about half the runs, `wien` in a third, `sevilla` in a fifth.
The count itself ranged 1 to 5, most often 2 or 3.""",
new="""returns a different optimal orientation. Over **800 relabellings** — eight seeds of 100, with `α_Φ`
and every input held fixed (`relabel6.py`) — **the orientation changed every time**, a mean of 25 of
159 edges moved, and the sink set came back exactly as `{english_channel, hangzhou}` in **64 of 800**
runs. `hangzhou` was an end in **786 of 800** and `english_channel` in **322**. The Asian end is the
robust one — not invariant, since orderings exist where it loses its end, but near enough that it is a
fact about that node. The European end is one of several the same world admits: `gulf_of_siam` held an
end in 459 runs, `wien` in 259, `rheinland` in 122, `sevilla` in 112. The count itself ranged 1 to 5,
most often 2 or 3.

*Proportions are pooled over all 800 draws rather than given as a per-seed range, because the range
is itself a function of which seeds are drawn: two honest eight-hundred-trial runs reported 97–100
and 96–100 per hundred for the same quantity.*"""))

E.append(dict(id="Y079b", clears="2.4's copy of the same proportions", section="2.4",
old="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in
   97–100 orderings per hundred, `english_channel` in 37–44, and the count ranges 1 to 5 (§1.6).""",
new="""   order required by item 1, not of the world alone:** on the 1444 field `hangzhou` is an end in 786
   of 800 relabellings, `english_channel` in 322, and the count ranges 1 to 5 (§1.6)."""))

E.append(dict(id="Y140b", clears="2.8's copy of the same proportion", section="2.8",
old="""which it does in 97–100 relabellings per hundred (§1.6)""",
new="""which it does in 786 of 800 relabellings (§1.6)"""))

E.append(dict(id="Y083", clears="Y083: the objective deviation", section="2.4",
old="""objective identical to within 4.4e-16 (`relabel6.py`, which validates its instrument against""",
new="""objective identical to within 4.44e-16 (`relabel6.py`, which validates its instrument against"""))

E.append(dict(id="Y010-158", clears="Y010/Y158: 'a majority' is exactly half", section="3.9",
old="""  artifacts of sweep scheduling rather than places, a majority of them terminate no good at all,""",
new="""  artifacts of sweep scheduling rather than places, **half** of them terminate no good at all (7 of
  14 on the 1444 field),"""))

E.append(dict(id="Y005", clears="Y005: name the ID that actually refuted the classifier", section="0",
old="""audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X030 and X034 — and passed by v4.0's own repair harness,
which v5.0 then refuted.""",
new="""audits that examined it** — `../v3-owner-agnostic/validation-v3.md` W041 and
`../v5-owner-agnostic/validation-v5.md` X035 — and passed by v4.0's own repair harness, which v5.0
then refuted."""))

E.append(dict(id="Y027-125", clears="Y027/Y125: whose rule and whose sweep", section="0",
old="""modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent
province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with
the whole-install sweep that maintained them.""",
new="""modifier classifier and everything it governed — the trade-good modifiers, great projects, permanent
province modifiers, buildings, centres of trade and the DLC conditionality — are deleted, along with
the whole-install sweep that maintained them. *(The two-test classifier is v4.0's; v3.0 used a
structural rule about which block of a trade-good definition a modifier sits in. The whole-install
sweep is v5.0's alone.)*"""))

E.append(dict(id="Y168", clears="Y168: the 5.96 figure's span", section="3.10",
old="""v1 through v4.0: "off by 5.96 ducats on a node paying ~250", where no node in the model has local trade value near 250.""",
new="""v1 through v3.0: "off by 5.96 ducats on a node paying ~250", where no node in the model has local trade value near 250 — v4.0 deleted it and its own harness asserted the deletion."""))

patch_lib.apply(E)
