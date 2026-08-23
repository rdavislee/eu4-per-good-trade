# -*- coding: utf-8 -*-
"""v6.1 batch AV -- Y974: 0 asserts 'covers well under half' and then, in the next sentence, declines
to give a ratio because the denominator is not well defined. Those cannot both stand. Drop the
proportion; the paragraph's own reasoning is why."""
import patch_lib
E = [dict(id="AV1", clears="AV1: 0 stops asserting the proportion it then declines to give",
section="0",
old="""**`verify6.py` checks figures in this document against values computed from the install, and it
covers well under half of what the document prints.** Neither a count nor a ratio is given here, for
two different reasons. The count moves whenever the prose does, because some checks are generated per
matching phrase — the harness prints its own count when it runs, and that is where to read it. The
ratio has no well-defined denominator: counting "the figures the spec prints" gives anywhere from 279
to 326 depending on how a numeric token is delimited, so any proportion built on it says more about
the tokeniser than about the harness.""",
new="""**`verify6.py` checks figures in this document against values computed from the install, and its
coverage is partial.** Neither a count nor a proportion is given here, for two different reasons, and
"partial" is as far as this paragraph will go. The count moves whenever the prose does, because some
checks are generated per matching phrase — the harness prints its own count when it runs, and that is
where to read it. A proportion has no well-defined denominator: counting "the figures the spec prints"
gives anywhere from 279 to 326 depending on how a numeric token is delimited, so any fraction built on
it says more about the tokeniser than about the harness. *An earlier draft of this paragraph asserted
"well under half" two sentences before refusing to give a ratio; the refusal is the part that survives.*""")]
patch_lib.apply(E)
