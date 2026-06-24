"""Search client abstraction for ResearcherAgent."""

from duckduckgo_search import DDGS

from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query."""
        documents = []
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if results:
                for r in results:
                    documents.append(SourceDocument(
                        title=r.get("title", ""),
                        url=r.get("href", ""),
                        snippet=r.get("body", "")
                    ))
        return documents
