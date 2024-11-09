---
title: "BOFU Content Ideas Generator"
summary: "Generate bottom-of-funnel content ideas for your product"
---

## Overview
This example shows how to generate bottom-of-funnel (BOFU) content ideas using AI. Perfect for creating conversion-focused content like case studies, comparison guides, and tutorials.

## Usage

```python
from pynions import QuickAI

# Initialize AI with default settings
ai = QuickAI()

# Generate BOFU content ideas
ideas = ai.generate_content_ideas(
    product="Marketing Automation Tool",
target_audience="B2B Marketing Managers"
)

# Save results
ai.save_result(ideas, prefix="bofu_ideas")
```


## Example Output

```markdown
Case Study
Title: "How Company X Increased Lead Quality by 300% with Our Tool"
Goal: Drive demo signups
ROI Calculator
Title: "Marketing Automation ROI Calculator"
Goal: Demonstrate cost savings
[...more ideas...]
```

3. Similarly, let's convert the advanced analysis example (referencing existing code):

41:126:examples/advanced.py

```python
class QuickAI:
def init(self, custom_config=None):
self.config = load_config(custom_config)
self.api_key = os.getenv("OPENAI_API_KEY")
if not self.api_key:
raise ValueError("Please add your OpenAI API key to .env file")
os.environ["OPENAI_API_KEY"] = self.api_key
# Initialize plugins
self.plugins = {}
if self.config["plugins"]["stats"]["enabled"]:
self.plugins["stats"] = StatsPlugin(self.config["plugins"]["stats"])
self.plugins["stats"].initialize()
def analyze(self, topic):
"""Analyze a topic using the configured LLM"""
try:
messages = [
{
"role": "user",
"content": self.config["prompt"]["template"].format(topic=topic),
}
]
# Start stats tracking if enabled
stats_plugin = self.plugins.get("stats")
if stats_plugin:
stats_plugin.start_tracking()
if self.config["output"]["stream"]:
# Get stats from non-streaming request
response = completion(
model=self.config["model"]["name"],
messages=messages,
temperature=self.config["model"]["temperature"],
stream=False,
)
if stats_plugin:
stats_plugin.collect_stats(response)
# Stream the response
print("\n📊 Analysis Results:")
print("------------------")
for chunk in completion(
model=self.config["model"]["name"],
messages=messages,
temperature=self.config["model"]["temperature"],
stream=True,
):
if chunk and chunk.choices[0].delta.content:
print(chunk.choices[0].delta.content, end="", flush=True)
print() # New line after streaming
# Display stats if enabled
if stats_plugin:
stats_plugin.display_stats()
return response.choices[0].message.content
else:
# Non-streaming response
response = completion(
model=self.config["model"]["name"],
messages=messages,
temperature=self.config["model"]["temperature"],
)
print("\n📊 Analysis Results:")
print("------------------")
print(response.choices[0].message.content)
if stats_plugin:
stats_plugin.collect_stats(response)
stats_plugin.display_stats()
return response.choices[0].message.content
except openai.OpenAIError as e:
return f"OpenAI API Error: {str(e)}"
except Exception as e:
return f"Unexpected Error: {str(e)}"
finally:
# Cleanup plugins
for plugin in self.plugins.values():
plugin.cleanup()
```
