#py3
import twitter
import logging
import csv
import os
from dotenv import load_dotenv
import GetOldTweets-python


def _config():
    # python -m
    # you need a .env file under current working directory, with content like CONSUMER_KEY=youe_key
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    api = twitter.Api(consumer_key=os.environ.get('CONSUMER_KEY'),
                      consumer_secret=os.environ.get('CONSUMER_SECRET'),
                      access_token_key=os.environ.get('ACCESS_TOKEN_KEY'),
                      access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')
                      )
    return api


# return a list
def _search():
    api = _config()
    query = 'q=pepsi%20&lang=en&count=10&until=2018-09-28'
    results = api.GetSearch(raw_query=query)

    web = 'l=en&q=pepsi%20since%3A2013-03-01%20until%3A2013-03-03'
    # results = api.GetSearch(raw_query="q=twitter%20&lang=en&result_type=recent&since=2014-07-19&count=10")
    # results = api.GetSearch(raw_query=web)
    return results


def _output():
    output_path = './output/'
    output_file = 'tweet.csv'
    csv_file = open(output_path + output_file, 'a+')
    logging.basicConfig(level=logging.DEBUG if False else logging.INFO, format='[%(asctime)s] - %(levelname)s - %(message)s')
    logging.info('Files is created under %s%s' % (output_path, output_file))
    writer = csv.writer(csv_file)
    results = _search()
    for index, text in enumerate(results):
        writer.writerow([index, [text]])


def init():
    # _config()
    # _search()
    _output()


# init()
