from typing import Literal

from pydantic import BaseModel, Field

class Requirement(BaseModel):
    description: str
    category: str
    source: Literal["explicit", "inferred"]

class RequirementGap(BaseModel):
    description: str
    question: str

class RequirementsAnalysis(BaseModel):
    issue_key: str

    requirements: list[Requirement] = Field(
        default_factory=list
    )

    gaps: list[RequirementGap] = Field(
        default_factory=list
    )

    suggested_test_scenarios: list[str] = Field(
        default_factory=list
    )