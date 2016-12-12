FROM python:2.7.12-onbuild

RUN mkdir -p /asset-aggregator
WORKDIR /asset-aggregator
COPY . /asset-aggregator

CMD python main.py --url https://gocardless.com
