#!/bin/bash

set -e

INPUT_FILE="$1"

if [ -n "$INPUT_FILE" ]; then
    shift
fi

if [ -z "$INPUT_FILE" ]; then
    read -rp "Please drop or enter the ISO/WBFS file path: " INPUT_FILE
    # Strip leading and trailing quotes if present
    INPUT_FILE="${INPUT_FILE#[\"\']}"
    INPUT_FILE="${INPUT_FILE%[\"\']}"
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' does not exist." >&2
    exit 1
fi

wit extract --psel DATA "$INPUT_FILE" wbi_extracted
python3 patch.py "$@"
wit copy --overwrite wbi_extracted/ wbi_patched.wbfs

echo "Successfully created wbi_patched.wbfs!"
