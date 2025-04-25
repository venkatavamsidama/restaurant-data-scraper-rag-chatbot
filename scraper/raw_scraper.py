import os
from concurrent.futures import ThreadPoolExecutor
from scraper.browser import get_webdriver
from scraper.storage import save_page, append_raw_metadata
from scraper.utils import rate_limit
from config.settings import RAW_DIR


class RawScraper:
    def __init__(self, urls: list[str], workers: int = 5):
        self.urls = urls
        self.workers = workers

    @rate_limit(delay=1.0)
    def _fetch(self, url: str) -> None:
        driver = get_webdriver()
        driver.get(url)
        html = driver.page_source
        driver.quit()

        filename = f"{url.split('//')[-1].replace('/', '_')}.html"
        save_page(filename, html)
        print(f"Saved {filename} from {html}")
        append_raw_metadata({'url': url, 'file': filename})

    def run(self) -> None:
        os.makedirs(RAW_DIR, exist_ok=True)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            pool.map(self._fetch, self.urls)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    with open('config/urls.txt') as f:
        urls = [u.strip() for u in f if u.strip()]
    RawScraper(urls).run()
    print(f"Scraped {len(urls)} pages into {RAW_DIR}.")