from difflib import SequenceMatcher

def calculate_hallucination_score(baseline_answer, sampled_answers):

    if not sampled_answers:
        return 0.0

    similarities = []

    for answer in sampled_answers:
        similarity = SequenceMatcher(
            None,
            baseline_answer.lower(),
            answer.lower()
        ).ratio()

        similarities.append(similarity)

    avg_similarity = sum(similarities) / len(similarities)

    # Scale down false positives
    hallucination_score = (1 - avg_similarity) * 0.4

    return round(hallucination_score, 2)