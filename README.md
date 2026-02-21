# AnatomyLocked Character Studio

Colab-based character studio for anatomy-accurate, identity-locked human reference images.
This is not a random image generator. Once a character is finalized, identity must remain stable.

## Goals

- Produce reusable character sets: neutral anatomy views, pose variants, lighting variants, scenes
- Keep identity consistent across renders while allowing realistic deformation from movement
- Support region-by-region refinement so completed parts stay locked while tuning others

## Identity Rules

### Must Never Change

- Bone structure, facial geometry, body proportions
- Permanent skin features (freckles, moles, scars, birthmarks) and exact placement

### Allowed to Vary

- Pose, posture, muscle flexion/compression, skin folds due to movement
- Hair style (root pattern consistent unless explicitly changed)
- Makeup, nail color, lighting, camera angle, optional clothing

### Forbidden

- Face drift, proportion changes, feature relocation
- Anatomy exaggeration or stylization that breaks realism

## Anatomy Focus

- Outputs prioritize anatomical correctness and realism
- Nudity is allowed when needed for anatomy study

## Project Artifacts

- Notebook: AnatomyLocked_Character_Studio.ipynb
- Script: anatomylocked_character_studio.py (auto-generated from the notebook)

## Suggested Workflow (High Level)

1. Select base model and ControlNet stack for pose, depth, and normals
2. Lock identity with deterministic seeds and identity embeddings
3. Iterate region-by-region while keeping locked regions fixed
4. Generate standardized character set outputs and validate against the checklist

## Direction Image Usage (ComfyUI)

- `OtherSetups/phase2_identity_lock.json` already supports external images through its two `LoadImage` nodes.
- You can use any image for look direction in `Character Reference` (it does not have to come from Phase 1 generation).
- Place/upload your files into ComfyUI `input` (drag-and-drop in ComfyUI also lands files there), then pick them from each `LoadImage` dropdown.
- Keep FaceID weight high (`0.85-1.0`) for stronger identity lock.
- Lower body IP-Adapter weight (for example, `0.4 -> 0.2`) if it fights pose adherence.

## Section 5 Identity Lock (Notebook/Script)

- Canonical character state is stored at `datasets/characters/<character_id>/character.json`.
- Section 5 adds an `identity_lock` block with:
  - reference image registrations + SHA-256 checksums
  - invariant feature entries (with optional mask files and mask checksums)
  - fingerprint metadata and thresholds
  - latest validation result (`last_validation`)
- Fingerprint backend fallback order is deterministic:
  - `insightface` -> `clip` -> `phash`
- Default behavior:
  - `require_face_detection = False`
  - `fail_on_missing_mask = True`
- Comfy translation for this lock schema is intentionally deferred until notebook Sections 5-8 are stable.

## Section 7 Plan (Regional Refinement Mode)

### Goal
- Build a repeatable regional refinement workflow that improves local fidelity (face/hair/torso) without violating Section 5 identity lock invariants and while respecting Section 6 canonical region masks.

### Core functions to implement (notebook first, then script mirror)
- `load_region_map(character_id)`
- `validate_region_map(region_map, masks_dir)`
- `run_regional_refinement(character_id, input_image_path, config=None)`
- `validate_regional_refinement(character_id, refined_image_path, strict=True)`
- `promote_refined_candidate(character_id, refined_image_path, report)`

### Gate policy
- Gate A (hard fail): identity lock pass required.
- Gate B (hard fail): all required regions processed.
- Gate C (configurable hard/soft fail): regional quality checks.
- Gate D (hard fail): provenance completeness for reproducibility.
- Summary status: `PASS`, `PASS_WITH_WARNINGS`, `FAIL`.

### Initial region scope
- `face_primary` (strictest identity constraints)
- `hair_silhouette`
- `upper_torso`

### Execution sequence
1. Finalize Section 6 schema + validators.
2. Add `regional_refinement` append-only block in `character.json`.
3. Implement load/validate helpers for region map + masks.
4. Implement deterministic per-region refinement/compositing.
5. Run identity validation with backend fallback (`insightface -> clip -> phash/dhash`).
6. Emit/persist validation report and promotion metadata.
7. Mirror notebook logic into `anatomylocked_character_studio.py`.
8. Run dry QA on 3-5 characters with varied pose/lighting.

## Checklist

See Character_Set_Validation_Checklist.md for a validation template.
