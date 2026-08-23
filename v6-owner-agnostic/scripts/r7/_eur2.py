import os,sys,collections,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pdx
from solver import N, ORDER, NIDX
import measure6 as M
EU4=M.EU4
EUR=set(int(x) for x in pdx.values(pdx.load(os.path.join(EU4,"map","continent.txt")).get("europe")))
ND=json.load(open("nodes.json"))
NODES=ND["nodes"] if isinstance(ND,dict) and "nodes" in ND else ND
def members(n):
    v=NODES[n] if isinstance(NODES,dict) else None
    return v["members"]
EU_NODES={n for n in ORDER if any(p in EUR for p in members(n))}
print("European nodes:",len(EU_NODES), sorted(EU_NODES))
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
sinks=sorted(M.sk(r)); print("sinks",sinks)
cape=NIDX["cape_of_good_hope"]
pairs=[]; capepairs=0
for e in sorted(EU_NODES):
    i=NIDX[e]
    for s in sinks:
        j=NIDX[s]
        if j in R[i]:
            pairs.append((e,s))
            if cape in R[i] and j in R[cape]: capepairs+=1
print("connected Europe->sink pairs:",len(pairs),"; with a Cape-transiting path:",capepairs)
# routes
def sp(a,b):
    s,t=NIDX[a],NIDX[b]
    dist={s:None}; par={}; q=collections.deque([s])
    while q:
        x=q.popleft()
        for y in adj[x]:
            if y not in dist: dist[y]=x; par[y]=x; q.append(y)
    if t not in dist: return None
    path=[t]
    while path[-1]!=s: path.append(par[path[-1]])
    return [ORDER[i] for i in reversed(path)]
print("white_sea->hangzhou:",sp("white_sea","hangzhou"))
print("sevilla->ganges_delta:",sp("sevilla","ganges_delta"))
print("english_channel->genua:",sp("english_channel","genua"))
print("english_channel reaches hangzhou:",NIDX["hangzhou"] in R[NIDX["english_channel"]])
