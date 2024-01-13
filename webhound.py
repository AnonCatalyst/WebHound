import requests
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
from tqdm import tqdm
import time
import logging

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/html/?q=",
    "Bing": "https://www.bing.com/search?q=",
    "Yahoo": "https://search.yahoo.com/search?p=",
    "Ask": "https://www.ask.com/web?q=",
    "AOL": "https://search.aol.com/aol/search?q=",
    "Yandex": "https://www.yandex.com/search/?text=",
    "StartPage": "https://www.startpage.com/do/dsearch?query=",
    "Baidu": "https://www.baidu.com/s?wd=",
    # Add more search engines as needed
}

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)

    def make_request(self, url, retry_count=3):
        headers = {"User-Agent": self.ua.random}
        for _ in range(retry_count):
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to make a request to {url}: {e}")
                if retry_count > 0:
                    self.logger.warning(f"Retrying... {retry_count} attempts remaining.")
                    retry_count -= 1
                    time.sleep(2)  # Introduce delay before retry
                else:
                    self.logger.warning("Maximum retries reached. Moving on to the next step.")
                    return None

    def execute_search(self, query, engine):
        url = SEARCH_ENGINES.get(engine)
        if url:
            self.logger.info(f"Searching on {engine}...")
            try:
                search_url = f"{url}{quote(query)}"
                with ThreadPoolExecutor(max_workers=5) as executor:
                    search_urls = [f"{search_url}&start={i}" for i in range(0, 101, 10)]
                    results = list(tqdm(executor.map(lambda u: self.make_request(u, retry_count=3), search_urls), total=len(search_urls), desc="Progress"))

                if results and all(result is not None for result in results):
                    self.logger.info(f"Search on {engine} completed successfully!")
                    return results
                else:
                    self.logger.warning(f"No results found on {engine}. Please try another search.")
                    return []

            except requests.exceptions.RequestException as e:
                self.logger.error(f"An error occurred during the search on {engine}: {e}")
                return []

    def print_results(self, results, engine):
        if not results:
            self.logger.warning(f"No results from {engine}")
            return

        self.logger.info(f"\n{'🔍'*10} Results from {engine} {'🔍'*10}\n")

        visited_links = set()
        result_count = 0

        try:
            for page_content in results:
                for item in page_content.select("div.tF2Cxc, div.result, li.b_algo"):
                    title = item.select_one("h2, h3")
                    link = item.find("a")["href"]
                    description = item.select_one("div.IsZvec, p")

                    if link in visited_links:
                        continue

                    visited_links.add(link)
                    result_count += 1

                    title_text = title.text.strip() if title else "Title not available"
                    link_text = link if link else "Link not available"
                    description_text = description.text.strip() if description else "Description not available"

                    self.logger.info(f"\n{'🔹'*10} Result {result_count} {'🔹'*10}\n"
                                     f"{'📖 Title:':<15} {colored(title_text, 'yellow')}\n"
                                     f"{'🌐 URL:':<15} {colored(link_text, 'cyan')}\n"
                                     f"{'📝 Description:':<15} {colored(description_text, 'green')}\n"
                                     f"{'🔹'*40}\n")

        except Exception as e:
            self.logger.error(f"An error occurred while processing a search result: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    query = input(colored("🔍 Enter your query: ", "cyan"))
    scraper = WebScraper()

    all_results = []
    for engine in SEARCH_ENGINES:
        result = scraper.execute_search(query, engine)
        if result:
            all_results.extend(result)
    
    if all_results:
        scraper.print_results(all_results, "All Engines")
