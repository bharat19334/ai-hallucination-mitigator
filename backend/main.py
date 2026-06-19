from fastapi import FastAPI
from pydantic import BaseModel

from services.llm_service import (
    generate_baseline_response,
    generate_stochastic_samples
)

from services.selfcheck_service import calculate_hallucination_score

app = FastAPI(title="AI Hallucination Mitigator")


class QueryRequest(BaseModel):
    query: str
    student_id: str


@app.get("/")
def health_check():
    return {
        "status": "success",
        "message": "Backend server is running perfectly!"
    }


@app.post("/api/v1/query/submit")
def submit_query(request: QueryRequest):

    print(f"\n--- New Query from {request.student_id} ---")

    # 1. Generate baseline answer
    baseline_answer = generate_baseline_response(request.query)

    # 2. Generate multiple responses
    samples = generate_stochastic_samples(
        request.query,
        num_samples=3
    )

    # 3. Calculate hallucination score
    h_score = calculate_hallucination_score(
        baseline_answer,
        samples
    )

    print(f"Hallucination Score: {h_score}")

    # 4. Decision
    if h_score > 0.25:
        risk_level = "HIGH"
    else:
        risk_level = "LOW"

    return {
        "status": "success",
        "query": request.query,
        "hallucination_score": h_score,
        "risk_level": risk_level,
        "response": baseline_answer
    }