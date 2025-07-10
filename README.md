# HR Copilot

Een slimme, strategische HR-assistent voor HR Business Partners in de financiële sector.

## Acties
- `/verzuimanalyse`: analyseert verzuimdata
- `/legalcheck`: toetst documenten aan wet- en regelgeving
- `/hrdatacheck`: analyseert maandelijkse HR-data

## Deployment

```
uvicorn main:app --host=0.0.0.0 --port=8000
```