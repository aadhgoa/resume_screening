from pydantic import BaseModel

class CandidateBase(BaseModel):
    candidate_name: str
    resume: str
    job_id: int

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    pass

    class Config:
        from_attributes = True
