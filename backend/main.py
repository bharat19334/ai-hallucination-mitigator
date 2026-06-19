from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = FastAPI()

# CORS Middleware (Crucial for Cloud Deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    student_id: str

@app.post("/api/v1/query/submit")
async def analyze_query(request: QueryRequest):
    # Logic for RAG + SelfCheckGPT goes here
    # Mocking response for structural integrity
    return {
        "hallucination_score": 0.1,
        "was_rag_triggered": True,
        "baseline_response": "Mock LLM output here...",
        "final_response": "Verified RAG output here..."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)