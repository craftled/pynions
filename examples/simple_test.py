from pynions import Flow
from pynions.tools.llm import AskLLM

# Create flow
flow = Flow()

# Add AI tool
flow.add_tool(AskLLM(prompt="Write a tweet about: {input}"))

# Run
result = await flow.run({"input": "AI tools for marketers"})
print(result["response"])
