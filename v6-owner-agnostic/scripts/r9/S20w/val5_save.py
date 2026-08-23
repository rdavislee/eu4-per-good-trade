# -*- coding: utf-8 -*-
"""Independent save reader for the round-5 audit. Parses province records out of
VANILLA_start.eu4's gamestate and dumps a JSON of the fields the spec's 1.3 claims turn on."""
import io, os, re, json, zipfile, sys

SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")

def matching_brace(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"': inq = not inq
        elif not inq:
            if c == "{": d += 1
            elif c == "}":
                d -= 1
                if d == 0: return k
        k += 1
    return len(s) - 1

def load(save=SAVE):
    raw = zipfile.ZipFile(save).read("gamestate").decode("latin-1")
    i = raw.index("\nprovinces={"); j = raw.index("{", i)
    body = raw[j+1:matching_brace(raw, j)]
    out = {}
    for m in re.finditer(r"^-(\d+)=\{", body, re.M):
        st = body.index("{", m.start())
        rec = body[st+1:matching_brace(body, st)]
        pid = int(m.group(1))
        d = {}
        for key in ("owner", "controller", "trade_goods", "base_tax", "base_production",
                    "base_manpower", "devastation", "prosperity", "revolt_risk", "name",
                    "unrest", "nationalism", "occupied", "num_of_revolts"):
            mm = re.search(r'^\t\t' + key + r'="?([^"\n]*)"?', rec, re.M)
            if mm: d[key] = mm.group(1).strip()
        out[pid] = d
    return raw, out

if __name__ == "__main__":
    raw, P = load()
    print("provinces parsed:", len(P))
    owned = {p: d for p, d in P.items() if d.get("owner")}
    print("owned:", len(owned))
    dev = {p: float(d["devastation"]) for p, d in P.items() if d.get("devastation") and float(d["devastation"]) != 0}
    print("devastated (any):", len(dev), sorted(dev.items())[:20])
    rr = {p: float(d["revolt_risk"]) for p, d in P.items() if d.get("revolt_risk") and float(d["revolt_risk"]) != 0}
    print("revolt_risk nonzero:", len(rr))
    print(sorted(rr.items()))
    un = {p: d["unrest"] for p, d in P.items() if d.get("unrest")}
    print("unrest keys:", len(un), sorted(un.items())[:10])
    json.dump({str(k): v for k, v in P.items()}, io.open("val5_save.json", "w", encoding="utf-8"))
    print("wrote val5_save.json")
