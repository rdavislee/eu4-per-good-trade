import os,sys,collections,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from solver import N, ORDER, NIDX
import measure6 as M
r=M.ph(); D=r["directed"]
adj=collections.defaultdict(list)
for u,v in D: adj[u].append(v)
def paths_exist_through(s,t,via):
    # does any directed path s->t pass through via?
    # reach sets
    def reach(x):
        seen={x};st=[x]
        while st:
            a=st.pop()
            for b in adj[a]:
                if b not in seen: seen.add(b); st.append(b)
        return seen
    return (via in reach(s)) and (t in reach(via))
def reach(x):
    seen={x};st=[x]
    while st:
        a=st.pop()
        for b in adj[a]:
            if b not in seen: seen.add(b); st.append(b)
    seen.discard(x); return seen
R={i:reach(i) for i in range(N)}
# European node list: look for europe_provinces.json or a EURO constant in measure6
eur=None
for name in ('EUROPE_NODES','EUR_NODES','EURO'):
    if hasattr(M,name): eur=getattr(M,name); print('found',name)
print('measure6 attrs with EU:',[a for a in dir(M) if 'EU' in a.upper() or 'eur' in a.lower()][:10])
sinks=sorted(M.sk(r))
print('sinks',sinks)
cape=NIDX['cape_of_good_hope']
# candidate european nodes by name
EURNAMES=['english_channel','north_sea','baltic_sea','white_sea','novgorod','lubeck','rheinland','saxony','wien','krakow','pest','venice','ragusa','genua','champagne','bordeaux','valencia','sevilla','constantinople','crimea','kiev','kazan']
print('22-list all present:',all(n in NIDX for n in EURNAMES))
import europe as E
print('europe module attrs:',[a for a in dir(E) if not a.startswith('_')][:25])
