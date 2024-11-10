import asyncio
import aiohttp
from typing import Any, Dict, Optional
from pynions.core import Plugin
from pynions.core.config import config


class JinaAIReader(Plugin):
    """Plugin for extracting content from URLs using Jina AI Reader API"""

    def __init__(self, plugin_config: Dict[str, Any] = None):
        super().__init__(plugin_config)
        self.api_key = config.get("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("JINA_API_KEY not found in configuration")

        self.base_url = "https://r.jina.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract content from a URL using Jina AI Reader"""
        url = input_data.get("url")
        if not url:
            raise ValueError("URL is required in input_data")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/{url}", headers=self.headers
                ) as response:
                    if response.status != 200:
                        error_msg = f"Jina API error: {response.status}"
                        if response.status == 401:
                            error_msg += " (Invalid API key)"
                        self.logger.error(error_msg)
                        return None

                    data = (await response.json()).get("data", {})
                    return {
                        "title": data.get("title", ""),
                        "description": data.get("description", ""),
                        "url": data.get("url", url),
                        "content": data.get("content", ""),
                    }

        except Exception as e:
            self.logger.error(f"Error extracting content: {str(e)}")
            return None


async def test_reader():
    """Test the Jina AI Reader with a sample URL"""
    url = "https://marketful.com/blog/marketing-planning-tools/"
    try:
        reader = JinaAIReader()
        print(f"\n🔄 Extracting content from: {url}")
        result = await reader.execute({"url": url})

        if not result:
            print("\n❌ Failed to extract content")
            return None

        print("\n✅ Successfully extracted content!")
        print("\nMetadata:")
        print("-" * 50)
        for key in ["title", "description", "url"]:
            if result[key]:
                print(f"{key.title()}: {result[key]}")

        print("\nContent:")
        print("-" * 50)
        print(result["content"])
        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    asyncio.run(test_reader())
