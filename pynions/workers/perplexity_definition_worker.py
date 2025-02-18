import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityDefinitionWorker(Worker):
    """Worker for extracting clear definitions and origins of topics using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.1,  # Lower temperature for more precise definitions
                "max_tokens": 2000,  # Reduced as definitions are typically concise
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/definitions", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/definitions/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract definition and origin information for a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing definition and origin for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a definition expert. Your task is to:
1. Find precise, authoritative definitions
2. Trace historical origins and etymology
3. Note key developments in meaning over time
4. Identify academic or industry-standard definitions
5. Only use reliable, verifiable sources
6. Note any variations in definition across different contexts""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research the definition and origin of '{topic}'. Focus on:
1. What is the most precise, current definition?
2. What is its origin/etymology?
3. How has the definition evolved?
4. Are there different definitions in different contexts?
5. What are the authoritative sources for this definition?

Only use reliable sources (academic papers, industry standards, official documentation).""",
                        },
                    ]
                }
            )

            if response:
                # Save the complete response
                saved_file = self.save_to_file(response, topic)
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
        worker = PerplexityDefinitionWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
