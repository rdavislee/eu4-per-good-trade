import re
path = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\tradenodes\00_tradenodes.txt"
text = open(path, encoding='latin-1').read()
nodes = {}
pattern = re.compile(r'^(\w+)\s*=\s*\{', re.M)
for m in pattern.finditer(text):
    name = m.group(1)
    start = m.end()
    depth = 1
    j = start
    while depth > 0 and j < len(text):
        if text[j] == '{': depth += 1
        elif text[j] == '}': depth -= 1
        j += 1
    block = text[start:j-1]
    nodes[name] = block

for target in ['cape_of_good_hope', 'girin', 'champagne', 'nippon']:
    if target in nodes:
        block = nodes[target]
        mem = re.search(r'members\s*=\s*\{([^}]*)\}', block)
        if mem:
            ids = mem.group(1).split()
            print(target, "members count:", len(ids), ids[:25])
        else:
            print(target, "no members found")
    else:
        print(target, "NOT FOUND as top-level node")
print("total nodes parsed:", len(nodes))
