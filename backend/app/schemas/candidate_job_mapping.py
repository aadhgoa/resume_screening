from pydantic import BaseModel

class EvaluatingCandidate(BaseModel):
    job_id: int
    candidate_id: int

class EvaluationResult(BaseModel):
    job_id: int
    candidate_id: int
    ai_score: float
    ai_recommendation: str
    feedback_comments: str = None