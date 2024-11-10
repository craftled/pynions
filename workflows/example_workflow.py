import asyncio
import os
from pynions import Config, DataStore, Workflow, WorkflowStep
from pynions.plugins.serper import SerperWebSearch


async def main():
    # Initialize plugin with minimal config (API key will be loaded from .env)
    serper_config = {"max_results": 20}  # Only non-sensitive configuration

    # Initialize plugin
    serper = SerperWebSearch(serper_config)

    # Create workflow steps
    serp_step = WorkflowStep(
        plugin=serper, name="fetch_serp", description="Fetch top 10 Google results"
    )

    # Create and configure workflow
    workflow = Workflow(
        name="serp_analysis", description="Analyze top 10 Google results for a query"
    )

    workflow.add_step(serp_step)

    # Execute workflow
    try:
        results = await workflow.execute(
            {"query": "best project management software 2024"}
        )

        # Save results using DataStore
        data_store = DataStore()
        data_store.save(results, "serp_analysis")

        # Display results summary
        print("\nAll search results:")
        for i, result in enumerate(results["fetch_serp"]["organic"], 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['link']}")

    except Exception as e:
        print(f"Workflow error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
