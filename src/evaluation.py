import pandas as pd
from retriever import get_recommendations

DATA_PATH = "data/Gen_AI Dataset.xlsx"

def extract_slug(url):
    return url.strip("/").split("/")[-1]

# def evaluate():
#     df = pd.read_excel(DATA_PATH)

#     total = len(df)
#     hits = 0

#     for _, row in df.iterrows():
#         query = row["Query"]
#         true_url = row["Assessment_url"]

#         true_slug = extract_slug(true_url)

#         recommendations = get_recommendations(query)
#         recommended_slugs = [extract_slug(r["url"]) for r in recommendations]

#         if true_slug in recommended_slugs:
#             hits += 1

#     recall_at_10 = hits / total

#     print(f"Total Queries: {total}")
#     print(f"Correct Hits: {hits}")
#     print(f"Recall@10: {recall_at_10:.4f}")

def evaluate():
    df = pd.read_excel(DATA_PATH)

    total = len(df)
    hits_at_10 = 0
    hits_at_50 = 0

    for _, row in df.iterrows():
        query = row["Query"]
        true_slug = extract_slug(row["Assessment_url"])

        recommendations_50 = get_recommendations(query, top_k=100)
        recommended_slugs_50 = [extract_slug(r["url"]) for r in recommendations_50]

        if true_slug in recommended_slugs_50[:10]:
            hits_at_10 += 1

        if true_slug in recommended_slugs_50:
            hits_at_50 += 1

    print("Recall@10:", hits_at_10 / total)
    print("Recall@50:", hits_at_50 / total)

if __name__ == "__main__":
    evaluate()


# import pandas as pd
# import json

# def extract_slug(url):
#     return url.strip("/").split("/")[-1]

# # Load dataset
# df = pd.read_excel("data/Gen_AI Dataset.xlsx")
# true_slugs = set(extract_slug(u) for u in df["Assessment_url"])

# # Load scraped catalog
# with open("data/raw_catalog.json") as f:
#     catalog = json.load(f)

# catalog_slugs = set(extract_slug(item["url"]) for item in catalog)

# intersection = true_slugs.intersection(catalog_slugs)

# print("Total unique true slugs:", len(true_slugs))
# print("Slugs found in catalog:", len(intersection))