# EU4 1.37.5 (build 835bfdf8) live-memory map — consolidated

All values are RVAs into `eu4.exe` (image base 0x140000000); add the live module base. A patch is a
new binary (spec 2.5) — re-derive on any update. Recovered by static disassembly (capstone/Ghidra)
plus live probing. Sources: the four RE passes in `scratchpad/re/{flowpass,merchants,ui,gates}.md`.

## Singletons / manager
- Game singleton `G = *(void**)(base+0x233FE78)`.
- `CTradeManager mgr = G+0x2198`. Node array: base `*(void**)(mgr+0x18)`, count `*(int32*)(mgr+0x24)`,
  stride **0x138**. Calc-order vector `*(mgr+0x30)`, count `*(int32*)(mgr+0x3c)`, stride 8.
- In-game interface `IGI = *(void**)(G+0x1E00)`; `IGI+0x2C` = map mode (**trade == 4**);
  `IGI+0x1228` = `CTradeNodeInterface` (`+0xF8` sim node, `+0xA0` window).

## CTradeNode (0x138 bytes) — sim fields, int32 fixed-point ×1000 unless noted
**Corrected by the flow-pass RE (supersedes earlier guesses):**
- **+0xB0 `current` = the node's collectible POOL** (NOT "gross local") · **+0xB4 local_value**
- **+0xB8 retention — PERMILLE** (`1000 − pull*1000/(pull+retain)`) · **+0xBC outgoing_value**
- +0xC4 `pirate_hunt` (privateer total is **+0xE8**) · **+0xCC `p_pow`** (NOT an accumulated total)
- +0xD0/+0xD4 collector_power (with/without pirates) · +0xDC/+0xE0 pull/retain power
- **+0x120 node id (== array index)** · +0x124 dirty · +0xA8 **CTradeNodeDefinition***
- +0xF0/+0xF8/+0x100 **incoming-link vector**, stride 0x20, built only at 0xB54C42:
  +0x00 vptr(0x1CE9258) · +0x08 0x165 · **+0x10 value (signed)** · **+0x14 `add` (steering extra)** ·
  **+0x18 source node's DEFINITION** (saved as `def->+0xD8`)
- +0x108/+0x110/+0x118 **vector<int32> trade_goods_size** (quantity ×1000; slot k ↔
  00_tradegoods.txt index k−1; inject_g = quantity × current price, spec 1.8)
- per-link runtime state: **`node+0x88[i]` share (permille)**, **`node+0x70[i]` enabled**
- **per-country record array**: `rec = *(char**)(node+0x18) + 0xC0*countryTagIdx`,
  count `*(int32*)(node+0x24)`; tag idx `(int16)(*(u64*)(country+0x20)>>32)`.
  Offsets proved by `Entry::Save` @0xB5E320:
  +0x10 tag (idx +0x14, valid byte +0x17) · +0x18 light_ship · +0x1C ship_power ·
  +0x20 privateer_mission · +0x24 privateer_money · +0x28 province_power ·
  **+0x2C power_fraction** · +0x34 **money** · +0x38 **total** · +0x3C potential · +0x40 prev ·
  +0x44 max_demand · **+0x48 val (trade power)** · +0x4C max_pow · +0x50 t_out · +0x54 t_in ·
  +0x58 add · +0x5C already_sent · +0x60/+0x78/+0x90 lists ·
  **+0xA8 steer target LINK INDEX** · **+0xAC type (0 collect / 1 steer)** ·
  **+0xAD has_capital** · **+0xAE has_trader** · +0xAF has_subject · +0xB0 trading_policy · +0xB8 policy date

## The engine's own value math (so the mod can substitute at the right point)
```
power           = min(val, max(0, max_pow*max_demand/1000)) + t_in − t_out
collect-eligible= has_trader ? (type==0) : has_capital
retention       = 1000 − pull*1000/(pull+retain)            [permille]
outgoing        = (1000 − retention) * (local + Σ incoming) / 1000
PushValue(0xB54670): share[i]*value_added_outgoing/1000 * (1000+Σ merchant bonuses)/1000
                     -> destination node's +0xB0, and appends the incoming record
pass 10 (0xB584F0):  rec.total = node.current * rec.power_fraction/1000
                     rec.money = rec.total * (1000 + trade_eff + [merchant? TRADE_MERCHANT_PRESENT])/1000
                     CCountry::AddDelayedIncome(country, 2, &money)   [0x338A90; category 2 = TRADE]
                     -> country+0x68 and ledger at country+0x760
```
- `value_added_outgoing == outgoing` always, because its multiplier global 0x2458F38 is a BSS dword
  **nothing in the image ever writes**. `power_fraction_push (+0x30)` is a dead field.
- Real save serializer is **0xB5A5B0** (the 0x13CF*/0x13D2* sites are tradeinterface.cpp widget names).

## THE HOOK POINTS (spec 2.6)
- **0xB4BF09** — after the whole calc-order loop, before the pass-10 loop; `rsi` = mgr. Every node's
  `+0xB0` (pool) and every `rec+0x2C` (power_fraction) are final and nothing recomputes them.
  Overwrite there => the engine's own collector division, ledger, AI readers and UI all consume the
  model's numbers. **This is where spec 2.6's write belongs.**
- 0xB4BF00 — per node, right after its own 0xB52160; downstream nodes not yet run, so their incoming
  records and +0xB0 are still editable.
- Each pass has exactly ONE E8 call site (all 5-byte detours): 0xB4BEFB→0xB52160, 0xB530A0→PushValue,
  0xB52C52→shares, 0xB52C6F→retention, 0xB4BF44→pass 10.
- Validated arithmetically on 4 saves: `val=max_pow*max_demand/1000` 1319/1319; `power_fraction`
  656/656; `total=current*power_fraction/1000` 656/656; `outgoing` 261/262; `current` 271/274.
- UI caches (display side, rewritten every frame from 0x814F99 while window open): +0x160 incoming,
  +0x164 outgoing, +0x168 local, +0x16C total, +0x170 our_from_this, +0x180 goods_produced.
- **No stored "total"**: node window (0x13CFC02), map box (0x1336656), tooltip (0x13D3D04) and the
  value pass (0xB52DCC) each recompute `local(+0xB4) + Σ incoming[i](+0x10) − outgoing(+0xBC)`.
  => writing local/link-values/outgoing drives the whole aggregate display with NO UI hooks.

## CTradeNodeDefinition
- vtable 0x1C439D0; name inline std::string at +0x10.
- +0x80/+0x88 incoming defs · +0x98/+0xA0 **outgoing link entries** (stride 0x78, target def at +0x30,
  drawn polyline at +0x58/+0x60) · +0xD8 node index · +0xDC location province ·
  +0xE5 `end` / +0xE6 `inland` (LIKELY).

## Monthly update / value pass
- Driver `fn 0xB4BA90(mgr)`, called from 0x75D7DE. Passes: 4 = 0xB51360 (clear/resize tgs),
  5 = 0xB51500 (fill tgs + local), 9 = 0xB52160 (flow/value). Write-back point 0xB4BF00 (rbx=node,
  rsi=mgr). Tick chain DailyTick 0xB79520 → 0x758430 → 0x75D690 → 0xB4BA90.
- Quantisation (probe 16): **in the simulation** — every value field is int32 ×1000 in live memory.

## Direction gates (spec 1.10) — THREE uint8 matrices on the manager
- A `G+0x2220` (BFS 0xB4D0D0, seed trade capital) · B `G+0x2228` (+every merchant node) ·
  C `G+0x2230` (gated BFS 0xB4D530). Size `G+0x2238`, stride `*(i32*)(G+0x21BC)`,
  index `countryIdx*stride + node->[0x120]`. Rebuilt each tick at **0xB4BD0A** inside the manager Update.
- Make every nation-pair gate TRUE: fill the matrices with 1 after each rebuild (detour at 0xB4BD0A).
- Out-of-line predicates: `IsNodeUpstreamOfCountry` 0xB4E020 (matrix B, 2 callers), treasure-fleet gate
  0x3E1D30 (matrix A, 3 callers). 21 gate sites total (see gates.md). Trade-conflict CB 0x38D8C0 does
  NO direction test (pure threshold — matches §1.10). No scripted is_upstream trigger exists.
- **Treasure fleets** `CCountry::SendTreasureFleet 0x3E1EC0`: walks outgoing lists greedily, first hop
  satisfying matrix A (0x3E23D5), privateer skim per node at `node.countries[c][0x20]/node[0xC8]`
  (0x3E2200). If gate forced true WITHOUT fixing matrix A, router finds no hop and teleports with zero
  skim — must detour the router (0x3E2358), not just fill the table (spec 3.12).

## Merchants / envoys / AI
- Merchants: `((CEnvoyContainer**)(country+0x1480))[1]`, vector<CEnvoy*> at +0x20/+0x28.
- CEnvoy (0x48 B, vtable 0x1CAC2F0): +0x10 CMerchantConstruction*, +0x18 action (0 free/1 travel/2 posted),
  +0x20 std::string name, +0x40 type (1=merchant), +0x44 id.
- CMerchantConstruction (0xA0 B, vtable 0x1C4B160): +0x38 dest prov, +0x40 country, +0x48 envoy,
  +0x80 node, +0x88/+0x90 from/to prov, +0x20..+0x30 travel dates/progress, +0x98 direction, +0x9C type.
- Node record mutators: SetTrader 0xB596E0, SetTraderFlags 0xB5E290, ClearTrader 0xB59B50.
- Commands (fill struct + call Execute, or post via 0xBFE50):
  - **send_merchant** token 0x27A0, Execute 0x274180, payload {country@0x50, CProvince*@0x58, envoyId@0x60, type@0x64}
  - **steer_command** token 0x2DB9, Execute **0x5DA4F0**, payload {country@0x50, linkIndex@0x58, nodeIndex@0x5C}
  - cancel_merchant token 0x2AC4, Execute 0x274870
- AI trade subsystem: vtable 0x1C43690 slot +0x60 = 0x1B82B0; driver OnDailyUpdate 0xE4890
  (`if(--[this+0x20]==0) update()`), **cadence hard-coded 10 + rng()%15 days (10–24, mean 17)**, no define.
  Manager 0x1BC1E0: re-steers at 0x1BCE6C (emit steer_command), does nothing while any merchant travels
  (0x1BCED0), places/relocates via evaluator 0x1BD6C0 with **×1.5 hysteresis** (0x1BD206) vs worst
  existing placement. => vanilla's own AI is already a computed-gain test with a 1.5× threshold + a
  de-facto dwell floor (travel + 10–24d tick), matching the user's §3.14 prior.

## UI hooks (spec 1.12)
- Node-window refresh 0x13CFB60 (callers: per-frame HUD 0x814F99, open path 0x13CD6AE). Format /1000 two
  decimals (helpers FormatMilli 0x1703850/0x1703C40, SetText 0x152AE10/0x152AD90).
- Listboxes 0x13D5560 built from the DEFINITION graph, carry NO value — per-entry additive.
- Link click 0x13CCE80 (both lists identical — probe 14). 0x831790 already two-way: with a merchant in
  placement mode tail-calls 0x1419470(nodeIdx) if 0x1418E70(nodeIdx) approves. So incoming-entry
  assignment = gate 0x1418E70 + per-entry data.
- Arrow layer (probe 7: SEPARATE from economic link) built by **0x10AFA70** from the definition file only,
  clears+rebuilds whole layer (callable on demand for a per-good view). Visibility zoom-only
  (DRAW_TRADEROUTES_CUTOFF at 0x233E9E8). No engine "selected trade good" state — fully DLL-owned.
- Probe 4 consumers of the signed incoming value: node total 0x13CFC23, map icon 0x1336663, map tooltip
  0x11C4EB7, entry tooltip 0x13D3D04 (has an explicit minus branch). Protect-trade/arrow-render consumers
  not found statically (open).

## Provinces, trade goods, prices (spec 1.3 / 1.8 live inputs)
```
provinces = *(char**)(G+0x1CA8)      INLINE array, stride 0x2E10, subscript == province id (id>=1)
nprov     = (G[0x1CB0]-G[0x1CA8])/0x2E10
goodsdb   = *(void**)(base+0x242BE70)      good(i) = goodsdb[0x10][i];  n = (db[0x18]-db[0x10])/8
price(i)  = *(char**)(*(void**)(G+0x25D0)+8) + i*0x38      count at pricevec+0x14
```
- CProvince (ints ×1000): +0x20 id · **+0xE8 CTradeNode*** · +0x2E0 state (prosperity at state+0x18,
  may be NULL) · +0x3E0/+0x3E4/+0x3E8 base_manpower/tax/production · +0x3F8 colonysize ·
  +0x428 local_autonomy · +0x42C devastation · **+0x458 CTradeGood*** · +0x468 owner · +0x470 controller ·
  +0x890 trade_power · +0x958 bit 0x10 = is_city · +0x998 modifier set.
- Country handles are 8 bytes: index `(int16)(h>>32)`, **byte 7 = validity** → `*(u8*)(prov+0x46F)!=0`
  means "has an owner".
- CTradeGood: **+0x7C base price**, **+0x18 std::string name**, +0x78 id. Price entry: **+4 current price**,
  +0x00 world supply (LIKELY). `change_price`: `current = base × max(10, 1000+Σ mod[+0x14])/1000` (0xD359A0).
- `GetGoodsProduced` **0xA112A0**:
  `out = max(0, (prov_mod(0x14)+ctry_mod(0x1EB)+add) × (1000 + max(-1000, prov_mod(0x15)+ctry_mod(0xB8)+pct))/1000)`
  `GetTradeValue` **0xA13FD0** = `goods_produced × current_price / 1000` (annual).
- Pass 5 (0xB51500, `this` = CTradeNode): trade power → **controller +0x470**, gated on owner validity
  +0x46F; `trade_goods_size[g] += goods_produced`; +0xB0/+0xB4 accumulate trade value then ×1000/12000
  = **÷12**. This is exactly spec's `Σ_g tgs(n,g)×price(g)÷12`; the residual is per-province vs per-good
  truncation.
- **TRAPS**: (a) the four condition modifiers (devastation/prosperity/under_siege/occupied) reach goods
  produced ONLY through the accumulator at prov+0x998 as modifier ids 0x14/0x15 — reading +0x42C as well
  DOUBLE-COUNTS devastation; (b) 0xA112A0 includes the owner's global_trade_goods_size (ids 0x1EB/0xB8)
  which spec §1.3 excludes — for owner-agnostic wealth read prov_mod(0x14)/(0x15) directly;
  (c) shipped files define **32** goods but the live tgs vector has **33** slots — read the count at
  runtime from `(db[0x18]-db[0x10])/8`, never hardcode.


## OBSERVED in the running game: power_fraction semantics (settles spec 3.10)
Dumped from the live records at sevilla / genua / english_channel (Castile 1444):
- `Σ power_fraction` per node = **0.995–0.998**, and it is **nonzero only for collectors**
  (every steering record, type=1 with a nonzero steer_link, has pf = 0).
- `rec.total = node.current × pf` reproduces exactly (sevilla tag#…401: pf 0.556, total 3.127 →
  current 5.62); `rec.money = total × (1 + trade efficiency)` (3.127 → 3.345).
- **Consequence: the mod must NOT overwrite power_fraction.** Spec 3.10's factorisation is
  literally how the engine is built — a good-independent share among collectors multiplying the
  collectible pool. Writing the model's pool into `+0xB0` is therefore *sufficient*: the engine's
  own division then pays every country `engine_powershare × model_pool`, which is exactly test
  E1's identity. `install_power_shares()` exists but stays behind the `pgt.INCOME` marker and is
  off by default.
- Caution recorded: the engine's collector set is not exactly `has_trader ? type==0 : has_capital`
  — genua shows records with trader=1/type=0/capital=0 carrying pf=0 (merchant likely in transit).
  Preserving the engine's own collector set is the reason not to invent shares.


## TRAP: never resolve engine indices through a tradenodes FILE
A merchant's steer target is stored as an **index into the engine's own outgoing-link list**
(`rec+0xA8`). The DLL was resolving that index through the vanilla
`common/tradenodes/00_tradenodes.txt`, while the running game had loaded the MOD's emitted file.
Measured difference between the two files: same 159 undirected edges (test A3 holds), but the
declaration order differs, **69 of 80 nodes have a different outgoing list**, and **77 links are
declared the opposite way round**. Resolving through the wrong file pointed most steering at the
wrong destination, silently. Effect of the fix (live): steer entries resolved 298 -> **425**.
Rule: read link order, link targets and node identity from LIVE MEMORY
(`install::live_link_targets`, definitions at `ptr@0x242BE48`), never from a file.


## TRAP: a rewritten rel32 must reach its target (x64 hooking)
Redirecting a 5-byte `call rel32` to your own code only works if that code sits within **±2GB** of
the call site. `VirtualAlloc(nullptr, ...)` can return anything in the 64-bit space; when it lands
further away the displacement truncates and the call jumps to garbage. Symptom observed here:
`EXCEPTION_ACCESS_VIOLATION at 0x7FF6A7C40000` — EU4's own **image base**, i.e. execution landed on
the DOS header, with a stack of unnamed `eu4.exe` frames. The game died the moment it unpaused.
Fix: allocate the thunk near the site (probe `VirtualAlloc` at increasing offsets from the call
site, allocation-granularity aligned) and assert the displacement fits in int32 before writing.
Note `detour.h` is immune: it jumps via `jmp [rip+0]; dq target`, an absolute 64-bit pointer.

## Tools
- Debug-log triples (__FILE__/__LINE__/msg): `re/logmap.txt` (1197 rows). Token table: `re/tokens.txt`
  (6648 rows) — `mov edx,<id>` in serializers gives field-offset ↔ save-key. RTTI is stripped (/GR-).
- Ghidra project: `C:\re\proj` (eu4 imported+analysed). `impl/tools/disasm.py`, `scratchpad/dumpfn.py`,
  `scratchpad/callxref.py`, `scratchpad/eu4re.py`.

## Trade field map (static RE, agent a112f303, 2026-08-24)

Confirms and corrects the offsets this DLL already uses. Two corrections worth keeping:

- **`definition+0xD8` is 1-BASED.** It is the definition's DB index, and the engine indexes
  `CTradeNode[def+0xD8]` directly (`0xB54C01`: `test ecx,ecx; jle ->null`), because slot 0 holds
  the node built from the `"Null"` sentinel definition. In vanilla it runs 1..80 and
  `node+0x120 == def+0xD8`. `incoming.from` in a save is the file position **+ 1**.
- **`Castile1444_12_22.eu4` is NOT vanilla** -- its meta names `mod/pgt_permute.mod` (probe B2,
  reversed declaration order), so its 80 nodes are in reverse `00_tradenodes.txt` order. Any
  ordering claim must use `VANILLA_start.eu4`.

Structure sizes: definition **0xE8**, outgoing link entry **0x78**, per-country record **0xC0**,
`CTradeNode` **0x138**.

Link entry (0x78): `+0x10` std::string name, `+0x30` resolved target def*, `+0x38` ordinal (its
own position at parse time), `+0x40` `path` intrusive list, **`+0x58/0x60/0x68` `control`
vector<float2>** (the ribbon polyline -- display-only), `+0x70` unknown, never set by the parser.

Country record (0xC0): `+0xA8` `steer_power` is a **bare 0-based position into
`def->outgoing`**, `+0xAC` type (0 collect / 1 steer). Canonical setter is
**`0xB5E290 SetTraderFlags(rec, bool hasTrader, u8 type)`** -- writes `+0xAC` and `+0xAE` together (the INNER function). The OUTER `0xB596E0 SetTrader(node, handle, type)` addresses the record, scores the outgoing links ONLY when type == 1 (`0xB59767`) and writes the chosen ordinal to `+0xA8` (`0xB599AE`) before calling it; its four callers are `0x25AE22` (arrival), `0x25B9A3` (instant placement), `0x27424A` (send_merchant command), `0x305C6C` (trade-capital move). nocollect.h hooks the OUTER prologue (15 relocatable bytes `48 89 5c 24 08 48 89 54 24 10 55 56 57 41 54`).
`+0xA8` readers use SIGNED compares with NO lower bound: a negative ordinal at `0xB54F8F`
zero-extends into `rax=0xFFFFFFFF` and writes ~16GB past `node+0x88`. Never write a negative;
a node with zero outgoing links must have `+0xAC == 0`.

Vector ownership (matters to `outlinks.h`): `def->outgoing` and `def->incoming` are real MSVC
`std::vector`s on the game's CRT heap. Growth (`0xB6AB50`, `0xCC220`) and teardown call
`operator delete` on OUR buffer if we repointed it. `CTradeSystem::Init` (`0xB4C620`) clears
every `incoming` (`end = begin`) and refills it via `Link()` (`0xB69710`), so an `incoming`
swap survives only until a graph rebuild. Also: `CalcSteerPower`'s zeroing loop iterates
`def->outgoing`'s count but writes into `node+0x88` -- enlarging outgoing without resizing
`node+0x88` is an immediate heap overflow. (`outlinks.h` already resizes both, with slack.)

Outgoing ORDER is load-bearing beyond drawing: `country+0xA8`, the parallel `node+0x88`
array, and BOTH directions of serialisation are positional. Reordering silently re-points
every steering merchant in the node.

## CTradeNode complete layout (static RE, agent a5bc7660, 2026-08-24)

Derived from `CTradeNode::Save` `0xB5A5B0` / `Load` `0xB59BB0` plus the ctor `0xB50FA0`,
move-ctor `0x785DD0` and dtor `0x7860E0` (which walk all 0x138 bytes, so padding and strides are
proven). Token names came from a static table at RVA **`0x1FD8660`** (6645 entries, stride
`0x208`, `{i32 id; char name[]}`) copied to `0x242B888` by `0x170D250` -- that table makes any
future save-format RE in this binary mechanical.

New fields this DLL did not have:

- **`+0x70/0x78/0x80` = `link_enabled`, one BYTE per outgoing link.** Resized to the link count
  every month by `0xB513B5`. Read UNBOUNDED at `0xB550A4` (the fallback even split). We do not
  extend `def->outgoing`, so this stays consistent -- but any future code that does must resize
  `+0x70` as well as `+0x88`.
- `+0x58/0x60/0x68` an unserialised `vector<T*>` cleared monthly (privateer share).
- `+0x124` is the calc-order **DFS visited flag**, not a dirty bit (set `0xB4B183`, cleared for
  all nodes at `0xB4BEC0`).
- `+0xC8 total` is total trade POWER, `+0xD0`/`+0xD4` are
  `collector_power_including_pirates` / `collector_power`.

Invariants measured across all 80 nodes of a save -- these are the ones our writes must not break:

| Invariant | Verified | Violated => |
|---|---|---|
| `current == local + SUM incoming.value - outgoing` | 80/80 | the user's own rule; a negative total |
| `outgoing == (1000-retention) * (local + SUM incoming.value) / 1000` | 80/80 | |
| `value_added_outgoing == outgoing` | 80/80 | splitting them creates or destroys value |
| `retention` in `[0,1000]` | | `>1000` => **negative `outgoing`** at `0xB52E84` |
| **`total != 0` whenever any country record exists** | | `0xB52B93` sets `power_fraction = -1`, which yields **negative income in pass 10** |
| `len(steer_power) >= outgoing link count` | | OOB at `0xB547F9`, `0xB5654D`, `0x13FC24D` |

`steer_power` does **not** always sum to 1000 -- measured sums are {0, 998, 999, 1000}, because
the normaliser at `0xB55014` truncates. Sum > 1000 duplicates value; sum < 1000 leaks it.

Unchecked accesses confirmed (all read `node+0x88` with no bound test): `0xB547F9` PushValue,
`0xB5654D`, `0x13FC24D`, `0xB556FF` (UI). And one unchecked **write**: `0xB54FBA` in
UpdateSteerPower -- its clamp at `0xB54FA5` only fires when `index > count-1`, so an EMPTY
`steer_power` (count-1 == -1) skips the clamp and writes out of bounds for any index >= 0.
Carrying slack in `+0x88` (which `outlinks.h` does) defuses all of these.

At our hook `0xB4BF09` the driver does only `for each valid node: 0xB584F0(node)`, and pass 10
writes NO CTradeNode field. So everything we write survives to the UI and to a save; only
`+0xB0 current`, `+0xD0`, `+0xE8` and the country records at `+0x18` are consumed afterwards.
Every scalar is wiped at the START of the next month by `0xB51290`/`0xB51360`.

## CGuiOverlappingElementsBox child list (measured live, 2026-08-25)

`director_flags` on a trade-link panel is a `CGuiOverlappingElementsBox` (vtable `0x1DA4910`).
Dumped `box+0xE8..0x120` in the running game: `+0xE8` heap ptr, **`+0xF0` and `+0xF8` two
vptrs** (the list sub-object begins at `+0xF0`, its vptr `0x1D90318`), **`+0x100` head,
`+0x108` tail** (node = `{payload@0, prev@8, next@0x10}`, 0x20 bytes), `+0x110` is NOT a count
(holds a float). Remove one child: `box->vt[0x270](box, holder, relayoutNow)`; clear all:
`vt[0x278]` (deletes children); relayout `vt[0x2C0]`.

On a FORWARD panel for link #0 the list is **empty after Update** across 10,932 inspections --
the engine does not draw reverse-end (`+0xA8 = 0`) records there, so no alias removal is needed.

## Box child removal is unlink-only (disassembled 2026-08-25)

`CGuiOverlappingElementsBox::vt[0x270]` = `0x163D8B0` forwards to the list sub-object's
`vt[0x40]` = `0x1530240`, which scans from `subobj+0x10` for `node->payload == child`
(`0x1530260`), frees the 0x20-byte LIST NODE via `0xDF1A0` (`0x153026E`, operand `rdx` = the
node), then tail-jumps to `0x4741B0(child, subobj+8)` to drop the child's reverse registration.
It never calls the child's destructor and never `operator delete`s the child. So after
`vt[0x270]` the holder is the caller's to destroy -- `flagfix.h`'s `vt[0](holder, 1)` after
removal is correct, not a double-free. 2048 live removals in one run without a fault agree.

## Drawing a country shield on a trade-link panel (shield-creation trace, 2026-08-25)

The engine row builder (0x13FDBE0..0x13FDDB0) inlines two helpers:
- **`0x152DF80` holder ctor**: `Holder* (Holder* this, CGui* gui, const std::string* windowName)`.
  Holder is 0x50 bytes from operator new (`0x1A332D4`); `+0x40` = the CGuiWindow built from the
  "trade_node_trader" template. The engine keeps a static MSVC std::string of that name at
  `0x232B4C0` (`{ptr@0, size=0x11@+0x10, cap=0x1F@+0x18}`); pass that.
- **`0x10B44B0` shield setup**: `f(iface rcx, elem rdx, uint64 handle r8, bool setFrame r9b,
  bool clickable [rsp+0x20], bool defaultTooltip [rsp+0x28], u8 flagA [rsp+0x30], u8 flagB [rsp+0x38])`.
  The panel passes `(1,1,0,1,0)`. `iface = *(*(*(0x233FE78)+0x1E00)+0x58)`. Sets `icon+0x1E8` =
  handle, the frame index, click delegates, then `vt[0x300]` and `vt[0x88]`.
- CGui manager: `*(void**)0x23494F0`. `window->vt[0xC8](window, "trade_node_trader_shield")` finds
  the icon; it returns a non-NULL fallback on a miss, so always build from the template.
- Append: `box->vt[0x260](box, holder, 0)`; then `box->vt[0x2C0](box)` once. Clear all: `vt[0x278]`
  (deletes the children).
- `icon+0x10` = the source definition location province; no reader found, set for fidelity.

The country handle is `*(uint64*)(rec+0x10)` -- copy it, never synthesise (the validity byte at
bits 56..63 matters). Shields we add are wiped by the engine count gate on the next frame, so they
are re-added from the Update hook every frame, the same cost the removal path already pays.

## Direct merchant placement (send-merchant trace, 2026-08-26)

**`0x3BAD90 PlaceMerchantAtNode(CCountry* rcx, CEnvoy* rdx, u8 mode r8b, CTradeNode* r9,
int32 steerLinkIndex [rsp+0x20], u8 force [rsp+0x28])`** -- mode 0 collect / 1 transfer;
steerLinkIndex -1 = engine's choice; force 1 skips the eligibility check. Callers: trade-company
add/remove `0x3BAB22`/`0x3BB173`, and `0x774E05` (picks the first envoy with `+0x18 == 0` and
calls with mode=0, link=-1, force=0).

Body: `operator new(0xA0)` -> `CMerchantConstruction` ctor `0x25AAF0` -> `mc+0x40 = country+0x20`
(the 8-byte handle; `CCountry+0x20` IS the handle, confirmed at `0x774E02`/`0x3BADD0` and
`0x305C27`) -> node location province -> `SetEnvoy(mc, prov, envoy, force*2+1)` -> `envoy+0x18 = 2`
(`0x3BAE14`) -> if steerLinkIndex >= 0: `GetTraderRecord` `0xB58CC0` then `rec+0xA8 = it`
(`0x3BAE33`). `force*2+1` in {1,3} takes SetEnvoy's instant branch (`0x25C9BD`; progress 0x3E8),
tail-jumps into Update, where `cmp ecx,3; je` at `0x25B920` skips `CanSendMerchantTo` and reaches
`SetTrader` at `0x25B9A3`. The `+0xA8` write lands after SetTrader's link scoring (`0xB599AE`), so
a passed index overrides. One call = send + steer, no queue, no gate, no travel.

Caveat: SetTrader on that path is guarded by `rec+0xAE == 0` (`0x25B98E`): at a node where the
country already has a trader the envoy is placed but the record's mode is not rewritten.

Envoy lifecycle: action 1 (travelling) set at `0x25C896`/`0x25C923` in SetEnvoy; action 2 (posted)
at `0x25AE0B` in `CMerchantConstruction::Update`, then SetTrader `0x25AE22`; action 0 (free) at
`0x9DC3EC` after `0x6FF570(envoy, 0)` (recall). `CMerchantConstruction+0x80` (posted node) is
written only by the ctor `0x25AB92` and the re-derive `0x25AC10` (`= province+0xE8`). `rec+0xAE`
has one semantic writer, `0xB5E2FF` inside SetTraderFlags `0xB5E290`, reached by `call 0xB599E5` and by ClearTrader's tail `jmp 0xB59BA4` (both enter at the prologue). Non-semantic writers of `+0xAC`: the deserializer `0xB5EDC5` and the record copy `0x785D81`.
`0x305C6C` = `SetTrader(homeNode, handle, 0)`, the default collect-at-home.

## `country+0x68` is NOT the monthly trade-income accumulator (measured 2026-08-26)

`AddDelayedIncome` (`0x338A90`) does `add [country+0x68], eax` and then posts the amount to the
per-category ledger at `country+0x760` (`0x338B05..0x338B17`, category in `edx`). Logging every
call from pass 10: category 2 (trade) fires once PER RECORD (52,614 calls/month across 80 nodes),
and the sum booked to a country equals `SUM rec.money` to the cent (Ming: 8.689 vs 8.69). Yet
`+0x68` moved only 0.253 for Ming -- it is drained or reset by something else within the month.
Use the ledger, or the booking sum, never `+0x68`, for any treasury reconciliation.
