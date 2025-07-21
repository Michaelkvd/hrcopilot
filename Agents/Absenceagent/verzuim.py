"""Functies voor het behandelen van verzuimcasuïstiek en vragen."""
from typing import Optional

from utils import text_matches, format_payload

# Kernwoorden die semantisch gerelateerd zijn aan verzuim. Worden gebruikt om
# te bepalen of deze module relevant is voor een binnengekomen vraag.
TRIGGERS = {
    "verzuim",
    "ziekte",
    "absentie",
    "re-integratie",
    "ziekmelding",
    "poortwachter",
    "arbodienst",
    "arbeidsongeschiktheid",
}


def match_terms(text: str) -> bool:
    """Return ``True`` if the text is gerelateerd aan verzuim."""
    return text_matches(text, TRIGGERS)


def beantwoord_vraag(vraag: str, dossier: Optional[str] = None) -> str:
    """Geef flexibel advies bij een verzuimvraag."""
    lower = vraag.lower()
    if "protocol" in lower:
        return "Raadpleeg het verzuimprotocol en leg afspraken vast in het dossier."
    if "wet" in lower or "wetgeving" in lower:
        return "Controleer de toepasselijke wet- en regelgeving rondom arbeidsongeschiktheid."
    return (
        "Elke situatie is uniek. Bespreek de casus met de medewerker en overweeg "
        "consultatie van de arbodienst of jurist voor passend advies."
    )


def analyse_tekst(text: str, periode: Optional[str] = None) -> dict:
    """Analyseer tekstuele input als ware het een document."""

    from Agents.Analysisagent import analysis as analysis_mod

    contents = text.encode()
    return analysis_mod.analyse_verzuim("tekst-input", contents, periode=periode)


def advies_niveaus(vraag: str, dossier: Optional[str] = None) -> dict:
    """Geef advies op operationeel, tactisch en strategisch niveau."""

    basis = beantwoord_vraag(vraag, dossier)
    return {
        "operationeel": basis,
        "tactisch": (
            "Analyseer verzuimpatronen, stem af met leidinggevenden en stuur bij "
            "waar nodig."
        ),
        "strategisch": (
            "Koppel verzuimcijfers aan bedrijfsdoelen en ontwikkel preventief beleid."
        ),
    }


def n8n_payload(vraag: str, dossier: Optional[str] = None) -> dict:
    """Retourneer een n8n-geschikte payload met adviesniveaus."""

    data = advies_niveaus(vraag, dossier)
    return format_payload("verzuim", data)
