from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Tuple
import random


def get_latest_cbs_quarter() -> str:
    """Return the most recent fully completed CBS quarter as ``YYYYKWX``."""

    today = datetime.now()
    year = today.year
    month = today.month

    # Determine current quarter.
    if 1 <= month <= 3:
        quarter = 1
    elif 4 <= month <= 6:
        quarter = 2
    elif 7 <= month <= 9:
        quarter = 3
    else:
        quarter = 4

    # Move one quarter back to get the last completed quarter.
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


def haal_cbs_benchmark(periode: str | None = None) -> dict:
    """Simuleer een CBS benchmark voor SBI-codes 6420 en 6622."""

    if periode is None:
        periode = get_latest_cbs_quarter()

    # Placeholder waarde, in een echte implementatie zou data via een API
    # van het CBS worden opgehaald.
    return {
        "sbi_codes": ["6420", "6622"],
        "periode": periode,
        "waarde": 4.0,
    }


def analyse_verzuim(
    filename: str,
    contents: bytes,
    sbi_code: str = "6420",
    periode: str | None = None,
) -> dict:
    """Analyse a single file and return placeholder data with risk advice."""

    if periode is None:
        periode = get_latest_cbs_quarter()

    # Placeholder berekening van het verzuimpercentage op basis van de
    # bestandslengte zodat de uitkomst deterministisch is in tests.
    verzuimpercentage = round(2 + (len(contents) % 8) * 0.5, 2)

    cbs_benchmark = haal_cbs_benchmark(periode)
    risico = bepaal_risico(verzuimpercentage)
    advies = genereer_aanbevelingen(risico)

    return {
        "filename": filename,
        "sbi_code": sbi_code,
        "periode": periode,
        "verzuimpercentage": verzuimpercentage,
        "cbs_benchmark": cbs_benchmark,
        "risico": risico,
        "advies": advies,
        "resultaat": "Analyse nog niet geïmplementeerd",
    }

def analyse_meerdere(files: Iterable[Tuple[str, bytes]]) -> List[dict]:
    """Analyse multiple ``(filename, content)`` tuples."""

    results: List[dict] = []
    for filename, content in files:
        results.append(analyse_verzuim(filename, content))
    return results

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
            data.get("cbs_benchmark", {}).get("waarde", 0),
        ],
    )
    ax.set_title("Verzuim vs Benchmark")
    return fig
