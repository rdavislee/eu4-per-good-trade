# -*- coding: utf-8 -*-
"""r12: reproduce the round-5 both-ends gate measurement on Castile1444_12_22.eu4.
Bears on Y1158 ("no session has observed it") and Y1326 ("no ... recorded session supports it")."""
import re, zipfile, collections, os
SAVE=r"C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\Castile1444_12_22.eu4"
raw=zipfile.ZipFile(SAVE).read("gamestate").decode("latin-1")
def mb(s,i):
    d=0;k=i;q=False
    while k<len(s):
        c=s[k]
        if c=='"': q=not q
        elif not q:
            if c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0: return k
        k+=1
    return len(s)-1
i2=raw.index("\ntrade={"); j2=raw.index("{",i2); tb=raw[j2+1:mb(raw,j2)]
order=[]; NODE={}
for mm in re.finditer(r"^\tnode=\{", tb, re.M):
    s2=tb.index("{",mm.start()); nd=tb[s2+1:mb(tb,s2)]
    nm=re.search(r'definitions="([a-z_]+)"',nd).group(1)
    order.append(nm); NODE[nm]=nd
print("nodes in save order: %d" % len(order))
# per-node per-country total power (val=) -- "holds power" at that node
POW=collections.defaultdict(dict)
for nm,nd in NODE.items():
    for cm in re.finditer(r'^\t\t([A-Z]{3})=\{', nd, re.M):
        s3=nd.index("{",cm.start()); cblk=nd[s3+1:mb(nd,s3)]
        v=re.search(r"^\t\t\tval=([\d.]+)", cblk, re.M)
        if v and float(v.group(1))>0: POW[nm][cm.group(1)]=float(v.group(1))
print("nodes with >=1 country holding power: %d" % sum(1 for n in order if POW[n]))
# incoming blocks -> per-link realised value
links=[]
for nm,nd in NODE.items():
    for im in re.finditer(r"^\t\tincoming=\{", nd, re.M):
        s3=nd.index("{",im.start()); ib=nd[s3+1:mb(nd,s3)]
        frm=re.search(r"from=(\d+)",ib); val=re.search(r"value=([-\d.]+)",ib)
        add=re.search(r"add=([-\d.]+)",ib)
        if not frm: continue
        up=order[int(frm.group(1))-1]
        links.append((up,nm,float(val.group(1)) if val else 0.0, float(add.group(1)) if add else 0.0))
print("incoming link blocks: %d" % len(links))
print("all 'from' indices resolved to a real node: %s" % all(l[0] in NODE for l in links))
zero=[l for l in links if l[2]==0.0]; nonzero=[l for l in links if l[2]!=0.0]
def bothends(u,v):
    return sorted(set(POW[u]) & set(POW[v]))
z_nobe=[l for l in zero if not bothends(l[0],l[1])]
nz_nobe=[l for l in nonzero if not bothends(l[0],l[1])]
print()
print("=== the round-5 gate table, reproduced ===")
print("  links total                                  : %d" % len(links))
print("  zero-value links                             : %d" % len(zero))
print("    of those, NO country holds power at both ends: %d" % len(z_nobe))
print("    of those, >=1 country holds both ends        : %d  (the gate cannot explain these)" % (len(zero)-len(z_nobe)))
print("  value-carrying links                         : %d" % len(nonzero))
print("    of those, NO country holds power at both ends: %d" % len(nz_nobe))
print()
print("  value-carrying links with NO both-ends holder (counterexamples to the gate):")
for u,v,val,add in nz_nobe: print("     %-22s -> %-22s value=%.3f" % (u,v,val))
print()
print("  zero-value links WITH both-ends holders (top by holder count):")
rows=sorted(((len(bothends(u,v)),u,v) for u,v,val,add in zero if bothends(u,v)), reverse=True)
for n,u,v in rows[:8]: print("     %-22s -> %-22s  %d both-ends holders" % (u,v,n))
# contingency + association
a=len(z_nobe); b=len(zero)-a; c=len(nz_nobe); d=len(nonzero)-c
print()
print("  contingency  [no both-ends holder / has one]:")
print("     zero-value : %3d / %3d" % (a,b))
print("     has value  : %3d / %3d" % (c,d))
try:
    import math
    n=a+b+c+d; chi=n*(a*d-b*c)**2/((a+b)*(c+d)*(a+c)*(b+d))
    print("     chi-square (1 df) = %.1f" % chi)
except Exception as e: print(e)

print()
print("=== the 3 counterexample links, in detail ===")
for u,v,val,add in nz_nobe:
    print("  %s -> %s   value=%.3f add=%.3f" % (u,v,val,add))
    print("     power holders at %-22s: %s" % (u, sorted(POW[u].items(), key=lambda t:-t[1])[:8] or "NONE"))
    print("     power holders at %-22s: %s" % (v, sorted(POW[v].items(), key=lambda t:-t[1])[:8] or "NONE"))
