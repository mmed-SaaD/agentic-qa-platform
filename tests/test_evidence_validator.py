import pytest

from backend.app.utils.evidence_validator import validate_requirement_evidence

from backend.app.schemas.requirements import Requirement, RequirementsAnalysis


def test_rejects_fabricated_evidence():

    issue = {
        "summary": "Customer login",
        "description": "Users can log in with email and password."
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="Users must enable MFA.",
                category="security",
                source="explicit",
                evidence="Users must enable MFA."
            )
        ]
    )

    with pytest.raises(ValueError):
        validate_requirement_evidence(analysis, issue)

def test_rejects_missing_evidence():

    issue = {
        "summary": "Customer login",
        "description": "Users can log in with email and password."
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="Users can log in.",
                category="functional",
                source="explicit",
                evidence=None
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="Explicit requirement is missing evidence"
    ):
        validate_requirement_evidence(analysis, issue)

from backend.app.utils.evidence_validator import is_ac_heading


def test_is_ac_heading():
    assert is_ac_heading("AC1 — Successful Login")
    assert is_ac_heading("AC2 - Invalid Password")
    assert is_ac_heading("AC3: Invalid Email")

    assert not is_ac_heading(
        "The system must reject an incorrect password."
    )

def test_rejects_ac_heading_as_description():
    issue = {
        "summary": "Customer Login",
        "description": (
            "AC1 — Successful Login\n"
            "The system authenticates valid customers."
        ),
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="AC1 — Successful Login",
                category="functional",
                source="explicit",
                evidence="The system authenticates valid customers.",
            )
        ],
    )

    with pytest.raises(
        ValueError,
        match="Requirement description must describe system behavior",
    ):
        validate_requirement_evidence(analysis, issue)


def test_rejects_ac_heading_as_evidence():
    issue = {
        "summary": "Customer Login",
        "description": (
            "AC1 — Successful Login\n"
            "The system authenticates valid customers."
        ),
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="The system must authenticate valid customers.",
                category="functional",
                source="explicit",
                evidence="AC1 — Successful Login",
            )
        ],
    )

    with pytest.raises(
        ValueError,
        match="Requirement evidence must contain supporting behavior",
    ):
        validate_requirement_evidence(analysis, issue)


def test_accepts_valid_behavioral_evidence():
    evidence = "The system authenticates valid customers."

    issue = {
        "summary": "Customer Login",
        "description": f"AC1 — Successful Login\n{evidence}",
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="The system must authenticate valid customers.",
                category="functional",
                source="explicit",
                evidence=evidence,
            )
        ],
    )

    validate_requirement_evidence(analysis, issue)