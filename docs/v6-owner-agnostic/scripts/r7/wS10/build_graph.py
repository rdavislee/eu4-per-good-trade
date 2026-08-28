import re, os

EU4 = r"C:/Program Files (x86)/Steam/steamapps/common/Europa Universalis IV"
path = EU4 + "/common/tradenodes/00_tradenodes.txt"
txt = open(path, encoding="latin-1").read()

def match_brace(s, i):
    d = 0; k = i; inq=False
    while k < len(s):
        c = s[k]
        if c=='"': inq = not inq
        elif not inq:
            if c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0: return k
        k+=1
    return len(s)

# top-level node blocks: name={ ... }
nodes = {}
i = 0
pat = re.compile(r'^([a-z_0-9]+)=\{', re.M)
for m in pat.finditer(txt):
    name = m.group(1)
    bopen = txt.index("{", m.start())
    bclose = match_brace(txt, bopen)
    block = txt[bopen+1:bclose]
    outs = re.findall(r'outgoing=\{\s*name="([a-z_0-9]+)"', block)
    nodes[name] = outs

print("num nodes:", len(nodes))
total_edges = sum(len(v) for v in nodes.values())
print("total outgoing edges:", total_edges)

import json
json.dump(nodes, open("node_graph.json","w"))
# print a couple
print("sevilla outgoing:", nodes.get("sevilla"))
print("safi outgoing:", nodes.get("safi"))
print("tunis outgoing:", nodes.get("tunis"))
print("english_channel outgoing:", nodes.get("english_channel"))
print("chesapeake_bay outgoing:", nodes.get("chesapeake_bay"))
