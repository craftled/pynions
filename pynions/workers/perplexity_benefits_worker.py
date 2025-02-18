import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityBenefitsWorker(Worker):
    """Worker for identifying advantages and benefits of a topic using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Balanced for comprehensive analysis
                "max_tokens": 2500,  # Sufficient for detailed benefits
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/benefits", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/benefits/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract benefits and advantages of a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing benefits and advantages of: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a benefits analysis expert. Your task is to:
1. Identify all significant advantages and benefits
2. Categorize benefits by type (e.g., financial, operational)
3. Find quantifiable impact metrics
4. Provide real-world success examples
5. Note context-specific benefits
6. Use data from reliable sources
7. Compare benefits across different scenarios""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research the benefits and advantages of '{topic}'. Focus on:
1. What are the main benefits and advantages?
2. How can these benefits be measured or quantified?
3. What real-world examples demonstrate these benefits?
4. How do benefits vary by context or implementation?
5. What ROI or impact metrics are available?
6. Are there any unique or unexpected advantages?
7. What do case studies reveal about the benefits?

Use authoritative sources and include specific metrics, case studies, and success stories where available. Organize benefits by category with clear examples.""",
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
        worker = PerplexityBenefitsWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
