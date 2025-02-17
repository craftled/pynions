import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI

# ANSI Color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"
BOLD = "\033[1m"


class PerplexityFeaturesWorker(Worker):
    """Worker for extracting feature information from a website using Perplexity AI"""

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
        os.makedirs("data/features", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/features/{domain}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract feature information from a domain"""
        domain = input_data["domain"]
        print(f"\n🔍 Analyzing features for {domain}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"What are the main features of {domain}? List them in detail with sources.",
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
        worker = PerplexityFeaturesWorker()
        result = await worker.execute({"domain": "notion.so"})

    asyncio.run(test())
