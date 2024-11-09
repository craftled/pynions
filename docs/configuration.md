---
title: "Configuration"
publishedAt: "2024-10-30"
updatedAt: "2024-11-09"
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
  "model": {
    "name": "gpt-4",
    "temperature": 0.7
  },
  "plugins": {
    "serper": {
      "max_results": 10
    }
  },
  "storage": {
    "data_dir": "data",
    "raw_dir": "data/raw",
    "output_dir": "data/output"
  }
}
```

### Environment Variables (.env)

Sensitive configuration in `pynions/config/.env`:

```bash
# Search API
SERPER_API_KEY=your_serper_key_here

# AI Models
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Content Processing
JINA_API_KEY=your_jina_key_here
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
