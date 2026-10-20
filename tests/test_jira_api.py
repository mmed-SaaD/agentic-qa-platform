import requests

from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)

def test_get_jira_issue_success():
    fake_issue={
        "key": "SCRUM-6",
        "fields": {
            "summary": "Retrieve Jira issues through the backend",
            "status": {"name": "À faire"},
            "description": "",
        },
    }

    with patch("backend.app.main.JiraClient") as mock_jira_client:
        mock_jira_client.return_value.get_issue.return_value = fake_issue
        
        response = client.get("/jira/issue/SCRUM-6")

        assert response.json() == {
            "key": "SCRUM-6",
            "summary": "Retrieve Jira issues through the backend",
            "status": "À faire",
            "description": "",
        }

        mock_jira_client.return_value.get_issue.assert_called_once_with(
            "SCRUM-6"
        )

def test_get_jira_issue_not_found():
    fake_response = requests.Response()
    fake_response.status_code = 404

    jira_error = requests.exceptions.HTTPError(
        "404 Client Error: Not Found",
        response=fake_response
    )

    with patch("backend.app.main.JiraClient") as mock_jira:
        mock_jira.return_value.get_issue.side_effect = jira_error

        response = client.get("/jira/issue/SCRUM-999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Jira issue not found or unaccessible"
    }

    mock_jira.return_value.get_issue.assert_called_once_with(
        "SCRUM-999999"
    )

def test_get_jira_issue_unauthorized():
    fake_response = requests.Response()
    fake_response.status_code = 401

    jira_error = requests.exceptions.HTTPError(
        "401 Client Error: Unauthorized",
        response = fake_response
    )

    with patch("backend.app.main.JiraClient") as mock_jira:
        mock_jira.return_value.get_issue.side_effect = jira_error

        response = client.get("/jira/issue/SCRUM-6")

        assert response.status_code == 502
        assert response.json() == {
            "detail": "Unable to access jira"
        }

        mock_jira.return_value.get_issue.assert_called_once_with(
        "SCRUM-6"
        )

def test_get_jira_issue_timeout():
    with patch("backend.app.main.JiraClient") as mock_jira:

        mock_jira.return_value.get_issue.side_effect = (
            requests.exceptions.Timeout("Jira request timed out")
        )

        response = client.get("/jira/issue/SCRUM-6")

        assert response.status_code == 502
        assert response.json() == {
            "detail" : "Unable to communicate with Jira"
        }

        mock_jira.return_value.get_issue.assert_called_once_with(
            "SCRUM-6"
        )

def test_get_jira_issue_with_adf_description():
    fake_issue = {
        "key": "SCRUM-6",
        "fields": {
            "summary": "User login",
            "status": {"name": "To Do"},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "Acceptance Criteria:"
                            }
                        ]
                    },
                    {
                        "type": "bulletList",
                        "content": [
                            {
                                "type": "listItem",
                                "content": [
                                    {
                                        "type": "paragraph",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "User can log in."
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }

    with patch("backend.app.main.JiraClient") as mock_jira:
        mock_jira.return_value.get_issue.return_value = fake_issue

        response = client.get("/jira/issue/SCRUM-6")

        assert response.status_code == 200
        assert response.json()["description"] == (
            "Acceptance Criteria:\n"
            "- User can log in.\n"
        )

