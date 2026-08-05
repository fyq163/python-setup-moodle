---
title: 5 · Recommended Reading
tag: Optional
---

A short, non-compulsory list to write cleaner Python and get editor features like
autocomplete and live error checking. All of these plug into the editors from Chapter 4.

## PEP 8 — Style Guide for Python Code

[PEP 8](https://peps.python.org/pep-0008/) is the official style convention for Python. You
do not need to memorize it — your editor can enforce it — but know the big ones:

- **Indent with 4 spaces** (never tabs).
- **Max line length 79** characters for code (99 is tolerated).
- **Naming:** `lowercase_with_underscores` for functions/variables,
  `CapitalizedWords` for classes, `UPPER_CASE` for constants.
- **Two blank lines** between top-level definitions; **one** between methods.

Reading it once makes your code readable to TAs and teammates — and to the AI agents.

## Language servers: `ty` and `pyright`

A **Language Server Protocol (LSP)** tool runs in the background and gives your editor
"brains": red squiggles for errors, hover docs, jump-to-definition, and safe rename.

- **pyright** — Microsoft's type checker for Python; fast, mature, the default in VS Code's
  Python extension (via Pylance).
- **ty** — Astral's (the uv makers) new type checker written in Rust; aims to be even
  faster. Still young, but worth watching.

Enable in your editor: install the **Python** extension (pyright/ty come along), or run
the checker from the terminal:

```bash
uv pip install pyright
pyright .            # type-check the project
```

## Linters: `ruff`

[ruff](https://docs.astral.sh/ruff/) is an extremely fast all-in-one **linter and
formatter** (it replaces `flake8`, `black`, `isort`, and more in one tool). One command
cleans and formats your code:

```bash
uv pip install ruff
ruff check .          # lint: report style/bug issues
ruff check --fix .    # lint + auto-fix what it can
ruff format .         # format: rewrite files to a consistent style
```

Drop a `ruff.toml` in your project to configure rules. Most teams adopt ruff because it
runs in milliseconds even on large codebases.

> 💡
> **Workflow:** write code → `ruff format .` → `ruff check .` → `uv run main.py`. Your
> editor shows the same warnings live if you enable the Ruff extension.
