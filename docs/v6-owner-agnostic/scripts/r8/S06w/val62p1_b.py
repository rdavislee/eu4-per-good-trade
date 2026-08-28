import zipfile, re, os
save = os.path.expanduser("~/OneDrive/Documents/Paradox Interactive/Europa Universalis IV/save games/VANILLA_start.eu4")
raw = zipfile.ZipFile(save).read("gamestate").decode("latin-1")
m = re.search(r"date=(\S+)", raw)
print("date:", m.group(1) if m else "NOT FOUND")
aw = len(re.findall(r'^active_war=\{', raw, re.M))
pw = len(re.findall(r'^previous_war=\{', raw, re.M))
print("active_war blocks:", aw, "| previous_war blocks:", pw)
i = raw.index("\nprovinces={"); j = raw.index("{", i)
def mb(s, k):
    d=0; inq=False
    while k < len(s):
        c=s[k]
        if c=='"': inq=not inq
        elif not inq:
            if c=="{": d+=1
            elif c=="}":
                d-=1
                if d==0: return k
        k+=1
    return len(s)-1
body = raw[j+1:mb(raw,j)]
mism=[]; owned=0; occ=0; sieged=0; unrest=[]
for m2 in re.finditer(r"^-(\d+)=\{", body, re.M):
    st = body.index("{", m2.start()); rec = body[st+1:mb(body,st)]
    o = re.search(r'^\t\towner="?([A-Za-z0-9]{3})', rec, re.M)
    c = re.search(r'^\t\tcontroller="?([A-Za-z0-9]{3})', rec, re.M)
    if re.search(r'^\t\tocc(upying_rebel_faction|upied)', rec, re.M): occ += 1
    if re.search(r'^\t\tsiege=', rec, re.M): sieged += 1
    u = re.search(r'^\t\tunrest=([-0-9.]+)', rec, re.M)
    if u and float(u.group(1)) != 0.0: unrest.append((m2.group(1), u.group(1)))
    if o:
        owned+=1
        if c and c.group(1)!=o.group(1): mism.append((m2.group(1), o.group(1), c.group(1)))
print("owned provinces:", owned, "| controller!=owner:", len(mism), mism[:10])
print("province records with a siege= field:", sieged, "| occupied-ish fields:", occ)
print("province records with non-zero unrest:", len(unrest), unrest[:10])
