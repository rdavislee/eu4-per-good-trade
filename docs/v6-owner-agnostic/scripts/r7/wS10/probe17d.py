import json

graph = json.load(open("node_graph.json"))
node_data = json.load(open("node_data.json"))

upstream = {n: [] for n in graph}
for u, outs in graph.items():
    for n in outs:
        upstream.setdefault(n, []).append(u)

for basis, thresh in [("province_power",10.0), ("province_power",2.0), ("val",10.0), ("val",2.0)]:
    pairs_dn = set()   # (tag, N, U) triples
    for N, data in node_data.items():
        for tag, cd in data["countries"].items():
            if basis in cd:
                v = float(cd[basis])
                if v >= thresh:
                    for U in upstream.get(N, []):
                        pairs_dn.add((tag,N,U))
    # dedup to (tag,U)
    pairs_tu = set((t,U) for (t,N,U) in pairs_dn)
    no_power_tu = [(t,U) for (t,U) in pairs_tu if "val" not in node_data[U]["countries"].get(t,{})]
    print(f"basis={basis} thresh={thresh}: triples={len(pairs_dn)} dedup(tag,U) pairs={len(pairs_tu)} no_val={len(no_power_tu)}")
