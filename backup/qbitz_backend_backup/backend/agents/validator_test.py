import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.agents.validator import ValidatorAgent

@pytest.mark.asyncio
@patch('backend.agents.validator.ValidatorAgent.agent_executor')
async def test_validate_success(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(return_value={'output': 'Validation passed'})
    agent = ValidatorAgent()
    result = await agent.validate()
    assert 'output' in result
    assert result['output'] == 'Validation passed'

@pytest.mark.asyncio
@patch('backend.agents.validator.ValidatorAgent.agent_executor')
async def test_validate_failure(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(side_effect=Exception('Validation failed'))
    agent = ValidatorAgent()
    with pytest.raises(Exception) as excinfo:
        await agent.validate()
    assert 'Validation failed' in str(excinfo.value)

@pytest.mark.asyncio
@patch('backend.agents.validator.ValidatorAgent.agent_executor')
async def test_validate_file_success(mock_agent_executor):
    mock_agent_executor.ainvoke = AsyncMock(return_value={'output': 'File validation passed'})
    agent = ValidatorAgent()
    result = await agent.validate_file('backend/agents/builder.py')
    assert 'output' in result
    assert result['output'] == 'File validation passed'
