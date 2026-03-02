# import faiss
# import numpy as np
# import json
# from sentence_transformers import SentenceTransformer

# MODEL_NAME = "all-MiniLM-L6-v2"
# INDEX_PATH = "data/faiss.index"
# META_PATH = "data/catalog_metadata.npy"

# model = SentenceTransformer(MODEL_NAME)
# index = faiss.read_index(INDEX_PATH)
# catalog = np.load(META_PATH, allow_pickle=True)

# def balance_results(results, query):
#     query_lower = query.lower()

#     wants_personality = any(word in query_lower for word in [
#         "collaborate", "team", "stakeholder", "personality", "behavior"
#     ])

#     wants_technical = any(word in query_lower for word in [
#         "java", "python", "sql", "technical", "developer", "engineer"
#     ])

#     wants_cognitive = any(word in query_lower for word in [
#         "cognitive", "analyst", "reasoning", "problem solving"
#     ])

#     final = []

#     # Always include top results first
#     for item in results:
#         if len(final) >= 10:
#             break
#         final.append(item)

#     # Optional balancing improvement
#     if wants_personality:
#         personality_items = [r for r in results if r["test_type"] == "P"]
#         final[:3] = personality_items[:3]

#     if wants_technical:
#         technical_items = [r for r in results if r["test_type"] == "K"]
#         final[3:6] = technical_items[:3]

#     if wants_cognitive:
#         cognitive_items = [r for r in results if r["test_type"] == "A"]
#         final[6:9] = cognitive_items[:3]

#     return final[:10]

# import re

# def tokenize(text):
#     return set(re.findall(r"\w+", text.lower()))

# def get_recommendations(query, top_k=100):
#     query_embedding = model.encode([query])
#     distances, indices = index.search(np.array(query_embedding), top_k)

#     query_tokens = tokenize(query)

#     results = []
#     seen_urls = set()

#     for idx in indices[0]:
#         item = catalog[idx]

#         if item["url"] in seen_urls:
#             continue
#         seen_urls.add(item["url"])

#         text = f"{item['title']} {item.get('description', '')}"
#         item_tokens = tokenize(text)

#         overlap_score = len(query_tokens.intersection(item_tokens))

#         results.append({
#             "title": item["title"],
#             "url": item["url"],
#             "test_type": item["test_type"],
#             "overlap_score": overlap_score
#         })

#     # Sort by overlap score descending
#     results = sorted(results, key=lambda x: x["overlap_score"], reverse=True)

#     return results[:10]
# # def get_recommendations(query, top_k=50):
# #     query_embedding = model.encode([query])
# #     distances, indices = index.search(np.array(query_embedding), top_k)

# #     results = []
# #     seen_urls = set()

# #     for idx in indices[0]:
# #         item = catalog[idx]

# #         # Remove duplicates
# #         if item["url"] in seen_urls:
# #             continue
# #         seen_urls.add(item["url"])

# #         results.append({
# #             "title": item["title"],
# #             "url": item["url"],
# #             "test_type": item["test_type"]
# #         })

# #     # balanced = balance_results(results, query)

# #     # # Final dedup safety
# #     # final = []
# #     # seen = set()
# #     # for r in balanced:
# #     #     if r["url"] not in seen:
# #     #         final.append(r)
# #     #         seen.add(r["url"])

# #     # return final[:10]
# #     return results[:10]


# if __name__ == "__main__":
#     test_query = "Looking to hire Java developers who collaborate with business teams"
#     recommendations = get_recommendations(test_query)

#     for r in recommendations:
#         print(r)

# import re
# import json

# def tokenize(text):
#     return set(re.findall(r"\w+", text.lower()))

# with open("data/raw_catalog.json") as f:
#     catalog = json.load(f)

# def get_recommendations(query, top_k=10):
#     query_tokens = tokenize(query)

#     scored = []

#     for item in catalog:
#         text = f"{item['title']} {item.get('description', '')}"
#         item_tokens = tokenize(text)

#         overlap = len(query_tokens.intersection(item_tokens))

#         scored.append({
#             "title": item["title"],
#             "url": item["url"],
#             "test_type": item["test_type"],
#             "score": overlap
#         })

#     # Sort by overlap score descending
#     scored = sorted(scored, key=lambda x: x["score"], reverse=True)

#     return scored[:top_k]

# import re
# import json
# from collections import Counter

# with open("data/raw_catalog.json") as f:
#     catalog = json.load(f)

# STOPWORDS = {
#     "i","am","for","the","and","a","an","of","to","who","can",
#     "also","with","in","is","this","that","looking","hiring",
#     "candidates","candidate","experience"
# }

# def tokenize(text):
#     return [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]

# # Build document frequency for simple IDF
# doc_freq = Counter()
# for item in catalog:
#     tokens = set(tokenize(item["title"] + " " + item.get("description","")))
#     for t in tokens:
#         doc_freq[t] += 1

# total_docs = len(catalog)

# def get_recommendations(query, top_k=10):
#     query_tokens = tokenize(query)

#     scored = []

#     for item in catalog:
#         text = item["title"] + " " + item.get("description","")
#         item_tokens = tokenize(text)

#         score = 0

#         for token in query_tokens:
#             if token in item_tokens:
#                 # simple IDF weight
#                 idf = total_docs / (1 + doc_freq[token])
#                 score += idf

#         # extra boost if token in title
#         title_tokens = tokenize(item["title"])
#         for token in query_tokens:
#             if token in title_tokens:
#                 score += 5  # strong boost

#         scored.append({
#             "title": item["title"],
#             "url": item["url"],
#             "test_type": item["test_type"],
#             "score": score
#         })

#     scored = sorted(scored, key=lambda x: x["score"], reverse=True)

#     return scored[:top_k]

import re
import json
import numpy as np
from collections import Counter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/raw_catalog.json") as f:
    catalog = json.load(f)

STOPWORDS = {
    "i","am","for","the","and","a","an","of","to","who","can",
    "also","with","in","is","this","that","looking","hiring",
    "candidates","candidate","experience"
}

def tokenize(text):
    return [w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS]

# Build IDF
doc_freq = Counter()
for item in catalog:
    tokens = set(tokenize(item["title"] + " " + item.get("description","")))
    for t in tokens:
        doc_freq[t] += 1

total_docs = len(catalog)

def keyword_score(query_tokens, item):
    text = item["title"] + " " + item.get("description","")
    item_tokens = tokenize(text)

    score = 0
    for token in query_tokens:
        if token in item_tokens:
            idf = total_docs / (1 + doc_freq[token])
            score += idf

    # boost title
    title_tokens = tokenize(item["title"])
    for token in query_tokens:
        if token in title_tokens:
            score += 5

    return score

def get_recommendations(query, top_k=10):
    query_tokens = tokenize(query)

    # Step 1: Keyword retrieve top 50
    scored = []
    for item in catalog:
        score = keyword_score(query_tokens, item)
        scored.append((item, score))

    scored = sorted(scored, key=lambda x: x[1], reverse=True)[:50]

    # Step 2: Semantic rerank on top 50
    query_embedding = model.encode([query])

    reranked = []
    for item, kw_score in scored:
        text = item["title"] + " " + item.get("description","")
        item_embedding = model.encode([text])

        sim = cosine_similarity(query_embedding, item_embedding)[0][0]

        final_score = kw_score + (sim * 10)  # weight semantic similarity

        reranked.append({
            "title": item["title"],
            "url": item["url"],
            "test_type": item["test_type"],
            "score": float(final_score)
        })  

    reranked = sorted(reranked, key=lambda x: x["score"], reverse=True)

    return reranked[:top_k]