from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from app.database import Base
import time
from sqlalchemy.exc import OperationalError

# Updated for Docker environment
DATABASE_URL = "postgresql://postgres:password@db:5432/resume_db"

# Models
class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_name = Column(String, index=True)
    job_description = Column(Text)
    key_points = Column(String) 


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    candidate_name = Column(String)
    resume = Column(Text)
    job_id = Column(Integer, ForeignKey("jobs.job_id"))


class JobCandidateMap(Base):
    __tablename__ = "job_candidate_map"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(Integer, ForeignKey("jobs.job_id"))
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id"))
    ai_score = Column(Float)
    ai_recommendation = Column(String)
    feedback_comments = Column(Text)


# Engine and Session Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Retry Logic for Initialization
def init_db_with_retries(engine, retries=5, delay=5):
    """
    Initializes the database with retry logic in case the DB is not yet ready.
    """
    for attempt in range(retries):
        try:
            print(f"Attempting to connect to the database (Attempt {attempt + 1}/{retries})...")
            Base.metadata.create_all(bind=engine)
            print("Database is ready!")
            break
        except OperationalError:
            if attempt < retries - 1:
                print("Database connection failed. Retrying in", delay, "seconds...")
                time.sleep(delay)
            else:
                print("Failed to connect to the database after multiple attempts.")
                raise

# Call this during app startup
# init_db_with_retries(engine)