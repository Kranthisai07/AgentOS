# AgentOS

AgentOS is an MCP-native, OS-style runtime for autonomous multi-agent LLM workflows.
This repository starts with foundational tool drivers and will grow into a research
prototype covering kernel scheduling, hierarchical memory, and safety enforcement.

## Current status

- Filesystem tool driver
- HTTP client tool driver

## Quick usage (Python)

```python
from agentos.tools import FilesystemTool, HttpClientTool

fs = FilesystemTool(root_dir=".")
print(fs.handle(op="list_dir", path="."))

http = HttpClientTool()
print(http.handle(op="get", url="https://example.com"))
```
