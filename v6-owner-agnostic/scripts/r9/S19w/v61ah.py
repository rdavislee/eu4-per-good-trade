# -*- coding: utf-8 -*-
"""v6.1 batch AH -- 2.4's closing note points at 84-of-290 as the superseding figure. That is now the
pre-second-term number; the current one is 13 of 290."""
import patch_lib
E = [dict(id="AH1", clears="AH1: point at the current figure, not the intermediate one", section="2.4",
old="""   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 84-of-290 above rather than
   contradicted by it.)*""",
new="""   `../v5-owner-agnostic/scripts/_audit_b_1444perm.py`. That script measures the unit-cost objective,
   so its figure describes the former solver and is superseded by the 13-of-290 above rather than
   contradicted by it.)*""")]
patch_lib.apply(E)
