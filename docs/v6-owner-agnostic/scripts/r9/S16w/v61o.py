# -*- coding: utf-8 -*-
"""v6.1 batch O -- the two other places that say the model reads all five province-state modifiers."""
import patch_lib
E = []

E.append(dict(id="O1", clears="O1: 2.2's build step names what is actually applied", section="2.2",
old="""   The only modifiers read are the five that describe the province's own condition, and at 1444 two
   are live: `devastation` on eleven provinces and `unrest` on twenty-one. `GP_COEFF` is **read from**""",
new="""   The only modifiers in scope are the five that describe the province's own condition, of which the
   reference implementation applies four; at 1444 `devastation` is live on eleven provinces, and
   `unrest` is live on twenty-one and **not read** (§1.3). `GP_COEFF` is **read from**"""))

E.append(dict(id="O2", clears="O2: 3.13's open question, scoped to what is applied", section="3.13",
old="""  reads development, the trade good and the five province-state modifiers, and nothing else — so""",
new="""  reads development, the trade good and the province-state modifiers of §1.3 — four of the five
  applied — and nothing else, so"""))

patch_lib.apply(E)
