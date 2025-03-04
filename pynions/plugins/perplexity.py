import os
import json
import httpx
import asyncio
from typing import Dict, Any
from .base import Plugin


class PerplexityAPI(Plugin):
    """Plugin for interacting with Perplexity AI API"""

    def __init__(self, config=None):
        super().__init__(config)
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        print(f"API Key found: {'Yes' if self.api_key else 'No'}")
        print(
            f"API Key starts with: {self.api_key[:8]}..."
            if self.api_key
            else "No API key"
        )

        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.default_config = {
            "model": "sonar-reasoning-pro",  # Supported Models https://docs.perplexity.ai/guides/model-cards
            "max_tokens": 1000,
            "temperature": 0.2,
            "top_p": 0.9,
            "search_domain_filter": None,
            "return_images": False,
            "return_related_questions": False,
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1,
            "response_format": None,
        }
        # Merge default config with provided config
        self.config = {**self.default_config, **(config or {})}
        self.initialize()

    def initialize(self):
        """Initialize the plugin"""
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is required")
        if not self.api_key.startswith("pplx-"):
            raise ValueError(
                "Invalid PERPLEXITY_API_KEY format. It should start with 'pplx-'"
            )

    def cleanup(self):
        """Cleanup plugin resources"""
        pass

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a request to Perplexity AI API with retry logic

        Args:
            input_data: Dictionary containing:
                - messages: List of message dictionaries with 'role' and 'content'
                - Any other optional parameters to override defaults

        Returns:
            API response as a dictionary
        """
        max_retries = 3
        retry_delay = 5  # seconds
        current_retry = 0

        while current_retry < max_retries:
            try:
                # Prepare the payload
                payload = {
                    **self.config,
                    "messages": input_data.get("messages", []),
                }

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                }

                # Using 2 minutes timeout for complex reasoning tasks
                timeout = httpx.Timeout(120.0, connect=30.0)
                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(
                        self.base_url, json=payload, headers=headers
                    )

                    try:
                        response_data = response.json()
                    except:
                        print(f"Raw response text: {response.text}")
                        raise ValueError("Failed to parse JSON response")

                    if response.status_code == 401:
                        raise ValueError("Invalid Perplexity API key")
                    elif response.status_code == 422:
                        error_data = response.json()
                        raise ValueError(
                            f"Invalid request: {error_data.get('detail', 'Unknown validation error')}"
                        )
                    elif response.status_code == 524:
                        if current_retry < max_retries - 1:
                            print(
                                f"Request timeout, retrying in {retry_delay} seconds..."
                            )
                            await asyncio.sleep(retry_delay)
                            current_retry += 1
                            continue
                        else:
                            raise ValueError(
                                "Maximum retries reached for timeout error"
                            )

                    response.raise_for_status()
                    return response.json()

            except httpx.TimeoutException as e:
                if current_retry < max_retries - 1:
                    print(f"Timeout error, retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    current_retry += 1
                    continue
                print(f"Timeout error after {max_retries} retries: {str(e)}")
                raise ValueError(
                    f"Request timed out after {max_retries} retries. The model is taking longer than expected to respond."
                )
            except httpx.HTTPError as e:
                if current_retry < max_retries - 1:
                    print(f"HTTP error, retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    current_retry += 1
                    continue
                print(f"HTTP error details after {max_retries} retries: {str(e)}")
                raise ValueError(f"HTTP error occurred: {str(e)}")
            except Exception as e:
                if current_retry < max_retries - 1:
                    print(f"Unexpected error, retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    current_retry += 1
                    continue
                print(f"Unexpected error details after {max_retries} retries: {str(e)}")
                raise ValueError(f"Error making request to Perplexity API: {str(e)}")

        raise ValueError(f"Failed after {max_retries} retries")
