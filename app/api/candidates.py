from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Candidate
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.embedding_service import get_embedding
from app.services.matching_service import add_candidate_to_index

# We use "APIRouter" to group our candidate-related endpoints together
router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/", response_model=CandidateResponse)
async def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """
    This endpoint takes a JSON body and saves a new candidate to our system.
    """
    
    # 1. First, we prepare the data to be saved in our SQL database
    db_candidate = Candidate(
        name=candidate.name,
        experience=candidate.experience,
        location=candidate.location,
        skill_description=candidate.skill_description
    )
    
    # 2. Tell the database to add and save it (commit)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    # 3. Next, we turn the skills text into AI numbers (Embeddings)
    # the 'await' keyword is used because this might take a second to calculate
    vector = await get_embedding(db_candidate.skill_description)

    # 4. We save those numbers back to the SQL database so we don't lose them
    db_candidate.embedding_vector = vector.tolist()
    db.commit()

    # 5. Finally, we add the new person to our FAISS fast-search index
    add_candidate_to_index(vector, db_candidate.id)

    # Return the saved candidate info back to the user
    return db_candidate
