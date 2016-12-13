# Problem

We would like you to write a simple (single-threaded) web crawler.
Given a starting URL, it should visit every reachable page under that domain.
For each page, it should determine the URLs of every static asset (images, javascript, stylesheets) on that page.
The crawler should output to STDOUT in JSON format listing the URLs of every static asset, grouped by page.

For example:
```json
[
  {
    "url": "http://www.example.org",
    "assets": [
      "http://www.example.org/image.jpg",
      "http://www.example.org/script.js"
    ]
  },
  {
    "url": "http://www.example.org/about",
    "assets": [
      "http://www.example.org/company_photo.jpg",
      "http://www.example.org/script.js"
    ]
  },
]
```

# How to run
*NOTE:* Python 2.7 must be installed.

First install dependencies with `pip install -r requirements.txt`.

To run with default url, execute `python main.py` in the terminal. This will run the crawler on `http://fayimora.com`.

To run the crawler with a custom url, pass in a url flag. For example, to run with `https://gocardless.com`, execute `python main.py --url https://gocardless.com`.

*NOTE:* The URL specified must contain the protocol and full domain name. `example.com` is invalid however, `http://example.com` is valid.

### Logging
When running on a large website, it can be boring staring at the terminal with no indication of what's happening. To fix this, you can enable logging with the `--log` flag. Example run with logging: `python main.py --log --url https://gocardless.com`


### Running in isolation
Love containers? Don't want to install dependencies on your computer? Docker has you covered.

First, you build the container by running the following commands in the rot folder of the project.

- `docker build -t fayimora/asset-aggregator .` (~81mb download on first run)
- `docker run fayimora/asset-aggregator`

Please note that the image name `fayimora/asset-aggregator` above can and probably should be changed to something else.

The docker container runs the crawler on `https://gocardless.com` with logging enabled. To disable this, edit the `Dockerfile` in the project and remove the `--log` flag. You can also edit the URL in the Dockerfile.


# How to run tests
*NOTE:* dependencies must be installed first. See above section.
execute `python test.py`
