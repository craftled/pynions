import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
from pynions import Worker
from pynions.plugins.litellm_plugin import LiteLLM
from pynions.workers.alternatives_search_worker import AlternativesSearchWorker


class AlternativesAnalysisWorker(Worker):
    """Worker for analyzing search results to extract alternative brands"""

    def __init__(self):
        self.llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze search results to extract alternative brands

        Args:
            input_data: dict containing:
                - brand: str - Original brand being researched
                - number_of_items: int - Number of alternatives to extract
                - search_results: dict - Raw search results from SerperWebSearch
        """
        brand = input_data["brand"]
        number_of_items = input_data.get("number_of_items", 5)
        search_results = input_data["search_results"]

        print("\n🤖 Analyzing search results...")

        try:
            alternatives_prompt = f"""
            Based on the search results, identify the top {number_of_items} most mentioned alternatives to {brand}.
            Return only the domain names (e.g., klaviyo.com) in a comma-separated list.
            
            Instructions:
            1. Only include domains that are actual alternatives to {brand}
            2. Verify each domain is mentioned in the search results
            3. Return in format: domain1.com, domain2.com, domain3.com
            4. Do not include {brand} in the results
            """

            response = await self.llm.execute(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": alternatives_prompt
                            + "\n\nSearch results:\n"
                            + str(search_results),
                        }
                    ]
                }
            )

            alternatives = [
                domain.strip()
                for domain in response["content"].split(",")
                if domain.strip() and "." in domain  # Basic domain validation
            ]

            if not alternatives:
                print("⚠️ No valid alternatives found in LLM response")
                return None

            print(f"✅ Extracted {len(alternatives)} alternatives")

            return {
                "brand": brand,
                "alternatives": alternatives,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            print(f"❌ Analysis error: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        test_brands = ["resend", "rewardful", "pipelince crm"]

        for brand in test_brands:
            print(f"\n🔍 Testing with brand: {brand}")

            # First get search results using AlternativesSearchWorker
            search_worker = AlternativesSearchWorker()
            search_results = await search_worker.execute(
                {"brand": brand, "number_of_items": 5}
            )

            if search_results:
                # Then analyze the results
                analysis_worker = AlternativesAnalysisWorker()
                result = await analysis_worker.execute(
                    {
                        "brand": brand,
                        "number_of_items": 5,
                        "search_results": search_results,
                    }
                )

                if result:
                    print("\nExtracted Alternatives for {brand}:")
                    print(json.dumps(result, indent=2))

                    print("\nAlternatives List:")
                    for idx, domain in enumerate(result["alternatives"], 1):
                        print(f"{idx}. {domain}")

                    print(f"\nTimestamp: {result['timestamp']}")
                    print("-" * 50)

    asyncio.run(test())
