class BaseAgent:
    """Simple base class for all agents."""

    name: str = "base"

    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    def handle(self, *args, **kwargs):
        """Handle a generic request and return a result."""
        raise NotImplementedError


from fastapi import UploadFile
from typing import List, Optional, Tuple
from pathlib import Path
from utils import Memory
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
from Agents.Complianceagent.compliance import (
    compliance_check,
    TRIGGERS as COMPLIANCE_TRIGGERS,
    match_terms as compliance_match,
)


class AbsenceAgent(BaseAgent):
    """Agent voor verzuimgerelateerde acties."""

    name = "absence"
    TRIGGERS = ABSENCE_TRIGGERS

    def __init__(self, orchestrator=None):
        super().__init__(orchestrator)

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

    def handle(self, *, file=None, text=None, periode=None, context=None, **kw):
        if file is None and not text:
            return {"status": "geen input"}
        result = self.analyse(file=file, text=text, periode=periode)
        if context is not None:
            context["absence"] = result
        if self.orchestrator:
            self.orchestrator.memory.add(
                kw.get("user", "anon"), {"absence_result": result}
            )
        return result


class LegalAgent(BaseAgent):
    """Agent voor juridische controles."""

    name = "legal"
    TRIGGERS = LEGAL_TRIGGERS

    def __init__(self, orchestrator=None):
        super().__init__(orchestrator)

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return legal_match(text)

    def analyse(self, file: Optional[UploadFile] = None, text: Optional[str] = None, intern_beleid: Optional[str] = None) -> dict:
        return legalcheck(file=file, input_text=text, intern_beleid=intern_beleid)

    def handle(self, *, file=None, text=None, intern_beleid=None, context=None, **kw):
        result = self.analyse(file=file, text=text, intern_beleid=intern_beleid)
        if context and "absence" in context:
            result["verzuim"] = context["absence"]
        if self.orchestrator:
            self.orchestrator.memory.add(
                kw.get("user", "anon"), {"legal_result": result}
            )
        return result


class AnalysisAgent(BaseAgent):
    """Agent voor algemene data-analyse."""

    name = "analysis"
    TRIGGERS = ANALYSIS_TRIGGERS

    def __init__(self, orchestrator=None):
        super().__init__(orchestrator)

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

    def handle(self, *, file=None, text=None, vraag="", formaat="json", context=None, **kw):
        if file is None:
            return {"status": "geen bestand"}
        mime, data, result = self.analyse(file, vraag, formaat)
        if self.orchestrator:
            self.orchestrator.memory.add(
                kw.get("user", "anon"), {"analysis_result": result}
            )
        return {"mime": mime, "result": result}


class ComplianceAgent(BaseAgent):
    """Agent voor compliancecontroles."""

    name = "compliance"
    TRIGGERS = COMPLIANCE_TRIGGERS

    def __init__(self, orchestrator=None):
        super().__init__(orchestrator)

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return compliance_match(text)

    def analyse(self, file: Optional[UploadFile] = None, text: Optional[str] = None) -> dict:
        return compliance_check(file=file, text=text)

    def handle(self, *, file=None, text=None, context=None, **kw):
        result = self.analyse(file=file, text=text)
        if self.orchestrator:
            self.orchestrator.memory.add(
                kw.get("user", "anon"), {"compliance_result": result}
            )
        return result




class FeedbackAgent(BaseAgent):
    """Agent voor feedback en logging."""

    name = "feedback"
    TRIGGERS = FEEDBACK_TRIGGERS | LOG_TRIGGERS

    def __init__(self, orchestrator=None):
        super().__init__(orchestrator)

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return feedback_match(text) or log_match(text)

    def store(self, gebruiker: str, bericht: str) -> dict:
        return store_feedback(gebruiker, bericht)

    def log(self, gebruiker: str, actie: str) -> dict:
        return registreer_gebruik(gebruiker, actie)

    def handle(self, *, gebruiker=None, bericht=None, actie=None, context=None, **kw):
        if bericht is not None:
            result = self.store(gebruiker or "anon", bericht)
            if self.orchestrator:
                self.orchestrator.memory.add(gebruiker or "anon", {"feedback": bericht})
            return result
        if actie is not None:
            result = self.log(gebruiker or "anon", actie)
            if self.orchestrator:
                self.orchestrator.memory.add(gebruiker or "anon", {"log": actie})
            return result
        return {"status": "geen feedback"}


class MainAgent:
    """Orchestrator die automatisch de juiste agent(en) aanroept."""

    def __init__(self, memory_path: Optional[Path] = None):
        self.memory = Memory(memory_path)
        self.absence = AbsenceAgent(self)
        self.legal = LegalAgent(self)
        self.analysis = AnalysisAgent(self)
        self.compliance = ComplianceAgent(self)
        self.feedback = FeedbackAgent(self)
        self.agents = [
            self.legal,
            self.absence,
            self.analysis,
            self.compliance,
            self.feedback,
        ]

    def detect_agent(self, text: str) -> Optional[BaseAgent]:
        """Kies een agent op basis van semantische triggers."""
        for agent in self.agents:
            if agent.match_terms(text):
                return agent
        return None

    def auto_route(self, text: str, user: str | None = None, **kwargs) -> dict:
        """Voer automatisch alle passende agents uit op basis van ``text``."""
        context = {}
        for agent in self.agents:
            if agent.match_terms(text):
                context[agent.name] = agent.handle(
                    text=text, **kwargs, context=context, user=user
                )
        if not context:
            context["status"] = "geen match"
        if user:
            self.memory.add(user, {"input": text, "output": context})
        return context

