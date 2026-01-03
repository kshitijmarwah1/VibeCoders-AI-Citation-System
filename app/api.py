from fastapi import APIRouter
from app.services.claim_extractor import extract_claims
from app.services.citation_extractor import extract_citations
from app.services.citation_verifier import verify_dois
from app.services.fact_checker import check_claims
from app.services.risk_scorer import calculate_risk

router = APIRouter()

@router.post("/verify")
def verify_text(payload: dict):
    text = payload.get("text", "")

    claims = extract_claims(text)
    citations = extract_citations(text)

    verified_dois, fake_dois = verify_dois(citations["dois"])
    claim_results = check_claims(claims)

    risk = calculate_risk(
        unverified_claims=len([c for c in claim_results if c["status"] != "Verified"]),
        fake_citations=len(fake_dois),
        broken_links=len(citations["urls"])
    )

    summary = (
        "High hallucination risk detected"
        if risk > 0.6
        else "Low hallucination risk"
    )

    return {
        "summary": summary,
        "hallucination_risk": risk,
        "claims": claim_results,
        "verified_dois": verified_dois,
        "fake_dois": fake_dois
    }
