import re

from backend.app.utils.acceptance_criteria import (
    extract_acceptance_criteria,
)


def resolve_requirement_evidence(analysis, issue):
    description = issue.get("description") or ""
    criteria = extract_acceptance_criteria(description)

    for requirement in analysis.requirements:
        if requirement.source != "explicit":
            continue

        evidence = requirement.evidence or ""

        # Accept only an exact AC heading or identifier as a reference
        match = re.fullmatch(
            r"(AC\d+)(?:\s*[-—–:]\s*.+)?",
            evidence.strip(),
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        ac_id = match.group(1).upper()
        criterion = criteria.get(ac_id)

        if criterion is None:
            continue

        # Replace the AC reference with original Jira evidence
        requirement.evidence = criterion["text"]

    return analysis