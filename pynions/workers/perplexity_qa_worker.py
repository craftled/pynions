import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityQAWorker(Worker):
    """Worker for generating comprehensive Q&A content using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Balanced for accurate answers
                "max_tokens": 4000,  # Higher for comprehensive Q&A
                "return_related_questions": True,  # Enable related questions
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/qa", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/qa/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate comprehensive Q&A content for a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Generating Q&A content for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a Q&A content expert. Your task is to:
1. Generate comprehensive FAQ content
2. Cover fundamental to advanced questions
3. Provide clear, accurate answers
4. Include practical examples
5. Address common misconceptions
6. Consider different user levels
7. Include relevant statistics
8. Cite authoritative sources""",
                        },
                        {
                            "role": "user",
                            "content": f"""Create a comprehensive Q&A guide about '{topic}'. Include:

1. Fundamental Questions
   - What is it?
   - Why is it important?
   - When should it be used?
   - Who should use it?

2. Implementation Questions
   - How to get started?
   - What resources are needed?
   - What are the key steps?
   - How to measure success?

3. Advanced Questions
   - What are best practices?
   - How to optimize?
   - What are common pitfalls?
   - How to scale?

4. Troubleshooting Questions
   - Common problems and solutions
   - Performance issues
   - Integration challenges
   - Maintenance concerns

5. Strategic Questions
   - Long-term considerations
   - Cost implications
   - ROI expectations
   - Future trends

Use authoritative sources and include specific examples, data points, and case studies where relevant. Structure answers to be clear and actionable.""",
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
        worker = PerplexityQAWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
