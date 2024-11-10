---
title: "Installation"
publishedAt: "2024-10-30"
updatedAt: "2024-11-10"
summary: "Step-by-step guide for installing Pynions and setting up your local marketing automation environment on macOS."
kind: "detailed"
---

## Prerequisites

1. Install Homebrew (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python 3.9+ via Homebrew:
```bash
brew install python
```

3. Verify Python installation:
```bash
python3 --version  # Should show 3.9 or higher
```

4. Install git:
```bash
brew install git
```

## Project Setup

1. Clone or create project:
```bash
# If starting fresh:
mkdir ~/Documents/pynions
cd ~/Documents/pynions

# If cloning:
git clone https://github.com/yourusername/pynions.git
cd pynions
```

2. Create virtual environment:
```bash
# Create venv
python3 -m venv venv

# Activate it
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Configuration

1. Set up environment variables:
```bash
# Copy example files to the correct location
mkdir -p pynions/config
cp .env.example pynions/config/.env
cp settings.example.json pynions/config/settings.json
```

2. Edit .env file:
```bash
# Open in your preferred editor
nano .env

# Add your API keys:
SERPER_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
JINA_API_KEY=your_key_here
```

## Verify Installation

1. Run test workflow:
```bash
# Make sure venv is activated
source venv/bin/activate

# Run example
python examples/serp_analysis.py
```

2. Check the output:
- Should see progress messages
- Results saved in `data/` directory
- No error messages

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
   - Select interpreter from virtual environment:
     `~/Documents/pynions/venv/bin/python`

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
# Verify installation
pip list

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. Read `03-configuration.md` for detailed API setup
2. Try example workflows in `examples/`
3. Check `04-plugins.md` for plugin usage
4. See `05-workflows.md` for creating custom workflows

## Development Tools

Optional but recommended tools:

1. HTTPie for API testing:
```bash
brew install httpie
```

2. jq for JSON processing:
```bash
brew install jq
```

3. Visual Studio Code extensions:
   - Python
   - Python Environment Manager
   - Git Lens
   - Docker (if using containers)

## Updating

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

To update Playwright:
```bash
playwright install
```
