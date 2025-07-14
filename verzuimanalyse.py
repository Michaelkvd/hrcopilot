import io
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation

def extract_text_from_file(filename, contents):
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(contents))
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(contents))
        return " ".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".pptx"):
        prs = Presentation(io.BytesIO(contents))
        text_runs = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text_runs.append(shape.text)
        return " ".join(text_runs)
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))
        return df.to_string()
    else:
        return ""

def analyse_verzuim(filename, contents):
    tekst = extract_text_from_file(filename, contents).lower()

    kernwoorden = ["verzuim", "ziekmelding", "verzuimpercentage", "langdurig", "kort verzuim", "ziekteverzuim"]
    herkenning = [kw for kw in kernwoorden if kw in tekst]

    # Simulatie: verzuimpercentage herkennen (placeholder)
    verzuimpercentage = 5.2 if "verzuim" in tekst else 2.5

    # Risicobepaling
    if verzuimpercentage > 5:
        risico = "hoog"
        advies = "Voer een diepgaande verzuimanalyse uit en betrek de bedrijfsarts."
    elif verzuimpercentage < 3:
        risico = "laag"
        advies = "Behoud huidige maatregelen, monitor preventief."
    else:
        risico = "matig"
        advies = "Analyseer knelpunten, verhoog inzet op preventie en dialoog."

    # Simulatie benchmark (placeholder)
    benchmark_sbi = {
        "6420": 3.8,
        "6622": 4.2
    }

    return {
        "kernwoorden_herkend": herkenning,
        "verzuimpercentage": verzuimpercentage,
        "risiconiveau": risico,
        "advies": advies,
        "cbs_benchmark": benchmark_sbi,
        "vergelijking_met_cbs": {
            "6420": f"{verzuimpercentage - benchmark_sbi['6420']:.1f}%",
            "6622": f"{verzuimpercentage - benchmark_sbi['6622']:.1f}%"
        }
    }
