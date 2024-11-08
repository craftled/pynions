# Frase Plugin

Extract and analyze content from URLs using the Frase.io API.

## Quick Test

Test content analysis with sample URLs:
```python
import asyncio
from pynions.plugins.frase import test_frase

# Test with sample URLs
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
asyncio.run(test_frase(urls))
```


## Use Cases for Marketers

### 1. Content Analysis
- Analyze competitor content structure
- Extract key entities and topics
- Identify content patterns

### 2. Research & Planning
- Generate content briefs
- Identify content gaps
- Research industry terminology

### 3. SEO Optimization
- Extract content metrics
- Analyze content length patterns
- Identify key entities and topics

## Output Format
The plugin returns a dictionary with:
- `items`: List of processed URLs with details
  - `title`: Page title
  - `url`: Original URL
  - `word_count`: Content length
  - `entities`: Extracted key terms and phrases
  - `questions`: Identified questions in content
- `aggregate_metrics`: Overall statistics
  - `avg_headers`: Average headers per page
  - `avg_word_count`: Average content length
  - `avg_external_links`: Average outbound links

## Common Issues

### API Key Issues
- Check if `FRASE_API_KEY` is in your `.env` file
- Verify key is valid and active
- Ensure proper API permissions

### Content Issues
- Some URLs may be blocked
- Rate limits may apply
- Large batches may timeout

## Best Practices

1. **URL Processing**
   - Process URLs in small batches
   - Add delays between large requests
   - Cache results when possible

2. **Error Handling**
   - Always check response status
   - Handle timeouts gracefully
   - Log processing failures

3. **Content Analysis**
   - Validate extracted metrics
   - Review entity extraction
   - Store processed results

## Next Steps
1. [Get your Frase API key](https://frase.io)
2. Try the quick test above
3. Integrate into your workflows
4. Start analyzing content at scale!

Need help? Check the [Debugging Guide](../debugging.md) for detailed solutions.
