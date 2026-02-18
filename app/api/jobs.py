from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.models import Job
from app.schemas.job import JobCreate, JobResponse, MatchResponse
from app.services.matching_service import find_matches

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # 1. Save to database
    db_job = Job(
        title=job.title, 
        country=job.country, 
        description=job.description
    )
    db.add(db_job)
    db.commit()
    
    # 2. Generate the AI numbers for the job description
    from app.services.embedding_service import get_embedding
    vector = await get_embedding(db_job.description)
    
    # 3. Save the vector to the database
    db_job.embedding_vector = vector.tolist()
    db.commit()
    
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[JobResponse])
async def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{job_id}/match", response_model=List[MatchResponse])
async def match_candidates_to_job(job_id: int, db: Session = Depends(get_db)):
    # 1. Look up the job info by its ID
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Sorry, we couldn't find that job!")

    # 2. Call our matching service to find the winners
    results = await find_matches(job.description, db)
    
    return results
