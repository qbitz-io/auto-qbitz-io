import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.agents.planner import PlannerAgent

@pytest.mark.asyncio
@patch('backend.agents.planner.PlannerAgent.agent_executor')
async def test_plan_success(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(return_value={'output': 'Plan created'})
    agent = PlannerAgent()
    result = await agent.plan('Create a new feature')
    assert 'output' in result
    assert result['output'] == 'Plan created'

@pytest.mark.asyncio
@patch('backend.agents.planner.PlannerAgent.agent_executor')
async def test_plan_failure(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(side_effect=Exception('Planning failed'))
    agent = PlannerAgent()
    with pytest.raises(Exception) as excinfo:
        await agent.plan('Create a new feature')
    assert 'Planning failed' in str(excinfo.value)
