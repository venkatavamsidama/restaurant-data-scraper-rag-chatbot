import os
from concurrent.futures import ThreadPoolExecutor
from browser import get_webdriver
from storage import save_page, append_metadata
from utils import rate_limit
from config.settings import RAW_DIR


class RawScraper:
    def __init__(self, urls: list[str], workers: int = 5):
        self.urls = urls
        self.workers = workers
        os.makedirs(RAW_DIR, exist_ok=True)

    @rate_limit(delay=1.0)
    def _fetch(self, url: str) -> None:
        driver = get_webdriver()
        driver.get(url)
        html = driver.page_source
        driver.quit()

        filename = f"{url.split('//')[-1].replace('/', '_')}.html"
        save_page(filename, html)
        append_metadata({'url': url, 'file': filename})

    def run(self) -> None:
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            pool.map(self._fetch, self.urls)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    with open('config/urls.txt') as f:
        urls = [line.strip() for line in f if line.strip()]

    scraper = RawScraper(urls)
    scraper.run()
    print(f"Scraped {len(urls)} pages into {RAW_DIR}.")