from pydantic import BaseModel
import typing as t
from enum import Enum


class TaskStates(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Prediction(BaseModel):
    code: str
    title: str
    confidence: float


class TaskStatus(BaseModel):
    task_state: str
    task_failed_msg: t.Optional[str]
    prediction: t.Optional[Prediction]
