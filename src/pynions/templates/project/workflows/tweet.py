try:
    from pynions import Workflow, AskLLM
except ImportError:
    print("❌ Error: pynions package not found.")
    print("💡 Try: pip install -r requirements.txt")
    exit(1)


async def main():
    """Example workflow that generates a tweet"""
    workflow = Workflow("Tweet Generator")

    workflow.add(
        AskLLM(
            prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
            model="gpt-4o-mini",
        )
    )

    result = await workflow.run({"topic": "AI automation"})
    print(f"\nGenerated tweet: {result['llm_response']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
