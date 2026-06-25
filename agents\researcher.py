from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools.web_search import search_web
from config.settings import settings


class ResearcherAgent:
    """
    Agent responsible for gathering information from the web
    and synthesizing research reports on a given topic.
    """

    SYSTEM_PROMPT = """You are an expert research analyst. Your job is to:
1. Search the web for relevant, up-to-date information
2. Critically evaluate sources and filter out noise
3. Synthesize findings into clear, structured reports
4. Cite sources and highlight confidence levels

Always think step-by-step and be thorough yet concise."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY,
        )

    def research(self, topic: str, depth: str = "standard") -> dict:
        """
        Research a topic and return a structured report.
        depth: 'quick' | 'standard' | 'deep'
        """
        max_results = {"quick": 3, "standard": 5, "deep": 10}.get(depth, 5)

        # Gather raw search results
        search_results = search_web(topic, max_results=max_results)
        context = "\n\n".join(
            [f"Source: {r.get('url', 'N/A')}\n{r.get('content', '')}" for r in search_results]
        )

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(
                content=f"""Research the following topic and produce a structured report:

TOPIC: {topic}

RAW SEARCH DATA:
{context}

Produce a report with:
- Executive Summary
- Key Findings (3-5 bullet points)
- Detailed Analysis
- Sources & References
- Confidence Level (High/Medium/Low)"""
            ),
        ]

        response = self.llm.invoke(messages)
        return {
            "topic": topic,
            "report": response.content,
            "sources": [r.get("url") for r in search_results],
            "depth": depth,
        }
