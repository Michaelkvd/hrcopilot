from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
from verzuimanalyse import analyse_verzuim, analyse_meerdere
from legalcheck import legalcheck

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyse_verzuim(file.filename, contents)
    return JSONResponse(content=result)


@app.post("/analyse_text/")
async def analyse_text(text: str = Form(...)):
    result = analyse_verzuim(input_text=text)
    return JSONResponse(content=result)


@app.post("/batch_upload/")
async def batch_upload(files: List[UploadFile] = File(...)):
    file_data = []
    for upload in files:
        contents = await upload.read()
        file_data.append((upload.filename, contents))
    result = analyse_meerdere(file_data)
    return JSONResponse(content=result)


@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(...)):
    result = legalcheck(file)
    return JSONResponse(content=result)
