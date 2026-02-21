# AnatomyLocked Comfy Workflow Suite

This suite is the Comfy-first implementation path for the project.

## Workflow files

- `phase1_exploration.json`
- `phase2_identity_lock.json`
- `phase3_regional_refinement_inpaint.json`
- `phase4_canonical_finalization.json`
- `phase5_reference_variants.json`

## Recommended run order

1. **Phase 1**: Explore candidate look and seed.
2. **Phase 2**: Lock identity/pose guidance with reference image.
3. **Phase 3**: Perform region-only inpaint refinement with masks.
4. **Phase 4**: Produce canonical frozen baseline render.
5. **Phase 5**: Produce reference variants (batch set).

## Notes on scope

- Comfy handles generation and visual iteration.
- Stateful governance (character JSON history, policy gates, section handoffs) is handled by the orchestration layer.
- This is intentional so workflows stay maintainable instead of one monolithic graph.

## Minimal manual usage in Comfy UI

1. Open ComfyUI.
2. Load one phase JSON file.
3. Set prompt/image/mask widgets.
4. Queue Prompt.
5. Save output and move to next phase.

## Minimal orchestrated usage (Python)

```python
from pathlib import Path
from orchestration import AnatomyLockedPipelineOrchestrator

orchestrator = AnatomyLockedPipelineOrchestrator(
    repo_root=Path("."),
    characters_root=Path("/content/drive/MyDrive/AI/datasets/characters"),
    comfy_base_url="http://127.0.0.1:8188",
)

orchestrator.run_phase1_exploration(character_id="CH-0001")
orchestrator.run_phase2_identity_lock(character_id="CH-0001")
orchestrator.run_phase3_regional_refinement(character_id="CH-0001")
orchestrator.run_phase4_canonical_finalization(character_id="CH-0001")
orchestrator.run_phase5_reference_variants(character_id="CH-0001")
```
