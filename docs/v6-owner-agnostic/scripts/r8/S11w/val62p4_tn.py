# Y485/Y486/Y487/Y490/Y494: parse each tradenodes file (vanilla and the three probe mods)
# and count links, declaration-order violations, and directed cycles.
import os, re, collections
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
MODS = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\mod"
FILES = {
    "vanilla":          os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt"),
    "pgt_permute":      os.path.join(MODS, "pgt_permute", "common", "tradenodes", "00_tradenodes.txt"),
    "pgt_cycle":        os.path.join(MODS, "pgt_cycle", "common", "tradenodes", "00_tradenodes.txt"),
    "pgt_flip":         os.path.join(MODS, "pgt_flip", "common", "tradenodes", "00_tradenodes.txt"),
    "pgt_flip_ordered": os.path.join(MODS, "pgt_flip_ordered", "common", "tradenodes", "00_tradenodes.txt"),
}

def parse(path):
    """Return (declaration order, {node: [outgoing targets]})."""
    src = re.sub(r"#[^\n]*", "", open(path, encoding="latin-1").read())
    order, out = [], collections.OrderedDict()
    cur = None
    depth = 0
    pend = None
    for line in src.split("\n"):
        s = line.strip()
        m = re.match(r"^([a-z_][a-z_0-9]*)\s*=\s*\{", s)
        if m and depth == 0:
            cur = m.group(1); order.append(cur); out[cur] = []
        if depth == 1 and s.startswith("outgoing"):
            pend = True
        if pend and 'name="' in s:
            out[cur].append(re.search(r'name="([^"]+)"', s).group(1)); pend = None
        depth += s.count("{") - s.count("}")
    return order, out

def cycles(out):
    colour = collections.defaultdict(int); found = []
    def dfs(u, path):
        colour[u] = 1; path.append(u)
        for v in out.get(u, []):
            if colour[v] == 1:
                found.append(path[path.index(v):] + [v]); return True
            if colour[v] == 0 and dfs(v, path): return True
        path.pop(); colour[u] = 2; return False
    for n in out:
        if colour[n] == 0 and dfs(n, []): break
    return found

for tag, path in FILES.items():
    if not os.path.exists(path):
        print("%-18s MISSING %s" % (tag, path)); continue
    order, out = parse(path)
    pos = {n: i for i, n in enumerate(order)}
    links = sum(len(v) for v in out.values())
    viol = [(u, v) for u in out for v in out[u]
            if v in pos and pos[v] < pos[u]]
    cyc = cycles(out)
    print("%-18s nodes=%-4d links=%-4d order-violations=%-4d cycles=%s"
          % (tag, len(order), links, len(viol), (cyc[0] if cyc else "none")))
    if tag == "pgt_flip_ordered" or tag == "pgt_flip":
        print("      sevilla outgoing=%s ; valencia outgoing=%s"
              % (out.get("sevilla"), out.get("valencia")))
    if tag == "vanilla":
        print("      sevilla outgoing=%s ; valencia outgoing=%s"
              % (out.get("sevilla"), out.get("valencia")))
        print("      end=yes nodes: %s" % re.findall(r"(?m)^([a-z_]+)=\{(?=(?:[^{}]|\{[^{}]*\})*end=yes)",
                                                     open(path, encoding="latin-1").read())[:5])
