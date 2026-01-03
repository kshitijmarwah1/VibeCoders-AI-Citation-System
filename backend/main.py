from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import random

app = FastAPI()

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

def fake_verify_claim(claim: str):
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
                "confidence": round(random.uniform(0.05, 0.3), 2),
                "citations": []
            }

    # Fake citations for verified claims
    fake_citations = [
        {
            "title": "Wikipedia",
            "url": "https://en.wikipedia.org"
        },
        {
            "title": "Britannica",
            "url": "https://www.britannica.com"
        }
    ]

    return {
        "status": "verified",
        "confidence": round(random.uniform(0.75, 0.95), 2),
        "citations": fake_citations
    }

@app.post("/verify")
def verify_text(data: TextInput):
    claims = extract_claims(data.text)
    results = []

    for c in claims:
        verification = fake_verify_claim(c)
        results.append({
                "claim": c,
                "status": verification["status"],
                "confidence": verification["confidence"],
                "citations": verification["citations"]
        })


    return {
        "total_claims": len(results),
        "claims": results
    }
