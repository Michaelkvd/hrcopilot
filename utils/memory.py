from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

UTILS_DIR = Path(__file__).resolve().parent
MEMORY_FILE = UTILS_DIR / "memory.json"


class Memory:
    """Simple persistent memory storage using a JSON file."""

    def __init__(self, path: Path | None = None):
        self.path = path or MEMORY_FILE
        self.data: dict[str, list[dict]] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text())
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data))

    def add(self, user: str, entry: dict) -> None:
        """Add an entry for ``user`` and persist it."""
        self.data.setdefault(user, []).append(
            {"timestamp": datetime.utcnow().isoformat(), **entry}
        )
        self._save()

    def get(self, user: str) -> list[dict]:
        return self.data.get(user, [])
