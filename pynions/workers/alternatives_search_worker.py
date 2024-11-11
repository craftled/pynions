import asyncio
import json
from typing import Dict, Any
from pynions import Worker
from pynions.plugins.serper import SerperWebSearch
from datetime import datetime


class AlternativesSearchWorker(Worker):
    """Worker for finding alternatives to a specific brand through SERP analysis"""

    def __init__(self):
        self.serper = SerperWebSearch({"max_results": 10})

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find alternatives for a given brand

        Args:
            input_data: dict containing:
                - brand: str - The brand to find alternatives for
                - number_of_items: int - Number of alternatives to find (default: 5)
        """
        brand = input_data["brand"]
        number_of_items = input_data.get("number_of_items", 5)

        print(f"\n🔎 Searching for {brand} alternatives...")
        print(f"📊 Looking for top {number_of_items} alternatives")

        try:
            results = await self.serper.execute(
                {"query": f"best {brand} alternatives {datetime.now().year}"}
            )

            if not results.get("organic"):
                raise ValueError("No search results found")

            print(f"✅ Found {len(results['organic'])} results")

            # Process and structure the results
            alternatives = []
            for result in results["organic"][:number_of_items]:
                alternatives.append(
                    {
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                        "position": result.get("position", 0),
                        "date": result.get("date", ""),
                        "sitelinks": result.get("sitelinks", []),
                    }
                )

            response_data = {
                "brand": brand,
                "search_parameters": results.get("searchParameters", {}),
                "alternatives": alternatives,
                "related_searches": results.get("relatedSearches", []),
                "people_also_ask": results.get("peopleAlsoAsk", []),
                "credits_used": results.get("credits", 0),
                "timestamp": datetime.now().isoformat(),
            }

            print(f"\n📝 Processed {len(alternatives)} alternatives")
            return response_data

        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        worker = AlternativesSearchWorker()
        result = await worker.execute({"brand": "mailchimp", "number_of_items": 5})

        if result:
            print("\nAlternatives Data:")
            print(json.dumps(result, indent=2))

            print("\nTop Alternatives Found:")
            for idx, alt in enumerate(result["alternatives"], 1):
                print(f"\n{idx}. {alt['title']}")
                print(f"   URL: {alt['link']}")
                if alt.get("date"):
                    print(f"   Date: {alt['date']}")
                if alt.get("sitelinks"):
                    print("   Sitelinks:")
                    for sitelink in alt["sitelinks"]:
                        print(f"   - {sitelink['title']}: {sitelink['link']}")

            if result.get("related_searches"):
                print("\nRelated Searches:")
                for search in result["related_searches"]:
                    print(f"- {search['query']}")

            if result.get("credits_used"):
                print(f"\n💰 Credits Used: {result['credits_used']}")

    asyncio.run(test())
