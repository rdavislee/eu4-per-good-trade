# -*- coding: utf-8 -*-
"""v6.1 batch I -- 3.13's self-coherence baseline, 3.6's degeneracy premise, and 3.9's Phi_ord
figures, which R3 says should not be maintained and which the sentence below them already disclaims."""
import patch_lib
E = []

E.append(dict(id="I1", clears="I1: 3.13's self-coherence baseline", section="3.13",
old="""  baseline is known — `Φ_w` agrees with the per-good graphs on **52.3%** of edge-goods *weighted by
  trade value*, and on 53.6% unweighted (§1.6) —""",
new="""  baseline is known — `Φ_w` agrees with the per-good graphs on **55.0%** of edge-goods *weighted by
  trade value*, and on 55.2% unweighted (§1.6) —"""))

E.append(dict(id="I2", clears="I2: 3.6's degeneracy premise, narrowed by the tie-break", section="3.6",
old="""support, which is a discrete selection. Measured on 1444: across 29 goods × 6 random 1e-9 demand
nudges, **zero** support-membership changes moved more than 1e-6 of flow, and the ±1% wealth-noise
flips all sat on near-zero-flow edges. At exactly degenerate inputs — two equal-hop corridors — the
map from `b` to the chosen support is discontinuous in principle, so this rests on the solver's
tie-selection being stable, which is the same premise §3.13 tracks for multiplayer.""",
new="""support, which is a discrete selection. Measured on 1444: across 29 goods × 6 random 1e-9 demand
nudges, **zero** support-membership changes moved more than 1e-6 of flow, and under ±1% wealth noise
on six seeds the aggregate map moved **no edge at all**. At exactly degenerate inputs — two equal-hop
corridors — the map from `b` to the chosen support is discontinuous in principle. §2.3's tie-break
narrows where that bites: on the aggregate graph it leaves the optimum unique, so the result no longer
rests on the solver's tie-selection; on the per-good graphs, whose `b` a wealth-weighted cost need not
separate, it still does (§2.4 item 1), and that is the premise §3.13 tracks for multiplayer."""))

E.append(dict(id="I3", clears="I3: 3.9 stops quoting figures for a rejected operator", section="3.9",
old="""  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: across 20 relabellings the end count runs **12 to 19** and the end set is
  **never twice the same**, so neither the count nor the share terminating no good is a property of
  the world. Most of those ends terminate no good,""",
new="""  artifacts of sweep scheduling rather than places — and the sharpest evidence for that is what
  relabelling does to them: its end count and end set both move with the node order, where `Φ_w`'s do
  not (§2.4 item 1 measures the installed graph as invariant over the orderings tried). No figure is
  given for `Φ_ord`'s spread, because the operator is not installed and R3 forbids maintaining one.
  Most of those ends terminate no good,"""))

patch_lib.apply(E)
