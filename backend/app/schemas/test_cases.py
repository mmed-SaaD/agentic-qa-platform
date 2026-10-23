from typing import Literal
from pydantic import BaseModel, Field




class TestCase(BaseModel):
    __test__ = False

    title: str = Field(min_length=5)
    type: Literal["positive", "negative", "boundary"]
    preconditions: list[str] = Field(default_factory=list)
    steps: list[str] = Field(min_length=3)
    expected_result: str = Field(min_length=10)

class TestDesignOutput(BaseModel):
    __test__ = False

    test_cases: list[TestCase] = Field(default_factory=list)

class TestDesignResult(TestDesignOutput):
    __test__ = False

    issue_key: str
