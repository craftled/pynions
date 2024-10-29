from typing import Optional, Dict, Any
from ..core.base import BaseTool
from ..core.rate_limit import RateLimiter
import litellm


class AskLLM(BaseTool):
    """LLM integration tool"""

    def __init__(
        self, prompt_template: str, model: str = "gpt-4o-mini", rate_limit: float = 0.5
    ):
        self.prompt_template = prompt_template
        self.model = model
        self.rate_limiter = RateLimiter(calls_per_second=rate_limit)

    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run LLM inference"""
        await self.rate_limiter.acquire()

        try:
            prompt = self.prompt_template.format(**data)
            response = await litellm.acompletion(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )
            return {"llm_response": response.choices[0].message.content}
        except Exception as e:
            raise RuntimeError(f"LLM call failed: {str(e)}") from e
