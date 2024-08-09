# WebHound 🚀

> **UPCOMING:** An update is currently under development—WebHound will soon feature a GUI, but you can still access the current command-line release!

> This project will likely be the 4th of 5 tools for the CT Window of Odinova.

![WebHound Logo](img/webhound.jpeg)

**WebHound** is your ultimate Python-powered command-line companion, designed to turbocharge your web searching experience with both efficiency and pizzazz! Imagine a digital sleuth with a nose for data, sniffing through the vast expanse of the internet, sniffing out valuable insights from a diverse array of search engines. Whether you're diving into Google’s treasure trove, peering through DuckDuckGo’s privacy lens, or unraveling Bing's web, WebHound has got you covered.

But that’s not all—this tool is more than just a search engine aggregator. It’s a seasoned OSINT detective with the knack for uncovering social platforms, forums, and news sites. With WebHound, you can effortlessly track down mentions of your query across titles and URLs, giving you a front-row seat to the digital chatter happening around your topic of interest.

WebHound’s charm lies not just in its comprehensive search capabilities but in how it presents the results. Expect colorful, organized output that makes scanning through search results as delightful as a game of treasure hunt. Detailed logging ensures you never miss a beat, while robust error handling means you can focus on your investigative work without worrying about unexpected hiccups.

So gear up, and let WebHound transform your terminal into a dynamic data-hunting machine. Dive into a world where search results are not just fetched but presented with flair and precision. Happy hunting! 🌐🔍✨

## Search Engines Covered:

- **Google**
- **DuckDuckGo**
- **StartPage**
- **Bing**
- **Ask**

## Detection Methods:

- **Social Platform Detection:** Identifies popular social platforms such as Facebook, Twitter, Instagram, and LinkedIn within search results.
- **Forum Detection:** Detects forums and community boards by analyzing keywords like "forum," "board," and "community."
- **News Detection:** Recognizes news sites and articles based on keywords like "news," "breaking," and "headline."
- **Query Mentions:** Detects occurrences of the search query within titles, URLs, and content.

## Features:

- **Multi-Engine Search:** Conduct searches across ten popular engines simultaneously to gather a wide range of results.
- **Colorful Output:** Presents search results in a visually appealing manner with highlighted titles, URLs, and descriptions for quick and easy reading.
- **Efficient Execution:** Utilizes multithreading to accelerate the search process, providing results in a fraction of the usual time.
- **User-Friendly Interface:** A simple and intuitive command-line interface for an effortless user experience.
- **Social Platform Detection:** Enhanced detection of social platforms and forums within search results.
- **Query Mentions:** Detects occurrences of the query in titles, URLs, and content to highlight relevant results.
- **Error Handling:** Robust error handling with retry logic to ensure reliable operation.
- **Result Logging:** Logs detailed page contents and search results to files, including:
  - **Page Contents Log:** Stores the raw HTML content of each search result page.
  - **Error Log:** Captures and records any issues encountered during the search process.
  - **Interaction Log:** Records interactions, including button clicks and window openings.

 ## Installation & Usage:

``` git clone https://github.com/AnonCatalyst/WebHound && cd WebHound```

``` python3 install.py```

``` python3 webhound.py```
