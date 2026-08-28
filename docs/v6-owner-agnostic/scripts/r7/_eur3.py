import os,sys,collections,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import N, ORDER, NIDX, ROWS
import measure6 as M
EU4=M.EU4
EUR=set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4,"map","continent.txt")).get("europe")))
NODES=json.load(open("nodes.json"))
NODES=NODES["nodes"] if isinstance(NODES,dict) and "nodes" in NODES else NODES
r=M.ph(); D=r["directed"]
adj=collections.defaultdict(list)
for u,v in D: adj[u].append(v)
def reach(x):
    seen={x};st=[x]
    while st:
        a=st.pop()
        for b in adj[a]:
            if b not in seen: seen.add(b); st.append(b)
    seen.discard(x);return seen
R={i:reach(i) for i in range(N)}
sinks=['genua','hangzhou']; cape=NIDX['cape_of_good_hope']
COUNTED={rr["pid"] for rr in ROWS}
def report(label,nodes):
    p=0;c=0
    for e in nodes:
        i=NIDX[e]
        for s in sinks:
            j=NIDX[s]
            if j in R[i]:
                p+=1
                if cape in R[i] and j in R[cape]: c+=1
    print("%-52s nodes=%2d pairs=%2d cape=%d"%(label,len(nodes),p,c))
A={n for n in ORDER if any(p in EUR for p in NODES[n]["members"])}
report("any member in continent europe",A)
B={n for n in ORDER if any(p in EUR and p in COUNTED for p in NODES[n]["members"])}
report("any COUNTED member in europe",B)
C={n for n in ORDER if sum(1 for p in NODES[n]["members"] if p in EUR)*2 > len(NODES[n]["members"])}
report("majority of members european",C)
named22=['english_channel','north_sea','baltic_sea','white_sea','novgorod','lubeck','rheinland','saxony','wien','krakow','pest','venice','ragusa','genua','champagne','bordeaux','valencia','sevilla','constantinople','crimea','kiev','kazan']
report("the doc's named 22",set(named22))
report("the doc's 18 western/central",set(named22[:18]))
EP=set(json.load(open("europe_provinces.json")))
E2={n for n in ORDER if any(p in EP for p in NODES[n]["members"])}
report("any member in europe_provinces.json",E2)
E3={n for n in ORDER if any(p in EP and p in COUNTED for p in NODES[n]["members"])}
report("any counted member in europe_provinces.json",E3)
# which nodes distinguish 25 vs 22
print("A minus named22:",sorted(A-set(named22)))
