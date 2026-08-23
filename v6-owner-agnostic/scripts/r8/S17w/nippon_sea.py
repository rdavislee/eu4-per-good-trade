import re
mappath = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\map\default.map"
text = open(mappath, encoding='latin-1').read()
m = re.search(r'sea_starts\s*=\s*\{([^}]*)\}', text, re.S)
sea = set(m.group(1).split())
print("sea_starts count:", len(sea))
print("1460 in sea_starts:", "1460" in sea)

nippon_members = ['1376', '1012', '1014', '1017', '1018', '1019', '1020', '1021', '1023', '1024', '1025', '1026', '1027', '1028', '1029', '1030', '1031', '1032', '1818', '1819', '1820', '1825', '1830', '1832', '1835']
# get full nippon list
tnpath = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\tradenodes\00_tradenodes.txt"
ttext = open(tnpath, encoding='latin-1').read()
pattern = re.compile(r'^(\w+)\s*=\s*\{', re.M)
nodes = {}
for mm in pattern.finditer(ttext):
    name = mm.group(1)
    start = mm.end()
    depth = 1
    j = start
    while depth > 0 and j < len(ttext):
        if ttext[j] == '{': depth += 1
        elif ttext[j] == '}': depth -= 1
        j += 1
    nodes[name] = ttext[start:j-1]

mem = re.search(r'members\s*=\s*\{([^}]*)\}', nodes['nippon'])
ids = mem.group(1).split()
print("full nippon members:", ids)
sea_in_nippon = [i for i in ids if i in sea]
print("sea members in nippon:", sea_in_nippon)
print("land count in nippon:", len(ids) - len(sea_in_nippon))

mem2 = re.search(r'members\s*=\s*\{([^}]*)\}', nodes['girin'])
ids2 = mem2.group(1).split()
sea_in_girin = [i for i in ids2 if i in sea]
print("sea members in girin:", sea_in_girin, "count", len(ids2))
