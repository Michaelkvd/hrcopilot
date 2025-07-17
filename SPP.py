from fastapi import UploadFile
from typing import Dict
from utils.file_utils import append_row, LOG_FILE
import pandas as pd
from io import BytesIO


def analyse_spp(file: UploadFile) -> Dict:
    contents = file.file.read()
    # Placeholder: derive counts from file size
    size = len(contents)
    grid = {
        "onderpresteerders": size % 5,
        "generiek": (size // 5) % 5,
        "toppers": (size // 25) % 5,
        "talenten": (size // 125) % 5,
    }
    risico = "hoog" if grid["onderpresteerders"] > 3 else "laag"
    acties = ["Actie 1", "Actie 2"]
    adviezen = ["Advies HR", "Advies management"]
    return {
        "grid": grid,
        "risico": risico,
        "acties": acties,
        "adviezen": adviezen,
    }


def genereer_spp_rapport(data: Dict, formaat: str = "excel") -> BytesIO:
    df = pd.DataFrame([data["grid"]])
    buf = BytesIO()
    if formaat == "excel":
        df.to_excel(buf, index=False)
    else:
        df.to_csv(buf, index=False)
    buf.seek(0)
    return buf


def log_spp(user: str, actie: str):
    append_row(LOG_FILE, [user, actie])
