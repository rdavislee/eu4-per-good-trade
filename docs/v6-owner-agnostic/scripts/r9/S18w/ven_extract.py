import zipfile
f = r'C:\Users\rdavi\OneDrive\Documents\Paradox Interactive\Europa Universalis IV\save games\Castile1444_12_22.eu4'
z = zipfile.ZipFile(f)
data = z.read('gamestate')
txt = data.decode('latin-1')

def extract_block(txt, start_idx):
    depth = 0
    for i in range(start_idx, len(txt)):
        if txt[i] == '{':
            depth += 1
        elif txt[i] == '}':
            depth -= 1
            if depth == 0:
                return txt[start_idx:i+1]
    return None

i = txt.find('definitions="venice"')
node_start = txt.rfind('node={', 0, i)
brace_idx = node_start + len('node=')
block = extract_block(txt, brace_idx)
with open('venice_block.txt', 'w', encoding='utf-8', errors='replace') as fo:
    fo.write(block)
print("wrote", len(block), "chars")
