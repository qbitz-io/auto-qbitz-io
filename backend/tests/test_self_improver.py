import asyncio
import pytest
from backend.agents.self_improver import SelfImproverAgent

@pytest.mark.asyncio
async def test_self_improver_improve_basic():
    agent = SelfImproverAgent()
    task = "Check system for any broken components and propose fixes."
    result = await agent.improve(task)
    assert isinstance(result, dict)
    assert "output" in result

@pytest.mark.asyncio
async def test_self_improver_improve_with_context():
    agent = SelfImproverAgent()
    task = "Generate tests for new capabilities."
    context = {"extra_info": "Test context data"}
    result = await agent.improve(task, context)
    assert isinstance(result, dict)
    assert "output" in result


if __name__ == "__main__":
    asyncio.run(test_self_improver_improve_basic())
    asyncio.run(test_self_improver_improve_with_context())
