import os,sys,collections,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX
import measure6 as M
r=M.ph(); D=set(r["directed"])
adj=collections.defaultdict(list)
for u,v in D: adj[u].append(v)
def has(a,b): return (NIDX[a],NIDX[b]) in D
north="white_sea novgorod kazan siberia samarkand lahore lhasa ganges_delta burma gulf_of_siam canton hangzhou".split()
print("northern route edges:")
for a,b in zip(north,north[1:]): print("  %-16s -> %-16s %s"%(a,b,has(a,b)))
ib="sevilla safi timbuktu katsina ethiopia gulf_of_aden comorin_cape ganges_delta".split()
print("iberian route edges:")
for a,b in zip(ib,ib[1:]): print("  %-16s -> %-16s %s"%(a,b,has(a,b)))
def bfs(a,b):
    s,t=NIDX[a],NIDX[b]; dist={s:0}; q=collections.deque([s])
    while q:
        x=q.popleft()
        for y in adj[x]:
            if y not in dist: dist[y]=dist[x]+1; q.append(y)
    return dist.get(t)
for a,b in [("white_sea","hangzhou"),("sevilla","hangzhou"),("english_channel","genua"),("malacca","english_channel")]:
    print("dist %s->%s = %s"%(a,b,bfs(a,b)))
# malacca to channel via cape vs via alexandria
print("malacca->english_channel via cape?  ")
