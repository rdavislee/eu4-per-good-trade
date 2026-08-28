# -*- coding: utf-8 -*-
"""v6.1 batch U -- 2.3's scope sentence reads as if per-good solves keep unit costs. They do not:
every per-good DRAIN run goes through Phase 2 and uses the tie-break. What keeps unit costs is the
separate FLOW/TREE comparison operators and verify.py's checks."""
import patch_lib
E = [dict(id="U1", clears="U1: which solves use the tie-break cost", section="2.3",
old="""Only DRAIN's Phase 2 uses this cost. The per-good flow operators in `flowop.py` and the checks in
`verify.py` keep unit arc costs, and `mincost_flow`'s cost argument defaults to unit for that reason.""",
new="""**Every DRAIN solve uses this cost, per good as well as aggregate** — Phase 2 is Phase 2 — and since
`w` is node wealth the same cost vector serves all of them. What keeps unit arc costs is the separate
comparison operators: the FLOW and TREE operators in `flowop.py` (§3.15's bake-off) and the per-good
checks in `verify.py`. `mincost_flow`'s cost argument defaults to unit so those are unaffected.

**A single cost vector does not make every solve unique, and §2.4 item 1 measures where it does not.**
Uniqueness of an LP optimum depends on the right-hand side as well as the objective: `b_w` has no zero
entries and its optimum is unique under this cost, while each `b_g` puts a different face of the
polytope in play and 84 of 290 per-good relabellings still move an edge. Adding a second wealth term
does not close it — see item 1 — because the obstruction is different routings with equal **totals**,
not individual arcs with equal costs.""")]
patch_lib.apply(E)
