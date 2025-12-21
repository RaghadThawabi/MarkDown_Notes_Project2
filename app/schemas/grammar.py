from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class GrammarReplacement(BaseModel):#suggested fix
    value: str


class GrammarIssueOut(BaseModel):
    id: UUID
    revision_id: UUID
    message: str
    short_message: Optional[str]
    offset: int
    length: int
    context: Optional[str]
    replacements: List[str]  #fixes
    issue_type: Optional[str]
    rule_id: Optional[str]
    category: Optional[str]
    is_applied: bool
    created_at: datetime

    class Config:
        orm_mode = True


class GrammarCheckResponse(BaseModel):
    revision_id: UUID
    total_issues: int
    issues: List[GrammarIssueOut]


class ApplyFixesRequest(BaseModel):#Request to apply specific fixes

    issue_ids: List[UUID]


class ApplyFixesResponse(BaseModel):# Response after applying fixes
    applied_count: int
    new_content: str
    message: str
