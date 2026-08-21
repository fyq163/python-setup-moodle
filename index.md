---
title: Python Setup Guide for HKU Beginners
tag: Home
---

## Why learn this when AI agents can code for you? 
An agent can *write* Python, but
it cannot *install* the interpreter on your machine, fix a broken `PATH`, or tell
you why `python` points to the wrong binary. When a script crashes, you still have
to run it, read the traceback, and rebuild the environment yourself — and you
cannot do any of that without a working setup. Learning this once means you are
never blocked just because a tool failed. 



## python version
We use **CPython** 3.14, the official
reference implementation of Python, rather than alternatives such as **PyPy**.
PyPy is a different implementation with a JIT compiler that can run some programs
much faster, but it is not the standard interpreter, may lag behind on new Python
features, and is rarely what courseware or libraries expect. CPython is what
`python.org` ships and what every tutorial in this guide assumes.


## How to use this guide: 
click a card below to jump to that chapter. Tags show
whether a chapter is required or can be skipped. You should **at least** see the 
[Installation page](https://python-install.quantinvest.qzz.io/pages/installation.html)
for required packages.