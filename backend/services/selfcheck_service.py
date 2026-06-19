from sentence_transformers import SentenceTransformer, util


similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_hallucination_score(baseline_answer: str, sampled_answers: list) -> float:
   
    print("Calculating Hallucination Score...")
    
    if not sampled_answers:
        return 0.0 
        
  
    baseline_embedding = similarity_model.encode(baseline_answer, convert_to_tensor=True)
    
    sample_embeddings = similarity_model.encode(sampled_answers, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(baseline_embedding, sample_embeddings)[0]

    avg_similarity = sum(cosine_scores).item() / len(cosine_scores)
    
    hallucination_score = 1.0 - max(0.0, avg_similarity) 
    return round(hallucination_score, 2)