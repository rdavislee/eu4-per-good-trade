import json, collections
d = [(r[0], tuple(r[1])) for r in json.load(open("val62p3_europe_sweep.json"))]
print("grid points:", len(d), "from", d[0][0], "to", d[-1][0])
# runs
runs = []
for f, s in d:
    if runs and runs[-1][2] == s: runs[-1][1] = f
    else: runs.append([f, f, s])
print("distinct maximal runs:", len(runs))
EU = {"english_channel","north_sea","baltic_sea","white_sea","novgorod","lubeck","rheinland",
      "saxony","wien","krakow","pest","venice","ragusa","genua","champagne","bordeaux",
      "valencia","sevilla","constantinople","crimea","kiev","kazan"}
ASIA = {"hangzhou","canton","gulf_of_siam","malacca","beijing","xian","girin","nippon","hokkaido",
        "ganges_delta","burma","doab","lahore","comorin_cape","gujarat","lhasa","samarkand",
        "siberia","yumen","kazan"}  # rough; we use explicit membership below
for a,b,s in runs:
    eu = [x for x in s if x in EU]
    print("  x%.3f - x%.3f  n=%d  %-70s EU=%d %s" % (a,b,len(s), ",".join(s), len(eu), eu))
print()
# hangzhou episodes
def episodes(name):
    out=[]; 
    for a,b,s in runs:
        inn = name in s
        if out and out[-1][2]==inn: out[-1][1]=b
        else: out.append([a,b,inn])
    return [(a,b) for a,b,i in out if i]
for nm in ("hangzhou","gulf_of_siam","english_channel","genua","rheinland"):
    print(nm, "held over:", episodes(nm))
print()
# widest interval with 3 European ends and none in Asia
EUNODES = EU
best=None
for a,b,s in runs:
    eu=[x for x in s if x in EUNODES]
    if len(eu)==3 and len(s)==3:
        if best is None or (b-a)>(best[1]-best[0]): best=(a,b,s)
print("widest run with exactly 3 ends, all European:", best)
# merge adjacent runs that both satisfy "3 European ends, none in Asia"
def ok(s):
    eu=[x for x in s if x in EUNODES]
    return len(eu)==3 and len(s)==3
merged=[]
for f,s in d:
    if ok(s):
        if merged and abs(merged[-1][1]-(f-0.001))<1e-9: merged[-1][1]=f
        else: merged.append([f,f])
print("maximal grid stretches with 3 ends all European:", merged)
# sink count trajectory
cnt=[(a,b,len(s)) for a,b,s in runs]
print("count sequence:", [c for _,_,c in cnt])
print("last set:", d[-1])
# narrow intervals
uniq = collections.Counter(s for a,b,s in runs)
narrow=[(a,b,s) for a,b,s in runs if (b-a)<0.01 and uniq[s]==1]
print("runs narrower than x0.01 whose set appears exactly once:", len(narrow))
for a,b,s in narrow[:20]: print("   x%.3f-x%.3f %s"%(a,b,",".join(s)))
narrow3=[(a,b,s) for a,b,s in runs if (b-a)<0.03 and uniq[s]==1]
print("runs narrower than x0.03 whose set appears exactly once:", len(narrow3))
