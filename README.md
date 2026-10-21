# Agentic QA Platform

**A hands-on QA engineering project bringing Jira, test automation, and local AI together.**

> **Status:** Active development — FastAPI backend, Jira issue retrieval, and an AI-powered RequirementsAgent are operational. The latest local test run reported **23 passed, 1 warning**.

## Overview

I started Agentic QA Platform to explore a practical question: **how can AI support a QA engineer without replacing sound testing practices?**

The idea is to connect real Jira issues to a set of focused QA tools and agents. The first working agent reads a Jira story, identifies testable requirements, highlights unanswered questions, and proposes test scenarios. Later stages will cover test-case design, execution, failure investigation, and release decisions.

I am building the project one component at a time, with automated tests, clear interfaces, and human review. An AI suggestion is a starting point for QA work, not an approved requirement.

## Implemented Features

- **FastAPI backend:** Root, health-check, Jira issue retrieval, and AI requirements-analysis endpoints.
- **Jira Cloud integration:** Authenticated Jira REST API v3 access through a reusable `JiraClient` using environment-based credentials.
- **Issue normalization:** Retrieve Jira issue details and convert Atlassian Document Format (ADF) descriptions into readable text.
- **API error handling:** Map missing/inaccessible Jira issues and upstream communication errors to appropriate HTTP responses.
- **Local LLM integration:** Reusable `OllamaClient` calling Ollama's `/api/generate` endpoint. The current development model is `qwen3:1.7b`.
- **RequirementsAgent:** Analyze Jira issue content to suggest requirements, clarification gaps, and test scenarios.
- **Structured AI output:** Parse JSON into Pydantic models and reject invalid JSON or invalid schemas.
- **Requirement provenance:** Classify requirements as `explicit` or `inferred` using a constrained Pydantic field. This is model-reported classification, **not yet independently verified against source evidence**.
- **Automated tests:** Pytest coverage for backend behavior, Jira-related functionality, ADF parsing, requirements schemas, and mocked agent responses. Latest reported run: **23 passed**.

## What I Am Working On Next

- Verify AI-generated requirements against exact Jira evidence and evaluate analysis quality.
- Extract and trace acceptance criteria to proposed tests.
- Build a dedicated **Test Design Agent** for structured test cases.
- Integrate **Playwright** for automated UI testing and collect execution artifacts.
- Add failure triage, defect-report drafts, and release risk assessment.
- Add human review before actions that modify Jira or affect releases.
- Explore multi-agent orchestration, PostgreSQL, a dashboard, Docker, CI/CD, and observability.

## Technology Stack

| Area | Technology | Status |
| --- | --- | --- |
| Language | Python | Implemented |
| API | FastAPI, Uvicorn | Implemented |
| HTTP clients | Requests | Implemented |
| Configuration | python-dotenv / environment variables | Implemented |
| Data validation | Pydantic | Implemented |
| Testing | Pytest, FastAPI TestClient, mocks | Implemented |
| Project management | Jira Cloud REST API v3 | Implemented (issue retrieval) |
| Local AI inference | Ollama, Qwen3 1.7B | Implemented |
| UI automation | Playwright | Planned |
| Agent orchestration | LangGraph (under consideration) | Planned |
| Database | PostgreSQL | Planned |
| Containerization | Docker | Planned |
| CI/CD | GitHub Actions | Planned |
| Version control | Git, GitHub | Implemented |

## Architecture

```text
                      Developer / API Client
                               |
                               v
                         FastAPI Backend
                               |
               +---------------+----------------+
               |                                |
               v                                v
      Jira issue retrieval            AI requirements endpoint
               |                                |
               v                                v
           JiraClient                    fetch_jira_issue()
               |                                |
               v                                v
        Jira Cloud API                   RequirementsAgent
                                                |
                                                v
                                           OllamaClient
                                                |
                                                v
                                        Local Ollama / Qwen3
                                                |
                                                v
                                    JSON parsing + Pydantic
                                                |
                                                v
                                     RequirementsAnalysis

           Future: Test Design Agent -> Test Execution -> Failure Triage
                                      -> Release Risk
```

**Responsibilities:**

- **API layer:** Accepts requests and exposes validated responses.
- **Jira service:** Handles external Jira communication and issue retrieval.
- **ADF parsing:** Converts Jira's rich-text description structure to plain text.
- **Ollama service:** Encapsulates communication with the local language model.
- **RequirementsAgent:** Builds the analysis prompt, parses model output, and returns typed analysis data.
- **Pydantic schemas:** Define the contract for requirements, gaps, and suggested scenarios.

## Project Structure

The following highlights the main components; additional test and package files may be present.

```text
agentic-qa-platform/
├── backend/
│   └── app/
│       ├── main.py
│       ├── agents/
│       │   └── requirements_agent.py
│       ├── schemas/
│       │   └── requirements.py
│       └── services/
│           ├── jira_client.py
│           └── ollama_client.py
├── scripts/
│   └── test_jira_connection.py
├── tests/
│   ├── test_requirements_agent.py
│   ├── test_requirements_schema.py
│   └── ...
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- Jira Cloud account and Atlassian API token
- [Ollama](https://ollama.com/) installed and running for AI analysis
- A system capable of running the chosen local model; the smaller `qwen3:1.7b` model is used for development on CPU

### 1. Clone the repository

```bash
git clone git@github.com:mmed-SaaD/agentic-qa-platform.git
cd agentic-qa-platform
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activation is `.venv\Scripts\Activate.ps1`.

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Jira credentials

Copy `.env.example` to `.env` and populate the Jira values:

```dotenv
JIRA_BASE_URL=https://your-site.atlassian.net
JIRA_EMAIL=your-atlassian-email@example.com
JIRA_API_TOKEN=your-api-token
```

**Never commit `.env`, passwords, or API tokens.** Ensure `.env` is ignored by Git.

### 5. Start Ollama and download the development model

Install Ollama on the host, then run:

```bash
ollama pull qwen3:1.7b
```

Make sure the Ollama service is running and accessible at `http://localhost:11434`. In the current setup, Ollama runs on Windows and the FastAPI backend runs in WSL. The client uses the Ollama HTTP API; the model must be available to the Ollama server receiving requests.

> The default model is currently configured in `backend/app/services/ollama_client.py`. If you choose a different model or host, adjust the client configuration accordingly.

### 6. Start FastAPI

From the repository root:

```bash
python -m uvicorn backend.app.main:app --reload
```

- API: http://127.0.0.1:8000
- Interactive API docs: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description | Status |
| --- | --- | --- | --- |
| `GET` | `/` | Root/welcome endpoint | Implemented |
| `GET` | `/health` | Application health check | Implemented |
| `GET` | `/jira/issue/{issue_key}` | Retrieve and normalize a Jira issue | Implemented |
| `POST` | `/ai/requirements/analyze/{issue_key}` | Analyze a Jira issue using the local RequirementsAgent | Implemented |

### Example: AI requirements analysis

Open `/docs` and execute:

```http
POST /ai/requirements/analyze/SHOP-2
```

An illustrative response (actual model output varies):

```json
{
  "issue_key": "SHOP-2",
  "requirements": [
    {
      "description": "Registered customers can log in using an email address and password.",
      "category": "functional",
      "source": "explicit"
    }
  ],
  "gaps": [
    {
      "description": "The expected response to invalid credentials is not specified.",
      "question": "What should the application display after an unsuccessful login?"
    }
  ],
  "suggested_test_scenarios": [
    "Verify login with valid credentials",
    "Verify the defined behavior for invalid credentials"
  ]
}
```

`source` accepts only `explicit` or `inferred`. The distinction is useful for review, but the current system does not yet verify whether each classification is factually supported by a quotation from Jira.

### Error handling

- Jira lookup and communication errors are translated into API errors.
- Invalid AI JSON or output that fails Pydantic validation is handled as a requirements-analysis error; the AI endpoint returns an upstream failure response rather than silently accepting malformed output.
- Ollama must be reachable for AI requests. Model inference can be slow on CPU-only hardware.

## Testing

Run the complete suite from the repository root:

```bash
python -m pytest -q
```

Latest locally reported result:

```text
23 passed, 1 warning in 0.72s
```

The suite includes mocked integrations so core behavior can be checked without requiring live Jira or Ollama calls for every test. Tests exercise valid and invalid requirements-analysis responses, including rejection of invalid `source` values.

The remaining warning should be investigated separately; a passing suite does not mean all runtime paths or AI output quality have been fully verified.

## Development Roadmap

### Phase 1 — Foundation

- [x] Initialize repository and Python environment
- [x] Implement FastAPI root and health endpoints
- [x] Add initial automated tests
- [x] Publish code to GitHub

### Phase 2 — Jira Integration

- [x] Configure Jira Cloud project and issue types
- [x] Authenticate using environment variables
- [x] Implement reusable `JiraClient`
- [x] Expose issue retrieval through FastAPI
- [x] Parse ADF descriptions
- [x] Add mocked Jira-related tests and error handling
- [ ] Add controlled issue creation/update workflows

### Phase 3 — Requirements Intelligence

- [x] Integrate local Ollama model
- [x] Implement `RequirementsAgent`
- [x] Generate structured requirements, gaps, and scenario suggestions
- [x] Validate output with Pydantic
- [x] Add explicit/inferred source classification
- [ ] Verify traceability against exact Jira evidence
- [ ] Evaluate semantic quality and reduce unsupported assumptions
- [ ] Add human review and approval

### Phase 4 — Test Design and Execution

- [ ] Implement dedicated Test Design Agent
- [ ] Generate structured test cases from reviewed requirements
- [ ] Integrate Playwright and automated execution
- [ ] Store execution results and artifacts
- [ ] Link tests to Jira requirements

### Phase 5 — Intelligent QA Workflows

- [ ] Analyze test failures
- [ ] Draft and triage defects with human approval
- [ ] Implement release risk assessment
- [ ] Introduce agent orchestration where useful

### Phase 6 — Production-Oriented Engineering

- [ ] Add persistence and dashboard
- [ ] Containerize the platform
- [ ] Configure GitHub Actions CI/CD
- [ ] Add structured logging, metrics, and AI evaluation
- [ ] Strengthen access controls and document deployment

## How I Approach This Project

- **Separation of concerns:** Keep API routes, integrations, schemas, and agents independently maintainable.
- **Testability:** Mock external dependencies and test error paths.
- **Traceability:** Distinguish explicit Jira requirements from inferred suggestions; future work will add evidence-level verification.
- **Security:** Store secrets outside source control and avoid leaking credentials in errors or logs.
- **Human oversight:** Require review before AI suggestions become accepted requirements or trigger external changes.
- **Incremental delivery:** Implement, test, and document features in small steps.

## About the Developer

Designed and developed by **[BAZOURHI Mohamed Saad](https://github.com/mmed-SaaD)**.

I am building Agentic QA Platform as part of my journey in QA engineering and test automation. It gives me a place to turn ideas into working features, practice reliable software engineering, and learn how AI can fit into a real testing workflow.

Feedback, ideas, and constructive suggestions are welcome.

