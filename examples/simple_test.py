import asyncio
import os
from dotenv import load_dotenv
from pynions import Flow, BaseTool
from pynions.tools.llm import AskLLM

# Load environment variables
load_dotenv()

# Verify we have API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"Using OpenAI API Key: {api_key[:6]}...")


class Uppercase(BaseTool):
    async def run(self, data):
        print("\n[Uppercase Tool] Converting to uppercase...")
        text = data.get("llm_response", "")
        result = text.upper()
        print(f"[Uppercase Tool] Result: {result}")
        return {"result": result}


async def main():
    print("\n=== Starting Pynions Test ===")

    # Create flow
    flow = Flow()

    # Create LLM tool with a more obvious prompt
    llm_tool = AskLLM(
        prompt_template="Act as a creative writer. Write a very short story about: {input}"
    )

    print("\n[Setup] Created flow with LLM and Uppercase tools")

    # Add steps
    flow.add_step(llm_tool)
    flow.add_step(Uppercase())

    print("\n[Running] Starting flow execution...")
    result = await flow.run(
        {
            "input": "a little red fox scientist in the woods in Lithuania trying to find the door to parallel universe"
        }
    )

    print("\n=== Final Results ===")
    print("Original LLM Response:", result.get("llm_response"))
    print("Uppercase Version:", result.get("result"))


if __name__ == "__main__":
    asyncio.run(main())
