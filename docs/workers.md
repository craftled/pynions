---
title: "Workers"
publishedAt: "2024-11-10"
updatedAt: "2024-11-10"
summary: "Standalone task executors that combine multiple plugins for specific data extraction needs."
kind: "detailed"
---

## Overview
Workers are specialized task executors that combine multiple plugins to perform specific data extraction and analysis tasks. Unlike workflows that chain multiple steps together, workers are focused on single, well-defined tasks that require coordination between multiple plugins.

## Features
- 🎯 Task-specific implementations
- 🔄 Automated data extraction
- 📊 Structured output
- 🛠 Plugin integration
- ⚡ Efficient processing

## Available Workers

### PricingResearchWorker
Extracts structured pricing data from any SaaS website by combining:
1. **Serper Web Search**: Finds pricing pages
2. **Jina AI Reader**: Extracts clean content
3. **LiteLLM**: Analyzes and structures pricing data

#### Usage

```python
from pynions.workers import PricingResearchWorker
async def analyze_pricing():
worker = PricingResearchWorker()
result = await worker.execute({"domain": "example.com"})
print(json.dumps(result, indent=2))
```


#### Output Structure

```json
{
"domain": "example.com",
"source": "https://example.com/pricing",
"pricing": {
"plans": ["plan names"],
    "pricing": {
        "plan_name": {
            "monthly_price": 0.0,
            "annual_price": 0.0,
"features": ["feature list"],
"limits": {"limit_type": "limit value"}
}
    },
    "currency": "USD"
    }
}
```


## Creating Custom Workers

1. Inherit from base Worker class
```python
from pynions.core import Worker
class CustomWorker(Worker):
def init(self):
# Initialize required plugins
self.plugin1 = Plugin1()
self.plugin2 = Plugin2()
async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
# Implement your worker logic
pass


## Best Practices

1. **Plugin Integration**
   - Initialize plugins in constructor
   - Handle plugin errors gracefully
   - Validate plugin responses

2. **Data Processing**
   - Use structured input/output
   - Validate extracted data
   - Clean and normalize output

3. **Error Handling**
   - Handle network timeouts
   - Validate input parameters
   - Provide meaningful error messages

4. **Performance**
   - Minimize API calls
   - Process only required data
   - Use efficient data structures

## Common Issues
- API rate limits
- Content extraction failures
- Data validation errors
- Network timeouts

Need help? Check our [Debugging Guide](debugging.md) for solutions.