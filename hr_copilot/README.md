# HR Copilot (Debug)

Deze versie bevat logging om fouten bij deployment op Railway op te sporen.

## Deployment

```
uvicorn main:app --host=0.0.0.0 --port=8000
```

## Logging

- Railway → Logs → zie console-uitvoer tijdens opstart en bij elke route-aanroep