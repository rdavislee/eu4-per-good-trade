# Mare Liberum: what it changes, and why

**TL;DR:** Vanilla draws the trade arrows once and they all point at Europe; the goods are
decoration. This mod computes a separate network for every trade good, every month, from
supply and wealth. Conquest captures producers, the two development buttons pull and push
trade, war bends the map and peace bends it back, merchants can work either end of a link,
and your capital does all the collecting. The controls stay vanilla's; the map stops being
scenery.

**Every trade good gets its own trade network, and every arrow on the map is computed from
the state of the world instead of drawn by a designer.** Trade stops being scenery you
compete over and becomes a system you can move.

## The map you were never allowed to touch

Vanilla's trade map is 80 nodes and 159 links, and the links were wired before release. The
wiki says it plainly: *"these connections between trade nodes are fixed and cannot be altered
during the course of play."* You get real choices *on* that map. Most nodes offer two or
three outgoing links to steer between (21 offer no choice at all), and trade power decides
who takes what share. But every choice is a fork in a road somebody else built. And all
roads end in the same place: exactly three nodes have no outgoing links (the **English
Channel, Genoa and Venice**), and every one of the other 77 drains into them. Whoever you
play, wherever you play, your trade's final destination was decided at the design desk, and
it is Europe.

Venice isn't an *end* (a node with nowhere further to send trade) because it earned it.
Measured by the wealth of the land that feeds it, Venice ranks 21st of 80. It's an end
because it's Venice.

Goods fare no better. The game knows what's in the barrel: the node window lists the goods
passing through, and "trading in" bonuses read them. But routing moves one undifferentiated
number. Grain, silk and spices flow the same direction at the same speed toward the same
three cities, because there is no market for anything, only a current.

Two limits follow, and both are bigger than they look. **You can grow your share of the
river, but you can never move the river**: no development, no conquest, no wonder turns a
single arrow, so the arrows of 1444 are the arrows of 1821. And **you cannot trade
backwards**: value only moves with the arrows, so Europe's cloth can never be *sold to* the
Americas, and nothing you will ever own can become the place the world's trade stops.

## What replaces it

**Twenty-nine separate trade networks at the 1444 start** (one per good in production, with
more coming online as latent goods like coal activate), plus one more network for wealth
itself. Thirty solves, every in-game month, each derived from two facts about the actual
world:

- **Supply** is where the good is physically produced, province by province.
- **Demand** is where the wealth is, and wealth is a property of the *place* (its
development, its trade good, its current condition), never of whoever owns it.

Each good's network orients every link so the good runs from surplus toward the places that
can pay for it. Nobody chose the directions. They fall out of the arithmetic, and they change
when the world changes: the same strait carrying cloth east and furs west in the same month.

The map you see in the trade map mode is that same calculation run on **wealth itself**: a
map of where the world's money drains. Its ends are an *output*. At the 1444 start the world
has two of them: **Genoa and Hangzhou**. Where it drains in 1650 depends on what you and two
hundred AI nations do about it.

A telling detail: on the 1444 field the English Channel is already the *richest* node in the
world, and it is still not an end. It drains toward Genoa. Being rich isn't enough; an end
has to out-pull everything around it.

## The new calculus



### Conquest buys supply, not arrows

Whose flag flies over a province is not a term in the model at all: only its development,
its trade good and its condition. (Condition is exactly what war ruins: devastated, besieged
and occupied land ships less and buys less, and peace brings both back.) So you cannot bend
trade toward yourself just by painting the map. Conquest still buys what it always bought
(trade power, and with it a share of the pool), but what's genuinely new is **supply**. Hold
the region that grows the spices and you hold the source of the spice network; from there the
good moves along its own graph toward demand, and when that demand is your home, home it
comes. In vanilla you conquer trade nodes. Here you conquer *producers*, and the map does the
delivery.

### The two development buttons do different jobs

- **Base tax is pure demand.** Developing tax makes a place hungrier, and goods orient toward
hunger. It is how you pull the world's commodities to your capital.
- **Base production is supply.** Developing production makes a province a *source*, and what
it makes flows outward, toward whoever wants it most. (Since goods are worth money, it adds
some pull of its own too; supply is never demand-free.)

In vanilla, development is development: more of either is more ducats and the map is
unmoved. Here the two buttons are different strategic instruments: dev production where your
best goods grow, dev tax where you want them to arrive.

### The ends of the earth can move, and you can fight over them

Because the aggregate map is wealth draining downhill, the world's ends sit wherever
concentrated wealth out-pulls its neighbours, for any nation, with no mission and no unique
mechanic. Both outcomes are real, and both happened in long hands-off tests. In a 201-year
campaign, Genoa and Hangzhou held as the world's two poles from 1444 all the way to 1645;
the structure can persist when nobody builds a challenger. In another run, by 1635 the ends
were the **English Channel, the Rhineland and Nippon** (Genoa and Hangzhou both dethroned).
(What we watched happen in that second world: Great Britain held both shores of the Channel
and developed them relentlessly.)

The ends answer to catastrophe too, and the tests are blunt: stripping every province of the
Hangzhou node bare flipped 35 links in a single tick, and within a few months the East's
terminus had moved to the Gulf of Siam. Hangzhou stopped terminating the East and began
draining inland. Devastating Champagne reversed the English Channel's outgoing trade; healing
it reverted every one of those flips exactly.

And the money follows the model, not the funnel: in control runs from the same 1444 start,
vanilla's top trade earner is Genoa (the bottom of the funnel), while under the mod it is
**Ming**, the largest economy on the map, which is where an honest model of 1444 says the
money should be.

### Prices reshape markets

How tightly a good's market concentrates follows its live price. Expensive goods chase the
richest individual markets, the way luxuries do; cheap goods spread wide across populous
regions, the way bulk staples do. Crash the price of grain and you can watch its market
spread: in testing, grain's ends dropped rich Venice and picked up populous Bordeaux and
Valencia (and far-off Patagonia). In vanilla, a price event is a number on your income and
nothing else.

### Merchants can push against the current

Every link has two ends, and a merchant can be assigned to **either one**, including the end
the goods are currently flowing *into*. From there it steers exactly the goods moving away
from it, and it is inert for the goods coming the other way. That is a move vanilla cannot
express at all, and it is what finally makes colonial trade behave the way it actually did:
Europe's cloth can be pushed *west* across the Atlantic, against the prevailing drain,
because that is where the demand is.

Measured, not hoped: a Castilian merchant put on the reverse end at Bordeaux became eligible
on exactly the six goods flowing its way (glass, iron, naval supplies, salt, wine, wool),
and on none of the goods flowing the other. The AI treats the reverse half of the board as
first-class too: Ming's opening picks steer Hangzhou and Xi'an *inland* toward Beijing,
trade pulled toward the capital, not exported to Europe by default. And across the 201-year
run, half of all AI merchant placements sat on reverse ends.

### Your capital collects; merchants steer

A deliberate rule change, and the biggest single change to how trade *plays*: **no merchant
is ever paid as a collector**. Collecting is your trade capital's job; it does it at full
strength with no merchant needed, and none allowed: the home node takes no merchant at all.
Merchants exist to move goods.

Here's why the old option isn't missed. Collecting abroad only ever existed because vanilla's
map is one-way: if a rich node sat downstream of your capital, its value could never flow
home, so the game let you park a merchant there and skim it on the spot, at a −50% penalty,
as a workaround. Under thirty networks there is no "downstream" anymore. Goods flow in every
direction, your capital's own wealth pulls them toward it, and a merchant at almost any node
in reach can steer value *home* instead of skimming it where it stands. The workaround lost
its job, so it's gone: the collect-or-steer dropdown is deleted, and every collect-anywhere
build with it. All of your trade income arrives at your capital, and everything else is
routing. (Vanilla's AI parks hundreds of collecting merchants in capitals at game start;
under this rule they march out onto the map within the first year.)

Two knock-ons worth knowing. Trade Efficiency now works on one node's take, while Trade
Steering works on everything you move. And since your capital is your only collection point,
*Wealth of Nations* (the DLC that lets you move your main trading city) is genuinely
valuable here.

### Trade power follows your goods

Trade power still propagates upstream, but the share a node passes on is now divided along
each good's own network, weighted by what the goods are worth, so your influence reaches the
places your goods actually go. About 1,400 more country entries appear in node trade-power
lists where vanilla showed none, and Genoa's own window shows countries steering *out of*
Genoa: the terminal node of vanilla's funnel became a place people push through. The flip
side, stated plainly: summed across the whole world, trade power runs about 5% below
vanilla's total, because a node now passes its fifth on once, split by goods, rather than
once per neighbour. Caravan power keeps its vanilla size but is earned now; the merchant has
to actually be steering a good on its link.

## More nuance, fewer clicks

The obvious fear: thirty maps must mean thirty times the micromanagement. The design goes the
other way: the *simulation* got deeper and the *controls* got simpler.

- **You never issue an order for a single good.** Trade power and steering intent stay
node-wide, exactly as in vanilla. There is no "spices order" to place.
- **One decision was removed outright**: collect-vs-steer. Capitals collect; merchants
steer; the home node takes no merchant at all. (Collecting abroad was vanilla's workaround
for value stranded downstream of your capital; with goods flowing every direction, nothing
is stranded.)
- **One merchant per country per node, vanilla range**: placing one covers every good
flowing away from that end at once.
- **Assignments survive the moving map.** A merchant is assigned to a link end, not a
direction; when a link flips, it stays put and works the new set of goods. And the map is
calmer than you'd guess: in an undisturbed test world, flips per month measured zero.
Across 201 years of wars, colonization and price swings, it moved about eight times a month,
across 159 links.
- **The UI is vanilla's UI.** Click a province and the whole trade interface becomes that
good's: its arrows, its numbers, its colors. Click the node icon and you're back on the
aggregate. No new screens to learn.

If you can play vanilla trade, you already know the controls. What changed is that the map
now answers to you.

## What stays vanilla

- **Your income is booked by the engine itself.** The mod computes each node's value and each
country's share and writes them into the game's own structures; the engine pays the ducats,
and every ledger line, tooltip and pie chart shows the economy that's actually running,
not a shadow of it.
- **Trade power sources are untouched.** Development, Centers of Trade, marketplaces, light
ships, trade companies: all add exactly the power they always did. Manufactories and
trade-company investments still pay off in full: they raise the *value* that moves.
Direction listens to the land itself (development, the good, the province's condition).
- **Trade leagues, merchant republics, embargoes and privateers keep their vanilla rules.**
They act through trade power, and shares still follow trade power. What no longer exists is
a map that hands Venice the terminus for free.
- **The world total tracks vanilla.** In control tests against unmodded runs from the same
start, world trade income ran a steady ~3% above vanilla: flat, with no drift and no
compounding.



## How do I know it works?

A 201-year hands-off campaign (1444–1645, speed 5, unattended) ran to completion without a
crash, and the world grew normally under it: colonization, wars, development all proceeding.
Every month, each country's ledger trade income is checked against what the mod computed,
inside the engine's own payment code: the worst disagreement across two centuries was about
three hundredths of a ducat, while the world economy doubled. Treasury bookings matched to
the cent. Save and reload, and the map comes back exactly as it was (not approximately,
exactly). The full live-game test record, results, retractions and residuals included, is
`[TESTING.md](TESTING.md)`, and the design document behind it is
`[per-good-trade-spec.md](per-good-trade-spec.md)`, including the arguments that lost.

## Known limits

- **One extra hitch, once a game month.** The re-solve measured 86 ms on the 1444 world and
about 150 ms on a dense late-game one, on the order of the engine's own monthly stall,
with the worst ordinary frame gap about a quarter of a second. In play it reads as one
small stutter at the month tick, and it does not grow as the campaign ages.
- **Rarely (7 months out of a 191-year test), one node's displayed total read negative for
that month.** Display only: the pool, the links and everyone's income stayed clean on those
same ticks.
- **Treasure fleets take a shortcut.** Colonial treasure always reaches its overlord, but
where the computed map has no route from colony to capital (at the shipped settings that
includes Mexico and Lima to Europe), the engine teleports the fleet home, so privateers get
fewer chances to raid it than the design intends.
- **The Trade Conflict casus belli can flicker.** It is granted when trade power at a node
crosses a threshold, and since power now moves with the map, the CB can appear and
disappear month to month.
- **One diplomacy check can still refuse.** Interactions gated on "is this country on my
trade route" are meant to always pass under thirty maps; one spot in the engine still runs
its own route check and can occasionally say no.
- **Single-player only, EU4 1.37.5 exactly.** The mod verifies the game binary and refuses
any other build. It does not detect ironman or multiplayer: nothing stops you, but
multiplayer clients would drift apart. Achievements are off, as with any mod. Saves made
with the mod are expected to load fine without it; trade reverts to vanilla's rules, and
merchants you placed on reverse ends come back steering vanilla's first outgoing link.

---

Vanilla asks: how much of a fixed river can you tax? This mod asks a better question: **where
should the rivers run, and what are you going to do about it?**

*→ [Install it](INSTALL.md) · [The story](WHY.md)*