# Worms Battle Island HAI Patcher

Patches *Worms Battle Island* to work as a Wii U VC Inject. It also has patches for disabeling the THQ and Team17 Intros.

There are two ways of applying the patch:

1. If you are using [UInjectForge](https://zestyts.itch.io/uinjectforge), you can just add the patches during the build.
2. For UWUVCI or Teconmoon VC Injector you can patch the wbfs file before injecting it.



**Note about Gamepad support:** You can use the Gamepad to emulate a horizontal Wii Mote and it will work for Gameplay. But be aware that you need a real Wii Mote Initially to create your Team as the on screen Keyboard for entering the names needs a pointer.



## UInjectForge

UInjectForge (UIF) can use the same patched ISO as UWUVCI, but with UIF you can also apply the [patches](https://github.com/jan-hofmeier/wbi-hai-patcher/tree/main/UInjectForge) directly:

On **Step 2**, after selecting the Source Game:

- Select **Horizontal Wii Remote**
- Expand **Game Files & Executable Patches**
- Click **Extract main.dol** and select a directory of your choice
- **Import Patch** and select the downloaded [vc-fix.uifdolpatch](https://github.com/jan-hofmeier/wbi-hai-patcher/blob/main/UInjectForge/vc-fix.uifdolpatch) **or** [no-intro.uifdolpatch](https://github.com/jan-hofmeier/wbi-hai-patcher/blob/main/UInjectForge/no-intro.uifdolpatch)
- Click **Preview Patch**
- Check **Apply executable patch during build**



## Patch ISO

For UWUVCI or Teconmoon VC Injector patch the wbfs

### Prerequisites

- Python 3.x
- [WIT](https://wit.wiimm.de/download.html) (Wiimms ISO Tool) installed and available in your `PATH`.
- Download this Repository

### Installation

Install Python dependencies:

- **Windows**:
  Double-click `install_requirements.bat` or run:
  ```cmd
  install_requirements.bat
  ```

- **Linux / macOS**:
  Run:
  ```bash
  ./install_requirements.sh
  ```

- **Manual (All Platforms)**:
  ```bash
  python -m pip install -r requirements.txt
  ```

### Usage

#### Simple / Shell Script & Batch File (`patch_iso.sh` / `patch_iso.bat`)

- **Windows**:
  Double-click `patch_iso.bat` or drag-and-drop your ISO/WBFS file onto `patch_iso.bat`.

  You can also run it from Command Prompt / PowerShell:
  ```cmd
  patch_iso.bat [PATH_TO_ISO_OR_WBFS] [OPTIONS]
  ```

- **Linux / macOS**:
  Run `patch_iso.sh` directly:
  ```bash
  ./patch_iso.sh [PATH_TO_ISO_OR_WBFS] [OPTIONS]
  ```

##### Notes
- If no file path is provided as the first argument, the script will prompt you to drop or type the path into the window.
- Additional options (like `--nointro` or `--intro`) are passed directly to `patch.py`.

Example:

```bash
# Windows
patch_iso.bat "Worms Battle Island.iso" --nointro

# Linux / macOS
./patch_iso.sh "Worms Battle Island.iso" --nointro
```

#### Python Patching Script (`patch.py`)

If you already extracted the game or want to run `patch.py` directly:

```bash
python patch.py [OPTIONS]
```

##### Options

- `--dol <PATH>`: Path to `main.dol` (defaults to `wbi_extracted/sys/main.dol`).
- `--dir <PATH>`, `--extract-dir <PATH>`: Path to the extracted game directory.
- `--nointro`: Skip intro videos and apply intro bypass patches.
- `--intro`: Keep intro videos and do not apply intro bypass patches.

If neither `--intro` nor `--nointro` is provided, `patch.py` will prompt you whether to keep the intro video (default: Yes).

---

## Technical Information

### What the patcher does

1. **Extraction & Rebuilding (`patch_iso.sh` / `patch_iso.bat`)**:
   - Extracts only the **DATA** partition (`wit extract --psel DATA`) into `wbi_extracted/`, bypassing update partitions. (Overwrites existing `wbi_extracted/` ).
   - Runs `patch.py`
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
