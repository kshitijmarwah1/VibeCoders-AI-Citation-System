def calculate_overall_score(results: list[dict]) -> float:
    if not results:
        return 0.0

    total = len(results)
    verified = sum(1 for r in results if r["status"] == "verified")

    avg_confidence = sum(r["confidence"] for r in results) / total
    verified_ratio = verified / total

    overall = (avg_confidence * 0.7) + (verified_ratio * 0.3)

    return round(overall, 2)
