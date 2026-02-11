import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.agents.toolsmith import ToolsmithAgent

@pytest.mark.asyncio
@patch('backend.agents.toolsmith.ToolsmithAgent.agent_executor')
async def test_create_tool_success(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(return_value={'output': 'Tool created'})
    agent = ToolsmithAgent()
    result = await agent.create_tool('Create a tool for parsing JSON')
    assert 'output' in result
    assert result['output'] == 'Tool created'

@pytest.mark.asyncio
@patch('backend.agents.toolsmith.ToolsmithAgent.agent_executor')
async def test_create_tool_failure(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(side_effect=Exception('Tool creation failed'))
    agent = ToolsmithAgent()
    with pytest.raises(Exception) as excinfo:
        await agent.create_tool('Create a tool for parsing JSON')
    assert 'Tool creation failed' in str(excinfo.value)
