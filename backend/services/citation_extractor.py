import re

def extract_citations(text: str):
    doi_pattern = r"10\.\d{4,9}/[-._;()/:A-Z0-9]+"
    url_pattern = r"https?://\S+"

    return {
        "dois": re.findall(doi_pattern, text, re.I),
        "urls": re.findall(url_pattern, text)
    }
