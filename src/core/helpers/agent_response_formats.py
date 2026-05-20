from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

from pydantic import BaseModel

@dataclass
class TaskStep:
    step_id: int
    name: str
    description: str
    type: str
    target_files: List[str]
    dependencies: List[int]
    expected_output: Optional[str] = None

@dataclass
class PlannerAgentResponseFormat(BaseModel):
    project_name: str
    project_description: str
    project_type: str
    plan_id: str
    total_steps: list[int]
    
    steps: List[TaskStep] = field(default_factory=list)
    folder_structure: Dict[str, str] = field(default_factory=dict)