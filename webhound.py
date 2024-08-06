import requests
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
from tqdm import tqdm
import random
import time
import logging
import json
from detect import DetectionHandler  

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
}

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)
        self.detection_handler = DetectionHandler('social_platforms.json')  # Initialize DetectionHandler

    def make_request(self, url, retry_count=3):
        headers = {"User-Agent": self.ua.random}
        for attempt in range(retry_count):
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to make a request to {url}: {e}")
                if attempt < retry_count - 1:
                    self.logger.warning(f"Retrying... {retry_count - attempt - 1} attempts remaining.")
                    time.sleep(random.uniform(2, 5))  # Introduce random delay before retry
                else:
                    self.logger.warning("Maximum retries reached. Moving on to the next step.")
                    return None

    def execute_search(self, query, engine):
        url = SEARCH_ENGINES.get(engine)
        if not url:
            self.logger.warning(f"Search engine '{engine}' is not supported.")
            return []

        self.logger.info(f"Searching on {engine}...")
        try:
            search_url = f"{url}{quote(query)}"
            search_urls = [f"{search_url}&start={i}" for i in range(0, 101, 10)]
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(self.make_request, u) for u in search_urls]
                results = []
                for future in tqdm(as_completed(futures), total=len(futures), desc=f"Progress ({engine})"):
                    result = future.result()
                    if result:
                        results.append(result)
                    time.sleep(random.uniform(1, 3))  # Introduce random delay to mimic human behavior

            if results:
                self.logger.info(f"Search on {engine} completed successfully!")
                return results
            else:
                self.logger.warning(f"No results found on {engine}.")
                return []

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred during the search on {engine}: {e}")
            return []

    def analyze_content(self, page_content, query):
        types_keywords = {
            "forum": ["forum", "board", "community"],
            "news": ["news", "breaking", "headline"]
        }
        detection_result = self.detection_handler.enhanced_detection(page_content, query, types_keywords)
        return detection_result


    def print_results(self, results, engine, query):
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

                    page_text = item.text.strip()
                    detection_result = self.analyze_content(page_text, query)

                    # Only print details if they meet the criteria
                    result_details = f"\n{'🔹'*10} Result {result_count} {'🔹'*10}\n"
                    result_details += f"{'📖 Title:':<15} {colored(title_text, 'yellow')}\n"
                    result_details += f"{'🌐 URL:':<15} {colored(link_text, 'cyan')}\n"
                    result_details += f"{'📝 Description:':<15} {colored(description_text, 'green')}\n"

                    if detection_result['is_forum']:
                        result_details += f"{'Forum:':<15} {colored(detection_result['is_forum'], 'magenta')}\n"
                    if detection_result['is_news']:
                        result_details += f"{'News:':<15} {colored(detection_result['is_news'], 'magenta')}\n"
                    if detection_result['query_mentions'] > 1:
                        result_details += f"{'Query Mentions:':<15} {colored(detection_result['query_mentions'], 'magenta')}\n"
                    if detection_result['social_platforms_detected']:
                        result_details += f"{'Social Platforms:':<15} {colored(', '.join(detection_result['social_platforms_detected']), 'magenta')}\n"

                    result_details += f"{'🔹'*40}\n"

                    self.logger.info(result_details)

        except Exception as e:
            self.logger.error(f"An error occurred while processing a search result: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    query = input(colored("🔍 Enter your query: ", "cyan"))
    scraper = WebScraper()

    all_results = []  # List to accumulate all search results

    # Execute searches in parallel
    with ThreadPoolExecutor(max_workers=len(SEARCH_ENGINES)) as executor:
        futures = {executor.submit(scraper.execute_search, query, engine): engine for engine in SEARCH_ENGINES}
        for future in as_completed(futures):
            engine = futures[future]
            result = future.result()
            if result:
                all_results.extend(result)  # Accumulate results from all engines

    # Print results from each engine
    if all_results:
        scraper.print_results(all_results, "All Engines", query)

