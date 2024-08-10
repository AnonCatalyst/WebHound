
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
from typing import List, Dict, Optional

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/html/?q=",
    "StartPage": "https://www.startpage.com/do/dsearch?query=",
    "Bing": "https://www.bing.com/search?q=",
}

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)
        self.detection_handler = DetectionHandler('social_platforms.json')  # Initialize DetectionHandler

    def make_request(self, url: str, retry_count: int = 3) -> Optional[BeautifulSoup]:
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
                    time.sleep(random.uniform(1, 3))  # Shorter random delay before retry
                else:
                    self.logger.warning("Maximum retries reached. Moving on to the next step.")
                    return None

    def execute_search(self, query: str, engines: List[str], date_range: Optional[str], language: Optional[str], country: Optional[str]) -> Dict[str, List[BeautifulSoup]]:
        results = {}
        
        # Search all engines at the same time
        with ThreadPoolExecutor(max_workers=len(engines)) as executor:
            futures = {
                executor.submit(self.search_engine, engine, query, date_range, language, country): engine
                for engine in engines
            }
            
            for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Search Engines"):
                engine = futures[future]
                engine_results = future.result()
                if engine_results:
                    results[engine] = engine_results
                else:
                    self.logger.warning(f"No results from {engine}.")
        
        return results

    def search_engine(self, engine: str, query: str, date_range: Optional[str], language: Optional[str], country: Optional[str]) -> List[BeautifulSoup]:
        url = SEARCH_ENGINES.get(engine)
        if not url:
            self.logger.warning(f"Search engine '{engine}' is not supported.")
            return []

        self.logger.info(f"Searching on {engine}...")
        try:
            search_url = f"{url}{quote(query)}"
            search_urls = [f"{search_url}&start={i}" for i in range(0, 101, 10)]
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(self.make_request, u) for u in search_urls]
                results = []
                for future in tqdm(as_completed(futures), total=len(futures), desc=f"Progress ({engine})"):
                    result = future.result()
                    if result:
                        results.append(result)
                    time.sleep(random.uniform(0.5, 1.5))  # Shorter random delay to speed up processing

            if results:
                self.logger.info(f"Search on {engine} completed successfully!")
                return results
            else:
                self.logger.warning(f"No results found on {engine}.")
                return []

        except requests.exceptions.RequestException as e:
            self.logger.error(f"An error occurred during the search on {engine}: {e}")
            return []

    def analyze_content(self, page_content: BeautifulSoup, query: str) -> Dict[str, any]:
        types_keywords = {
            "forum": ["forum", "board", "community"],
            "news": ["news", "breaking", "headline"]
        }
        text_content = page_content.get_text()
        detection_result = self.detection_handler.enhanced_detection(text_content, query, types_keywords)
        return detection_result

    def save_page_contents(self, engine: str, index: int, page_content: BeautifulSoup):
        with open('page-contents.log', 'a', encoding='utf-8') as f:
            f.write(f"=== Page Content from {engine} - Page {index} ===\n")
            f.write(page_content.prettify() + "\n")
            f.write("="*50 + "\n")

    def print_results(self, results: Dict[str, List[BeautifulSoup]], query: str):
        if not results:
            self.logger.warning("No results found.")
            return

        self.logger.info(f"\n{'🔍'*10} Search Results {'🔍'*10}\n")

        for engine, pages in results.items():
            visited_links = set()
            result_count = 0

            self.logger.info(f"\nResults from {engine}:\n")

            for index, page_content in enumerate(pages):
                if page_content is None:
                    self.logger.warning("Received NoneType page_content, skipping.")
                    continue

                # Save HTML content to a file
                self.save_page_contents(engine, index, page_content)

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
                    detection_result = self.analyze_content(page_content, query)

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

if __name__ == "__main__":
    # Set up logging configuration
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Create a file handler for debug logs
    file_handler = logging.FileHandler('debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # Create a stream handler for console logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show info and higher level logs on console
    console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Create a file handler for page contents
    page_contents_handler = logging.FileHandler('page-contents.log', mode='w', encoding='utf-8')
    page_contents_handler.setLevel(logging.DEBUG)
    page_contents_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(page_contents_handler)

    banner = """
    ─────█─▄▀█──█▀▄─█─────
    ────▐▌──────────▐▌────   WebHound:🐕
    ────█▌▀▄──▄▄──▄▀▐█────  Your trusty digital hound
    ───▐██──▀▀──▀▀──██▌───  sniffing out data across the web!💻
    ──▄████▄──▐▌──▄████▄──
   ~~~~~~~~~~~~~~~~~~~~~~~~
 """
    print(colored(banner, 'cyan'))

    query = input(colored("🔍 Enter your query: ", "cyan"))

    engines_input = input(colored("Enter search engines separated by commas (e.g., Google, Bing, StartPage, DuckDuckGo) or press Enter to use all: ", "cyan"))
    if not engines_input.strip():
        engines = list(SEARCH_ENGINES.keys())  # Use all engines if no input is provided
    else:
        engines = [engine.strip() for engine in engines_input.split(',')]

    date_range = input(colored("Enter date range (optional, e.g., 'past 24 hours'): ", "cyan"))
    language = input(colored("Enter language code (optional, e.g., 'en'): ", "cyan"))
    country = input(colored("Enter country code (optional, e.g., 'US'): ", "cyan"))

    scraper = WebScraper()

    all_results = scraper.execute_search(query, engines, date_range, language, country)

    if all_results:
        scraper.print_results(all_results, query)
