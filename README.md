# Pynions 🤖

[![PyPI version](https://badge.fury.io/py/pynions.svg)](https://badge.fury.io/py/pynions)
[![CI](https://github.com/yourusername/pynions/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/pynions/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/pynions.svg)](https://pypi.org/project/pynions/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/pynions/badge/?version=latest)](https://pynions.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://pepy.tech/badge/pynions)](https://pepy.tech/project/pynions)
[![Last Commit](https://img.shields.io/github/last-commit/yourusername/pynions)](https://github.com/yourusername/pynions/commits/main)

Fast, simple AI automation framework for personal and small team use. Think "personal Zapier/n8n" but with AI capabilities and full coding flexibility.

## Table of Contents

- [Pynions 🤖](#pynions-)
  - [Table of Contents](#table-of-contents)
  - [TL;DR](#tldr)
  - [Key Features](#key-features)
  - [Quick Example](#quick-example)
  - [Installation](#installation)
  - [Core Concepts](#core-concepts)
    - [1. Flows](#1-flows)
    - [2. API Integration](#2-api-integration)
    - [3. State Management](#3-state-management)
    - [4. Steps Tracking](#4-steps-tracking)
  - [Real-World Use Cases](#real-world-use-cases)
  - [Setup](#setup)
  - [Development](#development)
  - [Why Use This?](#why-use-this)
  - [Design Philosophy](#design-philosophy)
  - [Comparison with Alternatives](#comparison-with-alternatives)
  - [Example Projects](#example-projects)
  - [Getting Started](#getting-started)
  - [Contributing](#contributing)
    - [Development Setup](#development-setup)
  - [Need Help?](#need-help)
  - [License](#license)
  - [Contributors](#contributors)
  - [Star History](#star-history)

## TL;DR

Pynions is a lean Python framework for building AI-powered automation flows. Built for developers who want to automate research, monitoring, and content tasks without the overhead of complex frameworks.

## Key Features

- ⚡ Async-first design
- 🔄 Built-in caching and rate limiting
- 💾 Simple state management
- 🤖 Easy AI integration
- 📁 File-based storage
- 📦 Minimal dependencies

## Quick Example

```python
from pynions import Flow, State
from typing import Dict, Any

class ResearchState(State):
    query: str
    results: Dict[str, Any] = {}

class ResearchFlow(Flow[ResearchState]):
    async def run(self):
        # Built-in caching and rate limiting
        results = await self.call_api(
            "search",
            self.search_api,
            self.state.query,
            use_cache=True
        )

        self.state.results = results
        return results

# Usage
flow = ResearchFlow(query="python async frameworks")
results = await flow.run()
```

## Installation

```bash
# Using pip
pip install pynions

# Using uv (recommended)
uv pip install pynions

# Development installation
pip install "pynions[dev]"
```

## Core Concepts

### 1. Flows

- Each automation is a Flow
- Flows have state management
- Built-in logging and error handling
- Automatic caching
- Progress tracking

### 2. API Integration

```python
# Automatic caching and rate limiting
await self.call_api(
    key="unique_key",
    func=your_api_call,
    use_cache=True,
    cache_ttl=3600  # 1 hour
)
```

### 3. State Management

```python
class YourState(State):
    input_data: str
    processed: bool = False
    results: Dict[str, Any] = {}
```

### 4. Steps Tracking

```python
async def run(self):
    async with self.step("fetch"):
        # Step 1 logic
        pass

    async with self.step("process"):
        # Step 2 logic
        pass
```

## Real-World Use Cases

1. **Content Research**

```python
class ContentFlow(Flow[ContentState]):
    async def run(self):
        # Search competitors
        results = await self.call_api("search", self.search)

        # Analyze content
        analysis = await self.call_api("analyze", self.analyze)

        # Generate content
        content = await self.call_api("generate", self.generate)

        return content
```

2. **Price Monitoring**

```python
class PriceMonitor(Flow[PriceState]):
    async def run(self):
        current = await self.scrape_prices()
        changes = self.compare_with_previous(current)
        self.save_prices(current)

        if changes:
            await self.notify(changes)
```

## Setup

```bash
# Install
pip install pynions

# Create project
pynions init myproject
cd myproject

# Project structure
myproject/
├── flows/          # Your flows
├── data/           # Local storage
├── logs/           # Flow logs
└── .cache/        # API cache
```

## Development

```bash
# Clone
git clone https://github.com/yourusername/pynions.git
cd pynions

# Install dev version
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy src/pynions
```

## Why Use This?

1. **Simplicity**: No complex configurations or dependencies

2. **Developer Freedom**: Full Python power, no restrictions

3. **Performance**:

   - Async by default
   - Built-in caching
   - Minimal overhead

4. **Maintainability**:
   - Clear structure
   - Type hints
   - Automated testing
   - Good logging

## Design Philosophy

1. **Simple > Complex**

   - Minimal boilerplate
   - Clear patterns
   - No magic

2. **Practical > Perfect**

   - Focus on real use cases
   - Easy to modify
   - Fast to prototype

3. **Local > Cloud**
   - File-based storage
   - No external dependencies
   - Easy to debug

## Comparison with Alternatives

| Feature          | Pynions     | n8n/Zapier   | Custom Scripts |
| ---------------- | ----------- | ------------ | -------------- |
| Setup Time       | Minutes     | Hours        | Variable       |
| Flexibility      | Full Python | Limited      | Full           |
| AI Integration   | Built-in    | Limited      | Manual         |
| Maintenance      | Simple      | Complex      | Variable       |
| Cost             | Free        | Subscription | Free           |
| Learning Curve   | Low         | Medium       | High           |
| Local Execution  | Yes         | No           | Yes            |
| Caching          | Built-in    | Limited      | Manual         |
| Rate Limiting    | Built-in    | Yes          | Manual         |
| State Management | Built-in    | Limited      | Manual         |

## Example Projects

1. **Content Research Bot**

```python
from pynions import Flow

class ResearchBot(Flow):
    async def run(self):
        competitors = await self.search_competitors()
        analysis = await self.analyze_content(competitors)
        outline = await self.generate_outline(analysis)
        article = await self.write_article(outline)
        return article
```

2. **Market Monitor**

```python
from pynions import Flow

class MarketMonitor(Flow):
    async def run(self):
        # Monitor multiple sources
        await self.track_prices()
        await self.track_features()
        await self.track_sentiment()

        # Generate report
        return await self.generate_report()
```

## Getting Started

1. Install:

```bash
pip install pynions
```

2. Create project:

```bash
pynions init myproject
cd myproject
```

3. Create flow:

```python
# flows/my_flow.py
from pynions import Flow

class MyFlow(Flow):
    async def run(self):
        # Your automation logic here
        pass
```

4. Run flow:

```bash
pynions run flows/my_flow.py:MyFlow
```

## Contributing

We welcome contributions! Here's how you can help:

1. **Bug Reports**: Open an issue describing the bug
2. **Feature Requests**: Open an issue describing the feature
3. **Pull Requests**: Fork, create branch, submit PR
4. **Documentation**: Help improve or fix documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/pynions.git
cd pynions

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
isort .
```

## Need Help?

1. 📖 Check examples in `examples/`
2. 💻 Run `pynions --help`
3. 🐛 Check [GitHub issues](https://github.com/yourusername/pynions/issues)
4. 📚 Read the [documentation](https://pynions.readthedocs.io)
5. 🔍 Read the source (it's simple!)

## License

MIT License - see [LICENSE](LICENSE)

## Contributors

<a href="https://github.com/yourusername/pynions/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/pynions" />
</a>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/pynions&type=Date)](https://star-history.com/#yourusername/pynions&Date)

---

Built with ❤️ by [Your Name](https://github.com/yourusername)
