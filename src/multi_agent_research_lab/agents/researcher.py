"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.services.search_client import SearchClient
from multi_agent_research_lab.services.llm_client import LLMClient

class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        search_client = SearchClient()
        llm_client = LLMClient()

        # Optimize the search query using LLM instead of passing the full natural language prompt
        query_prompt = f"Extract 3-5 essential keywords from this request to use in a search engine. Return ONLY the keywords separated by spaces, nothing else.\nRequest: {state.request.query}"
        search_query = llm_client.complete("You are an expert search query generator.", query_prompt).content.strip().strip('"')

        sources = search_client.search(search_query, max_results=state.request.max_sources)
        state.sources.extend(sources)

        source_texts = "\n".join([f"[{i+1}] {s.title}\n{s.snippet}" for i, s in enumerate(sources)])
        
        sys_prompt = "You are a researcher. Extract and summarize the key facts from the provided sources that are relevant to the query."
        user_prompt = f"Query: {state.request.query}\nSources:\n{source_texts}"
        
        resp = llm_client.complete(sys_prompt, user_prompt)
        state.research_notes = resp.content
        state.agent_results.append(AgentResult(
            agent=self.name, 
            content=resp.content, 
            metadata={"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}
        ))
        return state
