---
title: "Configuration"
publishedAt: "2024-10-30"
updatedAt: "2024-11-10"
summary: "Simple configuration guide for marketers using Pynions"
kind: "detailed"
---

## Quick Setup

1. Copy `.env.example` to `.env` and add your API key:
```bash
cp .env.example .env
nano .env  # Add your OpenAI API key
```

2. (Optional) Create `pynions.json` if you need custom settings:
```bash
cp pynions.example.json pynions.json
```

That's it! You're ready to start using Pynions.

## Configuration Files

### 1. API Keys (.env)

Put your API keys in `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_key_here

# Optional (only if you use these features)
SERPER_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

### 2. Optional Settings (pynions.json)

If you need to customize settings, create `pynions.json` in the root directory:

```json
{
    "save_results": true,        // Save generated content to files
    "output_folder": "data",     // Where to save files
    "plugins": {
        "serper": {
            "results": 10,       // Number of search results
            "country": "us"      // Search region
        }
    }
}
```

All settings are optional and have sensible defaults.

## Using in Scripts

Access configuration in your scripts:

```python
from pynions.core.config import config

# Check API key
if not config.check_api_key():
    print("Add your OpenAI API key to .env file")
    exit()

# Get settings (with defaults)
output_dir = config.get("output_folder", "data")
save_to_file = config.get("save_results", True)
```

## AI Configuration

Pynions uses [LiteLLM](https://docs.litellm.ai/docs/) for AI features. You don't need to configure AI settings - they're handled automatically.

Example usage:
```python
from litellm import completion

response = completion(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

See [LiteLLM documentation](https://docs.litellm.ai/docs/) for more options.
