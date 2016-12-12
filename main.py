import click
import crawler
from utils import requests_html_reader
from jsonpickle import encode


@click.command()
@click.option('--url', default='https://fayimora.com', help="The URL we want to crawl")
def crawl(url):
    c = crawler.Crawler(url, requests_html_reader)
    # import time
    # start_time = time.time()
    results = c.run()
    # finish_time = time.time() - start_time
    json_string = encode(results, unpicklable=False)
    print(json_string) # print resulting json to STDOUT
    # print("--- %s seconds ---" % (finish_time))

if __name__ == '__main__':
    crawl()
