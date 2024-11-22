---
title: "Project Structure"
publishedAt: "2024-10-30"
updatedAt: "2024-11-09"
summary: "Simple guide to Pynions project organization"
kind: "detailed"
---

## Project Structure

```
my-pynions/                      # Your project folder
├── .env                         # API keys
├── pynions.json                 # Optional settings
├── data/                        # Generated content
│   └── content_ideas.txt
│
├── workflows/                   # Your marketing workflows
│   ├── blog_ideas.py
│   ├── social_posts.py
│   └── seo_research.py
│
└── README.md                    # Project documentation
```

## Key Files

### 1. Configuration Files

#### `.env` - API Keys
```bash
# Required
OPENAI_API_KEY=your-key-here

# Optional (for specific features)
SERPER_API_KEY=your-key-here
```

#### `pynions.json` - Optional Settings
```json
{
    "save_results": true,
    "output_folder": "data"
}
```

### 2. Your Workflows

Create Python workflows for your marketing tasks:

#### `workflows/blog_ideas.py`
```python
from litellm import completion
from pynions.core.config import config

def generate_blog_ideas():
    """Marketing workflow for blog ideation"""
    # Your blog idea generation workflow
    pass

if __name__ == "__main__":
    generate_blog_ideas()
```

### 3. Generated Content

Content is saved to the `data` folder by default:
- `data/content_ideas.txt`
- `data/blog_posts/`
- `data/social_media/`

## Core Components

Pynions handles these for you:

1. **Configuration** (`pynions.core.config`)
   - API key management
   - Settings handling
   - File saving

2. **AI Integration** (`litellm`)
   - Multiple AI models
   - Smart defaults
   - Error handling

3. **Plugins** (`pynions.plugins`)
   - Search (Serper)
   - Content Analysis
   - SEO Tools

## Best Practices

1. **Organization**
   - Keep workflows in `workflows/` folder
   - Use descriptive filenames
   - Group related content

2. **Configuration**
   - Keep API keys in `.env`
   - Use `pynions.json` for custom settings
   - Let Pynions handle the rest

3. **Content**
   - Save generated content to `data/`
   - Use subfolders for organization
   - Add dates to filenames

## Example Project

Here's a complete marketing automation project:

```
my-pynions/
├── .env                         # API keys
├── pynions.json                 # Custom settings
│
├── workflows/
│   ├── blog_ideas.py           # Blog ideation workflow
│   ├── social_calendar.py      # Social planning workflow
│   └── seo_keywords.py         # SEO research workflow
│
├── data/
│   ├── blog/                   # Blog content
│   ├── social/                 # Social posts
│   └── seo/                    # SEO data
│
└── README.md                   # Documentation
```

Need more examples? Check our [example workflows](https://docs.pynions.dev/examples) or join our [Discord](https://discord.gg/pynions)!
