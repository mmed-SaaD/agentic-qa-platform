import json

from pydantic import ValidationError

from backend.app.schemas.requirements import Requirement, RequirementsAnalysis
from backend.app.schemas.test_cases import (
    TestDesignOutput,
    TestDesignResult,
)
from backend.app.services.ollama_client import OllamaClient


class TestDesignError(Exception):
    __test__ = False
    pass


class TestDesignAgent:
    __test__ = False

    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client

    def build_prompt(self, analysis: RequirementsAnalysis) -> str:
        requirements_json = analysis.model_dump_json(indent=2)

        return f"""
            You are a senior QA engineer.

            Design high-quality manual test cases from the requirements below.

            REQUIREMENTS:
            {requirements_json}

            GENERAL RULES:
            1. Generate tests only for explicitly supported requirements.
            2. Each test must verify one distinct behavior.
            3. Do not generate duplicate or overlapping scenarios.
            4. Do not invent features, validation rules, limits, or error messages.
            5. Return valid JSON matching the requested schema.

            TEST CASE TITLES:
            1. Write a clear, specific title describing what is being verified.
            2. Start titles with "Verify" followed by the behavior or outcome.
            3. Titles must be understandable without reading the test steps.
            4. Do not use acceptance criteria identifiers as titles.
            5. Do not prefix titles with "Positive", "Negative", or "Boundary".
            6. Avoid vague titles such as "Valid Input" or "Invalid Data".

            Good titles:
            - Verify successful authentication with valid credentials
            - Verify rejection of an invalid authentication attempt
            - Verify required fields prevent incomplete form submission
            - Verify an authenticated session is terminated after logout

            Bad titles:
            - AC1 - Login
            - Positive Test: Login
            - Invalid Data
            - Test Registration

            TEST CLASSIFICATION:
            Classify tests according to the expected behavior being verified.

            positive:
            - Confirms the system performs an intended operation correctly.
            - Includes successful actions, UI behavior, security controls,
            and other expected system functionality.

            negative:
            - Confirms the system correctly handles invalid inputs,
            prohibited actions, or failure conditions.

            boundary:
            - Tests values at or immediately around an explicitly
            specified minimum, maximum, or threshold.
            - Do not generate boundary tests without a documented limit.

            PRECONDITIONS:
            Preconditions describe the required system state or test data
            that must exist BEFORE test execution begins.

            For every test:
            1. Identify the required starting state.
            2. Identify any necessary existing records, accounts, permissions,
            sessions, configuration, or test data.
            3. Write each required condition as a separate list item.
            4. Do not repeat test steps as preconditions.
            5. Use an empty list ONLY when no special setup is required.
            6. Do not invent prerequisites unsupported by the requirements.

            TEST STEPS:
            1. Provide at least 3 actionable steps.
            2. Write steps in execution order.
            3. Each step must describe an action performed by the tester.
            4. Do not include assertions or expected results as steps.
            5. Do not invent URLs, selectors, credentials, or interface elements.

            EXPECTED RESULT:
            1. Describe the observable outcome.
            2. Make the result specific and verifiable.
            3. Do not assume exact messages unless the requirements specify them.

            FINAL QUALITY CHECK:
            Before returning the JSON, review every test case:

            - Is the title descriptive and unique?
            - Is the classification consistent with the scenario?
            - Are all necessary preconditions included?
            - Are the steps executable?
            - Is the expected result verifiable?
            - Is the behavior supported by the requirements?
            - Does another test already cover the same scenario?

            Correct any problems before returning the final JSON.

            Return ONLY JSON matching the requested output schema.
        """.strip()

    def generate(self, analysis: RequirementsAnalysis) -> TestDesignResult:
        prompt = self.build_prompt(analysis)

        ai_response = self.ollama_client.generate(
            prompt,
            output_schema=TestDesignOutput,
        )

        try:
            data = json.loads(ai_response)

            ai_output = TestDesignOutput.model_validate(data)

            unique_cases = remove_duplicates(ai_output.test_cases)

            return TestDesignResult(
                issue_key=analysis.issue_key,
                test_cases=unique_cases,
            )

        except (json.JSONDecodeError, ValidationError, ValueError) as error:
            raise TestDesignError(
                "AI returned an invalid test design"
            ) from error

def remove_duplicates(test_cases):
    unique_cases = []
    seen = set()

    for test_case in test_cases:
        key = (
            test_case.type,
            tuple(test_case.steps),
            test_case.expected_result,
        )

        if key not in seen:
            seen.add(key)
            unique_cases.append(test_case)

    return unique_cases