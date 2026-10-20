from unittest.mock import Mock

from backend.app.services.requirements_agent import RequirementsAgent


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

    mock_client.generate.return_value = "AI analysis result"

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


