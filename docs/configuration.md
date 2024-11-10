---
title: "Configuration"
publishedAt: "2024-10-30"
updatedAt: "2024-11-10"
summary: "Learn how to configure Pynions with API keys and settings."
kind: "detailed"
---

## Configuration Structure

Pynions uses a two-part configuration system:

1. `pynions/config/settings.json` - Main application settings
2. `pynions/config/.env` - Environment variables and API keys

### Settings (settings.json)

Main configuration file located at `pynions/config/settings.json`:

```json
{
  "workflow": {
    "status_types": {
      "research": {
        "description": "Initial research and data gathering",
        "extensions": ["md", "txt"]
      },
      "brief": {
        "description": "Content brief or outline",
        "extensions": ["md"]
      },
      "draft": {
        "description": "First version of content",
        "extensions": ["md"]
      }
    }
  },
  "storage": {
    "data_dir": "data",
    "raw_dir": "data/raw",
    "output_dir": "data/output"
  },
  "plugins": {
    "serper": {
      "max_results": 10
    }
  }
}
```

### Environment Variables (.env)

Sensitive configuration like API keys are stored in `pynions/config/.env`:

```bash
# Search API
SERPER_API_KEY=your_serper_key_here

# AI Models
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Content Processing
JINA_API_KEY=your_jina_key_here
FRASE_API_KEY=your_actual_frase_key
```

## Setup Steps

1. Create config directory:

```bash
mkdir -p pynions/config
```

2. Copy example settings:

```bash
cp settings.example.json pynions/config/settings.json
```

3. Create environment file:

```bash
cp .env.example pynions/config/.env
```

4. Edit your settings and API keys:

```bash
# Edit settings
nano pynions/config/settings.json

# Add your API keys
nano pynions/config/.env
```

## Configuration Access

Access settings in your code:

```python
from pynions.config import load_config

# Load full config
config = load_config()

# Access settings
model_name = config["model"]["name"]
max_results = config["plugins"]["serper"]["max_results"]
```

*Note:* Environment variables are automatically loaded by the Plugin system. You don't need to manually load them in your code when using plugins.
