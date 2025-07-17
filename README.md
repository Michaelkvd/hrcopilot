# HR Copilot

Deze repository bevat een kleine FastAPI-applicatie die HR-processen ondersteunt. De focus ligt op twee modules:

1. **Verzuimanalyse** (`verzuimanalyse.py`)
   - Upload en analyseer verzuimdocumenten.
   - Batchverwerking van meerdere bestanden.
   - Genereer rapporten als PDF vanuit Markdown.
   - Maak een eenvoudige grafiek van het verzuim versus een benchmark.

2. **Juridische check** (`legalcheck.py`)
   - Controleer teksten of bestanden op juridische kernwoorden en begrippen.
   - Bepaal de complexiteit van een casus en geef advies, actieplan en vervolgvragen.
   - Ondersteunt ook Outlook `.msg` bestanden die automatisch naar tekst worden geconverteerd.
   - Geeft een overzicht van relevante bronnen uit bijvoorbeeld wetten.nl of rijksoverheid.nl.

De API definieert twee endpoints in `main.py`:

- `POST /upload/` – verzuimanalyse van een enkel bestand. Gebruik de query
  parameter `formaat=pdf` of `formaat=grafiek` om respectievelijk een PDF-rapport
  of PNG-grafiek te ontvangen.
- `POST /legalcheck/` – juridische analyse van tekst of (optioneel) een bestand.

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
