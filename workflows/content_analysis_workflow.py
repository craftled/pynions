import asyncio
import os
from typing import Dict, Any, List
from pynions import Config, DataStore, Workflow, WorkflowStep
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader
from pynions.plugins.litellm_plugin import LiteLLM
from datetime import datetime


async def content_analysis_workflow(keyword: str):
    """Analyze top ranking content and create an outline"""
    try:
        print(f"\n🔍 Analyzing content for: {keyword}")

        # Initialize plugins
        serper = SerperWebSearch({"max_results": 10})
        jina = JinaAIReader()
        llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 2000,
            }
        )

        # Create workflow steps
        search_step = WorkflowStep(
            plugin=serper, name="search", description="Find top 10 ranking pages"
        )

        # Create workflow
        workflow = Workflow(
            name="content_analysis", description="Analyze top ranking content"
        )
        workflow.add_step(search_step)

        # Execute search
        print("\n1️⃣ Searching for top ranking pages...")
        results = await workflow.execute({"query": keyword})

        if not results.get("search", {}).get("organic"):
            raise ValueError("No search results found")

        # Extract content from each URL
        print("\n2️⃣ Extracting content from URLs...")
        contents = []
        for idx, result in enumerate(results["search"]["organic"][:10], 1):
            url = result.get("link")
            print(f"\n   Processing {idx}/10: {url}")
            try:
                print("   🔄 Calling Jina AI Reader...")
                content = await jina.execute({"url": url})

                if content is None:
                    print("   ⚠️ No response from Jina AI")
                    continue

                if content.get("content"):
                    print(f"   ✅ Successfully extracted content:")
                    print(f"      - Title: {content.get('title', 'No title')[:50]}...")
                    print(
                        f"      - Content length: {len(content['content'])} characters"
                    )
                    contents.append(
                        {
                            "url": url,
                            "title": content.get("title", "No title"),
                            "content": content.get("content", ""),
                        }
                    )
                else:
                    print("   ⚠️ No content found in the response")

            except asyncio.TimeoutError:
                print(f"   ❌ Timeout error while extracting from {url}")
            except Exception as e:
                print(f"   ❌ Error extracting content: {str(e)}")
                continue

        # Analyze content and create outline
        print("\n3️⃣ Creating content outline...")
        analysis_prompt = f"""
        Analyze these {len(contents)} articles about "{keyword}" and create a detailed outline for a better article.
        
        Key points to consider:
        1. What topics are commonly covered?
        2. What unique angles are missing?
        3. What makes the top-ranking content successful?
        
        Format the response as:
        1. Content Gap Analysis
        2. Recommended Outline
        3. Key Differentiators
        """

        outline = await llm.execute(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": analysis_prompt
                        + "\n\nArticles to analyze:\n"
                        + "\n".join(
                            [
                                f"- {c['title']}: {c['content'][:500]}..."
                                for c in contents
                            ]
                        ),
                    }
                ]
            }
        )

        # Save results
        data_store = DataStore()
        data_store.save(
            {
                "keyword": keyword,
                "search_results": results["search"],
                "analyzed_content": contents,
                "outline": outline,
            },
            f"content_analysis_{keyword.replace(' ', '_')}",
        )

        print("\n✅ Analysis complete! Results saved to data store.")
        print("\n📋 Content Outline:")
        print("-" * 50)
        print(outline.get("content", "No outline generated"))

        # After creating the outline
        markdown_file = await save_markdown_brief(
            {
                "keyword": keyword,
                "analyzed_content": contents,
                "outline": outline,
                "search_results": results["search"],
            },
            keyword,
        )

        print(f"\n📝 Content brief saved to: {markdown_file}")

        return outline

    except Exception as e:
        print(f"\n❌ Workflow error: {str(e)}")
        return None


async def save_markdown_brief(data: Dict, keyword: str):
    """Save content brief as markdown with research citations"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"briefs/{keyword.replace(' ', '_')}_{timestamp}.md"

    # Create briefs directory if it doesn't exist
    os.makedirs("briefs", exist_ok=True)

    markdown_content = f"""# Content Brief: {keyword}

## Research Summary

### Top Ranking Content
{'-' * 50}
"""

    # Add top ranking URLs with titles
    for idx, content in enumerate(data["analyzed_content"], 1):
        markdown_content += f"\n{idx}. [{content['title']}]({content['url']}) - {len(content['content'])} chars"

    markdown_content += f"\n\n## Content Outline\n{'-' * 50}\n"

    # Add the outline with inline citations
    outline = data["outline"]["content"]

    # Add citations to outline by referencing source URLs
    for idx, content in enumerate(data["analyzed_content"], 1):
        cite_text = f"[{idx}]({content['url']})"
        outline = outline.replace(f"Example {idx}:", f"Example {cite_text}:")

    markdown_content += outline

    # Add research data
    markdown_content += "\n\n## Research Data\n"
    markdown_content += f"\n### Search Metrics\n{'-' * 50}\n"
    markdown_content += f"- Total sources analyzed: {len(data['analyzed_content'])}\n"
    markdown_content += f"- Average content length: {sum(len(c['content']) for c in data['analyzed_content']) // len(data['analyzed_content'])} characters\n"

    # Save markdown file
    with open(filename, "w") as f:
        f.write(markdown_content)

    return filename


if __name__ == "__main__":
    # Test the workflow
    keyword = input("\n📝 Enter a keyword to analyze: ")
    asyncio.run(content_analysis_workflow(keyword))
