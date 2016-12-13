import requests
import codecs


def requests_html_reader(url):
    """This reader uses the requests library to fetch a page and get its markup"""
    return requests.get(url).text


def test_html_reader(url):
    """This reader is use in test to open a local file and read its markup"""
    return codecs.open(url, encoding='utf-8').read()
