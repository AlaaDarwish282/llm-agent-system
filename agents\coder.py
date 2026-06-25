from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools.code_executor import execute_python
from config.settings import settings


class CoderAgent:
    """
    Agent that writes, debugs, and executes Python code
    to solve analytical or computational tasks.
    """

    SYSTEM_PROMPT = """You are a senior software engineer specializing in Python and data science.
Your responsibilities:
1. Write clean, well-commented, production-quality code
2. Debug errors iteratively
3. Explain your code clearly
4. Prefer standard libraries; use external libs only when necessary
5. Always handle edge cases and exceptions

Output code inside triple backticks with the python language tag."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0.0,
            api_key=settings.OPENAI_API_KEY,
        )
        self.max_retries = 3

    def _extract_code(self, text: str) -> str:
        """Extract Python code from LLM response."""
        import re
        pattern = r"```python\s*(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[0].strip() if matches else ""

    def generate_and_run(self, task: str) -> dict:
        """Generate code for a task, run it, and return results."""
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"Write Python code to accomplish this task:\n\n{task}"),
        ]

        for attempt in range(self.max_retries):
            response = self.llm.invoke(messages)
            code = self._extract_code(response.content)

            if not code:
                return {"success": False, "error": "No code generated", "code": "", "output": ""}

            result = execute_python(code)

            if result["success"]:
                return {
                    "success": True,
                    "code": code,
                    "output": result["stdout"],
                    "attempts": attempt + 1,
                }
            else:
                # Feed error back for self-correction
                messages.append(HumanMessage(content=response.content))
                messages.append(
                    HumanMessage(
                        content=f"The code produced an error:\n{result['stderr']}\n\nFix it and try again."
                    )
                )

        return {"success": False, "error": "Max retries exceeded", "code": code, "output": ""}
