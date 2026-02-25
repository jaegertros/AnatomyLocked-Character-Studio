# CLAUDE.md

## Project Summary

AnatomyLocked Character Studio is a Colab-based pipeline for producing anatomy-accurate, identity-locked human reference images. It is not a random image generator — once a character is finalized, identity must remain stable across all renders.

## Repository Layout

```
AnatomyLocked_Character_Studio.ipynb   # Primary notebook (source of truth)
anatomylocked_character_studio.py      # Script mirror (must stay in sync with notebook)
orchestration/                         # ComfyUI pipeline orchestration layer
  pipeline_orchestrator.py             #   API client, state store, stage wrappers
  __init__.py
OtherSetups/                           # ComfyUI workflow JSONs and setup docs
  phase1_exploration.json
  phase2_identity_lock.json
  phase3_regional_refinement_inpaint.json
  phase4_canonical_finalization.json
  phase5_reference_variants.json
  section10_reference_views.json
  models_and_setup.md
  workflow_suite.md
assets/controlnet/                     # ControlNet reference assets
Character_Set_Validation_Checklist.md  # Manual validation template
Character_Validation_History_Template.json
```

## Key Conventions

### Notebook-first development
- The notebook (`AnatomyLocked_Character_Studio.ipynb`) is the source of truth.
- `anatomylocked_character_studio.py` mirrors notebook logic and must be updated after every functional change.
- Callable names and signatures must match between notebook and script. Never ship notebook-only behavior.

### Section-based architecture
- The pipeline is divided into numbered sections (1-17). Each section has its own constants, state schema, and API functions.
- Constants follow the pattern `SECTION<N>_*` (e.g., `SECTION9_GATE_PASS`, `SECTION12_SCHEMA_VERSION`).
- Each section's state is stored as an append-only block inside `character.json` under the character directory.

### Phase-to-section mapping (ComfyUI workflows)
- Phase 1 = Section 3 (exploration)
- Phase 2 = Section 5 (identity lock)
- Phase 3 = Section 7 (regional refinement)
- Phase 4 = Section 8 (canonical finalization)
- Phase 5 = Section 10 (lighting/camera reference views)

### Canonical data locations
- Character state: `datasets/characters/<character_id>/character.json`
- Identity files: `.../identity/reference/*`, `.../identity/masks/*`
- Region masks: `.../identity/masks/regions/`

## Implementation Status

- **Sections 1-7**: Fully implemented in notebook and script
- **Sections 8-12**: Implemented (canonical finalization, pose deformation, reference views, export, save/reload)
- **Sections 13-17**: Planned / spec only

## Coding Style

- Python, snake_case for functions and variables
- Type hints on function signatures (e.g., `def foo(character_id: str) -> dict:`)
- Functions are prefixed with `_` for internal/private helpers
- Section-scoped constants at module level: `SECTION<N>_CONSTANT_NAME`
- Gate statuses: `"PASS"`, `"PASS_WITH_WARNINGS"`, `"FAIL"`
- Timestamps use `_utc_now_iso()` (ISO 8601 UTC)
- File hashes use SHA-256 via `_sha256_file()`
- Minimal comments — only for non-obvious logic

## Identity Rules (Domain-critical)

### Must never change
- Bone structure, facial geometry, body proportions
- Permanent skin features (freckles, moles, scars, birthmarks) and exact placement

### Allowed to vary
- Pose, posture, muscle flexion/compression, skin folds from movement
- Hair style (root pattern stays unless explicitly changed)
- Makeup, nail color, lighting, camera angle, optional clothing

### Forbidden
- Face drift, proportion changes, feature relocation
- Anatomy exaggeration or stylization that breaks realism

## Identity Lock Pipeline

- Fingerprint backend fallback order: `insightface` -> `clip` -> `phash` (dhash fallback)
- Defaults: `require_face_detection = False`, `fail_on_missing_mask = True`
- Thresholds: InsightFace centroid >= 0.35, best ref >= 0.45; CLIP centroid >= 0.82, best ref >= 0.86; pHash hamming <= 10

## Gate Policy Pattern

Sections use a standardized multi-gate validation pattern:
- Gate A (hard fail): identity lock pass required
- Gate B (hard fail): all required regions/stages processed
- Gate C (configurable): quality / metric checks
- Gate D (hard fail): provenance completeness for reproducibility
- Summary: `PASS`, `PASS_WITH_WARNINGS`, `FAIL`

## Commit Conventions

- Commit messages are short imperative sentences describing the change
- PRs typically use `codex/<slug>` branch naming
- Each section addition follows the pattern: constants/initializer first, then APIs, then orchestration wrappers

## Important Warnings

- Notebook JSON diffs are noisy — keep edits localized when modifying the `.ipynb`
- InsightFace/CLIP availability varies by runtime; always respect the fallback chain
- Comfy workflows cover generation only; stateful lifecycle requires the orchestration layer
- `character.json` state blocks are append-only — never mutate historical entries
