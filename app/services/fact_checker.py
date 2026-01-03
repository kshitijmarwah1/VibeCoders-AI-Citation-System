from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

# Dummy trusted reference (hackathon-safe)
TRUSTED_REFERENCE = "Transformers were introduced in 2017 by Vaswani et al."

def check_claims(claims):
    results = []

    for claim in claims:
        emb1 = model.encode(claim, convert_to_tensor=True)
        emb2 = model.encode(TRUSTED_REFERENCE, convert_to_tensor=True)
        score = float(util.cos_sim(emb1, emb2))

        if score > 0.75:
            status = "Verified"
        elif score > 0.4:
            status = "Uncertain"
        else:
            status = "Likely Hallucinated"

        results.append({
            "claim": claim,
            "confidence": round(score, 2),
            "status": status
        })

    return results
