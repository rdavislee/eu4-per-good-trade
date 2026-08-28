# Per-Good Trade

**Every trade good gets its own trade network, and every arrow on the map is computed from the state
of the world instead of drawn by a designer.** Trade stops being scenery you compete over and becomes
a system you can move.

## What is wrong with vanilla trade

Every arrow in vanilla was decided once, years ago, and never moves again. Novgorod flows to Lübeck.
The Ivory Coast flows to Sevilla. It flowed that way in 1444 and it will flow that way in 1821 —
whether the Caribbean is Spanish or Dutch or empty, whether Sevilla is a metropolis or a burnt-out
ruin, whether anybody is producing anything at all.

Two things follow, and both are bigger than they look.

**Your trade goods do not matter.** A node's value is a single number — a pile of ducats with no
contents. Grain, spices and cloth are identical the moment they enter the network: same direction,
same speed, same destination. Your province produces "value"; the tooltip names a good, and the name
is decoration. There is no market for spices, nowhere that cloth is scarce and grain abundant.

**And the trade powers of 1444 are the trade powers of 1821.** Venice is rich because the arrows
point at Venice. You cannot make Lübeck into a world market by building one, because no amount of
development moves a single arrow. You can take a bigger share of a fixed flow; you cannot change
where the flow goes.

## What replaces it

Thirty-odd separate networks, one per good, each re-derived every month from what is actually
happening in your game.

For each good the model reads where it is physically produced and where the wealth is that wants it,
then orients every link so the good runs from surplus toward demand. Nobody chose those directions —
they fall out of the arithmetic, and they change when the world changes.

The **aggregate map**, the one in the trade map mode, is that same operator run over *wealth itself*.
Its endpoints are the world's centers of trade: the places everything ultimately drains toward. They
are an output, not a setting.

## The new calculus

### Conquest is about supply, not about the arrows

Wealth here is **owner-agnostic** — a property of the place, not its owner. Development, trade good,
and the province's condition; nothing else. No autonomy, no ideas, no government modifiers. **A
province is worth exactly the same the day after you conquer it as the day before.**

So conquest does not bend trade toward you by fiat. What it gives you is *supply*: take the region
that grows the spices and you hold the source of the spice network. From there the good moves along
its own graph toward demand — and when that demand is at home, your conquest feeds your home node
directly. You are not capturing a node's share any more. You are capturing a **commodity**, and then
routing it.

That is a different war aim. In vanilla you conquer trade nodes. Here you conquer *producers*, and
the map does the delivery.

### Base tax and base production now pull in opposite directions

The sharpest change, and it falls straight out of the formulas:

```
goods_produced(p) = GP_COEFF · base_production(p) · (1 + goods modifiers)   ->  SUPPLY
tax_value(p)      = TAX_COEFF · base_tax(p)                                 ->  DEMAND (wealth)
```

- **Base tax is almost pure demand.** Developing tax at home makes home hungrier, and goods orient
  toward hunger. It is how you pull the world's commodities to your capital.
- **Base production is supply.** Developing production in a far-off province makes that place a
  *source*, and what it makes flows outward, toward whoever wants it most.

Develop production where your best goods are; develop tax where you want them to arrive. In vanilla,
development is development — more of either is more ducats and the map is unmoved. Here the two dev
buttons are different strategic instruments, and pressing the wrong one in the wrong province pushes
trade away from you.

### Centers of trade move, and you can build one

Because the aggregate map is wealth draining downhill, the world's trade centers sit wherever
concentrated wealth outweighs its neighbours. Shift the wealth, shift the center. Across a 200-year
test campaign the endpoints migrated from **Genoa and Hangzhou** to the **English Channel, the
Rhineland and Nippon** — and every move had a cause you could watch happening:

- Britain held both banks of the Channel and developed relentlessly. The Channel did not inherit its
  status; it was *built* into a world market.
- Korea and Japan became development juggernauts and pulled the eastern terminus to Nippon.
- China spent the era at war. **Devastation cuts both what a province produces and what it is
  worth**, so a country that is permanently a battlefield watches trade drain away from it. Hangzhou
  lost the east by being fought over.

The threshold is knife-edge — a couple of percent of relative wealth can move a world terminus. That
is not instability, it is leverage: **any nation can become the center of the world's trade**, with
no unique mechanic, no mission and no decision. Develop your home node hard enough and the arrows
turn around and point at you. Nothing in vanilla lets a Ming, a Vijayanagar or a Kilwa do that.

### Cheap goods spread, expensive goods concentrate

Price feeds a concentration exponent. While a good is expensive, demand for it concentrates on the
richest markets; when its price collapses the curve flattens, and poorer but more populous regions
carry relatively more of the demand — so the good's market *spreads out*.

Bulk goods behave like bulk goods, luxuries like luxuries. Crash the price of grain and its market
visibly de-concentrates. In vanilla a price change is a number on your income and nothing else.

### Merchants get a second option: push against the current

Every link has two ends and both can be worked. A merchant can push a good **against** the prevailing
flow to hold a market open — a move vanilla cannot express, because it only lets you send trade
downstream along a fixed arrow.

This is what finally makes colonial trade behave the way it actually did: a colonial nation can steer
**cloth from Europe back to the Americas**, because that is where the demand is, and that is what
happened. Vanilla can only drain the New World toward Europe, forever.

The AI plays this too — across a full-length run about a quarter of its merchant placements sit on
reversed ends.

### The map moves; your setup does not break

The obvious worry: if the arrows change every month, is managing merchants a nightmare? No.
Assignments attach to a **link end**, not to a direction. When a link flips, your merchant stays
where it is and works the other side; only the set of goods moving through it changes. And the links
that flip most often are the ones carrying almost no value — a link with real flow has a strong
reason to point the way it does.

## What deliberately does not change

- **Your income is still the engine's.** The mod decides where goods flow and writes the resulting
  node values into the game's own structures; EU4 divides the money by its own rules. Trade power,
  trade companies, privateers and light ships all behave as you know them.
- **Merchant placement, range and collect-vs-steer are vanilla's.** What changes is which choices
  exist.
- **The world total tracks vanilla.** Against unmodded control runs from the same start, world trade
  value stays within a few percent. This redistributes trade; it does not inflate it.

## On the evidence

The design was written as a specification before any of it was implemented, then attacked over
eleven adversarial audit rounds until every quantitative claim in it was backed by a measurement
against the real game: 1,176 claims confirmed, none refuted. The implementation was held to the same
standard by a 47-test suite run in the live game — a 201-year hands-off campaign, country-by-country
income agreement checked every month, determinism across save and reload, and compatibility with
total conversions including Anbennar and Extended Timeline.

The checks are built to fail on purpose before their passing is believed: a check that has only ever
been seen passing is an assertion, not a measurement. The direction gates, for instance, are verified
by deliberately breaking them and confirming the instrument notices, then restoring them and
confirming that it notices that too.

The specification is `per-good-trade-spec.md` — §1 is the mechanics, §3 the reasoning, including the
arguments that did not survive.
