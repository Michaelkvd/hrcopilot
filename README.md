# Verzuimanalyse Module (FastAPI)

Deze module maakt een verzuimanalyse op basis van geüploade documenten (Excel, PDF, Word, PowerPoint).

## Functies
- Bestandsupload (PDF, DOCX, PPTX, XLSX)
- Herkenning van relevante verzuim-termen
- Vergelijking met CBS-gegevens (SBI 6420 & 6622)
- Risicobepaling op basis van verzuimpercentages
- Aanbevelingen gebaseerd op risico

## Starten
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
