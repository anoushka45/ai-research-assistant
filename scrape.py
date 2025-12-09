# scrape.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "ai-research-assistant/0.1 (+https://github.com/anoushka45)"
}

def is_same_domain(base_url, target_url):
    return urlparse(base_url).netloc == urlparse(target_url).netloc

def scrape_text_from_url(url, max_chars=4000):
    """
    Fetch page and return cleaned visible text (truncated to max_chars).
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch URL: {e}")

    soup = BeautifulSoup(resp.text, "html.parser")

    # remove script/style/external nav footers to reduce noise
    for tag in soup(["script", "style", "nav", "footer", "aside", "form"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    # collapse whitespace
    text = " ".join(text.split())
    return text[:max_chars]
