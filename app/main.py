from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="AI Hallucination & Citation Verification API",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "AI Hallucination & Citation Verification API is running"}

# 3️⃣ Include router
app.include_router(router)
