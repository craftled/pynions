---
title: "Serper Web Search"
publishedAt: "2024-11-03"
updatedAt: "2024-11-03"
summary: "Extract search engine results and analytics using Serper.dev's powerful SERP API."
kind: "simple"
---

## Overview

The Serper Web Search plugin helps marketers extract detailed search engine results using Serper.dev's API. It provides rich SERP data including organic results, "People Also Ask" questions, and related searches.

## What It Does
- 🔍 Fetches comprehensive SERP data
- 📊 Extracts organic search results
- ❓ Captures "People Also Ask" questions
- 🔗 Includes related searches
- 📅 Shows publication dates when available
- 🌐 Provides detailed sitelinks

## Quick Start

1. Add your API key to `.env`:

```bash
SERPER_API_KEY=your_key_here
```

2. Use in your code:

```python
from pynions.plugins.serper import SerperWebSearch

# Create searcher
searcher = SerperWebSearch()
Execute search
result = await searcher.execute({
"query": "your search query here"
})
Use the search results
print(result["organic"]) # Organic results
print(result["peopleAlsoAsk"]) # Related questions
print(result["relatedSearches"]) # Related searches
```

## Quick Test

Test any search query using the built-in test function:

```python
import asyncio
from pynions.plugins.serper import test_search
# Test with your query
asyncio.run(test_search("best marketing automation tools 2024"))
```

## Use Cases for Marketers

### 1. SERP Analysis
- Track keyword rankings
- Monitor competitor positions
- Analyze SERP features

### 2. Content Research
- Find content gaps
- Discover related topics
- Understand user intent

### 3. Competitive Intelligence
- Track competitor content
- Monitor industry trends
- Identify new competitors

## Output Format
The plugin returns a dictionary with:
- `searchParameters`: Query details
- `organic`: List of organic search results
- `peopleAlsoAsk`: Related questions and answers
- `relatedSearches`: Related search queries
- `credits`: API credits used

## Common Issues

### API Key Issues
- Check if `SERPER_API_KEY` is in your `.env` file
- Verify key is valid
- Monitor API credit usage

### Rate Limiting
- Respect API rate limits
- Handle API timeout errors
- Monitor credit consumption

## Best Practices

1. **Query Optimization**
   - Use specific search terms
   - Include relevant parameters
   - Consider search intent

2. **Error Handling**
   - Check for empty results
   - Handle API errors gracefully
   - Log failed requests

3. **Data Processing**
   - Store results for analysis
   - Track changes over time
   - Export data for reporting

## Next Steps
1. [Get your Serper API key](https://serper.dev)
2. Try the quick test above
3. Integrate into your workflows
4. Start analyzing search results!

Need more help? Check the [Debugging Guide](../debugging.md) for detailed solutions.
