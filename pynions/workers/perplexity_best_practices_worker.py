import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityBestPracticesWorker(Worker):
    """Worker for identifying best practices and implementation guidelines using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Balanced for comprehensive analysis
                "max_tokens": 3000,  # Higher for detailed guidelines
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/best_practices", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/best_practices/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract best practices and implementation guidelines for a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing best practices and guidelines for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a best practices and implementation expert. Your task is to:
1. Identify proven best practices and guidelines
2. Organize recommendations by implementation phase
3. Provide specific, actionable steps
4. Include industry standards and frameworks
5. Note context-specific adaptations
6. Reference successful implementations
7. Consider scalability and maintenance
8. Include quality assurance measures""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research the best practices and implementation guidelines for '{topic}'. Focus on:
1. What are the established best practices?
2. What are the key implementation steps?
3. What quality standards should be followed?
4. How should progress be measured?
5. What tools and resources are recommended?
6. How should testing and validation be done?
7. What maintenance practices are important?
8. How do best practices vary by scale or context?

Use authoritative sources (industry standards, professional organizations, expert practitioners). Include specific examples of successful implementations and organize recommendations by phase with clear, actionable steps.""",
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
        worker = PerplexityBestPracticesWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
