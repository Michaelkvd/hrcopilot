from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.data_helpers import analyse_verzuimdata
from utils.prompt_templates import verzuimanalyse_prompt

router = APIRouter()

class VerzuimInput(BaseModel):
    data: dict
    branche: str

@router.post("/")
def analyse_verzuim(input: VerzuimInput):
    try:
        analyse_resultaat = analyse_verzuimdata(input.data)
        cbs_vergelijking = f"Wil je deze analyse vergelijken met CBS-data voor de branche '{input.branche}'?"
        wet_richtlijnen = "Let op de relevante wetgeving zoals WVP, Arbowet, Wet verbetering Poortwachter."
        return {
            "analyse": analyse_resultaat,
            "verzoek_cbs": cbs_vergelijking,
            "richtlijnen": wet_richtlijnen
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))