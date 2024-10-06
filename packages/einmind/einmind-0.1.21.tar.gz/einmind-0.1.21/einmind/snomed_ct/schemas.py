from pydantic import BaseModel
from enum import Enum
import typing as t


class TaskStates(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TermCategories(str, Enum):
    PROBLEM = "PROBLEM"
    PROCEDURE = "PROCEDURE"


class Prediction(BaseModel):
    code: str
    title: str
    confidence: float


class TaskStatus(BaseModel):
    task_state: str
    task_failed_msg: t.Optional[str]
    prediction: t.Optional[Prediction]
