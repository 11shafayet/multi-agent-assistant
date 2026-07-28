"""
MCP server exposing one tool: save_report.
This is the only 'write' capability given to the agent — deliberately narrow
scope instead of raw filesystem access, to demonstrate LLM06 (excessive agency)
mitigation.

Guardrails:
1. Path allowlist   - can only write inside OUTPUTS_DIR, blocks path traversal
2. No silent overwrite - refuses if file exists, unless overwrite=True is passed
3. Action logging   - every attempt (allowed or blocked) is logged with a timestamp
"""

import os
import re
from datetime import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("report-server")

OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

LOG_FILE = OUTPUTS_DIR / "_action_log.txt"


def log_action(message: str) -> None:
    timestamp = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def sanitize_filename(filename: str) -> str:
    filename = os.path.basename(filename)  # strips any directory components
    filename = re.sub(r"[^A-Za-z0-9_\-.]", "_", filename)
    return filename


@mcp.tool()
def save_report(filename: str, content: str, overwrite: bool = False) -> str:
    """Save the final report to a file inside the sandboxed outputs folder.

    Args:
        filename: name for the file, e.g. 'green_tea_report.txt'. No paths allowed.
        content: the text content to write.
        overwrite: must be explicitly True to overwrite an existing file.
    """
    safe_name = sanitize_filename(filename)
    if safe_name != filename:
        log_action(f"SANITIZED - '{filename}' -> '{safe_name}' (traversal or invalid chars stripped)")

    target_path = (OUTPUTS_DIR / safe_name).resolve()

    if OUTPUTS_DIR.resolve() not in target_path.parents and target_path != OUTPUTS_DIR.resolve():
        log_action(f"BLOCKED - path traversal attempt: {filename}")
        return f"BLOCKED: '{filename}' resolves outside the allowed outputs directory."

    if target_path.exists() and not overwrite:
        log_action(f"BLOCKED - overwrite refused (no flag): {safe_name}")
        return f"BLOCKED: '{safe_name}' already exists. Pass overwrite=True to replace it."

    target_path.write_text(content)

    log_action(f"ALLOWED - wrote {len(content)} chars to {safe_name} (overwrite={overwrite})")
    return f"Saved report to {safe_name}"


if __name__ == "__main__":
    mcp.run(transport="stdio")