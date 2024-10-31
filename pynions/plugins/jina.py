import os
import asyncio
import aiohttp
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from pynions.core import Plugin


class JinaAIReader(Plugin):
    """Plugin for extracting content from URLs using Jina AI Reader API"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        load_dotenv()  # Load environment variables
        self.api_key = os.getenv("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in environment variables")

        self.base_url = "https://r.jina.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    async def execute(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract content from a URL using Jina AI Reader

        Args:
            input_data: Dict containing 'url' key
        Returns:
            Extracted content as string or None if extraction fails
        """
        url = input_data.get("url")
        if not url:
            raise ValueError("URL is required in input_data")

        try:
            jina_url = f"{self.base_url}/{url}"
            async with aiohttp.ClientSession() as session:
                async with session.get(jina_url, headers=self.headers) as response:
                    if response.status != 200:
                        self.logger.error(f"Jina API error: {response.status}")
                        if response.status == 401:
                            self.logger.error("Invalid API key")
                        return None

                    content = await response.text()
                    return content

        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return None

    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        return bool(self.api_key)


async def test_reader():
    """Test the Jina AI Reader with a sample URL"""
    test_url = "https://www.close.com/blog/cold-email-software"

    try:
        # Initialize reader
        reader = JinaAIReader()

        # Extract content
        print(f"\n🔄 Extracting content from: {test_url}")
        result = await reader.execute({"url": test_url})

        if result:
            print("\n✅ Successfully extracted content!")
            print("\nFirst 500 characters:")
            print("-" * 50)
            print(result[:500] + "...")
            return result
        else:
            print("\n❌ Failed to extract content")
            return None

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_reader())
