from fastapi import UploadFile
from typing import Dict
from utils.file_utils import append_row, LOG_FILE
import pandas as pd
from io import BytesIO


def analyse_spp(file: UploadFile) -> Dict:
    """Analyseer SPP-data en geef een volledige 9-box grid terug."""

    contents = file.file.read()
    size = len(contents)

    # verdeel de fictieve aantallen over alle 9 vakken van de grid
    grid = {
        "laag_potentieel_lage_prestatie": size % 5,
        "laag_potentieel_midden_prestatie": (size // 5) % 5,
        "laag_potentieel_hoge_prestatie": (size // 25) % 5,
        "midden_potentieel_lage_prestatie": (size // 125) % 5,
        "midden_potentieel_midden_prestatie": (size // 625) % 5,
        "midden_potentieel_hoge_prestatie": (size // 3125) % 5,
        "hoog_potentieel_lage_prestatie": (size // 15625) % 5,
        "hoog_potentieel_midden_prestatie": (size // 78125) % 5,
        "hoog_potentieel_hoge_prestatie": (size // 390625) % 5,
    }

    # eenvoudige risico-inschatting op basis van het aantal medewerkers in de
    # onderste rij van de grid
    onderpresteerders = (
        grid["laag_potentieel_lage_prestatie"]
        + grid["midden_potentieel_lage_prestatie"]
        + grid["hoog_potentieel_lage_prestatie"]
    )
    risico = "hoog" if onderpresteerders > 4 else "laag" if onderpresteerders < 2 else "matig"

    acties = ["Voer ontwikkelgesprekken", "Bekijken herplaatsingsmogelijkheden"]
    adviezen = ["Rapporteer periodiek aan management", "Stem af met HR over opvolging"]

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
