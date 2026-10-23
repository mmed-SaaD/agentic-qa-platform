from backend.app.schemas.requirements import (
    Requirement,
    RequirementsAnalysis,
)
from backend.app.utils.evidence_resolver import (
    resolve_requirement_evidence,
)


def test_resolves_ac_heading_to_original_jira_text():
    issue = {
        "description": (
            "AC1 — Successful Login\n"
            "Given valid credentials,\n"
            "When the customer logs in,\n"
            "Then access is granted.\n"
        )
    }

    analysis = RequirementsAnalysis(
        issue_key="SHOP-2",
        requirements=[
            Requirement(
                description="The system must grant access after valid login.",
                category="functional",
                source="explicit",
                evidence="AC1 — Successful Login",
            )
        ],
    )

    result = resolve_requirement_evidence(analysis, issue)

    assert result.requirements[0].evidence == (
        "Given valid credentials,\n"
        "When the customer logs in,\n"
        "Then access is granted."
    )