import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityTrendsWorker(Worker):
    """Worker for identifying future trends and developments using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.3,  # Slightly higher for trend analysis
                "max_tokens": 3000,  # Higher for comprehensive trend analysis
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/trends", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/trends/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract future trends and developments for a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing future trends and developments for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a trends and future developments expert. Your task is to:
1. Identify emerging trends and patterns
2. Analyze future developments and predictions
3. Evaluate technology impacts and innovations
4. Consider market and industry shifts
5. Assess regulatory and policy changes
6. Note demographic and social influences
7. Examine competitive landscape changes
8. Consider global and regional variations""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research future trends and developments in '{topic}'. Focus on:
1. What are the emerging trends and patterns?
2. What technological developments are expected?
3. How is the market/industry evolving?
4. What innovations are on the horizon?
5. What regulatory changes are expected?
6. How are user/customer needs changing?
7. What competitive shifts are occurring?
8. What are the long-term predictions?

Use authoritative sources (industry reports, research papers, expert predictions, market analyses). Include specific examples, timelines, and data points where available. Organize trends by timeframe (near-term, mid-term, long-term) and impact level.""",
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
        worker = PerplexityTrendsWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
