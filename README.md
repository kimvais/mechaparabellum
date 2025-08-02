# Mechaparabellum

Tools for [Mechabellum](https://store.steampowered.com/app/669330/Mechabellum/)

> [!WARNING]
> These tools are work-in-progress and documentation exists only for subset of commands. Use them at your own risk.

> [!TIP]
> You __MUST__ go to "Settings" -> "Other" and :white_check_markcheck: `Automatically save replays` _and_ at least periodically go 
> "Collection" -> "Combat record" in order for these tools to do anything useful.

## Installation
>[!NOTE]
> Make sure you have a modern python interpreter (there have only been tested with 3.12+) and `uv` installed

In Powershell:

1. `git clone git@github.com:kimvais/mechaparabellum.git`
2.  `cd mechaparabellum`
3. `uv -p 3.13 env `
4. `. .venv/Scripts/activate.ps1`
5. `uv pip install .`

## Features
- Replay parsing, try `python -m mechaparabellum.replay parse_all`
- Log parsing, try `python -m mechaparabellum.cli parse`
