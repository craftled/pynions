import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityTypesWorker(Worker):
    """Worker for identifying and categorizing different types and variations of a topic using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Balanced for comprehensive categorization
                "max_tokens": 3000,  # Higher for detailed type descriptions
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/types", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/types/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract and categorize different types and variations of a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing types and categories for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a classification and categorization expert. Your task is to:
1. Identify all distinct types and variations
2. Create clear, logical categorization systems
3. Compare and contrast different types
4. Note industry-standard classifications
5. Highlight key characteristics of each type
6. Provide real-world examples of each type
7. Use authoritative sources for categorization""",
                        },
                        {
                            "role": "user",
                            "content": f"""Identify and categorize all types and variations of '{topic}'. Focus on:
1. What are the main categories or types?
2. How are they typically classified in the industry?
3. What are the key characteristics of each type?
4. What are real-world examples of each type?
5. How do different types compare to each other?
6. Are there any hybrid or emerging types?
7. What are the standard industry classifications?

Use authoritative sources (industry standards, academic papers, professional organizations). Structure the response with clear categories and comparisons.""",
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
        worker = PerplexityTypesWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
