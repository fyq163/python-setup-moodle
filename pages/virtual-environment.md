---
title: 2 · Virtual Environments
tag: Optional
---

A short, non-compulsory concept chapter. Understanding this now saves real pain later, when
two projects need *different* versions of the same package.

## Why you need a virtual environment

A Python **environment** is a private, isolated copy of the interpreter plus its installed
packages. Without one, every package you install lands in a single global location, and
versions collide:

- Project A needs `pandas 1.x`; Project B needs `pandas 2.x` → one of them breaks.
- You install packages into the **system Python** (`/usr/bin/python3` on macOS/Linux), which
  the operating system itself relies on. Upgrading or removing something there can break
  system tools.

A virtual environment keeps each project's dependencies in its own folder, so projects
never step on each other — and never touch the system Python.

> ⚠️
> On macOS/Linux, `/usr/bin/python3` is managed by the system. Installing packages into it
> with `sudo pip install …` can break OS tools. **Always work inside a project environment.**

## uv

**[uv](https://docs.astral.sh/uv/)** is a modern, extremely fast Python package and
environment manager written in Rust. It replaces `pip`, `virtualenv`, and parts of
`conda`. We recommend it for beginners because:

- One tool does everything (install Python, create envs, install packages, run scripts).
- It is 10–100× faster than `pip`.
- Environments are created in a local `.venv` folder — no global state to manage.

```bash
uv init myproject      # create a new project with a .venv
cd myproject
uv pip install pandas  # install a package into this project's env
uv run main.py         # run a script using this project's Python
```

## Locking & recording dependencies: `uv lock` and `requirements.txt`

Installing packages is only half the story. To make your project **reproducible** —
so someone else (or future you) can rebuild the exact same environment — you record
what you installed.

### `requirements.txt` (the classic, pip-style list)

A plain text file listing every package (and version) your project needs:

```text
pandas==2.2.2
numpy>=1.26.0
requests
```

- Generate it from your current env with pip/uv:

```bash
uv pip freeze > requirements.txt     # uv
pip freeze    > requirements.txt     # plain pip
```

- Rebuild an env from it on another machine:

```bash
uv pip install -r requirements.txt
```

The catch: `requirements.txt` only pins *top-level* packages. If `pandas` silently
pulls in a specific `numpy`, that sub-dependency version is **not fixed** — two people
can end up with different environments.

### `uv lock` (the modern, exact solution)

`uv` goes further with a **lockfile** — `uv.lock` — that pins **every** package,
including all transitive dependencies, to exact versions and hashes:

```bash
uv add pandas          # adds pandas AND writes/updates uv.lock + pyproject.toml
uv lock                # (re)resolve and write uv.lock without installing
uv sync                # install exactly what uv.lock specifies
```

`uv.lock` guarantees that everyone who runs `uv sync` gets a byte-for-byte identical
set of packages. Think of it as `requirements.txt` on steroids.

| | `requirements.txt` | `uv.lock` |
| --- | --- | --- |
| Pins top-level packages | Yes (if you use `==`) | Yes |
| Pins transitive deps | No | Yes — exact versions + hashes |
| Human-readable | Yes | Machine-generated (don't edit by hand) |
| Tool | pip / uv | uv only |

> 💡
> For coursework, `requirements.txt` is enough and easier to read. Once a project
> matters (a real app, a paper's analysis), switch to `uv.lock` so results stay
> reproducible. Either way, **keep the file alongside your project** so the environment
> travels with your code.

## conda / Anaconda / Miniconda

**conda** is an older, very popular environment manager, especially in data science. The
naming is confusing, so here is the split:

- **Anaconda** — the full distribution: conda plus 250+ pre-installed packages. Large
  (~3 GB). Good if you want everything out of the box.
- **Miniconda** — conda with *no* pre-installed packages. Small and clean. **We recommend
  Miniconda** if you go the conda route.
- **conda-forge** — a community channel (see below) of packages; usually more up to date
  than the default `defaults` channel.

Unlike uv/pip, conda can also install **non-Python** dependencies (e.g. CUDA, R), which is
why many scientists like it.

```bash
conda create --name py312 python=3.12   # create a named environment
conda activate py312                     # switch into it
```

## Channels: conda-forge and others

A **channel** is a repository conda downloads packages from. The two you will meet:

- `defaults` — Anaconda's official, curated channel.
- `conda-forge` — a community-run channel with broader, faster-updated packages.

We recommend preferring conda-forge:

```bash
conda create -n py312 python=3.12 -c conda-forge
```

This differs from **PyPI** (the Python Package Index), which is what `pip` and `uv` use.
conda packages and PyPI packages are not always interchangeable — generally, *inside* an
environment, prefer `uv pip`/`pip` for Python packages and let conda handle only what it
does best.

## `conda` vs `uv`: global vs local

A quick comparison to help you choose.

| Topic | conda (Miniconda) | uv |
| --- | --- | --- |
| Environment scope | **global** — named envs stored in one place (`~/miniconda3/envs`) | **local** — a `.venv` folder inside each project |
| Activate command | `conda activate <name>` | `source .venv/bin/activate` (macOS/Linux) / `.venv\Scripts\activate` (Windows) |
| Re-activate after restart | `conda activate <name>` again (env still exists globally) | `source .venv/bin/activate` again — or just `uv run` (no activate needed) |
| Non-Python deps | Yes (CUDA, R, …) | No (Python only) |
| Speed | Slower | Very fast |
| Best for | Data-science stacks needing system libs | Everyday Python projects |

> 💡
> Our default recommendation: **uv**. Create one `.venv` per project, and use `uv run`
> so you rarely have to activate manually. Switch to conda only if a package you need
> ships non-Python system libraries.
