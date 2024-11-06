---
title: "Content Analysis Workflow"
publishedAt: "2024-11-07"
updatedAt: "2024-11-07"
summary: "End-to-end workflow for analyzing content and generating detailed research-backed briefs."
---

## Overview
The Content Analysis workflow combines three powerful plugins to create comprehensive content briefs with research citations:

1. **Serper Web Search**: Finds top-ranking content and SERP data
2. **Jina AI Reader**: Extracts clean content from discovered URLs
3. **LiteLLM**: Analyzes content and generates structured outlines

## Features
- 🔍 SERP analysis and competitor research
- 📄 Clean content extraction from web pages
- 🤖 AI-powered content analysis
- 📝 Research-backed content briefs
- 🔗 Automatic citation linking

## Usage

```python
import asyncio
from workflows.content_analysis_workflow import content_analysis_workflow
# Run the workflow
asyncio.run(content_analysis_workflow("your keyword here"))
```

## Output
The workflow generates a structured markdown brief including:

1. **Research Summary**
   - Top-ranking content analysis
   - Content length statistics
   - Source citations

2. **Content Outline**
   - Topic structure
   - Key points to cover
   - Competitor insights

3. **Research Data**
   - SERP metrics
   - Content patterns
   - Audience insights

## Best Practices
1. Use specific, focused keywords
2. Review and validate generated briefs
3. Monitor API usage across plugins
4. Store briefs in version control

## Common Issues
- API rate limits
- Content extraction blocks
- Token usage optimization

Need help? Check our [Debugging Guide](../debugging.md) for solutions.