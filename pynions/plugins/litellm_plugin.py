import os
from typing import Dict, Any, Optional
import logging
from litellm import completion
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LiteLLM:
    """Plugin for interacting with LLMs using LiteLLM"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the LiteLLM plugin with configuration"""
        self.config = config or {}
        self.logger = logging.getLogger("pynions.plugins.litellm")

        # Set default model to gpt-4o
        self.model = self.config.get("model", "gpt-4o-mini")

        # Set API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            self.logger.warning("No OpenAI API key provided")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute LLM completion request"""
        try:
            # Extract parameters from input
            messages = input_data.get("messages", [])
            if not messages:
                raise ValueError("No messages provided for completion")

            # Get optional parameters
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 2000)

            # Make completion request (using sync for now as async isn't working well)
            response = completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract and return relevant response data
            usage_data = None
            if hasattr(response, "usage"):
                usage_data = {
                    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(
                        response.usage, "completion_tokens", 0
                    ),
                    "total_tokens": getattr(response.usage, "total_tokens", 0),
                }

            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": usage_data,
            }

        except Exception as e:
            self.logger.error(f"LiteLLM error: {str(e)}")
            return {"error": str(e), "content": None}


async def test_completion(prompt: str = "What is content marketing?"):
    """Test the LiteLLM plugin with a sample prompt"""
    try:
        llm = LiteLLM()
        print(f"\n🔄 Testing LiteLLM completion with prompt: {prompt}")

        result = await llm.execute({"messages": [{"role": "user", "content": prompt}]})

        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            return None

        print("\n✅ Successfully generated completion!")
        print("\nResponse:")
        print("-" * 50)
        print(result["content"])
        print("-" * 50)

        if result.get("usage"):
            print("\n📊 Token Usage:")
            print(f"- Prompt tokens: {result['usage'].get('prompt_tokens', 0)}")
            print(f"- Completion tokens: {result['usage'].get('completion_tokens', 0)}")
            print(f"- Total tokens: {result['usage'].get('total_tokens', 0)}")

        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    # Run test with a simple prompt
    import asyncio

    asyncio.run(test_completion())
