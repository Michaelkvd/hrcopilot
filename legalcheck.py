import os
import requests
from fastapi import UploadFile
from typing import Tuple

KEYWORDS = [
    "ontslag", "verzuim", "vso", "vaststellingsovereenkomst", "brief",
    "officiële waarschuwing", "beëindiging", "dienstverband"
]

def extract_text_from_file(file: UploadFile) -> str:
    # Simpele extensiegebaseerde extractie
    if file.filename.endswith(".pdf"):
        return file.file.read().decode("utf-8", errors="ignore")  # Placeholder
    elif file.filename.endswith(".docx") or file.filename.endswith(".doc"):
        return file.file.read().decode("utf-8", errors="ignore")  # Placeholder
    elif file.filename.endswith(".txt") or file.filename.endswith(".eml"):
        return file.file.read().decode("utf-8", errors="ignore")
    return ""

def detect_legal_issues(text: str) -> list:
    gevonden = []
    for word in KEYWORDS:
        if word.lower() in text.lower():
            gevonden.append(word)
    return gevonden

def query_external_sources(text: str) -> dict:
    # Simulatie van bronverificatie
    return {
        "wetten.nl": "Gevonden relevante wetsartikelen over arbeidsrecht",
        "rijksoverheid.nl": "Beleid m.b.t. ontslagprocedures en verzuim",
        "uwv.nl": "Checklist voor ontslagaanvragen bij langdurig verzuim"
    }

def generate_legal_advice(keywords: list, bronnen: dict) -> Tuple[str, str]:
    if not keywords:
        return ("Laag juridisch risico", "Geen directe actie vereist.")
    advies = f"Er zijn juridische risico's m.b.t. de volgende termen: {', '.join(keywords)}.\n"
    advies += "Controleer of de juiste procedure is gevolgd.\n"
    actieplan = "1. Documenteer correct\n2. Raadpleeg HR of juridisch adviseur\n3. Overweeg hoor-wederhoor"
    return (advies, actieplan)

def legalcheck(file: UploadFile) -> dict:
    text = extract_text_from_file(file)
    if not text:
        return {"fout": "Kon geen tekst extraheren uit bestand."}

    kernwoorden = detect_legal_issues(text)
    bronnen = query_external_sources(text)
    advies, actieplan = generate_legal_advice(kernwoorden, bronnen)

    markdown = f"""## Juridische Analyse\n
**Herkenbare begrippen:** {', '.join(kernwoorden) or 'Geen'}\n
**Advies:**\n{advies}\n
**Actieplan:**\n{actieplan}\n
**Geraadpleegde bronnen:**\n- wetten.nl\n- rijksoverheid.nl\n- uwv.nl\n"""

    return {
        "herkenning": kernwoorden,
        "advies": advies,
        "actieplan": actieplan,
        "bronnen": bronnen,
        "legal_markdown": markdown
    }