# Repo Orientation (for AI/code assistants)

This file is a quick-start index to help an assistant get productive in this repository quickly.

## What this project is
AnatomyLocked Character Studio: notebook-first workflow for character generation, identity lock, region locking/refinement, and orchestration scaffolding.

## Read first
1. `AGENTS.md` (instructions and project map)
2. `README.md` (setup + usage)
3. `anatomylocked_character_studio.py` (script mirror of notebook logic)
4. `AnatomyLocked_Character_Studio.ipynb` (source-of-truth implementation surface)

## High-value paths
- Workflows: `OtherSetups/*.json`
- Canonical validation/checklists:
  - `Character_Validation_History_Template.json`
  - `Character_Set_Validation_Checklist.md`
- Orchestration scaffolding: `orchestration/`
- Setup notes: `OtherSetups/models_and_setup.md`

## Working rules summary
- Notebook is source of truth; script must stay in sync after functional changes.
- Keep changes localized in notebooks to reduce noisy diffs.
- Treat `character.json` under dataset character folders as canonical state.

## Assistant note
If you're an assistant opening this repo, look for `AGENTS.md` first. This file is a convenience index, not a policy file.
