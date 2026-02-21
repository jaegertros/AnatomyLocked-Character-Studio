from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import uuid
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def patch_workflow_nodes(
    workflow: dict[str, Any],
    node_overrides: dict[str | int, dict[str, Any]] | None,
) -> dict[str, Any]:
    if not node_overrides:
        return workflow

    patched = json.loads(json.dumps(workflow))
    nodes = patched.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError("Workflow missing nodes array.")

    normalized: dict[str, dict[str, Any]] = {}
    for key, value in node_overrides.items():
        normalized[str(key)] = value

    for node in nodes:
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("id"))
        override = normalized.get(node_id)
        if not isinstance(override, dict):
            continue

        if "widgets_values" in override:
            widget_override = override["widgets_values"]
            if isinstance(widget_override, list):
                node["widgets_values"] = widget_override
            elif isinstance(widget_override, dict):
                existing = list(node.get("widgets_values") or [])
                for index_key, widget_value in widget_override.items():
                    index = int(index_key)
                    if index < 0:
                        raise ValueError(f"widgets_values index must be >= 0 for node {node_id}")
                    while len(existing) <= index:
                        existing.append(None)
                    existing[index] = widget_value
                node["widgets_values"] = existing
            else:
                raise TypeError("widgets_values override must be list or dict")

        if "title" in override:
            node["title"] = override["title"]

    return patched


@dataclass
class ComfyRunResult:
    stage: str
    prompt_id: str
    queued_at: str
    completed_at: str
    history: dict[str, Any]


class ComfyApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8188") -> None:
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = None
        headers = {"Content-Type": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        request = Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=60) as response:
                body = response.read().decode("utf-8")
            if not body:
                return {}
            parsed = json.loads(body)
            if not isinstance(parsed, dict):
                raise ValueError("Comfy API returned a non-object JSON payload")
            return parsed
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Comfy API HTTP error {exc.code} at {path}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Comfy API unreachable at {self.base_url}: {exc}") from exc

    def queue_prompt(self, workflow: dict[str, Any], client_id: str) -> tuple[str, dict[str, Any]]:
        response = self._request("POST", "/prompt", {"prompt": workflow, "client_id": client_id})
        prompt_id = response.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id:
            raise RuntimeError(f"Comfy API did not return prompt_id: {response}")
        return prompt_id, response

    def get_history(self, prompt_id: str) -> dict[str, Any] | None:
        response = self._request("GET", f"/history/{prompt_id}")
        run_entry = response.get(prompt_id)
        if isinstance(run_entry, dict):
            return run_entry
        return None

    def wait_for_completion(
        self,
        prompt_id: str,
        *,
        timeout_seconds: int = 1200,
        poll_seconds: float = 1.5,
    ) -> dict[str, Any]:
        started = time.time()
        while True:
            history = self.get_history(prompt_id)
            if history is not None:
                return history
            elapsed = time.time() - started
            if elapsed >= timeout_seconds:
                raise TimeoutError(f"Timed out waiting for prompt {prompt_id} after {timeout_seconds}s")
            time.sleep(poll_seconds)

    def run_workflow(
        self,
        *,
        workflow: dict[str, Any],
        stage: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        patched_workflow = patch_workflow_nodes(workflow, node_overrides)
        client_id = str(uuid.uuid4())
        queued_at = utc_now_iso()
        prompt_id, _ = self.queue_prompt(patched_workflow, client_id=client_id)
        history = self.wait_for_completion(prompt_id, timeout_seconds=timeout_seconds)
        return ComfyRunResult(
            stage=stage,
            prompt_id=prompt_id,
            queued_at=queued_at,
            completed_at=utc_now_iso(),
            history=history,
        )


class CharacterStateStore:
    def __init__(self, characters_root: Path) -> None:
        self.characters_root = Path(characters_root)

    def character_dir(self, character_id: str) -> Path:
        path = self.characters_root / character_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def character_json_path(self, character_id: str) -> Path:
        return self.character_dir(character_id) / "character.json"

    def load_record(self, character_id: str) -> dict[str, Any]:
        path = self.character_json_path(character_id)
        if not path.exists():
            return {
                "character_id": character_id,
                "created_at": utc_now_iso(),
                "orchestration": {
                    "schema_version": "orchestration.v1",
                    "runs": [],
                },
            }
        payload = load_json(path)
        payload.setdefault("character_id", character_id)
        payload.setdefault("orchestration", {"schema_version": "orchestration.v1", "runs": []})
        payload["orchestration"].setdefault("schema_version", "orchestration.v1")
        payload["orchestration"].setdefault("runs", [])
        return payload

    def save_record(self, character_id: str, record: dict[str, Any]) -> Path:
        path = self.character_json_path(character_id)
        save_json(path, record)
        return path

    def append_run(self, character_id: str, run: ComfyRunResult) -> Path:
        record = self.load_record(character_id)
        orchestration = record.setdefault("orchestration", {"schema_version": "orchestration.v1", "runs": []})
        runs = orchestration.setdefault("runs", [])
        runs.append(
            {
                "stage": run.stage,
                "prompt_id": run.prompt_id,
                "queued_at": run.queued_at,
                "completed_at": run.completed_at,
                "history": run.history,
            }
        )
        orchestration["updated_at"] = utc_now_iso()
        record["orchestration"] = orchestration
        return self.save_record(character_id, record)


class AnatomyLockedPipelineOrchestrator:
    def __init__(
        self,
        *,
        repo_root: Path,
        characters_root: Path,
        workflows_dir: Path | None = None,
        comfy_base_url: str = "http://127.0.0.1:8188",
    ) -> None:
        self.repo_root = Path(repo_root)
        self.workflows_dir = Path(workflows_dir) if workflows_dir else self.repo_root / "OtherSetups"
        self.state_store = CharacterStateStore(Path(characters_root))
        self.comfy = ComfyApiClient(comfy_base_url)

    def _workflow_path(self, filename: str) -> Path:
        path = self.workflows_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Workflow not found: {path}")
        return path

    def _load_workflow(self, filename: str) -> dict[str, Any]:
        return load_json(self._workflow_path(filename))

    def run_phase1_exploration(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow("phase1_exploration.json")
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage="phase1_exploration",
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run

    def run_phase2_identity_lock(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow("phase2_identity_lock.json")
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage="phase2_identity_lock",
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run

    def run_phase3_regional_refinement(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow("phase3_regional_refinement_inpaint.json")
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage="phase3_regional_refinement",
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run

    def run_phase4_canonical_finalization(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow("phase4_canonical_finalization.json")
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage="phase4_canonical_finalization",
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run

    def run_phase5_reference_variants(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        """Backward-compatible wrapper for the Section 10 reference views stage."""
        return self.run_phase5_section10_reference_views(
            character_id=character_id,
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )

    def run_phase5_section10_reference_views(
        self,
        *,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow("section10_reference_views.json")
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage="section10_reference_views",
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run

    def run_named_workflow(
        self,
        *,
        workflow_filename: str,
        stage_name: str,
        character_id: str,
        node_overrides: dict[str | int, dict[str, Any]] | None = None,
        timeout_seconds: int = 1200,
    ) -> ComfyRunResult:
        workflow = self._load_workflow(workflow_filename)
        run = self.comfy.run_workflow(
            workflow=workflow,
            stage=stage_name,
            node_overrides=node_overrides,
            timeout_seconds=timeout_seconds,
        )
        self.state_store.append_run(character_id, run)
        return run
