# -*- coding: utf-8 -*-
"""v6.1 batch AT -- six misdirected section references. 2.2 Solver is a build list; the connectedness
requirement is in 2.2a and the DLL shape and multiplayer discussion are in 2.1. Two of these are
pre-existing (the header target line and 1.1's reachability bullet); four I introduced this pass."""
import patch_lib
E = []

E.append(dict(id="AT1", clears="AT1: the header's connected-maps pointer", section="0",
old="""**Target:** EU4 1.37.5 Inca. Extended-timeline compatible. **Connected maps only** — see §2.2.""",
new="""**Target:** EU4 1.37.5 Inca. Extended-timeline compatible. **Connected maps only** — see §2.2a."""))

E.append(dict(id="AT2", clears="AT2: 1.1's reachability bullet points at the connectedness premise",
section="1.1",
old="""infeasible outright. §2.2 states the connectedness requirement and what the solver does when it
  is violated.""",
new="""infeasible outright. §2.2a states the connectedness requirement and what the solver does when it
  is violated."""))

E.append(dict(id="AT3", clears="AT3: 1.6's pointer to where the per-good economy is propagated",
section="1.6",
old="""proved and §2.2 propagates the per-good economy and writes it back — a per-good arrow that moved with""",
new="""proved and §2.1 propagates the per-good economy and writes it back — a per-good arrow that moved with"""))

E.append(dict(id="AT4", clears="AT4: 2.4's same pointer", section="2.4",
old="""   §2.2 propagates the per-good economy and writes it back — but it is no longer the difference""",
new="""   §2.1 propagates the per-good economy and writes it back — but it is no longer the difference"""))

E.append(dict(id="AT5", clears="AT5: 2.7's probe pointer to the multiplayer discussion", section="2.7",
old="""    save shows and compare. This settles what §2.2 may claim about the engine's own defence, and""",
new="""    save shows and compare. This settles what §2.1 may claim about the engine's own defence, and"""))

E.append(dict(id="AT6", clears="AT6: 3.6's pointer to the multiplayer discussion", section="3.6",
old="""replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.2 narrows it: the LP""",
new="""replaces the ε-magnitude question in §3.13 is the cross-machine question — and §2.1 narrows it: the LP"""))

patch_lib.apply(E)
