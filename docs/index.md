# Pynions Documentation

Fast, simple AI automation framework for Python developers.

## Install

```bash
pip install pynions
```

## Quick Example

```python
from pynions import Flow

class MyFlow(Flow):
    async def run(self):
        result = await self.call_api(
            "example",
            self.fetch_data,
            use_cache=True
        )
        return result
```

## Features

- 🚀 Minimal setup required
- 🔧 Built-in caching and rate limiting
- 🤖 Easy API integration
- 📊 Simple logging and monitoring

## Next Steps

- [Quick Start](quickstart.md)
- [API Reference](api.md)
- [Examples](https://github.com/yourusername/pynions/tree/main/examples)
