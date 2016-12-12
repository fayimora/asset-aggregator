import requests
import codecs


def requests_html_reader(url):
    return requests.get(url).text


def test_html_reader(url):
    return codecs.open(url, encoding='utf-8').read()
