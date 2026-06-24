"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        llm_client = LLMClient()
        
        sys_prompt = f"You are an expert technical writer. Synthesize a clear response with citations for the audience: {state.request.audience}."
        user_prompt = f"Query: {state.request.query}\nResearch Notes:\n{state.research_notes}\nAnalysis Notes:\n{state.analysis_notes}"
        
        resp = llm_client.complete(sys_prompt, user_prompt)
        state.final_answer = resp.content
        state.agent_results.append(AgentResult(
            agent=self.name, 
            content=resp.content,
            metadata={"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}
        ))
        return state
