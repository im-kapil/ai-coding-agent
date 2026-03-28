from pydantic import BaseModel, Field
from typing import List, Dict, Literal

class Progress(BaseModel):
    files_created: int = 0
    tasks_completed: int = 0


class HistoryItem(BaseModel):
    step: int
    tool: str
    status: str
    error: str | None = None


class State(BaseModel):
    goal: str

    status: Literal["analysed", "running", "completed", "error"] = "analysed"

    current_step: int = 0
    max_steps: int = 20

    files: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

    retry_count: Dict[int, int] = Field(default_factory=dict)

    progress: Progress = Field(default_factory=Progress)

    history: List[HistoryItem] = Field(default_factory=list)