from pydantic import BaseModel
from typing import List, Optional


class Step(BaseModel):
    id: str
    name: str
    status: Optional[str] = 'pending'


class Session(BaseModel):
    id: str
    name: Optional[str]
    steps: List[Step] = []
