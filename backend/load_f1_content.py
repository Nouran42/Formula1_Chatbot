import requests
from bs4 import BeautifulSoup
import json



urls = [
    'https://en.wikipedia.org/wiki/Formula_One',
    'https://en.wikipedia.org/wiki/2026_Formula_One_World_Championship',
    'https://simple.wikipedia.org/wiki/Formula_One',
    'https://en.wikipedia.org/wiki/List_of_Formula_One_Grand_Prix_winners_(constructors)'
]

def clean_html(html):
    """Extract and clean text from HTML content."""
    soup = BeautifulSoup(html, 'html.parser')

    
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)

def fetch_pages(urls):
    contents = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            cleaned = clean_html(response.text)
            contents.append({"url": url, "text": cleaned})
            print(f"Fetched: {url}")
        except Exception as e:
            print(f"Failed: {url} - {e}")
    return contents

if __name__ == "__main__":
    docs = fetch_pages(urls)
    with open("scraped_f1_content.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)

    for i, doc in enumerate(docs):
        print(f"\n=== Page {i+1} from {doc['url']} ===")
        print(doc["text"][:500]) \

    print(f"Fetched and saved {len(docs)} documents to scraped_f1_content.json.")