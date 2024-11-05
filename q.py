import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from litellm import acompletion

# Load environment variables
load_dotenv()

class QuickAI:
    async def analyze(self, topic):
        try:
            response = await acompletion(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": "You are a helpful AI assistant that analyzes topics."
                }, {
                    "role": "user",
                    "content": f"Analyze this topic: {topic}"
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

async def main():
    # Initialize
    print("\n🤖 Pynions Quick Start Demo")
    print("---------------------------")

    try:
        ai = QuickAI()

        # Get user input
        topic = input("\n📝 Enter a topic to analyze: ")

        # Process
        print("\n🔄 Analyzing...")
        result = await ai.analyze(topic)

        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/analysis_{timestamp}.txt"

        os.makedirs('data', exist_ok=True)
        with open(filename, 'w') as f:
            f.write(result)

        # Display result
        print("\n📊 Analysis Results:")
        print("------------------")
        print(result)
        print(f"\n✅ Results saved to: {filename}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Check if OPENAI_API_KEY is set in .env")
        print("2. Verify internet connection")
        print("3. Ensure OpenAI API is accessible")

if __name__ == "__main__":
    asyncio.run(main())