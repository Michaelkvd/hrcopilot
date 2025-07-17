# HR Copilot

Deze repository bevat een kleine FastAPI-applicatie die HR-processen ondersteunt. De focus ligt op verschillende modules:

1. **Verzuimcasuïstiek** (`Agents/Absenceagent/verzuim.py`)
   - Beantwoord vragen over dossiers en wetgeving rond verzuim.
   - Analyse van verzuimbestanden gebeurt via `Agents/Analysisagent/analysis.py`.
   - Genereer PDF-rapporten of een grafiek van het verzuim versus een benchmark.

2. **Juridische check** (`legalcheck.py`)
   - Controleer teksten of bestanden op juridische kernwoorden en begrippen.
   - Bepaal de complexiteit van een casus en geef advies, actieplan en vervolgvragen.
   - Ondersteunt ook Outlook `.msg` bestanden die automatisch naar tekst worden geconverteerd.
   - Geeft een overzicht van relevante bronnen uit bijvoorbeeld wetten.nl of rijksoverheid.nl.

De API definieert enkele endpoints in `main.py`:

- `POST /upload/` – analyse van verzuimdocumenten.
- `POST /batch_upload/` – verwerk meerdere documenten tegelijk.
- `POST /legalcheck/` – juridische analyse van tekst of (optioneel) een bestand.
- `POST /analyse/` – algemene bestandsanalyse.
- `POST /spp/` – analyse van SPP-data.

## Installatie en starten

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testen

Voer de unit tests uit met `pytest`:

```bash
pytest
```

## Privacyverklaring

In `privacyverklaring.txt` staat een korte toelichting op het tijdelijke gebruik van geuploade documenten. Er worden geen gegevens opgeslagen of gedeeld met derden.
