# -*- coding: utf-8 -*-
"""Disassemble eu4.exe around given RVAs, resolving RIP-relative operands to VAs.
Usage: python disasm.py <rva_hex> [count]"""
import sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\eu4.exe"

def main(rva, count):
    pe = pefile.PE(EXE, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    data = pe.__data__
    text = next(s for s in pe.sections if s.Name.rstrip(b"\x00") == b".text")
    foff = text.PointerToRawData + (rva - text.VirtualAddress)
    code = data[foff:foff + count * 12 + 64]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    n = 0
    for insn in md.disasm(code, rva):
        extra = ""
        if "rip" in insn.op_str:
            import re
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
            if m:
                disp = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                tgt = insn.address + insn.size + disp
                extra = "   ; -> VA 0x%x (eu4.exe+0x%x)" % (base + tgt, tgt)
        print("eu4.exe+0x%-7x  %-8s %s%s" % (insn.address, insn.mnemonic, insn.op_str, extra))
        n += 1
        if n >= count:
            break

if __name__ == "__main__":
    main(int(sys.argv[1], 16), int(sys.argv[2]) if len(sys.argv) > 2 else 40)
