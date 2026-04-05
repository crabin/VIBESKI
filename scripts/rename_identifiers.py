"""One-time script: rename secbot/hackbot identifiers to vibeski."""
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent

REPLACEMENTS = [
    # Python packages (order matters — longer first)
    ("hackbot_config", "vibeski_config"),
    ("secbot_cli", "vibeski_cli"),
    # Database file
    ("secbot.db", "vibeski.db"),
    # Entry-point groups
    ("secbot.tools.basic", "vibeski.tools.basic"),
    ("secbot.tools.advanced", "vibeski.tools.advanced"),
    # Env vars (SECBOT_ prefix — do before generic secbot)
    ("SECBOT_TOOL_MODULES_ADVANCED", "VIBESKI_TOOL_MODULES_ADVANCED"),
    ("SECBOT_TOOL_MODULES", "VIBESKI_TOOL_MODULES"),
    ("SECBOT_API_URL", "VIBESKI_API_URL"),
    ("SECBOT_DESKTOP", "VIBESKI_DESKTOP"),
    ("SECBOT_SERVER_HOST", "VIBESKI_SERVER_HOST"),
    ("SECBOT_SERVER_PORT", "VIBESKI_SERVER_PORT"),
    ("SECBOT_SERVER_RELOAD", "VIBESKI_SERVER_RELOAD"),
    # Generic names
    ("secbot-terminal-ui", "vibeski-terminal-ui"),
    ("secbot-cli-server", "vibeski-server"),
    ("hackbot-server", "vibeski-server"),
    ("secbot-server", "vibeski-server"),
    ("secbot-cli", "vibeski"),
    ("hackbot", "vibeski"),
    ("secbot", "vibeski"),
    ("Hackbot", "Vibeski"),
    ("HackBot", "VibeSkiBot"),
    ("HACKBOT", "VIBESKI"),
    ("SECBOT", "VIBESKI"),
]

EXTENSIONS = {".py", ".ts", ".tsx", ".toml", ".json", ".md", ".sh", ".bat", ".ps1", ".txt"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".ruff_cache", "dist", "secbot.egg-info"}

changed = 0
for path in ROOT.rglob("*"):
    if path.is_dir():
        continue
    if any(skip in path.parts for skip in SKIP_DIRS):
        continue
    if path.suffix not in EXTENSIONS:
        continue
    if path.name == "rename_identifiers.py":
        continue

    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue

    new_text = text
    for old, new in REPLACEMENTS:
        new_text = new_text.replace(old, new)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"  updated: {path.relative_to(ROOT)}")
        changed += 1

print(f"\nDone. {changed} files updated.")
