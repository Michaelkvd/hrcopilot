from utils.file_utils import append_row, FEEDBACK_FILE

# Termen die gebruikt kunnen worden om feedback- of logfunctionaliteit op te roepen.
TRIGGERS = {
    "feedback",
    "review",
    "opmerking",
    "logging",
    "logboek",
    "gebruik",
}


def match_terms(text: str) -> bool:
    """Return ``True`` if the text lijkt betrekking te hebben op feedback of logging."""
    lower = text.lower()
    return any(t in lower for t in TRIGGERS)


def store_feedback(user: str, feedback: str):
    append_row(FEEDBACK_FILE, [user, feedback])
    return {"status": "opgeslagen"}
