from pynions.core.workflow import Workflow
from pynions.tools.llm import LLM
async def main():
    """Example workflow that generates a tweet"""
    workflow = Workflow()
    llm = LLM()
tweet = await llm.complete("Write a tweet about AI automation")
print(f"Generated tweet: {tweet}")
if name == "main":
import asyncio
asyncio.run(main())