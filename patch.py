#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path

try:
    from ppc_asm.dol_file import DolFile
    from ppc_asm.assembler.ppc import nop, blr
except ImportError:
    sys.exit(
        "Error: Missing required dependency 'ppc_asm'.\n"
        "Please run './install_requirements.sh' or 'python3 -m pip install -r requirements.txt' to install dependencies."
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Patch Worms Battle Island DOL file.")
    parser.add_argument(
        "--dol",
        type=Path,
        help="Path to main.dol file (default: wbi_extracted/sys/main.dol)",
    )
    parser.add_argument(
        "--dir",
        "--extract-dir",
        type=Path,
        dest="extract_dir",
        help="Path to extracted ISO directory",
    )
    intro_group = parser.add_mutually_exclusive_group()
    intro_group.add_argument(
        "--nointro",
        action="store_true",
        help="Disable the intro video and apply intro patches",
    )
    intro_group.add_argument(
        "--intro",
        action="store_true",
        help="Keep the intro video and do not apply intro patches",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.extract_dir:
        extract_dir = args.extract_dir
        dol_path = args.dol if args.dol else extract_dir / "sys" / "main.dol"
    elif args.dol:
        dol_path = args.dol
        extract_dir = dol_path.parent.parent
    else:
        extract_dir = Path("wbi_extracted")
        dol_path = extract_dir / "sys" / "main.dol"

    if args.nointro:
        keep_intro = False
    elif args.intro:
        keep_intro = True
    else:
        try:
            response = input("Keep intro video? [Y/n]: ").strip().lower()
            if response == "" or response.startswith("y"):
                keep_intro = True
            else:
                keep_intro = False
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

    if not dol_path.exists():
        sys.exit(f"Error: DOL file not found at '{dol_path}'")

    dol_file = DolFile(dol_path)
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
            0x803353b0,
            [
                blr(),
            ]
        )

        if not keep_intro:
            # Disable intro patches
            dol_file.write_instructions(
                0x800958b4,
                [
                    nop(),
                ]
            )
            dol_file.write_instructions(
                0x800958d8,
                [
                    nop(),
                ]
            )

    if not keep_intro:
        video_files = [
            extract_dir / "files" / "DataWii" / "Video" / "T17.thp",
            extract_dir / "files" / "DataWii" / "Video" / "THQ.thp",
        ]
        for video_file in video_files:
            if video_file.exists():
                try:
                    video_file.unlink()
                    print(f"Removed intro video: {video_file}")
                except Exception as e:
                    print(f"Warning: Could not remove {video_file}: {e}")

    print("Patching complete.")


if __name__ == "__main__":
    main()
