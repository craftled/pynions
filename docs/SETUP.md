---
title: "Local Setup"
publishedAt: "2024-10-30"
updatedAt: "2024-11-03"
summary: "Detailed local setup guide for Pynions."
kind: "detailed"
---

## Prerequisites Installation (Mac)

1. Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python 3.9 or higher:
```bash
brew install python
```

3. Install Git:
```bash
brew install git
```

## Project Setup

1. Open Terminal on your Mac

2. Create a new directory for your project:
```bash
mkdir ~/Documents/pynions
cd ~/Documents/pynions
```

3. Initialize Git repository:
```bash
git init
```

4. Create the project structure:
```bash
# Create directories
mkdir -p pynions/plugins pynions/utils examples tests data

# Create empty files
touch README.md requirements.txt config.example.json .gitignore
touch pynions/__init__.py pynions/core.py
touch pynions/plugins/__init__.py
touch pynions/utils/__init__.py
touch examples/serp_analysis.py
touch tests/__init__.py
```

5. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate
```

6. Install dependencies:
```bash
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Configuration Setup

1. All configuration files are located in `pynions/config/`:
   - `.env` - For API keys and secrets
   - `settings.json` - For application settings

2. Copy example files:
```bash
cp .env.example pynions/config/.env
cp settings.example.json pynions/config/settings.json
```

3. Edit your configuration:
```bash
# Add your API keys
nano pynions/config/.env

# Modify settings if needed
nano pynions/config/settings.json
```

## Cursor IDE Setup

1. Install Cursor from https://cursor.sh/

2. Open Cursor and select "Open Folder"

3. Navigate to your project directory (~/Documents/pynions)

4. Set up Python interpreter:
   - Click on the Python version in the bottom status bar
   - Select the interpreter from your virtual environment:
     `~/Documents/pynions/venv/bin/python`

## Running Your First Workflow

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

2. Run the example SERP analysis:
```bash
python examples/serp_analysis.py
```

3. Check the results in the `data` directory

## Common Issues and Solutions

1. **Module not found errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again
   - Check if you're in the correct directory

2. **API errors**
   - Verify API keys in config.json
   - Check API service status
   - Look at logs in data/pynions.log

3. **Playwright errors**
   - Run `playwright install` again
   - Check Playwright documentation for Mac-specific issues

4. **Permission errors**
   - Run `chmod +x venv/bin/python` if needed
   - Ensure write permissions in data directory

## Development Workflow

1. Activate virtual environment:
```bash
source venv/bin/activate
```

2. Create new branch for features:
```bash
git checkout -b feature-name
```

3. Run tests:
```bash
pytest tests/
```

4. Commit changes:
```bash
git add .
git commit -m "Description of changes"
```

Remember to:
- Always work with the virtual environment activated
- Keep config.json in .gitignore
- Check logs in data/pynions.log for issues
- Run tests before committing changes
