---
title: "Jina AI Reader"
publishedAt: "2024-11-01"
updatedAt: "2024-11-03"
summary: "Extract clean, readable content from any webpage using Jina AI's content extraction capabilities."
kind: "simple"
---

## Overview
The Jina AI Reader plugin helps marketers extract clean, readable content from any webpage. Think of it as your personal content assistant that removes all the clutter and gives you just the important parts.

## What It Does
- 📄 Extracts main content from web pages
- 📋 Pulls out titles and descriptions
- 🧹 Removes ads and navigation elements
- 📱 Works with any public webpage

## Quick Start

1. Add your API key to `.env`:
```bash
JINA_API_KEY=your_key_here
```

2. Use in your code:
```python
from pynions.plugins.jina import JinaAIReader

# Create reader
reader = JinaAIReader()

# Extract content
result = await reader.execute({
    "url": "https://example.com/blog-post"
})

# Use the extracted content
print(result["title"])       # Page title
print(result["description"]) # Page description
print(result["content"])     # Main content
```

## Quick Test
Test any URL quickly using the built-in test function:
```python
import asyncio
from pynions.plugins.jina import test_reader

# Test with your URL
asyncio.run(test_reader("https://yoursite.com"))
```

## Use Cases for Marketers

### 1. Content Research
- Extract competitor blog posts
- Research industry trends
- Gather market insights

### 2. Content Monitoring
- Track competitor content updates
- Monitor industry news
- Keep up with market changes

### 3. Content Creation
- Research topics thoroughly
- Create content briefs
- Analyze successful content

## Output Format
The plugin returns a dictionary with:
- `title`: Page title
- `description`: Meta description or summary
- `url`: Original URL
- `content`: Main content text

## Common Issues

### API Key Issues
- Check if `JINA_API_KEY` is in your `.env` file
- Verify key is valid
- Ensure key has proper permissions

### Content Issues
- Some sites block content extraction
- Dynamic content might not be captured
- Paywalled content may be inaccessible

## Best Practices

1. **Rate Limiting**
   - Don't overload with too many requests
   - Add delays between bulk extractions
   - Consider caching results

2. **Error Handling**
   - Always check if result is None
   - Handle network timeouts
   - Log extraction failures

3. **Content Processing**
   - Validate extracted content
   - Clean up any remaining HTML
   - Store results for later use

## Next Steps
1. [Get your Jina AI API key](https://jina.ai)
2. Try the quick test above
3. Integrate into your workflows
4. Start automating your content research!

Need more help? Check the [Debugging Guide](../06-debugging.md) for detailed solutions.
