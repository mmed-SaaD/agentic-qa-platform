import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

class JiraClient:
    def __init__(self):
        self.jira_base_url = os.getenv("JIRA_BASE_URL")
        self.jira_email = os.getenv("JIRA_EMAIL")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN")

        if not all([self.jira_base_url, self.jira_email, self.jira_api_token]):
            raise RuntimeError("Missing required jira configuration")

        self.jira_base_url = self.jira_base_url.rstrip("/")

    def get_issue(self, issue_key):
        endpoint = f"{self.jira_base_url}/rest/api/3/issue/{issue_key}"

        response = requests.get(
            endpoint,
            auth=HTTPBasicAuth(self.jira_email, self.jira_api_token),
            headers={"Accept" : "application/json"},
            params={"fields" : "summary,status,description"},
            timeout=10
        )

        response.raise_for_status()

        return response.json()
