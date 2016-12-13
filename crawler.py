from parsel import Selector
from urlparse import urlparse, urljoin
import logging

LOG_FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger()

class Result(object):
    """Domain representing a single result"""
    def __init__(self, url, assets):
        self.url = url
        self.assets = assets


class Crawler(object):
    def __init__(self, url, html_reader, log_info=False):
        """ Sets the initial state of the crawler.
        url -- The full starting URL. This value must contain the protocol and domain.
                domain.tld will not be accepted but http://domain.tld will work fine
        html_reader -- The is the function that is used to fetch a page. There are many viable
                options out there this enables you to easily try them out. The function expect a url
                as a string and return the parsed document as a string.
                Signature: html_reader(string) -> string
        log_info -- boolean flag for logging. The crawler logs progress to the console if set to True
        """
        super(Crawler, self).__init__()
        self.url = str(url.split("#")[0])
        self.visited_sites = {} # make sure we dont visit a page more than once
        self.visit_queue = set([self.url]) # implemented as a set to avoid duplicates at all cost
        self.html_reader = html_reader
        if log_info:
            logger.setLevel(logging.INFO)


    def run(self):
        return self.parse_iter(self.url, [])


    # NOTE: This is a Recursive implementation of the crawler algorithm. Unfortunately, it can only be
    # used for smaller sites because python has a maxrecursion limit of 999. I had to re-write this as a
    # loop below in parse_iter
    # def parse_r(self, url, results): # this really should not be accesed from outside
    #     logger.info("Checking "+curr_url)
    #     if len(self.visit_queue) == 0: # no more pages to visit
    #         return results
    #
    #     if self.visited_sites.has_key(url): # this helps us avoid visiting a page more than once, site wide
    #         return self.parse_r(self.visit_queue.pop(), results)
    #
    #     self.visited_sites[url] = True
    #     html_doc = requests.get(url).text
    #
    #     logger.info("\tExtracting links...")
    #     child_pages = self.extract_links(html_doc)
    #     self.visit_queue = self.visit_queue.union(child_pages)
    #
    #     logger.info("\tExtracting assets...")
    #     page_assets = self.extract_asset_links(html_doc)
    #     new_result = Result(url=url, assets=page_assets)
    #     results.append(new_result)
    #
    #     return self.parse_r(self.visit_queue.pop(), results)


    def parse_iter(self, url, initial_results):
        """This function operates based on the Breadth First Search algorithm. Given a url and a set of initial results,
        it fetches the assets in that url, acccumulates child pages in the same page and
        """
        results = initial_results[:] # dont mutate the initial results
        while len(self.visit_queue) > 0:
            curr_url = self.visit_queue.pop()
            logger.info("Checking "+curr_url)

            if self.visited_sites.has_key(curr_url): # don't visit a node more than once
                continue

            self.visited_sites[curr_url] = True

            # make sure page is reachable
            try:
                html_doc = self.html_reader(curr_url)
            except Exception as e: # NOTE: we can make this more robust by having the readers throw custom exceptions
                continue

            logger.info("\tExtracting links...")
            child_pages = self.extract_links(html_doc)
            self.visit_queue = self.visit_queue.union(child_pages)

            logger.info("\tExtracting assets...")
            page_assets = self.extract_asset_links(html_doc)
            new_result = Result(url=curr_url, assets=page_assets)
            results.append(new_result)

        return results


    def extract_links(self, html_doc):
        """Helper function for extraction a type of asset from a document
        html_doc -- the document where links will be extracted from
        """
        sel = Selector(html_doc)
        links = set([])
        for tag in sel.css('a'):
            link = tag.xpath('@href').extract_first()
            link = self.build_url(link) # build full url with protocol and domain

            # stay within the domain and http protocol
            if (self.should_visit_url(link)):
                links.add(link)
        return links


    def should_visit_url(self, url):
        """This function ensures that the url parameter is a subset of our base domain.
        It also ensures that we only follow links on the http or https protocol
        """
        parsed_url = urlparse(url)
        parsed_base_url = urlparse(self.url)
        is_http_protocol = parsed_url.scheme.startswith('http')
        netloc_within_domain = parsed_base_url.netloc == parsed_url.netloc or parsed_url.netloc == ''
        return is_http_protocol and netloc_within_domain


    def build_url(self, path):
        """Convert the path into a full URL. If path is a full URL, it remains unchanged
        path -- path/url that needs to be completed
        """
        # domain = base_url.split("#")[0]
        return urljoin(self.url, path)


    def extract_asset_links(self, html_doc):
        """Extract a list of assets for the given html_doc.
        html_doc -- a string/unicode representation of the html page
        """
        sel = Selector(html_doc)
        assets = set([])

        logger.info("\t\tExtracting images...")
        images = self.extract_assets(sel.css('img'), '@src')

        logger.info("\t\tExtracting stylesheets...")
        stylesheets = self.extract_assets(sel.css('link'), '@href')

        logger.info("\t\tExtracting scripts...")
        scripts = self.extract_assets(sel.css('script'), '@src')

        logger.info("\t\tMerging assets...")
        assets = images.union(stylesheets).union(scripts)

        return assets


    def extract_assets(self, selectors, xpath_query):
        """Helper function for extraction a type of asset from a page
        selectors -- list of document selectors that will be queried
        xpath_query -- the query that will be used by xpath to extract values
        """
        results = set([])
        for selector in selectors:
            asset = selector.xpath(xpath_query).extract_first()
            if not asset: # ignore inline sheets and scripts
                continue
            results.add(self.build_url(asset))
        return results
