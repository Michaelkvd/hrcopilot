from utils.file_utils import append_row, LOG_FILE


def registreer_gebruik(user: str, actie: str):
    append_row(LOG_FILE, [user, actie])
    return {"status": "gelogd"}
