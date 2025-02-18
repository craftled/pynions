from typing import Dict, Any, Optional
import logging
from litellm import completion
from pynions.core import Plugin
from pynions.core.config import config


class LiteLLM(Plugin):
    """Plugin for interacting with LLMs using LiteLLM"""

    def __init__(self, plugin_config: Optional[Dict[str, Any]] = None):
        """Initialize the LiteLLM plugin with configuration"""
        super().__init__(plugin_config)
        self.logger = logging.getLogger("pynions.plugins.litellm")

        # Set default model and get appropriate API key
        self.model = self.config.get("model", "gpt-4o-mini")

        # Determine which API key to use based on model
        if "anthropic" in self.model:
            self.api_key = config.get("ANTHROPIC_API_KEY")
            if not self.api_key:
                raise ValueError("No Anthropic API key provided")
        else:
            self.api_key = config.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("No OpenAI API key provided")

        # Log configuration
        self.logger.info(f"Initialized LiteLLM with model: {self.model}")
        self.logger.info(
            f"Using API key for: {'Anthropic' if 'anthropic' in self.model else 'OpenAI'}"
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute LLM completion request with retry logic"""
        try:
            messages = input_data.get("messages", [])
            if not messages:
                raise ValueError("No messages provided for completion")

            # Get optional parameters with defaults
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens", 2000)
            max_retries = 5
            retry_delay = 10  # seconds between retries

            self.logger.info(f"Making completion request with {len(messages)} messages")
            self.logger.info(f"Model: {self.model}")
            self.logger.info(f"Temperature: {temperature}")
            self.logger.info(f"Max tokens: {max_tokens}")

            # Implement retry logic
            for attempt in range(max_retries):
                try:
                    # Make completion request
                    response = completion(
                        model=self.model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        api_key=self.api_key,
                        timeout=300,  # 5 minute timeout
                    )

                    # Extract usage data if available
                    usage_data = None
                    if hasattr(response, "usage"):
                        usage_data = {
                            "prompt_tokens": getattr(
                                response.usage, "prompt_tokens", 0
                            ),
                            "completion_tokens": getattr(
                                response.usage, "completion_tokens", 0
                            ),
                            "total_tokens": getattr(response.usage, "total_tokens", 0),
                        }

                    # Format response to match expected structure
                    formatted_response = {
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": response.choices[0].message.content,
                                }
                            }
                        ],
                        "model": response.model,
                        "usage": usage_data,
                    }

                    self.logger.info("Successfully generated completion")
                    if usage_data:
                        self.logger.info(f"Token usage: {usage_data}")

                    return formatted_response

                except Exception as e:
                    error_message = str(e)
                    if "overloaded" in error_message.lower():
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (
                                attempt + 1
                            )  # Exponential backoff
                            self.logger.warning(
                                f"Anthropic API overloaded. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})"
                            )
                            import asyncio

                            await asyncio.sleep(wait_time)
                            continue

                    self.logger.error(
                        f"LiteLLM error on attempt {attempt + 1}: {error_message}"
                    )
                    if attempt == max_retries - 1:
                        raise  # Re-raise the last error if all retries failed

            raise Exception(f"Failed after {max_retries} retries")

        except Exception as e:
            self.logger.error(f"LiteLLM error: {str(e)}")
            import traceback

            self.logger.error(traceback.format_exc())
            raise  # Re-raise the error for proper handling


async def test_completion(prompt: str = "What is SaaS content marketing?"):
    """Test the LiteLLM plugin with a sample prompt"""
    try:
        llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 2000,
            }
        )
        print(f"\n🔄 Testing LiteLLM completion with prompt: {prompt}")

        result = await llm.execute({"messages": [{"role": "user", "content": prompt}]})

        print("\n✅ Successfully generated completion!")
        print("\nResponse:")
        print("-" * 50)
        print(result["choices"][0]["message"]["content"])
        print("-" * 50)

        if result.get("usage"):
            print("\n📊 Token Usage:")
            print(f"- Prompt tokens: {result['usage'].get('prompt_tokens', 0)}")
            print(f"- Completion tokens: {result['usage'].get('completion_tokens', 0)}")
            print(f"- Total tokens: {result['usage'].get('total_tokens', 0)}")

        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_completion())
