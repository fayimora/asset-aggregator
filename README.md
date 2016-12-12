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



# How to run tests
