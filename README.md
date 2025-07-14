# Verzuimanalyse API (v2)

Deze FastAPI-module ondersteunt:
- Upload van verzuimdocumenten
- Analyse met benchmark, risiconiveau en aanbevelingen
- PDF-rapportgeneratie uit markdown
- Batchverwerking van meerdere bestanden via `/batch_upload/`
- Verkorte tekstanalyse via `/analyse_text/`
- Grafiekoutput als PNG.

## Starten

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```