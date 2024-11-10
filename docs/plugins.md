---
title: "Plugin Development"
publishedAt: "2024-10-30"
updatedAt: "2024-11-08"
summary: "Learn how to create custom plugins to extend Pynions with new capabilities and integrate additional tools into your marketing automation workflows."
kind: "detailed"
---

## Plugin System Overview

Pynions uses a simple plugin architecture where each plugin:

- Has a single responsibility
- Implements a common interface
- Is independently configurable
- Can be easily tested and maintained

## Basic Plugin Structure

```python
from pynions.core import Plugin
from typing import Any, Dict

class MyPlugin(Plugin):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)  # Automatically loads environment variables
        # Plugin-specific initialization

    async def execute(self, input_data: Any) -> Any:
        # Plugin logic here
        pass

    def validate_config(self) -> bool:
        # Configuration validation
        return True
```

Note: Environment variables are automatically loaded by the base Plugin class.

## Built-in Plugins

### 1. Serper Plugin (Google SERP Data)

```python
from pynions.plugins.serper import SerperWebSearch
serper = SerperWebSearch({
"max_results": 10 # Optional, defaults to 10
})
Execute search
result = await serper.execute({
"query": "your search query"
})
```

### 2. LiteLLM Plugin (AI Models)

```python
from pynions.plugins.litellm_plugin import LiteLLM

llm = LiteLLM({
    "api_key": "your_key_here",
    "model": "gpt-4"
})

response = await llm.execute({
    "prompt": "Summarize this article: ..."
})
```

### 3. Playwright Plugin (Web Scraping)

```python
from pynions.plugins.playwright_plugin import PlaywrightPlugin

browser = PlaywrightPlugin({
    "headless": True
})

content = await browser.execute({
    "url": "https://example.com"
})
```

### 4. Jina Plugin (Content Extraction)

```python
from pynions.plugins.jina import JinaAIReader

jina = JinaAIReader({
    "api_key": "your_key_here"
})

extracted = await jina.execute({
    "content": "Your content here"
})
```

### 5. Frase Plugin (NLP Content Analysis)

```python
from pynions.plugins.frase import Frase

frase = Frase({
"api_key": "your_key_here"
})

result = await frase.execute({
"serp_urls": ["url1", "url2"]
})
```

## Creating Custom Plugins

### 1. Create Plugin File

```bash
touch pynions/plugins/custom_plugin.py
```

### 2. Implement Plugin Class

```python
# custom_plugin.py
from pynions.core import Plugin
from typing import Any, Dict

class CustomPlugin(Plugin):
    """Custom plugin description"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.validate_config()

    async def execute(self, input_data: Any) -> Any:
        """Plugin logic here"""
        try:
            # Process input_data
            return result
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            raise

    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        required_keys = ['key1', 'key2']
        return all(key in self.config for key in required_keys)
```

### 3. Add Tests

```python
# tests/test_plugins/test_custom_plugin.py
import pytest
from pynions.plugins.custom_plugin import CustomPlugin

@pytest.mark.asyncio
async def test_custom_plugin():
    plugin = CustomPlugin({"key1": "value1", "key2": "value2"})
    result = await plugin.execute({"test": "data"})
    assert result is not None
```

## Plugin Best Practices

1. Single Responsibility

   - One main task per plugin
   - Clear input/output contract
   - Minimal dependencies

2. Error Handling

   - Use try/except blocks
   - Log errors appropriately
   - Raise meaningful exceptions

3. Configuration

   - Validate all config options
   - Provide sensible defaults
   - Document all settings

4. Testing

   - Unit tests for all methods
   - Integration tests with dependencies
   - Test error cases

5. Documentation
   - Clear docstrings
   - Usage examples
   - Configuration options

## Plugin Development Workflow

1. Plan Plugin

   - Define purpose
   - Specify input/output
   - List dependencies

2. Create Structure

   - Plugin class file
   - Test file
   - Example usage

3. Implement Features

   - Core functionality
   - Error handling
   - Configuration

4. Add Tests

   - Unit tests
   - Integration tests
   - Edge cases

5. Document
   - Code comments
   - Usage examples
   - Configuration guide

## Example: Complete Plugin

```python
# weather_plugin.py
from pynions.core import Plugin
from typing import Any, Dict
import aiohttp

class WeatherPlugin(Plugin):
    """Plugin for fetching weather data"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.base_url = "https://api.weather.com/v1"

    async def execute(self, input_data: Any) -> Any:
        """Fetch weather for location"""
        location = input_data.get('location')
        if not location:
            raise ValueError("Location required")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/weather",
                params={
                    "location": location,
                    "apikey": self.api_key
                }
            ) as response:
                return await response.json()

    def validate_config(self) -> bool:
        """Validate required configuration"""
        return bool(self.api_key)
```
