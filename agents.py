class BaseAgent:
    """Simple base class for all agents."""

    def handle(self, *args, **kwargs):
        raise NotImplementedError


from fastapi import UploadFile
from typing import List, Optional, Tuple
from Agents.Analysisagent import analysis as analysis_mod
from Agents.Legalagent.legalcheck import legalcheck
from Agents.CSagent.feedback import store_feedback
from Agents.CSagent.user_logging import registreer_gebruik
from Agents.Absenceagent.verzuim import beantwoord_vraag


class AbsenceAgent(BaseAgent):
    def analyse(self, file: UploadFile, periode: Optional[str] = None) -> dict:
        contents = file.file.read()
        file.file.seek(0)
        return analysis_mod.analyse_verzuim(file.filename, contents, periode=periode)

    def analyse_batch(self, files: List[UploadFile], periode: Optional[str] = None) -> List[dict]:
        items: List[Tuple[str, bytes]] = []
        for f in files:
            data = f.file.read()
            f.file.seek(0)
            items.append((f.filename, data))
        if periode is None:
            return analysis_mod.analyse_meerdere(items)
        return [analysis_mod.analyse_verzuim(n, c, periode=periode) for n, c in items]

    def pdf(self, markdown: str) -> bytes:
        return analysis_mod.genereer_pdf(markdown)

    def chart(self, data: dict):
        return analysis_mod.genereer_grafiek(data)


class LegalAgent(BaseAgent):
    def analyse(self, file: Optional[UploadFile] = None, text: Optional[str] = None, intern_beleid: Optional[str] = None) -> dict:
        return legalcheck(file=file, input_text=text, intern_beleid=intern_beleid)


class AnalysisAgent(BaseAgent):
    def analyse(self, file: UploadFile, vraag: str, formaat: str) -> Tuple[str, bytes, dict]:
        result = analysis_mod.analyse_bestand(file, vraag)
        analysis_mod.log_gebruik("user", "analyse")
        mime, data = analysis_mod.genereer_rapport(result, formaat)
        return mime, data, result

    def analyse_spp(self, file: UploadFile, formaat: str) -> Tuple[str, bytes | dict, str]:
        result = analysis_mod.analyse_spp(file)
        analysis_mod.log_spp("user", "spp")
        if formaat == "json":
            return "application/json", result, "json"
        buf = analysis_mod.genereer_spp_rapport(result, formaat)
        media = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            if formaat == "excel" else "text/csv"
        )
        return media, buf.getvalue(), "bytes"




class FeedbackAgent(BaseAgent):
    def store(self, gebruiker: str, bericht: str) -> dict:
        return store_feedback(gebruiker, bericht)

    def log(self, gebruiker: str, actie: str) -> dict:
        return registreer_gebruik(gebruiker, actie)


class MainAgent:
    def __init__(self):
        self.absence = AbsenceAgent()
        self.legal = LegalAgent()
        self.analysis = AnalysisAgent()
        self.feedback = FeedbackAgent()

