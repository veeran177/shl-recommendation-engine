##SHL Assessment Recommendation Engine
🔹 #Problem Statement
Build an AI-based recommendation system to suggest relevant SHL assessments based on hiring queries.

🔹 #Project Architecture

1. Data Collection
Scraped 394 assessment product pages from SHL catalog.
Extracted:
Title
Description
Test Type
URL
Stored in JSON format.

2. Embedding & Indexing
Used SentenceTransformers for semantic embeddings.
Built FAISS index for efficient similarity search.
Stored index and metadata for reuse.

3. Retrieval Strategy (Hybrid Model)
Stage 1:
TF-IDF keyword retrieval (high recall candidate generation)
Stage 2:
Semantic reranking using SentenceTransformer
Cosine similarity scoring
Final Output:
Top 10 ranked recommendations per query

4. Evaluation
Dataset: 65 hiring queries
Coverage: 39/51 true slugs available in scraped catalog
Recall@50: ~0.47 (best observed)
Recall@10: ~0.12–0.20 depending on strategy
Observations:
Some ground truth URLs were solution pages not present in scraped catalog.
Performance limited by coverage ceiling.
Architecture supports future extension with dynamic scraping (Selenium).

5. API Layer
FastAPI endpoint:
GET /recommend?query=Hiring Java developers
Returns top 10 recommendations in JSON format.

6. How To Run
Install dependencies:
pip install -r requirements.txt
Run API:
uvicorn app.main:app --reload
Generate submission file:

python src/generate_submission.py# shl-recommendation-engine
