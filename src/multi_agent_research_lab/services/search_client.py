"""Search client abstraction for ResearcherAgent."""

import requests

from multi_agent_research_lab.core.schemas import SourceDocument

class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query using Wikipedia API."""
        documents = []
        try:
            url = "https://en.wikipedia.org/w/api.php"
            headers = {"User-Agent": "MultiAgentResearchLab/1.0 (test@example.com)"}
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "utf8": 1,
            }
            resp = requests.get(url, params=params, headers=headers)
            resp.raise_for_status()
            results = resp.json().get("query", {}).get("search", [])
            
            for r in results[:max_results]:
                # For each search result, fetch the extract (summary)
                page_title = r.get("title", "")
                page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
                
                # Fetch snippet
                ex_params = {
                    "action": "query",
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "titles": page_title,
                    "format": "json"
                }
                ex_resp = requests.get(url, params=ex_params, headers=headers)
                ex_data = ex_resp.json().get("query", {}).get("pages", {})
                snippet = ""
                if ex_data:
                    page_id = list(ex_data.keys())[0]
                    snippet = ex_data[page_id].get("extract", r.get("snippet", ""))

                documents.append(SourceDocument(
                    title=page_title,
                    url=page_url,
                    snippet=snippet[:1000] # Limit length
                ))
        except Exception as e:
            print(f"Wikipedia search failed: {e}")
        return documents
