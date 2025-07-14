from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from verzuimanalyse import analyse_verzuim, analyse_meerdere
from legalcheck import legalcheck

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyse_verzuim(file.filename, contents)
    return JSONResponse(content=result)

@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(...)):
    result = legalcheck(file)
    return JSONResponse(content=result)


@app.post("/batch_upload/")
async def batch_upload(files: list[UploadFile] = File(...)):
    results = await analyse_meerdere(files)
    return JSONResponse(content=results)
