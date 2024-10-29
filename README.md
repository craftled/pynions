# Pynions 🤖

A lean Python framework for marketers who code. Build tiny AI-powered automations for your marketing tasks without the bloat. Perfect for growth hackers and marketing engineers who want to ship fast and iterate quickly.

## TL;DR

Pynions is a lean Python framework for building AI-powered automation workflows that run on your machine. Built for marketers who want to automate research, monitoring, and content tasks without cloud dependencies or complex setups. Perfect for personal and small team use.

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


async def main():
    """Example workflow that generates a tweet"""
    workflow = Workflow("Tweet Generator")

    workflow.add(
        AskLLM(
            prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
            model="gpt-4o-mini",
        )
    )

    result = await workflow.run({"topic": "AI automation"})
    print(f"\nGenerated tweet: {result['llm_response']}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

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

## Getting Started (5-Minute Setup)

### Prerequisites

1. **Development Environment**

   - Install [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/)
   - Install [Python 3.9+](https://www.python.org/downloads/)
     - Or terminal version (macOS/Linux)
       - `brew install python`

2. **Environment Setup**

   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Pynions**

   ```bash
   pip install pynions
   ```

4. **Configure Environment Variables**
   Create a `.env` file in your project:

   ```bash
   OPENAI_API_KEY=your_openai_key_here
   ```

5. **Create Your First Workflow**

   ```python
   from pynions import Workflow, AskLLM

   async def main():
       workflow = Workflow("Tweet Generator")

       workflow.add(
           AskLLM(
               prompt="Write a tweet about {topic}. Make it engaging and include relevant hashtags.",
               model="gpt-4o-mini"
           )
       )

       result = await workflow.run({"topic": "AI tools for marketers"})
       print(result["llm_response"])

   if __name__ == "__main__":
       import asyncio
       asyncio.run(main())
   ```

6. **Run Your Workflow**
   ```bash
   python tweet_generator.py
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
  - [Getting Started (5-Minute Setup)](#getting-started-5-minute-setup)
    - [Prerequisites](#prerequisites)
  - [Design Principles](#design-principles)
  - [Table of Contents](#table-of-contents)
  - [Core Concepts](#core-concepts)
    - [1. Workflows](#1-workflows)
    - [2. API Integration](#2-api-integration)
    - [3. State Management](#3-state-management)
    - [4. Steps Tracking](#4-steps-tracking)
  - [Setup](#setup)
  - [Why Use This?](#why-use-this)
  - [Design Philosophy](#design-philosophy)
  - [License](#license)
  - [Contributors](#contributors)
  - [Star History](#star-history)
  - [Quick Start (2 minutes)](#quick-start-2-minutes)

## Core Concepts

### 1. Workflows

- Each automation is a Workflow
- Workflows have state management
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

## Setup

```bash
# Install
pip install pynions

# Project structure
myproject/
├── workflows/          # Your workflows
├── data/           # Local storage
├── logs/           # Workflow logs
└── .cache/        # API cache
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
   - Single responsibility workflows

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

## Quick Start (2 minutes)

1. Install Pynions:

   ```bash
   pip install pynions
   ```

2. Add your OpenAI API key to `.env`:

   ```bash
   OPENAI_API_KEY=your_key_here
   ```

3. Run the example:
   ```bash
   python workflows/tweet.py
   ```
