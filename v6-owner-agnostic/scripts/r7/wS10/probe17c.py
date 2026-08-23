import json

graph = json.load(open("node_graph.json"))
node_data = json.load(open("node_data.json"))

upstream = {n: [] for n in graph}
for u, outs in graph.items():
    for n in outs:
        upstream.setdefault(n, []).append(u)

THRESH = 10.0

for basis in ["province_power","val"]:
    qualifying_pairs = []
    for N, data in node_data.items():
        for tag, cd in data["countries"].items():
            if basis in cd:
                val = float(cd[basis])
                if val >= THRESH:
                    for U in upstream.get(N, []):
                        qualifying_pairs.append((tag, N, U))
    no_power = [ (t,N,U) for (t,N,U) in qualifying_pairs if "val" not in node_data[U]["countries"].get(t,{}) ]
    print(basis, "total pairs:", len(qualifying_pairs), "no propagated val:", len(no_power))
