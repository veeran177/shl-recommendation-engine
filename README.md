# **Overview**
This project implements a hybrid AI-powered recommendation system that suggests relevant SHL assessments based on hiring queries.
The system combines traditional keyword-based retrieval with semantic embedding-based reranking to improve relevance and robustness.

## **Problem Statement**
Build an AI-based recommendation engine that:
Takes a hiring query as input
Returns the Top 10 most relevant SHL assessments
Evaluates performance using recall metrics
Provides an API endpoint for real-time access

## **System Architecture**
### 1. Data Collection
Scraped 394 assessment product pages from SHL’s product catalog
Extracted structured metadata:
Title
Description
Test Type
URL
Stored in raw_catalog.json

### 2️. Embeddings & Indexing
Used SentenceTransformers to generate semantic embeddings
Built a FAISS vector index for efficient similarity search
Stored:
faiss.index
catalog_metadata.npy
This enables scalable semantic retrieval.

### 3️. Hybrid Retrieval Strategy
The recommendation system uses a two-stage hybrid pipeline:
Stage 1 – Candidate Generation (High Recall)
TF-IDF keyword retrieval
Retrieves top candidate assessments based on lexical similarity
Stage 2 – Semantic Reranking
SentenceTransformer embeddings
Cosine similarity scoring
Reranks candidates for contextual relevance
Final Output
Top 10 ranked assessments returned per query

## **Evaluation**
Evaluation was performed using 65 hiring queries.
Dataset Coverage Analysis
51 unique ground-truth slugs in dataset
39 found in scraped catalog
Some solution pages were dynamically rendered and not scrapeable via static crawling

## **Performance**
Recall@50: ~0.47 (best observed)
Recall@10: ~0.12–0.20 depending on configuration

## **Observations**
Performance limited by dataset coverage ceiling
Hybrid retrieval improved ranking quality
System design supports extension via dynamic scraping (Selenium / Playwright)

## **API Layer**
Built using FastAPI
Endpoint
GET /recommend?query=Hiring Java developers
Example Response
{
  "query": "Hiring Java developers",
  "recommendations": [
    {
      "title": "Java 2 Platform Enterprise Edition 1.4 Fundamental",
      "url": "...",
      "test_type": "K",
      "score": 0.82
    }
  ]
}

## **How To Run Locally**
### 1️. Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
### 2️. Install Dependencies
pip install -r requirements.txt
### 3. Run API
uvicorn app.main:app --reload
Visit:
http://127.0.0.1:8000/recommend?query=Hiring Java developers
### 4. Generate Submission File
python src/generate_submission.py

This creates:
submission.csv
Project Structure
shl-recommendation-engine/
│
├── app/
│   └── main.py
│
├── data/
│   ├── raw_catalog.json
│   ├── Gen_AI Dataset.xlsx
│   ├── faiss.index
│   └── catalog_metadata.npy
│
├── src/
│   ├── scraper.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── evaluation.py
│   └── generate_submission.py
│
├── submission.csv
├── requirements.txt
└── README.md

## **Engineering Highlights**
Full end-to-end ML pipeline
Hybrid retrieval architecture
FAISS vector indexing
Evaluation framework
REST API deployment
Modular and extensible design

## **Future Improvements**
Dynamic solution page scraping using Selenium
Metadata enrichment (skills, job family tags)
Learning-to-rank reranker
Query expansion using LLM techniques
Deployment to cloud (Render / Railway / AWS)
