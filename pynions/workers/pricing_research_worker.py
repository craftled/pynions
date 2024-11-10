import asyncio
import json
from typing import Dict, Any
from pynions import Worker
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader
from pynions.plugins.litellm_plugin import LiteLLM


class PricingResearchWorker(Worker):
    """Worker for extracting pricing data from a website"""

    def __init__(self):
        self.serper = SerperWebSearch({"max_results": 1})
        self.jina = JinaAIReader()
        self.llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        )

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure pricing data from a domain"""
        domain = input_data["domain"]
        print(f"\n🔍 Analyzing pricing for {domain}")

        try:
            # Get pricing page URL
            search_result = await self.serper.execute(
                {"query": f"site:{domain} pricing"}
            )
            if not search_result.get("organic"):
                return None

            url = search_result["organic"][0]["link"]
            print(f"📄 Found pricing page: {url}")

            # Extract content
            content = await self.jina.execute({"url": url})
            if not content or not content.get("content"):
                return None

            print(f"✅ Extracted {len(content['content'])} characters")

            # Analyze with LLM - using full content
            response = await self.llm.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a precise pricing data extractor. Your task is to extract EXACT pricing information from websites.
                            Instructions:
                            1. Only include information that is explicitly stated in the content
                            2. Use exact prices, features, and limits as shown
                            3. Do not make assumptions or fill in missing data
                            4. If a value is not found, exclude it from the output

                            Output format:
                            {
                            "plans": ["exact plan names found"],
                            "pricing": {
                                "plan_name": {
                                "monthly_price": exact_number_from_content,
                                "annual_price": exact_number_from_content,
                                "features": ["exact feature text"],
                                "limits": {"exact limit name": "exact limit value"}
                                }
                            },
                            "currency": "exact currency code found"
                            }""",
                        },
                        {
                            "role": "user",
                            "content": f"Extract the pricing structure from this content. Only include explicitly stated information:\n\n{content['content']}",
                        },
                    ]
                }
            )

            # Parse response
            pricing_data = json.loads(response["content"])
            return {"domain": domain, "source": url, "pricing": pricing_data}

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        worker = PricingResearchWorker()
        result = await worker.execute({"domain": "rewardful.com"})
        if result:
            print("\nPricing Data:")
            print(json.dumps(result, indent=2))

    asyncio.run(test())
