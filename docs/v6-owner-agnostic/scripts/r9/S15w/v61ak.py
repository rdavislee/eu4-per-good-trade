# -*- coding: utf-8 -*-
"""v6.1 batch AK -- 2.2 now refers a probe to 2.7. Add it, or the reference dangles."""
import patch_lib
E = [dict(id="AK1", clears="AK1: the quantisation probe 2.2 refers to", section="2.7",
old="""11. **Caravan recipient.**""",
new="""11. **Is EU4's 1/1000 quantisation in the simulation or the serialiser?** Every trade number the
    engine writes to a save sits exactly on a 1/1000 grid (495 of 495 sampled). If the rounding is in
    the simulation, the engine erases sub-milli-ducat divergence every tick, which is how it survives
    lockstep multiplayer; if it is only in the save writer, it says nothing about determinism. Read a
    node's live trade value from memory at higher precision than the save shows and compare. This
    settles what §2.2 can claim about the engine's own defence, and whether the mod should adopt the
    same discipline at its write boundary.
12. **Caravan recipient.**"""),]
patch_lib.apply(E)
