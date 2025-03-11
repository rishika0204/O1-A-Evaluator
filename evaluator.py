def evaluate_evidence(criteria_scores: dict) -> str:
    """
    Evaluate overall evidence using a simple heuristic.
    Counts the number of criteria with a confidence score above a threshold
    and computes the average of the top three scores.
    Returns an overall rating: 'High', 'Medium', or 'Low'.
    """
    threshold = 0.5
    count_above_threshold = sum(1 for score in criteria_scores.values() if score >= threshold)
    
    # Compute the average of the top three scores.
    top_scores = sorted(criteria_scores.values(), reverse=True)[:3]
    avg_top = sum(top_scores) / len(top_scores) if top_scores else 0
    
    if count_above_threshold >= 3 and avg_top > 0.7:
        rating = "High"
    elif count_above_threshold >= 2 and avg_top > 0.5:
        rating = "Medium"
    else:
        rating = "Low"
        
    return rating
