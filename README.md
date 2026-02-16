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

## Checklist

See Character_Set_Validation_Checklist.md for a validation template.