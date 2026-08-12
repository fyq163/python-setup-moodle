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

You will see a *prompt* — something like `you@Mbp ~ %` — followed by a blinking cursor.
That prompt is the shell asking "what next?".

> 💡
> In the code blocks below, the `$` (or `%` on macOS zsh) at the start of a line is the
> **prompt**, not something you type. Only type what comes after it.

## How to find the terminal on your computer

- **macOS:** press `Cmd + Space` to open Spotlight, type `Terminal`, and press Enter.
  (Or use a nicer terminal such as iTerm2 or the one built into VS Code — see Chapter 4.)
- **Linux (Ubuntu/GNOME):** press `Ctrl + Alt + T`.
- **Windows:** install **Windows Terminal** from the Microsoft Store, then open
  **PowerShell**. Avoid the old `cmd.exe` — PowerShell understands more modern commands.
- how to find cmd.exe:![cmd.exe from windows start menu](https://pub-639e92bd227c4441a00a10db2a268512.r2.dev/image/GitHub-pages/python-install/windows-cmd.PNG)
- how to find powershell: ![Windows Terminal → PowerShell(DONE), or Linux Ctrl+Alt+T → GNOME Terminal.](https://pub-639e92bd227c4441a00a10db2a268512.r2.dev/image/GitHub-pages/python-install/windows-terminal.PNG)

## sudo and "run as administrator"

Some commands change system-level settings (installing software, editing protected files).
Those need elevated rights:

- **macOS / Linux:** prefix the command with `sudo` ("superuser do"). The first time,
  macOS/Linux asks for your password.
- **Windows:** right-click the terminal icon and choose **Run as administrator**, or use
  `Start-Process` in PowerShell.

> ⚠️
> Your **sudo password is usually your macOS/login password**. macOS deliberately shows
> nothing as you type — no dots, no asterisks. That is normal; just type and press Enter.

<details>
<summary>⚠️ Use <code>sudo</code> with caution — it can damage your computer</summary>

`sudo` grants full administrator (root) power, so a typo or a wrong command can
delete system files, break the operating system, or lock you out of your machine.
Before pressing Enter on a `sudo` command:

1. Make sure you understand what it does — if you copy-pasted it from the internet,
   know exactly why each part is there.
2. Never run `sudo` on a command you don't recognise, especially ones using `rm`,
   `dd`, or wildcards like `*` on system folders.
3. Prefer `sudo` for the single command you need, not for opening a long-lived root
   shell (`sudo -i` / `sudo su`).

For this guide's Python setup you will rarely need `sudo` at all — virtual
environments and `uv` install things into your own home folder, not system-wide.

</details>

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

<details>
<summary>Why there is no <code>python</code> on macOS？</summary>

On macOS, the command is `python3`, not `python`. Apple stopped shipping a plain `python`
command (it pointed to an ancient Python 2). So always use `python3`.

📝 **Jump ahead:** See [Chapter 3 · Installing Python](installation.html) for how many
Pythons live on a Mac and which one you should actually use. The `python3` you get by
default may be Apple's, not the one you want for your projects.

</details>

## Difference between options and arguments

A command line has two kinds of inputs:

- **Options / flags** modify *how* the command runs (e.g. `-l`, `--help`). They usually
  start with `-` or `--`.
- **Arguments** are the *targets* the command acts on — file names, URLs, values.

```bash
  cp -r project backup
#└┬┘ └┬┘  └┬┘    └┬┘
# │   │    │      └─ argument: destination
# │   │    └──────── argument: source
# │   └───────────── option: recursive
# └───────────────── command
```

## How the shell finds a command: the `PATH`

When you type `python3` and press Enter, the shell does **not** magically know what
`python3` means. It is really just a *name*. The shell asks the operating system:
"where is the program called `python3`?" — and the OS answers by searching a list
of folders called the **`PATH`**.

`PATH` is an **environment variable**: a colon-separated (`:`) list of directories
on Unix/macOS, or semicolon-separated (`;`) on Windows. Think of it as a set of
"places to look". To find a command, the system walks the list **in order** and
opens the first folder that contains a matching executable.

```
$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/Users/you/.local/bin
                 │        │      │                 └─ searched last
                 └────────┴──────┘─ searched first → first match wins
```

So `python3` is actually: *the system takes the name `python3` and looks through
every folder in `PATH` until it finds a file with that name it can run.* The first
match wins — which is why, if you have several Pythons installed, **the one found
earliest in `PATH` is the one that runs**.
- Unix:
```bash
# Show the folders your shell searches, in order:
echo $PATH                 # macOS / Linux
which python3              # macOS / Linux  → prints e.g. /usr/local/bin/python3
```
- Windows:
```bash
$env:PATH                  # Windows (PowerShell)
Get-Command python3        # Windows (PowerShell)
```

> [!TIP]
> This is also why a freshly installed Python sometimes **"doesn't work"** until you
> **reopen** the terminal: installing it adds its folder to `PATH`, but already-open
> shells loaded the old `PATH`. Close and reopen the terminal (or run the installer's
> "add to PATH" step) so the new folder is included. We return to this in
> [Chapter 3 · Installing Python](installation.html).

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

<details>
<summary>How the OS knows a file is executable</summary>

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
</details>

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

> 💡
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

- **macOS / Linux** use the forward slash `/` — e.g. `/Users/you/hello.py`.
- **Windows** traditionally uses the backslash `\` — e.g. `C:\Users\you\hello.py`.

> ⚠️
> Inside most programming languages the backslash `\` is an **escape character** (it
> changes the meaning of the next character, e.g. `\n` = newline). So in Python you must
> either double it (`"C:\\Users\\you"`) or use a **raw string** (`r"C:\Users\you"`).
> Forward slashes have no such problem and are safer in code.

### In PowerShell you can use *either*

**A nice surprise**: PowerShell accepts **both `/` and `\`** when you type a path, and it
normalises them automatically. So these all work:

```powershell
cd C:\Users\you\Documents      # classic Windows backslash
cd C:/Users/you/Documents      # forward slash — also fine in pwsh
cd ~/Documents                 # ~ means your home folder
Get-ChildItem C:/Users/you/hello.py
```

On macOS/Linux the shell only understands `/`; a `\` there is an escaping character,
not a separator. So when you write cross-platform scripts or Python code, **prefer `/`**
everywhere.

## Users and the home folder (`~`)

You may have noticed paths like `C:\Users\you\hello.py` (Windows) or
`/Users/you/hello.py` (macOS). That `you` is a **username** — every person who
logs into a computer gets their own account, and each account has its own private
space on disk.

### What does `<you>` mean in `C:\Users\<you>`?

In tutorials you will often see a placeholder like `C:\Users\<you>` or
`/home/<you>`. The `<you>` is **not literal text you type** — it is a stand-in
for *your own* username on the machine. Replace it with whatever name you used
when you set up the computer.

- On **Windows**, your user folder is `C:\Users\YourName`. If your account is
  named `alice`, your real path is `C:\Users\alice` — not `C:\Users\<you>`.
- On **macOS**, it is `/Users/YourName` (e.g. `/Users/you`).
- On **Linux**, it is `/home/YourName` (e.g. `/home/you`).

The angle brackets `< >` are a common notation meaning "fill in your own value
here". Whenever you copy a command, swap `<you>` for your actual username.

### `whoami` — ask "who am I right now?"

The `whoami` command prints the username of the account you are currently logged
into the shell as. It is handy when you are unsure whose home folder a path
refers to.

```bash
# macOS / Linux (bash, zsh):
whoami
# prints e.g. "you"  → that is the name that replaces <you> above
```

```bash
# Windows (PowerShell):
whoami
# prints e.g. "desktop-abc\alice"  → the part after "\" is your username,
# or use the shorter form:
$env:USERNAME
# prints just "alice"
```

> 📝
> **A small difference between systems.** On macOS/Linux, `whoami` returns just
> the short username (`you`). On Windows, the plain `whoami` command returns the
> **full account name including the machine/domain prefix** (e.g.
> `DESKTOP-ABC\alice`), because Windows accounts live inside a "domain". If you
> only want the bare username on Windows, use `$env:USERNAME` instead — it
> behaves like the Unix `whoami`.

### What is `~` (tilde)?

`~` is a **shortcut for your home folder** — the private directory the OS creates
for your account. Instead of typing the full `/Users/you` or
`C:\Users\you` every time, you can write `~` and the shell expands it.

- On macOS/Linux: `~` = `/Users/you`
- On Windows (PowerShell): `~` = `C:\Users\you`

```bash
cd ~              # go straight to your home folder
cd ~/Documents    # go to Documents inside your home folder
echo ~            # print the full path your ~ resolves to
```

```powershell
cd ~              # PowerShell also understands ~ as your home folder
cd ~/Documents
```

So `<you>` in `C:\Users\<you>` is just "your username", and `~` is the fast way
to refer to `C:\Users\<you>` (or `/Users/<you>`) without writing it out.

### Tab completion

You rarely have to type a long path or command name in full. Press **Tab** and the
shell finishes it for you; press Tab again to cycle through multiple matches.

Here is a real session in a project folder (the `<you>` part is your username, as
explained earlier — see *Users and the home folder (`~`)*):

```bash
# <you> at Mbp.lan in ~/PycharmProjects/python-setup-moodle on git:main x [11:17:03]
$ ls
AGENTS.md        assets           azure-api-key.py css              index.html       index.md         pages            readme.md        serve.py

# <you> at Mbp.lan in ~/PycharmProjects/python-setup-moodle on git:main x [11:17:04]
$ vim AGENT<Tab>
# → shell auto-completes to: vim AGENTS.md

# <you> at Mbp.lan in ~/PycharmProjects/python-setup-moodle on git:main x [11:17:29]
$ vim AGENTS.md
# → opens the file; no need to type the rest of the name by hand
```

```powershell
# In PowerShell the same Tab key works:
cd ~/Doc<Tab>      # → ~/Documents/
Get-Command pyth<Tab>   # → fills in the matching command name
```

> 💡
> If Tab does nothing, you may have typed a wrong starting letter — the shell only
> completes from what it can uniquely match. Tab is your best friend for avoiding
> typos in long paths.
