from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, StreamingResponse
from verzuimanalyse import analyse_verzuim, analyse_meerdere, genereer_pdf, genereer_grafiek
import io

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyse_verzuim(file.filename, contents)
    return JSONResponse(content=result)

@app.post("/batch-upload/")
async def batch_upload(files: list[UploadFile] = File(...)):
    resultaten = []
    for file in files:
        contents = await file.read()
        analyse = analyse_verzuim(file.filename, contents)
        resultaten.append(analyse)
    return resultaten

@app.post("/rapport-pdf/")
async def rapport_pdf(request: Request):
    data = await request.json()
    markdown = data.get("interpretatie_markdown", "")
    pdf_bytes = genereer_pdf(markdown)
    return StreamingResponse(io.BytesIO(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=rapport.pdf"})

@app.post("/grafiek/")
async def grafiek_endpoint(request: Request):
    data = await request.json()
    fig = genereer_grafiek(data)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")