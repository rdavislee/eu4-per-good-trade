import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
TN = os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt")

root = pdx.load(TN)

nodes = {}
order = []
for k, v in root:
    if k is None or not isinstance(v, pdx.Node):
        continue
    name = k
    order.append(name)
    members = []
    mem = v.get("members")
    if mem is not None:
        members = [int(x) for x in pdx.values(mem)]
    outgoing = []
    for og in v.getall("outgoing"):
        outgoing.append(og.get("name"))
    nodes[name] = {
        "location": v.get("location"),
        "inland": v.get("inland"),
        "end": v.get("end"),
        "ai_will_propagate_through_trade": v.get("ai_will_propagate_through_trade"),
        "members": members,
        "outgoing": outgoing,
        "keys": sorted(set(v.keys())),
        "n_outgoing_blocks": len(v.getall("outgoing")),
    }

print("N nodes:", len(nodes))
print("declaration order length:", len(order))
print()
inland = [n for n in order if nodes[n]["inland"] == "yes"]
print("inland=yes count:", len(inland))
print("inland nodes:", inland)
print()
ends = [n for n in order if nodes[n]["end"] == "yes"]
print("end=yes count:", len(ends))
print("end nodes:", ends)
print()
# nodes with no outgoing
noout = [n for n in order if not nodes[n]["outgoing"]]
print("nodes with zero outgoing blocks:", len(noout), noout)
print()
# edges
edges = []
for n in order:
    for m in nodes[n]["outgoing"]:
        edges.append((n, m))
print("directed edges:", len(edges))
und = set()
for a, b in edges:
    und.add(tuple(sorted((a, b))))
print("distinct undirected pairs:", len(und))
# check for bidirectional pairs (both n->m and m->n present)
es = set(edges)
bidir = [(a, b) for (a, b) in es if (b, a) in es]
print("bidirectional pairs (both directions declared):", len(bidir), bidir[:10])
print()
# member counts
mc = sorted(((len(nodes[n]["members"]), n) for n in order), reverse=True)
print("largest member counts:", mc[:8])
print("smallest member counts:", mc[-8:])
print()
for target in ("nippon", "champagne", "english_channel", "genua", "venice"):
    if target in nodes:
        print(target, "members:", len(nodes[target]["members"]))
print()
allkeys = set()
for n in order:
    allkeys |= set(nodes[n]["keys"])
print("all keys seen at node level:", sorted(allkeys))
print()
print("ai_will_propagate_through_trade present on:",
      sum(1 for n in order if nodes[n]["ai_will_propagate_through_trade"] is not None))

json.dump({"order": order, "nodes": nodes}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes.json"), "w"), indent=0)
