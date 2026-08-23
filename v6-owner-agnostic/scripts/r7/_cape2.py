import os,sys,collections,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from solver import N, ORDER, NIDX
import measure6 as M
r = M.ph()
D = r["directed"]           # set/list of (u,v)?
print('sample',list(D)[:3], 'len', len(D))
adj=collections.defaultdict(list)
for u,v in D: adj[u].append(v)
def reach(s):
    seen={s}; st=[s]
    while st:
        x=st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    seen.discard(s); return seen
R={i:reach(i) for i in range(N)}
cape=NIDX['cape_of_good_hope']
# def A: a reaches cape, cape reaches b, a reaches b
A=sum(1 for a in range(N) for b in range(N) if a!=b and cape in R[a] and b in R[cape] and b in R[a])
# BFS shortest path lengths
def bfs(s):
    dist={s:0}; q=collections.deque([s])
    while q:
        x=q.popleft()
        for y in adj[x]:
            if y not in dist: dist[y]=dist[x]+1; q.append(y)
    return dist
DIST={i:bfs(i) for i in range(N)}
# count shortest paths and how many pass through cape
def count_sp(s):
    # number of shortest paths from s to each node, and number passing through cape
    dist=DIST[s]
    order=sorted(dist,key=lambda k:dist[k])
    npath={s:1}; thru={s:0}
    for x in order:
        if x==s: continue
        npath[x]=0; thru[x]=0
        for u in range(N):
            if u in dist and dist.get(u,10**9)==dist[x]-1 and x in adj[u]:
                npath[x]+=npath.get(u,0)
                t=thru.get(u,0)
                if u==cape: t=npath.get(u,0)
                thru[x]+=t
    return dist,npath,thru
B=C=Dd=0
for a in range(N):
    dist,npath,thru = count_sp(a)
    for b in range(N):
        if b==a or b not in dist: continue
        if a==cape or b==cape: continue
        if thru[b]>0: B+=1                       # some shortest path transits
        if thru[b]==npath[b] and npath[b]>0: C+=1  # every shortest path transits
        if npath[b]==1 and thru[b]==1: Dd+=1     # unique shortest path through cape
print('A (a->cape, cape->b, a->b)          :',A)
print('B (some shortest path transits)     :',B)
print('C (every shortest path transits)    :',C)
print('D (unique shortest path via cape)   :',Dd)
print('cape indeg/outdeg:',sum(1 for u,v in D if v==cape), sum(1 for u,v in D if u==cape))
g=NIDX['genua']
print('genua indeg/outdeg:',sum(1 for u,v in D if v==g), sum(1 for u,v in D if u==g))
