import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions import Worker
from pynions.plugins.perplexity import PerplexityAPI


class PerplexityMethodologyWorker(Worker):
    """Worker for explaining how things work and their processes using Perplexity AI"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,  # Slightly higher for more detailed explanations
                "max_tokens": 3000,  # Higher for step-by-step explanations
                "return_related_questions": False,
            }
        )

    def save_to_file(self, data: Dict, topic: str) -> str:
        """Save the raw result to a JSON file"""
        # Create data directory if it doesn't exist
        os.makedirs("data/methodologies", exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/methodologies/{topic}_{timestamp}.json"

        # Save the raw data
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    async def execute(self, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract methodology and process information for a topic"""
        topic = input_data["topic"]
        print(f"\n🔍 Analyzing methodology and processes for: {topic}")
        print("⏳ This may take up to 3 minutes...")

        try:
            # Make the API request
            response = await self.perplexity.execute(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a process and methodology expert. Your task is to:
1. Break down complex processes into clear steps
2. Explain how systems and methods work
3. Identify key principles and mechanisms
4. Note any variations in methodology
5. Only use reliable, technical sources
6. Include real-world examples where relevant
7. Highlight critical dependencies and requirements""",
                        },
                        {
                            "role": "user",
                            "content": f"""Explain how '{topic}' works. Focus on:
1. What are the core mechanisms/processes involved?
2. What are the step-by-step procedures?
3. What are the key principles behind it?
4. What are the requirements and dependencies?
5. Are there different methodologies or approaches?
6. What are common implementation methods?

Only use technical documentation, academic sources, and industry standards. Include specific examples where helpful.""",
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
        worker = PerplexityMethodologyWorker()
        result = await worker.execute({"topic": "growth marketing"})

    asyncio.run(test())
