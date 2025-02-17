---
title: "Perplexity Plugin"
publishedAt: "2025-02-17"
updatedAt: "2025-02-17"
summary: "Advanced AI research and data extraction using Perplexity AI's API."
kind: "detailed"
---

## Overview

The Perplexity plugin provides advanced research and data extraction capabilities using Perplexity AI's API. It excels at:
- Real-time web research
- Source validation and citation
- Structured data extraction
- Cross-reference verification

## Configuration

### API Key Setup

1. Get your API key from [Perplexity AI](https://perplexity.ai)
2. Add to your `.env` file:
```bash
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxx
```

### Plugin Options

```python
from pynions.plugins.perplexity import PerplexityAPI

perplexity = PerplexityAPI({
    "model": "sonar-reasoning-pro",  # Default model
    "temperature": 0.2,              # Lower for more focused responses
    "max_tokens": 2000,              # Adjust based on needs
    "return_related_questions": False # Optional feature
})
```

Available options:
- `model`: Model to use (default: "sonar-reasoning-pro")
- `temperature`: Response randomness (0.0-1.0)
- `max_tokens`: Maximum response length
- `return_related_questions`: Include related queries
- `search_domain_filter`: Limit search to specific domains
- `return_images`: Include image results
- `top_k`: Number of search results to consider
- `stream`: Enable streaming responses
- `presence_penalty`: Control response repetition
- `frequency_penalty`: Control word frequency

## Usage Examples

### Basic Research Query

```python
response = await perplexity.execute({
    "messages": [
        {
            "role": "system",
            "content": "You are a research assistant. Provide factual information."
        },
        {
            "role": "user",
            "content": "What are the latest developments in AI regulation?"
        }
    ]
})

print(f"Found {len(response['citations'])} sources")
print(response['choices'][0]['message']['content'])
```

### Structured Data Extraction

```python
response = await perplexity.execute({
    "messages": [
        {
            "role": "system",
            "content": """Extract data in JSON format:
            {
                "key": "value",
                "array": ["items"],
                "nested": {"data": "here"}
            }"""
        },
        {
            "role": "user",
            "content": "Extract key information about cloud providers"
        }
    ]
})
```

### Source Validation

```python
response = await perplexity.execute({
    "messages": [
        {
            "role": "system",
            "content": "Find and validate official sources only."
        },
        {
            "role": "user",
            "content": "What is Company X's pricing structure?"
        }
    ]
})

# Check sources
for citation in response['citations']:
    print(f"Source: {citation}")
```

## Response Structure

```python
{
    "choices": [{
        "message": {
            "role": "assistant",
            "content": "Generated response"
        }
    }],
    "citations": [
        "source_url_1",
        "source_url_2"
    ],
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579
    }
}
```

## Best Practices

1. **Temperature Control**
   - Use low temperature (0.1-0.3) for factual research
   - Use higher temperature (0.7-0.9) for creative tasks

2. **Token Management**
   - Start with lower max_tokens (1000-2000)
   - Increase if responses are truncated
   - Monitor token usage for cost control

3. **Source Validation**
   - Always check citations array
   - Verify source authenticity
   - Cross-reference important data

4. **Error Handling**
   - Handle API timeouts (default: 3 minutes)
   - Validate response structure
   - Check for rate limits

## Common Issues

1. **API Key Issues**
   - Ensure key starts with "pplx-"
   - Check environment variable loading
   - Verify API key permissions

2. **Response Timeouts**
   - Default timeout is 180 seconds
   - Complex queries may need retries
   - Consider breaking into smaller queries

3. **Data Validation**
   - Always validate structured output
   - Check for missing required fields
   - Verify data types match expectations

## Testing

The plugin includes comprehensive tests:
- Direct question answering
- Web research capabilities
- Structured data output
- Custom configurations

Run tests with:
```bash
pytest pynions/tests/test_perplexity.py -v
``` 