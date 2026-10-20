import pytest

from unittest.mock import patch
from requests.exceptions import HTTPError
from requests.exceptions import Timeout

from backend.app.services.ollama_client import OllamaClient


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
            "model": "qwen3:4b",
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
