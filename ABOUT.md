# Per-Good Trade — what it is, and why

## The problem with vanilla trade

Open the trade map in vanilla EU4 and you are looking at a decision somebody made in 2013. Every
arrow on that map is hand-authored. Novgorod flows to Lübeck; the Ivory Coast flows to Sevilla; the
Caribbean flows to Sevilla. It flowed that way in 1444 and it will flow that way in 1821 — whether
the Caribbean is Spanish or Dutch or empty, whether Sevilla is a metropolis or a devastated ruin,
whether anyone is producing anything at all.

The map is a river system with the water already drawn in.

This has a consequence that is easy to miss because it is everywhere: **your trade goods do not
matter.** Not really. A node's value is one number — a pile of ducats with no contents. Grain,
spices and cloth are identical once they enter the network; they flow the same direction, at the
same time, to the same place. Your province produces "value". The tooltip names a good, and the name
is decoration. There is no market for spices, no place where cloth is scarce and grain abundant. The
trade good on your province is a modifier attached to a number, and the number goes downstream.

Because the arrows are fixed, so is the strategy. The trade powers of 1444 are the trade powers of
1700, because the map that makes them powerful cannot change. Conquering the source of a good does
not redirect it — it was always going to arrive in the same place. Devastating a region reroutes
nothing. Trade in vanilla is a fixed board you compete on, not a system you can alter.

## What this mod does

**Every trade good gets its own directed network, and every direction is computed from the world
rather than authored.**

Not thirty copies of the same map. Thirty *different* maps, each recomputed every month from what is
actually happening in your game.

Each month the mod reads the live world — every province's production, wealth, development and
devastation, and the current price of every good — and for each good forms a balance: where it is
produced, where it is wanted. Then it orients that good's network by asking a physical question
rather than a design one: *given this pattern of surplus and demand, which way must this good flow?*
The answer follows from conservation. Goods move from where they accumulate toward where they are
consumed, and the direction of every link falls out of the arithmetic.

The consequences are the point:

**Goods become real.** Spices flow toward the markets that want spices. Grain flows toward
population. Two goods produced in the same province can leave it in opposite directions, because
they are wanted in opposite places. Click a province and the map shows *that good's* network — its
own arrows, its own sinks, its own economy — and the numbers in the node window are that good's
numbers, not an undifferentiated pile.

**The map answers to the world.** Conquer the region that consumes a good and you move the market
that pulls it. Devastate a province and demand there falls, and routes toward it weaken. Let a price
collapse and that good's market spreads out instead of concentrating on the wealthiest nodes.
Colonise the New World and watch new sinks appear. In vanilla, none of these change a single arrow.

**Merchants gain a real decision.** Vanilla lets you push trade one way: downstream, along the drawn
arrow. Here every link has two ends and both can be worked, so a merchant can push *against* the
prevailing flow of a good to hold a market open. The AI understands this too — measured across a
200-year run, roughly a quarter of AI merchant placements sit on links vanilla could not express at
all, and about 30% of protective light-ship power ends up at nodes vanilla would never have sent a
fleet to.

**Trade becomes contestable.** This is the real change. Vanilla's trade map is scenery: you compete
for shares of a flow whose shape is permanent. Here the shape is an outcome. It reflects who is
producing, who is consuming, who has been burned, who has grown. Change the world and you change the
map — which means trade is something you can *win*, not merely something you can collect from.

## What it does not change

Deliberately conservative where the game is already good:

- **Your income is still the engine's.** The mod computes where goods flow and writes the resulting
  node values into the game's own structures; EU4 then divides money among countries by its own
  rules, unmodified. Trade power, merchants, trade companies and privateers work as you know them.
- **Placement, range, and collect-or-steer remain vanilla's.** What changes is which choices exist.
- **The world total tracks vanilla.** Measured against unmodded control runs from the same start, the
  world's trade value stays within a few percent — comparable to vanilla's own run-to-run variation.
  This is a redistribution of trade, not an inflation of it.

## On the evidence

This mod is unusual in how it was built, and that is worth a paragraph, because it should affect how
much you trust it.

The design was specified before it was implemented, and the specification was attacked in eleven
adversarial audit rounds until every quantitative claim in it was backed by a measurement against the
real game — 1,176 confirmed claims, none refuted. The implementation was then checked the same way
against a 47-test acceptance suite run in the live game: a 201-year hands-off campaign, income
agreement checked country by country every month, determinism across save and reload, and
compatibility with total conversions.

More to the point, the checks themselves were built to fail on purpose before their passing was
believed — a check that has only ever been seen passing is an assertion, not a measurement. The
direction gates, for instance, are verified by deliberately breaking them and confirming the
instrument reports it, then restoring them and confirming it reports that too.

The specification is `per-good-trade-spec.md` — §1 is the mechanics, §3 the reasoning, including the
arguments that did not survive.
