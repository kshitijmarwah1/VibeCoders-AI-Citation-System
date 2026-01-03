 **Read this completely before modifying any code.  
 This project is production-oriented. Do NOT simplify logic or remove safeguards.**

* * *

## 🔷 PROJECT NAME (Working Title)

**Universal AI Hallucination & Citation Verification System**

* * *

## 🔷 HIGH-LEVEL GOAL

This project is a **generic, domain-aware, multi-input AI verification system** designed to:

* Detect hallucinations in AI-generated or human-written content
    
* Verify factual claims using real web sources
    
* Assign confidence scores
    
* Detect contradictions across sources
    
* Provide explainable, human-readable reasoning
    
* Work for **any user**, **any domain**, **any input format**
    
* Use **only pretrained, free, open-source models**
    
* Be **multi-user safe** (no per-user customization)
    

This is **NOT** a chatbot.  
This is **NOT** a fine-tuned per-user system.

This is a **universal verification engine**, similar in spirit to:

* VirusTotal (but for claims)
    
* Plagiarism detectors
    
* AI safety middleware
    

* * *

## 🔷 CORE DESIGN PRINCIPLES (DO NOT VIOLATE)

1. **Deterministic Core**
    
    * Verification decisions must come from deterministic logic:
        
        * similarity scores
            
        * credibility weighting
            
        * contradiction detection
            
    * LLMs must NEVER decide truth.
        
2. **LLMs Are Advisory Only**
    
    * LLMs are used ONLY for:
        
        * explanations
            
        * reasoning summaries
            
    * They must NOT:
        
        * override status
            
        * modify confidence
            
        * introduce new claims
            
3. **Single Unified Verification Pipeline**
    
    * All inputs (text, PDF, URL, DOCX, batch) must funnel into:
        
        ```
        normalized_text → claim extraction → verification
        ```
        
4. **Domain-Aware, Not User-Aware**
    
    * Domains (medical, finance, legal, etc.) influence thresholds and models
        
    * Users do NOT influence logic or configuration
        
5. **Pretrained-Only Mode**
    
    * No training data
        
    * No fine-tuning
        
    * All models are loaded from Hugging Face or similar public sources
        
    * Architecture is fine-tuning ready, but disabled by design
        

* * *

## 🔷 CURRENT PROJECT STAGE

### ✅ STATUS: **Production-Ready MVP**

The system already supports:

* Claim extraction & filtering
    
* Semantic similarity using Sentence Transformers
    
* Web grounding via search
    
* Credibility weighting by domain
    
* Contradiction detection
    
* Domain detection (ML-based + fallback)
    
* Overall reliability scoring
    
* Multi-format input support
    
* LLM-based explanations (non-authoritative)
    
* Clean service-based backend architecture
    

* * *

## 🔷 BACKEND ARCHITECTURE OVERVIEW

```
services/
│
├── api/                    # FastAPI layer (routes only)
│   ├── main.py
│   └── routers/
│       └── verify.py
│
├── core/                   # ALL business logic lives here
│   ├── input/              # Multi-format input adapters
│   │   ├── text.py
│   │   ├── pdf.py
│   │   ├── docx.py
│   │   ├── url.py
│   │   ├── batch.py
│   │   └── normalize.py
│   │
│   ├── claims/
│   │   ├── extractor.py          # Claim extraction + filtering
│   │   ├── domain_detector.py    # ML-based domain detection
│   │   └── domain_classifier.py  # Pretrained classifier helper
│   │
│   ├── verification/
│   │   ├── search.py             # Web search + snippets
│   │   ├── semantic.py           # Similarity computation
│   │   ├── contradiction.py      # Cross-source conflict detection
│   │   ├── model_registry.py     # Pretrained model loader
│   │   └── verify.py             # CORE orchestration logic
│   │
│   ├── scoring/
│   │   ├── domain.py             # Domain credibility weights
│   │   ├── credibility.py        # Credibility score
│   │   └── aggregation.py        # Overall reliability score
│   │
│   ├── explainability/
│   │   └── traces.py             # Citation extraction
│   │
│   └── llm/
│       └── reasoner.py            # LLM explanation (advisory only)
│
├── config/
│   ├── settings.py               # Env vars
│   ├── domain_loader.py          # YAML loader
│   └── domains/                  # Domain configs
│       ├── general.yaml
│       ├── medical.yaml
│       ├── finance.yaml
│       ├── legal.yaml
│       └── technology.yaml
│
└── storage/
    └── cache.py                  # Global cache
```

* * *

## 🔷 VERIFICATION PIPELINE (STEP-BY-STEP)

**THIS IS THE MOST IMPORTANT PART — DO NOT BREAK THIS FLOW**

```
User Input (any format)
   ↓
Input Normalization (text/PDF/URL/DOCX)
   ↓
Claim Extraction
   ↓
Domain Detection (ML-based)
   ↓
For each claim:
   ├─ Web Search (sources + snippets)
   ├─ Semantic Similarity (domain model)
   ├─ Credibility Weighting (domain YAML)
   ├─ Contradiction Detection
   ├─ Final Confidence Score
   ├─ Status: verified / hallucinated
   └─ LLM Explanation (optional, advisory)
   ↓
Overall Reliability Score
   ↓
Final Response
```

* * *

## 🔷 DOMAIN SYSTEM (VERY IMPORTANT)

Domains affect:

* Similarity thresholds
    
* Contradiction penalties
    
* Credibility weights
    
* Embedding model choice
    

Domains are defined in **YAML**, not code.

Example fields:

```yaml
similarity_threshold
contradiction_threshold
contradiction_penalty
trusted_domains
credibility_weights
```

DO NOT hardcode thresholds in Python.

* * *

## 🔷 LLM INTEGRATION RULES

* LLMs are ONLY used in `core/llm/reasoner.py`
    
* LLM output is **pure explanation**
    
* LLM must not:
    
    * change status
        
    * change confidence
        
    * add facts
        
* If LLM fails → system still works
    

* * *

## 🔷 MULTI-USER SAFETY

* System is stateless per request
    
* No user sessions
    
* No personalization
    
* Cache is global and safe
    
* API is concurrency-safe
    

* * *

## 🔷 WHAT NOT TO DO (VERY IMPORTANT)

❌ Do NOT:

* Merge verification + explanation logic
    
* Let LLM decide correctness
    
* Add user-specific configs
    
* Remove domain YAMLs
    
* Hardcode thresholds
    
* Collapse files back into one file
    

* * *

## 🔷 WHAT IS SAFE TO EXTEND

✅ Safe future extensions:

* Frontend UX
    
* Async workers
    
* More input formats
    
* More pretrained models
    
* Deployment optimizations
    
* Better explanation prompts
    

* * *

## 🔷 EXPECTED OUTPUT STRUCTURE

Every verification response must include:

```json
{
  "domain": "...",
  "total_claims": 0,
  "overall_reliability": 0.0,
  "claims": [
    {
      "claim": "...",
      "status": "verified | hallucinated",
      "confidence": 0.0,
      "similarity": 0.0,
      "credibility": 0.0,
      "contradicted": false,
      "citations": [],
      "explanation": "..."
    }
  ]
}
```

* * *

## 🔷 FINAL INSTRUCTION TO AI ASSISTANT (IMPORTANT)

 When modifying this project:
 * Preserve architecture
 * Preserve verification logic  
 * Never simplify safety checks     
 * Ask before removing any module    
 * Treat this as a production system, not a demo
 