import zipfile, re, json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                    "Europa Universalis IV", "save games", "VANILLA_start.eu4")

def mb(s, i):
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"':
            inq = not inq
        elif not inq:
            if c == '{':
                d += 1
            elif c == '}':
                d -= 1
                if d == 0:
                    return k
        k += 1
    return len(s) - 1

raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
i = raw.index('\ntrade={'); j = raw.index('{', i)
trade = raw[j+1:mb(raw, j)]

node_order = []   # save-file order == node index (0-based), to be confirmed
node_blk = {}
for m in re.finditer(r'\tnode=\{', trade):
    st = trade.index('{', m.start())
    blk = trade[st+1:mb(trade, st)]
    name = re.search(r'definitions="([^"]+)"', blk).group(1)
    node_order.append(name)
    node_blk[name] = blk

ND = json.load(open(os.path.join(HERE, "nodes.json")))
OUT = {n: ND["nodes"][n]["outgoing"] for n in ND["order"]}

print("save node_order[:10]:", node_order[:10])
print("nodes.json order[:10]:", ND["order"][:10])
print("orders equal:", node_order == ND["order"])

idx = {n: k for k, n in enumerate(node_order)}

def get_steer_powers(blk):
    return [float(x) for x in re.findall(r'^\t\tsteer_power=([\d.\-]+)', blk, re.M)]

def get_incoming(blk):
    out = []
    for m in re.finditer(r'\t\tincoming=\{', blk):
        st = blk.index('{', m.start())
        body = blk[st+1:mb(blk, st)]
        d = {}
        for k in ("add", "value", "from"):
            g = re.search(r'%s=([\d.\-]+)' % k, body)
            if g: d[k] = float(g.group(1))
        out.append(d)
    return out

results = []
for n in node_order:
    outs = OUT.get(n, [])
    if len(outs) < 2:
        continue
    sp = get_steer_powers(node_blk[n])
    if len(sp) != len(outs):
        continue  # mismatch, skip
    # get actual received value at each downstream target, sourced from n
    recv = []
    for m in outs:
        entries = get_incoming(node_blk.get(m, ""))
        v = 0.0
        for e in entries:
            if int(e.get("from", -1)) == idx[n]:
                v += e.get("value", 0.0)
        recv.append(v)
    results.append((n, outs, sp, recv))

print()
print("total multi-outgoing nodes with matching steer_power count:", len(results))
print()
for n, outs, sp, recv in results:
    tot_recv = sum(recv)
    if tot_recv < 0.01:
        continue
    print(f"{n}: outs={outs}")
    print(f"   steer_power={sp}")
    print(f"   received  ={[round(v,4) for v in recv]}  (sum={round(tot_recv,4)})")
    # normalized comparisons
    sp_sum = sum(sp)
    sp_norm = [round(x/sp_sum,3) if sp_sum>0 else None for x in sp]
    recv_norm = [round(x/tot_recv,3) if tot_recv>0 else None for x in recv]
    print(f"   steer_power normalized={sp_norm}")
    print(f"   received   normalized={recv_norm}")
    print()
