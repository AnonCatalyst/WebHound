import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from termcolor import colored
from urllib.parse import quote
from fake_useragent import UserAgent

SEARCH_ENGINES = {
    "Google": "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/html/?q=",
    "Bing": "https://www.bing.com/search?q=",
}

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()

    def make_request(self, url):
        headers = {"User-Agent": self.ua.random}
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            print(colored(f"✅ Request to {url} successful. User-Agent: {headers['User-Agent']} 🚀", "green"))
            return BeautifulSoup(response.text, "html.parser")
        except requests.exceptions.RequestException as e:
            print(colored(f"❌ Error making request to {url}: {e} 🚨", "red"))
            return None

    def execute_search(self, query, engine):
        url = SEARCH_ENGINES.get(engine)
        if url:
            print(colored(f"🔄 Switching to {engine}... 🔄", "cyan"))
            time.sleep(2)

            print(colored(f"🔍 Searching on {engine}... 🔍", "cyan"))
            start_time = time.time()

            try:
                with ThreadPoolExecutor(max_workers=5) as executor:
                    results = list(executor.map(self.make_request, [f"{url}{quote(query)}&start={i}" for i in range(1, 31, 10)]))

                end_time = time.time()
                print(colored(f"⏰ Time Elapsed: {end_time - start_time:.2f} seconds ⏰", "cyan"))

                return results

            except Exception as e:
                print(colored(f"❌ An error occurred during the search on {engine}: {e} 🚨", "red"))
                return []

    def print_results(self, results, engine):
        if not results:
            print(colored(f"No results from {engine} 🤷‍♂️", "white"))
            return

        print(colored(f"\n{'🔍'*10} Results from {engine} {'🔍'*10}\n", "cyan"))
        for result in results:
            self.print_result(result)

    def print_result(self, result):
        try:
            for item in result.select("div.tF2Cxc, div.result, li.b_algo"):
                title = item.select_one("h2, h3")
                link = item.find("a")["href"]
                description = item.select_one("div.IsZvec, p")

                title_text = title.text.strip().replace(query, colored(query, "red", attrs=['bold'])) if title else "Title not available"
                link_text = colored(link, "cyan").replace(query, colored(query, "red", attrs=['bold'])) if link else "Link not available"
                description_text = description.text.strip().replace(query, colored(query, "red", attrs=['bold'])) if description else "Description not available"

                print(colored(f"\n{'🔹'*10} Result {'🔹'*10}\n"
                              f"{'📖 Title:':<15} {colored(title_text, 'yellow')}\n"
                              f"{'🌐 URL:':<15} {link_text}\n"
                              f"{'📝 Description:':<15} {colored(description_text, 'green')}\n"
                              f"{'🔹'*40}\n", "white"))

        except Exception as e:
            print(colored(f"❌ An error occurred while processing a search result: {e} 🚨", "red"))

if __name__ == "__main__":
    query = input(colored("🔍 Enter your query: ", "cyan"))
    scraper = Scraper()

    all_results = []
    for engine in SEARCH_ENGINES:
        results = scraper.execute_search(query, engine)
        all_results.extend(results)

    scraper.print_results(all_results, "All Engines")
