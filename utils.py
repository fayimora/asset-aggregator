import requests
import codecs


def requests_html_reader(url):
    """This reader uses the requests library to fetch a page and get its markup
    url -- The page we want to read, e.g http://codinghorror.com
    """
    return requests.get(url).text


def test_html_reader(file_path):
    """This reader is use in test to open a local file and read its markup
    file_path -- The location of the file we want to read, e.g /opt/app/page.html
    """
    return codecs.open(file_path, encoding='utf-8').read()
