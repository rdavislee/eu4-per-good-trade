import re
p=r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\tradenodes\00_tradenodes.txt"
txt=open(p,encoding='latin-1').read()
txt=re.sub(r'#.*','',txt)
# top-level blocks
nodes={}
i=0; n=len(txt)
while i<n:
    m=re.compile(r'([A-Za-z_0-9]+)\s*=\s*\{').search(txt,i)
    if not m: break
    name=m.group(1); j=m.end(); depth=1
    while depth>0 and j<n:
        if txt[j]=='{': depth+=1
        elif txt[j]=='}': depth-=1
        j+=1
    body=txt[m.end():j-1]
    nodes[name]={'inland':'inland=yes' in body.replace(' ',''),
                 'out':re.findall(r'outgoing\s*=\s*\{\s*name\s*=\s*"?([A-Za-z_0-9]+)"?', body)}
    i=j
print("nodes:",len(nodes))
inland=[k for k,v in nodes.items() if v['inland']]
print("inland:",len(inland))
print(sorted(inland))
adj=set()
for k,v in nodes.items():
    for o in v['out']:
        if o in nodes and nodes[o]['inland']:
            adj.add(k)
print("nodes with an outgoing link INTO an inland node (v1 reading surface):",len(adj))
print(sorted(adj))
# any node adjacent (either direction) to an inland node
adj2=set()
for k,v in nodes.items():
    if v['inland']: continue
    for o in v['out']:
        if o in nodes and nodes[o]['inland']: adj2.add(k)
for k in inland:
    for o in nodes[k]['out']:
        if o in nodes and not nodes[o]['inland']: adj2.add(o)
print("non-inland nodes adjacent (either direction) to an inland node:",len(adj2))
print("overlap inland & v1-surface:", len(set(inland)&adj))
