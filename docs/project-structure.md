---
title: "Project Structure"
publishedAt: "2024-10-30"
updatedAt: "2024-11-09"
summary: "Learn how to organize your Pynions project files and understand the recommended project structure for building local marketing automation workflows."
kind: "detailed"
---

## Complete File Structure

```
pynions/
├── data/                               # Data storage directory
│   ├── output/                         # Processed data storage
│   └── raw/                            # Raw data storage
│       └── .gitkeep
│
├── docs/                               # Documentation files
│   ├── examples/                       # Example workflows
│   ├── images/                         # Documentation images
│   ├── plugins/                        # Plugin documentation
│   ├── templates/                      # Template files
│   ├── use-cases/                      # Use case documentation
│   ├── workflows/                      # Workflow documentation
│   ├── changelog.md                    # Changelog
│   ├── configuration.md                # Configuration guide
│   ├── data-organization.md            # Data organization guide
│   ├── debugging.md                    # Debugging guide
│   ├── ENV_SETUP.md                    # Environment setup guide
│   ├── index.md                        # Index file
│   ├── installation.md                 # Installation instructions
│   ├── nav.json                        # Navigation order configuration for docs
│   ├── plugins.md                      # Plugin development guide
│   ├── project-structure.md            # Project structure guide
│   ├── quickstart.md                   # Quick start guide
│   ├── SETUP.md                        # Setup guide
│   ├── testing.md                      # Testing guide
│   └── workflows.md                    # Workflow creation guide
│
├── pynions/                            # Main package directory
│   ├── config/                         # Configuration files
│   │   ├── .env                        # Environment variables
│   │   ├── .env.example                # Environment variables example
│   │   ├── settings.json               # Settings
│   │   └── settings.py                 # Settings code
│   │
│   ├── core/                           # Core framework code
│   │   ├── __init__.py                 # Package initialization
│   │   ├── config.py                   # Configuration
│   │   ├── datastore.py                # Data storage
│   │   ├── plugin.py                   # Plugin base class
│   │   ├── utils.py                    # Utility functions
│   │   └── workflow.py                 # Workflow base class
│   │
│   ├── plugins/                        # Plugin modules
│   │   ├── __init__.py                 # Package initialization
│   │   ├── base.py                     # Plugin base class
│   │   ├── frase.py                    # Frase plugin
│   │   ├── jina.py                     # Jina plugin
│   │   ├── litellm_plugin.py           # LiteLLM plugin
│   │   ├── serper.py                   # Serper.dev plugin
│   │   └── stats.py                    # Stats plugin
│   │
│   ├── tests/                          # Test files
│   │   ├── test_plugins/               # Test plugin files
│   │   │   └── test_serper_plugin.py
│   │   ├── __init__.py                 # Package initialization
│   │   ├── conftest.py                 # Test configuration
│   │   └── test_core.py                # Core test file
│   │
│   └── workers/                        # Workers directory
│       └── pricing_research_worker.py  # Pricing research worker
│   │
│   └── __init__.py                     # Package initialization
│
├── workflows/                          # Workflow files
│   ├── content_analysis_workflow.py    # Content analysis workflow
│   ├── example_workflow.py             # Example workflow
│   └── research_workflow.py            # Research workflow
│
├── .cursorrules                        # Cursor IDE rules
├── .gitignore                          # Git ignore file
├── LICENSE                             # Project license
├── pyproject.toml                      # Pyproject configuration
├── pytest.ini                          # pytest configuration
├── README.md                           # Project readme
├── requirements.txt                    # Python dependencies
└── setup.py                            # Setup script
```

## Step-by-Step Setup on Mac

1. Open Terminal and create project directory:

```bash
# Create main project directory
mkdir ~/Documents/pynions
cd ~/Documents/pynions

# Create all directories
mkdir -p pynions/plugins pynions/utils docs/images examples/test_plugins tests/test_plugins data
```

2. Create all required files:

```bash
# Create Python files
touch pynions/__init__.py pynions/core.py
touch pynions/plugins/__init__.py pynions/plugins/serper_plugin.py
touch pynions/plugins/litellm_plugin.py pynions/plugins/playwright_plugin.py
touch pynions/plugins/jina_plugin.py
touch pynions/utils/__init__.py pynions/utils/helpers.py

# Create example files
touch examples/__init__.py examples/serp_analysis.py examples/content_workflow.py

# Create test files
touch tests/__init__.py tests/test_core.py
touch tests/test_plugins/test_serper_plugin.py

# Create config files
touch .env.example config.example.json requirements.txt pytest.ini
touch README.md .gitignore

# Create documentation files
touch docs/01-project-structure.md docs/02-installation.md
touch docs/03-configuration.md docs/04-plugins.md
touch docs/05-workflows.md docs/06-debugging.md
```

3. Copy file contents (see separate guides for each file)

## File Purposes

### Core Files

- `pynions/core.py`: Main framework functionality
- `requirements.txt`: Python package dependencies
- `.env.example`: Template for environment variables
- `config.example.json`: Template for configuration

### Plugin Files

- `serper_plugin.py`: Google SERP data extraction
- `litellm_plugin.py`: AI model integration
- `playwright_plugin.py`: Web scraping
- `jina_plugin.py`: Content extraction

### Documentation Files

- `01-project-structure.md`: Project organization (this file)
- `02-installation.md`: Setup instructions
- `03-configuration.md`: Configuration guide
- `04-plugins.md`: Plugin development guide
- `05-workflows.md`: Workflow creation guide
- `06-debugging.md`: Troubleshooting guide

### Example Files

- `serp_analysis.py`: SERP analysis workflow
- `content_workflow.py`: Content creation workflow

## Quick Copy-Paste Setup

Here's a one-liner to create the entire structure:

```bash
mkdir -p ~/Documents/pynions && cd ~/Documents/pynions && mkdir -p pynions/plugins pynions/utils docs/images examples tests/test_plugins data && touch pynions/__init__.py pynions/core.py pynions/plugins/__init__.py pynions/plugins/{serper,litellm,playwright,jina}_plugin.py pynions/utils/__init__.py pynions/utils/helpers.py examples/__init__.py examples/{serp_analysis,content_workflow}.py tests/__init__.py tests/test_core.py tests/test_plugins/test_serper_plugin.py .env.example config.example.json requirements.txt pytest.ini README.md .gitignore docs/{01-project-structure,02-installation,03-configuration,04-plugins,05-workflows,06-debugging}.md
```

## Next Steps

1. See `02-installation.md` for setting up your Python environment
2. Follow `03-configuration.md` to configure your APIs
3. Check `examples/` directory for sample workflows
4. Read through the docs in order for detailed understanding

## Notes

- All paths are relative to the project root
- The `data/` directory is for storing workflow results
- `.gitkeep` files are used to track empty directories
- Documentation follows a numbered sequence for easy navigation
