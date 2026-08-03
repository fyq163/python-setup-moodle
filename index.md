---
title: Python Setup Guide for HKU Beginners
tag: Home
---

## Why learn this when AI agents can code for you?

AI coding assistants (Copilot, CodeBuddy, Cursor, etc.) are great at writing code, but
they are not a substitute for understanding *your environment*. Three reasons this guide
is still worth your time:

1. **You debug what the agent builds.** When a script fails ("module not found", "wrong
   Python version"), the fix is almost always about the environment — a missing package,
   a wrong interpreter, or a broken `PATH`. Knowing the basics lets you fix it in seconds
   instead of guessing.
2. **Reproducibility matters.** Courses, TAs, and collaborators expect a project that runs
   on *their* machine too. A clean, isolated Python setup is what makes "works on my
   machine" go away.
3. **The agent needs a correct target.** An assistant writes code *for* a Python
   interpreter you provide. If that interpreter is the system one, or the wrong version,
   the generated code may not run. You are the one who points the tool at the right Python.

> [!NOTE]
> **Implementation note:** This guide uses **CPython**, the reference implementation of
> Python maintained by the Python Software Foundation. We do **not** use PyPy here. CPython
> is what you get from python.org and what nearly every course, tutorial, and package
> assumes. (PyPy is an alternative implementation focused on speed via a JIT compiler; it
> is excellent for long-running programs but not what beginners need day to day.)

## How to use this guide

Each chapter is a separate page. Inside a chapter, use the left table of contents (on
desktop) or the page headings (on mobile) to navigate. At the bottom of every page you
will find **Previous / Next** links.

The chapter cards below (and the top navigation) link to each chapter. Tags show whether a
chapter is required or can be skipped:

- **Required** — do this before writing any code.
- **Optional / Skippable** — come back when you need it, or skip if you already know it.

Every page is rendered from a Markdown file. To experiment, edit a `.md` and reload — the
page updates with no build step.
