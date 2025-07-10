from fastapi import FastAPI
import logging
from verzuimanalyse import router as verzuimanalyse_router
from legalcheck import router as legalcheck_router
from hrdatacheck import router as hrdatacheck_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("🚀 HR Copilot API wordt gestart...")

app = FastAPI(title="HR Copilot API")

app.include_router(verzuimanalyse_router, prefix="/verzuimanalyse", tags=["Verzuimanalyse"])
app.include_router(legalcheck_router, prefix="/legalcheck", tags=["LegalCheck"])
app.include_router(hrdatacheck_router, prefix="/hrdatacheck", tags=["HRDataCheck"])