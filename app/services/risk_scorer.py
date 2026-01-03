def calculate_risk(unverified_claims, fake_citations, broken_links):
    score = (
        0.4 * unverified_claims +
        0.4 * fake_citations +
        0.2 * broken_links
    )
    return round(min(score, 1.0), 2)
