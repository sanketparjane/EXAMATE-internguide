# app/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class Record:
    activity_head: str
    sub_activity: str
    suggested_credits: str
    suggested_weeks: str
    evidence_document: str
    evaluated_by: str
    id: Optional[int] = None