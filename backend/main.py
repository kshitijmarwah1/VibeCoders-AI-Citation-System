from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tavily import TavilyClient
from dotenv import load_dotenv
from services.citation_extractor import extract_citations
from services.similarity import compute_similarity
from services.credibility import calculate_credibility
from services.aggregate_score import calculate_overall_score
from services.contradiction import detect_contradiction
from services.cache import get_cached, set_cache
import os
import re
import logging
logging.basicConfig(level=logging.INFO)


app = FastAPI()

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextInput(BaseModel):
    text: str


@app.get("/")
def root():
    return {"message": "Backend is running"}


def extract_claims(text: str):
    sentences = re.split(r"[.!?]", text)
    claims = []

    opinion_starters = (
        "i think",
        "i believe",
        "in my opinion",
        "we think",
        "you should",
        "it seems",
        "probably",
        "maybe",
    )

    for s in sentences:
        cleaned = s.strip()

        if len(cleaned) < 20:
            continue

        lower = cleaned.lower()

        # Remove questions
        if cleaned.endswith("?"):
            continue

        # Remove opinions / subjective statements
        if lower.startswith(opinion_starters):
            continue

        claims.append(cleaned)

    return claims


def search_web_for_claim(claim: str):
    try:
        response = tavily.search(
            query=claim,
            search_depth="basic",
            max_results=3
        )
    except Exception as e:
        # Fail safely
        return [], []

    citations = []
    snippets = []

    for result in response.get("results", []):
        citations.append({
            "title": result.get("title"),
            "url": result.get("url")
        })

        if result.get("content"):
            snippets.append(result.get("content"))

    return citations, snippets



def verify_claim_with_search(claim: str):
    cached_result = get_cached(claim)
    if cached_result:
        return cached_result

    hallucination_keywords = [
        "sun revolves around the earth",
        "earth is flat",
        "humans can breathe in space",
        "moon is made of cheese",
    ]

    claim_lower = claim.lower()

    for keyword in hallucination_keywords:
        if keyword in claim_lower:
            return {
                "status": "hallucinated",
                "confidence": 0.05,
                "citations": [],
                "similarity": 0.0,
            }

    citations, snippets = search_web_for_claim(claim)

    similarity_score = compute_similarity(claim, snippets)
    credibility_score = calculate_credibility(citations)

    final_score = round(similarity_score * credibility_score, 2)
    
    has_contradiction = detect_contradiction(snippets)

    if has_contradiction:
        logging.warning(f"Contradiction detected for claim: {claim}")
        final_score = round(final_score * 0.7, 2)


    # 🔑 Threshold (very important)
    if final_score < 0.45:
        return {
            "status": "hallucinated",
            "confidence": final_score,
            "citations": citations,
            "similarity": round(similarity_score, 2),
            "credibility": credibility_score,
        }
    
    
    result = {
        "status": "verified",
        "confidence": final_score,
        "citations": citations,
        "similarity": round(similarity_score, 2),
        "credibility": credibility_score,
        "contradicted": has_contradiction
    }
    
    set_cache(claim, result)
    return result


@app.post("/verify")
def verify_text(data: TextInput):
    claims = extract_claims(data.text)
    results = []

    for c in claims:
        verification = verify_claim_with_search(c)
        results.append(
            {
                "claim": c,
                "status": verification["status"],
                "confidence": verification["confidence"],
                "citations": verification["citations"],
                "similarity": verification["similarity"],
                "credibility": verification["credibility"],
            }
        )

    extracted_citations = extract_citations(data.text)

    overall_score = calculate_overall_score(results)


    return {
        "total_claims": len(results),
        "overall_reliability": overall_score,
        "claims": results if results else [],
        "extracted_citations": extracted_citations or {
            "dois": [],
            "urls": []
        }
    }
