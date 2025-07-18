class BaseAgent:
    """Simple base class for all agents."""

    def handle(self, *args, **kwargs):
        raise NotImplementedError


from fastapi import UploadFile
from typing import List, Optional, Tuple
from Agents.Analysisagent import analysis as analysis_mod
from Agents.Analysisagent.analysis import TRIGGERS as ANALYSIS_TRIGGERS, match_terms as analysis_match
from Agents.Legalagent.legalcheck import (
    legalcheck,
    TRIGGERS as LEGAL_TRIGGERS,
    match_terms as legal_match,
)
from Agents.CSagent.feedback import (
    store_feedback,
    TRIGGERS as FEEDBACK_TRIGGERS,
    match_terms as feedback_match,
)
from Agents.CSagent.user_logging import (
    registreer_gebruik,
    TRIGGERS as LOG_TRIGGERS,
    match_terms as log_match,
)
from Agents.Absenceagent.verzuim import (
    beantwoord_vraag,
    TRIGGERS as ABSENCE_TRIGGERS,
    match_terms as absence_match,
)


class AbsenceAgent(BaseAgent):
    TRIGGERS = ABSENCE_TRIGGERS

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return absence_match(text)

    def analyse(
        self,
        file: Optional[UploadFile] = None,
        text: Optional[str] = None,
        periode: Optional[str] = None,
    ) -> dict:
        """Analyseer een verzuimdocument of tekst."""

        if file is None and text is None:
            return {
                "status": "geen input",
                "advies": "Geen gegevens ontvangen voor analyse.",
            }

            raise ValueError("file of text verplicht")

        if file is not None:
            contents = file.file.read()
            file.file.seek(0)
            filename = file.filename
        else:
            contents = text.encode()
            filename = "tekst-input"
        return analysis_mod.analyse_verzuim(filename, contents, periode=periode)

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
    TRIGGERS = LEGAL_TRIGGERS

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return legal_match(text)

    def analyse(self, file: Optional[UploadFile] = None, text: Optional[str] = None, intern_beleid: Optional[str] = None) -> dict:
        return legalcheck(file=file, input_text=text, intern_beleid=intern_beleid)


class AnalysisAgent(BaseAgent):
    TRIGGERS = ANALYSIS_TRIGGERS

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return analysis_match(text)

    def analyse(self, file: UploadFile, vraag: str, formaat: str) -> Tuple[str, bytes, dict]:
        result = analysis_mod.analyse_bestand(file, vraag)
        analysis_mod.log_gebruik("user", "analyse")
        mime, data = analysis_mod.genereer_rapport(result, formaat)
        return mime, data, result

    def analyse_spp(self, file: Optional[UploadFile], text: Optional[str], formaat: str) -> Tuple[str, bytes | dict, str]:
        result = analysis_mod.analyse_spp(file=file, text=text)
        analysis_mod.log_spp("user", "spp")
        if result.get("status") == "geen input" or formaat == "json":
            return "application/json", result, "json"
        buf = analysis_mod.genereer_spp_rapport(result, formaat)
        media = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            if formaat == "excel" else "text/csv"
        )
        return media, buf.getvalue(), "bytes"




class FeedbackAgent(BaseAgent):
    TRIGGERS = FEEDBACK_TRIGGERS | LOG_TRIGGERS

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return feedback_match(text) or log_match(text)

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

    def detect_agent(self, text: str) -> Optional[BaseAgent]:
        """Kies een agent op basis van semantische triggers."""
        if self.legal.match_terms(text):
            return self.legal
        if self.absence.match_terms(text):
            return self.absence
        if self.analysis.match_terms(text):
            return self.analysis
        if self.feedback.match_terms(text):
            return self.feedback
        return None

