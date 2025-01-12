import os
import json
from typing import List, Dict
from groq import Groq
from sqlalchemy.orm import Session
from app.model import Job, Candidate, JobCandidateMap
from app.schemas.candidate_job_mapping import EvaluatingCandidate


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def process_job_description(job_id: int, db: Session):
    # Retrieve the job description from the database
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if not job:
        raise ValueError(f"Job with ID {job_id} not found.")

    job_description = job.job_description

    # Prepare the prompt for OpenAI's API
    prompt = f"""
    Given the job title and description below, extract the key skills and qualifications that the recruiter is seeking:

    Job Title: {job.job_name}
    Job Description: {job_description}

    Key Skills and Qualifications:

    I want a JSON Output Format:
    
    key_skills_and_qualifications: [
        "Skill 1",
        "Skill 2",
        "Skill 3",
        ...
    ]
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
    )

    print(chat_completion.choices[0].message.content)

    return chat_completion.choices[0].message.content


def evaluate_resume(
    job_key_points: List[str], candidate_resume: str
) -> Dict[str, Dict[str, str]]:
    prompt = (
        "Evaluate the following candidate's resume against each job key point provided. "
        "For each key point, assign a score between 0 and 10 and provide reasoning based on the resume. "
        "Output the results in the following JSON format:\n\n"
        "{\n"
        '  "Key_skill1": {"score": <some_value>, "reason": "<evidence_from_resume>"},\n'
        '  "Key_skill2": {"score": <some_value>, "reason": "<evidence_from_resume>"},\n'
        "  ...\n"
        "}\n\n"
        "Job Key Points:\n"
    )
    for point in job_key_points:
        prompt += f"- {point}\n"
    prompt += "\nCandidate Resume:\n" + candidate_resume

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI trained to evaluate resumes against job requirements.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"}
    )

    evaluation = response.choices[0].message.content
    print(evaluation)
    return json.loads(evaluation)


def store_evaluation(
    db: Session, job_id: int, candidate_id: int, evaluation: Dict[str, Dict[str, str]]
):
    ai_score = sum(item["score"] for item in evaluation.values()) / len(evaluation)
    ai_score = round(ai_score, 2)
    ai_recommendation = "Recommended" if ai_score >= 7 else "Not Recommended"
    feedback_comments = json.dumps(evaluation, indent=2)

    job_candidate_map = JobCandidateMap(
        job_id=job_id,
        candidate_id=candidate_id,
        ai_score=ai_score,
        ai_recommendation=ai_recommendation,
        feedback_comments=feedback_comments,
    )
    db.add(job_candidate_map)
    db.commit()
    db.refresh(job_candidate_map)
    return job_candidate_map


def get_evaluation_result(evaluating: EvaluatingCandidate, db: Session):
    job = db.query(Job).filter(Job.job_id == evaluating.job_id).first()
    candidate = (
        db.query(Candidate)
        .filter(Candidate.candidate_id == evaluating.candidate_id)
        .first()
    )

    if not job:
        raise ValueError(f"Job with ID {evaluating.job_id} not found.")
    if not candidate:
        raise ValueError(f"Candidate with ID {evaluating.candidate_id} not found.")

    job_key_points = job.key_points  # Assuming key_points is a comma-separated string
    candidate_resume = candidate.resume

    evaluation = evaluate_resume(job_key_points, candidate_resume)
    return store_evaluation(db, job.job_id, candidate.candidate_id, evaluation)
