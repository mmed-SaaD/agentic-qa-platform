# Agentic QA Platform

**An AI-powered Quality Assurance platform combining test automation, Jira integration, and intelligent QA workflows.**

## Overview

Agentic QA Platform is a portfolio project designed to explore how AI agents can support the software testing lifecycle, from requirements analysis to test generation, execution, failure investigation, and defect reporting.

The project is being developed incrementally using Python, FastAPI, Pytest, Jira Cloud, and modern DevOps practices.

The long-term goal is to build a modular QA engineering platform in which AI agents assist human testers while maintaining traceability, test reliability, and human oversight.

> **Project status:** Early development — FastAPI foundation and Jira Cloud connectivity implemented. AI agents and advanced QA workflows are planned.

## Features

### Implemented

- FastAPI backend with root and health-check endpoints.
- Automated API health tests using Pytest.
- Secure Jira Cloud authentication using environment variables.
- Jira REST API v3 integration.
- Reusable `JiraClient` class for retrieving Jira issues.
- Retrieval of Jira issue keys, summaries, statuses, and descriptions.
- HTTP error detection using `raise_for_status()`.
- Initial Jira project management structure with Epics, Stories, and Tasks.

### In Progress

- Exposing Jira issue retrieval through FastAPI.
- Mapping Jira HTTP errors to appropriate backend responses.
- Automated unit tests for the Jira integration.
- Structured processing of Jira issue descriptions.

### Planned

- AI-assisted requirements analysis.
- AI-generated test scenarios and test cases.
- Automated UI and API test execution.
- AI-assisted failure analysis and defect triage.
- Jira bug-report creation with human approval.
- Requirements-to-tests traceability.
- Test execution reporting and release risk assessment.
- GitHub Actions CI/CD integration.
- PostgreSQL persistence.
- Web dashboard.
- Docker-based deployment.
- AI agent evaluation and observability.

## Technology Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Backend | FastAPI, Uvicorn |
| HTTP integration | Requests |
| Configuration | python-dotenv |
| Testing | Pytest, FastAPI TestClient |
| Test automation (planned) | Playwright |
| AI orchestration (planned) | LangGraph |
| Database (planned) | PostgreSQL |
| Containerization (planned) | Docker |
| CI/CD (planned) | GitHub Actions |
| Project management | Jira Cloud |
| Version control | Git, GitHub |

## Architecture

The platform follows a modular architecture that separates API endpoints, external integrations, automated testing, and future AI-agent workflows.

```text
                    User / Dashboard
                           |
                           v
                    FastAPI Backend
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
         Services       AI Agents     Test Engine
             |          (planned)      (planned)
             v
         JiraClient
             |
             v
       Jira Cloud REST API
```

### Architectural Responsibilities

**FastAPI Backend**

Receives HTTP requests, exposes application functionality, validates inputs, and returns structured API responses.

**Services**

Encapsulate communication with external systems. The Jira service manages authentication, API requests, and HTTP error detection.

**AI Agents (Planned)**

Will analyze requirements, propose tests, investigate failures, and assist with QA decisions using controlled tools and human approval.

**Test Engine (Planned)**

Will execute automated tests and collect results for reporting and analysis.

## Project Structure

```text
agentic-qa-platform/
├── backend/
│   └── app/
│       ├── main.py
│       └── services/
│           ├── __init__.py
│           └── jira_client.py
│
├── scripts/
│   └── test_jira_connection.py
│
├── tests/
│   └── test_health.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

The `.env` file is created locally and excluded from version control.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- A Jira Cloud account for Jira integration
- An Atlassian API token

### 1. Clone the Repository

```bash
git clone git@github.com:mmed-SaaD/agentic-qa-platform.git
cd agentic-qa-platform
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
JIRA_BASE_URL=https://your-site.atlassian.net
JIRA_EMAIL=your-atlassian-email@example.com
JIRA_API_TOKEN=your-api-token
```

Never commit your `.env` file, API tokens, or passwords.

### 5. Start the Backend

```bash
python -m uvicorn backend.app.main:app --reload
```

The backend runs locally at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description | Status |
|---|---|---|---|
| GET | `/` | Welcome message | Implemented |
| GET | `/health` | Application health check | Implemented |
| GET | `/jira/issues/{issue_key}` | Retrieve a Jira issue | In progress |

### Example Health Response

```json
{
  "status": "healthy",
  "service": "agentic-qa-platform"
}
```

### Planned Jira Issue Response

```json
{
  "key": "SCRUM-6",
  "summary": "Retrieve Jira issues through the backend",
  "status": "À faire",
  "description": {
    "type": "doc",
    "version": 1,
    "content": []
  }
}
```

Jira Cloud API v3 uses Atlassian Document Format (ADF) for rich-text descriptions. The example above abbreviates the description content.

## Jira Integration

The Jira integration uses the Jira Cloud REST API v3 with authenticated HTTPS requests.

The `JiraClient` service currently supports retrieving individual Jira issues.

Example:

```python
from backend.app.services.jira_client import JiraClient

client = JiraClient()
issue = client.get_issue("SCRUM-6")

print(issue["key"])
print(issue["fields"]["summary"])
```

The integration uses environment variables for credentials, an HTTP request timeout, and `raise_for_status()` for detecting HTTP errors.

A live connection to Jira Cloud has been verified with HTTP `200 OK`.

## Testing

The project uses Pytest for automated testing.

Run the test suite from the project root:

```bash
python -m pytest -v
```

The initial FastAPI health-check tests have passed.

Upcoming test coverage will include:

- Successful Jira issue retrieval.
- Nonexistent or inaccessible Jira issues.
- Authentication failures.
- Network errors and timeouts.
- Response validation.
- Verification that credentials are not exposed.

Jira integration unit tests will use mocked HTTP responses to avoid depending on external services.

## Development Roadmap

### Phase 1 — Project Foundation

- [x] Initialize Git repository.
- [x] Configure Python virtual environment.
- [x] Create FastAPI application.
- [x] Implement health-check endpoint.
- [x] Add initial Pytest tests.
- [x] Publish repository to GitHub.

### Phase 2 — Jira Integration

- [x] Create Jira Scrum space.
- [x] Define Epic, Story, and Task.
- [x] Configure secure API authentication.
- [x] Verify live Jira API connectivity.
- [x] Create reusable JiraClient.
- [ ] Expose Jira integration through FastAPI.
- [ ] Implement automated Jira client tests.
- [ ] Parse Atlassian Document Format.
- [ ] Add Jira issue creation and update capabilities.

### Phase 3 — AI-Powered Test Design

- [ ] Integrate an LLM provider.
- [ ] Implement requirements analysis.
- [ ] Extract acceptance criteria.
- [ ] Generate structured test scenarios.
- [ ] Add human review and approval.
- [ ] Evaluate test generation quality.

### Phase 4 — Test Automation

- [ ] Integrate Playwright.
- [ ] Implement automated test execution.
- [ ] Collect test results and artifacts.
- [ ] Associate test cases with Jira requirements.

### Phase 5 — Intelligent QA Workflows

- [ ] Implement failure analysis.
- [ ] Add AI-assisted defect triage.
- [ ] Generate Jira bug-report drafts.
- [ ] Implement release risk assessment.
- [ ] Introduce multi-agent orchestration.

### Phase 6 — Production-Oriented Engineering

- [ ] Add PostgreSQL.
- [ ] Implement a dashboard.
- [ ] Containerize the application.
- [ ] Configure GitHub Actions CI/CD.
- [ ] Add logging and observability.
- [ ] Strengthen security and access controls.
- [ ] Document architecture and deployment.

## Engineering Principles

This project emphasizes:

- **Separation of concerns:** API routes, services, and AI agents have distinct responsibilities.
- **Testability:** External integrations should be mockable and independently testable.
- **Security:** Credentials remain outside source code and are never intentionally exposed in API responses.
- **Traceability:** QA activities should be linked to their originating requirements.
- **Human oversight:** AI-generated actions affecting external systems should be reviewed before execution.
- **Incremental development:** Features are implemented, tested, and documented progressively.

## License

No license has been selected yet.

---

**Project:** Agentic QA Platform  
**Development status:** Active development  
**Primary focus:** QA Engineering, Test Automation, AI Agents, API Integration, and DevOps