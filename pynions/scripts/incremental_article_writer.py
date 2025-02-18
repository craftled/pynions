import asyncio
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pynions.plugins.perplexity import PerplexityAPI


class IncrementalArticleWriter:
    """Builds articles incrementally by researching and writing one section at a time"""

    def __init__(self):
        self.perplexity = PerplexityAPI(
            {
                "model": "sonar-reasoning-pro",
                "temperature": 0.2,
                "max_tokens": 4000,
                "return_related_questions": False,
            }
        )

    async def research_section(self, topic: str, section: str) -> Dict:
        """Research a specific section using Perplexity"""
        print(f"\n🔍 Researching {section} for {topic}...")

        response = await self.perplexity.execute(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a research expert. Find detailed, factual information with sources.
Focus on recent data (2020-2024 unless historical).
Verify all claims with reliable sources.
Include statistics, expert quotes, and case studies.""",
                    },
                    {
                        "role": "user",
                        "content": f"Research {section} of {topic}. Find comprehensive information, statistics, examples, and expert insights. Use only reliable sources.",
                    },
                ]
            }
        )

        return response

    async def write_section(self, topic: str, section: str, research: Dict) -> str:
        """Write a section using the research data"""
        print(f"\n✍️ Writing {section} section...")

        response = await self.perplexity.execute(
            {
                "messages": [
                    {
                        "role": "system",
                        "content": """You are writing a section of a professional article.
Use proper markdown formatting.
Create inline links for:
- Statistics and data points
- Mentioned tools and products
- Expert quotes and insights
- Companies and organizations
- Research papers and studies
Format: [descriptive text](url)
Write in clear, engaging language for professionals.""",
                    },
                    {
                        "role": "user",
                        "content": f"""Write the {section} section for an article about {topic}.

Research to use:
{research['choices'][0]['message']['content']}

Available sources for links:
{json.dumps(research.get('citations', []), indent=2)}

Requirements:
1. Use proper markdown formatting
2. Include inline links to sources (not numbered references)
3. Write 400-600 words
4. Use clear, professional language
5. Include relevant statistics and examples
6. Break into subsections if needed
7. Use bullet points for lists""",
                    },
                ]
            }
        )

        return response["choices"][0]["message"]["content"]

    def initialize_article(self, topic: str, audience: str) -> str:
        """Create the initial article file with title"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"data/articles/markdown/{topic.lower().replace(' ', '_')}_{timestamp}.md"
        )
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        title = f"# What Is {topic}: A Comprehensive Guide for {audience}\n\n"
        with open(filename, "w") as f:
            f.write(title)

        return filename

    def append_section(self, filename: str, content: str):
        """Append a section to the article file"""
        with open(filename, "a") as f:
            f.write(content + "\n\n")

    async def generate_article(self, topic: str, audience: str = "professionals"):
        """Generate a complete article section by section"""
        try:
            # Initialize article file
            article_file = self.initialize_article(topic, audience)
            print(f"\n📄 Created article file: {article_file}")

            # Define sections to generate
            sections = [
                "definition",
                "methodology",
                "types",
                "benefits",
                "challenges",
                "best_practices",
                "trends",
                "qa",
            ]

            # Generate each section
            for section in sections:
                print(f"\n📝 Working on {section.upper()} section...")

                # Research the section
                research_data = await self.research_section(topic, section)

                # Write the section using research
                section_content = await self.write_section(
                    topic, section, research_data
                )

                # Append to article
                self.append_section(article_file, section_content)
                print(f"✅ Completed {section} section")

            print(f"\n🎉 Article generation complete!")
            print(f"📄 Article saved to: {article_file}")
            return article_file

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return None


async def main():
    writer = IncrementalArticleWriter()
    await writer.generate_article("growth marketing", "marketing professionals")


if __name__ == "__main__":
    asyncio.run(main())
