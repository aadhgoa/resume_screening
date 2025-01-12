from pydantic import BaseModel
from typing import Optional


class JobBase(BaseModel):
    job_name: str
    job_description: str
    key_points: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    job_id: int

    class Config:
        from_attributes = True
