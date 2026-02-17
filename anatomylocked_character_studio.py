# -*- coding: utf-8 -*-
"""AnatomyLocked_Character_Studio.ipynb

Auto-generated from the notebook.
"""

"""# AnatomyLocked Character Studio"""

"""## Overview

This notebook is a **persistent human character studio** designed for:
- Reference-grade anatomy
- Identity-locked characters
- Regional anatomical refinement
- Pose-accurate deformation
- Reloadable, reusable characters
- Multi-character scene composition

This is **not** a random image generator.  
Once a character is finalized, they must only change in ways a real human could."""

"""## Quick Identity Guide

**Must never change**
- Bone structure, facial geometry, body proportions
- Permanent skin features (freckles, moles, scars, birthmarks) and exact placement

**Allowed to vary**
- Pose/posture, muscle flexion/compression, skin folds due to movement
- Hair style (same root pattern unless explicitly changed)
- Makeup, nail color, lighting, camera angle, optional clothing

**Realistic deformation is expected**
- Stretching, bending, and flexing should change appearance only in ways a real body would"""

"""## Identity Lock Helper (Quick Settings)

- Fix the base seed for the character and keep it constant for identity-locked renders.
- Use the same identity embedding and reference set across all variants.
- Lock completed regions while tuning others (region-by-region refinement).
- Change only one factor at a time (pose, lighting, or camera) to isolate drift.

## Required Output Set (Reference Table)

| Set | Purpose | Views / Notes |
| --- | ------- | ------------- |
| Neutral | Baseline anatomy | Front, back, left, right |
| 3/4 | Shape consistency | Front 3/4 and back 3/4 |
| Poses | Deformation realism | Standing, sitting, crouched, dynamic |
| Lighting | Form clarity | Key, fill, rim; soft and hard |
| Scenes (opt) | Storytelling | Optional environment renders |"""

"""## Drift Triage Checklist

- Confirm base model, ControlNet stack, and seed match the baseline.
- Compare invariant features (moles, scars, facial proportions) against the baseline set.
- If drift appears, change only one variable at a time (pose, lighting, or camera).
- Re-run a neutral view to verify the lock before generating variants.
- If drift persists, refresh the identity embedding reference set."""

from pathlib import Path
import json

template_path = Path("Character_Validation_History_Template.json")

if template_path.exists():
    print(f"Template already exists: {template_path.resolve()}")
else:
    template = {
        "character_id": "CH-0001",
        "created_date": "YYYY-MM-DD",
        "baseline": {
            "base_model": "",
            "controlnet_stack": {
                "pose": "",
                "depth": "",
                "normal": ""
            },
            "seed": 0,
            "identity_embedding": {
                "type": "",
                "reference_images": []
            }
        },
        "identity_lock": {
            "locked_regions": ["face", "torso"],
            "notes": ""
        },
        "render_sets": [
            {
                "set_id": "SET-0001",
                "date": "YYYY-MM-DD",
                "purpose": "neutral views",
                "lighting": "",
                "camera": "",
                "pose_pack": "",
                "outputs": {
                    "image_paths": []
                },
                "validation": {
                    "identity_invariants_pass": False,
                    "anatomy_accuracy_pass": False,
                    "notes": ""
                }
            }
        ],
        "issues": [
            {
                "date": "YYYY-MM-DD",
                "issue": "",
                "resolution": ""
            }
        ],
        "next_steps": ""
    }
    template_path.write_text(json.dumps(template, indent=2), encoding="utf-8")
    print(f"Created template: {template_path.resolve()}")

from datetime import date
from pathlib import Path
import json

template_path = Path("Character_Validation_History_Template.json")
output_dir = Path("character_histories")
output_dir.mkdir(exist_ok=True)

character_id = "CH-0001"
created_date = date.today().isoformat()

if not template_path.exists():
    print(f"Template not found: {template_path.resolve()}")
    print("Skipping history file creation. Add the template and re-run this cell.")
else:
    with template_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    data["character_id"] = character_id
    data["created_date"] = created_date

    output_path = output_dir / f"{character_id}_history.json"
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)

    print(f"Wrote {output_path}")

"""---

## Core Rules

### Identity Invariants (Must Never Change)
- Bone structure
- Facial geometry
- Body proportions
- Permanent skin features (freckles, moles, scars, birthmarks)
- Relative placement and shape of invariant features

### Allowed Variations
- Pose and posture
- Muscle flexion and compression
- Skin folding due to movement
- Hair style (root pattern remains consistent)
- Makeup and nail color
- Lighting and camera angle
- Clothing (optional)

### Forbidden Variations
- Face drift
- Proportion changes
- Feature relocation
- Anatomy exaggeration
- Stylization that breaks realism"""

"""---

## Expected Output

Each character produces a reusable reference package:
- Neutral anatomy views
- Pose variations
- Lighting variants
- Scene renders
- Reloadable identity data"""

"""---

# SECTION 1 — Environment Setup & Dependencies

**Purpose:**  
Prepare Colab environment, GPU, and required libraries.

- Python version check
- GPU availability
- Dependency installation
- Cache and output directories"""

"""📌 1.1 Mount Google Drive"""

from google.colab import drive

drive.mount('/content/drive')

"""📌 1.2 Define AI Workspace Paths"""

from pathlib import Path

# Base AI workspace
AI_BASE = Path("/content/drive/My Drive/AI")

# High-level directories
AI_DIRS = {
    "datasets": AI_BASE / "datasets",
    "experiments": AI_BASE / "Experiments",
    "images": AI_BASE / "Images",
    "rag": AI_BASE / "rag",
    "training": AI_BASE / "Training",
    "models": AI_BASE / "models",
}

# Model subdirectories (UNDER models/)
MODEL_DIRS = {
    # Diffusion base models live under models/diffusion_base/{sd, sdxl}
    "diffusion_base": AI_DIRS["models"] / "diffusion_base",
    "diffusion_sd": AI_DIRS["models"] / "diffusion_base" / "sd",
    "diffusion_sdxl": AI_DIRS["models"] / "diffusion_base" / "sdxl",
    # Back-compat alias for older cells
    "base_models": AI_DIRS["models"] / "diffusion_base",
    "audio_models": AI_DIRS["models"] / "audio_models",
    "checkpoints": AI_DIRS["models"] / "checkpoints",
    "controlnet": AI_DIRS["models"] / "controlnet",
    "llm": AI_DIRS["models"] / "llm",
    "loras": AI_DIRS["models"] / "loras",
}

# Guard: ensure Drive + base folders exist
if not AI_BASE.exists():
    raise FileNotFoundError(
        f"AI_BASE not found: {AI_BASE}. Did you mount Google Drive?"
    )

print("AI_BASE:", AI_BASE)
print("Model directories:")
for key in (
    "diffusion_base",
    "diffusion_sd",
    "diffusion_sdxl",
    "controlnet",
    "loras",
    "checkpoints",
):
    print(f" - {key}: {MODEL_DIRS[key]}")

# Fail fast if base model folder is empty
if not MODEL_DIRS["diffusion_base"].exists():
    raise FileNotFoundError(
        f"Base model folder missing: {MODEL_DIRS['diffusion_base']}"
    )
if not any(MODEL_DIRS["diffusion_base"].rglob("*")):
    raise FileNotFoundError(
        "No model files found under diffusion_base. "
        "Add SD/SDXL model files and re-run."
    )

"""<details>
<summary><strong>Optional: Model Downloads (Collapsed)</strong></summary>

Use this section only when you need to add new models. Supports Hugging Face, Civitai, Google Drive, and direct URLs."""

_DOWNLOAD_DEPS_READY = False
_HF_HUB_AVAILABLE = False

def ensure_download_deps() -> bool:
    global _DOWNLOAD_DEPS_READY, _HF_HUB_AVAILABLE, requests, gdown, tqdm, hf_hub_download, HfHubHTTPError
    if _DOWNLOAD_DEPS_READY:
        return True
    try:
        import requests
        import gdown
        from tqdm.auto import tqdm
        from huggingface_hub import hf_hub_download
        from huggingface_hub.utils import HfHubHTTPError
        _DOWNLOAD_DEPS_READY = True
        _HF_HUB_AVAILABLE = True
        print("Download dependencies are available.")
        return True
    except ImportError:
        print("Installing download dependencies...")
        !pip install -q huggingface_hub gdown requests tqdm
        import requests
        import gdown
        from tqdm.auto import tqdm
        from huggingface_hub import hf_hub_download
        from huggingface_hub.utils import HfHubHTTPError
        _DOWNLOAD_DEPS_READY = True
        _HF_HUB_AVAILABLE = True
        print("Download dependencies installed.")
        return True
    except Exception as exc:
        _DOWNLOAD_DEPS_READY = False
        _HF_HUB_AVAILABLE = False
        print(f"Download dependency setup failed: {exc}")
        return False

try:
    from google.colab import userdata
except Exception:
    userdata = None

def _get_colab_secret(name: str) -> str:
    if userdata is None:
        print("Colab userdata not available.")
        return ""
    try:
        token = userdata.get(name)
        if token:
            print(f"✓ {name} retrieved from Colab secrets.")
            return token
        print(f"✗ {name} not found in Colab secrets.")
        return ""
    except Exception as exc:
        print(f"✗ Error retrieving {name}: {exc}")
        return ""

def get_hf_token() -> str:
    return _get_colab_secret("HF_TOKEN")

def get_civit_token() -> str:
    return _get_colab_secret("CIVIT_TOKEN")

from pathlib import Path
from urllib.parse import urlparse

def _is_hf_url(parsed_url) -> bool:
    host = parsed_url.netloc.lower()
    return "huggingface.co" in host or "hf.co" in host

def _classify_download_name(filename: str) -> str:
    name = filename.lower()
    if "sdxl" in name or "sd_xl" in name or "sd xl" in name:
        return "sdxl"
    if (
        "v1-5" in name
        or "v15" in name
        or "sd15" in name
        or "stable-diffusion-v1" in name
        or "sd-v1" in name
    ):
        return "sd"
    if "controlnet" in name or "openpose" in name or "depth" in name or "normal" in name:
        return "controlnet"
    if "lora" in name or "lyco" in name:
        return "lora"
    if "audio" in name or "whisper" in name or "tts" in name:
        return "audio"
    if name.endswith(".bin") or name.endswith(".gguf"):
        return "llm"
    if name.endswith(".ckpt") or name.endswith(".safetensors") or name.endswith(".pt") or name.endswith(".pth"):
        return "checkpoint"
    return "checkpoint"

def download_file_direct(url: str, destination_path: Path) -> bool:
    if not _DOWNLOAD_DEPS_READY:
        print("Download dependencies not ready. Run ensure_download_deps() first.")
        return False
    print("Attempting direct download.")
    headers = {}
    if "civitai.com" in url:
        civit_token = get_civit_token()
        if civit_token:
            headers["Authorization"] = f"Bearer {civit_token}"
            print("Added Civitai token to headers for authenticated download.")
        else:
            print("Civitai token not found, attempting unauthenticated download.")

    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))

        with open(destination_path, "wb") as handle:
            with tqdm(total=total_size, unit="B", unit_scale=True, desc=destination_path.name) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)
                        pbar.update(len(chunk))
        return True
    except requests.exceptions.RequestException as exc:
        print(f"✗ Error during direct download: {exc}")
        if destination_path.exists():
            destination_path.unlink()
        return False

def download_file(url: str, destination_path: Path) -> bool:
    if not _DOWNLOAD_DEPS_READY:
        print("Download dependencies not ready. Run ensure_download_deps() first.")
        return False
    print(f"Attempting to download from {url} to {destination_path}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        parsed_url = urlparse(url)

        if _HF_HUB_AVAILABLE and _is_hf_url(parsed_url):
            print("Detected Hugging Face link.")
            hf_token = get_hf_token()
            path_parts = parsed_url.path.split("/")
            if len(path_parts) >= 5 and path_parts[3] == "resolve":
                repo_id = f"{path_parts[1]}/{path_parts[2]}"
                filename = path_parts[-1]
                if filename:
                    try:
                        downloaded_path = hf_hub_download(repo_id=repo_id, filename=filename, local_dir=destination_path.parent, local_dir_use_symlinks=False, token=hf_token if hf_token else None)
                        if Path(downloaded_path).name != destination_path.name:
                            Path(downloaded_path).rename(destination_path)
                        print(f"✓ Successfully downloaded {destination_path.name} from Hugging Face.")
                        return True
                    except HfHubHTTPError as exc:
                        print(f"✗ Error during Hugging Face download (HTTP Error): {exc}")
                        if "401 Client Error" in str(exc) or "403 Client Error" in str(exc):
                            print("    This might be a private model or require authentication. Check your HF_TOKEN.")
                        if destination_path.exists():
                            destination_path.unlink()
                        return False
                    except Exception as exc:
                        print(f"✗ Hugging Face download failed: {exc}. Attempting direct download.")
                        return download_file_direct(url, destination_path)
            print("Could not parse Hugging Face URL. Attempting direct download.")
            return download_file_direct(url, destination_path)

        if "drive.google.com" in url:
            print("Detected Google Drive link.")
            gdown.download(url, str(destination_path), quiet=False, fuzzy=True)
            print(f"✓ Successfully downloaded {destination_path.name}")
            return True

        return download_file_direct(url, destination_path)
    except gdown.exceptions.GDriveDownloadError as exc:
        print(f"✗ Error during Google Drive download: {exc}")
        if destination_path.exists():
            destination_path.unlink()
        return False
    except Exception as exc:
        print(f"✗ An unexpected error occurred: {exc}")
        if destination_path.exists():
            destination_path.unlink()
        return False

#@title Download model (optional)
ENABLE_MODEL_DOWNLOADS = False  #@param {type:"boolean"}
MODEL_URL = ""  #@param {type:"string"}
MODEL_TYPE_HINT = "auto"  #@param ["auto", "sd", "sdxl", "controlnet", "lora", "checkpoint", "llm", "audio"]

if ENABLE_MODEL_DOWNLOADS:
    if not MODEL_URL:
        print("Paste a model URL into MODEL_URL.")
    else:
        if ensure_download_deps():
            hint = None if MODEL_TYPE_HINT == "auto" else MODEL_TYPE_HINT
            smart_download_model(MODEL_URL, model_type_hint=hint)
        else:
            print("Download dependencies not ready.")
else:
    print("Downloads are disabled.")

"""</details>"""

"""📌 1.3 Create Missing Directories (Non-Destructive)"""

for name, path in AI_DIRS.items():
    path.mkdir(parents=True, exist_ok=True)
    print(f"✓ {name}: {path}")

"""📌 1.4 Quick Sanity Check (Optional)"""

assert AI_BASE.exists(), "AI base directory was not created correctly."
print("AI workspace is ready.")

"""🔍 1.5 Scan Existing Models & Assets"""

def scan_directory(path, extensions=None):
    results = []
    if not path.exists():
        return results

    for p in path.rglob("*"):
        if p.is_file():
            if extensions is None or p.suffix.lower() in extensions:
                results.append(p)
    return results

"""📦 Scan Diffusion / ML Models"""

MODEL_EXTS = {".ckpt", ".safetensors", ".pt", ".pth"}

base_models = scan_directory(MODEL_DIRS["diffusion_base"], MODEL_EXTS)
loras = scan_directory(MODEL_DIRS["loras"], MODEL_EXTS)
controlnets = scan_directory(MODEL_DIRS["controlnet"], MODEL_EXTS)
checkpoints = scan_directory(MODEL_DIRS["checkpoints"], MODEL_EXTS)


print(f"Base models: {len(base_models)}")
print(f"LoRAs: {len(loras)}")
print(f"ControlNets: {len(controlnets)}")
print(f"Checkpoints: {len(checkpoints)}")

"""📄 Optional: Print a Preview"""

def preview(files, limit=10):
    for f in files[:limit]:
        print(f" - {f.name}")

print("\nSample base models:")
preview(base_models)

print("\nSample LoRAs:")
preview(loras)

"""---

# SECTION 2 — Base Model & Control Stack Selection

**Purpose:**  
Define the foundational models used throughout the notebook.

Includes:
- Base diffusion model (photorealistic, anatomy-capable)
- ControlNet modules (pose, depth, normals)
- Identity embedding models
- Version locking and rationale

This section should rarely change."""

"""2.1 Model Registry Data Structures"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

@dataclass
class ModelEntry:
    name: str
    path: Path
    model_type: str     # e.g. "sd", "sdxl", "controlnet", "lora"
    size_mb: float

MODEL_REGISTRY: Dict[str, List[ModelEntry]] = {
    "sd": [],
    "sdxl": [],
    "controlnet": [],
    "lora": [],
    "checkpoint": [],
    "llm": [],
    "audio": [],
}

"""🔍 2.2 Helper: File Size Utility"""

def file_size_mb(path: Path) -> float:
    return round(path.stat().st_size / (1024 ** 2), 2)

"""🔍 2.3 Heuristic Model Classifier"""

def classify_model(path: Path) -> str:
    name = path.name.lower()
    parent_hint = "/".join(part.lower() for part in path.parts)

    if "/diffusion_base/sd/" in parent_hint:
        return "sd"
    if "/diffusion_base/sdxl/" in parent_hint:
        return "sdxl"
    if "/controlnet/" in parent_hint:
        return "controlnet"
    if "/loras/" in parent_hint:
        return "lora"
    if "/llm/" in parent_hint:
        return "llm"
    if "/audio_models/" in parent_hint:
        return "audio"

    if "controlnet" in name or "openpose" in name or "depth" in name or "normal" in name:
        return "controlnet"
    if "lora" in name or "lyco" in name:
        return "lora"
    if "audio" in name or "whisper" in name or "tts" in name:
        return "audio"
    if "sdxl" in name or "sd_xl" in name or "sd xl" in name:
        return "sdxl"
    if (
        "v1-5" in name
        or "v15" in name
        or "sd15" in name
        or "sd_1.5" in name
        or "sd-1.5" in name
        or "stable-diffusion-v1" in name
        or "sd-v1" in name
    ):
        return "sd"

    if path.suffix in {".ckpt", ".safetensors", ".pt", ".pth"}:
        return "checkpoint"
    if path.suffix in {".bin", ".gguf"}:
        return "llm"

    return "unknown"

"""🔍 2.4 Scan Model Directories & Populate Registry"""

MODEL_EXTS = {".ckpt", ".safetensors", ".pt", ".pth", ".bin", ".gguf"}

MODEL_EXTS = {".ckpt", ".safetensors", ".pt", ".pth", ".bin", ".gguf"}

# Clear registry to avoid stale counts
for _k in list(MODEL_REGISTRY.keys()):
    MODEL_REGISTRY[_k] = []

def register_models_from_dir(
    directory: Path,
    model_type_override: str | None = None,
    skip_subdirs: tuple[str, ...] = (),
):
    for p in directory.rglob("*"):
        if p.is_file() and p.suffix.lower() in MODEL_EXTS:
            parent_hint = "/".join(part.lower() for part in p.parts)
            if skip_subdirs and any(s in parent_hint for s in skip_subdirs):
                continue
            mtype = model_type_override or classify_model(p)
            if mtype in MODEL_REGISTRY:
                MODEL_REGISTRY[mtype].append(
                    ModelEntry(
                        name=p.name,
                        path=p,
                        model_type=mtype,
                        size_mb=file_size_mb(p)
                    )
                )

# Scan model subdirectories only
for key in [
    "diffusion_base",
    "diffusion_sd",
    "diffusion_sdxl",
    "checkpoints",
    "controlnet",
    "loras",
    "llm",
    "audio_models",
]:
    override = None
    skip_subdirs = ()
    if key == "diffusion_sd":
        override = "sd"
    elif key == "diffusion_sdxl":
        override = "sdxl"
    elif key == "diffusion_base":
        # Avoid double-counting if files are already in sd/sdxl subfolders
        skip_subdirs = ("/diffusion_base/sd/", "/diffusion_base/sdxl/")
    register_models_from_dir(MODEL_DIRS[key], override, skip_subdirs)

def preflight_checks(base_model_entry=None, use_controlnet=False, controlnet_entries=None):
    errors = []
    try:
        import torch
        if not torch.cuda.is_available():
            errors.append("CUDA not available. Ensure a GPU runtime is selected.")
    except Exception as exc:
        errors.append(f"Torch not available: {exc}")

    has_base = bool(MODEL_REGISTRY.get("sd")) or bool(MODEL_REGISTRY.get("sdxl"))
    if not has_base:
        errors.append(
            "No SD/SDXL base models found in the registry. "
            "Add models under models/diffusion_base/sd or models/diffusion_base/sdxl."
        )

    if base_model_entry is not None:
        try:
            if not Path(base_model_entry.path).exists():
                errors.append(f"Selected base model missing: {base_model_entry.path}")
        except Exception as exc:
            errors.append(f"Could not verify selected base model: {exc}")

    if use_controlnet:
        available = []
        if controlnet_entries:
            available = [e for e in controlnet_entries.values() if e is not None]
        if not available:
            errors.append(
                "USE_CONTROLNET is True but no ControlNet files are available. "
                "Add ControlNet weights or set USE_CONTROLNET=False."
            )

    if errors:
        print("Preflight checks failed:
")
        for err in errors:
            print(f" - {err}")
        raise RuntimeError("Preflight checks failed. See messages above.")

    print("Preflight checks passed.")
    return True

# Scan model subdirectories only
for key in [
    "diffusion_sd",
    "diffusion_sdxl",
    "checkpoints",
    "controlnet",
    "loras",
    "llm",
    "audio_models",
]:
    override = None
    if key == "diffusion_sd":
        override = "sd"
    elif key == "diffusion_sdxl":
        override = "sdxl"
    register_models_from_dir(MODEL_DIRS[key], override)

# List files in models/diffusion_base
base_dir = MODEL_DIRS["diffusion_base"]
print(f"diffusion_base: {base_dir}")

if not base_dir.exists():
    print("  (folder not found)")
else:
    files = [p for p in base_dir.rglob("*") if p.is_file()]
    if not files:
        print("  (no files found)")
    else:
        for p in sorted(files):
            rel = p.relative_to(base_dir)
            print(f"  - {rel}")

"""📊 2.5 Registry Summary"""

def print_registry_summary():
    print("📦 Model Registry Summary\n")
    for k, v in MODEL_REGISTRY.items():
        print(f"{k.upper():12s}: {len(v)} models")

print_registry_summary()

# Diagnostic: Base models in diffusion_base and their classification
_diag_files = scan_directory(MODEL_DIRS["diffusion_base"], MODEL_EXTS)
print("\nDiagnostic base models in diffusion_base:")
if not _diag_files:
    print("  (none found)")
else:
    for _p in _diag_files:
        print(f"  {_p.name} -> {classify_model(_p)}")

"""## Model Availability Snapshot (Run to Refresh)

Run the next cell to see what models and ControlNets are already available in this workspace."""

from IPython.display import Markdown, display

def build_registry_snapshot(limit: int = 5) -> str:
    rows = []
    for model_type, entries in MODEL_REGISTRY.items():
        if entries:
            names = ", ".join([e.name for e in entries[:limit]])
            if len(entries) > limit:
                names = f"{names} (+{len(entries) - limit} more)"
        else:
            names = "None"
        rows.append((model_type, len(entries), names))

    lines = ["| Type | Count | Sample |", "| --- | --- | --- |"]
    for model_type, count, names in rows:
        lines.append(f"| {model_type} | {count} | {names} |")
    return "\n".join(lines)

display(Markdown(build_registry_snapshot()))

from pathlib import Path

snapshot_path = Path("model_registry_snapshot.md")
snapshot_path.write_text(build_registry_snapshot(), encoding="utf-8")
print(f"Wrote {snapshot_path}")

"""📄 2.6 Preview Models (Human-Readable)"""

def preview_registry(model_type: str, limit: int = 10):
    entries = MODEL_REGISTRY.get(model_type, [])
    if not entries:
        print(f"No models registered for type: {model_type}")
        return

    print(f"\n{model_type.upper()} MODELS:")
    for e in entries[:limit]:
        print(f" - {e.name} ({e.size_mb} MB)")

preview_registry("sd")
preview_registry("sdxl")
preview_registry("controlnet")
preview_registry("lora")

"""### Recommended Base + ControlNet Sources (SDXL + SD1.5)

Place files in the model folders shown below. Use the optional download section to fetch any URL.

- SDXL base -> models/diffusion_base/sdxl
  https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors
- SDXL ControlNet OpenPose -> models/controlnet
  https://huggingface.co/diffusers/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors
- SDXL ControlNet Depth -> models/controlnet
  https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors
- SDXL ControlNet Normal -> models/controlnet
  https://huggingface.co/diffusers/controlnet-normal-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors

- SD1.5 base -> models/diffusion_base/sd
  https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors
- SD1.5 ControlNet OpenPose -> models/controlnet
  https://huggingface.co/lllyasviel/control_v11p_sd15_openpose/resolve/main/diffusion_pytorch_model.safetensors
- SD1.5 ControlNet Depth -> models/controlnet
  https://huggingface.co/lllyasviel/control_v11f1p_sd15_depth/resolve/main/diffusion_pytorch_model.safetensors
- SD1.5 ControlNet Normal -> models/controlnet
  https://huggingface.co/lllyasviel/control_v11p_sd15_normalbae/resolve/main/diffusion_pytorch_model.safetensors"""

"""⭐ 2.7 Default Model Selection"""

DEFAULT_MODELS = {
    "base_sd": None,
    "base_sdxl": None,
    "sd_controlnet_pose": None,
    "sd_controlnet_depth": None,
    "sd_controlnet_normal": None,
    "sdxl_controlnet_pose": None,
    "sdxl_controlnet_depth": None,
    "sdxl_controlnet_normal": None,
}

def _detect_family_from_entry(entry: ModelEntry) -> str:
    if entry.model_type in {"sd", "sdxl"}:
        return entry.model_type
    lowered = entry.name.lower()
    if "sdxl" in lowered or "sd_xl" in lowered or "sd xl" in lowered:
        return "sdxl"
    if "sd15" in lowered or "sd_1.5" in lowered or "sd-1.5" in lowered:
        return "sd"
    return "unknown"

def select_default(model_type: str, contains: str, family: str | None = None):
    for m in MODEL_REGISTRY.get(model_type, []):
        if contains.lower() in m.name.lower():
            if family:
                m_family = _detect_family_from_entry(m)
                if m_family != family:
                    continue
            return m
    return None

"""Example defaults (adjust names as needed)"""

DEFAULT_MODELS["base_sdxl"] = select_default("sdxl", "base")
DEFAULT_MODELS["base_sd"] = select_default("sd", "v1-5") or select_default("sd", "sd15")

DEFAULT_MODELS["sdxl_controlnet_pose"] = select_default("controlnet", "openpose", "sdxl")
DEFAULT_MODELS["sdxl_controlnet_depth"] = select_default("controlnet", "depth", "sdxl")
DEFAULT_MODELS["sdxl_controlnet_normal"] = (
    select_default("controlnet", "normal", "sdxl")
    or select_default("controlnet", "union", "sdxl")
 )

DEFAULT_MODELS["sd_controlnet_pose"] = select_default("controlnet", "openpose", "sd")
DEFAULT_MODELS["sd_controlnet_depth"] = select_default("controlnet", "depth", "sd")
DEFAULT_MODELS["sd_controlnet_normal"] = select_default("controlnet", "normal", "sd")

ACTIVE_BASE_FAMILY = "sdxl" if DEFAULT_MODELS["base_sdxl"] else "sd" if DEFAULT_MODELS["base_sd"] else None

if ACTIVE_BASE_FAMILY == "sdxl":
    ACTIVE_CONTROLNET_DEFAULTS = {
        "pose": DEFAULT_MODELS["sdxl_controlnet_pose"],
        "depth": DEFAULT_MODELS["sdxl_controlnet_depth"],
        "normal": DEFAULT_MODELS["sdxl_controlnet_normal"],
    }
elif ACTIVE_BASE_FAMILY == "sd":
    ACTIVE_CONTROLNET_DEFAULTS = {
        "pose": DEFAULT_MODELS["sd_controlnet_pose"],
        "depth": DEFAULT_MODELS["sd_controlnet_depth"],
        "normal": DEFAULT_MODELS["sd_controlnet_normal"],
    }
else:
    ACTIVE_CONTROLNET_DEFAULTS = {"pose": None, "depth": None, "normal": None}

print("⭐ Default Model Selection\n")
for k, v in DEFAULT_MODELS.items():
    print(f"{k:22s}: {v.name if v else 'None'}")

print("\nActive base family:", ACTIVE_BASE_FAMILY or "None")

def _detect_family(value) -> str:
    if isinstance(value, ModelEntry):
        if value.model_type in {"sd", "sdxl"}:
            return value.model_type
        lowered = value.name.lower()
    else:
        lowered = str(value).lower()
    if "sdxl" in lowered or "sd_xl" in lowered or "sd xl" in lowered:
        return "sdxl"
    if "sd15" in lowered or "sd_1.5" in lowered or "sd-1.5" in lowered:
        return "sd"
    return "unknown"

def warn_controlnet_compatibility(base_entry, control_entries):
    if base_entry is None:
        print("Base model not set. Skipping compatibility checks.")
        return

    base_family = _detect_family(base_entry)
    if base_family == "unknown":
        print(f"Base model family unknown: {base_entry.name}")
        return

    for key, entry in control_entries.items():
        if entry is None:
            continue
        control_family = _detect_family(entry)
        if control_family == "unknown":
            print(f"ControlNet {key} family unknown: {entry.name}")
            continue
        if control_family != base_family:
            print(
                f"⚠️ ControlNet {key} looks like {control_family} but base is {base_family}. "
                "Expect poor results or load errors."
            )

print("\nCompatibility checks:")
warn_controlnet_compatibility(
    DEFAULT_MODELS.get("base_sdxl"),
    {
        "pose": DEFAULT_MODELS.get("sdxl_controlnet_pose"),
        "depth": DEFAULT_MODELS.get("sdxl_controlnet_depth"),
        "normal": DEFAULT_MODELS.get("sdxl_controlnet_normal"),
    }
)
warn_controlnet_compatibility(
    DEFAULT_MODELS.get("base_sd"),
    {
        "pose": DEFAULT_MODELS.get("sd_controlnet_pose"),
        "depth": DEFAULT_MODELS.get("sd_controlnet_depth"),
        "normal": DEFAULT_MODELS.get("sd_controlnet_normal"),
    }
)

# Runtime configuration
# Set USE_CONTROLNET = True only after a successful base render.
USE_CONTROLNET = False

# Default output size for SDXL without ControlNet
OUTPUT_WIDTH = 768
OUTPUT_HEIGHT = 1024

# Optional: map controlnet keys to HF repo IDs for auto-download
# Example:
# CONTROLNET_REPO_IDS = {
#     "pose": "diffusers/controlnet-openpose-sdxl-1.0",
#     "depth": "diffusers/controlnet-depth-sdxl-1.0",
#     "normal": "diffusers/controlnet-normal-sdxl-1.0",
# }
CONTROLNET_REPO_IDS = {}

# Optional: per-controlnet conditioning scales
CONTROLNET_CONDITIONING_SCALES = {
    "pose": 1.0,
    "depth": 0.8,
    "normal": 0.8,
}

"""# **🔹 SECTION 2.8 — Diffusers Pipeline Initialization (Registry-Driven)**"""

"""**2.8.1 Install Diffusers Stack (Once)**"""

"""To ensure a `pip install` command runs only if necessary, you can check for the presence of a key module before executing the installation. This makes your notebook more efficient and prevents unnecessary re-installations. Here's an example using the `diffusers` library:"""

try:
    import diffusers
    import transformers
    from transformers import CLIPImageProcessor
    print("diffusers/transformers are available.")
except Exception as exc:
    print(f"Updating diffusers stack (missing CLIPImageProcessor): {exc}")
    !pip install -q -U diffusers transformers accelerate xformers safetensors torchvision
    print("Installation complete.")

"""**2.8.2 Imports & Accelerator Setup**"""

import torch
import os
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionControlNetPipeline,
    StableDiffusionXLPipeline,
    StableDiffusionXLControlNetPipeline,
    ControlNetModel
)
from diffusers.utils import load_image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

print(f"Using device: {DEVICE}, dtype: {DTYPE}")

"""**2.8.3 Resolve Base Model from Registry**"""

def require_model(entry, label):
    if entry is None:
        raise RuntimeError(f"Required model missing: {label}")
    return str(entry.path)

def infer_base_family(model_entry):
    if model_entry is None:
        return None
    if model_entry.model_type in {"sd", "sdxl"}:
        return model_entry.model_type
    lowered = model_entry.name.lower()
    if "sdxl" in lowered or "sd_xl" in lowered or "sd xl" in lowered:
        return "sdxl"
    return "sd"


def build_base_model_options():
    options = []
    for model_type in ("sd", "sdxl"):
        for entry in MODEL_REGISTRY.get(model_type, []):
            label = f"{model_type.upper()} • {entry.name} ({entry.size_mb} MB)"
            options.append((label, entry))
    return options


BASE_MODEL_OPTIONS = build_base_model_options()
if not BASE_MODEL_OPTIONS:
    raise RuntimeError("No base SD/SDXL models were found in the model registry.")

try:
    from google.colab import output as colab_output
    colab_output.enable_custom_widget_manager()
except Exception:
    pass

try:
    import ipywidgets as widgets
    from IPython.display import display

    base_model_widget = widgets.Dropdown(
        options=BASE_MODEL_OPTIONS,
        value=(DEFAULT_MODELS["base_sdxl"] or DEFAULT_MODELS["base_sd"] or BASE_MODEL_OPTIONS[0][1]),
        description="Base Model:",
        layout=widgets.Layout(width="95%"),
        style={"description_width": "initial"},
    )

    print("Available base models:")
    for idx, (label, _entry) in enumerate(BASE_MODEL_OPTIONS):
        print(f"  [{idx}] {label}")

    display(base_model_widget)
    print("If no dropdown appears in your environment, set BASE_MODEL_INDEX manually.")

    BASE_MODEL_INDEX = None  # Set to an integer index to force a model in non-widget environments.
    if isinstance(BASE_MODEL_INDEX, int) and 0 <= BASE_MODEL_INDEX < len(BASE_MODEL_OPTIONS):
        SELECTED_BASE_MODEL = BASE_MODEL_OPTIONS[BASE_MODEL_INDEX][1]
        print(f"Using manual base model index: {BASE_MODEL_INDEX}")
    else:
        SELECTED_BASE_MODEL = base_model_widget.value
except Exception as exc:
    print(f"⚠️ ipywidgets unavailable; falling back to automatic model selection. ({exc})")
    print("Available base models:")
    for idx, (label, _entry) in enumerate(BASE_MODEL_OPTIONS):
        print(f"  [{idx}] {label}")
    SELECTED_BASE_MODEL = DEFAULT_MODELS["base_sdxl"] or DEFAULT_MODELS["base_sd"] or BASE_MODEL_OPTIONS[0][1]

BASE_MODEL_PATH = require_model(SELECTED_BASE_MODEL, "Selected base model")
BASE_MODEL_FAMILY = infer_base_family(SELECTED_BASE_MODEL)

if BASE_MODEL_FAMILY == "sdxl":
    SELECTED_CONTROLNET_MODELS = {
        "pose": DEFAULT_MODELS["sdxl_controlnet_pose"],
        "depth": DEFAULT_MODELS["sdxl_controlnet_depth"],
        "normal": DEFAULT_MODELS["sdxl_controlnet_normal"],
    }
else:
    SELECTED_CONTROLNET_MODELS = {
        "pose": DEFAULT_MODELS["sd_controlnet_pose"],
        "depth": DEFAULT_MODELS["sd_controlnet_depth"],
        "normal": DEFAULT_MODELS["sd_controlnet_normal"],
    }

print(f"Selected base model: {SELECTED_BASE_MODEL.name}")
print(f"Detected base family: {BASE_MODEL_FAMILY}")
for c_key, c_entry in SELECTED_CONTROLNET_MODELS.items():
    print(f"ControlNet {c_key:6s}: {c_entry.name if c_entry else 'None'}")

preflight_checks(SELECTED_BASE_MODEL, USE_CONTROLNET, SELECTED_CONTROLNET_MODELS)

"""**2.8.4 Load ControlNet Models (If Available)**"""

CONTROLNETS = {}


def load_controlnet(key, model_entry):
    repo_id = CONTROLNET_REPO_IDS.get(key) if isinstance(CONTROLNET_REPO_IDS, dict) else None

    if model_entry is None and not repo_id:
        print(f"ControlNet {key} not found and no repo id provided.")
        return None

    if model_entry is not None:
        print(f"Loading ControlNet from file: {model_entry.name}")
        try:
            return ControlNetModel.from_single_file(
                model_entry.path,
                torch_dtype=DTYPE,
            )
        except Exception as exc:
            print(
                f"ControlNet {key} single-file load failed: {exc}. "
                "Some SDXL ControlNet weights require a config.json."
            )
            if not repo_id:
                print(
                    "Provide a ControlNet repo id in CONTROLNET_REPO_IDS "
                    "or download the full diffusers folder."
                )
                return None

    if repo_id:
        print(f"Loading ControlNet from repo: {repo_id}")
        try:
            return ControlNetModel.from_pretrained(
                repo_id,
                torch_dtype=DTYPE,
            )
        except Exception as exc:
            print(f"ControlNet {key} repo load failed: {exc}")
            return None

    return None


if USE_CONTROLNET:
    CONTROLNETS["pose"] = load_controlnet("pose", SELECTED_CONTROLNET_MODELS.get("pose"))
    CONTROLNETS["depth"] = load_controlnet("depth", SELECTED_CONTROLNET_MODELS.get("depth"))
    CONTROLNETS["normal"] = load_controlnet("normal", SELECTED_CONTROLNET_MODELS.get("normal"))
    ACTIVE_CONTROLNETS = [cn for cn in CONTROLNETS.values() if cn is not None]
    if not ACTIVE_CONTROLNETS:
        print("No ControlNets loaded. Proceeding without ControlNet.")
else:
    print("USE_CONTROLNET is False. Skipping ControlNet loading.")
    ACTIVE_CONTROLNETS = []

print(f"Active ControlNets: {len(ACTIVE_CONTROLNETS)}")

# ControlNet loading is handled above.

ACTIVE_CONTROLNETS = [cn for cn in CONTROLNETS.values() if cn is not None]
print(f"Active ControlNets: {len(ACTIVE_CONTROLNETS)}")

"""**2.8.5 Initialize the Pipeline**"""

is_single_checkpoint = os.path.isfile(BASE_MODEL_PATH)

if BASE_MODEL_FAMILY == "sdxl":
    if ACTIVE_CONTROLNETS:
        if is_single_checkpoint:
            pipe = StableDiffusionXLControlNetPipeline.from_single_file(
                BASE_MODEL_PATH,
                controlnet=ACTIVE_CONTROLNETS,
                torch_dtype=DTYPE,
                use_safetensors=True,
            )
        else:
            pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
                BASE_MODEL_PATH,
                controlnet=ACTIVE_CONTROLNETS,
                torch_dtype=DTYPE,
                safety_checker=None,
                variant="fp16"
            )
    else:
        if is_single_checkpoint:
            pipe = StableDiffusionXLPipeline.from_single_file(
                BASE_MODEL_PATH,
                torch_dtype=DTYPE,
                use_safetensors=True,
            )
        else:
            pipe = StableDiffusionXLPipeline.from_pretrained(
                BASE_MODEL_PATH,
                torch_dtype=DTYPE,
                safety_checker=None,
                variant="fp16"
            )
else:
    if ACTIVE_CONTROLNETS:
        pipe = StableDiffusionControlNetPipeline.from_single_file(
            BASE_MODEL_PATH,
            controlnet=ACTIVE_CONTROLNETS,
            torch_dtype=DTYPE,
            use_safetensors=True,
        )
    else:
        pipe = StableDiffusionPipeline.from_single_file(
            BASE_MODEL_PATH,
            torch_dtype=DTYPE,
            use_safetensors=True,
        )

pipe.to(DEVICE)

try:
    pipe.enable_xformers_memory_efficient_attention()
    print("✅ xFormers attention enabled.")
except ModuleNotFoundError:
    print("⚠️ xformers is not installed; running without memory-efficient attention.")
except Exception as exc:
    print(f"⚠️ Could not enable xformers attention: {exc}")

try:
    pipe.enable_model_cpu_offload()
except Exception as exc:
    print(f"⚠️ CPU offload could not be enabled: {exc}")


def print_runtime_package_versions():
    import importlib

    packages = [
        "torch",
        "torchvision",
        "xformers",
        "transformers",
        "diffusers",
        "accelerate",
        "bitsandbytes",
    ]

    for package_name in packages:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, "__version__", "unknown")
            print(f"{package_name:14s}: {version}")
        except ModuleNotFoundError:
            print(f"{package_name:14s}: not installed")


print("\nRuntime package versions:")
print_runtime_package_versions()

try:
    import xformers
    print("xformers is already installed.")
except ImportError:
    print("xformers not found, installing...")
    !pip install -q xformers
    print("xformers installation complete.")

"""**2.8.6 Deterministic Seeding (Critical for Identity Work)**"""

import random
import numpy as np

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

"""**2.8.7 Smoke Test (Minimal Render)**"""

set_seed(12345)

prompt = (
    "neutral anatomical reference photograph of an adult human, "
    "standing relaxed, evenly lit, realistic proportions"
)

image = pipe(
    prompt=prompt,
    num_inference_steps=30,
    guidance_scale=5.5,
    width=OUTPUT_WIDTH,
    height=OUTPUT_HEIGHT,
).images[0]

display(image)

"""---

# SECTION 3 — Exploration Mode (Free Variation Playground)

**Purpose:**  
Generate broad anatomical variations to discover promising candidates.

Characteristics:
- Controlled randomness
- No identity locking
- Multiple seeds
- Neutral reference lighting

**Output:**  
A set of candidate images for review."""

"""### Prompt Additions (Optional)

Add extra descriptors separated by commas (e.g., "athletic build, short hair")."""

"""### Quick First Render (No ControlNet)

Run this cell to validate the base pipeline before any ControlNet use."""

# Quick First Render (No ControlNet)
# This cell intentionally avoids ControlNet. If ControlNet is enabled,
# set USE_CONTROLNET=False and re-run Section 2.8 before running this cell.
if ACTIVE_CONTROLNETS:
    print("ControlNet is currently active. Set USE_CONTROLNET=False and re-run Section 2.8 to disable ControlNet.")
else:
    set_seed(20240217)
    quick_prompt = (
        "neutral anatomical reference photograph of an adult human, "
        "standing relaxed, evenly lit, realistic proportions"
    )
    quick_negative = "stylized, cartoon, deformed, extra limbs, low quality, blurry, lowres"
    quick_image = pipe(
        prompt=quick_prompt,
        negative_prompt=quick_negative,
        num_inference_steps=25,
        guidance_scale=5.5,
        width=OUTPUT_WIDTH,
        height=OUTPUT_HEIGHT,
    ).images[0]
    display(quick_image)

try:
    import ipywidgets as widgets
except ImportError:
    print("ipywidgets not found, installing...")
    !pip install -q ipywidgets
    import ipywidgets as widgets

from IPython.display import display

prompt_additions_text = widgets.Textarea(
    value="",
    placeholder="Comma-separated additions for the prompt...",
    description="Prompt +:",
    layout=widgets.Layout(width="80%", height="80px")
)

negative_additions_text = widgets.Textarea(
    value="",
    placeholder="Comma-separated additions for the negative prompt...",
    description="Negative +:",
    layout=widgets.Layout(width="80%", height="80px")
)

run_button = widgets.Button(description="Run", button_style="primary")
run_output = widgets.Output()

PROMPT_ADDITIONS = []
NEGATIVE_PROMPT_ADDITIONS = []

def _parse_additions(text: str):
    return [item.strip() for item in text.split(",") if item.strip()]

def _run_clicked(_):
    global PROMPT_ADDITIONS, NEGATIVE_PROMPT_ADDITIONS
    PROMPT_ADDITIONS = _parse_additions(prompt_additions_text.value)
    NEGATIVE_PROMPT_ADDITIONS = _parse_additions(negative_additions_text.value)
    with run_output:
        run_output.clear_output()
        print("Prompt additions set for next run.")
        print("Negative additions set for next run.")
    prompt_additions_text.value = ""
    negative_additions_text.value = ""

run_button.on_click(_run_clicked)
display(widgets.VBox([prompt_additions_text, negative_additions_text, run_button, run_output]))

from datetime import datetime
from pathlib import Path
import subprocess
import sys
import json

import numpy as np
from IPython.display import display
from PIL import Image, ImageDraw


def ensure_controlnet_aux_installed():
    try:
        import controlnet_aux  # noqa: F401
        print("controlnet_aux is already installed.")
    except ImportError:
        print("Installing controlnet_aux preprocessors...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "controlnet_aux", "opencv-python"])
        print("controlnet_aux installation complete.")


def make_sample_pose_image(width: int = 768, height: int = 1024) -> Image.Image:
    canvas = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(canvas)

    cx = width // 2
    head_r = width // 15
    shoulder_y = int(height * 0.24)
    hip_y = int(height * 0.50)
    knee_y = int(height * 0.72)
    foot_y = int(height * 0.92)

    draw.ellipse((cx - head_r, shoulder_y - 2 * head_r, cx + head_r, shoulder_y), outline=(20, 20, 20), width=12)
    draw.line((cx, shoulder_y, cx, hip_y), fill=(20, 20, 20), width=14)

    arm_span = width // 5
    elbow_drop = height // 10
    hand_drop = height // 7
    draw.line((cx, shoulder_y, cx - arm_span, shoulder_y + elbow_drop), fill=(20, 20, 20), width=12)
    draw.line((cx - arm_span, shoulder_y + elbow_drop, cx - int(arm_span * 0.6), shoulder_y + hand_drop), fill=(20, 20, 20), width=10)
    draw.line((cx, shoulder_y, cx + arm_span, shoulder_y + elbow_drop), fill=(20, 20, 20), width=12)
    draw.line((cx + arm_span, shoulder_y + elbow_drop, cx + int(arm_span * 0.6), shoulder_y + hand_drop), fill=(20, 20, 20), width=10)

    leg_span = width // 10
    draw.line((cx, hip_y, cx - leg_span, knee_y), fill=(20, 20, 20), width=13)
    draw.line((cx - leg_span, knee_y, cx - int(leg_span * 1.3), foot_y), fill=(20, 20, 20), width=11)
    draw.line((cx, hip_y, cx + leg_span, knee_y), fill=(20, 20, 20), width=13)
    draw.line((cx + leg_span, knee_y, cx + int(leg_span * 1.3), foot_y), fill=(20, 20, 20), width=11)

    return canvas


def generate_controlnet_conditioning_maps(source_image: Image.Image):
    from controlnet_aux import MidasDetector, NormalBaeDetector, OpenposeDetector

    openpose_detector = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
    depth_detector = MidasDetector.from_pretrained("lllyasviel/Annotators")
    normal_detector = NormalBaeDetector.from_pretrained("lllyasviel/Annotators")

    pose_map = openpose_detector(source_image)
    depth_map = depth_detector(source_image)
    normal_map = normal_detector(source_image)

    return {
        "pose": pose_map.convert("RGB"),
        "depth": depth_map.convert("RGB"),
        "normal": normal_map.convert("RGB"),
    }


EXPLORATION_DIR = AI_DIRS["images"] / "exploration" / datetime.utcnow().strftime("%Y%m%d_%H%M%S")
EXPLORATION_DIR.mkdir(parents=True, exist_ok=True)

conditioning_by_key = {}
active_controlnet_keys = []
source_image = None
source_path = None

if USE_CONTROLNET:
    ensure_controlnet_aux_installed()
    source_image = make_sample_pose_image(width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT)
    source_path = EXPLORATION_DIR / "controlnet_source_pose.png"
    source_image.save(source_path)
    print(f"Saved source pose image: {source_path}")

    conditioning_by_key = generate_controlnet_conditioning_maps(source_image)
    for key, cond_image in conditioning_by_key.items():
        cond_path = EXPLORATION_DIR / f"conditioning_{key}.png"
        cond_image.save(cond_path)
        print(f"Saved conditioning map ({key}): {cond_path}")

    active_controlnet_keys = [key for key, model in CONTROLNETS.items() if model is not None]
    if active_controlnet_keys:
        print(f"Using ControlNet conditioning maps for: {', '.join(active_controlnet_keys)}")
    else:
        print("No active ControlNets found; exploration will run without ControlNet conditioning.")
else:
    print("USE_CONTROLNET is False. Exploration will run without ControlNet.")

base_prompt = (
    "neutral anatomical reference photograph of an adult human, "
    "standing relaxed, evenly lit, realistic proportions"
)
base_negative_prompt = (
    "stylized, cartoon, exaggerated anatomy, deformed, extra limbs, "
    "low quality, blurry, lowres"
)

prompt_additions = ", ".join(PROMPT_ADDITIONS) if "PROMPT_ADDITIONS" in globals() else ""
negative_additions = ", ".join(NEGATIVE_PROMPT_ADDITIONS) if "NEGATIVE_PROMPT_ADDITIONS" in globals() else ""

prompt = base_prompt + (", " + prompt_additions if prompt_additions else "")
negative_prompt = base_negative_prompt + (", " + negative_additions if negative_additions else "")

seeds = [1001, 1002, 1003, 1004]
num_steps = 30
guidance_scale = 5.5

controlnet_conditioning_images = []
for key in active_controlnet_keys:
    controlnet_conditioning_images.append(conditioning_by_key[key])

results = []
for seed in seeds:
    set_seed(seed)
    call_kwargs = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "num_inference_steps": num_steps,
        "guidance_scale": guidance_scale,
    }

    if controlnet_conditioning_images:
        call_kwargs["image"] = (
            controlnet_conditioning_images[0]
            if len(controlnet_conditioning_images) == 1
            else controlnet_conditioning_images
        )
        cond_w, cond_h = controlnet_conditioning_images[0].size
        call_kwargs["width"] = cond_w
        call_kwargs["height"] = cond_h

        scales = []
        for key in active_controlnet_keys:
            scale = CONTROLNET_CONDITIONING_SCALES.get(key, 1.0)
            scales.append(scale)
        call_kwargs["controlnet_conditioning_scale"] = scales[0] if len(scales) == 1 else scales
    else:
        call_kwargs["width"] = OUTPUT_WIDTH
        call_kwargs["height"] = OUTPUT_HEIGHT
        scales = []

    image = pipe(**call_kwargs).images[0]
    filename = f"candidate_seed_{seed}.png"
    out_path = EXPLORATION_DIR / filename
    image.save(out_path)
    results.append((seed, out_path, image))
    print(f"Saved {out_path}")

# Save generation metadata for reproducibility
meta = {
    "created_at": datetime.utcnow().isoformat() + "Z",
    "base_model_name": SELECTED_BASE_MODEL.name if "SELECTED_BASE_MODEL" in globals() else None,
    "base_model_path": str(SELECTED_BASE_MODEL.path) if "SELECTED_BASE_MODEL" in globals() else None,
    "base_family": BASE_MODEL_FAMILY if "BASE_MODEL_FAMILY" in globals() else None,
    "prompt": prompt,
    "negative_prompt": negative_prompt,
    "num_steps": num_steps,
    "guidance_scale": guidance_scale,
    "seeds": seeds,
    "width": call_kwargs.get("width"),
    "height": call_kwargs.get("height"),
    "use_controlnet": bool(controlnet_conditioning_images),
    "controlnet_keys": list(active_controlnet_keys),
    "controlnet_conditioning_scales": scales,
    "controlnet_source": str(source_path) if source_path else None,
}

meta_path = EXPLORATION_DIR / "generation_meta.json"
meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(f"Wrote {meta_path}")

if source_image is not None:
    for label, preview_img in [("Source", source_image)] + [(k.title(), v) for k, v in conditioning_by_key.items()]:
        print(f"
{label} preview")
        display(preview_img)

for seed, path, image in results:
    display(image)

PROMPT_ADDITIONS = []
NEGATIVE_PROMPT_ADDITIONS = []

from PIL import Image

if not results:
    print("No exploration results found.")
else:
    cols = 2
    rows = (len(results) + cols - 1) // cols
    w, h = results[0][2].size
    grid = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
    for idx, (_, _, img) in enumerate(results):
        r = idx // cols
        c = idx % cols
        grid.paste(img, (c * w, r * h))

    grid_path = EXPLORATION_DIR / "grid.png"
    grid.save(grid_path)
    display(grid)
    print(f"Saved {grid_path}")

import csv

csv_path = EXPLORATION_DIR / "candidates.csv"
with csv_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "seed",
            "image_path",
            "prompt",
            "negative_prompt",
            "num_steps",
            "guidance_scale"
        ]
    )
    writer.writeheader()
    for seed, path, _ in results:
        writer.writerow({
            "seed": seed,
            "image_path": str(path),
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "num_steps": num_steps,
            "guidance_scale": guidance_scale
        })

print(f"Wrote {csv_path}")

"""---

# SECTION 4 — Candidate Selection & Identity Capture

**Purpose:**  
Promote one exploration image into a persistent character.

Steps:
- Select a single candidate image
- Assign a character name / ID
- Extract face embedding
- Capture base seed
- Initialize character directory

**Result:**  
A named character exists for the first time."""

from pathlib import Path
from datetime import datetime
import json
import shutil
import csv

CHARACTER_ROOT = AI_DIRS["datasets"] / "characters"
CHARACTER_ROOT.mkdir(parents=True, exist_ok=True)


def latest_exploration_dir(root_dir: Path | None = None) -> Path:
    root_dir = root_dir or (AI_DIRS["images"] / "exploration")
    if not root_dir.exists():
        raise FileNotFoundError(f"Exploration root not found: {root_dir}")

    dirs = [p for p in root_dir.iterdir() if p.is_dir()]
    if not dirs:
        raise FileNotFoundError(f"No exploration runs found under {root_dir}")

    return sorted(dirs, key=lambda p: p.name, reverse=True)[0]


def get_runtime_versions():
    import importlib

    packages = [
        "torch",
        "torchvision",
        "xformers",
        "transformers",
        "diffusers",
        "accelerate",
        "bitsandbytes",
    ]
    versions = {}
    for package_name in packages:
        try:
            module = importlib.import_module(package_name)
            versions[package_name] = getattr(module, "__version__", "unknown")
        except ModuleNotFoundError:
            versions[package_name] = "not installed"
    return versions


def select_candidate_from_csv(seed_or_index, exploration_dir: Path | None = None):
    exploration_dir = exploration_dir or latest_exploration_dir()
    csv_path = exploration_dir / "candidates.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Candidate CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        raise ValueError(f"No candidates found in {csv_path}")

    # Try matching seed first, then fallback to index
    seed_str = str(seed_or_index)
    selected = None
    for row in rows:
        if str(row.get("seed")) == seed_str:
            selected = row
            break

    if selected is None:
        index = int(seed_or_index)
        if index < 0 or index >= len(rows):
            raise IndexError(f"Candidate index out of range: {index}")
        selected = rows[index]

    image_path = selected["image_path"]

    meta_path = exploration_dir / "generation_meta.json"
    generation_meta = {}
    if meta_path.exists():
        generation_meta = json.loads(meta_path.read_text(encoding="utf-8"))

    generation_meta.update({
        "selected_seed": int(selected.get("seed", 0)),
        "selected_image_path": image_path,
        "prompt": selected.get("prompt"),
        "negative_prompt": selected.get("negative_prompt"),
        "num_steps": int(selected.get("num_steps", 0)),
        "guidance_scale": float(selected.get("guidance_scale", 0)),
    })

    return image_path, generation_meta


def init_character_from_candidate(
    candidate_image_path: str,
    character_id: str,
    base_seed: int,
    notes: str = "",
    metadata: dict | None = None,
    face_embedding=None,
) -> Path:
    candidate_path = Path(candidate_image_path).expanduser()
    if not candidate_path.exists():
        raise FileNotFoundError(f"Candidate image not found: {candidate_path}")

    character_dir = CHARACTER_ROOT / character_id
    if character_dir.exists():
        raise FileExistsError(f"Character already exists: {character_dir}")
    character_dir.mkdir(parents=True, exist_ok=False)

    candidate_name = f"candidate{candidate_path.suffix}"
    candidate_dest = character_dir / candidate_name
    shutil.copy2(candidate_path, candidate_dest)

    embedding_status = "pending"
    embedding_dim = None
    embedding_data = None
    if face_embedding is not None:
        embedding_status = "captured"
        embedding_data = list(face_embedding)
        embedding_dim = len(embedding_data)

    generation_meta = metadata or {}
    if "runtime_versions" not in generation_meta:
        generation_meta["runtime_versions"] = get_runtime_versions()

    metadata_out = {
        "character_id": character_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "candidate_image": candidate_name,
        "base_seed": int(base_seed),
        "notes": notes,
        "embedding_status": embedding_status,
        "embedding_dim": embedding_dim,
        "embedding": embedding_data,
        "generation": generation_meta,
    }

    (character_dir / "character.json").write_text(
        json.dumps(metadata_out, indent=2),
        encoding="utf-8",
    )
    (character_dir / "seed.txt").write_text(str(base_seed), encoding="utf-8")

    print(f"Initialized character at {character_dir}")
    return character_dir

# Option A: Set candidate_image_path manually
candidate_image_path = ""  # e.g., /content/drive/My Drive/AI/Images/exploration/20240101_000000/candidate_seed_1001.png
candidate_metadata = None

# Option B: Pick from latest exploration by seed or index
# candidate_image_path, candidate_metadata = select_candidate_from_csv(1001)  # by seed
# candidate_image_path, candidate_metadata = select_candidate_from_csv(0)     # by index

character_id = "CH-0001"
base_seed = 0
notes = ""

if not candidate_image_path:
    print("Set candidate_image_path or use select_candidate_from_csv and re-run this cell.")
else:
    init_character_from_candidate(
        candidate_image_path=candidate_image_path,
        character_id=character_id,
        base_seed=base_seed,
        notes=notes,
        metadata=candidate_metadata,
    )

"""---

# SECTION 5 — Identity Locking & Invariant Feature Definition

**Purpose:**  
Define what can never change for this character.

Includes:
- Facial geometry lock
- Body proportion constraints
- Invariant skin feature masks
- Identity validation checks

From this point forward, the character is identity-locked.

---

# SECTION 6 — Body Region Map Creation

**Purpose:**  
Divide the body into anatomically meaningful regions for refinement.

Example regions:
- Head
- Neck
- Shoulders
- Chest
- Abdomen
- Hips
- Thighs
- Calves
- Upper arms
- Forearms
- Hands
- Feet

Each region receives a mask or index.

---

# SECTION 7 — Regional Refinement Mode (Anatomical Sculpting)

**Purpose:**  
Iteratively refine anatomy one region at a time.

Workflow:
1. Lock entire body
2. Unlock one region
3. Adjust within realistic bounds
4. Freeze region permanently
5. Move to next region

This mirrors real sculpting discipline.

---

# SECTION 8 — Canonical Body Finalization

**Purpose:**  
Declare the anatomy complete.

Includes:
- Full-body lock
- Cross-pose consistency checks
- Identity snapshot
- Version tagging

After this point, anatomy should not be altered.

---

# SECTION 9 — Pose & Deformation Generation

**Purpose:**  
Generate realistic pose-driven deformation.

Examples:
- Standing
- Sitting
- Walking
- Reaching
- Twisting
- Bending
- Flexing

Rules:
- Deformation allowed
- Identity drift forbidden"""

"""---

# SECTION 10 — Lighting, Camera & Reference Views

**Purpose:**  
Create artist-friendly reference images.

Includes:
- Neutral studio lighting
- Orthographic-like views
- Camera angle sweeps
- Optional dramatic lighting

---

# SECTION 11 — Reference Set Export

**Purpose:**  
Export a complete, organized reference set.

Includes:
- Consistent filenames
- Pose labeling
- Lighting variants
- Metadata files

This output is ready for drawing, modeling, or study.

---

# SECTION 12 — Character Save & Reload System

**Purpose:**  
Persist characters across sessions.

Capabilities:
- Save character state
- Reload identity locks
- Resume rendering
- Continue refinement (if unlocked)

Characters become reusable assets.

---

# SECTION 13 — Scene Rendering (Single Character)

**Purpose:**  
Place a character into an environment while preserving identity.

Examples:
- Sitting on a bench
- Walking through a park
- Standing in conversation
- Environmental interaction

---

# SECTION 14 — Multi-Character Scene Composition

**Purpose:**  
Create scenes involving multiple characters.

Workflow:
1. Load characters independently
2. Generate poses separately
3. Match camera and lighting
4. Composite using depth awareness

Example:
- Character B sitting
- Character F approaching and waving

---

# SECTION 15 — Quality Control & Drift Detection

**Purpose:**  
Ensure long-term identity stability.

Includes:
- Embedding similarity checks
- Visual diffs
- Automated rejection rules
- Manual inspection tools

---

# SECTION 16 — Archive, Export & Versioning

**Purpose:**  
Long-term character management.

Includes:
- Version history
- Anatomy revisions
- Export formats
- Backup strategy

---

# SECTION 17 — Notes, Experiments & Future Extensions

**Purpose:**  
A sandbox for:
- Model upgrades
- New controls
- Experimental ideas
- Deferred features

This section keeps the rest of the notebook clean."""

