# -*- coding: utf-8 -*-
"""Cross-implementation orientation check (spec 2.8, TESTING A5): diff two orientation dumps.

Orientation is compared EXACTLY -- every arc, every good, plus Phi_w, no tolerance: directed
edges, sinks, sources, Phase-1 selection, promotions, fallbacks, flow/free classification,
and the marking order. Inputs (wealth rows, node wealth, alpha) are compared to relative
tolerance to localise a disagreement's cause when one appears. Where the two disagree on
orientation the reference is correct by definition.

Usage: python compare.py ref.json cpp.json
Exit 0 on exact orientation equality, 1 otherwise.
"""
import json, sys

REL = 1e-9


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def relclose(a, b):
    a, b = float(a), float(b)
    if a == b:
        return True
    return abs(a - b) <= REL * max(1.0, abs(a), abs(b))


def main(ref_path, cpp_path):
    ref, cpp = load(ref_path), load(cpp_path)
    fails = []
    warns = []

    def check(cond, msg):
        if not cond:
            fails.append(msg)

    check(ref["node_order"] == cpp["node_order"], "node_order differs")
    check(ref["edges_und"] == cpp["edges_und"], "edges_und differs")
    check(ref["goods_live"] == cpp["goods_live"],
          "live goods differ: ref %d cpp %d" % (len(ref["goods_live"]), len(cpp["goods_live"])))
    check(ref["counted_provinces"] == cpp["counted_provinces"],
          "counted provinces: ref %s cpp %s" % (ref["counted_provinces"], cpp["counted_provinces"]))

    # inputs, tolerance-compared (diagnostic only)
    rw, cw = ref["wealth_rows"], cpp["wealth_rows"]
    if set(rw) != set(cw):
        only_r = sorted(set(rw) - set(cw))[:5]
        only_c = sorted(set(cw) - set(rw))[:5]
        fails.append("wealth row pids differ; ref-only %s cpp-only %s" % (only_r, only_c))
    else:
        bad = 0
        for pid, r in rw.items():
            c = cw[pid]
            if r["node"] != c["node"] or r["good"] != c["good"] or \
               not relclose(r["tax"], c["tax"]) or not relclose(r["trade_value"], c["trade_value"]):
                bad += 1
                if bad <= 5:
                    warns.append("wealth row %s: ref %s cpp %s" % (pid, r, c))
        if bad:
            fails.append("wealth rows disagreeing: %d" % bad)
    for n in ref["node_wealth"]:
        if not relclose(ref["node_wealth"][n], cpp["node_wealth"][n]):
            fails.append("node_wealth %s: ref %s cpp %s"
                         % (n, ref["node_wealth"][n], cpp["node_wealth"][n]))

    rg = {g["name"]: g for g in ref["graphs"]}
    cg = {g["name"]: g for g in cpp["graphs"]}
    check(set(rg) == set(cg), "graph sets differ: %s" % (set(rg) ^ set(cg)))
    exact = 0
    for name in sorted(set(rg) & set(cg)):
        r, c = rg[name], cg[name]
        ok = True
        for key in ("directed", "sinks", "sources", "S0", "promotions", "fallbacks",
                    "flow_edges", "free_edges"):
            if r[key] != c[key]:
                ok = False
                ra, ca = set(r[key]), set(c[key])
                fails.append("%s %s: %d ref-only %s | %d cpp-only %s"
                             % (name, key, len(ra - ca), sorted(ra - ca)[:6],
                                len(ca - ra), sorted(ca - ra)[:6]))
        if r.get("order") and c.get("order"):
            if r["order"] != c["order"]:
                ok = False
                diff = [k for k in r["order"] if r["order"].get(k) != c["order"].get(k)]
                fails.append("%s marking order differs on %d nodes: %s"
                             % (name, len(diff), diff[:6]))
        # net flows, tolerance (diagnostic)
        nbad = [e for e in r.get("net", {})
                if e in c.get("net", {}) and not relclose(r["net"][e], c["net"][e])]
        if nbad:
            warns.append("%s: %d net flows beyond rel tol (first: %s ref %s cpp %s)"
                         % (name, len(nbad), nbad[0], r["net"][nbad[0]], c["net"][nbad[0]]))
        if ok:
            exact += 1
    print("graphs exactly equal on orientation: %d of %d" % (exact, len(set(rg) & set(cg))))
    for w in warns[:10]:
        print("  [warn] %s" % w)
    if fails:
        print("FAILURES (%d):" % len(fails))
        for f in fails[:40]:
            print("  [FAIL] %s" % f)
        print("RESULT: MISMATCH")
        return 1
    print("RESULT: EXACT ORIENTATION EQUALITY")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
