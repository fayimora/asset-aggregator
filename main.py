import click, crawler
from utils import requests_html_reader
from jsonpickle import encode
import logging, time

LOG_FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger()


@click.command()
@click.option('--url', default='https://fayimora.com', help="The URL we want to crawl")
@click.option('--log', default=False, is_flag=True, help="If progress should be logged")
def crawl(url, log):
    c = crawler.Crawler(url, requests_html_reader, log_info=log)
    start_time = time.time()
    results = c.run()
    finish_time = time.time() - start_time
    json_string = encode(results, unpicklable=False)
    print(json_string) # print resulting json to STDOUT
    logger.info("--- %s seconds ---" % (finish_time))

if __name__ == '__main__':
    crawl()
