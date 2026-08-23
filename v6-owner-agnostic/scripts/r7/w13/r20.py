# -*- coding: utf-8 -*-
"""v6 batch 20 — the three textual facts the clean extraction recorded. All three are mine:
a count I corrected in one place and not the other, a coefficient provenance I corrected in §2.2
and not in §1.3 or §2.3, and a mangled edit boundary in §1.6 that states one position twice."""
import patch_lib
E = []

E.append(dict(id="R20-16", clears="the mangled parenthetical in 1.6, stated twice", section="1.6",
old="""the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5
the 1444 field gives two sinks and a modestly grown Europe gives three or one (§1.6's Europe table),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration"; v5.0 over-corrected to "the count is set by `α_Φ`". Both are wrong in
the same way — the count is a function of the field **and** the constant, and only their
locations are emergent.** v2.0 through v4.0 said the count "emerges from concentration exactly as
per-good sink counts do" — it does not: `α_Φ` is a stipulated constant, the count is a step function
of it, and v2.1 chose the value with a target count in view — a calibration §2.3 withdraws without
replacing, since `α_Φ` is stipulated rather than derived. What the world
state moves is *where* the sinks are and *how the map drains toward them*, which is the property
§3.1's first goal actually asks for.""",
new="""the sinks are wherever the wealth flow terminates. **Both their count and their locations move with
the wealth field, and `α_Φ` sets how sharply concentration is read.** At the stipulated α_Φ = 1.5 the
1444 field gives two sinks, and a modestly grown Europe gives three or one (the Europe table below),
so neither the count nor the placement is fixed by the constant. *(v2.0 through v4.0 said the count
"emerges from concentration exactly as per-good sink counts do"; v5.0 over-corrected to "the count is
set by `α_Φ`". Both are wrong the same way — the count is a function of the field **and** the
constant. v2.1 also chose the value with a target count in view, a calibration §2.3 withdraws
without replacing.)* What the world state moves is *where* the sinks are and *how the map drains
toward them*, which is the property §3.1's first goal actually asks for."""))

E.append(dict(id="R20-13c", clears="§1.3's claim that neither coefficient is in a file", section="1.3",
old="""`GP_COEFF` and `TAX_COEFF` are in §2.3. Both were measured from the running game, not assumed:
neither is a define (`defines.lua` was searched), so both are engine constants recovered by
observation and each carries the observation that produced it.""",
new="""`GP_COEFF` and `TAX_COEFF` are in §2.3, and they have different provenance. **`GP_COEFF` is a
shipped file value** — `common/static_modifiers/00_static_modifiers.txt` carries
`provincial_production_size = { trade_goods_size = 0.2 … }`, localised "Base Production", which is
the same tooltip line the coefficient was measured off. It is therefore moddable and is **read at
runtime**, not hardcoded. `TAX_COEFF` is in no file that has been found — neither `defines.lua`,
`common/defines/`, nor that static-modifier block — so it stays a measured constant carrying the
observation that produced it."""))

E.append(dict(id="R20-23c", clears="§2.3's 'neither is a define' heading and claim", section="2.3",
old="""**Engine constants that are not defines.** The two wealth coefficients of §1.3 are hardcoded in
the binary — `defines.lua` and `common/defines/` were searched and contain neither. They are
therefore *measured*, and each is recorded with the observation that produced it. Re-measure them
against any patch that is not 1.37.5.""",
new="""**The two wealth coefficients, and where each comes from.** They are not the same kind of constant.
**`GP_COEFF` is a shipped file value**, in `common/static_modifiers/00_static_modifiers.txt` as
`provincial_production_size = { trade_goods_size = 0.2 … }` and localised "Base Production" — the
very line it was measured off. The emitter **reads it** rather than carrying 0.2, because a mod or a
patch can change it. **`TAX_COEFF` is not in any file that has been found** — `defines.lua`,
`common/defines/` and the static-modifier tables were searched — so it remains a measured constant
and must be re-measured against any patch that is not 1.37.5. *(v3.0 through v5.0 said neither
coefficient was in a file, and shipped a whole-install modifier sweep that walked past the block
holding one of them.)*"""))

E.append(dict(id="R20-ten", clears="'the devastated ten' against 'eleven counted provinces'",
section="1.3",
old="""   that line — province 265 is one, and it is also one of the devastated ten — and the engine treats""",
new="""   that line — province 265 is one, and it is also one of the devastated eleven — and the engine treats"""))

patch_lib.apply(E)
