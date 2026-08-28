# -*- coding: utf-8 -*-
"""v5 batch 5 — the band-width arithmetic (each width was the inclusive sample count, one step too wide)."""
import patch_lib
E = [dict(id="F55", clears="band widths: max-min, not the inclusive sample count", section="1.6",
old="""| 1 — `hangzhou` | **[1.43, 1.93]** | **0.51** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.46 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.32 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.02 |""",
new="""| 1 — `hangzhou` | **[1.43, 1.93]** | **0.50** — the widest band on this field, and the one α_Φ = 1.5 sits in |
| 3 — `doab`, `genua`, `hangzhou` | [2.26, 2.71] | 0.45 |
| 2 — `genua`, `hangzhou` | [1.94, 2.25] | 0.31 |
| 2 — `english_channel`, `hangzhou` | [1.41, 1.42] | 0.01 |""")]
patch_lib.apply(E)
