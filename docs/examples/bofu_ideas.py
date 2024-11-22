"""
Marketing Content Generator - Bottom of Funnel (BOFU) Ideas

This script helps marketers quickly generate conversion-focused content ideas
for their products or services. Just provide your product name and target audience!

Example usage:
    python bofu_ideas.py
    > Enter product: Marketing Automation Software
    > Enter target audience: Small Business Owners
"""

import os
from datetime import datetime
from litellm import completion
from pynions.core.config import config

def generate_content_ideas(product, target_audience):
    """Generate conversion-focused content ideas for your product"""
    if not config.check_api_key():
        return None

    print(f"🎯 Generating ideas for {product}...")
    
    prompt = f"""Generate 5 high-converting content ideas for {product} targeting {target_audience}.
    
    Include these content types:
    - Customer Success Story
    - Product Comparison Guide
    - ROI Calculator or Tool
    - Implementation Guide
    - Video Tutorial
    
    For each idea provide:
    1. Content Type
    2. Catchy Title
    3. Main Call-to-Action
    4. Key Conversion Goal
    """

    try:
        # Let litellm handle the defaults
        response = completion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        print("✅ Ideas generated successfully!")
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def save_to_file(content):
    """Save the ideas to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = config.get("output_folder", "data")
    filename = f"{output_folder}/bofu_ideas_{timestamp}.txt"
    
    os.makedirs(output_folder, exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)
    
    return filename

def main():
    """Run the content idea generator"""
    print("\n🎯 BOFU Content Ideas Generator")
    print("----------------------------")
    
    product = input("\n📦 What product/service are you marketing? ")
    audience = input("👥 Who is your target audience? ")
    
    result = generate_content_ideas(product, audience)
    if result:
        print("\n💡 Content Ideas:")
        print("--------------")
        print(result)
        
        if config.get("save_results", True):
            filename = save_to_file(result)
            print(f"\n💾 Ideas saved to: {filename}")

if __name__ == "__main__":
    main()
