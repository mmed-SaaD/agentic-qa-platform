import pytest
from pydantic import ValidationError

from backend.app.schemas.test_cases import TestCase 


def test_valid_test_case():
    test_case = TestCase(
        title="Successful login",
        type="positive",
        preconditions=["A registered customer exists"],
        steps=[
            "Open the login page",
            "Enter valid credentials",
            "Click Login",
        ],
        expected_result="Customer reaches the dashboard",
    )

    assert test_case.title == "Successful login"
    assert test_case.type == "positive"
    assert len(test_case.steps) == 3


def test_invalid_test_case_type():
    with pytest.raises(ValidationError):
        TestCase(
            title="Invalid test",
            type="unknown",
            expected_result="An error appears",
        )

def test_rejects_test_case_with_too_few_steps():
    with pytest.raises(ValidationError):
        TestCase(
            title="Successful login",
            type="positive",
            steps=["Click Login"],
            expected_result="User reaches the dashboard",
        )