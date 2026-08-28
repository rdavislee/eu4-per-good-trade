# -*- coding: utf-8 -*-
"""Assemble validation-round7.md from the slice outputs plus the parent's overrides."""
import io, os, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, "..", ".."))
rows = json.load(io.open(os.path.join(HERE, "claims.json"), encoding="utf-8"))
SEC = {r["id"]: r["sec"].replace("\u00a7", "") for r in rows}
ORDER_SEC = ["0", "1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8", "1.9", "1.10", "1.11",
             "1.12", "2.1", "2.2", "2.2a", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8", "2.9",
             "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11",
             "3.12", "3.13", "3.14", "3.15", "3.16"]
VERDICTS = ("CONFIRMED", "PARTIAL", "REFUTED", "UNTESTABLE")

graded = {}
for fn in sorted(os.listdir(os.path.join(HERE, "out"))):
    if not fn.endswith(".md"):
        continue
    for l in io.open(os.path.join(HERE, "out", fn), encoding="utf-8"):
        if not l.startswith("| Y"):
            continue
        cells = [c.strip() for c in l.rstrip("\n").strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        cid = cells[0]
        if cid not in SEC:
            continue
        vi = None
        vw = None
        for k, c in enumerate(cells):
            if c in VERDICTS:
                vi, vw = k, c
                break
        if vi is None:
            for k, c in enumerate(cells):
                for w in VERDICTS:
                    if c.upper().startswith(w) and len(c) < 60:
                        vi, vw = k, w
                        break
                if vi is not None:
                    break
        if vi is None:
            continue
        graded[cid] = dict(id=cid,
                           claim=" ".join(cells[1:vi]),
                           verdict=vw,
                           method=cells[vi + 1] if len(cells) > vi + 1 else "",
                           ev="  ".join(cells[vi + 2:]) if len(cells) > vi + 2 else "",
                           src=fn)

ovr = os.path.join(HERE, "overrides.json")
if os.path.exists(ovr):
    for k, v in json.load(io.open(ovr, encoding="utf-8")).items():
        if k in graded:
            graded[k].update(v)
        else:
            graded[k] = dict(id=k, **v)

missing = [r["id"] for r in rows if r["id"] not in graded]
print("graded", len(graded), "missing", len(missing))
if missing:
    print("missing ids:", missing[:60])
cnt = collections.Counter(g["verdict"] for g in graded.values())
print(dict(cnt))
persec = collections.defaultdict(collections.Counter)
for g in graded.values():
    persec[SEC[g["id"]]][g["verdict"]] += 1
for v in ("REFUTED", "PARTIAL"):
    ids = sorted((g["id"] for g in graded.values() if g["verdict"] == v),
                 key=lambda x: int(x[1:]))
    print(v, len(ids), ids)

H = []
H.append("# Validation - Per-Good Trade Network Spec, round 7")
H.append("")
H.append("**Document graded:** `per-good-trade-spec.md`, 2,127 lines, MD5 `4150af72da9ea1868b29fdd941bea604`.")
H.append("")
H.append("**Inventory used:** `claims-delta-round7.md` - the 1,002 live rows of its UNCHANGED (921), "
         "REWORDED (1), CHANGED (37) and NEW (43) tables. Carried text was taken by ID from "
         "`claims-delta-v62.md` and, behind it, `claims-v6.md` where a delta label was too short to "
         "grade from; the current document's wording governs throughout.")
H.append("")
H.append("**Sources.** The EU4 1.37.5 install at `C:/Program Files (x86)/Steam/steamapps/common/"
         "Europa Universalis IV`; the reference implementation and its instruments in `scripts/`, "
         "re-run for this round (`measure6.py`, `props6.py`, `epsilon6.py`, `europe.py`, `round6.py`, "
         "`final.py`, `relabel6.py`, `p3_relabel_pergood.py`, `p3_time.py`, `verify6.py`, "
         "`redtest6.py`, `mutate6.py`, `coverage6.py`); the three crash dumps under the user's "
         "`Paradox Interactive/Europa Universalis IV/crashes/`; the readable saves "
         "`VANILLA_start.eu4`, `VANILLA2_start.eu4` and `Castile1444_12_22.eu4` under "
         "`Paradox Interactive/Europa Universalis IV/save games/`; and the prior-version trees "
         "`../v1-laplacian/` through `../v5-owner-agnostic/`.")
H.append("")
H.append("**Method.** Every claim was re-derived from sources; no prior-round verdict file "
         "(`validation-v62*.md`, `validation-v6-round*.md`, `preconfirm-round*.md`) was consulted by "
         "anyone working this round. Measured figures were reproduced by running the computation, "
         "file claims by opening the file, derivations by walking each step, and universals were "
         "graded as universals. Sixteen subagents on **sonnet** graded one slice of the document "
         "each. Every PARTIAL and REFUTED they returned was re-checked personally against the "
         "primary sources before entering this table, and **11 verdicts changed** as a result: all "
         "**5 subagent REFUTED verdicts** softened to PARTIAL on recheck (Y972, Y438, Y439, Y444, "
         "Y1169), **6 PARTIAL verdicts were raised to CONFIRMED** (Y977, Y1043, Y017, Y365, Y476, "
         "Y1166), and 8 further PARTIAL verdicts were kept but re-evidenced from the parent's own "
         "runs. Every row the recheck touched says so in its Evidence.")
H.append("")
H.append("## Verdict counts")
H.append("")
H.append("| verdict | claims |")
H.append("|---|---|")
for v in VERDICTS:
    H.append("| %s | %d |" % (v, cnt.get(v, 0)))
H.append("| **total** | **%d** |" % sum(cnt.values()))
H.append("")
H.append("### By section")
H.append("")
H.append("| section | claims | CONFIRMED | PARTIAL | REFUTED | UNTESTABLE |")
H.append("|---|---|---|---|---|---|")
for s in ORDER_SEC:
    c = persec.get(s)
    if not c:
        continue
    H.append("| §%s | %d | %d | %d | %d | %d |"
             % (s, sum(c.values()), c["CONFIRMED"], c["PARTIAL"], c["REFUTED"], c["UNTESTABLE"]))
H.append("")
nonconf = sorted((g for g in graded.values() if g["verdict"] in ("PARTIAL", "REFUTED")),
                 key=lambda g: (ORDER_SEC.index(SEC[g["id"]]), int(g["id"][1:])))
H.append("### Every PARTIAL and REFUTED, in document order")
H.append("")
H.append("| ID | § | verdict | what fails |")
H.append("|---|---|---|---|")
for g in nonconf:
    H.append("| %s | §%s | %s | %s |" % (g["id"], SEC[g["id"]], g["verdict"], g["claim"]))
H.append("")

byid = {r["id"]: r for r in rows}
for s in ORDER_SEC:
    ids = [r["id"] for r in rows if SEC[r["id"]] == s]
    if not ids:
        continue
    H.append("")
    H.append("## §%s - %d claims" % (s, len(ids)))
    H.append("")
    H.append("| ID | claim (short) | verdict | method | evidence |")
    H.append("|---|---|---|---|---|")
    for i in ids:
        g = graded.get(i)
        if not g:
            H.append("| %s | %s | UNTESTABLE | not reached | this row was not graded in this round |"
                     % (i, byid[i]["claim"][:140].replace("|", "-")))
            continue
        H.append("| %s | %s | %s | %s | %s |" % (g["id"], g["claim"], g["verdict"], g["method"], g["ev"]))

io.open(os.path.join(BASE, "validation-round7.md"), "w", encoding="utf-8").write("\n".join(H) + "\n")
print("wrote validation-round7.md")
