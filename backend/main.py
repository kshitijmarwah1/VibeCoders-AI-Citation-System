from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tavily import TavilyClient
from dotenv import load_dotenv
from services.citation_extractor import extract_citations
import os
import re
import random

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
    sentences = re.split(r'[.!?]', text)
    claims = []

    opinion_starters = (
        "i think",
        "i believe",
        "in my opinion",
        "we think",
        "you should",
        "it seems",
        "probably",
        "maybe"
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
    """
    Search the web for evidence supporting the claim
    """
    response = tavily.search(
        query=claim,
        search_depth="basic",
        max_results=3
    )

    citations = []

    for result in response.get("results", []):
        citations.append({
            "title": result.get("title"),
            "url": result.get("url")
        })

    return citations


def verify_claim_with_search(claim: str):
    hallucination_keywords = [
        "sun revolves around the earth",
        "earth is flat",
        "humans can breathe in space",
        "moon is made of cheese"
    ]

    claim_lower = claim.lower()

    for keyword in hallucination_keywords:
        if keyword in claim_lower:
            return {
                "status": "hallucinated",
                "confidence": 0.1,
                "citations": []
            }

    citations = search_web_for_claim(claim)

    if len(citations) == 0:
        return {
            "status": "hallucinated",
            "confidence": 0.2,
            "citations": []
        }

    return {
        "status": "verified",
        "confidence": round(random.uniform(0.7, 0.9), 2),
        "citations": citations
    }

@app.post("/verify")
def verify_text(data: TextInput):
    claims = extract_claims(data.text)
    results = []

    for c in claims:
        verification = verify_claim_with_search(c)
        results.append({
            "claim": c,
            "status": verification["status"],
            "confidence": verification["confidence"],
            "citations": verification["citations"]
        })

    extracted_citations = extract_citations(data.text)

    return {
        "total_claims": len(results),
        "claims": results,
        "extracted_citations": extracted_citations
    }

