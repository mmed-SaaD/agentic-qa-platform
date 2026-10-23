import logging

import re

from backend.app.schemas.requirements import RequirementsAnalysis



logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    text = text.casefold()

    # Normalize quotation marks
    for quote in ["'", "“", "”", "‘", "’"]:
        text = text.replace(quote, '"')

    # Ignore whitespace immediately after commas
    text = re.sub(r",\s*", ",", text)

    # Normalize remaining whitespace
    return " ".join(text.split())

def is_ac_heading(text: str) -> bool:
    return bool(
        re.fullmatch(
            r"AC\d+\s*[-—–:]\s*.+",
            text.strip(),
            flags=re.IGNORECASE,
        )
    )

def validate_requirement_evidence(
    analysis: RequirementsAnalysis,
    issue: dict
) -> None:

    summary = issue.get("summary") or ""
    description = issue.get("description") or ""

    jira_text = f"{summary}\n{description}"

    for requirement in analysis.requirements:

        if is_ac_heading(requirement.description):
            raise ValueError(
                "Requirement description must describe system behavior, "
                "not just an acceptance criterion heading"
            )

        if requirement.source == "inferred":
            if requirement.evidence is not None:
                raise ValueError(
                    "Inferred requirement must not contain evidence"
                )

        if requirement.source == "explicit":

            if not requirement.evidence:
                raise ValueError(
                    "Explicit requirement is missing evidence"
                )

            if is_ac_heading(requirement.evidence):
                logger.warning(
                    "Heading-only evidence rejected for requirement: %s",
                    requirement.description,
                )
                raise ValueError(
                    "Requirement evidence must contain supporting behavior, not just an acceptance criterion heading"
                )

            if normalize_text(requirement.evidence) not in normalize_text(jira_text):
                logger.warning(
                    "Evidence validation failed for requirement: %s",
                    requirement.description,
                )

                raise ValueError(
                    "Requirement evidence was not found in Jira"
                )