import pytest

from unittest.mock import Mock, patch
from requests.exceptions import HTTPError
from requests.exceptions import Timeout

from backend.app.services.ollama_client import OllamaClient

from backend.app.schemas.requirements import RequirementsAIOutput


@patch("backend.app.services.ollama_client.requests.post")
def test_generate_returns_ai_response(mock_post):
    mock_response = mock_post.return_value

    mock_response.json.return_value = {
        "response": "Test login with an invalid password."
    }

    client = OllamaClient()

    result = client.generate("Suggest one negative login test.")

    assert result == "Test login with an invalid password."

    mock_post.assert_called_once_with(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:1.7b",
            "prompt": "Suggest one negative login test.",
            "stream": False,
            "think": False,
        },
        timeout=180,
    )

@patch("backend.app.services.ollama_client.requests.post")
def test_generate_raises_error_on_http_failure(mock_post):
    mock_response = mock_post.return_value

    mock_response.raise_for_status.side_effect = HTTPError(
        "500 server error"
    )

    client = OllamaClient()

    with pytest.raises(HTTPError):
        client.generate("Analyze this Jira story.")

    mock_response.raise_for_status.assert_called_once()

@patch("backend.app.services.ollama_client.requests.post")
def test_generate_raises_error_on_timeout(mock_post):
    mock_post.side_effect = Timeout(
        "Ollama did not respond in time."
    )

    client = OllamaClient()

    with pytest.raises(Timeout):
        client.generate("Analyze SHOP-2.")

    mock_post.assert_called_once()

def test_generate_sends_json_schema():
    client = OllamaClient()

    mock_response = Mock()
    mock_response.json.return_value = {
        "response": '{"requirements":[],"gaps":[],"suggested_test_scenarios":[]}'
    }

    with patch(
        "backend.app.services.ollama_client.requests.post"
    ) as mock_post:

        mock_post.return_value = mock_response

        result = client.generate(
            "Analyze this Jira story",
            output_schema=RequirementsAIOutput
        )

    payload = mock_post.call_args.kwargs["json"]

    assert payload["format"] == RequirementsAIOutput.model_json_schema()
    assert payload["stream"] is False
    assert result == mock_response.json.return_value["response"]

def test_generate_without_schema():
    client = OllamaClient()

    mock_response = Mock()
    mock_response.json.return_value = {
        "response": "Hello!"
    }

    with patch(
        "backend.app.services.ollama_client.requests.post"
    ) as mock_post:

        mock_post.return_value = mock_response

        result = client.generate("Say hello")

    payload = mock_post.call_args.kwargs["json"]

    assert "format" not in payload
    assert payload["prompt"] == "Say hello"
    assert payload["stream"] is False
    assert result == "Hello!"

    mock_post.assert_called_once_with(
        f"{client.base_url}/api/generate",
        json=payload,
        timeout=180
    )
