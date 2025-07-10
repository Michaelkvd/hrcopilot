from fastapi import FastAPI
from verzuimanalyse import router as verzuimanalyse_router
from legalcheck import router as legalcheck_router
from hrdatacheck import router as hrdatacheck_router

app = FastAPI(title="HR Copilot API")

app.include_router(verzuimanalyse_router, tags=["Verzuimanalyse"])
app.include_router(legalcheck_router, tags=["LegalCheck"])
app.include_router(hrdatacheck_router, tags=["HRDataCheck"])