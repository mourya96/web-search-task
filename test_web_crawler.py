import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import requests
from main import WebCrawler  # assuming you moved the class to web_crawler.py

class WebCrawlerTests(unittest.TestCase):

    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        html = '''
        <html><body>
            <h1>Title</h1>
            <a href="/about">About</a>
            <a href="https://external.com">External</a>
        </body></html>
        '''
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertIn("https://example.com/about", crawler.visited)
        self.assertNotIn("https://external.com", crawler.visited)

    @patch('requests.get')
    def test_crawl_error_logged(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")
        crawler = WebCrawler()

        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            crawler.crawl("https://example.com")
            self.assertIn("Error crawling https://example.com: Test Error", fake_out.getvalue())

    @patch('requests.get')
    def test_crawl_invalid_url(self, mock_get):
        mock_get.side_effect = requests.exceptions.InvalidURL("Invalid URL")
        crawler = WebCrawler()

        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            crawler.crawl("ht!tp://bad-url")
            self.assertIn("Error crawling ht!tp://bad-url: Invalid URL", fake_out.getvalue())

    def test_search_match_and_no_match(self):
        crawler = WebCrawler()
        crawler.index = {
            "page1": "contains the keyword",
            "page2": "irrelevant content"
        }
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

        results = crawler.search("notfound")
        self.assertEqual(results, [])

    def test_print_results_output(self):
        crawler = WebCrawler()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            crawler.print_results(["http://test.com"])
            self.assertIn("Search results:", mock_out.getvalue())
            self.assertIn("- http://test.com", mock_out.getvalue())

    def test_print_no_results_output(self):
        crawler = WebCrawler()
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            crawler.print_results([])
            self.assertIn("No results found.", mock_out.getvalue())

    @patch('requests.get')
    def test_page_with_no_links(self, mock_get):
        html = '<html><body><p>Just text, no links.</p></body></html>'
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertEqual(len(crawler.visited), 1)

    @patch('requests.get')
    def test_circular_links(self, mock_get):
        html1 = '''
        <html><body><a href="https://example.com/page2">Page 2</a></body></html>
        '''
        html2 = '''
        <html><body><a href="https://example.com">Back</a></body></html>
        '''
        responses = {
            "https://example.com": html1,
            "https://example.com/page2": html2
        }

        def side_effect(url, *args, **kwargs):
            response = MagicMock()
            response.text = responses[url]
            return response

        mock_get.side_effect = side_effect

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.visited)
        self.assertIn("https://example.com/page2", crawler.visited)
        self.assertEqual(len(crawler.visited), 2)

    @patch('requests.get')
    def test_duplicate_links(self, mock_get):
        html = '''
        <html><body>
            <a href="/about">About</a>
            <a href="/about">About Again</a>
        </body></html>
        '''
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # /about should be crawled only once
        self.assertIn("https://example.com/about", crawler.visited)
        self.assertEqual(len(crawler.visited), 2)

    @patch('requests.get')
    def test_timeout_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Timeout Error")

        crawler = WebCrawler()
        with patch('sys.stdout', new_callable=StringIO) as fake_out:
            crawler.crawl("https://example.com")
            self.assertIn("Timeout Error", fake_out.getvalue())

