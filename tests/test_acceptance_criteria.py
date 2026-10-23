from backend.app.utils.acceptance_criteria import (
    extract_acceptance_criteria,
)


def test_extract_acceptance_criteria():
    text = """
Acceptance Criteria
AC1 — Successful Login
Given valid credentials,
When the customer logs in,
Then access is granted.

AC2 — Invalid Password
Given an incorrect password,
When the customer logs in,
Then access is denied.

Business Rules
Passwords must never appear in logs.
"""

    result = extract_acceptance_criteria(text)

    assert len(result) == 2

    assert result["AC1"]["title"] == "Successful Login"

    assert "access is granted" in result["AC1"]["text"]

    assert result["AC2"]["title"] == "Invalid Password"

    assert "access is denied" in result["AC2"]["text"]

def test_last_ac_excludes_business_rules():
    text = """
AC1 — Successful Login
Given valid credentials,
When the customer logs in,
Then access is granted.

AC2 — Invalid Password
Given an incorrect password,
When the customer logs in,
Then access is denied.

Business Rules
Passwords must never appear in logs.
"""

    result = extract_acceptance_criteria(text)

    assert len(result) == 2

    assert "access is denied" in result["AC2"]["text"]

    assert "Business Rules" not in result["AC2"]["text"]

    assert "Passwords must never appear" not in result["AC2"]["text"]