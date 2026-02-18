from pydantic import BaseModel, Field

class CandidateBase(BaseModel):
    name: str
    skill_description: str
    experience: int = Field(..., ge=0)
    location: str

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int

    class Config:
        from_attributes = True
