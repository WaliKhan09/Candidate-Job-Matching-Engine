from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import candidates, jobs
from app.config import settings

# This line creates our database tables automatically when we start
Base.metadata.create_all(bind=engine)

# Initialize our FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A simple semantic matcher for jobs and candidates.",
    version="0.1.0"
)

# Connect our API routes
app.include_router(candidates.router)
app.include_router(jobs.router)

@app.on_event("startup")
def startup_event():
    from app.db.database import SessionLocal
    from app.services.matching_service import rehydrate_index
    db = SessionLocal()
    try:
        rehydrate_index(db)
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "Running", "message": "Welcome to the Matching Engine!"}

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    # Note: uvicorn.run("main:app") because main.py is in the root
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
