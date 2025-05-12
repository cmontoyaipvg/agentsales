# app/schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PlanStep(BaseModel):
    name: str
    arguments: Dict[str, Any]

class PlanSchema(BaseModel):
    steps: List[PlanStep]

class ReportSection(BaseModel):
    title: str
    content: str
    chart_mermaid: Optional[str] = None

class ReportSchema(BaseModel):
    summary: str
    sections: List[ReportSection]
    recommendations: List[str]
