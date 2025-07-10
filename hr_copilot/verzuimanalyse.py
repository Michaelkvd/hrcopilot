from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from utils.data_helpers import analyse_verzuimdata

logger = logging.getLogger(__name__)
router = APIRouter()

class VerzuimInput(BaseModel):
    data: dict
    branche: str

@router.post("")
def analyse_verzuim(input: VerzuimInput):
    logger.info("📊 Verzuimanalyse gestart")
    try:
        analyse_resultaat = analyse_verzuimdata(input.data)
        return {
            "analyse": analyse_resultaat,
            "verzoek_cbs": f"Wil je deze analyse vergelijken met CBS-data voor de branche '{input.branche}'?",
            "richtlijnen": "Let op de relevante wetgeving zoals WVP, Arbowet, Wet verbetering Poortwachter."
        }
    except Exception as e:
        logger.error(f"❌ Verzuimanalyse fout: {e}")
        raise HTTPException(status_code=500, detail=str(e))