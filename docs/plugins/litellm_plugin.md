---
title: "LiteLLM"
publishedAt: "2024-11-07"
updatedAt: "2024-11-07"
summary: "Universal interface for accessing 100+ LLMs through a single, consistent API."
kind: "simple"
---

## Overview
The LiteLLM plugin provides a unified interface to work with multiple Language Models (LLMs) through a single API. It supports 100+ LLMs while maintaining OpenAI-compatible input/output formats.

## What It Does
- 🤖 Universal access to 100+ LLMs
- 🔄 Consistent input/output formatting
- 📊 Token usage tracking and analytics
- ⚡ Automatic retries and error handling
- 💰 Cost monitoring across providers

## Quick Start

1. Add your API key to `.env`:```bash
OPENAI_API_KEY=your_key_here
# Add other provider keys as needed
```

2. Use in your code:
```python
from pynions.plugins.litellm_plugin import LiteLLM
Initialize LLM with any supported model
llm = LiteLLM({
"model": "gpt-4", # or any other supported model
"temperature": 0.7,
"max_tokens": 2000
})
Make calls with OpenAI-compatible format
result = await llm.execute({
"messages": [{
"role": "user",
"content": "Your prompt here"
}]
})
print(result["content"]) # Model response
```

## Output Format
The plugin returns a dictionary with:
- `content`: Model's response text
- `usage`: Token usage statistics
- `model`: Model used for generation
- `response_ms`: Response time in milliseconds

## Common Issues
- API key configuration
- Rate limits and quotas
- Token context length
- Model availability

## Best Practices
1. Choose appropriate models for your use case
2. Implement proper error handling
3. Monitor usage and costs
4. Cache responses when possible
5. Set reasonable timeouts

Need more help? Check the [Debugging Guide](../debugging.md) for solutions.
