# web-search-task

This project implements a simple **web crawler** in Python that can:

- Crawl internal pages from a given URL
- Index the textual content of those pages
- Perform keyword-based search on the crawled content

It also includes **unit tests** to ensure core functionalities are working correctly.

## Features

- Crawls HTML pages and follows internal links
- Builds a searchable index of page text
- Supports keyword search
- Error-handling for network and parsing issues
- Unit tests using `unittest` and `mock`

## Requirements

- Python 3.7+
- `requests`
- `beautifulsoup4`

Install dependencies with:

```bash
python -m pip install requests beautifulsoup4
```

## 🧪 Running the Tests

To run unit tests:

```bash
python -m unittest test_web_crawler.py
```

## Running the code

run `main.py` using the command:

```bash
python main.py
```

You can modify the `start_url` and `keyword` inside the `main()` function:

```python
def main():
    crawler = WebCrawler()
    start_url = "https://example.com"  # Replace with your own domain
    crawler.crawl(start_url)

    keyword = "test"  # 🔍 Keyword to search
    results = crawler.search(keyword)
    crawler.print_results(results)
```
