from fastapi import FastAPI
from pydantic import BaseModel
from services.llm_service import generate_baseline_response, generate_stochastic_samples # <-- Naya import
from services.vector_service import ingest_knowledge, search_knowledge
from services.selfcheck_service import calculate_hallucination_score # <-- Naya import

app = FastAPI(title="Edu AI Pipeline")

class QueryRequest(BaseModel):
    query: str
    student_id: str

class IngestRequest(BaseModel):
    text: str
    source: str

@app.get("/")
def health_check():
    return {"status": "success", "message": "Backend server is running perfectly!"}

@app.post("/api/v1/rag/ingest")
def add_to_knowledge_base(request: IngestRequest):
    result_msg = ingest_knowledge(text_content=request.text, source_name=request.source)
    return {"status": "success", "message": result_msg}

# --- THE ULTIMATE DECISION ENGINE ---
@app.post("/api/v1/query/submit")
def submit_query(request: QueryRequest):
    print(f"\n--- New Query from {request.student_id} ---")
    
    # 1. Generate Baseline Answer
    baseline_answer = generate_baseline_response(request.query)
    
    # 2. Generate 3 Samples for Verification
    samples = generate_stochastic_samples(request.query, num_samples=3)
    
    # 3. Calculate Hallucination Score
    h_score = calculate_hallucination_score(baseline_answer, samples)
    print(f"Calculated Hallucination Score: {h_score}")
    
    # 4. Decision Gate (Threshold = 0.3)
    final_answer = baseline_answer
    used_rag = False
    retrieved_facts = None
    
    if h_score > 0.25:
        print("🚨 High Hallucination Detected! Triggering RAG Pipeline...")
        try:
            retrieved_facts = search_knowledge(query=request.query)
            # Yahan hum LLM ko ek verified prompt bhejenge (Agla step)
            final_answer = f"⚠️ Baseline answer was unreliable. Grounded Fact from Database: {retrieved_facts}"
            used_rag = True
        except Exception as e:
            final_answer = f"Database error: {str(e)}"
    else:
        print("✅ Response is consistent. Skipping RAG.")
    
    return {
        "status": "success",
        "hallucination_score": h_score,
        "was_rag_triggered": used_rag,
        "final_response": final_answer,
        "baseline_response": baseline_answer
    }