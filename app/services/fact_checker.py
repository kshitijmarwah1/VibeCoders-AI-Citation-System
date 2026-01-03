def check_claims(claims):
    results = []

    for claim in claims:
        emb1 = model.encode(claim, convert_to_tensor=True)
        emb2 = model.encode(TRUSTED_REFERENCE, convert_to_tensor=True)
        score = float(util.cos_sim(emb1, emb2))

        if score > 0.75:
            status = "Verified"
            reason = "Matches trusted reference with high similarity"
        elif score > 0.4:
            status = "Uncertain"
            reason = "Partial match, insufficient evidence"
        else:
            status = "Likely Hallucinated"
            reason = "No reliable source supports this claim"

        results.append({
            "claim": claim,
            "confidence": round(score, 2),
            "status": status,
            "reason": reason
        })

    return results
