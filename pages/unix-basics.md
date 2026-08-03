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

## Why executables on Windows have an `.exe` extension

- **Windows** decides a file is a program by its **extension** (`.exe`, `.msi`, …). Double
  clicking `python.exe` runs it; renaming it loses that hint.
- **Unix-like systems** (macOS/Linux) decide by a **permission bit** (the file is marked
  *executable*) plus a **shebang** line (`#!/usr/bin/env python3`) at the top that tells
  the shell which interpreter to use. So Unix files often have **no extension** at all.

This is why you run `python.exe` on Windows but just `python3` on macOS/Linux.

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
