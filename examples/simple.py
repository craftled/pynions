from pynions import Workflow, AskLLM

async def main():
    # Create workflow
    workflow = Workflow("Tweet Generator")

    # Add AI tool
    workflow.add(
        AskLLM(
            prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
            model="gpt-4o-mini"
        )
    )

    # Run workflow
    result = await workflow.run({"topic": "AI tools for marketers"})
    
    # Print result
    print("\n📝 Generated Tweet:")
    print(result["llm_response"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
