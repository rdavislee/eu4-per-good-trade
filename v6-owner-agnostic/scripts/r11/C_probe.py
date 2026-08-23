# -*- coding: utf-8 -*-
"""Round-11 slice C: independent re-derivation of the save-structure facts §1.8's
inject_g(n) block rests on. Reproduces nothing from measure6.py/solver.py by import --
parses the save and the shipped files fresh, from scratch.
"""
import os, re, zipfile, collections, json, sys

EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SAVE = os.path.join(os.path.expanduser("~"), "OneDrive", "Documents", "Paradox Interactive",
                     "Europa Universalis IV", "save games", "VANILLA_start.eu4")
HERE = os.path.dirname(os.path.abspath(__file__))
R10 = os.path.join(os.path.dirname(HERE), "r10")

def matchbrace(s, i):
    """s[i] must be '{'. Return index of the matching '}'."""
    assert s[i] == "{"
    d = 0; k = i; inq = False
    while k < len(s):
        c = s[k]
        if c == '"':
            inq = not inq
        elif not inq:
            if c == "{":
                d += 1
            elif c == "}":
                d -= 1
                if d == 0:
                    return k
        k += 1
    raise RuntimeError("unbalanced braces")

# ------------------------------------------------------------ 1. tradegoods order
tg_text = open(os.path.join(EU4, "common", "tradegoods", "00_tradegoods.txt"),
                encoding="latin-1").read()
ORDERG = re.findall(r"(?m)^([a-z_]+)\s*=\s*\{", tg_text)
print("=== tradegoods file ===")
print("goods found in 00_tradegoods.txt (in file order):", len(ORDERG))
print(ORDERG)

# ------------------------------------------------------------ 2. save: trade block
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
i0 = raw.index("\ntrade={")
j0 = raw.index("{", i0)
trade_body = raw[j0 + 1: matchbrace(raw, j0)]

nodes = []
for m in re.finditer(r"(?m)^\tnode=\{", trade_body):
    s = trade_body.index("{", m.start())
    e = matchbrace(trade_body, s)
    blk = trade_body[s + 1:e]
    name_m = re.search(r'definitions="([^"]+)"', blk)
    lv_m = re.search(r"(?m)^\t\tlocal_value=([\-\d.]+)", blk)
    tgs_m = re.search(r"trade_goods_size=\{([^}]*)\}", blk, re.S)
    sizes = [float(x) for x in tgs_m.group(1).split()] if tgs_m else None
    nodes.append(dict(name=name_m.group(1) if name_m else None,
                       local_value=float(lv_m.group(1)) if lv_m else None,
                       sizes=sizes))

print()
print("=== node blocks ===")
print("node= blocks found under trade={}:", len(nodes))
lens = collections.Counter(len(n["sizes"]) if n["sizes"] is not None else -1 for n in nodes)
print("distribution of trade_goods_size slot counts:", dict(lens))
missing = [n["name"] for n in nodes if n["sizes"] is None]
print("nodes with NO trade_goods_size array:", missing)

# ------------------------------------------------------------ Y1280: slot count / map
print()
print("=== Y1280: slot map ===")
SLOTS = lens.most_common(1)[0][0] if lens else None
print("modal slot count:", SLOTS, "  all-80-agree:", len(lens) == 1)

# ------------------------------------------------------------ Y1282: all-zero slots
print()
print("=== Y1282: all-zero slots ===")
if SLOTS:
    allzero = []
    for k in range(SLOTS):
        vals = [n["sizes"][k] for n in nodes if n["sizes"] is not None]
        if all(v == 0.0 for v in vals):
            allzero.append(k)
    print("slot indices (0-indexed, matching raw array position) that are all-zero across all 80 nodes:", allzero)
    nonzero_any = [k for k in range(SLOTS) if k not in allzero]
    print("slots that are nonzero somewhere:", nonzero_any, " count:", len(nonzero_any))

# ------------------------------------------------------------ Y1310: province-level produced-quantity fields
print()
print("=== Y1310: province-level produced-quantity fields ===")
i1 = raw.index("\nprovinces={")
j1 = raw.index("{", i1)
prov_body = raw[j1 + 1: matchbrace(raw, j1)]
# scan ALL top-level province records for candidate produced-quantity field names
CANDIDATE_FIELDS = ["goods_produced", "trade_goods_size", "production", "produced",
                     "trade_value", "base_production", "trade_goods"]
first_hits = collections.Counter()
all_field_names = collections.Counter()
checked = 0
owned_checked = 0
for m in re.finditer(r"(?m)^-(\d+)=\{", prov_body):
    s = prov_body.index("{", m.start())
    e = matchbrace(prov_body, s)
    rec = prov_body[s + 1:e]
    checked += 1
    # top-level field names only (two-tab indent), first occurrence per name
    names = re.findall(r"(?m)^\t\t([a-zA-Z_0-9]+)\s*=", rec)
    for nm in set(names):
        all_field_names[nm] += 1
    if 'owner="' not in rec:
        continue
    owned_checked += 1
    for f in CANDIDATE_FIELDS:
        if re.search(r"(?m)^\t\t" + f + r"\s*=", rec):
            first_hits[f] += 1
print("total province records scanned:", checked)
print("owned province records among them:", owned_checked)
print("candidate produced-quantity field hit counts among OWNED provinces:", dict(first_hits))
print("ALL distinct top-level province field names seen, with province-record counts (top 60 by frequency):")
for nm, c in all_field_names.most_common(60):
    print("  %-30s %d" % (nm, c))

# ------------------------------------------------------------ Y1281: Jaccard slot-map vs membership
print()
print("=== Y1281: Jaccard(slot-map good-set, province-membership good-set) ===")
# tradenodes membership
tn_text = open(os.path.join(EU4, "common", "tradenodes", "00_tradenodes.txt"),
                encoding="latin-1").read()
NODE_MEMBERS = {}
for m in re.finditer(r"(?m)^([a-z_0-9]+)\s*=\s*\{", tn_text):
    nm = m.group(1)
    s = tn_text.index("{", m.end() - 1)
    e = matchbrace(tn_text, s)
    blk = tn_text[s + 1:e]
    mm = re.search(r"members\s*=\s*\{([^}]*)\}", blk, re.S)
    NODE_MEMBERS[nm] = [int(x) for x in mm.group(1).split()] if mm else []

# province trade goods: prefer save (post-roll) so unknown-good provinces resolve to real goods,
# same source the model itself uses for the twenty rolled ones. Track ownership too: the model
# (solver.province_table) only counts a province -- hence only lets it "produce" -- when it has an
# owner, and empirically (below) unowned provinces never carry nonzero trade_goods_size either.
PROV_GOOD = {}
PROV_OWNED = set()
for m in re.finditer(r"(?m)^-(\d+)=\{", prov_body):
    s = prov_body.index("{", m.start())
    e = matchbrace(prov_body, s)
    rec = prov_body[s + 1:e]
    g = re.search(r"(?m)^\t\ttrade_goods=\"?([a-z_]+)", rec)
    if g:
        PROV_GOOD[int(m.group(1))] = g.group(1)
    if re.search(r'(?m)^\t\towner="', rec):
        PROV_OWNED.add(int(m.group(1)))

unk = collections.Counter()
for pid, g in PROV_GOOD.items():
    if g == "unknown":
        unk["unknown_owned" if pid in PROV_OWNED else "unknown_unowned"] += 1
print("provinces with live trade_goods=unknown at save time:", dict(unk),
      "(cross-check: expect 0 owned -- engine has already rolled every owned province by save time)")

def slot_goods(node):
    if node["sizes"] is None:
        return set()
    out = set()
    for k in range(1, min(len(node["sizes"]), len(ORDERG) + 1)):
        if node["sizes"][k] != 0.0:
            out.add(ORDERG[k - 1])
    return out

def member_goods(nodename, owned_only=False, drop_unknown=True):
    mem = NODE_MEMBERS.get(nodename, [])
    out = set()
    for p in mem:
        if p not in PROV_GOOD:
            continue
        if owned_only and p not in PROV_OWNED:
            continue
        g = PROV_GOOD[p]
        if drop_unknown and g == "unknown":
            continue
        out.add(g)
    return out

def jacc_report(label, owned_only):
    inter_tot = union_tot = 0
    per_node = []
    for n in nodes:
        A = slot_goods(n)
        B = member_goods(n["name"], owned_only=owned_only)
        u = len(A | B); it = len(A & B)
        inter_tot += it; union_tot += u
        j = (it / u) if u else 1.0
        per_node.append((n["name"], j, sorted(A - B), sorted(B - A)))
    agg = inter_tot / union_tot if union_tot else 1.0
    mean = sum(j for _, j, _, _ in per_node) / len(per_node)
    print("--", label, "--")
    print("  aggregate (pooled) Jaccard:", round(agg, 6), " mean-of-per-node Jaccard:", round(mean, 6))
    mism = [t for t in per_node if t[1] < 1.0]
    print("  nodes with imperfect Jaccard:", len(mism))
    for t in mism[:25]:
        print("   ", t)
    return per_node

print("Test A -- ALL member provinces (owned + unowned/native), 'unknown' dropped from both sides:")
jacc_report("all members", owned_only=False)
print()
print("Test B -- OWNED member provinces only (matches solver.province_table's own filter):")
jacc_report("owned members only", owned_only=True)

# Per-slot (node-set) Jaccard, transposed: for each slot k, does the SET OF NODES with nonzero
# slot k equal the SET OF NODES holding >=1 owned province of the mapped good. This is the
# granularity A_slotmap.py (r10, read for context only, reproduced independently here) used.
print()
print("Test C -- per-slot node-set Jaccard (owned provinces only), the transposed formulation:")
gnodes = collections.defaultdict(set)
for pid, g in PROV_GOOD.items():
    if pid in PROV_OWNED and g != "unknown":
        nm = None
        for nn, mem in NODE_MEMBERS.items():
            if pid in mem:
                nm = nn; break
        if nm:
            gnodes[g].add(nm)
slot_nodesets = {k: set(n["name"] for n in nodes if n["sizes"] is not None and n["sizes"][k] > 0)
                 for k in range(SLOTS)}
allperfect = True
for k in range(SLOTS):
    if k in (0, 30, 32):
        continue
    g = ORDERG[k - 1]
    a = slot_nodesets[k]; b = gnodes.get(g, set())
    u = len(a | b); it = len(a & b)
    j = it / u if u else 1.0
    if j < 1.0:
        allperfect = False
    print("  slot %2d -> %-16s jaccard %.4f  (slot-nodes=%d good-nodes=%d)" % (k, g, j, len(a), len(b)))
print("  ALL 30 real-good slots at Jaccard 1.000:", allperfect)

# ------------------------------------------------------------ Y1277: inject vs local_value, x12
print()
print("=== Y1277: Sum_g size(n,g)*price(g) vs local_value, and x12 vs monthly field ===")
i2 = raw.index("\nchange_price={")
j2 = raw.index("{", i2)
cp_body = raw[j2 + 1: matchbrace(raw, j2)]
PRICE = {}
for m in re.finditer(r"(?m)^\t([a-z_]+)=\{", cp_body):
    s = cp_body.index("{", m.start())
    e = matchbrace(cp_body, s)
    blk = cp_body[s + 1:e]
    cp = re.search(r"current_price=([\d.]+)", blk)
    if cp:
        PRICE[m.group(1)] = float(cp.group(1))
print("goods with a current_price entry:", len(PRICE), "sample:", dict(list(PRICE.items())[:5]))

NEWWORLD = {"patagonia", "amazonas_node", "rio_grande", "james_bay", "california",
            "mississippi_river", "ohio", "mexico", "cuiaba", "lima", "laplata", "brazil",
            "panama", "carribean_trade", "chesapeake_bay", "st_lawrence"}

rows = []
for n in nodes:
    if n["sizes"] is None:
        continue
    lv = n["local_value"] if n["local_value"] is not None else 0.0  # cape_of_good_hope: no
    # local_value field at all in the save (node carries no current= either) -- an inactive
    # node with an all-zero trade_goods_size array too, so 0 is the correct comparator, not a drop.
    n = dict(n); n["local_value"] = lv
    annual = 0.0
    for k in range(1, min(len(n["sizes"]), len(ORDERG) + 1)):
        g = ORDERG[k - 1]
        annual += n["sizes"][k] * PRICE.get(g, 0.0)
    monthly = annual / 12.0
    ratio = (annual / n["local_value"]) if n["local_value"] else float("nan")
    rows.append(dict(name=n["name"], annual=annual, monthly=monthly,
                      local_value=n["local_value"], ratio=ratio,
                      exact=abs(monthly - n["local_value"]) < 5e-4,
                      newworld=n["name"] in NEWWORLD))

exact_12 = sum(1 for r in rows if round(r["ratio"], 2) == 12.00)
exact_match = sum(1 for r in rows if r["exact"])
print("nodes with a usable (sizes, local_value) pair:", len(rows))
print("nodes where annual/local_value rounds to exactly 12.00:", exact_12)
print("nodes where monthly (annual/12) matches local_value within 5e-4:", exact_match)

tot_annual = sum(r["annual"] for r in rows)
tot_lv12 = sum(r["local_value"] * 12.0 for r in rows)
shortfall = (tot_lv12 - tot_annual) / tot_lv12 * 100.0 if tot_lv12 else float("nan")
print("aggregate annual sum(size*price):", round(tot_annual, 2))
print("aggregate local_value*12 sum:", round(tot_lv12, 2))
print("aggregate shortfall (lv*12 - annual)/ (lv*12), %%:", round(shortfall, 2))

nonexact = [r for r in rows if not r["exact"]]
nonexact_sorted = sorted(nonexact, key=lambda r: (r["local_value"] * 12 - r["annual"]), reverse=True)
print("non-exact nodes:", len(nonexact), " of which New World:", sum(1 for r in nonexact if r["newworld"]))
print("worst offenders (largest local_value*12 - annual, absolute ducats):")
for r in nonexact_sorted[:15]:
    print("   %-20s annual=%10.3f  local_value*12=%10.3f  diff=%9.3f  ratio=%6.3f  NW=%s" %
          (r["name"], r["annual"], r["local_value"] * 12, r["local_value"] * 12 - r["annual"],
           r["ratio"], r["newworld"]))
print("total New World nodes present:", sum(1 for r in rows if r["newworld"]),
      "of", len(NEWWORLD), "listed")

missing = [n["name"] for n in nodes if n["sizes"] is None or n["local_value"] is None]
print("nodes dropped from this comparison (missing sizes/local_value):", missing)

# reconciliation under save-precision rounding (local_value stored to 3dp; try 3dp-round match)
exact_3dp = sum(1 for r in rows if round(r["monthly"], 3) == round(r["local_value"], 3))
print("nodes where round(monthly,3) == round(local_value,3):", exact_3dp)
diffs = sorted(abs(r["monthly"] - r["local_value"]) for r in rows)
print("abs(monthly-local_value) sorted, first 20:", [round(d, 4) for d in diffs[:20]])
print("abs(monthly-local_value) sorted, count <=0.001:", sum(1 for d in diffs if d <= 0.001),
      " <=0.005:", sum(1 for d in diffs if d <= 0.005),
      " <=0.01:", sum(1 for d in diffs if d <= 0.01),
      " <=0.05:", sum(1 for d in diffs if d <= 0.05))

print()
print("DONE")
