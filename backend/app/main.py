from fastapi import FastAPI
from app.routes import job_routes, candidate_routes
from app.model import engine, init_db_with_retries



app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db_with_retries(engine)

# Include routes
app.include_router(job_routes.router, tags=["Jobs"])
app.include_router(candidate_routes.router, tags=["Candidates"])

@app.get("/")
def root():
    return {"message": "Welcome to the Resume Screening API"}
