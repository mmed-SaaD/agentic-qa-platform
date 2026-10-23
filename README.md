# Agentic QA Platform

**An AI-assisted quality engineering platform connecting Jira requirements to structured test design, with a roadmap toward executable automation, CI/CD feedback, and release-risk analysis.**

> **Project status — 23 October 2026:** FastAPI backend, Jira integration, requirements analysis, and test design are implemented and exercised through the running application. **45 automated tests pass** (`pytest -q`, 1.10 s in the latest local run). Generation of executable Playwright/Pytest tests and downstream orchestration are the next development milestones.

## Why I built this

Traditional test automation often starts after someone has already interpreted the requirements and written the test scenarios. I started this project to explore how AI agents could support more of the QA lifecycle: retrieving real work items from Jira, interpreting requirements, identifying gaps, designing tests, and eventually turning approved cases into executable checks.

The goal is not to replace a QA engineer's judgment. It is to build a practical, reviewable workflow where AI accelerates repetitive analysis and drafting, while validation, traceability, and human review keep the output accountable.

This is an evolving portfolio project, developed hands-on from the backend foundation onward.

## Current capabilities

### 1. FastAPI backend

- Python/FastAPI service with a working `/health` endpoint and interactive API documentation at `/docs`.
- Modular separation between API routes, service clients, agents, and Pydantic schemas.
- Automated tests for API behavior, validation, and failure paths.

### 2. Jira Cloud integration

- Authenticated communication with a real Jira Cloud project using environment-based credentials.
- Retrieval of issues by key, including issue summary, status, and description.
- Conversion of Jira's Atlassian Document Format (ADF) descriptions into usable text.
- Explicit handling of missing/inaccessible issues and upstream communication failures.
- Real Jira project used during development: **SHOP**, including registration and login user stories.

**Implemented API route:** `GET /jira/issue/{issue_key}`.

### 3. Local Ollama integration

- Local LLM inference using Ollama, currently configured for **Qwen3 1.7B**.
- A reusable `OllamaClient` for sending prompts and requesting structured JSON output using a Pydantic-generated schema.
- Local inference avoids a paid hosted-LLM dependency for the current development workflow.
- Model upgrades can be evaluated separately from agent logic; a more capable model may improve output quality but does not eliminate the need for review.

### 4. Requirements Analysis Agent

- Takes a Jira issue and analyzes its requirements.
- Produces structured functional, non-functional, and security requirements where supported by the source.
- Identifies potential requirement gaps and suggests test scenarios.
- Tracks whether a requirement is **explicit** or **inferred**, with supporting evidence.
- Validates model output with Pydantic; malformed or invalid output is handled as an error rather than silently accepted.

**End-to-end behavior verified:** The running backend has retrieved real SHOP issues and produced structured requirements analysis through Ollama.

### 5. Test Design Agent

- Consumes the structured requirements analysis and generates manual test cases.
- **Generates per requirement**, rather than asking the model to design an entire story's tests in one large response.
- Produces structured test cases with:
  - descriptive title;
  - classification (`positive`, `negative`, or `boundary`);
  - preconditions;
  - actionable steps;
  - expected result.
- Validates generated data against Pydantic schemas.
- Combines results and removes **exact** duplicates based on test type, steps, and expected result.

**End-to-end behavior verified:** The running application has generated test cases for real SHOP stories, including login (`SHOP-2`) and registration (`SHOP-3`).

**Known limitation:** Valid JSON is not the same as correct QA reasoning. The current small model can omit preconditions, misclassify scenarios, include assertions in steps, or assume behavior not supported by the source requirements. Exact duplicate filtering does not detect semantically equivalent tests. **Generated cases are drafts that require QA review before automation.**

## Architecture

```text
                Jira Cloud (SHOP project)
                           |
                           v
                  FastAPI REST API
                           |
                     Jira Client
                           |
                  ADF text conversion
                           |
                           v
                 Requirements Agent
                           |
                    Ollama Client
                     (local LLM)
                           |
                 Pydantic validation
                           |
                           v
                  Test Design Agent
                  (per requirement)
                           |
                    Ollama Client
                           |
                 Pydantic validation
                           |
                  Exact deduplication
                           |
                           v
               Generated test-case drafts
                           |
                      QA review
                           |
                           v
              [Planned: automation agent]
                           |
              [Planned: Playwright/Pytest]
                           |
          [Planned: CI/CD, reports, triage]
```

The brackets in the diagram identify **planned components**, not functionality already delivered.

## Technology stack

| Area | Technology |
| --- | --- |
| Backend/API | Python, FastAPI |
| Data contracts | Pydantic |
| Work-item management | Jira Cloud REST API |
| LLM runtime | Ollama (local) |
| Current model | Qwen3 1.7B |
| HTTP communication | Python HTTP clients |
| Automated verification | Pytest, FastAPI TestClient, `unittest.mock` |
| Development environment | WSL/Linux, Python virtual environment |
| Source control | Git, GitHub |
| Planned executable browser tests | Playwright + Pytest |
| Planned delivery/reporting | CI/CD and test reporting integration |

## Testing strategy and evidence

The project uses **both isolated automated tests and real pipeline testing**. They are complementary and should not be confused.

### Automated tests (mocks and controlled inputs)

Mocks are used where appropriate to simulate Jira or Ollama responses and isolate the component under test. This lets the suite verify API behavior, data parsing, schema constraints, expected service calls, and error handling quickly and repeatably, without depending on network access or nondeterministic LLM responses.

**Latest locally reported result:**

```text
$ pytest -q
............................................. [100%]
45 passed in 1.10s
```

This is evidence of the automated test suite's latest run, **not** a claim that 45 end-to-end tests were executed against Jira and Ollama.

### Real end-to-end pipeline checks

In addition to the mocked tests, the **actual running application** has been exercised using real services:

1. Connect to Jira Cloud and retrieve SHOP issues through the backend.
2. Parse issue descriptions, including ADF content.
3. Call the locally running Ollama model for requirements analysis.
4. Validate and return structured requirements output through FastAPI.
5. Generate structured test cases from the analyzed requirements using the Test Design Agent.
6. Inspect the returned cases for relevance, classification, prerequisites, and unsupported assumptions.

These checks establish that the integrated **Jira → FastAPI → Ollama → requirements analysis → test design** workflow has run in practice. They are **manual integration/end-to-end exercises**, not yet a continuously automated live-service E2E suite. The eventual **generated Playwright/Pytest execution pipeline has not been implemented yet**.

### Quality philosophy

- **Mocks are additional safeguards**, not the sole evidence that the platform works.
- Real-service tests verify integration; isolated tests make regressions easier to diagnose.
- Pydantic validates structure, not the factual correctness of an AI-generated scenario.
- AI-generated test cases should be reviewed before they are accepted or automated.

## Project evolution

| Phase | Work completed |
| --- | --- |
| Foundation | Repository, WSL/Python environment, FastAPI service, health check, first automated tests |
| Jira connectivity | Jira Cloud configuration, issue retrieval, credential handling, error mapping |
| Jira content handling | ADF description parsing and focused parser tests |
| Requirements intelligence | Requirements Agent, structured schemas, local Ollama integration, output validation |
| Real project workflow | SHOP Jira project with product-oriented stories, replacing earlier integration-demo tickets as the main test inputs |
| Test design | TestCase/TestDesign schemas, Test Design Agent, API integration, duplicate filtering |
| Test design refinement | Per-requirement generation, clearer titles and classifications, review of real SHOP-2/SHOP-3 outputs |
| Current verification | **45 automated tests passing**, plus successful live Jira/Ollama pipeline exercises |

## Running locally

### Prerequisites

- Python and a working virtual environment.
- Access to a Jira Cloud project and an API token.
- Ollama installed and reachable from the backend environment.
- The configured Ollama model downloaded locally.

### 1. Get the code and install dependencies

```bash
 git clone https://github.com/mmed-SaaD/agentic-qa-platform.git
 cd agentic-qa-platform
 python3 -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt
```

If your dependency file is located in a subdirectory, use the corresponding path.

### 2. Configure Jira access

Create a local `.env` from the project's `.env.example` and provide your own values:

```dotenv
JIRA_BASE_URL=https://your-site.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
```

Never commit `.env` or API tokens to Git.

### 3. Start or verify Ollama

```bash
ollama list
ollama run qwen3:1.7b
```

Ollama must remain accessible to the FastAPI backend. In WSL/Windows environments, the host address may need adjustment depending on how Ollama is installed and networked.

### 4. Start FastAPI

From the repository root:

```bash
uvicorn backend.app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the available endpoints. The interactive documentation is the source of truth for request methods and paths as routes evolve.

### 5. Run the automated test suite

```bash
pytest -q
```

### 6. Exercise the live pipeline

Using `/docs`, retrieve a Jira issue, run requirements analysis, and generate test cases for a SHOP issue such as `SHOP-2` or `SHOP-3`. Review the resulting JSON rather than treating schema-valid output as automatically correct.

## Current limitations

- The local Qwen3 1.7B model sometimes produces incomplete preconditions or unsupported assumptions.
- Per-requirement generation can increase inference time because it makes multiple Ollama requests.
- Exact duplicate removal does not catch paraphrased or semantically overlapping scenarios.
- Test cases are currently generated as **manual test specifications**, not executable browser tests.
- No automated approval gate or full requirement-to-test traceability has been completed yet.
- Failure triage, release-risk scoring, and CI/CD feedback loops remain future work.

## Roadmap

1. **Next — Automation generation:** Convert reviewed test cases into executable Playwright/Pytest scripts against a defined test application with known behavior and selectors.
2. **Execution and feedback:** Run generated tests, capture results and failures, and produce useful reports.
3. **Traceability:** Link generated tests and execution results back to source requirements/Jira issues.
4. **CI/CD integration:** Trigger and report automated runs in a repeatable pipeline.
5. **Failure triage:** Investigate failing tests and distinguish likely product defects from flaky tests or environment issues.
6. **Release risk:** Summarize coverage, failures, and outstanding risk for a release decision.
7. **Model evaluation:** Compare the current small local model with a stronger Ollama model using the same stories and quality criteria.

Roadmap items are planned capabilities, not claims of current implementation.

## Repository

GitHub: [mmed-SaaD/agentic-qa-platform](https://github.com/mmed-SaaD/agentic-qa-platform)

## Author

**Designed and developed by BAZOURHI Mohamed Saad (Me- :D)** as a hands-on QA engineering and AI automation portfolio project.

---

*Last updated: 23 October 2026.*
