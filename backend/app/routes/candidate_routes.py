from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model import Candidate
from app.schemas.candidate_schemas import CandidateCreate, CandidateResponse
from app.schemas.candidate_job_mapping import EvaluatingCandidate, EvaluationResult
from app.database import get_db
from app.utils.utils import get_evaluation_result

router = APIRouter(prefix="/candidates", tags=["Candidates"])

@router.post("/", response_model=CandidateResponse)
def add_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    new_candidate = Candidate(candidate_name=candidate.candidate_name, resume=candidate.resume, job_id=candidate.job_id)
    db.add(new_candidate)   
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

@router.get("/", response_model=list[CandidateResponse])
def get_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    candidates = db.query(Candidate).offset(skip).limit(limit).all()
    return candidates

# Get candidate by Job ID
@router.get("/job/{job_id}", response_model=list[CandidateResponse])
def get_candidates_by_job_id(job_id: int, db: Session = Depends(get_db)):
    candidates = db.query(Candidate).filter(Candidate.job_id == job_id).all()
    return candidates

@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


# Evaluate Candidate
@router.post("/evaluate", response_model=EvaluationResult)
def evaluate_candidate(evalute: EvaluatingCandidate, db: Session = Depends(get_db)):
    return get_evaluation_result(evaluating=evalute, db=db)