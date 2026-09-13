#!/bin/bash

set -e

wit extract "$1" wbi_extracted
python3 patch.py
rm wbi_patched.iso
wit copy wbi_extracted/ wbi_patched.iso
