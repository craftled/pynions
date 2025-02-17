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
                            "role": "user",
                            "content": f"What is the company background and key information about {domain}? Include company history, mission, key team members, notable achievements, and funding if available. Only use official sources and recent reliable news.",
                        }
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
        result = await worker.execute({"domain": "notion.so"})

    asyncio.run(test())
