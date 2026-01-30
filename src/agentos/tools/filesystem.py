from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .base import Tool, ToolError, ToolResponse, require_keys


class FilesystemTool(Tool):
    name = "filesystem"
    description = "Filesystem access with root path sandboxing."

    def __init__(self, root_dir: str | Path) -> None:
        self._root = Path(root_dir).resolve()

    def handle(self, **kwargs: Any) -> ToolResponse:
        try:
            require_keys(kwargs, ["op"])
            op = kwargs["op"]
            if op == "read_file":
                return self._read_file(kwargs)
            if op == "write_file":
                return self._write_file(kwargs)
            if op == "list_dir":
                return self._list_dir(kwargs)
            if op == "mkdir":
                return self._mkdir(kwargs)
            if op == "delete_file":
                return self._delete_file(kwargs)
            raise ToolError(f"Unsupported op: {op}")
        except ToolError as exc:
            return ToolResponse(ok=False, data={}, error=str(exc))

    def _resolve(self, rel_path: str) -> Path:
        target = (self._root / rel_path).resolve()
        if self._root not in target.parents and target != self._root:
            raise ToolError("Path escapes tool root")
        return target

    def _read_file(self, payload: Dict[str, Any]) -> ToolResponse:
        require_keys(payload, ["path"])
        target = self._resolve(payload["path"])
        if not target.exists() or not target.is_file():
            raise ToolError("File not found")
        content = target.read_text(encoding="utf-8", errors="replace")
        return ToolResponse(ok=True, data={"path": str(target), "content": content})

    def _write_file(self, payload: Dict[str, Any]) -> ToolResponse:
        require_keys(payload, ["path", "content"])
        target = self._resolve(payload["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(payload["content"]), encoding="utf-8")
        return ToolResponse(ok=True, data={"path": str(target)})

    def _list_dir(self, payload: Dict[str, Any]) -> ToolResponse:
        rel = payload.get("path", ".")
        target = self._resolve(rel)
        if not target.exists() or not target.is_dir():
            raise ToolError("Directory not found")
        entries: List[str] = [p.name for p in target.iterdir()]
        return ToolResponse(ok=True, data={"path": str(target), "entries": entries})

    def _mkdir(self, payload: Dict[str, Any]) -> ToolResponse:
        require_keys(payload, ["path"])
        target = self._resolve(payload["path"])
        target.mkdir(parents=True, exist_ok=True)
        return ToolResponse(ok=True, data={"path": str(target)})

    def _delete_file(self, payload: Dict[str, Any]) -> ToolResponse:
        require_keys(payload, ["path"])
        target = self._resolve(payload["path"])
        if not target.exists() or not target.is_file():
            raise ToolError("File not found")
        target.unlink()
        return ToolResponse(ok=True, data={"path": str(target)})
