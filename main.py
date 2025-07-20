from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional
from io import BytesIO

from agents import MainAgent

ADMIN_USER = "admin"
app = FastAPI()
main_agent = MainAgent()


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(None),
    text: Optional[str] = Form(None),
    periode: Optional[str] = None,
    formaat: Optional[str] = "json",
):
    if file is None and text is None:
        return JSONResponse(content={"status": "geen input"})

    result = main_agent.absence.analyse(file=file, text=text, periode=periode)
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
        pdf_data = main_agent.absence.pdf(markdown)
        return StreamingResponse(BytesIO(pdf_data), media_type="application/pdf")
    if formaat == "grafiek":
        fig = main_agent.absence.chart(result)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    return JSONResponse(content=result)


@app.post("/batch_upload/")
async def batch_upload(files: List[UploadFile] = File(...), periode: Optional[str] = None):
    result = main_agent.absence.analyse_batch(files, periode)
    return JSONResponse(content=result)


@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(None), text: Optional[str] = Form(None)):
    result = main_agent.legal.analyse(file=file, text=text)
    return JSONResponse(content=result)


@app.post("/compliance/")
async def compliance(file: UploadFile = File(None), text: Optional[str] = Form(None)):
    result = main_agent.compliance.analyse(file=file, text=text)
    return JSONResponse(content=result)


@app.post("/analyse/")
async def analyse(file: UploadFile = File(...), vraag: str = "", formaat: str = "json"):
    mime, data, result = main_agent.analysis.analyse(file, vraag, formaat)
    if mime != "application/json":
        return StreamingResponse(BytesIO(data), media_type=mime)
    return JSONResponse(content=result)


@app.post("/spp/")
async def spp(file: UploadFile = File(None), text: Optional[str] = Form(None), formaat: str = "excel"):
    media, data, data_type = main_agent.analysis.analyse_spp(file, text, formaat)
    if media == "application/json":
        return JSONResponse(content=data)
    return StreamingResponse(BytesIO(data), media_type=media)


@app.post("/feedback/")
async def feedback(gebruiker: str = Form(...), bericht: str = Form(...)):
    if gebruiker != ADMIN_USER:
        return JSONResponse(status_code=403, content={"error": "alleen beheerder"})
    result = main_agent.feedback.store(gebruiker, bericht)
    return JSONResponse(content=result)


@app.post("/log/")
async def log(gebruiker: str = Form(...), actie: str = Form(...)):
    if gebruiker != ADMIN_USER:
        return JSONResponse(status_code=403, content={"error": "alleen beheerder"})
    result = main_agent.feedback.log(gebruiker, actie)
    return JSONResponse(content=result)


@app.post("/auto/")
async def auto_route(
    text: str = Form(""),
    file: UploadFile | None = File(None),
    vraag: str = Form(""),
    intern_beleid: str | None = Form(None),
    gebruiker: str | None = Form(None),
    bericht: str | None = Form(None),
    actie: str | None = Form(None),
    periode: str | None = Form(None),
    formaat: str = "json",
):
    result = main_agent.auto_route(
        text,
        file=file,
        vraag=vraag,
        intern_beleid=intern_beleid,
        gebruiker=gebruiker,
        bericht=bericht,
        actie=actie,
        periode=periode,
        formaat=formaat,
        user=gebruiker,
    )
    return JSONResponse(content=result)
