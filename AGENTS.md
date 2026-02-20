# AGENTS.md

## Project Map
- Primary notebook: `AnatomyLocked_Character_Studio.ipynb`
- Script mirror (auto-generated style): `anatomylocked_character_studio.py`
- Comfy workflows: `OtherSetups/phase1_exploration.json`, `OtherSetups/phase2_identity_lock.json`
- Setup/docs: `README.md`, `OtherSetups/models_and_setup.md`
- Assets: `assets/controlnet/*`
- Validation templates: `Character_Validation_History_Template.json`, `Character_Set_Validation_Checklist.md`

## Current Implementation Coverage
- Implemented end-to-end in notebook/script:
  - Section 1: environment + dependencies
  - Section 2: model/control stack selection and pipeline wiring
  - Section 3: exploration generation + candidate outputs
  - Section 4: candidate promotion into character directory
  - Section 5: identity lock core (schema, fingerprints, invariant masks, validation)
- Placeholder/spec only (not implemented yet):
  - Sections 6 through 17

## Canonical Data Locations
- Canonical character state:
  - `AI_DIRS["datasets"] / "characters" / <character_id> / "character.json"`
- Section 5 identity files:
  - `.../identity/reference/*`
  - `.../identity/masks/*`
- `Character_Validation_History_Template.json` is non-canonical and optional for reporting/history.

## Notebook-to-Script Sync Rules
- Notebook is the source of truth for feature development.
- `anatomylocked_character_studio.py` must mirror notebook logic after each functional change.
- Keep callable names and signatures aligned between notebook and script.
- Do not ship notebook-only behavior that is absent in script.

## Comfy Workflow Coverage and Gaps
- Current Comfy coverage:
  - Phase 1 exploration
  - Phase 2 identity + pose guidance with IP-Adapter + ControlNet
- Gap:
  - Comfy does not yet implement notebook Section 5 lock schema/validation pipeline.
- Decision:
  - Comfy translation starts after notebook Sections 5-8 are stable.

## Section-by-Section Status (1-17)
- 1: Implemented
- 2: Implemented
- 3: Implemented
- 4: Implemented
- 5: Implemented (core lock)
- 6: Planned
- 7: Planned
- 8: Planned
- 9: Planned
- 10: Planned
- 11: Planned
- 12: Planned
- 13: Planned
- 14: Planned
- 15: Planned
- 16: Planned
- 17: Planned

## Active Decisions and Defaults
- Notebook-first implementation flow.
- Canonical lock record stored per character in `character.json`.
- Section 5 fingerprint fallback chain:
  - `insightface` -> `clip` -> `phash` (dhash fallback if imagehash unavailable)
- Section 5 defaults:
  - `require_face_detection = False`
  - `fail_on_missing_mask = True`
  - thresholds:
    - InsightFace centroid >= 0.35
    - InsightFace best ref >= 0.45
    - CLIP centroid >= 0.82
    - CLIP best ref >= 0.86
    - pHash hamming <= 10

## Known Risks and Technical Debt
- InsightFace/CLIP dependency availability varies by runtime; fallback behavior must be monitored.
- Notebook and script are duplicated surfaces and can drift if not synchronized carefully.
- Sections 6-17 are still spec-only and can constrain future data model changes.
- Large JSON notebook diffs are noisy; edits should stay localized where possible.

## Next Priority Queue
1. Implement Section 6 (body region map schema + mask storage).
2. Implement Section 7 (regional refinement pipeline and lock interactions).
3. Implement Section 8 (canonical finalization and freeze semantics).
4. Design Comfy parity plan for Sections 5-8 once notebook flow stabilizes.

## Working Notes (Append-only)
- 2026-02-20:
  - Added Section 5 core implementation in notebook/script:
    - `load_character_record`
    - `save_character_record`
    - `create_identity_lock`
    - `validate_identity_lock`
  - Added identity fingerprint backends with fallback and invariant mask validation.
  - Kept Comfy unchanged by design; translation deferred until Sections 5-8 stabilize.
