# -*- coding: utf-8 -*-
"""Static cross-reference finder for the RE session (spec 2.9 memory track).
Locates the trade code in eu4.exe by finding RIP-relative references to the trade assert/log
strings (trade.cpp, tradenode.cpp, trademanager.cpp, "tradenode init [", ...). The referencing
instructions are the trade functions; their addresses (as eu4.exe+offset, matching the live
module base) are the code seams the DLL hooks. Purely static -- no running game needed.

Usage: python xref.py "<string>" [more strings...]
"""
import sys, re
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\eu4.exe"


def main(strings):
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = pe.__data__
    secs = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("latin-1")
        secs.append((name, s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData))
        print("section %-8s VA 0x%x size 0x%x raw 0x%x" % (name, s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData))
    print("image base 0x%x" % base)

    def va_to_off(va):
        rva = va - base
        for _, vaddr, vsize, praw, sraw in secs:
            if vaddr <= rva < vaddr + max(vsize, sraw):
                return praw + (rva - vaddr)
        return None

    def off_to_rva(off):
        for _, vaddr, vsize, praw, sraw in secs:
            if praw <= off < praw + sraw:
                return vaddr + (off - praw)
        return None

    # locate each string's RVA (search whole file, map to RVA)
    targets = {}
    for needle in strings:
        nb = needle.encode("latin-1") + b"\x00"
        idx = data.find(nb)
        if idx < 0:
            idx = data.find(needle.encode("latin-1"))
        if idx < 0:
            print("  string not found: %r" % needle); continue
        rva = off_to_rva(idx)
        targets[needle] = rva
        print("string %-28r file 0x%x rva 0x%x va 0x%x" % (needle, idx, rva, base + rva))

    # Robust xref: scan .text for the 4-byte RIP-relative displacement that resolves to each
    # string RVA. A RIP-relative operand's disp32 sits at some offset; the effective address is
    # (rva just AFTER the disp32) + int32(disp). So for every 4-byte window, check if it points
    # at a target. This finds all lea/mov/push [rip+disp] refs without instruction alignment.
    import struct
    text = next(s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text")
    tstart = text.PointerToRawData
    tsize = text.SizeOfRawData
    trva = text.VirtualAddress
    code = data[tstart:tstart + tsize]
    want_rvas = {rva: name for name, rva in targets.items()}
    md = Cs(CS_ARCH_X86, CS_MODE_64)

    print("\n=== code references (eu4.exe+offset) ===")
    hits = []
    for i in range(0, len(code) - 4):
        disp = struct.unpack_from("<i", code, i)[0]
        end_rva = trva + i + 4
        tgt = end_rva + disp
        if tgt in want_rvas:
            # the referencing instruction starts a few bytes before i; decode a small window
            wstart = max(0, i - 3)
            insns = list(md.disasm(code[wstart:i + 8], trva + wstart))
            desc = ""
            for ins in insns:
                if ins.address <= trva + i < ins.address + ins.size and "rip" in ins.op_str:
                    desc = "%s %s @ eu4.exe+0x%x" % (ins.mnemonic, ins.op_str, ins.address)
                    break
            code_rva = trva + i - 3   # approx instruction start (disp32 is last 4 bytes of a 7B lea)
            hits.append((code_rva, want_rvas[tgt], desc))
            print("eu4.exe+0x%-9x -> %-22r %s" % (code_rva, want_rvas[tgt], desc))
    print("\n%d references found" % len(hits))
    return hits


if __name__ == "__main__":
    args = sys.argv[1:] or ["tradenode init [", "tradenode.cpp", "trade.cpp", "trademanager.cpp",
                            "tradenodedatabase.cpp"]
    main(args)
