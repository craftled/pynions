---
title: "Configuration"
publishedAt: "2024-10-30"
updatedAt: "2024-11-03"
summary: "Learn how to configure Pynions with API keys and settings to power your local marketing automation workflows."
kind: "detailed"
---

## Overview

Pynions uses two types of configuration:
1. `.env` for sensitive data (API keys)
2. `config.json` for application settings

## Environment Variables (.env)

### Setup
```bash
cp .env.example .env
```

### Required Variables
```bash
# Search API
SERPER_API_KEY=your_serper_key_here

# AI Models
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Content Processing
JINA_API_KEY=your_jina_key_here

# Optional Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Getting API Keys

1. Serper.dev API Key:
   - Visit https://serper.dev
   - Sign up for an account
   - Navigate to Dashboard → API Keys
   - Copy your key

2. OpenAI API Key:
   - Visit https://platform.openai.com
   - Sign up/Login
   - Go to API section
   - Create new key

3. Anthropic API Key:
   - Visit https://console.anthropic.com
   - Create account
   - Navigate to API section
   - Generate key

4. Jina AI Key:
   - Visit https://jina.ai
   - Create account
   - Go to API section
   - Generate key

## Application Configuration (config.json)

### Setup
```bash
cp config.example.json config.json
```

### Configuration Structure
```json
{
  "plugins": {
    "serper": {
      "max_results": 10,
      "country": "us",
      "language": "en"
    },
    "litellm": {
      "default_model": "gpt-4",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "jina": {
      "chunk_size": 1000,
      "overlap": 200
    }
  },
  "storage": {
    "data_dir": "data",
    "max_file_size_mb": 100
  },
  "logging": {
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S"
  }
}
```

### Plugin Configuration Options

#### Serper Plugin
```json
{
  "max_results": 10,    // Number of results to fetch
  "country": "us",      // Target country
  "language": "en",     // Result language
  "auto_retry": true,   // Retry failed requests
  "timeout": 30         // Request timeout in seconds
}
```

#### LiteLLM Plugin
```json
{
  "default_model": "gpt-4",    // Default AI model
  "temperature": 0.7,          // Response creativity (0-1)
  "max_tokens": 2000,          // Maximum response length
  "fallback_model": "gpt-3.5-turbo" // Fallback model
}
```

#### Jina Plugin
```json
{
  "chunk_size": 1000,   // Text chunk size
  "overlap": 200,       // Overlap between chunks
  "batch_size": 10      // Processing batch size
}
```

## Environment-Specific Configuration

### Development
```bash
# .env.development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Production
```bash
# .env.production
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Validation

Run configuration validation:
```bash
python -m pynions.utils.validate_config
```

## Security Best Practices

1. Never commit .env files
2. Rotate API keys regularly
3. Use different keys for dev/prod
4. Limit API key permissions
5. Monitor API usage

## Troubleshooting

### Common Issues

1. Missing API Keys:
```bash
# Check if keys are loaded
python -c "import os; print(os.getenv('SERPER_API_KEY'))"
```

2. Invalid JSON:
```bash
# Validate config.json
python -m json.tool config.json
```

3. Permission Issues:
```bash
# Fix file permissions
chmod 600 .env
chmod 644 config.json
```
