import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from backend.agents.scoring_agent import ScoringAgent

@pytest.mark.asyncio
async def test_score_code_valid_function():
    agent = ScoringAgent()
    code = """
def add(a, b):
    return a + b
"""
    # Assuming score_code is sync, wrap in async
    result = await asyncio.to_thread(agent.score_code, code)
    assert result['criteria_scores']['functionality'] > 0
    assert 'issues' in result

@pytest.mark.asyncio
async def test_score_code_syntax_error():
    agent = ScoringAgent()
    code = """
def broken_func(
    print("missing closing parenthesis")
"""
    result = await asyncio.to_thread(agent.score_code, code)
    assert any('Syntax error' in issue[1] for issue in result['issues'])

@pytest.mark.asyncio
@patch('backend.agents.scoring_agent.ScoringAgent.score_code', new_callable=AsyncMock)
async def test_score_code_mocked_llm(mock_score):
    mock_score.return_value = {
        'criteria_scores': {'functionality': 3.0, 'code_quality': 2.0},
        'issues': [],
        'total_score': 5.0
    }
    agent = ScoringAgent()
    result = await agent.score_code('def foo(): pass')
    assert result['total_score'] == 5.0
