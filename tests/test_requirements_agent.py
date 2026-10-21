import json

import pytest

from unittest.mock import Mock

from backend.app.services.requirements_agent import RequirementsAgent, RequirementsAnalysisError

from pydantic import ValidationError


def test_requirements_agent_build_prompt():
    mock_client = Mock()

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-2",
        "summary": "Customer Login",
        "description": "Users must log in with valid credentials."
    }

    prompt = agent.build_prompt(issue)

    assert "SHOP-2" in prompt
    assert "Customer Login" in prompt
    assert "Users must log in with valid credentials." in prompt
    assert "Identify functional requirements" in prompt
    assert "Identify missing or ambiguous requirements" in prompt

def test_analyze_calls_ollama_client():
    mock_client = Mock()

    mock_client.generate.return_value = """
    {
        "requirements": [
            {
                "description": "Users can log in",
                "category": "functional",
                "source": "explicit"
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-2",
        "summary": "User login",
        "description": "Users can log in using their credentials."
    }

    result = agent.analyze(issue)

    mock_client.generate.assert_called_once_with(
        agent.build_prompt(issue)
    )

    assert result.issue_key == "SHOP-2"
    assert len(result.requirements) == 1
    assert result.requirements[0].description == "Users can log in"
    assert result.requirements[0].category == "functional"

def test_analyze_raises_error_for_invalid_json():
    mock_client = Mock()
    mock_client.generate.return_value = "This is not valid JSON"

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-2",
        "summary": "User login",
        "description": "Users can log in."
    }
    
    with pytest.raises(RequirementsAnalysisError, match="AI returned an invalid requirements analysis"):
        agent.analyze(issue)

def test_analyze_raises_error_for_invalid_schema():
    mock_client = Mock()
    mock_client.generate.return_value = """
    {
        "requirements": [
            {
                "description": "Users can log in"
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-2",
        "summary": "User login",
        "description": "Users can log in."
    }

    with pytest.raises(RequirementsAnalysisError, match="AI returned an invalid requirements analysis"):
        agent.analyze(issue)

def test_analyze_rejects_invalid_requirement_source():
    mock_client = Mock()

    mock_client.generate.return_value = """
    {
        "requirements": [
            {
                "description": "Users can log in",
                "category": "functional",
                "source": "guessed"
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-2",
        "summary": "Customer login",
        "description": "Users can log in using email and password."
    }

    with pytest.raises(RequirementsAnalysisError):
        agent.analyze(issue)