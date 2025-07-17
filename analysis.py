from fastapi import UploadFile
from typing import List, Tuple, Optional
import pandas as pd
from io import BytesIO
from utils.file_utils import append_row, LOG_FILE


RISK_LEVELS = ["laag", "matig", "verhoogd", "hoog"]


def analyse_bestand(file: UploadFile, vraag: str) -> dict:
    # Simplified placeholder analysis based on file size
    contents = file.file.read()
    grootte = len(contents)
    risico_index = min(grootte % 4, 3)
    risico = RISK_LEVELS[risico_index]
    scenario = {
        "als": vraag,
        "dan": "placeholder scenario",
    }
    aanbevelingen = [f"Aanbeveling {i+1}" for i in range(risico_index + 2)]
    return {
        "bestand": file.filename,
        "risico": risico,
        "scenario": scenario,
        "aanbevelingen": aanbevelingen,
    }


def genereer_rapport(data: dict, formaat: str = "json") -> Tuple[str, bytes]:
    if formaat == "excel":
        buf = BytesIO()
        df = pd.DataFrame([data])
        df.to_excel(buf, index=False)
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", buf.getvalue()
    return "application/json", BytesIO(str(data).encode()).getvalue()


def log_gebruik(user: str, actie: str):
    append_row(LOG_FILE, [user, actie])
