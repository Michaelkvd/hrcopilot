"""Functies voor het behandelen van verzuimcasuïstiek en vragen."""
from typing import Optional


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
