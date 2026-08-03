---
title: 4 · Code Editors & IDEs
tag: Required
---

Pick any editor and point it at the Python interpreter you created in Chapter 3. You
can also use the terminal skills from Chapter 1 inside the editor's built-in terminal.

## Visual Studio Code family (VS Code, Cursor, CodeBuddy, Trae…)

These editors share the same engine and the same **Python extension**, so the steps are
identical:

1. Install [VS Code](https://code.visualstudio.com/) (or Cursor / CodeBuddy / Trae).
2. Open the **Extensions** view (`Ctrl/Cmd + Shift + X`) and install **Python** (by
   Microsoft). This also installs the Pylance language server.
3. Open your project folder (**File → Open Folder**).
4. Select the interpreter: press `Ctrl/Cmd + Shift + P`, type **"Python: Select
   Interpreter"**, and choose the environment you made in Chapter 3 (the `.venv` or conda
   env). The bottom-right status bar then shows that Python.
5. Use the built-in terminal (`Ctrl/Cmd + `` `) to run `uv run main.py` or
   `python main.py`.

![TODO: Screenshot of VS Code — the "Python: Select Interpreter" picker, highlighting the virtual environment created in Chapter 3.](../assets/img/placeholder.svg)

> [!TIP]
> Once the interpreter is selected, the play button (▶) and the terminal both use *your*
> project's Python — not the system one. That is the whole point.

## PyCharm Community Edition

PyCharm is a Python-focused IDE with a free **Community** edition (the **Professional**
edition adds web/DB features and is paid, though free for students).

1. Download [PyCharm Community](https://www.jetbrains.com/pycharm/download/).
2. **New Project** → choose a location. Under "Python Interpreter", select **Previously
   configured interpreter** and point it at your `conda` env or the `python` inside
   `.venv/bin` (macOS/Linux) / `.venv\Scripts\python.exe` (Windows). Or let PyCharm create
   a new `venv` for you.
3. Right-click a `.py` file and choose **Run**.

References: [PyCharm + conda](https://www.anaconda.com/docs/getting-started/working-with-conda/ides/pycharm),
[Python path](https://www.anaconda.com/docs/getting-started/working-with-conda/ides/python-path)

## Other popular coding CLIs

A newer wave of editors runs **inside the terminal** — perfect if you liked Chapter 1:

- **opencode** — an open agentic coding CLI.
- **kilo** (within OpenCode) and **mimo** — terminal-based assistants.

They are just editors with an AI chat bolted on; everything from Chapter 1 (paths, `cd`,
running scripts) still applies. Launch them in your project folder and they use whatever
Python your shell currently has active.

## GitHub Copilot — student subscription

GitHub Copilot is an AI pair-programmer that suggests code as you type. **Students get it
free** (and many other developer tools) through the [GitHub Education](https://education.github.com/)
pack with a school email.

1. Register with your `.edu` / university email at GitHub Education.
2. In VS Code / JetBrains, install the **GitHub Copilot** extension and sign in.
3. Start typing — suggestions appear inline; press `Tab` to accept.

> [!TIP]
> **Tip:** With a school email you can often get GitHub Copilot (and other developer tools)
> for free via the GitHub Education pack. Even the editor used to write this guide
> (CodeBuddy) offers student access — check your faculty's software portal too.
