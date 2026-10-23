import json
from unittest.mock import Mock

import pytest

from backend.app.services.agents.test_design_agent import (
    TestDesignAgent,
    TestDesignError,
)
from backend.app.schemas.requirements import RequirementsAnalysis
from backend.app.schemas.test_cases import TestDesignOutput


def test_generate_test_cases():

    mock_client = Mock()

    mock_client.generate.return_value = json.dumps({
        "test_cases": [
            {
                "title": "Verify successful login",
                "type": "positive",
                "preconditions": ["A registered customer exists"],
                "steps": [
                    "Open the login page",
                    "Enter valid credentials",
                    "Click Login"
                ],
                "expected_result": "Customer reaches the dashboard"
            }
        ]
    })

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[],
        gaps=[],
        suggested_test_scenarios=[],
    )

    agent = TestDesignAgent(mock_client)

    result = agent.generate(analysis)

    assert result.issue_key == "SHOP-2"
    assert len(result.test_cases) == 1
    assert result.test_cases[0].title == "Verify successful login"
    assert result.test_cases[0].type == "positive"

    mock_client.generate.assert_called_once_with(
        agent.build_prompt(analysis),
        output_schema=TestDesignOutput,
    )


def test_generate_rejects_invalid_json():
    mock_client = Mock()
    mock_client.generate.return_value = "not valid JSON"

    analysis = RequirementsAnalysis(issue_key="SHOP-2")
    agent = TestDesignAgent(mock_client)

    with pytest.raises(TestDesignError):
        agent.generate(analysis)


def test_generate_rejects_invalid_test_type():
    mock_client = Mock()

    mock_client.generate.return_value = json.dumps({
        "test_cases": [
            {
                "title": "Verify login",
                "type": "unknown",
                "steps": ["Click Login"],
                "expected_result": "Login succeeds"
            }
        ]
    })

    analysis = RequirementsAnalysis(issue_key="SHOP-2")
    agent = TestDesignAgent(mock_client)

    with pytest.raises(TestDesignError):
        agent.generate(analysis)