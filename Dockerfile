FROM python:2.7-onbuild

RUN mkdir -p /asset-aggregator
WORKDIR /asset-aggregator
COPY . /asset-aggregator

CMD python main.py --log --url https://gocardless.com
