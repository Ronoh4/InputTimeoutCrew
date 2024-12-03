from crewai_tools import BaseTool
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")

class OrganicSearchTool(BaseTool):
    name: str = "General Google Search"
    description: str = (
        "Performs a general organic Google search and retrieves organic results. "
        "Use this tool to extract the most relevant web results for a given query."
    )

    def _run(self, query: str) -> dict:
        params = {
            "engine": "google",
            "q": query,
            "api_key": serper_api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", None)

        if organic_results:
            # Return top 6 results
            top_results = organic_results[:6]
            return {"results": top_results}
        else:
            return {"error": "No general search results found."}
