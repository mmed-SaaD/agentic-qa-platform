import requests

from fastapi import FastAPI, HTTPException

from backend.app.services.jira_client import JiraClient

from backend.app.utils.adf_parser import extract_text_from_adf

from backend.app.schemas.requirements import RequirementsAnalysis

from backend.app.services.ollama_client import OllamaClient
from backend.app.services.requirements_agent import RequirementsAgent, RequirementsAnalysisError


app = FastAPI(
    title="Agentic QA Platform",
    description="AI-assisted Quality Engineering Platform",
    version="0.1.0"
)

@app.get("/")
def root():
    return{
        "message" : "Welcome to the Agentic QA Platform"
    }

@app.get("/health")
def health_check():
    return{
        "status" : "healthy",
        "service" : "agentic-qa-platform"
    }

def fetch_jira_issue(issue_key: str) -> dict:
    client = JiraClient()
    issue = client.get_issue(issue_key)

    return {
        "key": issue["key"],
        "summary": issue["fields"]["summary"],
        "status": issue["fields"]["status"]["name"],
        "description": extract_text_from_adf(
            issue["fields"]["description"]
        ),
    }

@app.get("/jira/issue/{issue_key}")
def get_jira_issue(issue_key: str):
    try: 
        return fetch_jira_issue(issue_key)

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code

        if status_code in(401,403):
            raise HTTPException(
                status_code = 502,
                detail = "Unable to access jira"
            ) from error

        if status_code == 404:
            raise HTTPException(
                status_code = 404,
                detail = "Jira issue not found or unaccessible"
            ) from error

        raise HTTPException(
            status_code = 502,
            detail = "Jira returned an error"
        ) from error

    except requests.exceptions.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail="Unable to communicate with Jira"
        ) from error

@app.post(
    "/ai/requirements/analyze/{issue_key}",
    response_model=RequirementsAnalysis 
)
def analyze_jira_requirements(issue_key: str):
    try:
        issue = fetch_jira_issue(issue_key)

        ollama_client = OllamaClient()
        agent = RequirementsAgent(ollama_client)

        return agent.analyze(issue)
    
    except RequirementsAnalysisError as error:
        raise HTTPException(
            status_code=502,
            detail="AI returned an invalid requirements analysis"
        ) from error