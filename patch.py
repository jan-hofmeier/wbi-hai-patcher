#!/usr/bin/env python3

import pathlib
from ppc_asm.dol_file import DolFile
from ppc_asm.assembler.ppc import *

dol_file = DolFile(pathlib.Path("wbi_extracted/sys/main.dol"))
dol_file.set_editable(True)
with dol_file:
    # Don't init HID
    dol_file.write_instructions(
        0x801193e0,
        [
            nop(),
        ]
    )
    # Don't poll HID
    dol_file.write_instructions(
        0x801193e0,
        [
            blr(),
        ]
    )