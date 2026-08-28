import json

graph = json.load(open("node_graph.json"))
node_data = json.load(open("node_data.json"))

upstream = {n: [] for n in graph}
for u, outs in graph.items():
    for n in outs:
        upstream.setdefault(n, []).append(u)

THRESH = 10.0  # TRADE_PROPAGATE_THRESHOLD(2) * TRADE_PROPAGATE_DIVIDER(5)

qualifying_pairs = []
for N, data in node_data.items():
    for tag, cd in data["countries"].items():
        if "val" in cd:
            val = float(cd["val"])
            if val >= THRESH:
                for U in upstream.get(N, []):
                    qualifying_pairs.append((tag, N, U))

print("THRESH=10 total candidate pairs:", len(qualifying_pairs))

no_power = []
for tag, N, U in qualifying_pairs:
    cd = node_data[U]["countries"].get(tag, {})
    if "val" not in cd:
        no_power.append((tag,N,U))
print("no val in upstream:", len(no_power))

eng = [(t,N,U) for (t,N,U) in qualifying_pairs if t=="ENG" and N=="english_channel"]
for t,N,U in eng:
    cd = node_data[U]["countries"].get(t,{})
    print("ENG", N, "->", U, "val=", cd.get("val","MISSING"))
