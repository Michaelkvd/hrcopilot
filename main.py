from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List, Optional

from verzuimanalyse import analyse_verzuim, analyse_meerdere
from legalcheck import legalcheck

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), periode: Optional[str] = None
):
    contents = await file.read()
    file.file.seek(0)
    result = analyse_verzuim(file.filename, contents, periode=periode)
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
