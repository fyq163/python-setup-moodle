---
target: python-beginner installation guide
target-audience: new entrance post-graduate students with mixed background
target-Language: English
target-platform: arm64-macos, amd64-windows, x86_64-linux
---
# python-beginner installation guide
This repo serves as tutorial for beginners to learn how to use install a python environment and use it to learn simple python lession.

## what will be covered:
1. basic unix-alike system introduction, path, command line (bash, zsh)
2. basic python distribution and installation on different system, virtual environment etc
3. how to run codes
4. how to what to put in place of --config 
## development phase
- phase1: in html format, pure html for github page and paste to html previewer
- phase2: tutorials in markdown format, with code snippets
## your work step
- [X] plan for structure, ready to distribute github page
- [X] write first part
- [ ] write second part
- [ ] write third part

## how to write this repo
### welcome page
show welcome to hku students, and give a brief introduction to the repo.
To better facilitate programming bootcamp students, we will provide a series of tutorials to help them learn how to install python on their pc and use it to learn simple python lessons. 
There are secions that can be skipped for those who have already learned the basics of programming. e.g. basic unix-alike system introduction.
And why it's necessary to learn this while agents can do it for you. Also mention difference with pypy and cpython and state we use cpython

(index table with hyperlink)

### basic unix-alike system introduction (very basic )
- (very short) what is command line, bash for linux, zsh for macos, recommand pwsh for windows, hot to find them on computer; how to invoke 
- sudo and run as administrator, sudo password is usually your macos login password
- (short) useage of `-h`,`--help`, with example of (very short) difference of `-` and `--`
```
# fyq at Mbp.lan in ~/.pi [11:06:42]
$ ls -la

# fyq at Mbp.lan in ~/.pi [11:38:03]
$ python -h                    
zsh: command not found: python

# fyq at Mbp.lan in ~/.pi [11:38:15]
$ python3 -h
usage: /Applications/Xcode.app/Contents/Developer/usr/bin/python3 [option] ... [-c cmd | -m mod | file | -] [arg] ...
Options and arguments (and corresponding environment variables):
```
- why there is no `python` on macos (with link jump to how many pythons are there on macos)
- difference of Options and arguments
- why executables on windows has `exe` extension and why unix does not have
- pwsh commands: unix-like aliases and its original commands and why windows is not prefered. e.g. `Get-Command` = `which`
### (short, non-compulsory)concept of virtual enviroment
- why need virtual env rather than standalone python, why uv is prefered. why /usr/bin/python3 cannot be used directly
- uv
- conda:https://www.anaconda.com/docs/getting-started/concepts/anaconda-or-miniconda
- anaconda 
- miniconda, difference of channels, conda-forge and others
- difference of `conda` and `uv`, `conda activate` vs `source .venv/bin/activate`, global vs local enviroment
### (very detail) How to installation python executable
- how to choose version (amd64, arm64, x86_64, exe) and how to set up first python enviroment
- standalone installation, double click exe to install
    - win: 
        - https://www.python.org/downloads/windows/
        - typecially it will be installed under the path of 
    - macos: 
        - with standalone installer, is should be need to add path mannually?: https://www.python.org/downloads/macos/
        - with brew: `brew install python@3.12`
        - typecially it will be installed under the path of 
    - linux:
        - with apt/yum/pacman: `apt install python`?
        - with standalone installer:https://www.python.org/downloads/source/
        - typecially it will be installed under the path of 
    
- with conda:
    - url: 
        - macos:https://www.anaconda.com/docs/getting-started/miniconda/install/mac-cli-install#using-miniconda-in-a-commercial-setting
        - windows:https://www.anaconda.com/docs/getting-started/miniconda/install/windows-cli-install#powershell
        - linux:https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install#installation-steps
    - how to install
        - introduce cli reference`conda create --name py310 python=3.12`
        - `conda activate <enviroment name>` condaand how to re-activate after close terminal
        - how to set specific pre-installed python executable for new env to save space
- with uv:
    - url: https://docs.astral.sh/uv/getting-started/installation/#pypi
    - how to install
        - curl, brew, winget (from url)
        - `uv install python`
        - `uv init` ,`uv pip install pandas`, and `uv run` and how to re-activate after close terminal
        - how to set specific pre-installed python executable for new env to save space
#### after install, test if it works
copy this command to your terminal and run it
```sh
python3 -c "import sys; print(sys.executable)"
```
it might return `/Applications/Xcode.app/Contents/Developer/usr/bin/python3` which differs from what you have installed, explain why and how to fix it. might be path issue.
#### how to debug
1. find the correct executable path
2. put into .zshrc or activate virtual env

### (short) code editor/IDE and how to configure 
- https://www.anaconda.com/docs/getting-started/working-with-conda/ides/pycharm#creating-a-new-conda-environment-from-a-pycharm-project
- https://www.anaconda.com/docs/getting-started/working-with-conda/ides/vscode
- https://www.anaconda.com/docs/getting-started/working-with-conda/ides/python-path
#### visual studio code series (vscode, cursor, codebuddy, trae etc)
#### pycharm community version
#### other poular coding cli
how to use can refer to command line part above 
- github copilot, student subscription:
- opencode series: opencode, kilo, mimo
### (very short; non-compulsory) recommand reading section
#### pep8
#### lsp: ty, pyright
#### lint tools: ruff

# Design.md
- commands should be seperated per system type, should be ready to paste and execute
- so the code block should not have copyable `$` which will mislead the reader
- 
