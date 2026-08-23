# -*- coding: utf-8 -*-
"""v6.1 batch L -- the harness's check count, now that the harness checks it."""
import patch_lib
E = [dict(id="L1", clears="L1: the check count the harness now verifies", section="0",
old="""**`verify6.py` runs 31 checks against values computed from the install, and that is well short of
what the document prints.**""",
new="""**`verify6.py` runs 32 checks against values computed from the install, and that is well short of
what the document prints.** One of those 32 is this sentence: the harness reads its own stated count
out of the document and fails when it disagrees with the count it actually ran, because a stale
self-description is invisible to every other check in it.""")]
patch_lib.apply(E)
