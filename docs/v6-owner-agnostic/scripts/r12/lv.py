# -*- coding: utf-8 -*-
"""r12 independent probe: node local_value reconstruction.
Grades Y1331 (57 of 79 digit-for-digit), Y1363 (cape_of_good_hope carries no field),
Y1364 (the identity + count), Y1332 (3.4% low)."""
import os, re, zipfile, collections, math
EU4 = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV"
SAVE = r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\VANILLA_start.eu4"

tgt = open(os.path.join(EU4,"common","tradegoods","00_tradegoods.txt"), encoding="latin-1").read()
GOODS = re.findall(r"^([a-z_]+) = \{", tgt, re.M)
raw = zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")

def matchbrace(txt, i):
    d=0; k=i; inq=False
    while k < len(txt):
        c=txt[k]
        if c=='"': inq = not inq
        elif not inq:
            if c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0: return k
        k+=1
    return len(txt)-1

# --- prices, in save order (slot order) ---
m0 = re.search(r"^change_price=\{", raw, re.M)
st = raw.index("{", m0.start()); pb = raw[st+1:matchbrace(raw, st)]
slot_order=[]; price={}
for mm in re.finditer(r"^\t([a-z_]+)=\{", pb, re.M):
    s2 = pb.index("{", mm.start()); blk = pb[s2+1:matchbrace(pb, s2)]
    cp = re.search(r"current_price=([\d.]+)", blk)
    slot_order.append(mm.group(1)); price[mm.group(1)] = float(cp.group(1)) if cp else None
print("goods in 00_tradegoods.txt : %d  -> %s ... %s" % (len(GOODS), GOODS[:3], GOODS[-2:]))
print("change_price slot order    : %d entries, slot0=%r slot1=%r last=%r" % (len(slot_order), slot_order[0], slot_order[1], slot_order[-1]))
print("slot order == ['nogoods']+GOODS ? %s" % (slot_order == ["nogoods"]+GOODS))

# --- node blocks ---
i2 = raw.index("\ntrade={"); j2 = raw.index("{", i2); tb = raw[j2+1:matchbrace(raw, j2)]
nodes=[]
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2 = tb.index("{", mm.start()); nd = tb[s2+1:matchbrace(tb, s2)]
    name = re.search(r'definitions="([a-z_]+)"', nd).group(1)
    blk = re.search(r"trade_goods_size=\{([^}]*)\}", nd, re.S)
    sz = [float(x) for x in blk.group(1).split()] if blk else []
    # local_value at node top level only (depth-1 keys of the node block)
    lv_all = re.findall(r"local_value=([-\d.eE+]+)", nd)
    lv_top = re.findall(r"^\t\tlocal_value=([-\d.eE+]+)", nd, re.M)
    nodes.append(dict(name=name, sz=sz, lv_top=lv_top, lv_all=lv_all, blk=nd))

print("\nnode blocks                : %d" % len(nodes))
print("nodes with a top-level local_value : %d" % sum(1 for n in nodes if n["lv_top"]))
print("nodes with NO local_value anywhere : %s" % [n["name"] for n in nodes if not n["lv_all"]])
print("nodes with NO top-level local_value: %s" % [n["name"] for n in nodes if not n["lv_top"]])
print("multi local_value at top level     : %s" % [(n["name"],len(n["lv_top"])) for n in nodes if len(n["lv_top"])>1])
print("trade_goods_size slot counts       : %s" % dict(collections.Counter(len(n["sz"]) for n in nodes)))

# --- reconstruction ---
def recon_annual(sz):
    return sum(sz[k]*price[slot_order[k]] for k in range(len(sz)) if sz[k])

rows=[]
for n in nodes:
    if not n["lv_top"]: continue
    ann = recon_annual(n["sz"])
    eng_s = n["lv_top"][0]
    eng = float(eng_s)
    rows.append((n["name"], ann, ann/12.0, eng, eng_s))

print("\n=== comparison over the %d nodes carrying the field ===" % len(rows))
dec = collections.Counter(len(s.split(".")[1]) if "." in s else 0 for _,_,_,_,s in rows)
print("decimals in the save's local_value strings: %s" % dict(dec))

def trunc(x, d):
    f = 10.0**d
    return math.floor(x*f + 1e-9)/f

for d in (2,3):
    cnt = sum(1 for _,_,r12,eng,s in rows if abs(trunc(r12,d)-trunc(eng,d)) < 0.5/10**d/2)
    print("  truncate both to %ddp, equal        : %d of %d" % (d, cnt, len(rows)))

# digit-for-digit: format recon to the same decimal count the save prints, truncated
cnt_dfd=0; misses=[]
for name, ann, r12, eng, s in rows:
    d = len(s.split(".")[1]) if "." in s else 0
    a = ("%%.%df" % d) % trunc(r12, d)
    b = s
    # normalise -0.000
    if float(a)==float(b): cnt_dfd+=1
    else: misses.append((name, a, b, r12, eng))
print("  DIGIT-FOR-DIGIT (recon truncated to the save's own decimals) : %d of %d" % (cnt_dfd, len(rows)))

print("\n  nodes NOT matching digit-for-digit (%d):" % len(misses))
for name,a,b,r12,eng in sorted(misses, key=lambda t:-(t[4]-t[3])):
    print("    %-24s recon/12=%-12s engine=%-12s  raw recon/12=%.6f" % (name,a,b,r12))

# alternative counts for sensitivity
print("\n=== sensitivity: what count does each rule give? ===")
for tol in (0.0, 1e-9, 1e-6, 1e-4, 1e-3, 5e-3, 1e-2):
    print("  |recon/12 - engine| <= %-8g -> %d of %d" % (tol, sum(1 for _,_,r,e,_ in rows if abs(r-e)<=tol), len(rows)))
r_exact = sum(1 for _,ann,r,e,_ in rows if e>0 and round(ann/e,2)==12.00)
print("  round(annual/engine,2)==12.00        -> %d of %d" % (r_exact, len(rows)))
print("  round(recon/12,2)==round(engine,2)   -> %d of %d" % (sum(1 for _,_,r,e,_ in rows if round(r,2)==round(e,2)), len(rows)))

tot_r = sum(r for _,_,r,_,_ in rows); tot_e = sum(e for _,_,_,e,_ in rows)
print("\naggregate recon/12 = %.4f   engine sum = %.4f   shortfall = %.3f%%" % (tot_r, tot_e, 100.0*(tot_r-tot_e)/tot_e))
# also aggregate over all 80 including cape
print("cape_of_good_hope block: has trade_goods_size sum = %s" % [sum(n['sz']) for n in nodes if n['name']=='cape_of_good_hope'])
