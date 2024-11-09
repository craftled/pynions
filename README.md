# Pynions 🚀

A lean open-source Python framework for building AI-powered automation workflows that run on your machine. Built for marketers who want to automate research, monitoring, and content tasks without cloud dependencies or complex setups.

Think of it as Zapier/n8n but for local machines, designed specifically for marketing workflows.

## What is Pynions?

Pynions helps marketers automate:

- Content research and analysis
- SERP monitoring and tracking
- Content extraction and processing
- AI-powered content generation
- Marketing workflow automation

## Key Features

- 🚀 Start small, ship fast
- 🔌 Easy API connections to your existing tools
- 🤖 AI-first but not AI-only
- 📦 Zero bloat, minimal dependencies
- 🛠 Built for real marketing workflows
- ⚡ Quick to prototype and iterate
- 🌐 Local-first, no cloud dependencies

## Technology Stack

- Python for all code
- Pytest for testing
- LiteLLM for unified LLM access
- Jina AI for content extraction
- Serper for SERP analysis
- Playwright for web automation
- dotenv for configuration
- httpx for HTTP requests

## Quick Start

```bash
# Create project directory
mkdir pynions && cd pynions

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Set up configuration
mkdir -p pynions/config
cp .env.example pynions/config/.env
cp settings.example.json pynions/config/settings.json

# Add your API keys to .env
nano pynions/config/.env
```

## Example Workflow

```python
import asyncio
from pynions.core.workflow import Workflow, WorkflowStep
from pynions.core.config import load_config
from pynions.core.datastore import save_result
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader

async def main():
    # Load configuration
    config = load_config()

    # Initialize plugins
    serper = SerperWebSearch(config["plugins"]["serper"])
    jina = JinaAIReader(config["plugins"]["jina"])

    # Create workflow
    workflow = Workflow(
        name="content_research",
        description="Research and analyze content"
    )

    # Add steps
    workflow.add_step(WorkflowStep(
        plugin=serper,
        name="search",
        description="Search for relevant content"
    ))

    workflow.add_step(WorkflowStep(
        plugin=jina,
        name="extract",
        description="Extract clean content"
    ))

    # Execute workflow
    results = await workflow.execute({
        "query": "marketing automation trends 2024"
    })

    # Save results
    save_result(
        content=results,
        project_name="trends_research",
        status="research"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Built-in Plugins

- **SerperWebSearch**: Google SERP data extraction using Serper.dev API
- **JinaAIReader**: Clean content extraction from web pages
- **LiteLLMPlugin**: Unified access to various LLM APIs
- **FraseAPI**: Content analysis and metrics extraction
- **PlaywrightPlugin**: Web scraping and automation
- **StatsPlugin**: Track and display request statistics
- More plugins coming soon!

## Documentation

1. [Project Structure](docs/01-project-structure.md)
2. [Installation Guide](docs/02-installation.md)
3. [Configuration Guide](docs/03-configuration.md)
4. [Plugin Development](docs/04-plugins.md)
5. [Workflow Creation](docs/05-workflows.md)
6. [Debugging Guide](docs/06-debugging.md)

## Requirements

- Python 3.8 or higher
- pip and venv
- Required API keys:
  - OpenAI API key
  - Serper dev API key
  - Perplexity API key (optional)

## Configuration

### Environment Variables (pynions/config/.env)

```bash
# Search API
SERPER_API_KEY=your_serper_key_here

# AI Models
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Content Processing
JINA_API_KEY=your_jina_key_here
FRASE_API_KEY=your_frase_key_here
```

### Application Config (pynions/config/settings.json)

See [settings.example.json](pynions/config/settings.example.json) for all available options.

## Philosophy

- Smart and safe defaults
  - OpenAI's "gpt-4o-mini" is the default LLM
  - Serper is the default search tool
  - Perplexity is the default research tool
- No AI-only, always human in the loop
- Minimal dependencies
- No cloud dependencies
- No proprietary formats
- No tracking
- No telemetry
- No bullshit

## Common Issues

1. **Module not found errors**

```bash
pip install -r requirements.txt
```

2. **API Key errors**

- Check if `.env` file exists
- Verify API keys are correct
- Remove quotes from API keys in `.env`

3. **Permission errors**

```bash
chmod 755 data
```

## Contributing

See [Project Structure](docs/01-project-structure.md) for:

- Code organization
- Testing requirements
- Documentation standards

## License

MIT License - see [LICENSE](LICENSE) for details

## Support

If you encounter issues:

1. Check the [Debugging Guide](docs/06-debugging.md)
2. Review relevant documentation sections
3. Test components in isolation
4. Use provided debugging tools
5. Check common issues section

## Credits

Built with ☕️ and dedication by a marketer who codes.
