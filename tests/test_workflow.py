import pytest
from pynions import Workflow, BaseTool


class MockTool(BaseTool):
    async def run(self, data):
        return {"result": data["input"] + " processed"}


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
    
    result = await workflow.run({"input": "test"})
    assert result["result"] == "test processed processed"
