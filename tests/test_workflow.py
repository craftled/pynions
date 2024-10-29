import pytest
from pynions import Workflow, BaseTool


class MockTool(BaseTool):
    async def run(self, data):
        input_text = data.get("result", data.get("input", ""))
        return {"result": input_text + " processed"}


@pytest.mark.asyncio
async def test_basic_workflow():
    workflow = Workflow("Test", debug=True)
    workflow.add(MockTool())

    result = await workflow.run({"input": "test"})
    assert result["result"] == "test processed"


@pytest.mark.asyncio
async def test_workflow_chaining():
    workflow = Workflow("Test Chain", debug=True)
    workflow.add(MockTool()).add(MockTool())

    result = await workflow.run({"input": "test"})
    assert result["result"] == "test processed processed"
