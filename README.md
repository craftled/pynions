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
- LiteLLM for LLM API calls
- dotenv for .env file management
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
cp .env.example .env
cp config.example.json config.json

# Add your API keys to .env
# Edit with your actual keys
nano .env
```

## Example Workflow

```python
import asyncio
from pynions import Workflow, WorkflowStep, Config, DataStore, SerperWebSearch

async def main():
    # Load configuration
    config = Config("config.json")
    data_store = DataStore()

    # Initialize plugins
    serper = SerperWebSearch(config.get_plugin_config("serper"))

    # Create workflow steps
    serp_step = WorkflowStep(
        plugin=serper,
        name="fetch_serp",
        description="Fetch top 10 Google results"
    )

    # Create workflow
    workflow = Workflow(
        name="serp_analysis",
        description="Analyze top 10 Google results for a query"
    )
    workflow.add_step(serp_step)

    # Execute workflow
    results = await workflow.execute({
        "query": "best project management software 2024"
    })

    # Save results
    data_store.save(results, "serp_analysis")

if __name__ == "__main__":
    asyncio.run(main())
```

## Built-in Plugins

- **SerperWebSearch**: Google SERP data extraction using Serper.dev API
- **JinaAIReader**: Clean content extraction from web pages
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

### Environment Variables (.env)
```bash
SERPER_API_KEY=your_serper_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
JINA_API_KEY=your_jina_key_here
```

### Application Config (config.json)
See [config.example.json](config.example.json) for all available options.

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
