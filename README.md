# Pynions 🤖

A lean Python framework for marketers who code. Build tiny AI-powered automations for your marketing tasks without the bloat. Perfect for growth hackers and marketing engineers who want to ship fast and iterate quickly.

## TL;DR

Pynions is a lean Python framework for building AI-powered automation flows that run on your machine. Built for marketers who want to automate research, monitoring, and content tasks without cloud dependencies or complex setups. Perfect for personal and small team use.

## Key Features

- 🚀 Start small, ship fast
- 🔌 Easy API connections to your existing tools
- 🤖 AI-first but not AI-only
- 📦 Zero bloat, minimal dependencies
- 🛠 Built for real marketing workflows
- ⚡ Quick to prototype and iterate
- 🌐 Local-first, no cloud dependencies

## Quick Example

```python
from pynions import Workflow, AskLLM

# Create a simple content workflow
workflow = Workflow("Tweet Generator")

# Add AI tool
workflow.add(
    AskLLM(
        prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
        model="gpt-4o-mini"
    )
)

# Run workflow
result = await workflow.run({"topic": "AI tools for marketers"})
print(result["llm_response"])
```

## Why Marketers Love This

1. **Start Tiny, Grow Fast**

   - Build small, focused automations
   - No massive setups or configurations
   - Expand as needed

2. **Connect What You Already Use**

   - Works with your existing marketing stack
   - Simple API integrations
   - No vendor lock-in

3. **Ship & Iterate Quickly**

   - Build internal tools in minutes
   - Test new processes rapidly
   - Fail fast, learn faster

4. **Growth Mindset Built-in**
   - Perfect for A/B testing
   - Easy to measure and modify
   - Built for experimentation

## Getting Started (2-Minute Setup)

1. Install:

```bash
pip install pynions
```

2. Create your first pynion:

```python
from pynions import Workflow, AskLLM

# Create a simple content workflow
workflow = Workflow("Tweet Generator")

# Add AI tool
workflow.add(
    AskLLM(
        prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
        model="gpt-4o-mini"
    )
)

# Run workflow
result = await workflow.run({"topic": "AI tools for marketers"})
print(result["llm_response"])
```

3. Run it:

```bash
python -m pynions run quick_test.py
```

## Design Principles

1. **Small is Beautiful**

   - Tiny, focused automations
   - Minimal dependencies
   - Fast to build and modify

2. **Code > Configuration**

   - Simple Python scripts
   - No complex UIs
   - Full control

3. **Marketing First**
   - Built for marketing workflows
   - Easy API integrations
   - Growth-focused features

## Table of Contents

- [Pynions 🤖](#pynions-)
  - [TL;DR](#tldr)
  - [Key Features](#key-features)
  - [Quick Example](#quick-example)
  - [Why Marketers Love This](#why-marketers-love-this)
  - [Getting Started (2-Minute Setup)](#getting-started-2-minute-setup)
  - [Design Principles](#design-principles)
  - [Table of Contents](#table-of-contents)
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

1. **Local-First**

   - Runs on your machine
   - Your data stays with you
   - No cloud dependencies
   - Works offline
   - Easy to debug locally

2. **Simple > Complex**

   - Minimal boilerplate
   - Clear patterns
   - No magic
   - Single responsibility flows

3. **Practical > Perfect**

   - Focus on real use cases
   - Easy to modify
   - Fast to prototype
   - Quick iteration cycles

4. **Your Tools, Your Rules**
   - Connect to your existing APIs
   - Use your preferred AI models
   - Store data your way
   - Full control over execution

## Comparison with Alternatives

| Feature          | Pynions     | n8n/Zapier   | Custom Scripts | LangChain |
| ---------------- | ----------- | ------------ | -------------- | --------- |
| Setup Time       | Minutes     | Hours        | Variable       | Variable  |
| Flexibility      | Full Python | Limited      | Full           | Full      |
| AI Integration   | Built-in    | Limited      | Manual         | Yes       |
| Maintenance      | Simple      | Complex      | Variable       | Variable  |
| Cost             | Free        | Subscription | Free           | Free      |
| Learning Curve   | Low         | Medium       | High           | High      |
| Local Execution  | Yes         | No           | Yes            | Yes       |
| Caching          | Built-in    | Limited      | Manual         | Yes       |
| Rate Limiting    | Built-in    | Yes          | Manual         | Yes       |
| State Management | Built-in    | Limited      | Manual         | Yes       |

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

<a href="https://github.com/tomaslau/pynions/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=tomaslau/pynions" />
</a>

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=tomaslau/pynions&type=Date)](https://star-history.com/#tomaslau/pynions&Date)

---

Built with ☕️ by [Tomas Laurinavicius](https://github.com/tomaslau)
