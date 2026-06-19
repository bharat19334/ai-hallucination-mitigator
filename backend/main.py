from fastapi import FastAPI, Body # Body add kiya
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    student_id: str

@app.post("/api/v1/query/submit")
async def analyze_query(data: QueryRequest): # Pydantic model fix
    print(f"Received query: {data.query}") # Logs mein check karne ke liye
    return {
        "hallucination_score": 0.15,
        "was_rag_triggered": True,
        "baseline_response": f"Processed: {data.query}",
        "final_response": "Verified RAG output"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)