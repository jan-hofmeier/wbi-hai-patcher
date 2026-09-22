# wbi-hai-patcher

Patches *Worms Battle Island* to work with HAI-IOS (Wii U VC Inject).

## Prerequisites

- Python 3.x
- `wit` (Wiimms ISO Tool) installed and available in your `PATH`.

## Installation

Install Python dependencies by running:

```bash
./install_requirements.sh
```

Or manually:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

### Simple / Shell Script (`patch_iso.sh`)

Run `patch_iso.sh` directly:

```bash
./patch_iso.sh [PATH_TO_ISO_OR_WBFS] [OPTIONS]
```

- If no file path is provided as the first argument, the script will prompt you to drop or type the path into the window.
- Additional options (like `--nointro` or `--intro`) are passed directly to `patch.py`.

Example:

```bash
./patch_iso.sh "Worms Battle Island.iso" --nointro
```

### Python Patching Script (`patch.py`)

If you already extracted the game or want to run `patch.py` directly:

```bash
python3 patch.py [OPTIONS]
```

#### Options

- `--dol <PATH>`: Path to `main.dol` (defaults to `wbi_extracted/sys/main.dol`).
- `--dir <PATH>`, `--extract-dir <PATH>`: Path to the extracted game directory.
- `--nointro`: Skip intro videos and apply intro bypass patches.
- `--intro`: Keep intro videos and do not apply intro bypass patches.

If neither `--intro` nor `--nointro` is provided, `patch.py` will prompt you whether to keep the intro video (default: Yes).

---

## Technical Information

### What the patcher does

1. **Extraction & Rebuilding (`patch_iso.sh`)**:
   - Extracts only the **DATA** partition (`wit extract --psel DATA`) into `wbi_extracted/`, bypassing update partitions.
   - Overwrites existing `wbi_extracted/` directories and `wbi_patched.wbfs` files if present (`--overwrite`).
   - Copies the modified directory structure into a `.wbfs` file using `wit copy`.

2. **DOL Assembly Patching (`patch.py`)**:
   - Uses `ppc_asm` (`ppc_asm.dol_file.DolFile`) to modify PowerPC instructions in `main.dol`:
     - **Disable HID Initialization**: Replaces instruction at address `0x801193e0` with `nop` (no operation).
     - **Disable HID Polling**: Replaces instruction at address `0x803353b0` with `blr` (branch to link register / return).

3. **No-Intro Patches & Cleanup**:
   - When `--nointro` is selected:
     - Patches address `0x800958b4` with `nop`.
     - Patches address `0x800958d8` with `nop`.
     - Deletes the intro video files:
       - `files/DataWii/Video/T17.thp`
       - `files/DataWii/Video/THQ.thp`
