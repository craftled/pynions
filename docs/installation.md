---
title: "Installation"
publishedAt: "2024-10-30"
updatedAt: "2024-11-14"
summary: "Complete guide for installing and configuring Pynions on your local machine."
kind: "detailed"
---

## Prerequisites

1. Install Homebrew (if not already installed):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python 3.9+ and Git:

```bash
brew install python git

#Verify installations
python3 --version # Should show 3.9 or higher
git --version
```

## Project Setup

1. Create project structure:

```bash
# Create main directory
mkdir -p ~/Documents/pynions && cd ~/Documents/pynions

# Initialize git repository
git init
Create core directories
mkdir -p pynions/{plugins,utils,config} docs/{examples,plugins,workflows} tests/test_plugins data/{raw,output}

#Create core Python files
touch pynions/init.py pynions/core.py
touch pynions/plugins/init.py pynions/plugins/{serper,litellm,playwright,jina}plugin.py
touch pynions/utils/init.py pynions/utils/helpers.py

#Create example files
touch examples/init.py examples/{serp_analysis,content_workflow}.py

# Create test files
touch tests/init.py tests/test_core.py tests/test_plugins/test_serper_plugin.py

# Create configuration files
touch .env.example config.example.json requirements.txt pytest.ini
touch README.md .gitignore

# Create documentation files
touch docs/{project-structure,installation,configuration,plugins,workflows,debugging}.md
```

2. Set up Python environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Configuration

### Environment Setup

1. Copy configuration templates:

```bash
cp .env.example pynions/config/.env
cp settings.example.json pynions/config/settings.json
```

2. Configure API keys in `.env`:

```bash
# Required API Keys
SERPER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Optional API Keys
ANTHROPIC_API_KEY=your_key_here
JINA_API_KEY=your_key_here
FRASE_API_KEY=your_key_here
```

### Configuration Loading

The system loads configuration in this order:

1. System environment variables
2. `.env` file variables
3. `settings.json` settings

Environment variables are automatically loaded by the base Plugin class.

### Security Best Practices

- Never commit `.env` file
- Keep API keys secure
- Regularly rotate keys
- Use minimum required permissions
- Verify `.env` is in `.gitignore`
- Remove quotes from API keys in `.env`
- Don't include actual API keys in settings.json

## Verify Installation

1. Run test workflow:

```bash
# Ensure venv is activated
source venv/bin/activate

# Run example
python examples/serp_analysis.py
```

2. Check output:

- Progress messages should appear
- Results in `data/` directory
- No error messages
- Check logs in data/pynions.log

## IDE Setup (Cursor)

1. Download Cursor:

   - Visit https://cursor.sh
   - Download Mac version
   - Install application

2. Open project:

   - Open Cursor
   - File -> Open Folder
   - Select `~/Documents/pynions`

3. Configure Python interpreter:
   - Click Python version in status bar
   - Select: `~/Documents/pynions/venv/bin/python`

## Common Issues

### Python Version Issues

```bash
# Check Python version
python --version

# If needed, specify Python 3 explicitly
python3 --version
```

### Virtual Environment Issues

```bash
# Deactivate if already in a venv
deactivate

# Remove existing venv if needed
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate
source venv/bin/activate
```

### Permission Issues

```bash
# Fix venv permissions
chmod +x venv/bin/activate
chmod +x venv/bin/python

# Fix data directory permissions
chmod 755 data
```

### Module Not Found Issues

```bash
# Verify virtual environment is activated
which python # Should show: ~/Documents/pynions/venv/bin/python

# Verify installation
pip list

# Reinstall dependencies
pip install -r requirements.txt
```

### API Issues

```bash
# Check if environment variables are loaded
python -c "import os; print(os.getenv('SERPER_API_KEY'))"

# Common fixes:
- Check if .env file exists
- Verify API keys are correct
- Remove quotes from API keys
- Ensure .env is in correct location (pynions/config/.env)
```

### Playwright Issues

```bash
# Install browsers
playwright install

# If that fails, try with sudo
sudo playwright install

# Verify installation
playwright --version
```

## Development Workflow

1. Always work with activated virtual environment
2. Create feature branches for new work:

```bash
git checkout -b feature-name
```

3. Run tests before committing:

```bash
pytest tests/
```

4. Follow git workflow:

```bash
git add .
git commit -m "Description of changes"
```

Remember to:

- Keep config.json in .gitignore
- Check logs in data/pynions.log for issues
- Run tests before committing changes
- Test components in isolation when debugging

## Development Tools

Optional but recommended:

1. HTTPie for API testing:

```bash
brew install httpie
```

2. jq for JSON processing:

```bash
brew install jq
```

3. VS Code extensions:
   - Python
   - Python Environment Manager

## Updating

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```

To update Playwright:

```bash
playwright install
```

## Next Steps

1. Read [Configuration](configuration) for detailed API setup
2. Try example workflows in [Examples](examples)
3. Check [Plugins](plugins) for plugin usage
4. See [Workflows](workflows) for creating custom workflows
5. Review [Debugging](debugging) if you encounter issues
