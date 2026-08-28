# -*- coding: utf-8 -*-
"""v6.1 batch AL -- undo the probe insertion and renumber it as 16.

Inserting it as item 11 pushed the caravan probe to 12, which broke the live cross-references in 1.7
and 3.11 ("item 11 settles the recipient") and collided with 2.7's own prose, which already uses
12-15 for a separate block. 16 is free."""
import patch_lib
E = []

E.append(dict(id="AL1", clears="AL1: restore the caravan probe to item 11", section="2.7",
old="""11. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid (495 of 495 sampled). If the rounding is in
    the simulation, the engine erases sub-milli-ducat divergence every tick, which is how it survives
    lockstep multiplayer; if it is only in the save writer, it says nothing about determinism. Read a
    node's live trade value from memory at higher precision than the save shows and compare. This
    settles what §2.2 can claim about the engine's own defence, and whether the mod should adopt the
    same discipline at its write boundary.
12. **Caravan recipient.**""",
new="""11. **Caravan recipient.**"""))

E.append(dict(id="AL2", clears="AL2: add the quantisation probe as item 16, after the existing set",
section="2.7",
old="""All writes land atomically at the tick hook with the sim paused.""",
new="""16. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid — 495 of 495 sampled values, across
    `total`, `val`, `p_pow`, `retention`, `collector_power` and `max_pow`. If the rounding happens in
    the simulation then the engine erases sub-milli-ducat divergence every tick, which is a plausible
    part of how it survives lockstep multiplayer; if it happens only in the save writer it says
    nothing about determinism. Read a node's live trade value from memory at higher precision than the
    save shows and compare. This settles what §2.2 may claim about the engine's own defence, and
    whether the mod should round at its own write boundary. *It does not bear on the solver's
    determinism either way: §2.2's orientation margins are 3.8e-8 to 7.5e-6, three to five orders
    below a 1e-3 grid, so quantising the model's inputs to match would erase the §2.3 tie-break rather
    than protect it.*

All writes land atomically at the tick hook with the sim paused."""))

patch_lib.apply(E)
