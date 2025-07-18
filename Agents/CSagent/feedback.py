from utils.file_utils import append_row, FEEDBACK_FILE
from utils import text_matches

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
    return text_matches(text, TRIGGERS)


def store_feedback(user: str, feedback: str):
    append_row(FEEDBACK_FILE, [user, feedback])
    return {"status": "opgeslagen"}
