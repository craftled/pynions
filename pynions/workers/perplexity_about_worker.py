import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityAboutWorker(Worker):
    """Worker for extracting company information from a website using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,
                "max_tokens": 4000,
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, domain: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/about", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/about/{domain}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract company information from a domain"""
        domain = input_data["domain"]
        print(f"\n🔍 Analyzing company information for {domain}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a company research expert. When analyzing companies:
1. Prioritize CURRENT information over historical data
2. Verify leadership information from the most recent sources
3. Note any acquisitions or ownership changes
4. Check for recent press releases about leadership changes
5. Cross-reference information across multiple sources
6. Indicate when information might be outdated""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research current company information for {domain}. Focus on:

1. Current ownership status (independent/acquired/public)
2. Current leadership team (CEO, key executives)
3. Company history and major milestones
4. Recent developments (last 12 months)
5. Mission and values
6. Notable achievements and metrics

Prioritize official sources (company website, press releases) and recent news. If you find conflicting information about leadership or ownership, note this and provide dates for the information.""",
                        },
                    ]
                }
            )

            if response:
                # Save the complete response
                saved_file = self.save_to_file(response, domain)
                print(f"\n💾 Response saved to: {saved_file}")
                return response
            else:
                print("❌ No response from API")
                return None

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return None


# Test
if __name__ == "__main__":

    async def test():
        worker = PerplexityAboutWorker()
        result = await worker.execute({"domain": "rewardful.com"})

    asyncio.run(test())
