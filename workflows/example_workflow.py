import asyncio
from pynions.core import Workflow, WorkflowStep, Config, DataStore
from pynions.plugins.serper import SerperWebSearch


async def main():
    # Load configuration
    config = Config("config.json")

    # Initialize data store
    data_store = DataStore()

    # Initialize plugins
    serper = SerperWebSearch(config.get_plugin_config("serper"))

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

        # Save results
        data_store.save(results, "serp_analysis")

    except Exception as e:
        print(f"Workflow error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
