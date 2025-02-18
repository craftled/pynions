import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityChallengesWorker(Worker):
    """Worker for identifying challenges and limitations of a topic using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Balanced for comprehensive analysis
                "max_tokens": 2500,  # Sufficient for detailed challenges
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/challenges", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/challenges/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract challenges and limitations of a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing challenges and limitations of: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a challenges and risk analysis expert. Your task is to:
1. Identify significant challenges and limitations
2. Categorize issues by type (technical, operational, etc.)
3. Assess impact and severity of challenges
4. Find common failure points and pitfalls
5. Note context-specific difficulties
6. Use data from real-world examples
7. Analyze mitigation strategies
8. Consider regulatory and compliance issues""",
                        },
                        {
                            "role": "user",
                            "content": f"""Research the challenges and limitations of '{topic}'. Focus on:
1. What are the main challenges and limitations?
2. What are common pitfalls and failure points?
3. How do these challenges impact implementation?
4. What are the technical limitations?
5. What operational difficulties exist?
6. Are there regulatory or compliance challenges?
7. What resource constraints are common?
8. How do challenges vary by context or scale?

Use authoritative sources and include specific examples, case studies, and industry reports. Organize challenges by category and severity, with real-world examples of how organizations have faced these issues.""",
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
        worker = PerplexityChallengesWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
