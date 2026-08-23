# -*- coding: utf-8 -*-
"""v6.1 batch P -- section 0 stops quoting the harness's check count, for the same reason it stopped
quoting a coverage ratio: some checks are generated per matching phrase, so the total moves with the
prose and any number printed here needs maintenance on every edit."""
import patch_lib
E = [dict(id="P1", clears="P1: no maintained figure for the harness's own size", section="0",
old="""**`verify6.py` runs 32 checks against values computed from the install, and that is well short of
what the document prints.** One of those 32 is this sentence: the harness reads its own stated count
out of the document and fails when it disagrees with the count it actually ran, because a stale
self-description is invisible to every other check in it.""",
new="""**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** No count is given here: some of its checks are
generated per matching phrase, so the total moves whenever the prose does. The harness prints its own
count when it runs, and that is where to read it.""")]
patch_lib.apply(E)
