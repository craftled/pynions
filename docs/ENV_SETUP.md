---
title: "Environment Setup"
publishedAt: "2024-10-30"
updatedAt: "2024-11-10"
summary: "ENV setup guide for Pynions."
kind: "detailed"
---

## Setting Up Environment Variables

1. Create your .env file by copying the example:

```bash
cp .env.example .env
```

2. Edit your .env file with your actual API keys:

```bash
nano .env  # or use your preferred editor
```

3. Add your API keys:

```
SERPER_API_KEY=your_actual_serper_key
OPENAI_API_KEY=your_actual_openai_key
ANTHROPIC_API_KEY=your_actual_anthropic_key
JINA_API_KEY=your_actual_jina_key
FRASE_API_KEY=your_actual_frase_key
```

## Configuration Files

The project now uses two types of configuration:

1. `.env` file for sensitive data:

   - API keys
   - Credentials
   - Environment-specific settings

2. `settings.json` for non-sensitive settings:
   - Plugin configurations
   - Default values
   - Feature flags
   - Logging preferences

## Security Best Practices

1. Never commit .env file:

```bash
# Verify .env is in .gitignore
cat .gitignore | grep .env
```

2. Keep `settings.json` updated:
   - Add new variables as needed
   - Remove unused variables
   - Don't include actual API keys

## Troubleshooting

If your API calls aren't working:

1. Check if .env file exists:

```bash
ls -la .env
```

2. Verify environment variables are loaded:

```python
import os
print(os.getenv('SERPER_API_KEY'))  # Should print your key
```

3. Common issues:
   - .env file not copied from .env.example
   - .env file in wrong directory (should be in `pynions/config/`)
   - Invalid API key format
   - Missing required variables

## Loading Order

The configuration system loads in this order:

1. System environment variables
2. .env file variables
3. settings.json settings

Later values override earlier ones.

## Automatic Loading

Environment variables are automatically loaded by the base Plugin class. You don't need to manually load them in your plugins or workflows. Just ensure your `.env` file is in the correct location:

```bash
pynions/config/.env
```
