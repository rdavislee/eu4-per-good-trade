# EU4 Trade System Overhaul: Mare Liberum

**TL;DR:** Free trade overhaul for EU4 1.37.5. Every trade good gets its own trade network,
recomputed every in-game month from where the good is produced and where the world's wealth
sits, so trade can flow in any direction and the world's trade capitals are earned, not
scripted. The controls stay vanilla's. Single-player, installs in two drops and a checkbox.
Download:
[github.com/rdavislee/eu4-per-good-trade/releases](https://github.com/rdavislee/eu4-per-good-trade/releases/latest).

In vanilla you can win every war as the Aztecs and Mexico still can never become a place the
world's trade flows *to*. The three nodes where trade terminates (the English Channel, Genoa,
Venice) were picked before the game shipped, and no conquest on the planet adds a fourth.
Colonize the American west coast as Japan and the continent drains east toward Europe anyway,
forever. Paradox patched everything else over the years, development, institutions, reform
tracks, but the arrows were never a number they could tune. They're the architecture.

Mare Liberum replaces the architecture. The design problem: cloth crossed the Atlantic
westward while sugar crossed it eastward, on the same water, at the same time, and one
directed graph cannot say that. Twenty-nine can. **Every good gets its own network,
re-derived monthly from where it's made and where the wealth is.** Trade ends wherever
concentrated wealth out-pulls its neighbours. Develop Mexico and the world's trade can
genuinely terminate there. No mission, no mercy from a designer.

## What changes in play

- **Conquest captures supply.** Taking the region that grows the spices makes you the source
  of the spice network, and the map carries the good toward whoever wants it most. Owning
  more land does nothing by itself; pull comes from development and land, not flags.
- **Development is two levers.** Base tax is demand: it makes a place hungrier, and goods
  orient toward hunger. Base production is supply: it makes the province a source. Develop
  your capital region hard enough and the networks bend toward you.
- **Merchants work both ends of a link.** Your capital collects; merchants steer, including
  against the prevailing current. In one test run Portugal steered sugar toward Sevilla while
  Caraíbas, its own colonial nation, steered cloth back across the same link to the
  Caribbean. The AI plays the reverse board unprompted; about half its placements sit on
  reverse ends.
- **Nothing is ever ordered per good.** A merchant covers every good on its link end at once.
  If you can play vanilla trade, you already know the controls.

![The per-good view: cloth in 1635](media/cloth-view-1635.jpg)
*Click a province and the entire trade UI becomes that good's map: its own arrows, numbers
and sinks. You see where your good actually goes, who is pulling it, and which end of which
link a merchant should work.*

## The proof

A campaign nobody played: 1444 into the 1600s, hands-off, AI only.

| ![Hangzhou, 1444](media/hangzhou-1444.jpg) | ![Nippon, 1635](media/nippon-1635.jpg) |
|---|---|
| *1444: the East's flows converge on Hangzhou.* | *The same region in 1635: the terminus has moved to Nippon.* |

At 1444 the world drains to Genoa and Hangzhou. By the 1600s the ends had moved to the
English Channel, the Rhineland and Nippon: Britain developed until the Channel out-pulled
everything around it, and when China split into warring states, the east lost its sink to the
fighting. Nobody scripted any of it, and out on the Atlantic, sugar sailed east while cloth
sailed west at the same time. The world total tracks vanilla.

## The fine print

EU4 **1.37.5** exactly, Steam, Windows, single-player. The model is a DLL beside `eu4.exe`
that solves every network once a month and writes the results into the engine's own
structures, so the ledger, the tooltips and the AI all see the real economy. That is also why
it can't go on the Steam Workshop, and why your antivirus may side-eye it: the build is
bit-reproducible, so you can build it yourself and verify the hash instead of trusting me.
Install steps and the rest of the documentation:
**[github.com/rdavislee/eu4-per-good-trade](https://github.com/rdavislee/eu4-per-good-trade)**.

The name is from Grotius: *Mare Liberum*, "The Free Sea," the 1609 argument that the sea and
its trade belong to no one. Vanilla shipped a closed sea. This opens it.
