import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

jira_url = os.getenv("JIRA_BASE_URL")
jira_email = os.getenv("JIRA_EMAIL")
jira_api_token = os.getenv("JIRA_API_TOKEN")

if not all([jira_url, jira_email, jira_api_token]):
    raise RuntimeError("Missing required Jira environment variables !")

issue_key = "SCRUM-6"

#JIRA Cloud REST API endpoint
endpoint = f"{jira_url.rstrip('/')}/rest/api/3/issue/{issue_key}"

params = {
    "fields" : "summary,status,description"
}

response = requests.get(
    endpoint,
    auth=HTTPBasicAuth(jira_email, jira_api_token),
    headers={"Accept": "application/json"},
    params=params,
    timeout=15,
)

print("HTTP status code:", response.status_code)

if response.status_code == 200:
    issue = response.json()

    print("Issue key:", issue["key"])
    print("Summary:", issue["fields"]["summary"])
    print("Status:", issue["fields"]["status"]["name"])
    print("Description:", issue["fields"]["description"])

else:
    print("Jira request failed.")
    print("Check your credentials, site URL, and issue permissions.")