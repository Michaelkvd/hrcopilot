from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.data_helpers import analyse_hrdata

router = APIRouter()

class HRDataInput(BaseModel):
    huidige_data: dict
    vorige_data: dict

@router.post("/hrdatacheck")
def analyse_hr(input: HRDataInput):
    try:
        analyse = analyse_hrdata(input.huidige_data, input.vorige_data)
        return {"analyse": analyse}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))