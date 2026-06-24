"""LangGraph workflow skeleton."""

from langgraph.graph import StateGraph, END

from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.writer import WriterAgent


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def __init__(self):
        self.supervisor = SupervisorAgent()
        self.researcher = ResearcherAgent()
        self.analyst = AnalystAgent()
        self.writer = WriterAgent()

    def build(self) -> object:
        graph = StateGraph(ResearchState)

        graph.add_node("supervisor", self.supervisor.run)
        graph.add_node("researcher", self.researcher.run)
        graph.add_node("analyst", self.analyst.run)
        graph.add_node("writer", self.writer.run)

        def route_decision(state: ResearchState) -> str:
            if not state.route_history:
                return END
            last_route = state.route_history[-1]
            if last_route == "done":
                return END
            return last_route

        graph.set_entry_point("supervisor")
        graph.add_conditional_edges("supervisor", route_decision)
        graph.add_edge("researcher", "supervisor")
        graph.add_edge("analyst", "supervisor")
        graph.add_edge("writer", "supervisor")

        return graph.compile()

    def run(self, state: ResearchState) -> ResearchState:
        app = self.build()
        # LangGraph invoke returns a dict if the schema is Pydantic
        final_state_dict = app.invoke(state)
        return ResearchState(**final_state_dict)
