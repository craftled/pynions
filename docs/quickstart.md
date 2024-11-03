---
title: "Quickstart"
publishedAt: "2024-10-30"
updatedAt: "2024-11-03"
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

# Create folders and files
mkdir -p pynions/plugins data

# Install required packages
pip install aiohttp litellm python-dotenv
```

### 2. Create Config Files
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 3. Copy-Paste This Complete Working Example
Create `quickstart.py` and paste this complete code:

```python
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class QuickAI:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("Please add your OpenAI API key to .env file")
    
    async def analyze(self, topic):
        from litellm import completion
        
        try:
            response = await completion(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Give me 3 key points about: {topic}. Be concise."
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

async def main():
    # Initialize
    print("\n🤖 Pynions Quick Start Demo")
    print("---------------------------")
    
    try:
        ai = QuickAI()
        
        # Get user input
        topic = input("\n📝 Enter a topic to analyze: ")
        
        # Process
        print("\n🔄 Analyzing...")
        result = await ai.analyze(topic)
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/analysis_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(result)
        
        # Display result
        print("\n📊 Analysis Results:")
        print("------------------")
        print(result)
        print(f"\n✅ Results saved to: {filename}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Check if OPENAI_API_KEY is set in .env")
        print("2. Verify internet connection")
        print("3. Ensure OpenAI API is accessible")

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Run It!
```bash
# Add your OpenAI API key to .env file (replace with your actual key)
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run the demo
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
