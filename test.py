import unittest
from crawler import Crawler
from utils import requests_html_reader, test_html_reader


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.domain = 'http://localhost:8090'
        self.crawler = Crawler(self.domain, test_html_reader)
        self.test_html_doc_page1 = test_html_reader('./test-data/page1.html')
        self.test_html_doc_page2 = test_html_reader('./test-data/page2.html')


    def test_build_url(self):
        built_url = self.crawler.build_url('/page1')
        built_url2 = self.crawler.build_url(self.domain+'/page2')

        self.assertEqual(built_url, self.domain+'/page1')
        self.assertEqual(built_url2, self.domain+'/page2')


    def test_should_visit_url(self):
        should_visit_github = self.crawler.should_visit_url('https://github.com')
        should_visit_twitter = self.crawler.should_visit_url('https://twitter.com')
        should_visit_local = self.crawler.should_visit_url(self.domain)

        self.assertFalse(should_visit_github)
        self.assertFalse(should_visit_twitter)
        self.assertTrue(should_visit_local)


    def test_extract_links(self):
        page1_links = self.crawler.extract_links(self.test_html_doc_page1)
        page2_links = self.crawler.extract_links(self.test_html_doc_page2)

        # test that we get the right number of links
        self.assertEqual(len(page1_links), 2)
        self.assertEqual(len(page2_links), 1)

        # test that we get the full URL for each links
        self.assertTrue(self.domain+'/page1.html' in page1_links)
        self.assertTrue(self.domain+'/page2.html' in page1_links)

        # test that we did not follow the github or wiki links
        self.assertFalse('https://github.com/fayimora' in page2_links)
        self.assertFalse('https://en.wikipedia.org/wiki/William_Shakespeare' in page2_links)


    def test_extract_asset_links(self):
        page2_assets = self.crawler.extract_asset_links(self.test_html_doc_page2)

        # we should get 4 assets back
        self.assertEqual(len(page2_assets), 4)


    def test_parse_iter(self):
        crawler = Crawler(self.domain, requests_html_reader)
        results = crawler.parse_iter(self.domain, [])

        # make sure we get a list back
        self.assertTrue(type(results), list)

        # there should be three pages in the result, index, page and page2
        self.assertTrue(len(results), 3)
        expected_urls = [self.domain, self.domain+'/page1.html', self.domain+'/page2.html']
        for i, result in enumerate(results):
            self.assertTrue(result.url in expected_urls)
            # self.assert()



if __name__ == '__main__':
    unittest.main()
