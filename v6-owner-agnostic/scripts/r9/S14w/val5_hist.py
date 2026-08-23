# -*- coding: utf-8 -*-
"""History-file parser used by the round-5 audit: value of a key effective at 1444.11.11,
undated block first, then every dated block on or before the start date in date order."""
import io, os, re
H = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\history\provinces"
START = (1444, 11, 11)

def blocks(tx):
    tx = re.sub(r"#[^\n]*", "", tx)
    spans = []
    for m in re.finditer(r"(\d{3,4})\.(\d{1,2})\.(\d{1,2})\s*=\s*\{", tx):
        k = tx.index("{", m.start()); st = k; d = 0
        while k < len(tx):
            if tx[k] == "{": d += 1
            elif tx[k] == "}":
                d -= 1
                if d == 0: break
            k += 1
        spans.append((m.start(), k + 1,
                      (int(m.group(1)), int(m.group(2)), int(m.group(3))), tx[st+1:k]))
    keep = []; prev = 0
    for s, e, dt, body in spans:
        keep.append(tx[prev:s]); prev = e
    keep.append(tx[prev:])
    return "".join(keep), spans

def eff(tx, key, additive=False):
    ud, spans = blocks(tx)
    val = None
    m = re.findall(r"^\s*" + key + r"\s*=\s*(-?[\d.]+)", ud, re.M)
    if m: val = float(m[-1])
    for s, e, dt, body in sorted(spans, key=lambda x: x[2]):
        if dt <= START:
            mm = re.findall(r"\b" + key + r"\s*=\s*(-?[\d.]+)", body)
            for x in mm:
                if additive: val = (val or 0.0) + float(x)
                else: val = float(x)
    return val

def files():
    out = {}
    for fn in os.listdir(H):
        m = re.match(r"^\s*(\d+)", fn)
        if m: out[int(m.group(1))] = os.path.join(H, fn)
    return out

def text(pid, F=None):
    F = F or files()
    return io.open(F[pid], encoding="latin-1", errors="replace").read()
