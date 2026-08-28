import zipfile, re, json, os, collections
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"val62p2_b_prop3.py")).read().split("DIV,RAWTHR")[0])
DIV,RAWTHR=5.0,10.0
# who receives in african_great_lakes?
for nd in ("african_great_lakes","chesapeake_bay"):
    print("###",nd)
    for c,d in sorted(info.get(nd,{}).items()):
        if d.get("max_pow",0.0)>0:
            pure = not (d.get("province_power") or d["trader"] or d["light_ship"])
            print("   ",c,"max_pow",d.get("max_pow"),"pp",d.get("province_power"),"pure_receiver" if pure else "")
# clean threshold bracket: only nodes with >=1 pure receiver; country pure (no pp/trader/ship) upstream
prop=[];noprop=[]
live={n for n in ND["order"] if any((not (e.get("province_power") or e["trader"] or e["light_ship"])) and e.get("max_pow",0)>0 for e in info.get(n,{}).values())}
for n in live:
    cands=set()
    for m2 in OUT.get(n,[]):
        for c in info.get(m2,{}): cands.add(c)
    for c in cands:
        e=info.get(n,{}).get(c)
        if e is None: continue
        if e.get("province_power") or e["trader"] or e["light_ship"]: continue
        tot=sum(info.get(m2,{}).get(c,{}).get("province_power",0.0) for m2 in OUT.get(n,[]))
        if tot<=0: continue
        (prop if e.get("max_pow",0.0)>0 else noprop).append((tot,n,c))
prop.sort(); noprop.sort()
print("PURE receivers: propagating min:",prop[:3])
print("PURE receivers: NON-propagating max:",noprop[-5:])
print("counts prop/noprop:",len(prop),len(noprop))
# ship power: entries with ship_power
ships=[]
for n in ND["order"]:
    for c,d in info.get(n,{}).items():
        if d.get("ship_power",0.0)>0: ships.append((n,c,d["ship_power"]))
print("entries with ship_power:",len(ships), ships[:8])
