import spacy

nlp = spacy.load("en_core_web_sm")

def extract_claims(text: str):
    doc = nlp(text)
    claims = []
    for sent in doc.sents:
        if len(sent.ents) > 0:
            claims.append(sent.text.strip())
    return claims
