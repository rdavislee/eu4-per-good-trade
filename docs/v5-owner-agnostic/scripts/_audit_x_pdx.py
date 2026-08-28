"""Independent PDX-script parser for the v5 audit. Not derived from scripts/pdx.py."""
import re, io

TOK = re.compile(r'"[^"]*"|[^\s{}=]+|[{}=]')

def strip_comments(text):
    out = []
    for line in text.split('\n'):
        # naive: '#' outside quotes starts a comment
        q = False; buf = []
        for ch in line:
            if ch == '"': q = not q
            if ch == '#' and not q: break
            buf.append(ch)
        out.append(''.join(buf))
    return '\n'.join(out)

def tokenize(text):
    return TOK.findall(strip_comments(text))

class Blk(list):
    """list of (key, value) pairs; value is str or Blk. Preserves duplicates."""
    def get(self, k, default=None):
        for kk, vv in self:
            if kk == k: return vv
        return default
    def getall(self, k):
        return [vv for kk, vv in self if kk == k]
    def keylist(self):
        return [kk for kk, vv in self]

def parse_tokens(toks, i=0, top=True):
    b = Blk()
    while i < len(toks):
        t = toks[i]
        if t == '}':
            return b, i+1
        if t == '=':
            i += 1; continue
        if t == '{':
            # anonymous block (list element)
            sub, i = parse_tokens(toks, i+1, False)
            b.append((None, sub)); continue
        key = t.strip('"')
        # lookahead
        if i+1 < len(toks) and toks[i+1] == '=':
            if i+2 < len(toks) and toks[i+2] == '{':
                sub, i = parse_tokens(toks, i+3, False)
                b.append((key, sub))
            else:
                b.append((key, toks[i+2].strip('"'))); i += 3
        elif i+1 < len(toks) and toks[i+1] == '{':
            sub, i = parse_tokens(toks, i+2, False)
            b.append((key, sub))
        else:
            b.append((key, None)); i += 1
    return b, i

def parse(text):
    b, _ = parse_tokens(tokenize(text))
    return b

def parse_file(path):
    with open(path, 'rb') as f:
        raw = f.read()
    for enc in ('utf-8-sig', 'utf-8', 'cp1252', 'latin-1'):
        try:
            return parse(raw.decode(enc))
        except UnicodeDecodeError:
            continue
    return parse(raw.decode('latin-1', 'replace'))

def flatten(b, prefix=''):
    """yield (path, key, value) for scalar leaves"""
    for k, v in b:
        if isinstance(v, Blk):
            yield from flatten(v, prefix + (k or '?') + '/')
        else:
            yield (prefix, k, v)
