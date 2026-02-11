import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.agents.builder import BuilderAgent

@pytest.mark.asyncio
@patch('backend.agents.builder.BuilderAgent.agent_executor')
async def test_build_success(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(return_value={'output': 'Build successful'})
    agent = BuilderAgent()
    result = await agent.build('Build a new feature', {'language': 'python', 'filename': 'new_feature'})
    assert 'output' in result
    assert result['output'] == 'Build successful'

@pytest.mark.asyncio
@patch('backend.agents.builder.BuilderAgent.agent_executor')
async def test_build_failure(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(side_effect=Exception('Build failed'))
    agent = BuilderAgent()
    with pytest.raises(Exception) as excinfo:
        await agent.build('Build a new feature', {'language': 'python', 'filename': 'new_feature'})
    assert 'Build failed' in str(excinfo.value)
