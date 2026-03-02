import pandas as pd
from retriever import get_recommendations

DATA_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "submission.csv"

def extract_slug(url):
    return url.strip("/").split("/")[-1]

def generate():
    df = pd.read_excel(DATA_PATH)

    submission_rows = []

    for _, row in df.iterrows():
        query = row["Query"]

        results = get_recommendations(query)

        urls = [r["url"] for r in results]

        submission_rows.append({
            "Query": query,
            "Top_10_URLs": ", ".join(urls)
        })

    submission_df = pd.DataFrame(submission_rows)
    submission_df.to_csv(OUTPUT_PATH, index=False)

    print("Submission file created:", OUTPUT_PATH)

if __name__ == "__main__":
    generate()