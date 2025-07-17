from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
from io import BytesIO

from verzuimanalyse import (
    analyse_verzuim,
    analyse_meerdere,
    bepaal_risico,
    genereer_aanbevelingen,
    genereer_pdf,
    genereer_grafiek,
)
from legalcheck import legalcheck
from analysis import analyse_bestand, genereer_rapport, log_gebruik
from SPP import analyse_spp, genereer_spp_rapport, log_spp
from feedback import store_feedback
from user_logging import registreer_gebruik

ADMIN_USER = "admin"

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    periode: Optional[str] = None,
    formaat: Optional[str] = "json",
):
    contents = await file.read()
    file.file.seek(0)
    result = analyse_verzuim(file.filename, contents, periode=periode)
    if formaat == "pdf":
        markdown = (
            f"# Verzuimrapport\n"
            f"**Bestand:** {result['filename']}\n"
            f"**Periode:** {result['periode']}\n"
            f"**Verzuimpercentage:** {result['verzuimpercentage']}\n"
            f"**Benchmark:** {result['branche_benchmark']['waarde']}\n"
            f"**Risico:** {result['risico']}\n"
            f"**Advies:** {result['advies']}\n"
        )
        pdf_data = genereer_pdf(markdown)
        return StreamingResponse(BytesIO(pdf_data), media_type="application/pdf")
    if formaat == "grafiek":
        fig = genereer_grafiek(result)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    return JSONResponse(content=result)


@app.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...), periode: Optional[str] = None
):
    contents = []
    for f in files:
        data = await f.read()
        contents.append((f.filename, data))
    if periode is None:
        result = analyse_meerdere(contents)
    else:
        result = [
            analyse_verzuim(name, data, periode=periode)
            for name, data in contents
        ]
    return JSONResponse(content=result)

@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(...)):
    result = legalcheck(file)
    return JSONResponse(content=result)


@app.post("/analyse/")
async def analyse(file: UploadFile = File(...), vraag: str = "", formaat: str = "json"):
    result = analyse_bestand(file, vraag)
    log_gebruik("user", "analyse")
    mime, data = genereer_rapport(result, formaat)
    if mime != "application/json":
        return StreamingResponse(BytesIO(data), media_type=mime)
    return JSONResponse(content=result)


@app.post("/spp/")
async def spp(file: UploadFile = File(...), formaat: str = "excel"):
    result = analyse_spp(file)
    log_spp("user", "spp")
    if formaat == "json":
        return JSONResponse(content=result)
    if formaat == "json":
        return JSONResponse(content=result)
    buf = genereer_spp_rapport(result, formaat)
    media = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if formaat == "excel"
        else "text/csv"
    )
    return StreamingResponse(buf, media_type=media)


@app.post("/feedback/")
async def feedback(gebruiker: str = Form(...), bericht: str = Form(...)):
    if gebruiker != ADMIN_USER:
        return JSONResponse(status_code=403, content={"error": "alleen beheerder"})
    if gebruiker != ADMIN_USER:
        return JSONResponse(status_code=403, content={"error": "alleen beheerder"})
    result = store_feedback(gebruiker, bericht)
    return JSONResponse(content=result)


@app.post("/log/")
async def log(gebruiker: str = Form(...), actie: str = Form(...)):
    if gebruiker != ADMIN_USER:
        return JSONResponse(status_code=403, content={"error": "alleen beheerder"})
    result = registreer_gebruik(gebruiker, actie)
    return JSONResponse(content=result)
