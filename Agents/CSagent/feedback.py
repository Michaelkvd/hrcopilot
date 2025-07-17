from utils.file_utils import append_row, FEEDBACK_FILE


def store_feedback(user: str, feedback: str):
    append_row(FEEDBACK_FILE, [user, feedback])
    return {"status": "opgeslagen"}
