from utils.file_utils import append_row, LOG_FILE
from utils import text_matches

TRIGGERS = {"gebruik", "log", "logging", "audit"}


def match_terms(text: str) -> bool:
    return text_matches(text, TRIGGERS)


def registreer_gebruik(user: str, actie: str):
    append_row(LOG_FILE, [user, actie])
    return {"status": "gelogd"}
