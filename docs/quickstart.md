---
title: "Quickstart"
publishedAt: "2024-10-30"
updatedAt: "2024-11-09"
summary: "Get started with Pynions in 2 minutes by setting up your first local AI workflow. No cloud dependencies, just Python and a few API keys."
kind: "detailed"
---

## Super Quick Setup (Copy-Paste Ready)

### 1. Create Project & Install

```bash
# Create project directory and enter it
mkdir ~/Documents/pynions && cd ~/Documents/pynions

# Create virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Create project structure
mkdir -p pynions/config pynions/plugins pynions/core data/output data/raw

# Install required packages
pip install aiohttp litellm python-dotenv httpx
```

### 2. Create Config Files

```bash
# Create config directory and files
mkdir -p pynions/config
cp .env.example pynions/config/.env
cp settings.example.json pynions/config/settings.json

# Add your API key to .env
nano pynions/config/.env
```

### 3. Copy-Paste This Complete Working Example

Create `quickstart.py` and paste this complete code:

```python
import asyncio
import os
from datetime import datetime
from pynions.core.config import load_config
from pynions.core.datastore import save_result
from pynions.plugins.litellm import LiteLLMPlugin

async def main():
    # Load configuration
    config = load_config()

    # Initialize LiteLLM plugin
    ai = LiteLLMPlugin(config["plugins"]["litellm"])

    print("\n🤖 Pynions Quick Start Demo")
    print("---------------------------")

    try:
        # Get user input
        topic = input("\n📝 Enter a topic to analyze: ")

        # Process with AI
        print("\n🔄 Analyzing...")
        response = await ai.analyze(topic)

        # Save result using core utilities
        save_result(
            content=response,
            project_name="quickstart",
            status="research"
        )

        # Display result
        print("\n📊 Analysis Results:")
        print("------------------")
        print(response)
        print(f"\n✅ Results saved to data/output/quickstart/")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Check if API keys are set in pynions/config/.env")
        print("2. Verify internet connection")
        print("3. Ensure API services are accessible")

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Run It!

```bash
# Make sure your API keys are in pynions/config/.env
python quickstart.py
```

## What You Get

- A working AI analysis tool
- Results saved to data folder
- Easy to modify and extend

## Next Steps

1. Try different topics
2. Modify the analysis prompt
3. Add more features
4. Check the full documentation

## Common Issues

1. **"Module not found" error**

   ```bash
   pip install aiohttp litellm python-dotenv
   ```

2. **API Key error**

   - Check .env file exists
   - Verify API key is correct
   - Make sure no quotes in .env file

3. **Permission error**
   ```bash
   chmod 755 data
   ```

## 30-Second Test Run

```bash
# Quick test with a simple topic
echo "OPENAI_API_KEY=your-key-here" > .env
python quickstart.py
# Enter topic: "artificial intelligence"
```

That's it! You should see AI-generated analysis of your topic and the results saved to a file.

Need the full version? Check out the complete documentation for all features and capabilities.
