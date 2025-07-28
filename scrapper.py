import requests
from bs4 import BeautifulSoup
import re
import json

# Load URLs from file
with open('data/urls.txt') as f:
    urls = [line.strip() for line in f if line.strip()]

data = []

for url in urls:
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        main = soup.find('main') or soup  # fallback if <main> not available
        text = main.get_text(" ", strip=True)
        text = re.sub(r'\s+', ' ', text)
        # Split by paragraphs/headings or 500-1000 char chunks
        chunks = [text[i:i+700] for i in range(0, len(text), 700)]
        for chunk in chunks:
            if len(chunk) > 50:  # skip very small ones
                data.append({"url": url, "content": chunk})
    except Exception as e:
        print(f"Error scraping {url}: {e}")

with open('vectors/raw_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Scraped {len(data)} chunks.")

