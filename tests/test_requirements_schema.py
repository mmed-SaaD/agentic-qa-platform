import pytest
from pydantic import ValidationError

from backend.app.schemas.requirements import (
    Requirement,
    RequirementGap,
    RequirementsAnalysis,
)


def test_requirements_analysis_valid():
    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="Customers can log in.",
                category="functional",
            )
        ],
        gaps=[
            RequirementGap(
                description="Session timeout is unspecified.",
                question="When should sessions expire?",
            )
        ],
        suggested_test_scenarios=[
            "Login with valid credentials"
        ],
    )

    assert analysis.issue_key == "SHOP-2"
    assert len(analysis.requirements) == 1
    assert analysis.requirements[0].category == "functional"
    assert len(analysis.gaps) == 1


def test_requirements_analysis_default_lists():
    analysis = RequirementsAnalysis(issue_key="SHOP-2")

    assert analysis.requirements == []
    assert analysis.gaps == []
    assert analysis.suggested_test_scenarios == []


def test_requirements_analysis_missing_issue_key():
    with pytest.raises(ValidationError):
        RequirementsAnalysis()
