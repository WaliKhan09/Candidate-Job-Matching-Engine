from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.embedding_service import get_embedding
from app.services.matching_service import add_candidate_to_index
from typing import List

router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/", response_model=CandidateResponse)
async def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    
    db_candidate = Candidate(
        name=candidate.name,
        experience=candidate.experience,
        location=candidate.location,
        skill_description=candidate.skill_description
    )
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    vector = await get_embedding(db_candidate.skill_description)

    db_candidate.embedding_vector = vector.tolist()
    db.commit()

    add_candidate_to_index(vector, db_candidate.id)

    return db_candidate

@router.get("/", response_model=List[CandidateResponse])
async def get_all_candidates(db: Session = Depends(get_db)):
    candidates = db.query(Candidate).all()
    return candidates
