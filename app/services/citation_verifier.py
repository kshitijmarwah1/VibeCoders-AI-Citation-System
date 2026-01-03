import requests

def verify_dois(dois):
    verified = []
    fake = []

    for doi in dois:
        try:
            r = requests.get(f"https://api.crossref.org/works/{doi}", timeout=5)
            if r.status_code == 200:
                verified.append(doi)
            else:
                fake.append(doi)
        except:
            fake.append(doi)

    return verified, fake
