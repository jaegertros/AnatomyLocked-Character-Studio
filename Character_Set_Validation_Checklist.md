# Character Set Validation Checklist

Use this checklist to validate identity consistency, anatomy accuracy, and set completeness.

## Metadata

- Character ID:
- Base seed(s):
- Base model:
- ControlNet stack (pose/depth/normal):
- Date:

## Identity Invariants (Must Never Change)

- [ ] Bone structure matches baseline
- [ ] Facial geometry matches baseline
- [ ] Body proportions match baseline
- [ ] Permanent skin features match baseline (freckles, moles, scars, birthmarks)
- [ ] Feature placement matches baseline (exact location and shape)

## Allowed Variations (Within Realism)

- [ ] Pose/posture changes only
- [ ] Muscle flexion/compression looks anatomically correct
- [ ] Skin folding due to movement looks realistic
- [ ] Hair changes keep base root pattern unless explicitly changed
- [ ] Makeup/nail color matches intended variant
- [ ] Lighting/camera angle changes only
- [ ] Clothing is optional and does not alter anatomy

## Forbidden Variations (Must Not Appear)

- [ ] No face drift across renders
- [ ] No proportion changes
- [ ] No feature relocation
- [ ] No anatomy exaggeration
- [ ] No stylization that breaks realism

## Anatomy Accuracy

- [ ] Shoulder, pelvis, and spine alignment is correct
- [ ] Limb length and joint placement are correct
- [ ] Hands and feet are anatomically plausible
- [ ] Muscle groups and tendons are consistent with pose
- [ ] Skin deformation matches pose and tension

## Coverage: Required Set

- [ ] Neutral views (front, back, left, right)
- [ ] 3/4 views (front and back)
- [ ] Pose variants (standing, sitting, crouched, dynamic)
- [ ] Lighting variants (key, fill, rim; soft and hard)
- [ ] Scene renders (optional)

## Notes

- Issues found:
- Fixes applied:
- Next steps:
