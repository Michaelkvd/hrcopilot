from datetime import datetime
from typing import Any, Dict


def format_payload(module: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a simple payload structure for n8n workflows."""
    return {
        "module": module,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }
