from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model import Job
from app.schemas.job_schemas import JobCreate, JobResponse
from app.database import get_db
from app.utils.utils import process_job_description

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobCreate)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(job_name=job.job_name, job_description=job.job_description)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=list[JobResponse])
def get_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, db: Session = Depends(get_db)):
    # Find the job by job_id
    job_to_update = db.query(Job).filter(Job.job_id == job_id).first()

    # If the job doesn't exist, raise an error
    if not job_to_update:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update the job key-skill and qualifications
    key_skills_and_qualifications = process_job_description(job_id, db)
    job_to_update.key_points = key_skills_and_qualifications
    db.commit()
    db.refresh(job_to_update)
    return job_to_update

@router.delete("/{job_id}", response_model=JobResponse)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    # Find the job by job_id
    job = db.query(Job).filter(Job.job_id == job_id).first()
    
    # If the job doesn't exist, raise an error
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete the job and commit the transaction
    db.delete(job)
    db.commit()
    
    return job 
