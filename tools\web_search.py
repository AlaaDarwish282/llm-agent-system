from typing import Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from config.settings import settings
import os

os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY


def get_web_search_tool(max_results: int = 5) -> TavilySearchResults:
    """Return a Tavily web search tool."""
    return TavilySearchResults(max_results=max_results)


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Perform a web search and return structured results."""
    tool = get_web_search_tool(max_results)
    results = tool.invoke(query)
    return results
