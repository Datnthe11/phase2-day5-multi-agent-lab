import os
from dataclasses import dataclass

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from multi_agent_research_lab.core.errors import StudentTodoError


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.0):
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Extract token usage if available
        input_tokens = None
        output_tokens = None
        if hasattr(response, "response_metadata") and "token_usage" in response.response_metadata:
            usage = response.response_metadata["token_usage"]
            input_tokens = usage.get("prompt_tokens")
            output_tokens = usage.get("completion_tokens")

        return LLMResponse(
            content=str(response.content),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
