from ..core.base import BaseTool
from ..rate_limit import RateLimit
import litellm


class AskLLM(BaseTool):
    def __init__(self, prompt_template: str, model: str = "gpt-4o-mini"):
        self.prompt_template = prompt_template
        self.model = model

    @RateLimit(calls_per_second=0.5)  # Limit to 1 call per 2 seconds
    async def run(self, data: dict) -> dict:
        prompt = self.prompt_template.format(**data)
        response = await litellm.acompletion(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return {"llm_response": response.choices[0].message.content}
