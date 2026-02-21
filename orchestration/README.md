# Orchestration Layer (Phase Start)

This folder provides the first implementation step for a modular ComfyUI pipeline architecture.

## What this adds

- Comfy API client for submitting and tracking workflow runs
- Workflow node override patching at runtime
- Character state persistence (`character.json`) run history under `orchestration.runs`
- Stage wrappers for existing workflows:
  - `OtherSetups/phase1_exploration.json`
  - `OtherSetups/phase2_identity_lock.json`
  - `OtherSetups/phase3_regional_refinement_inpaint.json`
  - `OtherSetups/phase4_canonical_finalization.json`
  - `OtherSetups/section10_reference_views.json` (Section 10 alias of Phase 5 reference variants)

## Phase ↔ section mapping

Comfy workflow filenames remain phase-oriented, while notebook implementation status is section-oriented.

- Phase 1 → Section 3 (exploration)
- Phase 2 → Section 5 (identity lock guidance)
- Phase 3 → Section 7 (regional refinement)
- Phase 4 → Section 8 (canonical finalization)
- Phase 5 → Section 10 (lighting, camera, and reference views)

## Why this exists

A single monolithic Comfy graph is not a good fit for stateful lifecycle operations (identity lock policy, region freeze gates, QC policy, versioning). This layer keeps Comfy responsible for generation while Python handles orchestration and governance.

## Usage sketch

```python
from pathlib import Path
from orchestration import AnatomyLockedPipelineOrchestrator

repo_root = Path(".")
characters_root = Path("/content/drive/MyDrive/AI/datasets/characters")

orchestrator = AnatomyLockedPipelineOrchestrator(
    repo_root=repo_root,
    characters_root=characters_root,
    comfy_base_url="http://127.0.0.1:8188",
)

phase1_run = orchestrator.run_phase1_exploration(
    character_id="CH-0001",
    node_overrides={
        2: {"widgets_values": {0: "full body neutral anatomical reference"}},
        5: {"widgets_values": {0: 123456789, 1: "fixed"}},
    },
)

phase2_run = orchestrator.run_phase2_identity_lock(
    character_id="CH-0001",
    node_overrides={
        8: {"widgets_values": {0: "your_candidate_image.png"}},
        12: {"widgets_values": {0: "pose_reference.png"}},
    },
)

phase3_run = orchestrator.run_phase3_regional_refinement(
    character_id="CH-0001",
    node_overrides={
        2: {"widgets_values": {0: "character_base.png"}},
        3: {"widgets_values": {0: "region_mask.png"}},
    },
)

phase4_run = orchestrator.run_phase4_canonical_finalization(
    character_id="CH-0001",
)

section10_run = orchestrator.run_phase5_section10_reference_views(
    character_id="CH-0001",
    node_overrides={
        2: {"widgets_values": {0: "studio softbox, neutral gray seamless"}},
        5: {"widgets_values": {0: "50mm lens, eye-level, orthographic style"}},
        7: {"widgets_values": {0: "front|three-quarter-left|profile-right"}},
    },
)

print(
    phase1_run.prompt_id,
    phase2_run.prompt_id,
    phase3_run.prompt_id,
    phase4_run.prompt_id,
    section10_run.prompt_id,
)
```

## Next implementation targets

1. Add explicit stage contracts for Sections 6/7 handoff and freeze-state enforcement.
2. Add QC hooks for Section 15 policy checks and rejection rules.
3. Add export/archival manifesting for Sections 11/16.
4. Add a thin notebook cell wrapper for easy Colab invocation.
