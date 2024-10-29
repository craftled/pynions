import pytest
import asyncio
from pynions import Flow, State
from datetime import datetime


class TestState(State):
    value: str = ""
    processed: bool = False


class TestFlow(Flow[TestState]):
    async def run(self):
        async with self.step("process"):
            self.state.processed = True
            return {"status": "success"}


@pytest.mark.asyncio
async def test_basic_flow():
    """Test basic flow execution"""
    flow = TestFlow(value="test")
    result = await flow.run()

    assert result["status"] == "success"
    assert flow.state.processed == True
    assert isinstance(flow.get_duration(), float)


@pytest.mark.asyncio
async def test_cache():
    """Test API calling with cache"""

    async def mock_api():
        await asyncio.sleep(0.1)
        return {"data": "test"}

    flow = TestFlow()

    # First call
    result1 = await flow.call_api("test", mock_api)

    # Second call (should be cached)
    result2 = await flow.call_api("test", mock_api)

    assert result1 == result2
