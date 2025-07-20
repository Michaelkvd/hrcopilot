from typing import List, Optional
from utils import text_matches
from agents import BaseAgent

TRIGGERS = {"workflow", "plan", "stap", "procedure"}

class WorkflowAgent(BaseAgent):
    """Agent die stapsgewijs andere agents kan aanroepen."""

    name = "workflow"
    TRIGGERS = TRIGGERS

    @classmethod
    def match_terms(cls, text: str) -> bool:
        return text_matches(text, cls.TRIGGERS)

    def handle(self, *, text: str | None = None, user: str | None = None, context: Optional[dict] = None, **kw) -> dict:
        if not text:
            return {"status": "geen input"}

        steps = [s.strip() for s in text.splitlines() if s.strip()]
        ctx = context or {}
        results: List[dict] = []
        for step in steps:
            agent = self.orchestrator.detect_agent(step)
            if agent:
                res = agent.handle(text=step, context=ctx, user=user, **kw)
                ctx[agent.name] = res
                results.append({"stap": step, "agent": agent.name, "resultaat": res})
            else:
                results.append({"stap": step, "agent": None, "resultaat": {"status": "geen match"}})
        if user and self.orchestrator:
            self.orchestrator.memory.add(user, {"workflow": results})
        return {"stappen": results}
