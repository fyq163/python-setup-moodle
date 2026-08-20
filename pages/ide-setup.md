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
   ![vscode plugin marketplace](https://pub-639e92bd227c4441a00a10db2a268512.r2.dev/image/GitHub-pages/python-install/vscode-extension-python.png)
5. Use the built-in terminal (`Ctrl/Cmd + `` `) to run `uv run main.py` or
   `python main.py`.
![Screenshot of VS Code — the "Python: Select Interpreter" picker, highlighting the virtual environment created in Chapter 3.](https://pub-639e92bd227c4441a00a10db2a268512.r2.dev/image/GitHub-pages/python-install/vscode-interpreter-selection.png)

> 💡
> Once the interpreter is selected, the play button (▶) and the terminal both use *your*
> project's Python — not the system one. That is the whole point.

## PyCharm

> ❗
> Since 2025, JetBrains has **merged the Community and Professional editions** of PyCharm
> into a single product. The **basic features are free to use**; the **advanced features
> require a paid subscription**. As a student, you can get that subscription for free via
> the [JetBrains Student Pack](https://www.jetbrains.com/academy/student-pack/) — sign in
> with your school email and the advanced features unlock at no cost.

PyCharm is a Python-focused IDE. The **basic features** (editing, running, debugging Python)
are free; the **advanced features** (web frameworks, database tools, etc.) need a
subscription, which students get free with the Student Pack above.

1. Download [PyCharm](https://www.jetbrains.com/pycharm/download/).
2. **New Project** → choose a location. Under "Python Interpreter", select **Previously
   configured interpreter** and point it at your `conda` env or the `python` inside
   `.venv/bin` (macOS/Linux) / `.venv\Scripts\python.exe` (Windows). Or let PyCharm create
   a new `venv` for you.
3. Right-click a `.py` file and choose **Run**.
- ![PyCharm change interpreter](https://pub-639e92bd227c4441a00a10db2a268512.r2.dev/image/GitHub-pages/python-install/pycharm-interpreter-selection.png)
References: [PyCharm + conda](https://www.anaconda.com/docs/getting-started/working-with-conda/ides/pycharm),
[Python path](https://www.anaconda.com/docs/getting-started/working-with-conda/ides/python-path)

## GitHub Copilot — university subscription

GitHub Copilot is an AI pair-programmer that suggests code as you type. **Students get it
free** (and many other developer tools) through the [GitHub Copilot - Information Technology Services - HKU](https://its.hku.hk/software/github-copilot/)

## OpenCode and other terminal coding CLIs

OpenCode is the AI coding agent used in the bootcamp. Install it from
<https://opencode.ai/> and **connect it to your environment** — no command-line setup is
needed here. (It is independent of the Python stack.)

> 💡 opencode, kilo, mimo and similar run **inside the terminal** — everything from
> Chapter 1 (paths, `cd`, running scripts) still applies. Launch them in your project
> folder and they use whatever Python your shell currently has active.
