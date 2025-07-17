from fastapi import UploadFile
from typing import Dict
from utils.file_utils import append_row, LOG_FILE
import pandas as pd
from io import BytesIO


def analyse_spp(file: UploadFile) -> Dict:

    """Analyseer SPP-data en geef een volledige 9-box grid terug."""

    contents = file.file.read()
    buf = BytesIO(contents)
    try:
        df = pd.read_excel(buf)
    except Exception:
        buf.seek(0)
        df = pd.read_csv(buf)

    grid_keys = [
        "laag_potentieel_lage_prestatie",
        "laag_potentieel_midden_prestatie",
        "laag_potentieel_hoge_prestatie",
        "midden_potentieel_lage_prestatie",
        "midden_potentieel_midden_prestatie",
        "midden_potentieel_hoge_prestatie",
        "hoog_potentieel_lage_prestatie",
        "hoog_potentieel_midden_prestatie",
        "hoog_potentieel_hoge_prestatie",
    ]

    grid = {k: 0 for k in grid_keys}

    norm_cols = {c.strip().lower().replace(" ", "_"): c for c in df.columns}
    for key in grid_keys:
        if key in norm_cols:
            grid[key] = int(df[norm_cols[key]].sum())

    if all(v == 0 for v in grid.values()):
        numeric = df.select_dtypes(include="number").values.flatten()
        for i, key in enumerate(grid_keys):
            if i < len(numeric):
                grid[key] = int(numeric[i])

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

=======
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
main
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
