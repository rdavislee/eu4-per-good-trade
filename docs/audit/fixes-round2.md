# Proposed v6.1 fixes — values to be independently confirmed

Negotiated with the no-context validation agent that produced `validation-v6.md`
(112 CONFIRMED / 28 PARTIAL / 3 REFUTED over Y001–Y143). Each row states an identifier, the value or
statement currently in the spec, and the value proposed to replace it. **Nothing here has been applied
to the specification.**

Two mechanism fixes were applied to `scripts/solver.py` and `scripts/measure6.py` before this list was
written, because every figure below depends on them:

- **M-a.** The solver reads the trade good the engine **rolled** at start for the twenty provinces whose
  history says `trade_goods = unknown`, instead of pricing them at zero. Primary source is the 1444
  save's `gamestate`; a province record header sits at column 0 and its fields are indented two tabs.
- **M-b.** The coal-activation counterfactual holds every non-repriced input fixed. Province 4237 is in
  the latent-coal set *and* in the devastated eleven, so a reprice that drops its devastation measures
  "coal activates" plus "one province heals".

---

## Numeric values proposed for the spec

| id | quantity | spec now | proposed |
|---|---|---|---|
| N01 | world wealth | 10,594.70 | **10,607.40** |
| N02 | counted provinces | 2,472 | 2,472 (unchanged) |
| N03 | provinces the classifier was worth, of 2,472 | 87 | **88** |
| N04 | largest \|b_w\| | 0.0226 | **0.0225** |
| N05 | sinks per good, min/max/mean | 1–8, mean 3.52 | **1–8, mean 3.72** |
| N06 | `Φ_w` self-coherence, edge-goods | 53.5% | **53.6%** |
| N07 | `Φ_w` self-coherence, value-weighted | 52.1% | **52.3%** |
| N08 | ordered pairs connected | 90.2% (5,703 of 6,320) | **89.6%** (count to be read from the run) |
| N09 | widest α band on [1, 8] | 1.70 wide, [3.51, 5.21] | **1.71 wide, [3.50, 5.21]** |
| N10 | coal activation, edge flips | 13 of 159 | **10 of 159** |
| N11 | coal activation, wealth delta | 217 ducats | **214.60 ducats** |
| N12 | caravan cap share, median (flag basis, 26 nodes) | 21.9% | **21.6%** |
| N13 | caravan cap share, median (derived basis, 25 nodes) | 21.3% | **17.7%** — to be checked, the two bases may have been swapped |
| N14 | max development at 1444 | "runs past 50" | **33** |
| N15 | solve cost, per good, average | 3–7 ms | **3.7–9.7 ms** |
| N16 | solve cost, runs inside 0.17–0.21 s | 1 of 12 | **6 of 12** |
| N17 | non-executable `change_price` blocks | 7 quoted + 3 wrapped | **4 `effect_tooltip` + 3 insight `effect = "…"` + 3 `tooltip = { }`** |
| N18 | §3.9 node-wealth ranks of genua / gulf_of_siam / sevilla | 3rd, 2nd, 7th | **4th, 3rd, 7th**; `mexico` is 2nd |
| N19 | scale test, sink set at ×10⁻⁶ | "sink set survives" | **collapses to `{genua}`** |
| N20 | v1 identity residual | "failed at 1e-5" | 1e-5 was the **residual**; v1's ε was **1e-6** |

## Statements proposed for change

| id | claim | proposed |
|---|---|---|
| S01 | `verify6.py` re-derives each figure from the document | Five needles carried typed values and one, `sources`, was a text check on a spelled-out word. All are now computed. The claim stands only if re-audited, and the two `(measure6.py)` attributions must be **earned**, not retained. |
| S02 | `on_startup` fires `flavor_geo.1`, which carries `add_base_*` and can move development before the first tick | **Keep** "`on_startup` fires `flavor_geo.1`" — it is in `00_on_actions.txt`'s own `events = { }` list. **Delete** the `add_base_*` clause and the pre-tick conclusion: `flavor_geo.1`'s whole effect is legitimacy, a country modifier and a flag. The keys are in `flavor_geo.3`, which `on_startup` does not fire. |
| S03 | development can move before the first tick | Delete. The history parse matches the save on **2,472 / 2,472** provinces. |
| S04 | a route runs from `english_channel` to the Asian sink (Hansa and Danube) | Delete. `english_channel` is a sink with **out-degree 0**; no route leaves it. `measure6.py`'s route check must also distinguish "no route" from "a route that avoids the Cape" — it reported the former as the latter. |
| S05 | "wrong in every audit that examined it" | Replace the universal with the count: wrong in **both independent audits** — `validation-v3.md` W041 and `validation-v5.md` X030/X034 — and **passed by v4.0's own repair harness, which v5.0 then refuted**. |
| S06 | per-good propagation breaks the income identity; the error is ≤ 0.1% | **Both halves go.** A single node scalar *does* reproduce every collector's income exactly: `ps̄_C = Σ_g v_g·cs_g·ps_C(g) / Σ_g v_g·cs_g` gives `collect_pool · ps̄_C = income_C` as an algebraic identity, with `Σ_C ps̄_C = 1`. The real cost is that `ps̄_C` is **value-weighted, so it is not derivable from trade power alone** — installing it means writing a country a fictitious per-node power, and whatever else reads that field then reads a fiction. |
| S07 | uniform wealth equalises `Σ wealth^α_Φ` per node | Delete or restate. Nodes hold 0–72 counted provinces, so uniform per-province wealth does not equalise a per-node sum. |
| S08 | the tax tooltip schema is `trunc(base_tax/12)` | `trunc(6/12)` is 0.50 and 0.49 was observed. Only `base_tax × 0.083333` truncated reproduces both readings. |
| S09 | one tooltip observation fixes the divisor to [12.00, 12.14] | **(11.73, 12.14]**. |
| S10 | the devastation scaling is read from a file | No file states the scaling; it is an assumption. `prosperity`'s direction is likewise unmarked in the spec. |
| S11 | the 12-month trading-policy cooldown covers the two banded policies | It covers **every** trading policy, Propagate Religion included. |
| S12 | v3.0 carries the `12·X` schema and the 0.6125 arithmetic | It carries neither; the attribution should name only the versions that do. |
| S13 | §2.8's containment set is grounded on the wealth tie | It is grounded on **T3**, not on the tie. |
| S14 | the Europe table shows the Channel's basin growing | At ×2.00 the sink is `genua` alone, so the table does not show that. State what the table shows. |

## What to confirm

For every N-row: compute the value independently from the install, the save, or the reference
implementation, and report the value obtained. For every S-row: the claim is a statement about a file,
a script, or an algebraic fact — settle it against that source and report what it says. Where a value
cannot be settled without a running game, say so rather than estimating.
