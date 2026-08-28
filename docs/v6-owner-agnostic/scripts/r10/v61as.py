# -*- coding: utf-8 -*-
"""v6.1 batch AS -- the multiplayer block lives in 2.1 Shape (line 832), not 2.2 Solver (line 896).
Four references I added this pass point readers at 2.2 for it. Also 2.2's own DLC/solver text was
edited under a '2.2' label when it is in 2.1; the cross-references are what matter."""
import patch_lib
E = []

E.append(dict(id="AS1", clears="AS1: 0's pointer to the multiplayer discussion", section="0",
old="""move with it. §2.2 records what multiplayer would additionally need, which is now build discipline
rather than a design change.""",
new="""move with it. §2.1 records what multiplayer would additionally need, which is now build discipline
rather than a design change."""))

E.append(dict(id="AS2", clears="AS2: 2.7's probe pointer", section="2.7",
old="""    determinism either way: §2.2's orientation margins are 3.8e-8 to 7.5e-6, three to five orders""",
new="""    determinism either way: §2.1's orientation margins are 3.8e-8 to 7.5e-6, three to five orders"""))

E.append(dict(id="AS3", clears="AS3: 3.6's pointer", section="3.6",
old="""makes robust to a few units in the last place. What is left is build discipline (§2.2).""",
new="""makes robust to a few units in the last place. What is left is build discipline (§2.1)."""))

E.append(dict(id="AS4", clears="AS4: 3.13's pointer", section="3.13",
old="""- **Multiplayer build discipline.** Not LP pivot determinism, which §2.2 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.2 and §3.6.""",
new="""- **Multiplayer build discipline.** Not LP pivot determinism, which §2.1 retires: the optimum is
  unique with a margin 8 to 10 orders above float noise, so a few units in the last place cannot
  change it. What is open is whether the shipped solver build does runtime CPU dispatch or threads its
  reductions — either would break bit-identity across hosts running the same binary — and whether the
  DLL reproduces the reference implementation's orientation exactly (§2.8), which cannot be tested
  until the DLL exists. Replaces v1's ε-magnitude question; see §2.1 and §3.6."""))

patch_lib.apply(E)
