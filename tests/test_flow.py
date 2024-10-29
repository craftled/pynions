import pytest
from pynions.workflow import Flow


async def test_basic_flow():
    async def step1(data):
        return {"step1": "done"}

    async def step2(data):
        return {"step2": data["step1"] + " and more"}

    flow = Flow()
    flow.add_step(step1)
    flow.add_step(step2)

    result = await flow.run()
    assert result["step1"] == "done"
    assert result["step2"] == "done and more"


async def test_flow_with_initial_data():
    async def step1(data):
        return {"result": data["input"] + " processed"}

    flow = Flow()
    flow.add_step(step1)

    result = await flow.run({"input": "test"})
    assert result["result"] == "test processed"
