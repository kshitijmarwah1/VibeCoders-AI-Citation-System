def calculate_overall_score(results: list[dict]) -> float:
    """
    Calculate overall reliability score from claim verification results.
    Combines average confidence with verification ratio.
    """
    if not results:
        return 0.0

    try:
        total = len(results)
        verified = sum(1 for r in results if r.get("status") == "verified")
        
        # Calculate average confidence (handle missing confidence)
        confidences = [r.get("confidence", 0.0) for r in results if isinstance(r.get("confidence"), (int, float))]
        if not confidences:
            return 0.0
        
        avg_confidence = sum(confidences) / len(confidences)
        verified_ratio = verified / total if total > 0 else 0.0

        # Weighted combination: 70% confidence, 30% verification ratio
        overall = (avg_confidence * 0.7) + (verified_ratio * 0.3)

        return round(overall, 2)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error calculating overall score: {e}")
        return 0.0

