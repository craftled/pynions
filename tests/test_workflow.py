import pytest
from pynions import Workflow, BaseTool


class MockTool(BaseTool):
    async def run(self, data):
        # First try to get the result from previous tool
        input_text = data.get("result", data.get("input", ""))
        return {"result": input_text + " processed"}


@pytest.mark.asyncio
async def test_basic_workflow():
    workflow = Workflow("Test")
    workflow.add(MockTool())

    result = await workflow.run({"input": "test"})
    assert result["result"] == "test processed"


@pytest.mark.asyncio
async def test_workflow_chaining():
    workflow = Workflow("Test Chain")
    workflow.add(MockTool()).add(MockTool())

    # For debugging, let's track each step
    result = await workflow.run({"input": "test"})
    print(f"\nFinal result: {result}")  # This will help us see the actual output

    assert result["result"] == "test processed processed"
