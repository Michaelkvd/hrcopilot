from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from utils.data_helpers import analyse_hrdata

logger = logging.getLogger(__name__)
router = APIRouter()

class HRDataInput(BaseModel):
    huidige_data: dict
    vorige_data: dict

@router.post("")
def analyse_hr(input: HRDataInput):
    logger.info("📈 HRDataCheck gestart")
    try:
        analyse = analyse_hrdata(input.huidige_data, input.vorige_data)
        return {"analyse": analyse}
    except Exception as e:
        logger.error(f"❌ HRDataCheck fout: {e}")
        raise HTTPException(status_code=500, detail=str(e))