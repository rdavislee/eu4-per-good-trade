# -*- coding: utf-8 -*-
"""v6.1 batch AG -- the noise result is quoted at three seeds in 1.6 and six in 2.3 and 3.6. Both are
real (measure6.py runs three; the edge-flip probe ran six) but the document should say which is which."""
import patch_lib
E = [dict(id="AG1", clears="AG1: attribute the two noise samples", section="1.6",
old="""largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on three seeds. Its""",
new="""largest `|b_w|` **0.0347**; the sink set is unchanged under ±1% wealth noise on the three seeds
`measure6.py` runs, and on a six-seed run no edge moved at all (§3.6). Its""")]
patch_lib.apply(E)
