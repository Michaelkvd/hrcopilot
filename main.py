from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

from verzuimanalyse import analyse_verzuim, analyse_meerdere
from legalcheck import legalcheck

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file.file.seek(0)
    result = analyse_verzuim(file.filename, contents)
    return JSONResponse(content=result)


@app.post("/batch_upload/")
async def batch_upload(files: List[UploadFile] = File(...)):
    contents = []
    for f in files:
        data = await f.read()
        contents.append((f.filename, data))
    result = analyse_meerdere(contents)
    return JSONResponse(content=result)

@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(...)):
    result = legalcheck(file)
    return JSONResponse(content=result)
