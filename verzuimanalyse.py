from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Tuple


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


def analyse_verzuim(
    filename: str,
    contents: bytes,
    sbi_code: str = "6420",
    periode: str | None = None,
) -> dict:
    """Analyse a single file and return placeholder data."""

    if periode is None:
        periode = get_latest_cbs_quarter()

    return {
        "filename": filename,
        "sbi_code": sbi_code,
        "periode": periode,
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
