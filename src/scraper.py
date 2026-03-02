# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import json
# import time

# BASE_URL = "https://www.shl.com"
# CATALOG_URL = "https://www.shl.com/products/product-catalog/?start={}"

# headers = {
#     "User-Agent": "Mozilla/5.0"
# }

# session = requests.Session()
# session.headers.update(headers)

# def scrape_catalog():
#     all_links = set()
#     start = 0

#     while True:
#         print(f"Scraping listing page starting at {start}...")
#         url = CATALOG_URL.format(start)
#         response = session.get(url)

#         if response.status_code != 200:
#             break

#         soup = BeautifulSoup(response.text, "html.parser")

#         page_links = 0

#         for link in soup.find_all("a", href=True):
#             href = link["href"]
#             if "/products/product-catalog/view/" in href:
#                 full_url = urljoin(BASE_URL, href)
#                 if full_url not in all_links:
#                     all_links.add(full_url)
#                     page_links += 1

#         if page_links == 0:
#             break

#         start += 12
#         time.sleep(1)

#     print(f"Total product pages collected: {len(all_links)}")
#     return list(all_links)


# def scrape_details(product_urls):
#     results = []

#     for idx, url in enumerate(product_urls):
#         print(f"Processing {idx+1}/{len(product_urls)}")

#         try:
#             response = session.get(url)
#             soup = BeautifulSoup(response.text, "html.parser")

#             title_tag = soup.find("h1")
#             title = title_tag.text.strip() if title_tag else ""

#             desc_tag = soup.find("div", class_="product-catalogue-training-calendar__row")
#             description = desc_tag.text.strip() if desc_tag else ""

#             test_type_tag = soup.find("span", class_="product-catalogue__key")
#             test_type = test_type_tag.text.strip() if test_type_tag else ""

#             if test_type not in ["A", "K", "P"]:
#                 continue

#             results.append({
#                 "title": title,
#                 "description": description,
#                 "test_type": test_type,
#                 "url": url
#             })

#             time.sleep(1)

#         except Exception:
#             continue

#     print(f"Total valid assessments: {len(results)}")
#     return results


# if __name__ == "__main__":
#     links = scrape_catalog()
#     data = scrape_details(links)

#     with open("data/raw_catalog.json", "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=2)

#     print("Saved to data/raw_catalog.json")


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_solution_products():
    solution_url = "https://www.shl.com/solutions/products/"
    response = requests.get(solution_url, headers=headers)

    if response.status_code != 200:
        print("Failed to load solutions page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=True)

    solution_links = set()

    for link in links:
        href = link["href"]

        if "/solutions/products/" in href and href.count("/") > 3:
            full_url = urljoin(BASE_URL, href)
            solution_links.add(full_url)

    print(f"Found {len(solution_links)} solution product links")
    return list(solution_links)

def scrape_solution_details(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.text.strip() if title_tag else "No Title"

    description_tag = soup.find("p")
    description = description_tag.text.strip() if description_tag else ""

    return {
        "title": title,
        "description": description,
        "test_type": "Solution",  # mark separately
        "url": url
    }


import json

def merge_solution_products():
    with open("data/raw_catalog.json") as f:
        catalog = json.load(f)

    existing_urls = set(item["url"] for item in catalog)

    solution_links = scrape_solution_products()

    for link in solution_links:
        if link in existing_urls:
            continue

        details = scrape_solution_details(link)
        if details:
            catalog.append(details)
            print("Added:", details["title"])

    print("New total catalog size:", len(catalog))

    with open("data/raw_catalog.json", "w") as f:
        json.dump(catalog, f, indent=2)

if __name__ == "__main__":
    merge_solution_products()