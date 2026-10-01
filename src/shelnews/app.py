from dataclasses import asdict

from fastapi import FastAPI
from pydantic import BaseModel

from .classifier import classify

app = FastAPI(title="SHEL News API")


class ClassifyRequest(BaseModel):
    headline: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify")
def classify_headline(req: ClassifyRequest):
    return asdict(classify(req.headline))
