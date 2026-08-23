import re, sys

path = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\common\tradenodes\00_tradenodes.txt"
text = open(path, encoding='latin1').read()

# find top-level node blocks: identifier = { ... } at top level (not nested outgoing etc.)
# Simple brace-depth tokenizer
i = 0
n = len(text)
nodes = []  # (name, start_idx, end_idx, depth0 body)
depth = 0
tok_start = None
pos = 0
# We'll scan for pattern: NAME = { at depth 0
pattern = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{')
idx = 0
node_list = []
while True:
    m = pattern.search(text, idx)
    if not m:
        break
    name = m.group(1)
    brace_start = m.end() - 1  # position of '{'
    # only consider top-level (depth==0 before this match)
    # compute depth at m.start() by counting braces from start of file to m.start() -- expensive but file is small
    prefix = text[:m.start()]
    d = prefix.count('{') - prefix.count('}')
    if d == 0:
        # find matching close brace
        depth2 = 0
        j = brace_start
        while j < n:
            if text[j] == '{':
                depth2 += 1
            elif text[j] == '}':
                depth2 -= 1
                if depth2 == 0:
                    break
            j += 1
        body = text[brace_start+1:j]
        node_list.append((name, m.start(), j, body))
        idx = j+1
    else:
        idx = m.end()

print("top-level blocks found:", len(node_list))
names = [nm for nm,_,_,_ in node_list]
print("first 5:", names[:5])
print("last 5:", names[-5:])

# Now for each node body, find "outgoing = { ... }" blocks (there can be multiple) and extract the "name" field inside.
outgoing_pat = re.compile(r'outgoing\s*=\s*\{')
end_pat = re.compile(r'\bend\s*=\s*yes\b')

order_index = {name.lower(): idx for idx,(name,_,_,_) in enumerate(node_list)}

links = []  # (src, dst, src_index_in_file, dst_index_in_file)
end_nodes = []

for idx_n,(name, s, e, body) in enumerate(node_list):
    if end_pat.search(body):
        end_nodes.append(name)
    for om in outgoing_pat.finditer(body):
        ostart = om.end()-1
        depth2 = 0
        j = ostart
        while j < len(body):
            if body[j] == '{':
                depth2 += 1
            elif body[j] == '}':
                depth2 -= 1
                if depth2 == 0:
                    break
            j += 1
        obody = body[ostart+1:j]
        nm = re.search(r'name\s*=\s*"?([A-Za-z_][A-Za-z0-9_]*)"?', obody)
        if nm:
            dst = nm.group(1)
            links.append((name, dst))

print("total outgoing links found:", len(links))
print("end=yes nodes:", end_nodes, "count:", len(end_nodes))

# check declaration order: convention = emit in decreasing order, i.e. an outgoing link's target must
# be declared AFTER the source in the file (per engine's error text: "an outgoing is defined after in the file")
violations = []
for src, dst in links:
    si = order_index.get(src.lower())
    di = order_index.get(dst.lower())
    if si is None or di is None:
        print("MISSING INDEX", src, dst, si, di)
        continue
    # engine wants: for src -> dst (outgoing), the destination (the one further down chain, "outgoing")
    # error message: "X=>y ERROR: outgoing is defined after" -- meaning it wants outgoing target defined AFTER source? 
    # Let's just record ordering both ways for inspection
    violations.append((src, dst, si, di, di > si))

after_count = sum(1 for *_, ok in violations if ok)
before_count = len(violations) - after_count
print("dst declared AFTER src (index):", after_count, "of", len(violations))
print("dst declared BEFORE src (index):", before_count, "of", len(violations))
