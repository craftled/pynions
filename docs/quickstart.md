---
title: "Quickstart"
publishedAt: "2024-10-30"
updatedAt: "2024-11-09"
summary: "Get started with Pynions in 60 seconds - perfect for marketers!"
kind: "detailed"
---

## Quick Setup (Just 2 Steps!)

### 1. Install & Configure

```bash
# Create project and enter it
mkdir my-pynions && cd my-pynions

# Install Pynions
pip install pynions

# Add your OpenAI API key
cp .env.example .env
echo "OPENAI_API_KEY=your-key-here" > .env
```

### 2. Create Your First Workflow

Create `workflows/content_ideas.py` and paste this complete example:

```python
from litellm import completion
from pynions.core.config import config
import os

def generate_content_ideas(topic):
    """Marketing workflow for content ideation"""
    
    # Check API key
    if not config.check_api_key():
        return None
        
    print(f"🎯 Analyzing {topic}...")
    
    prompt = f"""Generate 3 content ideas for {topic}.
    Include for each:
    1. Content Type (blog, video, etc)
    2. Catchy Title
    3. Key Points (3-5)
    """
    
    try:
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_ideas(content):
    """Save workflow results"""
    output_folder = config.get("output_folder", "data")
    os.makedirs(output_folder, exist_ok=True)
    
    filename = f"{output_folder}/content_ideas.txt"
    with open(filename, "w") as f:
        f.write(content)
    return filename

def main():
    print("\n🎯 Content Idea Generator")
    print("----------------------")
    
    topic = input("\n📝 What topic should we analyze? ")
    
    if result := generate_content_ideas(topic):
        print("\n💡 Your Content Ideas:")
        print("-------------------")
        print(result)
        
        if config.get("save_results", True):
            filename = save_ideas(result)
            print(f"\n💾 Ideas saved to: {filename}")

if __name__ == "__main__":
    main()
```

That's it! Run your workflow:
```bash
python workflows/content_ideas.py
```

## What You Get

1. **AI-Powered Content Ideas**: Get instant content suggestions for any topic
2. **Auto-Save**: Results saved to files (optional)
3. **Simple Setup**: Just one API key needed
4. **Marketing Focus**: Built for content creators

## Next Steps

1. **Customize Settings** (Optional)
   Create `pynions.json` to customize where files are saved:
   ```json
   {
       "save_results": true,
       "output_folder": "my_content"
   }
   ```

2. **Try More Examples**
   Check out the `examples` folder for more marketing workflows:
   - Blog post generator
   - Social media scheduler
   - Content repurposing
   - SEO optimization

3. **Read the Docs**
   Visit our [documentation](https://docs.pynions.dev) for more examples and guides.

## Need Help?

- Join our [Discord community](https://discord.gg/pynions)
- Check [common issues](https://docs.pynions.dev/debugging)
- Email us: support@pynions.dev
