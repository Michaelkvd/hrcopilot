
from fastapi import UploadFile
from typing import List, Optional, Tuple
import tempfile
import os
import extract_msg

KEYWORDS = [
    "ontslag", "verzuim", "vso", "vaststellingsovereenkomst", "brief",
    "officiële waarschuwing", "beëindiging", "dienstverband", "adviesaanvraag",
    "OVO", "overgang van onderneming", "beding", "leaver"
]
ALGEMENE_JURIDISCHE_BEGRIPPEN = [
    "concurrentiebeding", "relatiebeding", "studiekostenbeding", "arbeidsovereenkomst",
    "proeftijd", "eenzijdige wijziging", "transitievergoeding", "billijke vergoeding",
    "herplaatsing", "getuigschrift", "reorganisatie", "collectief ontslag",
    "disfunctioneren", "opzegtermijn", "op staande voet", "wederzijds goedvinden"
]

BRONNEN_INFO = {
    "wetten.nl": {
        "art. 7:653 BW": "Concurrentiebeding en de juridische voorwaarden voor handhaving.",
        "art. 7:669 BW": "Regels omtrent beëindiging arbeidsovereenkomst door werkgever.",
    },
    "rijksoverheid.nl": {
        "ontslagprocedure": "Beleid, toelichting en stappen rond ontslagprocedures."
    },
    "uwv.nl": {
        "ontslagaanvraag": "Handleiding en formulieren bij ontslagaanvraag wegens langdurig verzuim."
    },
    "ontslag.nl": {
        "algemeen": "Algemene uitleg over ontslag en rechten van werknemer."
    },
    "maxius.nl": {
        "transitievergoeding": "Wettelijke informatie over transitievergoeding bij ontslag."
    }
}

def extract_text_from_input(
    file: Optional[UploadFile] = None,
    input_text: Optional[str] = None
) -> str:
    if input_text and len(input_text) > 20:
        return input_text
    if file:
        if file.filename.endswith(".eml"):
            try:
                from email import policy
                from email.parser import BytesParser

                msg = BytesParser(policy=policy.default).parsebytes(file.file.read())
                if msg.is_multipart():
                    parts = [p.get_content() for p in msg.walk() if p.get_content_type() == "text/plain"]
                    return "\n".join(parts)
                return msg.get_content()
            except Exception:
                return ""
        if file.filename.endswith((".pdf", ".docx", ".doc", ".txt")):
            try:
                return file.file.read().decode("utf-8", errors="ignore")
            except Exception:
                return ""
        if file.filename.endswith(".msg"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".msg") as tmp:
                    tmp.write(file.file.read())
                    tmp.flush()
                    msg = extract_msg.Message(tmp.name)
                    text = f"{msg.subject}\n{msg.body}" if msg.body else msg.subject
                os.unlink(tmp.name)
                return text or ""
            except Exception:
                return ""
    return ""

def flexibele_begrippenherkenning(text: str) -> Tuple[list, list]:
    gevonden_kernwoorden = [word for word in KEYWORDS if word.lower() in text.lower()]
    gevonden_juridische = [begrip for begrip in ALGEMENE_JURIDISCHE_BEGRIPPEN if begrip.lower() in text.lower()]
    return gevonden_kernwoorden, gevonden_juridische

def casus_complexiteit_score(keywords: list, juridische_begrippen: list) -> str:
    totaal = len(keywords) + len(juridische_begrippen)
    if totaal == 0:
        return "eenvoudig"
    elif totaal <= 2:
        return "middelmatig"
    else:
        return "complex"

def bronnen_check(keywords: list, juridische_begrippen: list) -> dict:
    relevante_bronnen = {}
    for bron, artikelen in BRONNEN_INFO.items():
        hits = []
        for trefwoord in keywords + juridische_begrippen:
            for wet, uitleg in artikelen.items():
                if trefwoord.lower() in wet.lower() or trefwoord.lower() in uitleg.lower():
                    hits.append((wet, uitleg))
        if hits:
            relevante_bronnen[bron] = hits
    if not relevante_bronnen:
        relevante_bronnen["wetten.nl"] = [
            ("art. 7:610 BW", "Algemene bepalingen over de arbeidsovereenkomst."),
        ]
    return relevante_bronnen


def genereer_vragen(kernwoorden: List[str], juridische_begrippen: List[str]) -> List[str]:
    vragen: List[str] = []
    if "ontslag" in kernwoorden:
        vragen.append("Welke stappen zijn al ondernomen richting ontslag?")
    if "verzuim" in kernwoorden:
        vragen.append("Is het verzuimprotocol volledig gevolgd?")
    if "concurrentiebeding" in juridische_begrippen:
        vragen.append("Bestaat er een geldig concurrentiebeding in het contract?")
    if not vragen:
        vragen.append("Kunt u extra informatie delen over de situatie?")
    return vragen

def generate_legal_advice(
    kernwoorden: list,
    juridische_begrippen: list,
    bronnen: dict,
    complexiteit: str,
    input_text: str,
    intern_beleid: Optional[str] = None
) -> Tuple[str, str, List[str]]:
    # Flexibele GPT-stijl adviezen
    if not kernwoorden and not juridische_begrippen:
        advies = (
            "Op basis van de aangeleverde informatie zijn er geen duidelijke juridische risico’s gedetecteerd. "
            "Toch is het verstandig om alert te blijven op signalen die alsnog tot juridische vragen kunnen leiden."
        )
        actieplan = (
            "Voor nu zijn er geen directe acties vereist. "
            "Mocht de situatie veranderen of aanvullende informatie beschikbaar komen, heroverweeg dan deze analyse."
        )
        vragen = genereer_vragen(kernwoorden, juridische_begrippen)
        return advies, actieplan, vragen

    # Dynamisch advies op basis van context
    aandachtspunten = kernwoorden + juridische_begrippen
    advies = (
        f"Deze casus bevat juridische aandachtspunten rondom: {', '.join(aandachtspunten)}. "
        f"{'Het betreft een complexe zaak waarbij zorgvuldig handelen essentieel is.' if complexiteit == 'complex' else ''}"
        " Overweeg welke belangen er spelen, raadpleeg waar nodig een jurist en neem voldoende tijd om alle relevante stappen te doorlopen. "
    )
    if intern_beleid:
        advies += f"Neem aanvullend het interne beleid in acht: {intern_beleid} "

    # Dynamisch actieplan
    actieplan = "Een mogelijk vervolgtraject bestaat uit:\n"
    stappen = []
    stappen.append("• Leg alle communicatie en acties volledig vast in het dossier.")
    if complexiteit == "complex":
        stappen.append("• Schakel direct juridische ondersteuning of een HR-expert in.")
    else:
        stappen.append("• Beoordeel of externe ondersteuning noodzakelijk is of dat interne afstemming volstaat.")
    if bronnen:
        stappen.append("• Raadpleeg relevante wet- en regelgeving, bijvoorbeeld:")
        for bron, hits in bronnen.items():
            for wet, uitleg in hits:
                stappen.append(f"   - {bron}: {wet} – {uitleg}")
    else:
        stappen.append("• Controleer of aanvullende bronnen geraadpleegd moeten worden.")
    stappen.append("• Evalueer de situatie regelmatig en pas het plan waar nodig aan.")

    actieplan += "\n".join(stappen)
    vragen = genereer_vragen(kernwoorden, juridische_begrippen)
    return advies, actieplan, vragen

def legalcheck(
    file: Optional[UploadFile] = None,
    input_text: Optional[str] = None,
    intern_beleid: Optional[str] = None
) -> dict:
    text = extract_text_from_input(file=file, input_text=input_text)
    if not text or len(text) < 20:
        return {
            "status": "onvoldoende input",
            "advies": (
                "De aangeleverde input is te beperkt om een juridische beoordeling te kunnen geven. "
                "Lever meer context, een document of aanvullende informatie aan voor een grondige analyse."
            ),
            "actieplan": (
                "Voeg een relevante brief, beleidsstuk of extra context toe zodat een gerichte analyse mogelijk is."
            ),
            "legal_markdown": "## Juridische Analyse\n**Status:** Onvoldoende input voor analyse.\n"
        }

    kernwoorden, juridische_begrippen = flexibele_begrippenherkenning(text)
    complexiteit = casus_complexiteit_score(kernwoorden, juridische_begrippen)
    bronnen = bronnen_check(kernwoorden, juridische_begrippen)
    advies, actieplan, vragen = generate_legal_advice(
        kernwoorden, juridische_begrippen, bronnen, complexiteit, text, intern_beleid
    )

    markdown = f"""## Juridische Analyse
**Herkenbare kernwoorden:** {', '.join(kernwoorden) or 'Geen'}
**Herkenbare juridische begrippen:** {', '.join(juridische_begrippen) or 'Geen'}
**Complexiteit casus:** {complexiteit}
**Advies:**
{advies}
**Actieplan:**
{actieplan}
**Relevante bronnen/artikelen:**
"""
    for bron, hits in bronnen.items():
        for wet, uitleg in hits:
            markdown += f"- **{bron}**: {wet} – {uitleg}\n"
    if not bronnen:
        markdown += "Geen specifieke bronnen gevonden.\n"
    if intern_beleid:
        markdown += f"\n**Interne beleidsinformatie:**\n{intern_beleid}\n"
    if vragen:
        markdown += "\n**Vervolgvragen:**\n"
        for q in vragen:
            markdown += f"- {q}\n"

    return {
        "status": "ok",
        "herkenning_kernwoorden": kernwoorden,
        "herkenning_juridische_begrippen": juridische_begrippen,
        "complexiteit": complexiteit,
        "advies": advies,
        "actieplan": actieplan,
        "bronnen": bronnen,
        "verdiepende_vragen": vragen,
        "legal_markdown": markdown
    }
