from pydantic import BaseModel
from typing import List

class JobBase(BaseModel):
    title: str
    country: str
    description: str

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    candidateId: str
    similarityScore: float
    experience: int

    class Config:
        from_attributes = True
