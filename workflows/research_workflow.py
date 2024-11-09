from pynions import Workflow, WorkflowStep, DataStore
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader
from datetime import datetime
import os
from urllib.parse import urlparse


async def save_markdown_brief(data: dict, keyword: str) -> str:
    """Save research results as a markdown brief"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = "research_briefs"
    os.makedirs(folder_name, exist_ok=True)

    filename = os.path.join(folder_name, f"{keyword.replace(' ', '_')}_{timestamp}.md")

    # Extract domains from URLs
    domains = [
        urlparse(result["link"]).netloc for result in data["search"]["organic"][:3]
    ]

    with open(filename, "w", encoding="utf-8") as f:
        # Header
        f.write(f"# Research Brief: {keyword}\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Research Summary
        f.write("## Research Summary\n\n")
        f.write(f"- Total Results Analyzed: {len(data['search']['organic'])}\n")
        f.write(f"- Top Domains: {', '.join(domains)}\n\n")

        # SERP Analysis
        f.write("## SERP Analysis\n\n")
        if "peopleAlsoAsk" in data["search"]:
            f.write("### People Also Ask\n")
            for question in data["search"]["peopleAlsoAsk"]:
                f.write(f"- {question['question']}\n")
            f.write("\n")

        if "relatedSearches" in data["search"]:
            f.write("### Related Searches\n")
            for search in data["search"]["relatedSearches"]:
                f.write(f"- {search['query']}\n")
            f.write("\n")

        # Detailed Content Analysis
        f.write("## Detailed Content Analysis\n\n")
        for result in data["search"]["organic"]:
            f.write(f"### {result['title']}\n")
            f.write(f"- URL: {result['link']}\n")
            f.write(f"- Snippet: {result['snippet']}\n")

            if result.get("content"):
                f.write("\n#### Key Content:\n")
                # Clean and format the content
                content = result["content"].replace("\n\n\n", "\n\n").strip()
                f.write(f"{content}\n\n")
                f.write("-" * 50 + "\n\n")

        return filename


async def research_workflow(keyword: str, max_results: int = 5):
    """Research workflow combining SERP data and content extraction"""
    print(f"\n🔍 Researching: {keyword}")
    print("-" * 50)

    # Initialize plugins and data store
    serper = SerperWebSearch({"max_results": max_results})
    jina = JinaAIReader()
    data_store = DataStore()

    # Create workflow
    workflow = Workflow(
        name="research", description="Research and content extraction workflow"
    )
    workflow.add_step(
        WorkflowStep(
            plugin=serper, name="search", description="Search for relevant content"
        )
    )

    # Execute search
    results = await workflow.execute({"query": keyword})

    # Extract content from URLs
    print("\n📄 Extracting content from URLs...")
    for idx, result in enumerate(results["search"]["organic"], 1):
        url = result.get("link")
        print(f"\n   Processing {idx}/{max_results}: {url}")

        content = await jina.execute({"url": url})
        if content and content.get("content"):
            result["content"] = content["content"]
            print(f"   ✅ Content extracted: {len(content['content'])} characters")
        else:
            print("   ⚠️ No content extracted")

    # Save results
    data_store.save(results, f"research_{keyword.replace(' ', '_')}")

    # Generate markdown brief
    brief_file = await save_markdown_brief(results, keyword)
    print(f"\n📝 Research brief saved to: {brief_file}")

    return results


async def test_research(keyword: str = "best project management software 2024"):
    """Test the research workflow"""
    results = await research_workflow(keyword)

    if results:
        print("\n📊 Research Summary:")
        print(f"Total Results: {len(results['search']['organic'])}")

        print("\n📑 Top Results:")
        for result in results["search"]["organic"]:
            print(f"\n{result.get('position')}. {result.get('title')}")
            print(f"   URL: {result.get('link')}")
            print(f"   Snippet: {result.get('snippet')[:200]}...")
            print("-" * 30)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_research())
