# Backend Agents Tests Documentation

## Overview

This directory contains asynchronous tests for backend agents, including the ScoringAgent and others.

## Test Setup

- Tests are written using `pytest` with `pytest-asyncio` for async support.
- The `unittest.mock` library is used for mocking asynchronous methods.
- Tests are located in files named `*_test.py`.

## Mocking Approach

- Use `unittest.mock.patch` to replace async methods with `AsyncMock` for controlled return values.
- This allows testing of agent behavior without invoking real external dependencies or LLM calls.

Example:
```python
from unittest.mock import AsyncMock, patch

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
```

## Running the Async Tests

1. Ensure you have the backend dependencies installed, including `pytest` and `pytest-asyncio`.

2. From the `backend` directory, run:

```bash
pytest -v --asyncio-mode=auto
```

3. This will discover and run all tests, including async tests.

4. Review the output for pass/fail status.

## Notes

- Async tests use `pytest.mark.asyncio` decorator.
- Some synchronous methods are wrapped with `asyncio.to_thread` to run asynchronously in tests.

---

This documentation helps maintainers and contributors understand the test infrastructure and how to extend or run tests effectively.