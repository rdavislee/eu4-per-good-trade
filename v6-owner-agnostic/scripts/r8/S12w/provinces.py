"""Build the 1444.11.11 province dataset from history/provinces.

Applies the base block plus every dated block <= 1444.11.11, in date order.
"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
HERE = os.path.dirname(os.path.abspath(__file__))
START = (1444, 11, 11)

DATE_RE = re.compile(r"^(\d{1,4})\.(\d{1,2})\.(\d{1,2})$")


def build():
    hist = os.path.join(EU4, "history", "provinces")
    provs = {}
    for fn in os.listdir(hist):
        m = re.match(r"^\s*(\d+)", fn)
        if not m:
            continue
        pid = int(m.group(1))
        root = pdx.load(os.path.join(hist, fn))
        state = {}
        dated = []
        for k, v in root:
            if k is None:
                continue
            dm = DATE_RE.match(k)
            if dm:
                d = (int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
                if d <= START:
                    dated.append((d, v))
            else:
                state[k] = v
        # spec v6.0 M1b: `add_base_*` in a dated block ACCUMULATES onto the base value; it does
        # not replace it.  v5.0 and earlier wrote state["add_base_tax"] and left base_tax alone,
        # so a pre-start development grant was silently dropped (province 1, Uppland: base_tax 5
        # undated + 1 at 1436.4.28; the game has 6).
        ADD = {"add_base_tax": "base_tax",
               "add_base_production": "base_production",
               "add_base_manpower": "base_manpower"}
        for d, blk in sorted(dated, key=lambda x: x[0]):
            for k, v in blk:
                if k is None or DATE_RE.match(k or ""):
                    continue
                if k in ADD:
                    tgt = ADD[k]
                    try:
                        state[tgt] = float(state.get(tgt, 0) or 0) + float(v)
                    except (TypeError, ValueError):
                        pass
                    continue
                state[k] = v
        provs[pid] = state
    return provs


def num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


if __name__ == "__main__":
    provs = build()
    print("provinces parsed:", len(provs))
    owned = {p: s for p, s in provs.items() if s.get("owner") and s.get("owner") not in ("---",)}
    print("owned at 1444.11.11:", len(owned))
    cities = {p: s for p, s in owned.items() if s.get("is_city") == "yes"}
    print("is_city=yes and owned:", len(cities))
    goods = {}
    for p, s in owned.items():
        g = s.get("trade_goods")
        goods[g] = goods.get(g, 0) + 1
    print("distinct trade goods among owned provinces:", len(goods))
    for g, c in sorted(goods.items(), key=lambda x: -x[1]):
        print("   %-18s %4d" % (g, c))
    out = {}
    for p, s in provs.items():
        out[p] = {
            "owner": s.get("owner"),
            "controller": s.get("controller") or s.get("owner"),
            "trade_goods": s.get("trade_goods"),
            "base_tax": num(s.get("base_tax")),
            "base_production": num(s.get("base_production")),
            "base_manpower": num(s.get("base_manpower")),
            "is_city": s.get("is_city"),
        }
    json.dump(out, open(os.path.join(HERE, "prov1444.json"), "w"))
    print("wrote prov1444.json")
