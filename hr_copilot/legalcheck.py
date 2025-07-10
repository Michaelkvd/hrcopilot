from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.legal_sources import check_legality

router = APIRouter()

class LegalInput(BaseModel):
    document: str

@router.post("/")
def legal_check(input: LegalInput):
    try:
        resultaat = check_legality(input.document)
        bronnen = [
            "https://wetten.overheid.nl",
            "https://www.rijksoverheid.nl",
            "https://www.uwv.nl"
        ]
        return {
            "advies": resultaat,
            "bronnen": bronnen
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))