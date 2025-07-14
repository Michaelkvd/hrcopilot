from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from verzuimanalyse import analyse_verzuim
from legalcheck import legalcheck

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    result = analyse_verzuim(file)
    return JSONResponse(content=result)

@app.post("/legalcheck/")
async def upload_legal(file: UploadFile = File(...)):
    result = legalcheck(file)
    return JSONResponse(content=result)