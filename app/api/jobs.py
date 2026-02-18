from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import Job
from app.schemas.job import JobCreate, JobResponse, MatchResponse
from app.services.matching_service import find_matches

# This router handles everything related to Job postings
router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """
    Adds a new job to our system and generates its AI vector representation.
    """
    # 1. Save basics to database
    db_job = Job(
        title=job.title, 
        country=job.country, 
        description=job.description
    )
    db.add(db_job)
    db.commit()
    
    # 2. Generate the AI numbers for the job description
    # This helps us match it against candidates later
    from app.services.embedding_service import get_embedding
    vector = await get_embedding(db_job.description)
    
    # 3. Save the vector to the database
    db_job.embedding_vector = vector.tolist()
    db.commit()
    
    db.refresh(db_job)
    return db_job

@router.get("/{job_id}/match", response_model=List[MatchResponse])
async def match_candidates_to_job(job_id: int, db: Session = Depends(get_db)):
    """
    Finds the best candidates for a specific job using semantics!
    """
    # 1. Look up the job info by its ID
    job = db.query(Job).filter(Job.id == job_id).first()
    
    # If the ID doesn't exist, we return a 404 error
    if not job:
        raise HTTPException(status_code=404, detail="Sorry, we couldn't find that job!")

    # 2. Call our special matching service to find the winners
    # It does the heavy lifting of finding similar vectors
    results = await find_matches(job.description, db)
    
    return results
