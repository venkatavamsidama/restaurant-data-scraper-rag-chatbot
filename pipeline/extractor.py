import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_fields(base_url: str) -> dict:
    """Extracts HTML from all pages starting from base_url without JavaScript."""
    visited = set()
    all_html = []

    def fetch_and_clean(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for script in soup(['script']):
            script.extract()
        return soup

    def crawl(url):
        if url in visited:
            return
        visited.add(url)
        
        soup = fetch_and_clean(url)
        all_html.append(soup.prettify())
        
        # Find all <a> links
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            # Only crawl if it is a valid HTTP(S) URL and not already visited
            if next_url.startswith('http') and next_url not in visited:
                crawl(next_url)

    crawl(base_url)
    
    return {'full_html': "\n".join(all_html)}
