import json

import pytest

from unittest.mock import Mock

from backend.app.schemas.requirements import Requirement, RequirementsAIOutput, RequirementsAnalysis

from backend.app.services.agents.requirements_agent import RequirementsAgent, RequirementsAnalysisError

from backend.app.utils.evidence_validator import validate_requirement_evidence

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
                "description": "Registered customers can log in using email and password.",
                "category": "functional",
                "source": "explicit",
                "evidence": "Registered customers can log in using email and password."
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    agent = RequirementsAgent(mock_client)

    issue = {
        "key": "SHOP-99",
        "summary": "Customer login",
        "description": "Registered customers can log in using email and password."
    }

    result = agent.analyze(issue)

    mock_client.generate.assert_called_once_with(
        agent.build_prompt(issue),
        output_schema=RequirementsAIOutput
    )

    assert result.issue_key == "SHOP-99"
    assert len(result.requirements) == 1
    assert result.requirements[0].description == "Registered customers can log in using email and password."
    assert result.requirements[0].category == "functional"
    assert result.requirements[0].source == "explicit"
    assert result.requirements[0].evidence == "Registered customers can log in using email and password."

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

def test_analyze_accepts_structurally_valid_evidence():
    mock_client = Mock()

    mock_client.generate.return_value = """
    {
        "requirements": [
            {
                "description": "Users must enable MFA",
                "category": "security",
                "source": "explicit",
                "evidence": "Users must enable MFA"
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    issue = {
        "key": "SHOP-2",
        "summary": "Customer login",
        "description": "Users can log in with email and password."
    }

    agent = RequirementsAgent(mock_client)

    result = agent.analyze(issue)

    assert result.issue_key == "SHOP-2"
    assert len(result.requirements) == 1
    assert result.requirements[0].description == "Users must enable MFA"
    assert result.requirements[0].source == "explicit"

def test_analyze_accepts_inferred_requirement():
    mock_client = Mock()

    mock_client.generate.return_value = """
    {
        "requirements": [
            {
                "description": "The system should limit repeated failed login attempts.",
                "category": "security",
                "source": "inferred",
                "evidence": null
            }
        ],
        "gaps": [],
        "suggested_test_scenarios": []
    }
    """

    issue = {
        "key": "SHOP-99",
        "summary": "Customer login",
        "description": "Registered customers can log in using email and password."
    }

    agent = RequirementsAgent(mock_client)

    result = agent.analyze(issue)

    assert result.issue_key == "SHOP-99"
    assert len(result.requirements) == 1

    requirement = result.requirements[0]

    assert requirement.source == "inferred"
    assert requirement.evidence is None
    assert requirement.category == "security"

    mock_client.generate.assert_called_once_with(
        agent.build_prompt(issue),
        output_schema=RequirementsAIOutput
    )

def test_rejects_inferred_requirement_with_evidence():
    issue = {
        "summary": "Customer login",
        "description": "Users can log in using email and password."
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-99",
        requirements=[
            Requirement(
                description="The system should limit failed login attempts.",
                category="security",
                source="inferred",
                evidence="Users can log in using email and password."
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="Inferred requirement must not contain evidence"
    ):
        validate_requirement_evidence(analysis, issue)