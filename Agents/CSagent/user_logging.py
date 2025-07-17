from utils.file_utils import append_row, LOG_FILE

TRIGGERS = {"gebruik", "log", "logging", "audit"}


def match_terms(text: str) -> bool:
    lower = text.lower()
    return any(t in lower for t in TRIGGERS)


def registreer_gebruik(user: str, actie: str):
    append_row(LOG_FILE, [user, actie])
    return {"status": "gelogd"}
