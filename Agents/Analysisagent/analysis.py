from fastapi import UploadFile
from typing import Iterable, List, Tuple, Optional, Dict
import pandas as pd
from io import BytesIO
from datetime import datetime
import random
from utils.file_utils import append_row, LOG_FILE


RISK_LEVELS = ["laag", "matig", "verhoogd", "hoog"]


def analyse_bestand(file: UploadFile, vraag: str) -> dict:
    """Analyse a single file based on size and return risk information."""

    contents = file.file.read()
    file.file.seek(0)
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


def get_latest_cbs_quarter() -> str:
    """Return the most recent fully completed CBS quarter as ``YYYYKWX``."""

    today = datetime.now()
    year, month = today.year, today.month

    quarter = (month - 1) // 3 + 1
    if quarter == 1:
        return f"{year - 1}KW4"
    return f"{year}KW{quarter - 1}"


def bepaal_risico(verzuimpercentage: float) -> str:
    """Classificeer het verzuimrisico op basis van het percentage."""

    if verzuimpercentage > 5:
        return "hoog"
    if verzuimpercentage < 3:
        return "laag"
    return "matig"


def genereer_aanbevelingen(risico: str) -> str:
    """Geeft beknopte vervolgstappen voor het opgegeven risiconiveau."""

    if risico == "laag":
        return (
            "Het risico is laag. Blijf periodiek de cijfers monitoren en houd"
            " contact met medewerkers over eventueel beginnende klachten."
        )

    opties_matig = [
        "Voer een verdiepend onderzoek uit naar frequente verzuimoorzaken",
        "Plan individuele verzuimgesprekken om knelpunten te achterhalen",
        "Inventariseer mogelijkheden voor preventief gezondheidsbeleid",
    ]
    opties_hoog = [
        "Start een intensief re-integratietraject met betrokkenheid van de bedrijfsarts",
        "Stel een concreet actieplan op om langdurig verzuim terug te dringen",
        "Onderzoek aanvullende ondersteuning zoals arbeidsdeskundig advies",
    ]

    random.seed(risico)
    keuzes = opties_matig if risico == "matig" else opties_hoog
    adviezen = "; ".join(random.sample(keuzes, k=2))
    return f"Mogelijke vervolgstappen: {adviezen}"


def haal_branchenorm(periode: str | None = None) -> dict:
    """Simuleer een algemene branchenorm zonder specifieke codes."""

    if periode is None:
        periode = get_latest_cbs_quarter()

    return {
        "periode": periode,
        "waarde": 4.0,
    }


def analyse_verzuim(
    filename: str,
    contents: bytes,
    periode: str | None = None,
) -> dict:
    """Analyse a single file and return placeholder data with risk advice."""

    if periode is None:
        periode = get_latest_cbs_quarter()

    verzuimpercentage = round(2 + (len(contents) % 8) * 0.5, 2)

    branche_benchmark = haal_branchenorm(periode)
    risico = bepaal_risico(verzuimpercentage)
    advies = genereer_aanbevelingen(risico)
    beleidsadvies = (
        f"Het verzuimpercentage bedraagt {verzuimpercentage}. "
        "Overweeg teaminterventie of coachingsinzet."
    )

    return {
        "filename": filename,
        "periode": periode,
        "verzuimpercentage": verzuimpercentage,
        "branche_benchmark": branche_benchmark,
        "risico": risico,
        "advies": advies,
        "beleidsadvies": beleidsadvies,
        "resultaat": "Analyse nog niet geïmplementeerd",
    }


def analyse_meerdere(files: Iterable[Tuple[str, bytes]]) -> List[dict]:
    """Analyse multiple ``(filename, content)`` tuples."""

    return [analyse_verzuim(fn, data) for fn, data in files]


def patroon_analyse(files: Iterable[Tuple[str, bytes]]) -> dict:
    maanden = len(files)
    frequentie = sum(len(c) for _, c in files) % 10
    langdurig = [name for name, c in files if len(c) % 5 == 0]
    return {
        "maanden": maanden,
        "meldingsfrequentie": frequentie,
        "langdurige_dossiers": langdurig,
    }


def genereer_pdf(markdown: str) -> bytes:
    """Render markdown to PDF and return the binary data."""

    from weasyprint import HTML

    html = HTML(string=markdown.replace("\n", "<br>"))
    return html.write_pdf()


def genereer_grafiek(data: dict):
    """Create a simple bar chart comparing internal data with a benchmark."""

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.bar(
        ["Intern", "Benchmark"],
        [
            data.get("verzuimpercentage", 0),
            data.get("branche_benchmark", {}).get("waarde", 0),
        ],
    )
    ax.set_title("Verzuim vs Benchmark")
    return fig


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

    onderpresteerders = (
        grid["laag_potentieel_lage_prestatie"]
        + grid["midden_potentieel_lage_prestatie"]
        + grid["hoog_potentieel_lage_prestatie"]
    )
    risico = "hoog" if onderpresteerders > 4 else "laag" if onderpresteerders < 2 else "matig"

    acties = ["Voer ontwikkelgesprekken", "Bekijk herplaatsingsmogelijkheden"]
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
