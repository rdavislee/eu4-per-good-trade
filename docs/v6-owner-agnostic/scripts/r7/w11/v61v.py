# -*- coding: utf-8 -*-
"""v6.1 batch V -- 2.8's per-good row. The tie-break changed the per-good graphs, so both the sink
range and the demand-decile rates needed re-measuring."""
import patch_lib
E = [dict(id="V1", clears="V1: 2.8's per-good sink range and decile rates", section="2.8",
old="""| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 1 to 8 per good; high-demand nodes are sinks at 16.8% in the top demand decile vs 6.9% in the bottom (a barbell: LP branch ends land in poor pockets) |""",
new="""| Most goods, 1444 | Sinks are `{selected ∩ flow-terminal} ∪ promoted` (§1.1) — 2 to 8 per good; high-demand nodes are sinks at **19.8%** among each good's top eight demanders (46 of 232) against **6.9%** among its bottom eight (16 of 232), a barbell whose lower arm is LP branch ends landing in poor pockets. *The statistic is per-good deciles of nodes pooled over the 29 goods, not deciles of the pooled (good, node) pairs; the two constructions differ and only this one gives these figures.* |""")]
patch_lib.apply(E)
