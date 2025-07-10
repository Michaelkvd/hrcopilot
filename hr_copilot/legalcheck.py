from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from utils.legal_sources import check_legality

logger = logging.getLogger(__name__)
router = APIRouter()

class LegalInput(BaseModel):
    document: str

@router.post("")
def legal_check(input: LegalInput):
    logger.info("📄 LegalCheck gestart")
    try:
        resultaat = check_legality(input.document)
        return {
            "advies": resultaat,
            "bronnen": [
                "https://wetten.overheid.nl",
                "https://www.rijksoverheid.nl",
                "https://www.uwv.nl"
            ]
        }
    except Exception as e:
        logger.error(f"❌ LegalCheck fout: {e}")
        raise HTTPException(status_code=500, detail=str(e))