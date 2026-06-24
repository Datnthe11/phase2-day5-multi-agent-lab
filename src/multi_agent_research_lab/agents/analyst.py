"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        llm_client = LLMClient()
        
        sys_prompt = "You are an analyst. Extract key claims, compare viewpoints, and flag weak evidence from the following research notes."
        user_prompt = f"Query: {state.request.query}\nResearch Notes:\n{state.research_notes}"
        
        resp = llm_client.complete(sys_prompt, user_prompt)
        state.analysis_notes = resp.content
        state.agent_results.append(AgentResult(
            agent=self.name, 
            content=resp.content,
            metadata={"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}
        ))
        return state
