# WebHound 🚀

> **UPCOMING:** An update is currently under development—WebHound will soon feature a GUI, but you can still access the current command-line release! The client version will also be improved, but that update will follow the WebHound GUI.

> This project will likely be the 4th of 5 tools for the CT Window of Odinova.

![WebHound Logo](img/webhound.jpeg)

WebHound is a Python-powered command-line tool that brings efficiency and style to your web searches. Like a true web hound, it sniffs out and fetches data from a variety of search engines, detects social platforms and forums, and organizes the results with flair. All from the comfort of your terminal, WebHound ensures a comprehensive search experience with detailed logging and robust error handling. 🌐🔍✨

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
