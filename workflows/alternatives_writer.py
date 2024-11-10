import asyncio
import logging
from pynions.core import Workflow, WorkflowStep
from pynions.plugins.serper import SerperWebSearch
from pynions.plugins.jina import JinaAIReader
from pynions.plugins.litellm_plugin import LiteLLM
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def verify_company_data(domain: str, data_type: str) -> dict:
    """Verify specific data from company website using targeted search"""
    print(f"\n🔍 Verifying {data_type} data for {domain}")

    search_queries = {
        "pricing": f"site:{domain} pricing",
        "features": f"site:{domain} features",
        "integrations": f"site:{domain} integrations",
        "about": f"site:{domain} about",
    }

    serper = SerperWebSearch({"max_results": 5})
    jina = JinaAIReader()

    print(f"   Searching: {search_queries[data_type]}")
    results = await serper.execute({"query": search_queries[data_type]})
    verified_data = []

    for idx, result in enumerate(results.get("organic", []), 1):
        url = result["link"]
        print(f"   Processing {idx}/5: {url}")

        try:
            content = await jina.execute({"url": url})
            if content and content.get("content"):
                print(f"   ✅ Content extracted: {len(content['content'])} characters")
                verified_data.append({"url": url, "content": content["content"]})
            else:
                print("   ⚠️ No content extracted")
        except Exception as e:
            print(f"   ❌ Error extracting content: {str(e)}")
            continue

    return {"domain": domain, "data_type": data_type, "sources": verified_data}


async def brand_alternatives_workflow(brand: str, number_of_items: int = 5):
    """Research and verify alternatives to a specific brand"""
    print(f"\n🔎 Starting research for {brand} alternatives")
    print(f"📊 Looking for top {number_of_items} alternatives")
    print("-" * 50)

    try:
        # Step 1: Initial SERP research
        print("\n1️⃣ Performing initial search...")
        workflow = Workflow(name="brand_alternatives")
        workflow.add_step(
            WorkflowStep(
                plugin=SerperWebSearch({"max_results": 10}),
                name="initial_search",
                description=f"Search for {brand} alternatives",
            )
        )

        results = await workflow.execute(
            {"query": f"best {brand} alternatives {datetime.now().year}"}
        )

        # Step 2: Extract alternatives
        print("\n2️⃣ Analyzing search results...")
        llm = LiteLLM(
            {
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_tokens": 1000,
            }
        )

        alternatives_prompt = f"""
        Based on the search results, identify the top {number_of_items} most mentioned alternatives to {brand}.
        Return only the domain names (e.g., klaviyo.com) in a comma-separated list.
        """

        alternatives_response = await llm.execute(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": alternatives_prompt
                        + "\n\nSearch results:\n"
                        + str(results.get("initial_search", {})),
                    }
                ]
            }
        )

        # Step 3: Verify data for each alternative
        print("\n3️⃣ Verifying data for each alternative...")
        alternatives = alternatives_response["content"].split(",")
        verified_data = {}

        for domain in alternatives:
            domain = domain.strip()
            print(f"\n📌 Processing {domain}")
            verified_data[domain] = {}

            for data_type in ["pricing", "features", "integrations", "about"]:
                verified_data[domain][data_type] = await verify_company_data(
                    domain, data_type
                )

        print("\n✅ Research complete!")
        return verified_data

    except Exception as e:
        print(f"\n❌ Workflow error: {str(e)}")
        logger.error(f"Workflow failed: {str(e)}")
        return None


if __name__ == "__main__":
    brand = input("Enter brand name to research: ")
    number_of_items = int(input("Number of alternatives to find: "))

    results = asyncio.run(
        brand_alternatives_workflow(brand=brand, number_of_items=number_of_items)
    )
