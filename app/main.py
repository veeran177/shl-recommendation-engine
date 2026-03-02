import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi import FastAPI
from retriever import get_recommendations

app = FastAPI(title="SHL Recommendation Engine")

@app.get("/")
def home():
    return {"message": "SHL Assessment Recommendation API"}

@app.get("/recommend")
def recommend(query: str):
    results = get_recommendations(query)
    return {"query": query, "recommendations": results}