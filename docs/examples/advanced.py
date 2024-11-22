"""Advanced Pynions example showing stats tracking and streaming"""

from datetime import datetime
from litellm import completion
from pynions.core.config import config
from pynions.plugins import StatsPlugin


class ContentAnalyzer:
    """Advanced content analysis with stats tracking"""

    def __init__(self):
        """Initialize with stats plugin"""
        # Check API key
        if not config.check_api_key():
            raise ValueError("Add your OpenAI API key to .env file")
            
        # Initialize stats plugin
        self.stats = StatsPlugin()
        self.stats.initialize()

    async def analyze(self, topic):
        """Analyze a topic with stats tracking"""
        print(f"🔍 Analyzing: {topic}")
        
        prompt = f"""Give me 3 key points about: {topic}. 
        Be concise and focus on actionable insights."""
        
        try:
            # Make completion request
            response = completion(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
                stream=True  # Enable streaming
            )
            
            # Track stats
            self.stats.track_request(
                model="gpt-4o-mini",
                prompt_tokens=len(prompt),
                completion_tokens=len(response.choices[0].message.content)
            )
            
            content = response.choices[0].message.content
            
            # Save if enabled
            if config.get("save_results", True):
                self.save_analysis(content)
                
            return content
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

    def save_analysis(self, content):
        """Save analysis results"""
        output_folder = config.get("output_folder", "data")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_folder}/analysis_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(content)
            
        print(f"💾 Saved to: {filename}")


async def main():
    """Run an example analysis"""
    analyzer = ContentAnalyzer()
    
    print("\n🤖 Advanced Pynions Example")
    print("------------------------")
    
    topic = input("\n📝 What topic should we analyze? ")
    
    if result := await analyzer.analyze(topic):
        print("\n📊 Analysis Results:")
        print("-----------------")
        print(result)
        
        # Show stats
        print("\n📈 Usage Statistics:")
        print("-----------------")
        analyzer.stats.show()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
