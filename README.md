# Terminal Strategy Game

A turn-based terminal strategy game written in Python by a team of four students.

## Current status

Phase 1 is complete: the project structure and Python package layout are in place.
Game behavior will be added incrementally in later phases.

## Setup

Create and activate a virtual environment, then install the development dependency:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run

```bash
python main.py
```

## Test

```bash
python -m pytest
```

## Planned architecture

- `game/`: game engine, map, players, resources, and save/load support
- `units/`: base unit and specialized unit types
- `ai/`: rule-based AI opponent
- `tests/`: automated tests for each major component
- `saves/`: JSON campaign save files

## Team branches

- `feature/game-engine`
- `feature/map-resources`
- `feature/units-combat`
- `feature/ai-save-load`