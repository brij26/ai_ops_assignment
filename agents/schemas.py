from pydantic import BaseModel
from typing import List, Literal

class PlanStep(BaseModel):
    description: str
    tool: Literal["weather", "air_quality"]
    input: str

class Plan(BaseModel):
    steps: List[PlanStep]

class ExecutionResult(BaseModel):
    step: str
    output: dict

class FinalAnswer(BaseModel):
    city: str
    weather: dict
    air_quality: dict
