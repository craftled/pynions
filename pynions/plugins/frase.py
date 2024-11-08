from pynions.core import Plugin
import os
import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import json


class Frase(Plugin):
    """Plugin for processing URLs using Frase.io API"""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        load_dotenv()
        # Get API key from config or environment
        self.api_key = config.get("api_key") if config else None
        if not self.api_key:
            self.api_key = os.getenv("FRASE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "FRASE_API_KEY not found in environment variables or config"
            )

        # Update base URL and headers according to docs
        self.base_url = "https://api.frase.io/api/v1/process_serp"
        self.headers = {
            "token": self.api_key,  # API key should be in token header field
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def execute(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute the Frase API request"""
        try:
            # Validate input
            if "serp_urls" not in params:
                self.logger.error("serp_urls is required in params")
                return None

            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json={"serp_urls": params["serp_urls"]},  # Simplified payload
                    timeout=30,
                ) as response:
                    # Get response text first as mentioned
                    text = await response.text()

                    if response.status != 200:
                        self.logger.error(f"Error from Frase API: {response.status}")
                        self.logger.error(f"Response text: {text}")
                        return None

                    try:
                        # Parse response text as JSON
                        return json.loads(text)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Failed to parse JSON response: {e}")
                        self.logger.error(f"Raw response: {text}")
                        return None

        except Exception as e:
            self.logger.error(f"Error processing URLs: {e}")
            return None


async def test_frase(urls: List[str] = None):
    """Test the Frase API with sample URLs"""
    if urls is None:
        urls = [
            "https://www.goodhousekeeping.com/home/gardening/g4348/summer-flowers/",
            "https://www.countryliving.com/life/g32036880/flowers-bloom-in-summer/",
        ]

    try:
        plugin = Frase()
        print(f"\n🔄 Processing {len(urls)} URLs...")
        result = await plugin.execute({"serp_urls": urls})

        if not result:
            print("\n❌ Failed to process URLs")
            return None

        print("\n✅ Successfully processed URLs!")

        # Print raw response for debugging
        print("\n🔍 Raw API Response:")
        print("-" * 50)
        print(json.dumps(result, indent=2))
        print("-" * 50)

        # Print items summary if available
        if "items" in result:
            print("\n📄 Processed Items:")
            print("-" * 50)
            for idx, item in enumerate(result["items"], 1):
                print(f"\n{idx}. {item.get('title', 'No title')}")
                print(f"   URL: {item.get('url', 'No URL')}")
                if "word_count" in item:
                    print(f"   Word count: {item['word_count']}")
                if (
                    "questions" in item and item["questions"]
                ):  # Check if questions exists and is not None
                    print(f"   Questions found: {len(item['questions'])}")
                if (
                    "entities" in item and item["entities"]
                ):  # Check if entities exists and is not None
                    print(f"   Entities found: {len(item['entities'])}")

        # Print aggregate metrics if available
        if "aggregate_metrics" in result:
            print("\n📊 Aggregate Metrics:")
            print("-" * 50)
            metrics = result["aggregate_metrics"]
            for key, value in metrics.items():
                print(f"{key}: {value}")

        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")
        return None


if __name__ == "__main__":
    asyncio.run(test_frase())
