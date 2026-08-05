---
title: 1 · Basic Unix-like Systems
tag: Skippable
---

A very short, friendly introduction to the command line. If you already open a terminal
daily, you can skip this chapter — but a 5-minute read helps if terms like *shell*, *PATH*,
or *sudo* are new to you.

## What is the command line?

The command line (also called the *terminal* or *shell*) is a text interface where you
type commands instead of clicking icons. You type a command, press Enter, and the computer
does exactly that.

The program that reads your commands is the **shell**. Different systems ship different
defaults:

- **Linux** → `bash` (Bourne Again Shell), and increasingly `zsh` on newer distros.
- **macOS** → `zsh` since macOS Catalina (older versions used `bash`).
- **Windows** → PowerShell (`pwsh`) or the older `cmd.exe`. We recommend PowerShell.

You will see a *prompt* — something like `fyq@Mbp ~ %` — followed by a blinking cursor.
That prompt is the shell asking "what next?".

> [!TIP]
> In the code blocks below, the `$` (or `%` on macOS zsh) at the start of a line is the
> **prompt**, not something you type. Only type what comes after it.

## How to find the terminal on your computer

- **macOS:** press `Cmd + Space` to open Spotlight, type `Terminal`, and press Enter.
  (Or use a nicer terminal such as iTerm2 or the one built into VS Code — see Chapter 4.)
- **Linux (Ubuntu/GNOME):** press `Ctrl + Alt + T`.
- **Windows:** install **Windows Terminal** from the Microsoft Store, then open
  **PowerShell**. Avoid the old `cmd.exe` — PowerShell understands more modern commands.

![TODO: Screenshot of opening the terminal — macOS Spotlight → Terminal, Windows Terminal → PowerShell, or Linux Ctrl+Alt+T → GNOME Terminal.](../assets/img/placeholder.svg)

## sudo and "run as administrator"

Some commands change system-level settings (installing software, editing protected files).
Those need elevated rights:

- **macOS / Linux:** prefix the command with `sudo` ("superuser do"). The first time,
  macOS/Linux asks for your password.
- **Windows:** right-click the terminal icon and choose **Run as administrator**, or use
  `Start-Process` in PowerShell.

> [!WARNING]
> Your **sudo password is usually your macOS/login password**. macOS deliberately shows
> nothing as you type — no dots, no asterisks. That is normal; just type and press Enter.

```bash
sudo whoami
# macOS/Linux: enter your login password when prompted
# prints "root" → you are now acting as the administrator
```

## Using `-h` / `--help`

Almost every command accepts *flags* that change its behavior. A **single dash** (`-`)
introduces a short flag (one letter); a **double dash** (`--`) introduces a long, readable
flag.

```bash
ls -la          # short flags: -l (long format) + -a (include hidden files)
python3 --help  # long flag: full help text
```

When stuck, append `-h` or `--help` to nearly any command to see its options.

```bash
ls -la
python3 -h
# zsh: command not found: python  →  we use python3 (see below)
```

## Why there is no `python` on macOS

On macOS, the command is `python3`, not `python`. Apple stopped shipping a plain `python`
command (it pointed to an ancient Python 2). So always use `python3`.

> [!NOTE]
> **Jump ahead:** See [Chapter 3 · Installing Python](installation.html) for how many
> Pythons live on a Mac and which one you should actually use. The `python3` you get by
> default may be Apple's, not the one you want for your projects.

## Difference between options and arguments

A command line has two kinds of inputs:

- **Options / flags** modify *how* the command runs (e.g. `-l`, `--help`). They usually
  start with `-` or `--`.
- **Arguments** are the *targets* the command acts on — file names, URLs, values.

```bash
cp -r project backup
#   └┬┘ └┬┘   └┬┘    └┬┘
#    │   │    │      └─ argument: destination
#    │   │    └──────── argument: source
#    │   └───────────── option: recursive
#    └───────────────── command
```

## What is an "executable"? (and why `python` is one)

An **executable** is simply a file the operating system knows how to *run directly* —
as a program, not as data to be opened in another program. When you type `python3` and
press Enter, you are asking the OS to launch the `python3` executable; it then reads
your script and executes it line by line.

So **Python itself is an executable** (`python.exe` on Windows, `python3` on macOS/Linux).
Your `.py` script is *not* an executable on its own — it is **data** that the Python
executable interprets. That is the key mental model:

```
python3  hello.py
│        │
│        └─ your script = DATA (text the interpreter reads)
└────────── the executable = PROGRAM (actually runs)
```

### How the OS knows a file is executable

Different systems use different signals:

- **Windows** decides by the file **extension** (`.exe`, `.msi`, …). Double-clicking
  `python.exe` runs it; renaming it to `python.txt` makes Windows treat it as text.
- **Unix-like systems** (macOS/Linux) decide by a **permission bit** (the file is marked
  *executable* with `chmod +x`) plus a **shebang** line (`#!/usr/bin/env python3`) at the
  top that tells the shell which interpreter to use. So Unix programs often have **no
  extension** at all.

This is why you run `python.exe` on Windows but just `python3` on macOS/Linux — and why
your own `.py` files need `python3` in front of them (unless you add a shebang and make
them executable, as seen in Chapter 3).

## PowerShell notes (Windows)

PowerShell ships convenience *aliases* that mimic Unix commands, but its native commands
are different (verb-noun cmdlets). We recommend PowerShell over `cmd.exe`.

```powershell
# PowerShell alias   ≈   Unix command
Get-Command          # ≈ which   (locate a command)
Get-ChildItem        # ≈ ls      (list files)
Get-Location         # ≈ pwd     (print working directory)
Set-Location         # ≈ cd      (change directory)
```

> [!TIP]
> In PowerShell, the path separator is `\` (back-slash) and environment variables use
> `$env:NAME` (e.g. `$env:PATH`) instead of Unix `$NAME`.

## Why Windows is less preferred (for this guide)

We recommend PowerShell over `cmd.exe`, but **Unix-like shells (bash/zsh) are still
preferred over Windows overall**, and here is the honest reason:

- **A different command grammar.** Windows uses verb-noun cmdlets (`Get-ChildItem`,
  `Set-Location`) while Unix uses short names (`ls`, `cd`). Most tutorials, Stack
  Overflow answers, and this guide's commands are written for Unix — on Windows you
  must mentally translate them.
- **The backslash tax.** Windows paths use `\`, which is an escape character in nearly
  every programming language, so you constantly fight `\\` or raw strings (see above).
  Unix's `/` just works everywhere, including inside Python.
- **Case-insensitive filesystem.** `Readme.md` and `readme.md` are the same file on
  Windows but different on macOS/Linux. This silently breaks imports and `git` diffs
  when code moves between systems.
- **Legacy split.** Two shells (`cmd.exe` and PowerShell), two path styles, and
  years of conflicting advice make Windows setups more error-prone for beginners.

None of this means Windows is "bad" — millions use it daily. It just means you will
meet more friction following Python tutorials written from a Unix point of view, so
expect to adapt commands rather than copy them verbatim.

## Path separators: `/` (slash) vs `\` (backslash)

A **path** tells the OS where a file lives. The character that separates folders
differs by system:

- **macOS / Linux** use the forward slash `/` — e.g. `/Users/fyq/hello.py`.
- **Windows** traditionally uses the backslash `\` — e.g. `C:\Users\fyq\hello.py`.

> [!WARNING]
> Inside most programming languages the backslash `\` is an **escape character** (it
> changes the meaning of the next character, e.g. `\n` = newline). So in Python you must
> either double it (`"C:\\Users\\fyq"`) or use a **raw string** (`r"C:\Users\fyq"`).
> Forward slashes have no such problem and are safer in code.

### In PowerShell you can use *either*

A nice surprise: **PowerShell accepts both `/` and `\`** when you type a path, and it
normalises them automatically. So these all work:

```powershell
cd C:\Users\fyq\Documents      # classic Windows backslash
cd C:/Users/fyq/Documents      # forward slash — also fine in pwsh
cd ~/Documents                 # ~ means your home folder
Get-ChildItem C:/Users/fyq/hello.py
```

On macOS/Linux the shell only understands `/`; a `\` there is an escaping character,
not a separator. So when you write cross-platform scripts or Python code, **prefer `/`**
everywhere.

## Tab completion

You rarely have to type a long path or command name in full. Press **Tab** and the
shell finishes it for you; press Tab again to cycle through multiple matches.

```bash
# Type a few letters of a file or command, then press Tab:
pyth<Tab>          # → expands to python3 (or python.exe on Windows)
cd ~/Doc<Tab>      # → expands to ~/Documents/
cd ~/Documents/pro<Tab>   # → expands to the matching file/folder
```

```powershell
# In PowerShell the same Tab key works:
cd ~/Doc<Tab>      # → ~/Documents/
Get-Command pyth<Tab>   # → fills in the matching command name
```

> [!TIP]
> If Tab does nothing, you may have typed a wrong starting letter — the shell only
> completes from what it can uniquely match. Tab is your best friend for avoiding
> typos in long paths.
