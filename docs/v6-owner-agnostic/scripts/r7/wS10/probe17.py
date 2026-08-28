import json

graph = json.load(open("node_graph.json"))  # node -> list of outgoing (downstream) nodes
node_data = json.load(open("node_data.json"))

# upstream[N] = nodes U such that N in graph[U]  (U is immediately upstream of N)
upstream = {n: [] for n in graph}
for u, outs in graph.items():
    for n in outs:
        upstream.setdefault(n, []).append(u)

THRESH = 2.0

qualifying_pairs = []  # (country, N, U) candidate propagation pairs
for N, data in node_data.items():
    for tag, cd in data["countries"].items():
        if "val" in cd:
            val = float(cd["val"])
            if val >= THRESH:
                for U in upstream.get(N, []):
                    qualifying_pairs.append((tag, N, U))

print("total (country, upstream-node) candidate pairs:", len(qualifying_pairs))

no_power = []
for tag, N, U in qualifying_pairs:
    cd = node_data[U]["countries"].get(tag, {})
    has_val = "val" in cd
    if not has_val:
        no_power.append((tag, N, U))

print("pairs with NO val entry in upstream node:", len(no_power))

# England-specific check
eng_pairs = [(t,N,U) for (t,N,U) in qualifying_pairs if t=="ENG"]
print("England qualifying pairs:", len(eng_pairs))
for t,N,U in eng_pairs:
    cd = node_data[U]["countries"].get(t, {})
    print(f"  ENG in {N} (val={node_data[N]['countries']['ENG']['val']}) -> upstream {U}: val={cd.get('val','MISSING')}")
