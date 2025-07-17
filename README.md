# HR Copilot

HR Copilot is een compacte FastAPI-applicatie ter ondersteuning van uiteenlopende HR-vraagstukken. De applicatie bestaat uit meerdere **agents** die elk een specifiek domein behandelen.

## Architectuur

```
Agents/
  Absenceagent/     - analyse van verzuimvragen en dossiers
  Analysisagent/    - generieke bestand‑ en SPP‑analyses
  CSagent/          - feedback en gebruiksregistratie
  Legalagent/       - juridische controles
utils/              - hulpfuncties voor opslag van feedback en logs
main.py             - definieert alle API‑routes
agents.py           - installeert de bovengenoemde agents
```

De `MainAgent` in `agents.py` bundelt de afzonderlijke agents en wordt gebruikt door de endpoints in `main.py`. Daarnaast kan de `MainAgent` op basis van **semantische triggers** een passende agent selecteren. Woorden als "ontslag", "spp" of "feedback" worden automatisch gekoppeld aan de betreffende module.

### Belangrijkste agents

1. **AbsenceAgent** (`Agents/Absenceagent/`)
   - Beantwoordt verzuimgerelateerde vragen.
   - Voert analyses uit op documenten en kan een PDF‑rapport of grafiek genereren.
2. **LegalAgent** (`Agents/Legalagent/`)
   - Herkent juridische kernwoorden en begrippen in teksten of bestanden (waaronder `.msg`, Office‑ en PDF‑bestanden).
   - Bepaalt de complexiteit van een casus en geeft advies, actieplan en vervolgvragen.
3. **AnalysisAgent** (`Agents/Analysisagent/`)
   - Voert algemene analyses uit op bestanden en ondersteunt een SPP‑analyse (9‑box grid).
   - Resultaten kunnen als JSON, Excel of CSV worden teruggegeven.
4. **FeedbackAgent** (`Agents/CSagent/`)
   - Slaat feedback op en registreert gebruiksacties. Alleen de beheerder mag deze routes aanroepen.

## API‑endpoints

De volgende routes zijn beschikbaar:

- `POST /upload/` – analyseer één verzuimdocument en kies optioneel voor een PDF of grafiek als resultaat.
- `POST /batch_upload/` – verwerk meerdere documenten in één keer.
- `POST /legalcheck/` – voer een juridische check uit op tekst of een geüpload bestand.
- `POST /analyse/` – algemene bestandsanalyse met risicobepaling.
- `POST /spp/` – analyse van SPP‑data (9‑box grid) uit een bestand of tekst in JSON, Excel of CSV. Kolomnamen mogen spaties bevatten en `normaal` wordt gezien als synoniem voor `midden`.
- `POST /spp/` – analyse van SPP‑data (9‑box grid) uit een bestand of tekst in JSON, Excel of CSV.
- `POST /feedback/` – sla feedback op (alleen beheerdersaccount).
- `POST /log/` – registreer een gebruikersactie (alleen beheerdersaccount).

## Installatie en starten

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Python 3.10 wordt gebruikt (zie `runtime.txt`).

## Testen

De unit tests draaien met `pytest`:

```bash
pytest
```

## Privacyverklaring

Zie `privacyverklaring.txt` voor een toelichting op het tijdelijke gebruik van geüploade documenten. Er worden geen gegevens opgeslagen of gedeeld met derden.
