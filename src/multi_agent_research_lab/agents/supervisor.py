"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        if state.iteration >= 5:
            state.record_route("done")
            return state

        if not state.research_notes:
            route = "researcher"
        elif not state.analysis_notes:
            route = "analyst"
        elif not state.final_answer:
            route = "writer"
        else:
            route = "done"

        state.record_route(route)
        return state
