from pynions import Workflow
from pynions.tools.llm import AskLLM

# Create a content generation workflow
workflow = Workflow("Content Generator")

# Add tools in sequence
workflow.add(
    AskLLM(prompt="Generate 5 tweet ideas about: {topic}. Format as a numbered list.")
).add(
    AskLLM(
        prompt="For this tweet idea: {tweet_ideas}\n\nGenerate 3 variations with different tones: professional, casual, and humorous. Format as a numbered list."
    )
)

# Run workflow
result = await workflow.run({"topic": "AI tools for marketing automation"})

print("\n🎯 Generated Tweets:")
print(result["llm_response"])
