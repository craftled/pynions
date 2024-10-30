import os
from datetime import datetime
from dotenv import load_dotenv
from litellm import completion

# Load API key from .env file
load_dotenv()


def generate_content_ideas(product, target_audience):
    """Generate BOFU content ideas for a specific product and audience"""
    try:
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "Error: Please add your OpenAI API key to .env file"

        prompt = f"""Generate 5 bottom-of-funnel (BOFU) content ideas for {product} targeting {target_audience}.
        Focus on conversion-focused content types like:
        - Case studies
        - Comparison guides
        - ROI calculators
        - Implementation guides
        - Product tutorials
        - Customer success stories
        
        For each idea, include:
        - Content type
        - Working title
        - Key conversion goal
        
        Be specific and actionable."""

        # Get AI response
        response = completion(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


def save_to_file(content):
    """Save the ideas to a file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/bofu_ideas_{timestamp}.txt"

    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Save content
    with open(filename, "w") as f:
        f.write(content)

    return filename


def main():
    # Show welcome message
    print("\n🎯 BOFU Content Ideas Generator")
    print("----------------------------")

    # Get input from user
    product = input("\n📦 What product/service are you marketing? ")
    audience = input("👥 Who is your target audience? (e.g., B2B Marketing Managers) ")

    # Generate ideas
    print("\n🔄 Generating ideas...")
    result = generate_content_ideas(product, audience)

    # Show results
    print("\n💡 Content Ideas:")
    print("--------------")
    print(result)

    # Save results
    filename = save_to_file(result)
    print(f"\n💾 Ideas saved to: {filename}")


if __name__ == "__main__":
    main()
