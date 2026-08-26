# Departures from spec

The specification (`per-good-trade-spec.md`, v6.6) is unchanged and remains the authority for
everything not listed here. Each entry below is a deliberate, user-directed departure: what the
spec says, what the implementation does instead, why, and how it is measured. Entries are dated;
none is applied without a user decision recorded in the entry.

---

## D1. Merchants never collect (2026-08-26)

**Spec.** §1.7: "Placement, range, and the collect/steer choice are vanilla." §3.14: the AI's
collect/steer choice is vanilla's.

**Departure.** No merchant collects, for the AI and the player alike. The only collecting standing
at a node is a country's trade capital, and no merchant may be placed at the trade capital.
Engine side: a prologue hook on the outer `SetTrader` (`0xB596E0`) forces transfer for any
trader record except a capital's; a per-tick sweep converts records that were collecting before
the hook existed. AI side: the frontier plan never targets the capital, and vanilla's 573
collect-at-home opening merchants are recalled first (value 0 under the rule). Player side: the
node window's collect action is inert (the hook), and the map-panel steer buttons are the control.

**Why.** The user's model of merchants: they exist to steer goods home along the per-good graphs;
collection is what the capital does with what arrives.

**Measured.** `[nocollect]` lines: 37-38 save-start collectors converted on tick 1, 0 after;
573 -> 8 capital merchants over 11 ticks; E1 ~660/660, E4 clean throughout (TESTING.md G block).

**Residual -- closed 2026-08-26.** At a Phi_w END node (genua, hangzhou) the engine has no
outgoing entry, and four of OUR guards (relink demotion, syncrec skip, the no-collect hook and
sweep) kept a merchant there at `type = 0` -- paid as a collector with the -50% non-capital
penalty (user-reported). The guards dated from the 0xB5654D crash, since fixed by the slack-padded
per-link buffer; the other engine check (0xB53C77) is a SIGNED compare that exits on index 0 at
N = 0. All four relaxed: end-node merchants are written as transferring with index 0 like any
reverse end. Measured: 10 monthly updates, no death, 0 merchants collect at end nodes, the AI
plans genua, E1 664/664. Appending reverse-end entries to the definition graph (relink's ALLOUT)
remains OFF: it corrupts the heap through the engine's own consumers (two deaths at tick 3,
`ntdll` heap fault, with and without our AI acting). D3 additionally makes any merchant record's
collector share 0, so the payment side never depends on the engine's type byte.

---

## D2. AI merchant assignment: the frontier model (2026-08-26)

**Spec.** §3.14 scores link ends by a denial/gain rule with vanilla's reassignment cadence as an
open question.

**Departure.** Home = the trade-capital node. Network = home + the nodes holding the country's
merchants, grown one node per placement. Candidates = frontier edges (one end in the network,
one out; the merchant stands outside and steers inward) that the engine's own
`CanSendMerchantTo` (`0x3532C0`) accepts. Score = flow moving inward on the edge x the product of
(my power / all power) at every node on the shortest network path home (with the merchant-present
floor at every network node except home) x the share at home. A posted merchant standing off the
plan is moved only when a planned node beats it by x1.5, with a three-month dwell. Cadence: the
working default the spec reserved for the user -- it fires 1-3 recalls per tick world-wide.

**Measured.** TESTING.md G block: 25-35% of placements on Phi_w-incoming ends, zero target churn,
recalled envoys still at their target one and three ticks later.

---

## D3. Trade-power propagation per good (approved 2026-08-26, in progress)

**Spec.** §1.9 preserves vanilla: a country's provincial power at node m, if it meets
`TRADE_PROPAGATE_THRESHOLD` (2), sends `1/TRADE_PROPAGATE_DIVIDER` (a fifth) of it to the nodes
immediately upstream of m, one hop, summed at the receiver, no merchant condition; direction is
read from Phi_w. §1.8 makes only the *eligibility* of that power per good.

**Measured vanilla rule (the engine's own records, 1444, two ticks).** The propagated amount is
folded into `val` (`rec+0x48`); `province_power` (`rec+0x28`) is the source. On the 186 records
that carry nothing but provincial power and propagation (no merchant, capital, ships or
subject transfers), `val - province_power` equals the sum over the downstream Phi_w neighbours
of `province_power/5` (threshold 2) for 98 records under the FULL rule -- each upstream node
receives the whole fifth -- and for 9 under a divided fifth. The engine's figure runs ~0.7%
above the exact fifth (fixed-point rounding). `rec+0x50/+0x54` are NOT propagation: they pair
between countries at the same node (subject -> overlord transfers; `+0xAF has_subject`).

**Departure.** For each good g, the fifth travels along g's own graph instead of Phi_w:

    prop_g(n, c) = sum over m with edge n -> m in g's graph of  [pp_c(m) >= 2] * pp_c(m) / 5

so a country's power at n for good g is

    P_c(n, g) = own_c(n) + prop_g(n, c),     own_c(n) = max(0, val_c(n) - prop_Phi_w(n, c))

where `prop_Phi_w` is the vanilla amount the engine already added (recomputed by the same rule
from `province_power` along the installed Phi_w) and is removed so that nothing propagates
twice. `P_c(n, g)` replaces the single aggregate power in §1.8's per-good split (P_collect(g),
P_transfer(g)) and in the steering shares.

Optional scaling (off by default, `PROP_FLOW_SCALED`): multiply each term by g's share of m's
inflow that came from n, `f_g(n->m) / sum_x f_g(x->m)`. It divides the fifth among the goods a
link carries instead of granting it in full per good; it also lowers every per-good power below
vanilla's aggregate. Left off until the user chooses.

**Consequences the implementation must carry.**
1. The model computes the collector division itself: `power_fraction` (`rec+0x2C`) is written
   per record before the engine's division as the country's flow-weighted share of the node's
   pool, `sum_g collected_g(n) * P_c(n,g)/P_collect(n,g) / sum_g collected_g(n)`, so pass 10 pays
   the model's figure. E1 is re-based on that prediction.
2. A merchant the table says steers at an END node gets collector share 0 -- the engine and the
   model agree on who is paid without the engine needing an outgoing entry there. This closes
   D1's residual, and the AI may plan end nodes again.
3. The AI's path shares keep the aggregate power for now (own + vanilla propagation); the
   per-good gradient is the follow-up that also tells light ships where to go.

**Why.** Per-good graphs disagree with Phi_w on ~45% of edge-goods; propagating along Phi_w gives
a reverse-end merchant no upstream power for the goods it actually steers and credits power along
links a good never uses. Per-good propagation is what makes steering against Phi_w self-consistent
-- the "vibrant map" the user asked for.

**Implementation notes (review 2026-08-26).** The subtraction of the vanilla fifths follows the
INSTALLED graph (Phi_w, or the selected good's graph in a per-good view), never the attach-time link
list; `own` is signed (a subject's transfer deficit is carried, not clamped) and only the final
per-good power is clamped at 0, with the +2 merchant floor applied to that final power for
table-owned standings only. The written shares round to nearest permille and sum to 1.000 per
node where the engine's own summed to 0.995-0.998, so world collected income runs ~0.2-0.5%
above the engine's -- inside E3's null spread; not a regression. The normalisation divides by the
collected value of the goods that HAVE a collector at the node (a collector-less good's value is
redistributed onto the other goods' collectors: one engine pool must go somewhere). The optional
flow scaling is NOT implemented (documented only). The engine's amount runs ~0.7% above the exact
fifth (fixed-point rounding); it leaves `own` high by 0.007 x prop and cancels in the shares.
Open: whether `t_in - t_out` (subject transfers) is inside `val` or added after it -- install.h's
instruction reading and the probe disagree; a probe restricted to records with t_out > 0 settles
it. The offline suite (`aitest`, `econtest`, the 30/30 cross-check) still routes with the aggregate
power: it is a Phi_w-propagation CONTROL, not a model of the live tick.

**Measurement plan.** (a) offline: per-good powers reproduce vanilla's aggregate exactly when all
graphs equal Phi_w (identity test on the 1444 standings); (b) in game: E1 (engine-divided income ==
model prediction with the written shares) stays at all countries, E4 clean, world collected
income within the E3 null spread; (c) the number of AI placements on reverse ends and the flow on
them, before and after.
