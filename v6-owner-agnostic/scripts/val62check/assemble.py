# -*- coding: utf-8 -*-
"""Assemble validation-v62.md from the seven fragments, applying coordinator recheck edits."""
import re, io, collections, hashlib, os

BASE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod\per-good-trade\v6-owner-agnostic"
os.chdir(BASE)

ORDER = ["0","1.1","1.2","1.3","1.4","1.5","1.6","1.7","1.8","1.9","1.10","1.11","1.12",
         "2.1","2.2","2.2a","2.3","2.4","2.5","2.6","2.7","2.8","2.9",
         "3.1","3.2","3.3","3.4","3.5","3.6","3.7","3.8","3.9","3.10","3.11","3.12","3.13","3.14","3.15","3.16"]

blocks = {}
for n in range(1, 8):
    txt = io.open("validation-v62-part%d.md" % n, encoding="utf-8").read()
    parts = re.split(r"(?m)^## ", txt)
    for p in parts:
        m = re.match(r"\u00a7(\d+(?:\.\d+)?a?)\b", p)
        if not m:
            continue
        key = m.group(1)
        blocks[key] = "## " + p.rstrip() + "\n"
missing = [s for s in ORDER if s not in blocks]
assert not missing, "missing sections: %r" % missing

S = "\u00a7"  # section sign
D = "\u2014"  # em dash

R = {
"Y651": "| Y651 | Two-node cycle: STACK_OVERFLOW at one address, 1002 frames, three launches; vanilla and reversed file load | CONFIRMED | artifact read [rechecked by coordinator] | three engine crash dumps exist: crashes/eu4_20260820_{134250,134617,165621}, each `Unhandled Exception C00000FD (EXCEPTION_STACK_OVERFLOW) at 0x00007FF6DDE6A8B4`, exactly 1002 `eu4.exe` frames, meta.yml `Mods: mod/pgt_cycle.mod`; pgt_cycle's only diff vs vanilla adds `valencia -> sevilla`, closing a 2-cycle with vanilla's `sevilla -> valencia` (00_tradenodes.txt L1980/L2039); the two no-crash controls (vanilla; 159 backwards links, error.log exactly 159 lines) recorded in `../v2-drain/game-session.md` L99-152 |",
"Y652": "| Y652 | Engine walks the node graph recursively; a cycle never terminates | PARTIAL | artifact read + derivation check [rechecked by coordinator] | recursion and nontermination on the tested cycle are proven by the dumps (1002 same-module frames, single exception address, three launches) and the differential controls pin cyclicity as the cause (vanilla and 159-backwards both load, game-session.md L104-108); but the routine's identity (a node-graph walk) and the universal over all cycles rest on inference from one two-node construction " + D + " disassembly or further cycle shapes would settle |",
"Y653": "| Y653 | Acyclicity enforced because engine provably cannot survive its absence, not (as v2) unprovability | PARTIAL | file read + artifact read [rechecked by coordinator] | v2's contrast wording confirmed verbatim (`../v2-drain/per-good-trade-spec.md` L613-615: 'acyclicity is enforced because we cannot prove the engine tolerates its absence'); the crash basis is real and artifact-verified (see Y651), but **provably** turns one reproduced two-node construction into a universal proof " + D + " what exists is a measurement of one cycle class, not a proof over cyclic inputs |",
"Y667": "| Y667 | 'Any non-collector with power is transferring' is the loose community summary and is wrong | PARTIAL | measurement [rechecked by coordinator: save trade-ledger scan] | the engine's own ledger distinguishes transferring from inert non-collectors (Castile1444_12_22.eu4): at `sevilla`, `pull_power` 17.642 = FRA 3.319 + ARA 14.323 exactly; at `venice` (an end node) 15.199 of non-collector power sits in `total` with **no** `pull_power` field; `bordeaux`/`lubeck`/`north_sea`/`white_sea`/`rheinland` show non-collector power partially excluded from `pull_power` (e.g. lubeck 78.372 vs 66.632) " + D + " so the quoted statement is wrong: that half CONFIRMED from engine arithmetic; the 'loose community summary' attribution is unverifiable within the materials (community sources excluded) |",
"Y487": "| Y487 | 2-node cycle: STACK_OVERFLOW at 0x00007FF6DDE6A8B4, 1002 frames, three launches, controls fine, both from game-session.md | PARTIAL | artifact read + observation cited by the claim [rechecked by coordinator] | the observation itself is artifact-true: three dumps on disk (2026-08-20 13:42:50 / 13:46:17 / 16:56:21) with identical address, 1002 frames each, cycle mod loaded " + D + " so 'reproduced on three launches' is correct, and 'the dump records no per-frame addresses' verified (frames read '(function-name not available) (+ 0)'); but the sentence cites *both* observations to `../v2-drain/game-session.md`, which records **two** launches ('reproduced on two independent launches', 'stack overflow, twice', L71-72) " + D + " the third dump post-dates the cited record, so the citation, not the count, is wrong |",
"Y137": "| Y137 | v3.0-v5.0 said neither coefficient in a file, shipped a sweep that walked past the block holding one | PARTIAL | file read + instrument read [rechecked by coordinator] | text half confirmed in all three versions (v3 L544-545, v4 L617, v5 L717: 'hardcoded in the binary " + D + " defines.lua and common/defines/ were searched and contain neither'); the sweep survives and confirms the mechanism: `../v4-owner-agnostic/scripts/audit_modifiers.py` loads `common/static_modifiers` definitions (L21) with `trade_goods_size` among WEALTH_KEYS (L30) yet reports only history-applied modifiers, so `provincial_production_size` (GP_COEFF's block) never surfaced " + D + " 'walked past the block' confirmed; but only v4's tree ships the sweep (v3 has no scripts dir; v5's 61 scripts include no modifier sweep), so 'v3.0 through v5.0 ... shipped' overstates |",
"Y992": "| Y992 | TIE_EPS sink set unchanged ~1e-6 to ~1, band edges from tolerance floor and base-cost ceiling | PARTIAL | measurement [rechecked by coordinator: `val62c_eps.py`, shipped code path; downgraded from a validator REFUTED] | the interval statement is true but the asserted band structure is not: on the shipped path (alpha_Phi=2.0, TIE_EPS2 and LP_OPTS as shipped) the sink set `{genua, hangzhou}` is unchanged at **every** eps from 1e-13 to 1e+12 (24 grid values) " + D + " no transition exists at either claimed edge, so 'below that range it ... stops registering' and 'above it ... stops being a perturbation' are both contradicted for the sink set (orientation drifts by up to 16 edges below 1e-4 and up to 25 above 3; the sinks never move); the cited `scripts/epsilon6.py` cannot run (TypeError: mcf() got an unexpected keyword argument 'cost') and its own docstring pins alpha_Phi=1.5, the pre-v6.1 operator |",
"Y109": "| Y109 | Sweep re-reported on uniform 0.001 grid x1.000-2.600 (europe.py); table withdrawn; x1.973-2.456 three European ends | PARTIAL | measurement [rechecked by coordinator; downgraded from CONFIRMED] | the figures hold: sweep rebuilt on the exact grid (1601 points, `val62p3_europe_sweep.json`), coordinator-validated by from-scratch recomputation at 14 boundary-critical points (14/14 match); x1.973-2.456 carries `{english_channel, genua, rheinland}` " + D + " three European ends, none in Asia " + D + " exactly; but the parenthetical attributes the sweep to `europe.py`, and shipped `europe.py` hardcodes a=1.5, a 0.01 step and x1.00-1.60 (L19, L31-33) " + D + " it cannot produce the documented experiment |",
"Y1109": "| Y1109 | Structural families account for several hundred uses (round6.py, comments stripped) | CONFIRMED | measurement [rechecked by coordinator] | `round6.py` re-run: home_trade_node 36 + *_active_trade_node 165 + *_trade_node_member_province 171 + highest_value_trade_node 38 = **410**; the 15 `all_trade_node_member_province` uses its regex misses (Y412's finding) only raise this to ~425 " + D + " 'several hundred' holds under either count |",
"Y416": "| Y416 | The overlord always receives the treasure fleet | CONFIRMED | file read + design stipulation [rechecked by coordinator] | census types this DESIGN/stipulated: " + S + "1.11 states the mod's own rule and " + S + "3.12 argues it; the vanilla gate the rule removes is file-attested " + D + " `TREASURE_FLEET_TOOLTIP_CANT_REACH_DELAYED:0 'They will keep their gold income instead...'` shows vanilla's non-delivery case " + D + " and the overlord-receipt mechanic by `treasure_fleet_income` modifiers (subject_type_upgrades L47, government_reforms L296); as a stipulation with verified premises the claim stands |",
"Y286": "| Y286 | Coefficients measured on Garnatah (223: 6/4/silk, autonomy 0) and Caceres (1747: 2/2/wool) | CONFIRMED | measurement [rechecked by coordinator: direct save read] | VANILLA_start.eu4: province 223 = base_tax 6.000, base_production 4.000, trade_goods silk, owner GRA, `local_autonomy` absent; 1747 = 2.000 / 2.000 / wool / CAS with `local_autonomy=3.500` **present** " + D + " the same save writes the field when nonzero and omits it at zero, so 223's autonomy 0 is established by the file's own convention, not inferred |",
"Y979": "| Y979 | (CHANGED) `unrest` is deliberately not read; 1444 liveness no longer asserted | CONFIRMED | file read [rechecked by coordinator: the delta instructs grading the new wording, which drops the liveness clause] | `common/static_modifiers/00_static_modifiers.txt` defines `unrest` (local_tax_modifier -0.02 per point); `solver.py:89` `STATE_TAX_MOD = {}` " + D + " defined in the file, deliberately not read; the withdrawn 21-province liveness reading is present in v6.1-frozen and absent from v6.2, as the delta records |",
"Y357": "| Y357 | Item 14: the incoming entry only navigates " + D + " clicking Safi in Sevilla switched the window, dispatched nothing | CONFIRMED | observation cited by the claim + file read [rechecked by coordinator] | the observation is recorded in the cited artifact: `../v2-drain/game-session.md` A1/V067 " + D + " 'Clicked the incoming entry; window navigated to Safi', verdict 'CONFIRMED (navigates only)' (L351-362, L562); corroborated by `interface/tradeinterface.gui` naming the element `NextNodeButton` |",
"Y535": "| Y535 | Engine tooltip and identifier `merchant_steering_to_inland` both read as the inland node; if so " + S + "3.11 inverts | CONFIRMED | file read [rechecked by coordinator] | the sentence asserts how the two artifacts *read*, with the runtime consequence explicitly conditional ('if that holds'); both verified: `eu4.exe` carries `merchant_steering_to_inland` verbatim, and localisation ships `MERCHANT_STEERING_TO_INLAND:0 'Merchant steering towards inland'` and `MERCHANT_PRESENT_INLAND:0 'Merchant present inland'` " + D + " both name the inland side; the antecedent's runtime truth is exactly open probe 11, which the document leaves open |",
"Y1043": "| Y1043 | v6.0 listed Australia, Venice, Deccan among termini; none holds either sink on this field | CONFIRMED | measurement + file read [rechecked by coordinator] | field fact re-derived: spices sinks `{brazil, genua}`, cloves sinks `{brazil, genua, kongo}` " + D + " australia/venice/deccan hold none (coordinator per-good DRAIN run); the v6.0 attribution is verifiable from the project's change record: `changes-v6.md` L395-396 ('It listed Australia, Venice and Deccan among the termini') with the superseded row quoted at L5938 |",
"Y194": "| Y194 | v3.0-v5.0's province-scoped rule was wrong in both independent audits that examined it | CONFIRMED | file read [rechecked by coordinator: both audits located] | audit 1: `../v4-owner-agnostic/validation-v4.md` W041 " + D + " v3.0's structural rule missed the fourth modifier (`chinaware` `local_autonomy` -0.1, 'the fourth v3.0 missed'); audit 2: `../v5-owner-agnostic/validation-v5.md` X024/X044/X045 " + D + " the two-test version wrong on `industrious_personality`, `production_leader` (not local), `bonus_from_merchant_republics` (not local) |",
}

A = {
"Y214": "rechecked: coordinator extended the sample to 7 of 60 (C037, C038, C049 gold invisible to wealth at L457-463, C101 no trade supply range at L778, C128 50/40 at L814, C130 50/50 at L815, C132 reversal at L817-820) " + D + " all folded in; the universal over all 60 remains unexhausted",
"Y217": "rechecked: L81 blanket sentence vs L94-95 concession re-read; Y1080's misattribution is a concrete instance",
"Y015": "rechecked: coordinator's three tokenisations give 307/261/130 unique (1817/1208/316 raw) " + D + " endpoints 279/326 not reproduced by any construction tried",
"Y270": "rechecked: " + S + "3.13 L1879-1884 re-read " + D + " 'Not LP pivot determinism, which " + S + "2.1 retires'; the open items are build/CPU-dispatch bit-identity and DLL fidelity",
"Y1080": "rechecked: grep confirms measure6.py and measure6.out carry no core-node count; props6.py:126 computes it",
"Y041": "rechecked: save fields and trunc arithmetic re-verified by coordinator; the on-screen strings remain out of reach of the materials",
"Y046": "rechecked: 0.49*1.25=0.6125->0.61 vs 6*0.0833333*1.25=0.62499975->0.62 re-computed; ordering argument sound; tooltip unobservable",
"Y288": "rechecked: `global_trade_goods_size_modifier` used in 38 common/ files; tooltip composition unobservable",
"Y291": "rechecked: same arithmetic re-verified; display unobservable",
"Y293": "rechecked: iqta 0.05 and GRA ideas 0.15 re-confirmed; church estate carries `global_tax_modifier = 0.2` (loyalty-scaled), no flat +5%",
"Y295": "rechecked: 75+25+5+15 = 120 file-confirmed; the Clergy 5 derivable only via loyalty arithmetic, total 125.0% unobservable",
"Y353": "rechecked: coordinator greps of defines.lua (COLLECT/OUTSIDE/COLLECTING) and localisation found no -50% off-home collect figure; a save-ledger fit against an off-home collector would settle it",
"Y375": "rechecked: no defines/localisation source found for the both-ends power condition",
"Y379": "rechecked: counterexample re-verified from VANILLA_start.eu4 " + D + " ENG has province_power 177.336 in english_channel yet its chesapeake_bay entry carries only max_demand (no power), and chesapeake_bay's outgoing includes english_channel (00_tradenodes.txt) " + D + " 'no condition on the receiving node' fails",
"Y111": "rechecked: cache validated 14/14 boundary points by from-scratch recomputation; hangzhou 1.000-1.368 / 1.948-1.972, gulf_of_siam 1.187-1.381 only; 3 sub-0.01 segments but exactly one (x1.702-1.709) carries a set appearing once " + D + " the plural fails",
"Y117": "rechecked: coordinator computed loose=81 exact; some/every/unique-shortest-path via the Cape give 71/60/43 " + D + " no construction yields 69",
"Y412": "rechecked: round6.py:232 regex omits `all_`; doc L841 lists it; 15 `all_trade_node_member_province` uses across common/",
"Y420": "rechecked: mapmode_trade.dds verified present; the present-tense display behaviour awaits a built DLL",
"Y421": "rechecked: trade_route_arrow*.dds verified present; same gap",
"Y422": "rechecked: mapmode_trade_goods.dds verified present; same gap",
"Y445": "rechecked: implemented census is boolean OR over 29 live goods (measure6.py L90-101) giving the 5723 quoted at " + S + "3.8; as specified (30 solves incl. Phi_w) it gives 5758, and as a count its max entry is 26 " + D + " description and instrument disagree on both axes",
"Y1032": "rechecked: coordinator re-ran p3_perm.py section B " + D + " copper flips [0,0,2,0,0,2] (sum 4, not 12), paper [2,2,2,0,2,0] (sum 8, exact), max spread 7.66e-10 (exact)",
"Y1035": "rechecked: coordinator's independent construction (val62c_y1035.py) gives deltas 0.043 edge-goods / 0.098 value-weighted " + D + " only the value-weighted metric touches the claimed 0.1-0.2; sinks/spg/acyclicity identical in both worlds",
"Y143": "rechecked: shipped p3_relabel_pergood.py prints 76 (first-order+LP_OPTS) / 12 (full+default tol) / 0 (full+LP_OPTS) " + D + " final figure exact, 84 and 13 reproduced by no construction (76/80/86 and 12 across four independent builds)",
"Y1055": "rechecked: p3_bisect.py re-run " + D + " unset == 1e-7 exactly for all three seeds; the flip count over 4 perms is 2/8/6 by seed, so the quoted 8 is one seed's value; 1e-8 gives 0 for all seeds (confirmed)",
"Y516": "rechecked: L1296-1298 re-read " + D + " 'Items 12-15 are done. They were run ...' followed by 'Item 12 was dropped rather than run'; the folded-into sections verified",
"Y537": "rechecked: coordinator re-derived graph-sources (spices {kongo, the_moluccas}; cloves {the_moluccas}) and sinks " + D + " figures exact; but kongo is Central Africa, contradicting 'Source in Indonesia, and both source there alone' in the same sentence, and spices is *produced* in 18 nodes, so 'source' can only mean graph-sources",
"Y591": "rechecked: coordinator re-ran the instrument " + D + " s-c operator unreachable demand 17.07% unweighted (7.7% value-weighted), genua a cloves sink unreachable from supply (both exact); 'one sixth' (16.67%) matches no construction, nearest is the unweighted 17.07%",
"Y708": "rechecked: both trigger strings verified in eu4.exe by coordinator grep; 'nothing else' remains an absence-of-string inference",
"Y721": "rechecked: defines re-read " + D + " GOLD_INFLATION/TREASURE_FLEET_INFLATION are flat 0.5; INFLATION_FROM_PEACE_GOLD 0.02 'per month of income' shows an income-relative normalisation exists for peace gold, but no file states it for treasure fleets",
"Y732": "rechecked: L1816-1818 vs L1301-1303 re-read " + D + " item 14 'settled, spec confirmed ... " + S + "1.7 stands' did not change what the spec says; item 13 did; item 11 unrun",
"Y790": "rechecked: defines.lua carries only COLONY_MIN_AUTONOMY = 50; no 90/20/0 constants and no pre-Common-Sense file among the materials",
"Y702": "rechecked by coordinator: same five files re-read " + D + " v1 L438/440, v2 L706/708, v3 L984/986 quote 5.7e-14/1.4e-14; v4 L1074 quotes 1.3e-16 and attributes the old figures to 'v1 through v3.0'; finding reproduced",
"Y991": "rechecked: shipped p3_relabel_pergood.py prints 76 of 290 for the first-order config (with LP_OPTS; no first-order+default config is shipped), vs the doc's 84 " + D + " direction holds, figure unreproduced (76/80/86 across three builds)",
"Y1007": "rechecked: relabelling half as Y991/Y143 (76/12/0 vs 84/13/0); alt-optimum half exact " + D + " p3_bisect margins show exactly one good (paper) with a zero-reduced-cost arc off support under the full cost",
}

def apply_edits(block):
    out = []
    for line in block.splitlines():
        m = re.match(r"\| (Y\d+) \|", line)
        if m:
            iid = m.group(1)
            if iid in R:
                line = R[iid]
            elif iid in A:
                body = line.rstrip()
                assert body.endswith("|"), iid
                line = body[:-1].rstrip() + " " + D + " [" + A[iid] + "] |"
        out.append(line)
    return "\n".join(out) + "\n"

VER = collections.Counter()
SECC = {}
ids_seen = set()
sections_out = []
for s in ORDER:
    blk = apply_edits(blocks[s])
    c = collections.Counter()
    for line in blk.splitlines():
        m = re.match(r"\| (Y\d+) \|", line)
        if not m:
            continue
        iid = m.group(1)
        assert iid not in ids_seen, "dup " + iid
        ids_seen.add(iid)
        cells = [x.strip() for x in re.split(r"(?<!\\)\|", line)]
        verdict = None
        for cell in cells:
            if cell in ("CONFIRMED", "PARTIAL", "REFUTED", "UNTESTABLE"):
                verdict = cell
                break
        assert verdict, "no verdict in " + iid
        c[verdict] += 1
    SECC[s] = c
    VER.update(c)
    sections_out.append(blk)

exp = set(l.split()[0] for l in io.open("scripts/val62check/all_ids.txt", encoding="utf-8"))
assert ids_seen == exp, ("id mismatch", len(ids_seen), sorted(exp - ids_seen)[:5], sorted(ids_seen - exp)[:5])

md5 = hashlib.md5(open("per-good-trade-spec.md", "rb").read()).hexdigest()

hdr = io.StringIO()
hdr.write("# Validation " + D + " Per-Good Trade Network Spec v6.2\n\n")
hdr.write("**Document under test.** `per-good-trade-spec.md`, 2,079 lines, MD5 `%s` " % md5 + D + " verified at audit start and at assembly; unchanged throughout.\n\n")
hdr.write("**Inventory.** `claims-delta-v62.md` " + D + " every row of its UNCHANGED (809), REWORDED (20), CHANGED (46) and NEW (84) tables: **959 live claims**, all graded. REMOVED rows are not claims and are not graded. Full census text from `claims-v6.md` where a delta label is compressed; the current document's wording governs, and CHANGED rows are graded on the new assertion.\n\n")
hdr.write("**Sources.** The EU4 1.37.5 install; `scripts/` (instruments re-run, never quoted); `../v1-laplacian/` through `../v5-owner-agnostic/`; EU4 saves as engine-produced evidence (`VANILLA_start.eu4`, `Castile1444_12_22.eu4`, and their trade ledgers); the engine's own crash artifacts (`crashes/eu4_20260820_*`) and the surviving probe mods (`mod/pgt_cycle`, `mod/pgt_flip*`). The running game was not among the materials: claims only a live observation can settle are UNTESTABLE with the missing observation named.\n\n")
hdr.write("**Process.** Seven validators graded disjoint slices in parallel, re-deriving every claim from sources. Every REFUTED and PARTIAL verdict " + D + " and every boundary case " + D + " was then re-verified by the coordinating auditor directly against the primary sources before entering this file; rows carrying \"rechecked\" notes record that re-derivation. Twelve verdicts changed under recheck, including one validator REFUTED downgraded to PARTIAL (Y992) and two UNTESTABLEs settled by engine crash artifacts the validator had not found (Y651, Y652).\n\n")
hdr.write("**Verdicts.**\n\n")
hdr.write("| verdict | claims |\n|---|---|\n")
for v in ("CONFIRMED", "PARTIAL", "REFUTED", "UNTESTABLE"):
    hdr.write("| %s | %d |\n" % (v, VER[v]))
hdr.write("| **total** | **%d** |\n\n" % sum(VER.values()))
hdr.write("Per section:\n\n| " + S + " | CONFIRMED | PARTIAL | REFUTED | UNTESTABLE | total |\n|---|---|---|---|---|---|\n")
for s in ORDER:
    c = SECC[s]
    hdr.write("| " + S + "%s | %d | %d | %d | %d | %d |\n" % (s, c["CONFIRMED"], c["PARTIAL"], c["REFUTED"], c["UNTESTABLE"], sum(c.values())))
hdr.write("\n---\n\n")

with io.open("validation-v62.md", "w", encoding="utf-8") as f:
    f.write(hdr.getvalue())
    f.write("\n".join(sections_out))

print("wrote validation-v62.md")
print("totals:", dict(VER), "sum", sum(VER.values()))
partials = []
unt = []
for s in ORDER:
    pass
for line in io.open("validation-v62.md", encoding="utf-8"):
    m = re.match(r"\| (Y\d+) \|", line)
    if m:
        if "| PARTIAL |" in line:
            partials.append(m.group(1))
        elif "| UNTESTABLE |" in line:
            unt.append(m.group(1))
print("PARTIAL (%d): %s" % (len(partials), " ".join(partials)))
print("UNTESTABLE (%d): %s" % (len(unt), " ".join(unt)))
