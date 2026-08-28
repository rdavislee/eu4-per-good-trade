"""Minimal Paradox-script tokenizer/parser, good enough for 00_tradenodes.txt,
trade_goods, prices, colonial_regions, etc.

Produces a nested structure:  dict-like list of (key, value) pairs, since PDX
files repeat keys (e.g. multiple `outgoing={}` blocks).
"""
import re, io, sys, os

TOK = re.compile(r'"[^"]*"|[{}=]|[^\s{}=]+')

def strip_comments(text):
    out = []
    for line in text.split("\n"):
        # '#' starts a comment, but not inside quotes.  PDX files here have no
        # '#' inside quotes; keep it simple but quote-aware anyway.
        inq = False
        cut = len(line)
        for i, ch in enumerate(line):
            if ch == '"':
                inq = not inq
            elif ch == '#' and not inq:
                cut = i
                break
        out.append(line[:cut])
    return "\n".join(out)


def tokenize(text):
    return TOK.findall(strip_comments(text))


class Node(list):
    """list of (key, value) pairs; value is str or Node."""
    def get(self, key, default=None):
        for k, v in self:
            if k == key:
                return v
        return default

    def getall(self, key):
        return [v for k, v in self if k == key]

    def keys(self):
        return [k for k, _ in self]


def parse(text):
    toks = tokenize(text)
    pos = 0

    def parse_block(depth):
        nonlocal pos
        node = Node()
        while pos < len(toks):
            t = toks[pos]
            if t == '}':
                pos += 1
                return node
            if t == '=':
                pos += 1
                continue
            if t == '{':
                # anonymous block (array element that is itself a block)
                pos += 1
                node.append((None, parse_block(depth + 1)))
                continue
            # t is a key or a bare value
            key = t.strip('"')
            pos += 1
            if pos < len(toks) and toks[pos] == '=':
                pos += 1
                if pos < len(toks) and toks[pos] == '{':
                    pos += 1
                    node.append((key, parse_block(depth + 1)))
                else:
                    node.append((key, toks[pos].strip('"')))
                    pos += 1
            else:
                # bare token: array element
                node.append((None, key))
        return node

    return parse_block(0)


def load(path, encoding="latin-1"):
    with open(path, "r", encoding=encoding, errors="replace") as f:
        return parse(f.read())


def values(node):
    """bare (keyless) values in a block, e.g. members={ 1 2 3 }"""
    return [v for k, v in node if k is None and isinstance(v, str)]
