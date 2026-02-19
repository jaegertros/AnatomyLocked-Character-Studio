# Models & Setup Reference

## Custom Nodes (install first via ComfyUI Manager)

Open ComfyUI Manager → Install Custom Nodes → search each:

| Node Pack | Author | Purpose |
|---|---|---|
| ComfyUI_IPAdapter_plus | cubiq | IP-Adapter FaceID + body conditioning |
| comfyui_controlnet_aux | Fannovel16 | DWPreprocessor, DepthAnything, etc. |

Restart ComfyUI after installing both.

---

## Models to Download

### Already have (from your Drive)
- `sd_xl_base_1.0.safetensors` — SDXL base ✓
- `controlnet-openpose-sdxl-1.0.safetensors` — Pose ControlNet ✓
- `controlnet-depth-sdxl-1.0.safetensors` — Depth ControlNet ✓

### New models needed for Phase 2

#### 1. IP-Adapter FaceID Plus v2 (SDXL)
```
File:   ip-adapter-faceid-plusv2_sdxl.bin
Folder: models/ipadapter/
URL:    https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin
Size:   ~1.7 GB
```

#### 2. IP-Adapter Plus SDXL (body consistency)
```
File:   ip-adapter-plus_sdxl_vit-h.safetensors
Folder: models/ipadapter/
URL:    https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors
Size:   ~1.1 GB
```

#### 3. CLIP Vision ViT-H (required by both IP-Adapters above)
```
File:   CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors
Folder: models/clip_vision/
URL:    https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/image_encoder/model.safetensors
        (rename after download)
Size:   ~3.9 GB
```

#### 4. InsightFace buffalo_l (for FaceID — auto-downloaded)
InsightFace downloads this automatically on first use to `~/.insightface/models/`.
In Colab this means it re-downloads each session. To cache it on Drive:
- After first run, copy `~/.insightface/` to `/content/drive/MyDrive/AI/models/insightface/`
- Add a cell to your Colab notebook: `!ln -sf /content/drive/MyDrive/AI/models/insightface ~/.insightface`

---

## extra_model_paths.yaml addition

Add `ipadapter` to your ComfyUI extra_model_paths.yaml so ComfyUI finds the new folder:

```yaml
comfyui:
  base_path: /content/drive/MyDrive/AI/models
  checkpoints: checkpoints
  clip: clip
  clip_vision: clip_vision        # already present — good
  controlnet: controlnet
  embeddings: embeddings
  ipadapter: ipadapter            # ADD THIS LINE
  loras: loras
  upscale_models: upscale_models
  vae: vae
```

Your ComfyUI notebook already writes this file — add the `ipadapter` line to the
`extra_model_paths` dict in the Environment Setup cell.

---

## Download snippet for your Colab notebook

Add this to the downloads cell (same pattern as your existing code):

```python
ipadapter_path = os.path.join(base_models, "ipadapter")
os.makedirs(ipadapter_path, exist_ok=True)

# IP-Adapter FaceID Plus v2 SDXL
download(
    "https://huggingface.co/h94/IP-Adapter-FaceID/resolve/main/ip-adapter-faceid-plusv2_sdxl.bin",
    ipadapter_path
)

# IP-Adapter Plus SDXL (body)
download(
    "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/ip-adapter-plus_sdxl_vit-h.safetensors",
    ipadapter_path
)

# CLIP Vision ViT-H (rename to match workflow)
download(
    "https://huggingface.co/h94/IP-Adapter/resolve/main/sdxl_models/image_encoder/model.safetensors",
    clip_vision_path,
    "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
)
```

---

## Workflow import

1. Open ComfyUI in your browser
2. Drag `phase1_exploration.json` onto the canvas, or use Load button
3. When you have a character you like from Phase 1, load `phase2_identity_lock.json`
4. Set the "Character Reference" LoadImage node to your Phase 1 candidate
5. Set "Pose Reference" to your 3d.sk photo

---

## Tuning cheat sheet (Phase 2)

| Problem | Fix |
|---|---|
| Face drifting between renders | Raise FaceID weight toward 1.0 |
| Pose being ignored | Raise ControlNet strength (try 1.1) |
| Body type inconsistent | Raise body IP-Adapter weight (0.4 → 0.6) |
| Body weight fighting pose | Lower it (0.4 → 0.2) or set end_at=0.5 |
| Overall looks wrong but hard to say why | Lock seed, change one parameter at a time |
| InsightFace not detecting face | Ensure reference image has a clear front-facing crop |
