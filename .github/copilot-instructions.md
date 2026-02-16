# AnatomyLocked Character Studio - Copilot Instructions

## Project purpose
- Build a Colab-based character studio for anatomy-accurate, identity-locked human reference images.
- Output reusable character sets (neutral views, pose variants, lighting variants, scenes) suitable for art and storytelling references.
- This is not a random image generator; once a character is finalized, identity must remain stable.

## Core constraints
- Identity invariants: bone structure, facial geometry, body proportions, permanent skin features (freckles, moles, scars, birthmarks), and their exact placement.
- Allowed variations: pose/posture, muscle flexion/compression, skin folds due to movement, hair style (same root pattern unless explicitly changed), makeup/nail color, lighting, camera angle, optional clothing.
- Forbidden variations: face drift, proportion changes, feature relocation, anatomy exaggeration, stylization that breaks realism.

## Pipeline goals
- Support iterative tuning: lock completed parts while refining others (region-by-region refinement).
- Provide tools and prompts for consistent identity across multiple renders (deterministic seeds, identity embeddings, ControlNet for pose/depth/normal guidance).
- Keep a clean separation between identity, pose, lighting, and styling controls.

## Data and realism
- Prioritize anatomically correct outputs; no stylization that breaks human realism.
- Allow nudity for anatomy study outputs when needed.
- Use reference sets (user-provided) to tune models and validate accuracy.

## Repository context
- Primary artifact: AnatomyLocked_Character_Studio.ipynb (Colab notebook).
- Exported script: anatomylocked_character_studio.py (auto-generated from notebook).
- README is minimal and may be expanded.

## Editing guidance
- Prefer changes in the notebook first; regenerate the script only if needed.
- Keep prompts and code deterministic and explicit to reduce identity drift.
- Add brief comments only for non-obvious logic.
