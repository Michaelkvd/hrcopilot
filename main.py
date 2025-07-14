from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from verzuimanalyse import analyse_verzuim
import uvicorn

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                  "application/pdf",
                                  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                  "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
        raise HTTPException(status_code=400, detail="Bestandstype niet ondersteund.")

    contents = await file.read()
    result = analyse_verzuim(file.filename, contents)
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
