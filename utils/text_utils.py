from typing import Iterable


def text_matches(text: str, triggers: Iterable[str]) -> bool:
    """Return True if any trigger is present in lowercase ``text``."""
    lower = text.lower()
    return any(t in lower for t in triggers)
