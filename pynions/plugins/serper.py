import asyncio
import aiohttp
from typing import Dict, Any, Optional
from pynions.core import Plugin
from pynions.core.config import config


class SerperWebSearch(Plugin):
    """Plugin for fetching SERP data using Serper.dev API"""

    def __init__(self, plugin_config: Dict[str, Any] = None):
        super().__init__(plugin_config)
        self.api_key = config.get("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in configuration")

        self.base_url = "https://google.serper.dev/search"
        self.headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute SERP search request"""
        query = input_data.get("query")
        if not query:
            raise ValueError("Query is required in input_data")

        payload = {
            "q": query,
            "num": self.config.get("max_results", 10),
            "include_people_also_ask": True,
            "include_related_searches": True,
            "include_top_stories": True,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url, headers=self.headers, json=payload
                ) as response:
                    if response.status != 200:
                        error_msg = f"Serper API error: {response.status}"
                        if response.status == 401:
                            error_msg += " (Invalid API key)"
                        self.logger.error(error_msg)
                        return None

                    return await response.json()

        except Exception as e:
            self.logger.error(f"Error fetching search results: {str(e)}")
            return None


async def test_search(query: str = "best marketing automation tools 2024"):
    """Test the Serper Web Search with a sample query"""
    try:
        searcher = SerperWebSearch()
        print(f"\n🔍 Searching for: {query}")
        result = await searcher.execute({"query": query})

        if not result:
            print("\n❌ Failed to fetch search results")
            return None

        print("\n✅ Successfully fetched search results!")

        # Print search parameters
        if "searchParameters" in result:
            print("\n⚙️ Search Parameters:")
            print("-" * 50)
            params = result["searchParameters"]
            print(f"Query: {params.get('q')}")
            print(f"Type: {params.get('type')}")
            print(f"Engine: {params.get('engine')}")

        # Print organic results
        print("\n🌐 Organic Results:")
        print("-" * 50)
        for item in result.get("organic", []):
            print(f"\nPosition: {item.get('position', 'N/A')}")
            print(f"Title: {item.get('title')}")
            print(f"Link: {item.get('link')}")
            print(f"Snippet: {item.get('snippet')}")
            if "date" in item:
                print(f"Date: {item.get('date')}")
            if "sitelinks" in item:
                print("\nSitelinks:")
                for sitelink in item["sitelinks"]:
                    print(f"- {sitelink.get('title')}: {sitelink.get('link')}")
            print("-" * 30)

        # Print "People Also Ask" questions
        if "peopleAlsoAsk" in result and result["peopleAlsoAsk"]:
            print("\n❓ People Also Ask:")
            print("-" * 50)
            for item in result["peopleAlsoAsk"]:
                print(f"\nQ: {item.get('question')}")
                print(f"A: {item.get('snippet')}")
                print(f"Source: {item.get('title')} ({item.get('link')})")
                print("-" * 30)

        # Print related searches
        if "relatedSearches" in result and result["relatedSearches"]:
            print("\n🔍 Related Searches:")
            print("-" * 50)
            for item in result["relatedSearches"]:
                print(f"- {item.get('query')}")

        # Print credits used
        if "credits" in result:
            print(f"\n💰 Credits Used: {result['credits']}")

        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    asyncio.run(test_search())
