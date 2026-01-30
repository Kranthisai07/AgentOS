from __future__ import annotations

import re
import urllib.request
from typing import Any, Dict

from .base import Tool, ToolError, ToolResponse, require_keys


_CHARSET_RE = re.compile(r"charset=([\w-]+)", re.IGNORECASE)


class HttpClientTool(Tool):
    name = "http_client"
    description = "HTTP client for safe GET requests."

    def handle(self, **kwargs: Any) -> ToolResponse:
        try:
            require_keys(kwargs, ["op"])
            op = kwargs["op"]
            if op == "get":
                return self._get(kwargs)
            raise ToolError(f"Unsupported op: {op}")
        except ToolError as exc:
            return ToolResponse(ok=False, data={}, error=str(exc))

    def _get(self, payload: Dict[str, Any]) -> ToolResponse:
        require_keys(payload, ["url"])
        url = payload["url"]
        timeout = float(payload.get("timeout", 10))
        max_bytes = int(payload.get("max_bytes", 100_000))

        request = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(max_bytes + 1)
            truncated = len(raw) > max_bytes
            if truncated:
                raw = raw[:max_bytes]

            content_type = response.headers.get("Content-Type", "")
            encoding = self._extract_charset(content_type) or "utf-8"
            text = raw.decode(encoding, errors="replace")

            return ToolResponse(
                ok=True,
                data={
                    "url": url,
                    "status": response.status,
                    "headers": dict(response.headers.items()),
                    "content_type": content_type,
                    "truncated": truncated,
                    "body": text,
                },
            )

    def _extract_charset(self, content_type: str) -> str | None:
        match = _CHARSET_RE.search(content_type)
        if not match:
            return None
        return match.group(1)
