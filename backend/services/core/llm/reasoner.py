from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Load once (VERY IMPORTANT) - lazy loading to avoid startup failures
_reasoning_pipeline = None
_reasoning_model = None
_reasoning_tokenizer = None

def _get_reasoning_pipeline():
    """Lazy load the reasoning pipeline with a better model."""
    global _reasoning_pipeline, _reasoning_model, _reasoning_tokenizer
    if _reasoning_pipeline is None:
        try:
            # Use CPU-only for stability
            try:
                _reasoning_pipeline = pipeline(
                    "text2text-generation",
                    model="google/flan-t5-base",
                    max_length=256,
                    device=-1  # CPU only
                )
                logger.info("Loaded reasoning model: google/flan-t5-base")
            except Exception as e:
                logger.warning(f"Failed to load reasoning model: {e}")
                return None
        except Exception as e:
            logger.error(f"Failed to load reasoning pipeline: {e}")
            return None
    return _reasoning_pipeline

def generate_explanation(
    claim: str,
    status: str,
    confidence: float,
    citations: list[dict],
    similarity: float = 0.0,
    credibility: float = 0.0,
    contradicted: bool = False
) -> str:
    """
    Generate a human-readable, detailed explanation.
    This NEVER changes verification result.
    If LLM fails, returns a deterministic explanation.
    """
    try:
        pipeline = _get_reasoning_pipeline()
        if pipeline is None:
            return _generate_deterministic_explanation(claim, status, confidence, citations, similarity, credibility, contradicted)

        # Build source list with titles
        sources_list = []
        for cite in citations[:3]:
            title = cite.get("title", "")
            url = cite.get("url", "")
            if title and title != "Untitled":
                sources_list.append(title)
            elif url:
                sources_list.append(url.split("/")[-1] if "/" in url else url)
        
        sources_text = ", ".join(sources_list) if sources_list else "No reliable sources found"

        # Create a detailed, structured prompt
        contradicted_note = "- Note: Some sources contradict this claim" if contradicted else ""
        
        if status == "verified":
            prompt = f"""Task: Explain why this claim is verified.

Claim: "{claim}"

Verification Details:
- Status: VERIFIED
- Confidence Score: {confidence:.2f} (on scale 0-1)
- Similarity to Sources: {similarity:.2f}
- Source Credibility: {credibility:.2f}
- Sources Found: {sources_text}
{contradicted_note}

Generate a clear, concise explanation (2-3 sentences) that:
1. States the claim is verified
2. Mentions the confidence level and why
3. References the sources found
4. Avoids repeating the claim verbatim

Explanation:"""
        else:
            sources_display = sources_text if sources_text != "No reliable sources found" else "Limited or no reliable sources"
            prompt = f"""Task: Explain why this claim appears to be hallucinated or unverified.

Claim: "{claim}"

Verification Details:
- Status: HALLUCINATED/UNVERIFIED
- Confidence Score: {confidence:.2f} (on scale 0-1, low indicates unverified)
- Similarity to Sources: {similarity:.2f} (low similarity suggests no supporting evidence)
- Source Credibility: {credibility:.2f}
- Sources Found: {sources_display}
{contradicted_note}

Generate a clear, concise explanation (2-3 sentences) that:
1. States the claim is unverified or potentially incorrect
2. Explains why (low similarity, lack of sources, or contradictions)
3. Mentions what evidence was found (or lack thereof)
4. Avoids repeating the claim verbatim

Explanation:"""

        # Generate with CPU-safe parameters
        output = pipeline(
            prompt,
            max_length=200,
            min_length=30,
            do_sample=False,  # Deterministic for stability
            num_return_sequences=1
        )
        
        # Safely extract text from output
        if isinstance(output, list) and len(output) > 0:
            if isinstance(output[0], dict):
                explanation = output[0].get("generated_text", "").strip()
            else:
                explanation = str(output[0]).strip()
        else:
            explanation = str(output).strip()
        
        # Clean up explanation
        explanation = explanation.replace("Explanation:", "").strip()
        explanation = explanation.replace("explanation:", "").strip()
        
        # Ensure explanation is meaningful and not just repeating the claim
        if not explanation or len(explanation) < 20:
            raise ValueError("Explanation too short or empty")
        
        # Check if explanation is just repeating the claim
        claim_words = set(claim.lower().split()[:5])  # First 5 words
        explanation_words = set(explanation.lower().split()[:5])
        overlap = len(claim_words.intersection(explanation_words))
        
        if overlap >= 3 and len(explanation.split()) < 15:
            # Too similar to claim, generate deterministic instead
            logger.warning("Generated explanation too similar to claim, using deterministic")
            return _generate_deterministic_explanation(claim, status, confidence, citations, similarity, credibility, contradicted)
            
        return explanation
    except Exception as e:
        logger.warning(f"Explanation generation failed: {e}")
        return _generate_deterministic_explanation(claim, status, confidence, citations, similarity, credibility, contradicted)


def _generate_deterministic_explanation(
    claim: str,
    status: str,
    confidence: float,
    citations: list[dict],
    similarity: float = 0.0,
    credibility: float = 0.0,
    contradicted: bool = False
) -> str:
    """Generate a deterministic, detailed explanation."""
    source_count = len(citations)
    
    if status == "verified":
        if contradicted:
            return f"This claim is verified with {confidence:.2f} confidence, though some sources present conflicting information. " \
                   f"Similarity to reliable sources is {similarity:.2f}, with source credibility of {credibility:.2f}. " \
                   f"Found {source_count} source(s) supporting this claim."
        else:
            return f"This claim is verified with {confidence:.2f} confidence. " \
                   f"The claim shows {similarity:.2f} similarity to reliable sources with {credibility:.2f} credibility score. " \
                   f"Verification is based on {source_count} source(s) that support this statement."
    else:
        if contradicted:
            return f"This claim appears to be unverified or incorrect (confidence: {confidence:.2f}). " \
                   f"Sources contradict this claim, with only {similarity:.2f} similarity to reliable information. " \
                   f"Found {source_count} source(s), but they do not support this claim."
        else:
            return f"This claim appears to be unverified or potentially incorrect (confidence: {confidence:.2f}). " \
                   f"Limited similarity ({similarity:.2f}) to reliable sources and low credibility ({credibility:.2f}) suggest insufficient evidence. " \
                   f"Only {source_count} source(s) found, and they do not strongly support this claim."
