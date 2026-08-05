---
title: 3 · Installing Python
tag: Required
---

The detailed chapter. Three methods (standalone / conda / uv) × three platforms (macOS
arm64, Windows amd64, Linux x86_64). **Pick one method** — we recommend **uv** for
beginners. You only need Python installed once per machine.

## How to choose a version & architecture

- **Version:** pick a recent stable release — **Python 3.12** or **3.13** are safe choices
  in 2026. Not Python 2 (dead since 2020) and the very latest `.0` release if a package
  you need hasn't caught up yet.
- **Architecture** (your CPU type):
  - **macOS:** Apple Silicon Macs (M1/M2/M3/M4) → **arm64**. Intel Macs → **x86_64**.
  - **Windows:** almost all modern PCs → **amd64** (also called x64).
  - **Linux:** most desktops/servers → **x86_64**; newer ARM boards → **aarch64**.

If you are unsure, the installer pages below usually auto-detect the right one.

> **⚠️ Choose a Stable Release (all methods & platforms).** Whether you use the standalone
> installer, conda, or uv, pick a **Stable Release** — the latest stable version (e.g.
> Python 3.12.x or 3.13.x). **Do not** download or install anything marked *Pre-release* or
> *Development*: those builds are for testing and may be unstable or break your packages.

## Method A · With uv (most recommended)

Best for beginners: one fast tool, local environments, minimal fuss.

1. Install uv. Open the uv website (docs.astral.sh/uv) in your browser, go to the
   **Installation** page, and download the installer for your system (macOS, Windows, or
   Linux). Run it and follow the on-screen prompts — pick the default options when asked.
   When it finishes, uv is installed.

> 📝 After install, **close the terminal and open a new one**, then verify with `uv --version`.

2. Install a Python and create your first project:

```bash
uv python install 3.12          # download CPython 3.12 (one time)
uv init myproject               # create a project folder with a .venv
cd myproject
uv pip install pandas           # install a package into this project
uv run main.py                  # run a script with this project's Python
```

- **After closing the terminal**, you do **not** need to "activate" — just run
  `uv run <script>` from the project folder and uv uses the local `.venv` automatically.
- **To pin a pre-installed interpreter** (avoid re-downloading), set it in
  `pyproject.toml`: `requires-python = "&gt;=3.12"` and `uv venv --python 3.12`.

## Method B · With conda (Miniconda, recommended)

Best if you will use data-science packages with non-Python system dependencies.

1. Install Miniconda. Open the Miniconda website (anaconda.com) in your browser, find the
   **Miniconda** download for your system (macOS, Windows, or Linux), and download the
   installer. Run it and follow the on-screen prompts — when asked whether to "Add Miniconda
   to PATH" or "run conda init", you can leave the default; we explain `conda init` below.
   When it finishes, Miniconda is installed.

   > 📝 After install, **close the terminal and open a new one** so the `conda` command is
   > available. Then verify with `conda --version`.
2. Create and activate an environment:

```bash
conda create --name py312 python=3.12
conda activate py312
python --version
```

- **After closing the terminal**, the environment deactivates. Re-enter it with
  `conda activate py312` — the environment still exists globally, so you never recreate it.
- **To save disk space**, point conda at a Python you already installed instead of letting
  it download another copy: `conda create --name py312 --clone base` or use
  `conda create --name py312 python=$(python3 --version 2>&1 | cut -d' ' -f2)`.

### What to do if you are asked to run `conda init`

The first time you open a terminal after installing conda, `conda activate` may fail with a
message like *"To activate this environment, run `conda init` first."* Here is why, and what
to do.

**Why `conda init` is needed.** `conda activate` only works if conda has hooked into your
shell's startup file. `conda init` writes a small block of code into that file so the shell
loads conda automatically every time you open a new terminal. Until you do this, the shell
doesn't know what `conda activate` means.

**How to do it.** Just run it once for your shell (the command is harmless to re-run):

```bash
conda init bash        # Linux default shell
conda init zsh         # macOS default shell
conda init powershell  # Windows (run in PowerShell)
```

Then **close and reopen the terminal** — the change only takes effect in new sessions.

**Where does conda write the code?**
- **macOS / Linux (unix):** into your shell's rc file in your home directory —
  `~/.bashrc` for bash, `~/.zshrc` for zsh. Open a new terminal and conda is ready.
- **Windows:** into your **PowerShell profile script** (e.g.
  `C:\Users\<you>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`),
  *not* a `.bashrc`/`.zshrc` (those don't exist on Windows). If you use Git Bash on Windows,
  conda instead writes to `~/.bashrc` under your Git install.

**After `conda init`, you get a permanent prompt prefix.** Every new terminal will now show
your current conda environment in the prompt, e.g. `(base)` when no environment is active.
That `(base)` is a reminder of which environment your commands run in.

> **⚠️ Don't use `base` as your main environment.** `base` is conda's built-in default env.
> Keep it clean and instead `conda activate py312` (or any env you create) for real work,
> so packages for different projects don't clash. Tip: run `conda config --set
> auto_activate_base false` to stop conda from auto-activating `base` every time you open a
> terminal.

## Method C · Standalone installer

Best if you want the official Python and nothing else.

### Windows

1. Open the python.org Windows download page in your browser.
2. Download the **Windows installer (64-bit)** — the `amd64` executable.
3. **Important:** on the first setup screen, tick **"Add python.exe to PATH"** before
   clicking Install Now.
4. After install, reopen PowerShell and verify:

```powershell
python --version
# Python 3.12.x   (on Windows the command is `python`, not `python3`)
```
Most Windows personal computers are amd64 architecture; if you have a Microsoft Surface, it may be arm64.
To be sure which one you have, run this in PowerShell and check the value it prints:
```powershell
echo $env:PROCESSOR_ARCHITECTURE
# ARM64  -> you have an Arm-based Surface; download the arm64 installer
# AMD64  -> standard x64 PC; download the amd64 installer
```
Typical install path:
```text
C:\Users\<you>\AppData\Local\Programs\Python\Python312\
```

> ⚠️\
> If `python --version` still says "command not found" or opens the Microsoft Store, you
> forgot to tick **Add to PATH**. Re-run the installer and choose "Modify", then enable
> "Add Python to environment variables".

### macOS

Two routes:

- **Official installer** — open the python.org macOS download page in your browser and
  **always choose the "macOS 64-bit universal2" build.** A universal2 installer works on
  both Apple Silicon (arm64) and Intel Macs, so you don't need to figure out your chip.
  Avoid the "macOS 64-bit Intel-only installer": it only supports Intel Macs and only exists
  for older Python versions, so it's already outdated. Download the `.pkg`, double-click to
  run, and follow the prompts. It may ask you to manually adjust `PATH` — see "after install"
  below.
- **Homebrew** (recommended if you already use it): open the Homebrew website (brew.sh),
  install Homebrew first if you don't have it, then use it to install Python 3.12. It adds
  itself to PATH automatically when brew is set up.

Typical paths:
```text
# Official installer:
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3
# Homebrew:
/opt/homebrew/bin/python3        # Apple Silicon
/usr/local/bin/python3           # Intel
```

### Linux

Use your package manager, or build from source.

- Open your distro's software tool (or the package manager the system already uses) and
  install `python3` — e.g. on Debian/Ubuntu use `apt`, on Fedora use `dnf`, on Arch use
  `pacman`. The package-manager Python is usually at `/usr/bin/python3`.
- Or open the python.org source page in your browser, download the source tarball, then
  compile it yourself (more advanced — skip unless you have a reason).

> 📝
> On Linux, the system `python3` (e.g. `/usr/bin/python3`) is used by the OS. For your
> own projects, still create a virtual environment (Chapter 2) rather than installing
> packages globally with `sudo`.

## After install · test it works

Run this in your terminal. It prints the path of the Python that actually runs — this is
the one your commands use.

```bash
python3 -c "import sys; print(sys.executable)"
```

On macOS you might see something like:
```text
/opt/homebrew/bin/python3        # good — the one you installed
# or, if you forgot to set PATH:
/Applications/Xcode.app/Contents/Developer/usr/bin/python3   # Apple's, not yours
```

> ⚠️
> If it points to **Xcode's** or the **system** Python instead of what you installed, your
> `PATH` is wrong. Fix it by either activating your environment (`conda activate …` /
> `source .venv/bin/activate`) or adding the install path to your shell config
> (`~/.zshrc` on macOS, `~/.bashrc` on Linux). Then reopen the terminal and re-test.

## How to debug a broken install

1. **Find the correct executable path** with `which python3` (macOS/Linux) or
   `Get-Command python` (PowerShell).
2. **Confirm PATH**: `echo $PATH` (macOS/Linux) or `$env:PATH` (PowerShell) — your install
   directory should appear *before* system paths.
3. **Activate your environment** (conda / `.venv`) — this is the easiest fix and avoids
   touching `PATH` at all.
4. As a last resort, add the install path to your shell startup file and restart the
   terminal.

## Run your first program

Now that Python is installed, let's run a real script. Create a file named
`hello.py` (any plain-text editor works) and paste the code below. Then run it with
`python3 hello.py` (or `uv run hello.py` if you used uv).

This example prints a friendly greeting and reports your machine's architecture
(`platform.machine()`), the Python version, and the operating system — a quick sanity
check that your install is alive and that you know which CPU it runs on.

```python
import sys
import platform

def main():
    # 1. The classic first program
    print("Hello, world!")

    # 2. Report the computer architecture and environment
    print("\n--- Your machine ---")
    print(f"OS        : {platform.system()} {platform.release()}")
    print(f"Arch      : {platform.machine()}")   # e.g. arm64, x86_64, AMD64
    print(f"Python    : {sys.version.splitlines()[0]}")
    print(f"Executable: {sys.executable}")

if __name__ == "__main__":
    main()
```

Expected output (your numbers will differ):

```text
Hello, world!

--- Your machine ---
OS        : Darwin 24.0.0
Arch      : arm64
Python    : 3.12.4 (main, Jun  6 2024, 10:26:29) [Clang 15.0.0]
Executable: /opt/homebrew/bin/python3
```

> 💡
> The `if __name__ == "__main__":` line is a Python convention: it makes `main()` run
> only when you execute the file directly (not when you `import` it as a module later).
> Copy the block above — every code block on this site has a **Copy** button.

> 📝
> **About the shebang line (`#!/usr/bin/env python3`).** It is *not* Python
> syntax and does nothing when you run the file through an interpreter — it's only a
> tip for the operating system.
>
> ```python
> #!/usr/bin/env python3
> print("Hello, world!")
> ```
>
> **What it is / why write it.** On macOS & Linux the `#!` (shebang) tells the OS which
> program should run the file when you launch it directly. After `chmod +x hello.py`
> you can run `./hello.py` and the OS finds `python3` for you. Using
> `/usr/bin/env python3` (not a hardcoded `/usr/bin/python3`) lets `env` search `PATH`,
> so it picks up whatever Python you have active (conda / uv's `.venv`).
>
> **Why it "does nothing".** The shebang only matters when the OS launches the file
> itself. The moment you run it explicitly — `python3 hello.py` / `uv run hello.py`,
> exactly what we used above — Python treats that line as an ordinary comment and
> ignores it. So far it has had no effect at all.
>
> | How you run it | Shebang used? |
> | --- | --- |
> | `python3 hello.py` / `uv run hello.py` | No — ignored as a comment |
> | `./hello.py` (after `chmod +x`) | Yes — OS uses it to find the interpreter |
>
> **Windows:** the shebang is meaningless there — Windows picks the program from the
> `.py` extension/association, not the first line, so you can leave it out.
