from sqlalchemy import Column, Integer, String, Text, JSON
from app.db.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skill_description = Column(Text)
    experience = Column(Integer)
    location = Column(String)
    embedding_vector = Column(JSON, nullable=True)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    country = Column(String)
    description = Column(Text)
    embedding_vector = Column(JSON, nullable=True)
