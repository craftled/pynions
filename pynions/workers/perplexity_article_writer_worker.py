import asyncio
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pynions.core import Worker
from pynions.plugins.litellm_plugin import LiteLLM


class PerplexityArticleWriterWorker(Worker):
    """Worker for generating articles using Claude 3.5 Sonnet"""

    def __init__(self, worker_config: Optional[Dict[str, Any]] = None):
        """Initialize the article writer worker"""
        super().__init__(worker_config)
        self.logger = logging.getLogger("pynions.workers.article_writer")

        # Initialize LiteLLM plugin with Claude 3.5 Sonnet and maximized settings
        self.llm = LiteLLM(
            {
                "model": "anthropic/claude-3-5-sonnet-20240620",
                "temperature": 0.7,  # Good balance for creative yet focused writing
                "max_tokens": 8192,  # Maximized for comprehensive articles
                "max_completion_tokens": 8192,
                "stream": True,  # Enable streaming for large outputs
                "timeout": 600,  # 10-minute timeout for long articles
            }
        )

        self.logger.info(
            "Initialized ArticleWriter with Claude 3.5 Sonnet (maximized settings)"
        )

    def _create_article_prompt(
        self, topic: str, audience: str, research_data: Dict
    ) -> str:
        """Create a comprehensive prompt for article generation"""

        # Extract and format all citations for easy reference
        all_citations = {}
        for section_name, section_data in research_data["sections"].items():
            citations = section_data.get("citations", [])
            for url in citations:
                domain = url.split("//")[-1].split("/")[0]
                # Create a more descriptive key based on the domain and section
                key = f"{domain}_{section_name}"
                all_citations[key] = url

        # Format citations as inline markdown links
        formatted_citations = "\n".join(
            [f"- [{k}]({v})" for k, v in all_citations.items()]
        )

        return f"""Write a comprehensive, publication-ready article about {topic} for {audience}. This should be a substantial piece (2000-3000 words) that thoroughly explores the topic and provides actionable insights.

Key Requirements:
1. Write in a clear, authoritative tone for {audience}
2. Use proper markdown formatting
3. Use inline markdown links (format: [descriptive text](url))
4. Focus on actionable insights
5. Maintain consistent structure
6. Remove any meta-commentary or thinking-out-loud sections
7. Keep paragraphs short (2-3 sentences maximum)
8. Add extra line breaks between paragraphs
9. Break down complex ideas into bullet points
10. Use subheadings to organize content
11. Include comparison tables where relevant
12. Focus on readability and scannability
13. Use bold text for emphasis
14. Include plenty of real-world examples and data

Writing Style:
1. Start each section with a hook
2. Break long explanations into smaller chunks
3. Use transitional phrases between ideas
4. Include specific examples after concepts
5. Add bullet points for lists longer than 3 items
6. Create white space for better readability
7. Bold key terms and concepts
8. Use active voice
9. Keep sentences concise
10. Vary paragraph length (but keep them short)

Available Citations (Use as inline links):
{formatted_citations}

Research Data to Incorporate:
Definition: {research_data['sections']['definition']['choices'][0]['message']['content']}
Methodology: {research_data['sections']['methodology']['choices'][0]['message']['content']}
Types: {research_data['sections']['types']['choices'][0]['message']['content']}
Benefits: {research_data['sections']['benefits']['choices'][0]['message']['content']}
Challenges: {research_data['sections']['challenges']['choices'][0]['message']['content']}
Best Practices: {research_data['sections']['best_practices']['choices'][0]['message']['content']}
Trends: {research_data['sections']['trends']['choices'][0]['message']['content']}
Q&A: {research_data['sections']['qa']['choices'][0]['message']['content']}

Article Structure:
# What Is {topic}: A Comprehensive Guide for {audience}

[Introduction - 250-300 words]
- Clear definition and importance
- Market context and relevance for {audience}
- Overview of key benefits
- Article roadmap

## Core Principles [400-500 words]
- 4-5 fundamental principles
- Detailed explanation of each
- Real-world examples
- Implementation considerations

## Key Features & Capabilities [400-500 words]
- Comprehensive feature breakdown
- Technical specifications
- Integration possibilities
- Comparison with alternatives

## Benefits & ROI [400-500 words]
- Detailed analysis of benefits
- ROI calculations and metrics
- Case studies and success stories
- Industry-specific advantages

## Implementation Guide [400-500 words]
- Step-by-step setup process
- Technical requirements
- Best practices
- Common pitfalls to avoid

## Advanced Strategies [300-400 words]
- Advanced use cases
- Power user tips
- Optimization techniques
- Scaling considerations

## Future Developments [200-300 words]
- Upcoming features
- Industry trends
- Integration roadmap
- Market predictions

## Getting Started [200-300 words]
- Quick start guide
- Resource requirements
- Timeline expectations
- Next steps

[Conclusion - 150-200 words]
- Key takeaways
- Strategic recommendations
- Call to action

Writing Guidelines:
1. NO meta-commentary or thinking sections
2. NO numbered citations - use inline links
3. Keep paragraphs focused and concise
4. Use bullet points for lists
5. Include relevant statistics
6. Link to sources naturally in text
7. Maintain professional tone
8. Focus on actionability
9. Add comparison tables
10. Include specific implementation steps

Please write the complete article now, following this structure and incorporating all research data provided."""

    def _format_citations(self, citations: List[str]) -> str:
        """Format citations into markdown inline links"""
        formatted_citations = []
        for url in citations:
            # Extract domain name for link text
            domain = url.split("//")[-1].split("/")[0]
            formatted_citations.append(f"[{domain}]({url})")
        return ", ".join(formatted_citations)

    def _create_section_prompt(
        self, section_name: str, section_data: Dict[str, Any], audience: str
    ) -> str:
        """Create a prompt for generating a section of the article"""
        content = section_data["choices"][0]["message"]["content"]
        citations = section_data.get("citations", [])
        formatted_citations = self._format_citations(citations)

        prompt = f"""You are writing the {section_name} section for an article. Your audience is {audience}.

Research Data:
{content}

Available Sources:
{formatted_citations}

Write a CONCISE, publication-ready section that:
1. Opens with a strong, clear statement
2. Presents key insights in a logical flow
3. Uses inline markdown links for citations
4. Maintains professional yet engaging tone
5. Focuses on actionable insights

Format Guidelines:
- 2-3 concise paragraphs
- Use bullet points for lists
- Include only essential information
- Link to sources naturally in text
- Avoid jargon and repetition

Please write the section now:"""

        return prompt

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the article writing process"""
        try:
            # Load research data
            research_files = [
                f for f in os.listdir("data/articles") if f.endswith(".json")
            ]
            if not research_files:
                raise ValueError("No research data files found")

            latest_file = sorted(research_files)[-1]
            research_path = f"data/articles/{latest_file}"

            self.logger.info(f"Loading research data from: {research_path}")

            with open(research_path, "r") as f:
                research_data = json.load(f)

            # Extract metadata
            topic = research_data.get("topic", "Unknown Topic")
            audience = research_data.get("audience", "general audience")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            self.logger.info(
                f"Writing comprehensive article about {topic} for {audience}"
            )

            # Create the comprehensive article prompt
            article_prompt = self._create_article_prompt(topic, audience, research_data)

            # Generate the complete article
            self.logger.info("Generating article with maximized settings...")
            response = await self.llm.execute(
                {"messages": [{"role": "user", "content": article_prompt}]}
            )

            if not response or "choices" not in response:
                raise ValueError("Invalid response from LLM")

            article_content = response["choices"][0]["message"]["content"]

            # Post-process the content to remove any remaining think sections
            article_content = self._clean_article_content(article_content)

            # Save article
            output_dir = "data/articles/markdown"
            os.makedirs(output_dir, exist_ok=True)

            output_path = (
                f"{output_dir}/{topic.lower().replace(' ', '_')}_{timestamp}.md"
            )
            with open(output_path, "w") as f:
                f.write(article_content)

            self.logger.info(f"Article saved to: {output_path}")

            # Count citations used
            total_citations = len(
                set(
                    citation
                    for section_data in research_data["sections"].values()
                    for citation in section_data.get("citations", [])
                )
            )

            return {
                "status": "success",
                "file_path": output_path,
                "topic": topic,
                "audience": audience,
                "metadata": {
                    "total_citations": total_citations,
                    "word_count": len(article_content.split()),
                    "generated_at": datetime.now().isoformat(),
                    "model": "anthropic/claude-3-5-sonnet-20240620",
                },
            }

        except Exception as e:
            self.logger.error(f"Error generating article: {str(e)}")
            import traceback

            self.logger.error(traceback.format_exc())
            raise

    def _clean_article_content(self, content: str) -> str:
        """Clean the article content by removing think sections and improving formatting"""
        # Remove any content between <think> tags
        import re

        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)

        # Remove multiple consecutive blank lines
        content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

        # Remove any remaining HTML-like tags
        content = re.sub(r"<[^>]+>", "", content)

        # Ensure consistent heading formatting
        content = re.sub(
            r"^#{1,6}\s*",
            lambda m: m.group(0).rstrip() + " ",
            content,
            flags=re.MULTILINE,
        )

        # Ensure proper spacing around lists
        content = re.sub(r"([^\n])\n- ", r"\1\n\n- ", content)

        # Clean up citation formatting
        content = re.sub(r"\[(\d+)\]", "", content)  # Remove numbered citations

        return content.strip()


async def test_article_writer():
    """Test the article writer with existing research data"""
    try:
        writer = PerplexityArticleWriterWorker()
        print("\n🔄 Testing article writer...")

        result = await writer.execute({})

        if result["status"] == "success":
            print("\n✅ Successfully generated article!")
            print(f"\nArticle saved to: {result['file_path']}")
            print(f"Topic: {result['topic']}")
            print(f"Target audience: {result['audience']}")
            print(f"Total citations: {result['metadata']['total_citations']}")
            print(f"Word count: {result['metadata']['word_count']}")
            print(f"Generated at: {result['metadata']['generated_at']}")
            print(f"Model: {result['metadata']['model']}")

        return result

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_article_writer())
